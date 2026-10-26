"""CSV-Import und -Export fuer Beitragkarten (Article), Termine (Event),
Sektionen (Section) sowie Nutzer mit Profil (User + Profile).

Ein Export-/Import-Ordner enthaelt bis zu vier CSV-Dateien (articles.csv,
sections.csv, events.csv, users.csv) sowie die darin per Dateiname
referenzierten Bilder und Profilfotos im selben Ordner. Format wie in flask-crm: Semikolon als Trennzeichen, UTF-8
mit BOM (damit Excel Umlaute korrekt anzeigt). Datum/Uhrzeit in lokaler Zeit
(Europe/Berlin) als "JJJJ-MM-TT HH:MM"; gespeichert wird wie in der Administration in UTC.

Aufruf im web-Container:
    python csv_transfer.py export <ordner>
    python csv_transfer.py import <ordner> [--user admin]

In der Administration gibt es dieselben Funktionen als ZIP-Download (/export) und
als Ordner-Upload (/import).
"""

import csv
import html
import io
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from uuid import uuid4
from zoneinfo import ZoneInfo

from PIL import Image, ImageOps
from flask import current_app

from models import (
    db, Article, Section, Event, Profile, User, PROFILE_FUNCTIONS, ROLES, ROLE_MEMBER,
    VISIBILITY_CHOICES, VISIBILITY_MEMBERS,
)
import images as image_tools

BERLIN = ZoneInfo("Europe/Berlin")
DELIMITER = ";"
ENCODING = "utf-8-sig"
DATETIME_FORMAT = "%Y-%m-%d %H:%M"

ARTICLE_FILE = "articles.csv"
ORDER_STEP = 10  # Abstand der Ordnungsnummern beim Import
SECTION_FILE = "sections.csv"
EVENT_FILE = "events.csv"
USER_FILE = "users.csv"
FILES = (ARTICLE_FILE, SECTION_FILE, EVENT_FILE, USER_FILE)

# Spaltenreihenfolge der CSV-Dateien. "id" wird nur zur Orientierung
# exportiert und beim Import ignoriert (es werden immer neue Datensaetze
# angelegt).
# Beitraege: "image_fit" = auto (oder leer) / cover / contain / blur; das Bild
# wird nie zugeschnitten, nur verkleinert (siehe images.py).
# Sektionen: "image_orientation" ist wie im Upload-Formular kein Modellfeld:
# leer = Bild unveraendert uebernehmen, "landscape"/"portrait" = wie beim
# Upload in der Administration zuschneiden und als WebP speichern.
ARTICLE_COLUMNS = [
    "id", "title", "description", "body", "image_filename", "image_fit",
    "on_index", "on_consulting", "on_academy", "on_stories", "is_banner",
    "order_number", "col_size", "updated_at",
]
SECTION_PAGES = ("index", "consulting", "academy")
SECTION_COLUMNS = [
    "id", "kicker", "title", "description", "body", "image_filename",
    "image_orientation", "image_position",
    "on_index", "slot_index_index", "slot_position_index",
    "on_consulting", "slot_index_consulting", "slot_position_consulting",
    "on_academy", "slot_index_academy", "slot_position_academy",
    "updated_at",
]
EVENT_COLUMNS = [
    "id", "title", "category", "subtitle", "all_day", "starts_at", "ends_at",
    "location", "updated_at",
]

# Nutzer und Profil in einer Zeile (1:1). Profilspalten bleiben leer, wenn
# ein Konto kein Profil hat (z. B. der Admin aus init_db.py).
# password_hash ist der bcrypt-Hash: damit bleiben Passwoerter nach einem
# Neuaufbau der Datenbank gueltig. Leer = Konto ohne bekanntes Passwort
# (Person setzt es ueber "Passwort vergessen"). functions = Schluessel durch
# Komma getrennt (coach, smeo_staff). photo_filename = Bilddatei im Ordner.
USER_COLUMNS = [
    "id", "username", "email", "role", "is_active", "password_hash",
    "created_at", "last_login_at",
    "first_name", "last_name", "display_name", "organization", "job_title",
    "functions", "city", "phone", "bio", "website", "photo_filename",
    "email_visibility", "phone_visibility", "bio_visibility", "profile_updated_at",
]
PROFILE_COLUMNS = USER_COLUMNS[8:]

TRUE_VALUES = {"1", "true", "ja", "j", "yes", "y", "x", "wahr"}
FALSE_VALUES = {"", "0", "false", "nein", "n", "no", "falsch"}


class CsvImportError(Exception):
    """Fehler beim Import; enthaelt alle gefundenen Probleme als Liste."""

    def __init__(self, errors):
        self.errors = errors
        super().__init__("\n".join(errors))


# --------------------------------------------------------------------------
# Hilfsfunktionen
# --------------------------------------------------------------------------

