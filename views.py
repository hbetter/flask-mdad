import os
from uuid import uuid4
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from PIL import Image
from flask import Flask, render_template, redirect, url_for, request, flash, send_file, send_from_directory, session
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_migrate import Migrate

from models import db, User, Article, Section, Event
import csv_transfer
import images
import lexicon_data


# Jede Beitragkarte kann unabhängig auf mehreren dieser Seiten erscheinen
# (daher Tickboxen statt eines einzelnen Typs). "Banner" ist bewusst kein
# Listeneintrag hier, sondern ein eigenes Feld (is_banner), weil es nur
# einmal gleichzeitig vergeben werden darf.
ARTICLE_FLAGS = [
    ("on_index", "Indexseite"),
    ("on_consulting", "Beratung"),
    ("on_academy", "Akademie"),
    ("on_stories", "Erfolgsgeschichten"),
]

# Sektionen gibt es nur auf den drei Seiten mit statischem Aufbau (kein
# Banner, keine Erfolgsgeschichten-Sektionen).
SECTION_FLAGS = [
    ("on_index", "Indexseite"),
    ("on_consulting", "Beratung"),
    ("on_academy", "Akademie"),
]

# Interner Wert (englisch) -> sichtbares Label (deutsch) fuer die
# Eventkategorie (was fuer eine Veranstaltung es inhaltlich ist,
# unabhaengig von der Terminart/dem Format oben).
EVENT_CATEGORIES = [
    ("webinar", "Webinar"),
    ("inhouse", "Probe Spielraum"),
    ("certification", "Spiele Coach Zertifizierung"),
    ("trial", "Spiele Event"),
]
EVENT_CATEGORY_LABELS = dict(EVENT_CATEGORIES)

# Bootstrap-Icons-Name (ohne "bi-"-Praefix) je Kategorie - wird dezent als
# Hintergrundgrafik auf den Terminkarten dargestellt (Bedienfeld und
# oeffentlicher Bereich), damit die Kategorie auch ohne Lesen des Badges
# auf einen Blick erkennbar ist.
EVENT_CATEGORY_ICONS = {
    "webinar": "camera-video",
    "inhouse": "house-door",
    "certification": "award",
    "trial": "dice-5",
}

# Bootstrap-Modal-ID je Kategorie, dessen zugehoeriges AC-Formular den
# "Platz sichern"-Button auf der Startseite (templates/index.html) als
# Modal statt als Sprung zu "#contact" oeffnet (siehe base.html fuer die
# Modals selbst). Kategorien ohne Eintrag hier haben (noch) kein eigenes
# Formular-Modal und behalten den Sprung zu "#contact".
EVENT_CATEGORY_MODAL = {
    "webinar": "webinarModal",
    "certification": "spieleCoachModal",
    "trial": "spieleEventModal",
}

DEFAULT_COL_SIZE = "col-12 col-md-6 col-lg-4"
RESIZED_IMAGE_WIDTH = 1280
RESIZED_IMAGE_HEIGHT = 715

LANDSCAPE_WIDTH = 1280
LANDSCAPE_HEIGHT = 715

PORTRAIT_WIDTH = 900
PORTRAIT_HEIGHT = 1200

app = Flask(__name__)
# Hinter Nginx (nginx/playfulfuture.de.conf): X-Forwarded-Proto/-Host/-For
# des vorgeschalteten Proxys uebernehmen, damit url_for(..., _external=True)
# (z. B. sitemap.xml) https://playfulfuture.de statt http:// erzeugt. Ohne
# Proxy (Entwicklung) fehlen die Header, dann aendert sich nichts.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
app.config["SECRET_KEY"] = "entwicklungs-schluessel-123"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Hochgeladene Bilder liegen ausserhalb von static/ in data/uploads (wie die
# Datenbank in data/postgres nicht im Repository und im Produktionsbetrieb
# per Volume eingebunden, siehe docker-compose.prod.yml). Ausgeliefert ueber
# die Route /uploads/<dateiname> bzw. in Produktion direkt von Nginx.
app.config["UPLOAD_FOLDER"] = os.path.join("data", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "webp"}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


# Cache-Busting fuer CSS/JS/Bilder aus static/: Nginx liefert static/ mit
# "expires 7d" aus, Browser behalten daher eine Woche lang alte Dateien.
# Jede mit url_for("static", ...) erzeugte Adresse bekommt deshalb die
# Aenderungszeit der Datei angehaengt (z. B. custom.css?v=1760527913).
# Aendert sich die Datei, aendert sich die Adresse und Browser laden neu.
@app.url_defaults
def add_static_version(endpoint, values):
    if endpoint != "static" or "filename" not in values or "v" in values:
        return
    path = os.path.join(app.static_folder, values["filename"])
    try:
        values["v"] = int(os.stat(path).st_mtime)
    except OSError:
        pass


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def crop_to_aspect_ratio(img, target_width, target_height):
    target_ratio = target_width / target_height
    current_ratio = img.width / img.height

    if current_ratio > target_ratio:
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) // 2
        top = 0
        right = left + new_width
        bottom = img.height
    else:
        new_height = int(img.width / target_ratio)
        left = 0
        top = (img.height - new_height) // 2
        right = img.width
        bottom = top + new_height

    return img.crop((left, top, right, bottom))


