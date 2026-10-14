"""CSV-Import und -Export fuer Karten (Card), Sektionen (Section) und Termine (Event).

Ein Export-/Import-Ordner enthaelt bis zu drei CSV-Dateien (cards.csv,
sections.csv, events.csv) sowie die darin per Dateiname referenzierten Bilder
im selben Ordner. Format wie in flask-crm: Semikolon als Trennzeichen, UTF-8
mit BOM (damit Excel Umlaute korrekt anzeigt). Datum/Uhrzeit in lokaler Zeit
(Europe/Berlin) als "JJJJ-MM-TT HH:MM"; gespeichert wird wie im Bedienfeld in UTC.

Aufruf im web-Container:
    python csv_transfer.py export <ordner>
    python csv_transfer.py import <ordner> [--user admin]

Im Bedienfeld gibt es dieselben Funktionen als ZIP-Download (/export) und
als Ordner-Upload (/import).
"""

import csv
import io
import os
import shutil
import sys
from datetime import datetime, timezone
from uuid import uuid4
from zoneinfo import ZoneInfo

from PIL import Image
from flask import current_app

from models import db, Card, Section, Event

BERLIN = ZoneInfo("Europe/Berlin")
DELIMITER = ";"
ENCODING = "utf-8-sig"
DATETIME_FORMAT = "%Y-%m-%d %H:%M"

CARD_FILE = "cards.csv"
SECTION_FILE = "sections.csv"
EVENT_FILE = "events.csv"
FILES = (CARD_FILE, SECTION_FILE, EVENT_FILE)