def _format_datetime(value):
    if value is None:
        return ""
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(BERLIN).strftime(DATETIME_FORMAT)


def _parse_datetime(value):
    # Lokale Zeit (Europe/Berlin) -> timezone-aware UTC. Akzeptiert
    # "JJJJ-MM-TT HH:MM", mit Sekunden, mit "T" als Trenner oder nur das Datum.
    value = (value or "").strip().replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            naive = datetime.strptime(value, fmt)
        except ValueError:
            continue
        return naive.replace(tzinfo=BERLIN).astimezone(timezone.utc)
    raise ValueError(f"ungültiges Datum „{value}“ (erwartet JJJJ-MM-TT HH:MM)")


def _format_bool(value):
    return "1" if value else "0"


def _parse_bool(value):
    v = (value or "").strip().lower()
    if v in TRUE_VALUES:
        return True
    if v in FALSE_VALUES:
        return False
    raise ValueError(f"ungültiger Ja/Nein-Wert „{value}“ (erwartet 1 oder 0)")


def _parse_int(value, default=None):
    v = (value or "").strip()
    if not v:
        return default
    try:
        return int(v)
    except ValueError:
        raise ValueError(f"ungültige Zahl „{value}“")


def _text(row, key):
    v = (row.get(key) or "").strip()
    return v or None


# --------------------------------------------------------------------------
# Bereinigung von HTML beim Import
# --------------------------------------------------------------------------
# Texte werden auf der Website mit "white-space: pre-line" ausgegeben, d. h.
# Zeilenumbrueche im Text sind sichtbar. HTML fuer Absaetze und Umbrueche ist
# deshalb unnoetig: <p>, <div>, Ueberschriften, Listen und <br> werden beim
# Import durch Zeilenumbrueche ersetzt, alle uebrigen Tags entfernt. Erhalten
# bleiben nur Hervorhebungen und Links.
KEEP_TAGS = {"strong": "strong", "b": "strong", "em": "em", "i": "em", "a": "a"}
PARAGRAPH_TAGS = {"p", "div", "section", "article", "blockquote", "ul", "ol",
                  "table", "h1", "h2", "h3", "h4", "h5", "h6"}
DROP_CONTENT_TAGS = {"script", "style", "head", "title"}
LINK_PROTOCOLS = ("http://", "https://", "mailto:", "tel:", "/", "#")


class _HtmlCleaner(HTMLParser):
    def __init__(self, collapse_whitespace):
        super().__init__(convert_charrefs=True)
        self.collapse = collapse_whitespace
        self.out = []
        self.open_tags = []
        self.skip_depth = 0

    def _break(self, newlines):
        self.out.append("\x00" * newlines)  # Platzhalter, spaeter aufgeloest

    def handle_starttag(self, tag, attrs):
        if tag in DROP_CONTENT_TAGS:
            self.skip_depth += 1
            return
        if tag == "br":
            self._break(1)
        elif tag in PARAGRAPH_TAGS:
            self._break(2)
        elif tag == "li":
            self._break(1)
            self.out.append("• ")
        elif tag == "tr":
            self._break(1)
        elif tag in KEEP_TAGS:
            name = KEEP_TAGS[tag]
            if name == "a":
                href = (dict(attrs).get("href") or "").strip()
                if not href.lower().startswith(LINK_PROTOCOLS):
                    self.open_tags.append(None)  # Link ohne gueltiges Ziel: nur Text
                    return
                extra = ""
                if dict(attrs).get("target") == "_blank":
                    extra = ' target="_blank" rel="noopener"'
                self.out.append(f'<a href="{html.escape(href)}"{extra}>')
            else:
                self.out.append(f"<{name}>")
            self.open_tags.append(name)

    def handle_startendtag(self, tag, attrs):
        if tag == "br":
            self._break(1)

    def handle_endtag(self, tag):
        if tag in DROP_CONTENT_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if tag in PARAGRAPH_TAGS:
            self._break(2)
        elif tag in ("td", "th"):
            self.out.append(" ")
        elif tag in KEEP_TAGS:
            name = KEEP_TAGS[tag]
            # zum passenden offenen Tag schliessen (verschachtelte Fehler tolerieren)
            if name in self.open_tags or (name == "a" and None in self.open_tags):
                while self.open_tags:
                    top = self.open_tags.pop()
                    if top:
                        self.out.append(f"</{top}>")
                    if top == name or (name == "a" and top is None):
                        break

    def handle_data(self, data):
        if self.skip_depth:
            return
        data = data.replace("\xa0", " ")
        if self.collapse:
            data = re.sub(r"\s+", " ", data)
        self.out.append(html.escape(data, quote=False))

    def result(self):
        for top in reversed(self.open_tags):
            if top:
                self.out.append(f"</{top}>")
        text = "".join(self.out)
        # Zeilenumbruch-Platzhalter: mehrere hintereinander -> max. eine Leerzeile
        text = re.sub(r"\x00+", lambda m: "\n" if len(m.group()) == 1 else "\n\n", text)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n[ \t]+", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Leere Hervorhebungen entfernen (<strong></strong> nach dem Bereinigen)
        text = re.sub(r"<(strong|em)>\s*</\1>", "", text)
        return text.strip()