def resize_and_save_image(file_storage, upload_folder, target_width=RESIZED_IMAGE_WIDTH, target_height=RESIZED_IMAGE_HEIGHT):
    if not file_storage or not file_storage.filename:
        return None

    if not allowed_file(file_storage.filename):
        return None

    try:
        img = Image.open(file_storage.stream)
        img = img.convert("RGB")
        img = crop_to_aspect_ratio(img, target_width, target_height)
        img = img.resize((target_width, target_height), Image.LANCZOS)

        filename = f"{uuid4().hex}.webp"
        filepath = os.path.join(upload_folder, filename)

        img.save(filepath, "WEBP", quality=85, method=6)
        return filename
    except Exception:
        return None


def delete_uploaded_image(filename):
    if not filename:
        return

    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(path):
        os.remove(path)


def get_banner_text():
    banner = Article.query.filter_by(is_banner=True).first()
    return banner.description if banner else None


@app.template_filter("datetimeformat")
def datetimeformat(value, format="%d.%m.%Y %H:%M"):
    if value is None:
        return ""

    berlin_tz = ZoneInfo("Europe/Berlin")

    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)

    local_value = value.astimezone(berlin_tz)
    return local_value.strftime(format)


def parse_local_datetime(value):
    # Wandelt den Wert eines <input type="datetime-local"> (lokale Zeit,
    # Europe/Berlin) in ein timezone-aware UTC-datetime zum Speichern um.
    if not value:
        return None

    try:
        naive = datetime.strptime(value, "%Y-%m-%dT%H:%M")
    except ValueError:
        return None

    berlin_tz = ZoneInfo("Europe/Berlin")
    return naive.replace(tzinfo=berlin_tz).astimezone(timezone.utc)


def resolve_event_datetime(form, all_day, prefix):
    # Termine haben getrennte Datum- und Uhrzeit-Felder (kein <input
    # type="datetime-local">, siehe add_event.html/edit_event.html). Bei
    # ganztaegigen Terminen wird die Uhrzeit ignoriert (Feld ist ausgeblendet,
    # wird aber trotzdem mitgesendet) und auf 00:00 gesetzt. prefix ist
    # "starts_at" oder "ends_at" und waehlt das jeweilige Feldpaar aus.
    date_str = form.get(f"{prefix}_date")
    time_str = "00:00" if all_day else form.get(f"{prefix}_time")

    if not date_str or not time_str:
        return None

    return parse_local_datetime(f"{date_str}T{time_str}")


@app.template_filter("dateinput")
def dateinput(value):
    # Formatiert ein gespeichertes UTC-datetime als Vorbelegung fuer ein
    # <input type="date"> (lokale Zeit, Europe/Berlin).
    if value is None:
        return ""

    berlin_tz = ZoneInfo("Europe/Berlin")

    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)

    return value.astimezone(berlin_tz).strftime("%Y-%m-%d")


@app.template_filter("timeinput")
def timeinput(value):
    # Gegenstueck zu dateinput, formatiert die Uhrzeit fuer ein
    # <input type="time"> (lokale Zeit, Europe/Berlin).
    if value is None:
        return ""

    berlin_tz = ZoneInfo("Europe/Berlin")

    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)

    return value.astimezone(berlin_tz).strftime("%H:%M")


@app.template_filter("eventcategorylabel")
def eventcategorylabel(value):
    return EVENT_CATEGORY_LABELS.get(value, value)


@app.template_filter("eventcategoryicon")
def eventcategoryicon(value):
    return EVENT_CATEGORY_ICONS.get(value, "calendar-event")


@app.template_filter("eventcategorymodal")
def eventcategorymodal(value):
    return EVENT_CATEGORY_MODAL.get(value)


@app.template_filter("eventdaterange")
def eventdaterange(item):
    # Kompakte Anzeige von Start bis Ende eines Termins (Bedienfeld/Portal):
    # ganztaegig -> nur Datum (nur einmal, wenn Start- und Endtag gleich
    # sind, sonst als Datumsspanne); mit Uhrzeit -> Datum + Uhrzeitspanne,
    # bzw. volle Datum-Uhrzeit-Spanne, wenn der Termin ueber Tage hinweg
    # geht. Ersetzt die vorherige separate "Ganztaegig"-Markierung, da die
    # Spanne selbst schon zeigt, ob eine Uhrzeit relevant ist.
    berlin_tz = ZoneInfo("Europe/Berlin")

    def to_local(value):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(berlin_tz)

    start = to_local(item.starts_at)
    end = to_local(item.ends_at) if item.ends_at else None
    same_day = end is None or start.date() == end.date()

    if item.all_day:
        if same_day:
            return start.strftime("%d.%m.%Y")
        return f"{start.strftime('%d.%m.%Y')} – {end.strftime('%d.%m.%Y')}"

    if same_day:
        if end is None:
            return start.strftime("%d.%m.%Y, %H:%M")
        return f"{start.strftime('%d.%m.%Y, %H:%M')} – {end.strftime('%H:%M')}"

    return f"{start.strftime('%d.%m.%Y %H:%M')} – {end.strftime('%d.%m.%Y %H:%M')}"


# Anzahl der Slots je Seite - reine Zahl, ohne jeden Bezug zu den
# statischen Inhalten der Seite (kein Kicker-/Titeltext, keine Kopplung an
# deren Reihenfolge oder Anzahl im Template). Slot i liegt zwischen dem i.
# und (i+1). Element auf der Seite, unabhaengig davon, was dort steht.
# Bewusst simpel gehalten, damit das auf andere Projekte uebertragbar bleibt.
PAGE_SLOT_COUNT = {
    "index": 10,
    "consulting": 4,
    "academy": 3,
}