# Spaltenreihenfolge der CSV-Dateien. "id" wird nur zur Orientierung
# exportiert und beim Import ignoriert (es werden immer neue Datensaetze
# angelegt). "image_orientation" ist wie im Upload-Formular kein Modellfeld:
# leer = Bild unveraendert uebernehmen, "landscape"/"portrait" = wie beim
# Upload im Bedienfeld zuschneiden und als WebP speichern.
CARD_COLUMNS = [
    "id", "title", "description", "body", "image_filename", "image_orientation",
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
    """Schreibt alle Karten, Sektionen und Termine als CSV in target_dir und
    kopiert die referenzierten Bilder dazu. Liefert (Anzahlen, Hinweise)."""
    os.makedirs(target_dir, exist_ok=True)
    upload_folder = _upload_folder()
    warnings = []
    images = set()

    cards = Card.query.order_by(Card.order_number.asc(), Card.id.asc()).all()
    _write_csv(os.path.join(target_dir, CARD_FILE), CARD_COLUMNS, [
        [c.id, c.title, c.description or "", c.body, c.image_filename or "", "",
         _format_bool(c.on_index), _format_bool(c.on_consulting),
         _format_bool(c.on_academy), _format_bool(c.on_stories),
         _format_bool(c.is_banner), c.order_number, c.col_size,
         _format_datetime(c.updated_at)]
        for c in cards
    ])
    images.update(c.image_filename for c in cards if c.image_filename)

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

    for name in sorted(images):
        src = os.path.join(upload_folder, name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(target_dir, name))
        else:
            warnings.append(f"Bild „{name}“ fehlt in static/uploads und wurde nicht exportiert.")

    counts = {"cards": len(cards), "sections": len(sections), "events": len(events),
              "images": len(images) - len(warnings)}
    return counts, warnings


# --------------------------------------------------------------------------
# Import
# --------------------------------------------------------------------------

class _ImageImporter:
    """Kopiert/konvertiert Bilder aus dem Importordner nach static/uploads und
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


def _parse_cards(path, images, errors):
    fieldnames, rows = _read_csv(path)
    if not _check_columns(CARD_FILE, fieldnames, ["title", "body"], errors):
        return []
    parsed = []
    for line, row in rows:
        try:
            title, body = _text(row, "title"), _text(row, "body")
            if not title or not body:
                raise ValueError("title und body dürfen nicht leer sein")
            image, orientation = _image_fields(row, images)
            parsed.append({
                "title": title, "body": body,
                "description": _text(row, "description"),
                "image": image, "orientation": orientation,
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
            errors.append(f"{CARD_FILE} Zeile {line}: {exc}")
    banners = sum(1 for c in parsed if c["is_banner"])
    if banners > 1:
        errors.append(f"{CARD_FILE}: Es darf höchstens eine Karte als Banner markiert sein ({banners} gefunden).")
    elif banners == 1 and Card.query.filter_by(is_banner=True).first():
        errors.append(f"{CARD_FILE}: Es existiert bereits ein Banner – is_banner der importierten Karte auf 0 setzen oder das bestehende Banner vorher entfernen.")
    return parsed


def _parse_sections(path, images, errors):
    from views import PAGE_SLOT_COUNT
    fieldnames, rows = _read_csv(path)
    if not _check_columns(SECTION_FILE, fieldnames, ["title", "body"], errors):
        return []
    parsed = []
    for line, row in rows:
        try:
            title, body = _text(row, "title"), _text(row, "body")
            if not title or not body:
                raise ValueError("title und body dürfen nicht leer sein")
            image, orientation = _image_fields(row, images)
            position = (_text(row, "image_position") or "right").lower()
            if position not in ("left", "right"):
                raise ValueError(f"image_position „{position}“ muss left oder right sein")
            item = {
                "title": title, "body": body, "kicker": _text(row, "kicker"),
                "description": _text(row, "description"),
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
                if not _text(row, key):
                    raise ValueError(f"{key} darf nicht leer sein")
            category = _text(row, "category")
            if category not in EVENT_CATEGORY_LABELS:
                raise ValueError(f"unbekannte category „{category}“ (erlaubt: {', '.join(EVENT_CATEGORY_LABELS)})")
            starts_at = _parse_datetime(row["starts_at"])
            ends_at = _parse_datetime(row["ends_at"])
            if ends_at < starts_at:
                raise ValueError("ends_at liegt vor starts_at")
            parsed.append({
                "title": _text(row, "title"), "category": category,
                "subtitle": _text(row, "subtitle"),
                "all_day": _parse_bool(row.get("all_day")),
                "starts_at": starts_at, "ends_at": ends_at,
                "location": _text(row, "location"),
                "updated_at": _parse_datetime(row["updated_at"]) if _text(row, "updated_at") else None,
            })
        except ValueError as exc:
            errors.append(f"{EVENT_FILE} Zeile {line}: {exc}")
    return parsed


def import_from_dir(source_dir, user):
    """Liest cards.csv, sections.csv und events.csv (soweit vorhanden) aus
    source_dir und legt die Eintraege neu an, mit user als Autor. Alles oder
    nichts: bei einem Fehler wird nichts gespeichert und CsvImportError
    ausgeloest. Liefert die Anzahlen der angelegten Datensaetze."""
    from views import DEFAULT_COL_SIZE, place_section_in_slot

    present = [name for name in FILES if os.path.isfile(os.path.join(source_dir, name))]
    if not present:
        raise CsvImportError([f"Keine der Dateien {', '.join(FILES)} gefunden."])

    images = _ImageImporter(source_dir)
    errors = []
    cards = _parse_cards(os.path.join(source_dir, CARD_FILE), images, errors) if CARD_FILE in present else []
    sections = _parse_sections(os.path.join(source_dir, SECTION_FILE), images, errors) if SECTION_FILE in present else []
    events = _parse_events(os.path.join(source_dir, EVENT_FILE), errors) if EVENT_FILE in present else []
    if errors:
        raise CsvImportError(errors)

    now = datetime.now(timezone.utc)
    try:
        for c in cards:
            db.session.add(Card(
                title=c["title"], body=c["body"], description=c["description"],
                image_filename=images.store(c["image"], c["orientation"]) if c["image"] else None,
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

        db.session.commit()
    except Exception:
        db.session.rollback()
        images.rollback()
        raise

    return {"cards": len(cards), "sections": len(sections), "events": len(events),
            "images": len(images.created)}


# --------------------------------------------------------------------------
# Kommandozeile
# --------------------------------------------------------------------------

def main(argv):
    import argparse
    from views import app
    from models import User

    parser = argparse.ArgumentParser(description="CSV-Import/-Export für Karten, Sektionen und Termine")
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
            print(f"Exportiert: {counts['cards']} Karten, {counts['sections']} Sektionen, "
                  f"{counts['events']} Termine, {counts['images']} Bilder → {args.directory}")
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
        print(f"Importiert: {counts['cards']} Karten, {counts['sections']} Sektionen, "
              f"{counts['events']} Termine, {counts['images']} Bilder")
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