def clean_html(value):
    """Entfernt unnoetiges HTML aus einem Inhaltstext (siehe oben). Reiner
    Text ohne Tags bleibt bis auf Leerraum am Rand unveraendert."""
    if not value:
        return value
    looks_like_html = re.search(r"<\s*/?\s*(p|br|div|h[1-6]|li|ul|ol|table)\b", value, re.I)
    cleaner = _HtmlCleaner(collapse_whitespace=bool(looks_like_html))
    cleaner.feed(value)
    cleaner.close()
    text = cleaner.result()
    # "##" (Grenze Anreisser/Weiterlesen) in eine eigene Zeile ohne Leerraum drumherum
    text = re.sub(r"\s*##\s*", "\n##\n", text, count=1)
    return text.strip() or None


def plain_text(value):
    """Fuer einzeilige Felder (Titel, Untertitel, Kicker, Ort): alle Tags
    entfernen, Entities aufloesen, Leerraum zusammenfassen."""
    if not value:
        return value
    text = re.sub(r"<[^>]+>", " ", value)
    text = html.unescape(text).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip() or None


def _rich(row, key):
    return clean_html(_text(row, key))


def _plain(row, key):
    return plain_text(_text(row, key))


def _write_csv(path, columns, rows):
    with open(path, "w", encoding=ENCODING, newline="") as f:
        writer = csv.writer(f, delimiter=DELIMITER)
        writer.writerow(columns)
        writer.writerows(rows)


def _read_csv(path):
    with open(path, encoding=ENCODING, newline="") as f:
        content = f.read()
    try:
        dialect = csv.Sniffer().sniff(content[:8192], delimiters=";,\t")
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = DELIMITER
    reader = csv.DictReader(io.StringIO(content, newline=""), delimiter=delimiter)
    fieldnames = [(name or "").strip() for name in (reader.fieldnames or [])]
    reader.fieldnames = fieldnames
    # line_num ist die Zeilennummer in der Datei (bei mehrzeiligen Texten die
    # letzte Zeile des Datensatzes) - fuer Fehlermeldungen.
    rows = []
    for row in reader:
        rows.append((reader.line_num, row))
    return fieldnames, rows


def _upload_folder():
    return os.path.join(current_app.root_path, current_app.config["UPLOAD_FOLDER"])


# --------------------------------------------------------------------------
# Export
# --------------------------------------------------------------------------

def export_to_dir(target_dir):
    """Schreibt alle Beitragkarten, Sektionen und Termine als CSV in target_dir und
    kopiert die referenzierten Bilder dazu. Liefert (Anzahlen, Hinweise)."""
    os.makedirs(target_dir, exist_ok=True)
    upload_folder = _upload_folder()
    warnings = []
    images = set()

    articles = Article.query.order_by(Article.order_number.asc(), Article.id.asc()).all()
    _write_csv(os.path.join(target_dir, ARTICLE_FILE), ARTICLE_COLUMNS, [
        [c.id, c.title, c.description or "", c.body, c.image_filename or "", c.image_fit,
         _format_bool(c.on_index), _format_bool(c.on_consulting),
         _format_bool(c.on_academy), _format_bool(c.on_stories),
         _format_bool(c.is_banner), c.order_number, c.col_size,
         _format_datetime(c.updated_at)]
        for c in articles
    ])
    images.update(c.image_filename for c in articles if c.image_filename)

    sections = Section.query.order_by(Section.id.asc()).all()
    section_rows = []
    for s in sections:
        row = [s.id, s.kicker or "", s.title, s.description or "", s.body,
               s.image_filename or "", "", s.image_position]
        for page in SECTION_PAGES:
            slot = getattr(s, f"slot_index_{page}")
            pos = getattr(s, f"slot_position_{page}")
            row += [_format_bool(getattr(s, f"on_{page}")),
                    "" if slot is None else slot, "" if pos is None else pos]
        row.append(_format_datetime(s.updated_at))
        section_rows.append(row)
    _write_csv(os.path.join(target_dir, SECTION_FILE), SECTION_COLUMNS, section_rows)
    images.update(s.image_filename for s in sections if s.image_filename)

    events = Event.query.order_by(Event.starts_at.asc(), Event.id.asc()).all()
    _write_csv(os.path.join(target_dir, EVENT_FILE), EVENT_COLUMNS, [
        [e.id, e.title, e.category, e.subtitle or "", _format_bool(e.all_day),
         _format_datetime(e.starts_at), _format_datetime(e.ends_at),
         e.location, _format_datetime(e.updated_at)]
        for e in events
    ])

    # Nutzer mit Profil; Profilfotos liegen in data/uploads/avatars/ und
    # werden flach (nur Dateiname) in den Exportordner kopiert.
    users = User.query.order_by(User.id.asc()).all()
    user_rows = []
    photos = {}
    for u in users:
        row = [u.id, u.username, u.email or "", u.role, _format_bool(u.is_active),
               u.password_hash or "", _format_datetime(u.created_at), _format_datetime(u.last_login_at)]
        p = u.profile
        if p:
            photo = os.path.basename(p.photo_filename) if p.photo_filename else ""
            if photo:
                photos[photo] = p.photo_filename
            row += [p.first_name, p.last_name, p.display_name or "", p.organization or "",
                    p.job_title or "", ",".join(p.functions or []), p.city, p.phone or "",
                    p.bio or "", p.website or "", photo, p.email_visibility,
                    p.phone_visibility, p.bio_visibility, _format_datetime(p.updated_at)]
        else:
            row += [""] * len(PROFILE_COLUMNS)
        user_rows.append(row)
    _write_csv(os.path.join(target_dir, USER_FILE), USER_COLUMNS, user_rows)

    copied = 0
    for name in sorted(images):
        src = os.path.join(upload_folder, name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(target_dir, name))
            copied += 1
        else:
            warnings.append(f"Bild „{name}“ fehlt in data/uploads und wurde nicht exportiert.")
    copied_photos = 0
    for name, stored in sorted(photos.items()):
        src = os.path.join(upload_folder, stored)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(target_dir, name))
            copied_photos += 1
        else:
            warnings.append(f"Profilfoto „{stored}“ fehlt in data/uploads und wurde nicht exportiert.")

    counts = {"articles": len(articles), "sections": len(sections), "events": len(events),
              "users": len(users), "images": copied, "photos": copied_photos}
    return counts, warnings