PAGE_LABELS = {"index": "Indexseite", "consulting": "Beratung", "academy": "Akademie"}
PAGE_FLAG_ATTR = {"index": "on_index", "consulting": "on_consulting", "academy": "on_academy"}
PAGE_SLOT_INDEX_ATTR = {
    "index": "slot_index_index",
    "consulting": "slot_index_consulting",
    "academy": "slot_index_academy",
}
PAGE_SLOT_POSITION_ATTR = {
    "index": "slot_position_index",
    "consulting": "slot_position_consulting",
    "academy": "slot_position_academy",
}

SLOT_LETTERS = "abcdefghijklmnopqrstuvwxyz"


def slot_occupants(page_key, slot, exclude_section_id=None):
    # Sektionen, die aktuell in diesem Slot dieser Seite stehen, sortiert
    # nach ihrer Position innerhalb des Slots.
    flag_attr = PAGE_FLAG_ATTR[page_key]
    slot_attr = PAGE_SLOT_INDEX_ATTR[page_key]
    pos_attr = PAGE_SLOT_POSITION_ATTR[page_key]

    sections = (
        Section.query
        .filter_by(**{flag_attr: True, slot_attr: slot})
        .all()
    )
    sections = [s for s in sections if s.id != exclude_section_id]
    sections.sort(key=lambda s: (getattr(s, pos_attr) or 0, s.id))
    return sections


def sections_by_slot(page_key):
    # Fuer die oeffentlichen Seiten: alle Slots dieser Seite mit den
    # jeweils darin platzierten Sektionen (in Position-Reihenfolge).
    return {
        slot: slot_occupants(page_key, slot)
        for slot in range(1, PAGE_SLOT_COUNT[page_key] + 1)
    }


def slot_options(page_key, exclude_section_id=None):
    # (Wert, Label)-Paare fuer die Auswahl beim Hinzufuegen/Bearbeiten einer
    # Sektion. Ist ein Slot noch frei, gibt es nur "Slot N". Stehen dort
    # schon n Sektionen, gibt es n+1 Optionen "Slot Na", "Slot Nb", ... fuer
    # jede moegliche Einfuegeposition davor/dazwischen/danach. Wert-Format:
    # "<Slot>:<Position>".
    options = []
    for slot in range(1, PAGE_SLOT_COUNT[page_key] + 1):
        occupants = slot_occupants(page_key, slot, exclude_section_id=exclude_section_id)
        if not occupants:
            options.append((f"{slot}:1", f"Slot {slot}"))
            continue
        for i in range(len(occupants) + 1):
            options.append((f"{slot}:{i + 1}", f"Slot {slot}{SLOT_LETTERS[i]}"))
    return options


def parse_slot_value(value, page_key):
    # Prueft einen eingereichten "<Slot>:<Position>"-Wert gegen die Seite
    # und liefert (slot, position) oder None bei ungueltiger Eingabe.
    if not value or ":" not in value:
        return None
    slot_str, pos_str = value.split(":", 1)
    if not slot_str.isdigit() or not pos_str.isdigit():
        return None
    slot = int(slot_str)
    position = int(pos_str)
    if not (1 <= slot <= PAGE_SLOT_COUNT[page_key]) or position < 1:
        return None
    return slot, position


def place_section_in_slot(page_key, section, slot, insert_position):
    # Setzt die Sektion an insert_position (1-basiert) unter den anderen
    # aktuell in diesem Slot platzierten Sektionen ein und nummeriert alle
    # Positionen im Slot lueckenlos neu durch.
    flag_attr = PAGE_FLAG_ATTR[page_key]
    slot_attr = PAGE_SLOT_INDEX_ATTR[page_key]
    pos_attr = PAGE_SLOT_POSITION_ATTR[page_key]

    others = slot_occupants(page_key, slot, exclude_section_id=section.id)
    insert_position = max(1, min(insert_position, len(others) + 1))
    others.insert(insert_position - 1, section)

    setattr(section, flag_attr, True)
    for i, s in enumerate(others, start=1):
        setattr(s, slot_attr, slot)
        setattr(s, pos_attr, i)


def clear_section_slot(page_key, section):
    setattr(section, PAGE_SLOT_INDEX_ATTR[page_key], None)
    setattr(section, PAGE_SLOT_POSITION_ATTR[page_key], None)


def section_slot_labels(sections):
    # Fuer die Bedienfeld-Anzeige: pro Seite, auf der eine Sektion aktiv ist,
    # ihr aktueller Slot (mit Buchstabe, falls dort mehrere Sektionen stehen).
    labels = {section.id: {} for section in sections}
    for page_key in PAGE_SLOT_COUNT:
        for slot in range(1, PAGE_SLOT_COUNT[page_key] + 1):
            occupants = slot_occupants(page_key, slot)
            for i, s in enumerate(occupants):
                if s.id not in labels:
                    continue
                suffix = SLOT_LETTERS[i] if len(occupants) > 1 else ""
                labels[s.id][page_key] = f"{PAGE_LABELS[page_key]}: Slot {slot}{suffix}"
    return labels


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    banner = get_banner_text()
    articles = (
        Article.query
        .filter_by(on_index=True)
        .order_by(Article.order_number.asc(), Article.id.asc())
        .all()
    )
    sections_in_slot = sections_by_slot("index")
    # Alle Termine chronologisch, wie im Bedienfeld, aber ohne Filterung nach
    # user_id: die Indexseite ist oeffentlich und zeigt saemtliche Termine.
    events = (
        Event.query
        .order_by(Event.starts_at.asc(), Event.id.asc())
        .all()
    )
    return render_template(
        "index.html",
        articles=articles,
        sections_in_slot=sections_in_slot,
        events=events,
        banner=banner,
    )