# --------------------------------------------------------------------------
# Import
# --------------------------------------------------------------------------

class _ImageImporter:
    """Kopiert/konvertiert Bilder aus dem Importordner nach data/uploads und
    merkt sich die neuen Dateien, um sie bei einem Abbruch wieder zu entfernen."""

    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.upload_folder = _upload_folder()
        self.created = []
        self.cache = {}

    def check(self, name):
        # Nur reine Dateinamen im Importordner, keine Pfade.
        if os.path.basename(name) != name or name in (".", ".."):
            raise ValueError(f"Bildname „{name}“ darf keinen Pfad enthalten")
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
        if ext not in current_app.config["ALLOWED_EXTENSIONS"]:
            raise ValueError(f"Bild „{name}“ hat keinen erlaubten Dateityp")
        path = os.path.join(self.source_dir, name)
        if not os.path.isfile(path):
            raise ValueError(f"Bild „{name}“ liegt nicht im Importordner")
        try:
            with Image.open(path) as img:
                img.verify()
        except Exception:
            raise ValueError(f"„{name}“ ist keine lesbare Bilddatei")

    def store(self, name, orientation):
        key = (name, orientation)
        if key in self.cache:
            return self.cache[key]
        from views import (crop_to_aspect_ratio, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT,
                           PORTRAIT_WIDTH, PORTRAIT_HEIGHT)
        os.makedirs(self.upload_folder, exist_ok=True)
        src = os.path.join(self.source_dir, name)
        if orientation:
            width, height = ((PORTRAIT_WIDTH, PORTRAIT_HEIGHT) if orientation == "portrait"
                             else (LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT))
            new_name = f"{uuid4().hex}.webp"
            with Image.open(src) as img:
                img = crop_to_aspect_ratio(img.convert("RGB"), width, height)
                img = img.resize((width, height), Image.LANCZOS)
                img.save(os.path.join(self.upload_folder, new_name), "WEBP",
                         quality=85, method=6)
        else:
            new_name = f"{uuid4().hex}.{name.rsplit('.', 1)[-1].lower()}"
            shutil.copyfile(src, os.path.join(self.upload_folder, new_name))
        self.created.append(new_name)
        self.cache[key] = new_name
        return new_name

    def store_article(self, name, fit):
        # Beitragsbilder: nicht zuschneiden, nur verkleinern; Darstellung
        # (image_fit) bei "auto" anhand des Bildes waehlen (images.py).
        key = ("article", name, fit)
        if key in self.cache:
            return self.cache[key]
        new_name, final_fit = image_tools.save_article_image(
            os.path.join(self.source_dir, name), name, self.upload_folder, fit=fit
        )
        self.created.append(new_name)
        self.cache[key] = (new_name, final_fit)
        return new_name, final_fit

    def store_avatar(self, name):
        """Profilfoto wie beim Upload: quadratisch zuschneiden, EXIF entfernen,
        als WebP in data/uploads/avatars/ speichern."""
        from members import AVATAR_SIZE, AVATAR_SUBFOLDER
        key = ("avatar", name)
        if key in self.cache:
            return self.cache[key]
        os.makedirs(os.path.join(self.upload_folder, AVATAR_SUBFOLDER), exist_ok=True)
        with Image.open(os.path.join(self.source_dir, name)) as img:
            img.load()
            img = ImageOps.exif_transpose(img).convert("RGB")
            img = ImageOps.fit(img, (AVATAR_SIZE, AVATAR_SIZE), Image.LANCZOS, centering=(0.5, 0.4))
            new_name = f"{AVATAR_SUBFOLDER}/{uuid4().hex}.webp"
            img.save(os.path.join(self.upload_folder, new_name), "WEBP", quality=85, method=6)
        self.created.append(new_name)
        self.cache[key] = new_name
        return new_name

    def rollback(self):
        for name in self.created:
            try:
                os.remove(os.path.join(self.upload_folder, name))
            except OSError:
                pass