@app.route("/stories")
def stories():
    banner = get_banner_text()
    articles = (
        Article.query
        .filter_by(on_stories=True)
        .order_by(Article.order_number.asc(), Article.id.asc())
        .all()
    )
    return render_template(
        "stories.html",
        articles=articles,
        banner=banner,
    )


@app.route("/consulting")
def consulting():
    banner = get_banner_text()
    articles = (
        Article.query
        .filter_by(on_consulting=True)
        .order_by(Article.order_number.asc(), Article.id.asc())
        .all()
    )
    sections_in_slot = sections_by_slot("consulting")
    return render_template(
        "consulting.html",
        articles=articles,
        sections_in_slot=sections_in_slot,
        banner=banner,
    )


@app.route("/academy")
def academy():
    banner = get_banner_text()
    articles = (
        Article.query
        .filter_by(on_academy=True)
        .order_by(Article.order_number.asc(), Article.id.asc())
        .all()
    )
    sections_in_slot = sections_by_slot("academy")
    return render_template(
        "academy.html",
        articles=articles,
        sections_in_slot=sections_in_slot,
        banner=banner,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username", "") or "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Falscher Nutzername oder Passwort.", "danger")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    banner = get_banner_text()
    # Fehler eines fehlgeschlagenen Imports (siehe import_data) werden im
    # Import-Modal angezeigt, das dann automatisch geoeffnet wird.
    import_errors = session.pop("import_errors", None)
    open_import = bool(import_errors) or request.args.get("import") == "1"
    user_articles = (
        Article.query
        .filter_by(user_id=current_user.id)
        .order_by(Article.order_number.asc(), Article.id.asc())
        .all()
    )
    article_orders = (
        Article.query
        .order_by(Article.order_number.asc(), Article.id.asc())
        .all()
    )
    user_sections = (
        Section.query
        .filter_by(user_id=current_user.id)
        .order_by(Section.id.asc())
        .all()
    )
    transition_labels = section_slot_labels(user_sections)

    # Slot-Auswahl je Sektion und Seite fuers Positionierungs-Modal (gleiche
    # Optionen wie im vollstaendigen Bearbeiten-Formular, hier aber fuer
    # jede angezeigte Sektion einzeln vorberechnet).
    section_slot_choices = {}
    for section in user_sections:
        section_slot_choices[section.id] = {}
        for page_key in PAGE_SLOT_COUNT:
            slot = getattr(section, PAGE_SLOT_INDEX_ATTR[page_key])
            position = getattr(section, PAGE_SLOT_POSITION_ATTR[page_key])
            section_slot_choices[section.id][page_key] = {
                "options": slot_options(page_key, exclude_section_id=section.id),
                "current": f"{slot}:{position}" if slot and position else None,
            }

    user_events = (
        Event.query
        .filter_by(user_id=current_user.id)
        .order_by(Event.starts_at.asc(), Event.id.asc())
        .all()
    )
    return render_template(
        "dashboard.html",
        articles=user_articles,
        article_flags=ARTICLE_FLAGS,
        banner=banner,
        article_orders=article_orders,
        sections=user_sections,
        section_flags=SECTION_FLAGS,
        transition_labels=transition_labels,
        section_slot_choices=section_slot_choices,
        events=user_events,
        # Gesamtzahlen fuer die Rueckfrage vor dem Export (der Export umfasst
        # alle Eintraege, nicht nur die des angemeldeten Nutzers).
        export_counts={
            "articles": Article.query.count(),
            "sections": Section.query.count(),
            "events": Event.query.count(),
        },
        import_errors=import_errors,
        past_event_count=past_events_query().count(),
        open_import=open_import,
    )


@app.route("/add-article", methods=["GET", "POST"])
@login_required
def add_article():
    if request.method == "POST":
        on_index = request.form.get("on_index") == "1"
        on_consulting = request.form.get("on_consulting") == "1"
        on_academy = request.form.get("on_academy") == "1"
        on_stories = request.form.get("on_stories") == "1"
        is_banner = request.form.get("is_banner") == "1"

        if is_banner:
            existing_banner = Article.query.filter_by(is_banner=True).first()
            if existing_banner:
                flash(
                    "Ein Banner existiert bereits und kann nicht erneut angelegt werden.",
                    "warning",
                )
                return redirect(url_for("dashboard"))
        file = request.files.get("image")
        image_filename = None
        image_fit = "cover"
        if file and file.filename:
            # Beitragsbilder werden nicht zugeschnitten; die Darstellung
            # (image_fit) waehlt bei "auto" images.py anhand des Bildes.
            if not allowed_file(file.filename):
                flash("Nur Bilddateien sind erlaubt: png, jpg, jpeg, gif, webp", "warning")
                return redirect(url_for("add_article"))
            try:
                image_filename, image_fit = images.save_article_image(
                    file.stream, file.filename, app.config["UPLOAD_FOLDER"],
                    fit=request.form.get("image_fit", "auto"),
                )
            except ValueError:
                flash("Die Datei ist keine lesbare Bilddatei.", "warning")
                return redirect(url_for("add_article"))
        order_number = int(request.form.get("order_number") or 0)
        col_size = request.form.get("col_size") or DEFAULT_COL_SIZE

        new_item = Article(
            on_index=on_index,
            on_consulting=on_consulting,
            on_academy=on_academy,
            on_stories=on_stories,
            is_banner=is_banner,
            title=request.form.get("title"),
            description=request.form.get("description"),
            body=request.form.get("body"),
            order_number=order_number,
            user_id=current_user.id,
            image_filename=image_filename,
            image_fit=image_fit,
            col_size=col_size,
            updated_at=datetime.now(timezone.utc),
        )
        db.session.add(new_item)
        db.session.commit()
        flash("Inhalt hinzugefügt!", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "add_article.html", article_flags=ARTICLE_FLAGS, image_fit_choices=images.FIT_CHOICES
    )


@app.route("/add-event", methods=["GET", "POST"])
@login_required
def add_event():
    if request.method == "POST":
        all_day = request.form.get("all_day") == "1"
        starts_at = resolve_event_datetime(request.form, all_day, "starts_at")
        ends_at = resolve_event_datetime(request.form, all_day, "ends_at")
        category = request.form.get("category")

        if starts_at is None or ends_at is None:
            flash("Bitte ein gültiges Start- und Enddatum (und, falls nicht ganztägig, jeweils eine Uhrzeit) angeben.", "warning")
            return redirect(url_for("add_event"))

        if ends_at < starts_at:
            flash("Das Enddatum darf nicht vor dem Startdatum liegen.", "warning")
            return redirect(url_for("add_event"))

        if category not in EVENT_CATEGORY_LABELS:
            flash("Bitte eine gültige Eventkategorie wählen.", "warning")
            return redirect(url_for("add_event"))

        new_event = Event(
            title=request.form.get("title"),
            category=category,
            all_day=all_day,
            subtitle=request.form.get("subtitle"),
            starts_at=starts_at,
            ends_at=ends_at,
            location=request.form.get("location"),
            user_id=current_user.id,
            updated_at=datetime.now(timezone.utc),
        )
        db.session.add(new_event)
        db.session.commit()
        flash("Termin hinzugefügt!", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "add_event.html",
        event_categories=EVENT_CATEGORIES,
    )


@app.route("/edit-event/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    item = Event.query.get_or_404(event_id)

    if item.author != current_user:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        title = request.form.get("title")
        subtitle = request.form.get("subtitle")
        location = request.form.get("location")
        category = request.form.get("category")
        all_day = request.form.get("all_day") == "1"
        starts_at = resolve_event_datetime(request.form, all_day, "starts_at")
        ends_at = resolve_event_datetime(request.form, all_day, "ends_at")

        if starts_at is None or ends_at is None:
            flash("Bitte ein gültiges Start- und Enddatum (und, falls nicht ganztägig, jeweils eine Uhrzeit) angeben.", "warning")
            return redirect(url_for("edit_event", event_id=item.id))

        if ends_at < starts_at:
            flash("Das Enddatum darf nicht vor dem Startdatum liegen.", "warning")
            return redirect(url_for("edit_event", event_id=item.id))

        if category not in EVENT_CATEGORY_LABELS:
            flash("Bitte eine gültige Eventkategorie wählen.", "warning")
            return redirect(url_for("edit_event", event_id=item.id))

        if title is not None and title.strip():
            item.title = title.strip()

        if subtitle is not None:
            item.subtitle = subtitle.strip()

        if location is not None and location.strip():
            item.location = location.strip()

        item.category = category
        item.all_day = all_day
        item.starts_at = starts_at
        item.ends_at = ends_at
        item.updated_at = datetime.now(timezone.utc)

        db.session.commit()
        flash("Termin aktualisiert.", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "edit_event.html",
        event=item,
        event_categories=EVENT_CATEGORIES,
    )


@app.route("/delete-event/<int:event_id>", methods=["POST"])
@login_required
def delete_event(event_id):
    item = Event.query.get_or_404(event_id)

    if item.author == current_user:
        db.session.delete(item)
        db.session.commit()
        flash("Termin gelöscht.", "info")

    return redirect(url_for("dashboard"))


def past_events_query():
    # Termine des angemeldeten Nutzers, deren Ende in der Vergangenheit liegt.
    # Gespeichert wird in UTC ohne Zeitzonenangabe, daher hier ebenfalls
    # "naive" UTC-Zeit vergleichen.
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    return Event.query.filter(Event.user_id == current_user.id, Event.ends_at < now_utc)


@app.route("/delete-past-events", methods=["POST"])
@login_required
def delete_past_events():
    count = past_events_query().delete(synchronize_session=False)
    db.session.commit()
    if count:
        flash(f"{count} vergangene{'r' if count == 1 else ''} Termin{'' if count == 1 else 'e'} gelöscht.", "info")
    else:
        flash("Es gibt keine vergangenen Termine.", "info")
    return redirect(url_for("dashboard", _anchor="events"))


@app.route("/add-section", methods=["GET", "POST"])
@login_required
def add_section():
    if request.method == "POST":
        on_index = request.form.get("on_index") == "1"
        on_consulting = request.form.get("on_consulting") == "1"
        on_academy = request.form.get("on_academy") == "1"
        image_position = request.form.get("image_position")
        if image_position not in ("left", "right"):
            image_position = "right"

        file = request.files.get("image")
        image_filename = None
        image_orientation = request.form.get("image_orientation", "landscape")
        if file and file.filename:
            if image_orientation == "portrait":
                image_filename = resize_and_save_image(
                    file,
                    app.config["UPLOAD_FOLDER"],
                    target_width=PORTRAIT_WIDTH,
                    target_height=PORTRAIT_HEIGHT,
                )
            else:
                image_filename = resize_and_save_image(
                    file,
                    app.config["UPLOAD_FOLDER"],
                    target_width=LANDSCAPE_WIDTH,
                    target_height=LANDSCAPE_HEIGHT,
                )
            if not image_filename:
                flash("Nur Bilddateien sind erlaubt.", "warning")
                return redirect(url_for("add_section"))

        flags = {"index": on_index, "consulting": on_consulting, "academy": on_academy}
        placements = {}
        for page_key, flag in flags.items():
            if not flag:
                continue
            parsed = parse_slot_value(request.form.get(f"slot_{page_key}"), page_key)
            if parsed is None:
                flash(
                    "Bitte für jede ausgewählte Seite einen gültigen Slot wählen.",
                    "warning",
                )
                return redirect(url_for("add_section"))
            placements[page_key] = parsed

        new_section = Section(
            on_index=on_index,
            on_consulting=on_consulting,
            on_academy=on_academy,
            kicker=request.form.get("kicker"),
            title=request.form.get("title"),
            description=request.form.get("description"),
            body=request.form.get("body"),
            user_id=current_user.id,
            image_filename=image_filename,
            image_position=image_position,
            updated_at=datetime.now(timezone.utc),
        )
        db.session.add(new_section)
        db.session.flush()  # id fuer die Slot-Platzierung verfuegbar machen

        for page_key, (slot, position) in placements.items():
            place_section_in_slot(page_key, new_section, slot, position)

        db.session.commit()
        flash("Sektion hinzugefügt!", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "add_section.html",
        section_flags=SECTION_FLAGS,
        slot_options_index=slot_options("index"),
        slot_options_consulting=slot_options("consulting"),
        slot_options_academy=slot_options("academy"),
    )


@app.route("/edit-section/<int:section_id>", methods=["GET", "POST"])
@login_required
def edit_section(section_id):
    item = Section.query.get_or_404(section_id)

    if item.author != current_user:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        on_index = request.form.get("on_index") == "1"
        on_consulting = request.form.get("on_consulting") == "1"
        on_academy = request.form.get("on_academy") == "1"

        flags = {"index": on_index, "consulting": on_consulting, "academy": on_academy}
        placements = {}
        for page_key, flag in flags.items():
            if not flag:
                continue
            parsed = parse_slot_value(request.form.get(f"slot_{page_key}"), page_key)
            if parsed is None:
                flash(
                    "Bitte für jede ausgewählte Seite einen gültigen Slot wählen.",
                    "warning",
                )
                return redirect(url_for("edit_section", section_id=item.id))
            placements[page_key] = parsed

        item.on_index = on_index
        item.on_consulting = on_consulting
        item.on_academy = on_academy

        for page_key, flag in flags.items():
            if flag:
                slot, position = placements[page_key]
                place_section_in_slot(page_key, item, slot, position)
            else:
                clear_section_slot(page_key, item)

        kicker = request.form.get("kicker")
        title = request.form.get("title")
        description = request.form.get("description")
        body = request.form.get("body")

        if kicker is not None:
            item.kicker = kicker.strip()

        if title is not None and title.strip():
            item.title = title.strip()

        if description is not None:
            item.description = description.strip()

        if body is not None and body.strip():
            item.body = body.strip()

        image_position = request.form.get("image_position")
        if image_position in ("left", "right"):
            item.image_position = image_position

        item.updated_at = datetime.now(timezone.utc)

        delete_image = request.form.get("delete_image") == "1"

        if delete_image and item.image_filename:
            delete_uploaded_image(item.image_filename)
            item.image_filename = None

        file = request.files.get("image")
        image_filename = None
        image_orientation = request.form.get("image_orientation", "landscape")
        if file and file.filename:
            if image_orientation == "portrait":
                image_filename = resize_and_save_image(
                    file,
                    app.config["UPLOAD_FOLDER"],
                    target_width=PORTRAIT_WIDTH,
                    target_height=PORTRAIT_HEIGHT,
                )
            else:
                image_filename = resize_and_save_image(
                    file,
                    app.config["UPLOAD_FOLDER"],
                    target_width=LANDSCAPE_WIDTH,
                    target_height=LANDSCAPE_HEIGHT,
                )
            if not image_filename:
                flash("Nur Bilddateien sind erlaubt: png, jpg, jpeg, gif, webp", "warning")
                return redirect(url_for("edit_section", section_id=item.id))

            delete_uploaded_image(item.image_filename)
            item.image_filename = image_filename

        db.session.commit()
        flash("Sektion aktualisiert.", "success")
        return redirect(url_for("dashboard"))

    def current_slot_value(page_key):
        slot = getattr(item, PAGE_SLOT_INDEX_ATTR[page_key])
        position = getattr(item, PAGE_SLOT_POSITION_ATTR[page_key])
        return f"{slot}:{position}" if slot and position else None

    return render_template(
        "edit_section.html",
        section=item,
        section_flags=SECTION_FLAGS,
        slot_options_index=slot_options("index", exclude_section_id=item.id),
        slot_options_consulting=slot_options("consulting", exclude_section_id=item.id),
        slot_options_academy=slot_options("academy", exclude_section_id=item.id),
        current_slot_index=current_slot_value("index"),
        current_slot_consulting=current_slot_value("consulting"),
        current_slot_academy=current_slot_value("academy"),
    )


@app.route("/delete-section/<int:section_id>", methods=["POST"])
@login_required
def delete_section(section_id):
    item = Section.query.get_or_404(section_id)

    if item.author == current_user:
        delete_uploaded_image(item.image_filename)
        db.session.delete(item)
        db.session.commit()
        flash("Sektion gelöscht.", "info")

    return redirect(url_for("dashboard"))


@app.route("/edit-article/<int:article_id>", methods=["GET", "POST"])
@login_required
def edit_article(article_id):
    item = Article.query.get_or_404(article_id)

    if item.author != current_user:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        new_is_banner = request.form.get("is_banner") == "1"

        if new_is_banner:
            existing_banner = Article.query.filter(
                Article.is_banner == True,
                Article.id != item.id,
            ).first()
            if existing_banner:
                flash("Ein Banner existiert bereits.", "warning")
                return redirect(url_for("dashboard"))

        item.on_index = request.form.get("on_index") == "1"
        item.on_consulting = request.form.get("on_consulting") == "1"
        item.on_academy = request.form.get("on_academy") == "1"
        item.on_stories = request.form.get("on_stories") == "1"
        item.is_banner = new_is_banner

        title = request.form.get("title")
        description = request.form.get("description")
        body = request.form.get("body")

        if title is not None and title.strip():
            item.title = title.strip()

        if description is not None:
            item.description = description.strip()

        if body is not None and body.strip():
            item.body = body.strip()


        item.updated_at = datetime.now(timezone.utc)
        item.order_number = int(request.form.get("order_number"))
        item.col_size = request.form.get("col_size")

        delete_image = request.form.get("delete_image") == "1"

        if delete_image and item.image_filename:
            delete_uploaded_image(item.image_filename)
            item.image_filename = None


        file = request.files.get("image")
        # Fehlt image_fit im Formular (Schnellbearbeitungs-Modal im
        # Bedienfeld), bleibt die bisherige Darstellung unveraendert.
        fit_choice = request.form.get("image_fit")
        if file and file.filename:
            if not allowed_file(file.filename):
                flash("Nur Bilddateien sind erlaubt: png, jpg, jpeg, gif, webp", "warning")
                return redirect(url_for("edit_article", article_id=item.id))
            try:
                image_filename, image_fit = images.save_article_image(
                    file.stream, file.filename, app.config["UPLOAD_FOLDER"],
                    fit=fit_choice or "auto",
                )
            except ValueError:
                flash("Die Datei ist keine lesbare Bilddatei.", "warning")
                return redirect(url_for("edit_article", article_id=item.id))

            delete_uploaded_image(item.image_filename)
            item.image_filename = image_filename
            item.image_fit = image_fit
        elif fit_choice in images.FIT_VALUES:
            item.image_fit = fit_choice
        elif fit_choice == "auto" and item.image_filename:
            # "Automatisch" fuer das bereits gespeicherte Bild neu auswerten
            item.image_fit = images.fit_for_stored_image(
                os.path.join(app.config["UPLOAD_FOLDER"], item.image_filename)
            )

        db.session.commit()
        flash("Beitrag aktualisiert.", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "edit_article.html",
        article=item,
        article_flags=ARTICLE_FLAGS,
        image_fit_choices=images.FIT_CHOICES,
        banner=get_banner_text(),
    )


@app.route("/delete-article/<int:article_id>", methods=["POST"])
@login_required
def delete_article(article_id):
    item = Article.query.get_or_404(article_id)

    if item.author == current_user:
        delete_uploaded_image(item.image_filename)
        db.session.delete(item)
        db.session.commit()
        flash("Beitrag gelöscht.", "info")

    return redirect(url_for("dashboard"))


# CSV-Export/-Import (Logik in csv_transfer.py). Der Export liefert ein ZIP
# mit articles.csv, sections.csv, events.csv und den Bildern; der Import nimmt
# einen ganzen Ordner (CSV-Dateien + Bilder im selben Ordner) oder dieses
# ZIP entgegen.
@app.route("/export")
@login_required
def export_data():
    import io
    import tempfile
    import zipfile

    with tempfile.TemporaryDirectory() as tmp:
        counts, warnings = csv_transfer.export_to_dir(tmp)
        if warnings:
            with open(os.path.join(tmp, "export_hinweise.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(warnings) + "\n")
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for name in sorted(os.listdir(tmp)):
                zf.write(os.path.join(tmp, name), arcname=name)
    buffer.seek(0)
    stamp = datetime.now(ZoneInfo("Europe/Berlin")).strftime("%Y-%m-%d")
    return send_file(
        buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"mdad-export-{stamp}.zip",
    )


def _safe_basename(name):
    # Nur den Dateinamen ohne Ordnerpfad verwenden (beim Ordner-Upload
    # schickt der Browser "ordner/datei.csv"); versteckte Dateien wie
    # .DS_Store ueberspringen.
    base = os.path.basename((name or "").replace("\\", "/"))
    if not base or base.startswith("."):
        return None
    return base


MAX_IMPORT_ERRORS_SHOWN = 20


def _import_failed(errors):
    # Fehler ueber die Session ans Bedienfeld weiterreichen (dort im
    # Import-Modal angezeigt). Begrenzt, damit das Session-Cookie klein bleibt.
    shown = errors[:MAX_IMPORT_ERRORS_SHOWN]
    if len(errors) > MAX_IMPORT_ERRORS_SHOWN:
        shown.append(f"… und {len(errors) - MAX_IMPORT_ERRORS_SHOWN} weitere Fehler.")
    session["import_errors"] = shown
    return redirect(url_for("dashboard"))


@app.route("/import", methods=["GET", "POST"])
@login_required
def import_data():
    if request.method == "POST":
        import tempfile
        import zipfile

        files = [f for f in request.files.getlist("files") if f and f.filename]
        if not files:
            return _import_failed(["Bitte einen Ordner oder eine ZIP-Datei auswählen."])

        with tempfile.TemporaryDirectory() as tmp:
            for upload in files:
                base = _safe_basename(upload.filename)
                if base is None:
                    continue
                if base.lower().endswith(".zip"):
                    zip_path = os.path.join(tmp, ".upload.zip")
                    upload.save(zip_path)
                    try:
                        with zipfile.ZipFile(zip_path) as zf:
                            for member in zf.infolist():
                                member_base = _safe_basename(member.filename)
                                if member.is_dir() or member_base is None:
                                    continue
                                with zf.open(member) as src, open(os.path.join(tmp, member_base), "wb") as dst:
                                    dst.write(src.read())
                    except zipfile.BadZipFile:
                        return _import_failed([f"„{base}“ ist keine gültige ZIP-Datei."])
                    finally:
                        os.remove(zip_path)
                else:
                    upload.save(os.path.join(tmp, base))

            try:
                counts = csv_transfer.import_from_dir(tmp, current_user)
            except csv_transfer.CsvImportError as exc:
                return _import_failed(exc.errors)

        flash(
            f"Import abgeschlossen: {counts['articles']} Beiträge, {counts['sections']} Sektionen, "
            f"{counts['events']} Termine, {counts['images']} Bilder.",
            "success",
        )
        return redirect(url_for("dashboard"))

    # Der Import ist ein Modal im Bedienfeld; ein direkter Aufruf von /import
    # (z. B. nach einem zu grossen Upload) oeffnet dieses Modal.
    return redirect(url_for("dashboard", **{"import": "1"}))


@app.errorhandler(RequestEntityTooLarge)
def handle_too_large(_error):
    limit_mb = app.config["MAX_CONTENT_LENGTH"] // (1024 * 1024)
    message = f"Die hochgeladenen Dateien sind zusammen größer als {limit_mb} MB."
    if request.endpoint == "import_data":
        return _import_failed([message + " Größere Bestände bitte über die Kommandozeile importieren (siehe README)."])
    flash(message, "warning")
    return redirect(request.url)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(
        os.path.abspath(app.config["UPLOAD_FOLDER"]), filename, max_age=7 * 24 * 3600
    )


@app.route("/imprint")
def imprint():
    banner = get_banner_text()
    return render_template("imprint.html", banner=banner)


@app.route("/privacy")
def privacy():
    banner = get_banner_text()
    return render_template("privacy.html", banner=banner)


@app.route("/lexicon")
def lexicon():
    # Statische Lexikonseite (Inhalte in lexicon_data.py), vorerst ohne
    # Menuepunkt - nur direkt ueber /lexicon erreichbar.
    banner = get_banner_text()
    groups, terms_by_slug = lexicon_data.build_lexicon()
    page_url = url_for("lexicon", _external=True)
    # Strukturierte Daten (schema.org DefinedTermSet), damit Suchmaschinen
    # die Seite als Glossar mit einzelnen Begriffen erkennen.
    structured_data = {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "name": "Lexikon: Gesundheit, Resilienz und Wandel in der Arbeitswelt",
        "url": page_url,
        "inLanguage": "de",
        "hasDefinedTerm": [
            {
                "@type": "DefinedTerm",
                "name": term["term"],
                "description": term["short"],
                "url": page_url + "#" + term["slug"],
            }
            for term in lexicon_data.LEXICON_TERMS
        ],
    }
    return render_template(
        "lexicon.html",
        banner=banner,
        groups=groups,
        letters={letter for letter, _ in groups},
        alphabet=[chr(c) for c in range(ord("A"), ord("Z") + 1)],
        categories=lexicon_data.LEXICON_CATEGORIES,
        term_count=len(terms_by_slug),
        structured_data=structured_data,
        quick_terms=lexicon_data.LEXICON_QUICK_TERMS,
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/sitemap.xml")
def sitemap():
    pages = []
    pages.append({
        "loc": url_for("index", _external=True),
        "lastmod": datetime.utcnow().date().isoformat()
    })
    pages.append({
        "loc": url_for("stories", _external=True),
        "lastmod": datetime.utcnow().date().isoformat()
    })

    return render_template("sitemap.xml", pages=pages)