def _check_columns(filename, fieldnames, required, errors):
    missing = [c for c in required if c not in fieldnames]
    if missing:
        errors.append(f"{filename}: Spalte(n) fehlen: {', '.join(missing)}")
        return False
    return True


def _image_fields(row, images):
    name = _text(row, "image_filename")
    orientation = (_text(row, "image_orientation") or "").lower() or None
    if orientation not in (None, "landscape", "portrait"):
        raise ValueError(f"image_orientation „{orientation}“ muss leer, landscape oder portrait sein")
    if name:
        images.check(name)
    return name, orientation


def _parse_articles(path, images, errors):
    fieldnames, rows = _read_csv(path)
    if not _check_columns(ARTICLE_FILE, fieldnames, ["title", "body"], errors):
        return []
    parsed = []
    for line, row in rows:
        try:
            title, body = _plain(row, "title"), _rich(row, "body")
            if not title or not body:
                raise ValueError("title und body dürfen nicht leer sein")
            image = _text(row, "image_filename")
            if image:
                images.check(image)
            # image_orientation wird bei Beitraegen ignoriert; stattdessen
            # image_fit (leer = auto, siehe images.py).
            fit = (_text(row, "image_fit") or "auto").lower()
            if fit != "auto" and fit not in image_tools.FIT_VALUES:
                raise ValueError(f"image_fit „{fit}“ muss leer, auto, cover, contain oder blur sein")
            parsed.append({
                "title": title, "body": body,
                "description": _plain(row, "description"),
                "image": image, "fit": fit,
                "on_index": _parse_bool(row.get("on_index")),
                "on_consulting": _parse_bool(row.get("on_consulting")),
                "on_academy": _parse_bool(row.get("on_academy")),
                "on_stories": _parse_bool(row.get("on_stories")),
                "is_banner": _parse_bool(row.get("is_banner")),
                "order_number": _parse_int(row.get("order_number"), 0),
                "col_size": _text(row, "col_size"),
                "updated_at": _parse_datetime(row["updated_at"]) if _text(row, "updated_at") else None,
            })
        except ValueError as exc:
            errors.append(f"{ARTICLE_FILE} Zeile {line}: {exc}")
    banners = sum(1 for c in parsed if c["is_banner"])
    if banners > 1:
        errors.append(f"{ARTICLE_FILE}: Es darf höchstens ein Beitrag als Banner markiert sein ({banners} gefunden).")
    elif banners == 1 and Article.query.filter_by(is_banner=True).first():
        errors.append(f"{ARTICLE_FILE}: Es existiert bereits ein Banner – is_banner des importierten Beitrags auf 0 setzen oder das bestehende Banner vorher entfernen.")
    return parsed


def _parse_sections(path, images, errors):
    from views import PAGE_SLOT_COUNT
    fieldnames, rows = _read_csv(path)
    if not _check_columns(SECTION_FILE, fieldnames, ["title", "body"], errors):
        return []
    parsed = []
    for line, row in rows:
        try:
            title, body = _plain(row, "title"), _rich(row, "body")
            if not title or not body:
                raise ValueError("title und body dürfen nicht leer sein")
            image, orientation = _image_fields(row, images)
            position = (_text(row, "image_position") or "right").lower()
            if position not in ("left", "right"):
                raise ValueError(f"image_position „{position}“ muss left oder right sein")
            item = {
                "title": title, "body": body, "kicker": _plain(row, "kicker"),
                "description": _plain(row, "description"),
                "image": image, "orientation": orientation, "image_position": position,
                "updated_at": _parse_datetime(row["updated_at"]) if _text(row, "updated_at") else None,
                "pages": {},
            }
            for page in SECTION_PAGES:
                flag = _parse_bool(row.get(f"on_{page}"))
                slot = _parse_int(row.get(f"slot_index_{page}"))
                pos = _parse_int(row.get(f"slot_position_{page}"), 1)
                if slot is not None and not (1 <= slot <= PAGE_SLOT_COUNT[page]):
                    raise ValueError(f"slot_index_{page} muss zwischen 1 und {PAGE_SLOT_COUNT[page]} liegen")
                if slot is not None and not flag:
                    slot = None  # Slot ohne Haekchen wird ignoriert
                item["pages"][page] = (flag, slot, max(pos, 1))
            parsed.append(item)
        except ValueError as exc:
            errors.append(f"{SECTION_FILE} Zeile {line}: {exc}")
    return parsed


def _parse_events(path, errors):
    from views import EVENT_CATEGORY_LABELS
    fieldnames, rows = _read_csv(path)
    required = ["title", "category", "starts_at", "ends_at", "location"]
    if not _check_columns(EVENT_FILE, fieldnames, required, errors):
        return []
    parsed = []
    for line, row in rows:
        try:
            for key in required:
                value = _plain(row, key) if key in ("title", "location") else _text(row, key)
                if not value:
                    raise ValueError(f"{key} darf nicht leer sein")
            category = _text(row, "category")
            if category not in EVENT_CATEGORY_LABELS:
                raise ValueError(f"unbekannte category „{category}“ (erlaubt: {', '.join(EVENT_CATEGORY_LABELS)})")
            starts_at = _parse_datetime(row["starts_at"])
            ends_at = _parse_datetime(row["ends_at"])
            if ends_at < starts_at:
                raise ValueError("ends_at liegt vor starts_at")
            parsed.append({
                "title": _plain(row, "title"), "category": category,
                "subtitle": _plain(row, "subtitle"),
                "all_day": _parse_bool(row.get("all_day")),
                "starts_at": starts_at, "ends_at": ends_at,
                "location": _plain(row, "location"),
                "updated_at": _parse_datetime(row["updated_at"]) if _text(row, "updated_at") else None,
            })
        except ValueError as exc:
            errors.append(f"{EVENT_FILE} Zeile {line}: {exc}")
    return parsed


def _parse_users(path, images, errors):
    from members import EMAIL_PATTERN, normalize_website
    fieldnames, rows = _read_csv(path)
    if not _check_columns(USER_FILE, fieldnames, ["username", "email"], errors):
        return []
    roles = {key for key, _ in ROLES}
    visibilities = {key for key, _ in VISIBILITY_CHOICES}
    parsed, seen = [], set()
    for line, row in rows:
        try:
            username = _text(row, "username")
            email = (_text(row, "email") or "").lower() or None
            if not username:
                raise ValueError("username darf nicht leer sein")
            if email and not EMAIL_PATTERN.match(email):
                raise ValueError(f"ungültige E-Mail-Adresse „{email}“")
            for key in {username.lower(), email} - {None}:
                if key in seen:
                    raise ValueError(f"„{key}“ kommt in users.csv mehrfach vor")
                seen.add(key)
            role = (_text(row, "role") or ROLE_MEMBER).lower()
            if role not in roles:
                raise ValueError(f"role „{role}“ muss admin oder member sein")
            if role == ROLE_MEMBER and not email:
                raise ValueError("Mitglieder brauchen eine E-Mail-Adresse")
            password_hash = _text(row, "password_hash")
            if password_hash and not password_hash.startswith("$2"):
                raise ValueError("password_hash ist kein bcrypt-Hash (leer lassen, wenn unbekannt)")
            item = {
                "username": username, "email": email, "role": role,
                "is_active": _parse_bool(row.get("is_active") if _text(row, "is_active") else "1"),
                "password_hash": password_hash,
                "created_at": _parse_datetime(row["created_at"]) if _text(row, "created_at") else None,
                "last_login_at": _parse_datetime(row["last_login_at"]) if _text(row, "last_login_at") else None,
                "profile": None,
            }
            if any(_text(row, col) for col in PROFILE_COLUMNS):
                first, last, city = _plain(row, "first_name"), _plain(row, "last_name"), _plain(row, "city")
                if not (first and last and city):
                    raise ValueError("Profil braucht first_name, last_name und city")
                functions = [f.strip() for f in (_text(row, "functions") or "").split(",") if f.strip()]
                unknown = [f for f in functions if f not in PROFILE_FUNCTIONS]
                if unknown:
                    raise ValueError(f"unbekannte functions {', '.join(unknown)} (erlaubt: {', '.join(PROFILE_FUNCTIONS)})")
                vis = {}
                for field in ("email", "phone", "bio"):
                    value = (_text(row, f"{field}_visibility") or VISIBILITY_MEMBERS).lower()
                    if value not in visibilities:
                        raise ValueError(f"{field}_visibility „{value}“ muss public oder members sein")
                    vis[field] = value
                photo = _text(row, "photo_filename")
                if photo:
                    images.check(photo)
                item["profile"] = {
                    "first_name": first, "last_name": last, "city": city,
                    "display_name": _plain(row, "display_name"),
                    "organization": _plain(row, "organization"),
                    "job_title": _plain(row, "job_title"),
                    "functions": functions,
                    "phone": _plain(row, "phone"),
                    "bio": _text(row, "bio"),
                    "website": normalize_website(_text(row, "website")) or None,
                    "photo": photo,
                    "email_visibility": vis["email"], "phone_visibility": vis["phone"],
                    "bio_visibility": vis["bio"],
                    "updated_at": _parse_datetime(row["profile_updated_at"]) if _text(row, "profile_updated_at") else None,
                }
            parsed.append(item)
        except ValueError as exc:
            errors.append(f"{USER_FILE} Zeile {line}: {exc}")
    return parsed


def _apply_profile(profile, data, images):
    for key in ("first_name", "last_name", "city", "display_name", "organization", "job_title",
                "functions", "phone", "bio", "website", "email_visibility", "phone_visibility",
                "bio_visibility"):
        setattr(profile, key, data[key])
    if data["updated_at"]:
        profile.updated_at = data["updated_at"]
    if data["photo"]:
        profile.photo_filename = images.store_avatar(data["photo"])


def import_from_dir(source_dir, user):
    """Liest articles.csv, sections.csv und events.csv (soweit vorhanden) aus
    source_dir und legt die Eintraege neu an, mit user als Autor. Alles oder
    nichts: bei einem Fehler wird nichts gespeichert und CsvImportError
    ausgeloest. Liefert die Anzahlen der angelegten Datensaetze."""
    from views import DEFAULT_COL_SIZE, place_section_in_slot

    present = [name for name in FILES if os.path.isfile(os.path.join(source_dir, name))]
    if not present:
        raise CsvImportError([f"Keine der Dateien {', '.join(FILES)} gefunden."])

    images = _ImageImporter(source_dir)
    errors = []
    articles = _parse_articles(os.path.join(source_dir, ARTICLE_FILE), images, errors) if ARTICLE_FILE in present else []
    sections = _parse_sections(os.path.join(source_dir, SECTION_FILE), images, errors) if SECTION_FILE in present else []
    events = _parse_events(os.path.join(source_dir, EVENT_FILE), errors) if EVENT_FILE in present else []
    users = _parse_users(os.path.join(source_dir, USER_FILE), images, errors) if USER_FILE in present else []
    if errors:
        raise CsvImportError(errors)

    now = datetime.now(timezone.utc)

    # Ordnungsnummern beim Import in 10er-Schritten neu vergeben (10, 20, 30, ...),
    # damit spaeter Beitraege dazwischen eingeordnet werden koennen. Die
    # Reihenfolge ergibt sich aus der order_number der CSV, bei Gleichstand
    # aus der Zeilenreihenfolge. Importierte Beitraege kommen hinter die
    # bereits vorhandenen.
    max_existing = db.session.query(db.func.max(Article.order_number)).scalar() or 0
    next_number = (max_existing // ORDER_STEP + 1) * ORDER_STEP
    ordered = sorted(enumerate(articles), key=lambda t: (t[1]["order_number"], t[0]))
    for offset, (_index, item) in enumerate(ordered):
        item["order_number"] = next_number + offset * ORDER_STEP

    try:
        for c in articles:
            image_filename, image_fit = (
                images.store_article(c["image"], c["fit"]) if c["image"] else (None, "cover")
            )
            db.session.add(Article(
                title=c["title"], body=c["body"], description=c["description"],
                image_filename=image_filename, image_fit=image_fit,
                on_index=c["on_index"], on_consulting=c["on_consulting"],
                on_academy=c["on_academy"], on_stories=c["on_stories"],
                is_banner=c["is_banner"], order_number=c["order_number"],
                col_size=c["col_size"] or DEFAULT_COL_SIZE,
                updated_at=c["updated_at"] or now, user_id=user.id,
            ))

        new_sections = []
        for s in sections:
            section = Section(
                title=s["title"], body=s["body"], kicker=s["kicker"],
                description=s["description"], image_position=s["image_position"],
                image_filename=images.store(s["image"], s["orientation"]) if s["image"] else None,
                on_index=s["pages"]["index"][0],
                on_consulting=s["pages"]["consulting"][0],
                on_academy=s["pages"]["academy"][0],
                updated_at=s["updated_at"] or now, user_id=user.id,
            )
            db.session.add(section)
            new_sections.append((section, s["pages"]))
        db.session.flush()

        # Slots je Seite in der Reihenfolge der CSV-Positionen belegen. Bereits
        # vorhandene Sektionen im selben Slot bleiben davor stehen; die
        # importierten werden dahinter eingereiht.
        for page in SECTION_PAGES:
            placed = [(sec, pages[page][1], pages[page][2]) for sec, pages in new_sections
                      if pages[page][1] is not None]
            placed.sort(key=lambda t: (t[1], t[2], t[0].id))
            for sec, slot, _pos in placed:
                place_section_in_slot(page, sec, slot, 10_000)
                db.session.flush()

        for e in events:
            db.session.add(Event(
                title=e["title"], category=e["category"], subtitle=e["subtitle"],
                all_day=e["all_day"], starts_at=e["starts_at"], ends_at=e["ends_at"],
                location=e["location"], updated_at=e["updated_at"] or now,
                user_id=user.id,
            ))

        # Nutzer: neue Konten werden angelegt (mit Passwort-Hash aus der CSV).
        # Bestehende Konten (gleicher Nutzername oder gleiche E-Mail) behalten
        # Rolle, Sperre und Passwort; nur ihr Profil wird uebernommen.
        replaced_photos = []
        new_users = updated_users = 0
        for u in users:
            with db.session.no_autoflush:
                existing = User.query.filter(db.or_(
                    User.username == u["username"],
                    *([User.email == u["email"], User.username == u["email"]] if u["email"] else []),
                )).first()
            if existing is None:
                account = User(
                    username=u["username"], email=u["email"], role=u["role"], is_active=u["is_active"],
                    password_hash=u["password_hash"] or _unusable_password_hash(),
                    created_at=u["created_at"] or now, last_login_at=u["last_login_at"],
                )
                db.session.add(account)
                new_users += 1
            else:
                account = existing
                if u["profile"]:
                    updated_users += 1
            if u["profile"]:
                profile = account.profile
                if profile is None:
                    profile = Profile(user=account, first_name="", last_name="", city="")
                    db.session.add(profile)
                elif u["profile"]["photo"] and profile.photo_filename:
                    replaced_photos.append(profile.photo_filename)
                _apply_profile(profile, u["profile"], images)
            db.session.flush()

        db.session.commit()
    except Exception:
        db.session.rollback()
        images.rollback()
        raise

    # Ersetzte Profilfotos erst nach erfolgreichem Speichern entfernen
    for stored in replaced_photos:
        try:
            os.remove(os.path.join(images.upload_folder, stored))
        except OSError:
            pass

    return {"articles": len(articles), "sections": len(sections), "events": len(events),
            "users": new_users, "users_updated": updated_users,
            "images": sum(1 for n in images.created if not n.startswith("avatars/")),
            "photos": sum(1 for n in images.created if n.startswith("avatars/"))}


def _unusable_password_hash():
    # Zufaelliges, unbekanntes Passwort: die Person setzt ueber "Passwort
    # vergessen" ein eigenes.
    import secrets
    from flask_bcrypt import generate_password_hash
    return generate_password_hash(secrets.token_urlsafe(32)).decode("utf-8")


def format_counts(counts, verb="Importiert"):
    parts = [f"{counts['articles']} Beiträge", f"{counts['sections']} Sektionen",
             f"{counts['events']} Termine"]
    if "users_updated" in counts:
        parts.append(f"{counts['users']} neue{'r' if counts['users'] == 1 else ''} Nutzer")
        if counts["users_updated"]:
            n = counts["users_updated"]
            parts.append(f"{n} bestehende{'s Profil' if n == 1 else ' Profile'} aktualisiert")
    else:
        parts.append(f"{counts['users']} Nutzer")
    parts.append(f"{counts['images']} Bilder")
    if "photos" in counts:
        parts[-1] += f" und {counts['photos']} Profilfotos"
    return f"{verb}: " + ", ".join(parts)


# --------------------------------------------------------------------------
# Kommandozeile
# --------------------------------------------------------------------------

def main(argv):
    import argparse
    from views import app
    from models import User

    parser = argparse.ArgumentParser(description="CSV-Import/-Export für Beiträge, Sektionen, Termine und Nutzer")
    sub = parser.add_subparsers(dest="command", required=True)
    p_exp = sub.add_parser("export", help="Daten und Bilder in einen Ordner exportieren")
    p_exp.add_argument("directory")
    p_imp = sub.add_parser("import", help="Daten und Bilder aus einem Ordner importieren")
    p_imp.add_argument("directory")
    p_imp.add_argument("--user", default="admin", help="Autor der importierten Einträge (Standard: admin)")
    args = parser.parse_args(argv)

    with app.app_context():
        if args.command == "export":
            counts, warnings = export_to_dir(args.directory)
            for w in warnings:
                print(f"Hinweis: {w}")
            print(format_counts(counts, "Exportiert") + f" → {args.directory}")
            return 0

        user = User.query.filter_by(username=args.user).first()
        if user is None:
            print(f"Nutzer „{args.user}“ nicht gefunden.", file=sys.stderr)
            return 1
        try:
            counts = import_from_dir(args.directory, user)
        except CsvImportError as exc:
            print("Import abgebrochen, nichts wurde gespeichert:", file=sys.stderr)
            for e in exc.errors:
                print(f"  - {e}", file=sys.stderr)
            return 1
        print(format_counts(counts))
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
