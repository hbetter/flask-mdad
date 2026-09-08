import os
from uuid import uuid4
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from PIL import Image
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_migrate import Migrate

from models import db, User, Card, Section, Event


# Jede Karte kann unabhängig auf mehreren dieser Seiten erscheinen
# (daher Tickboxen statt eines einzelnen Typs). "Banner" ist bewusst kein
# Listeneintrag hier, sondern ein eigenes Feld (is_banner), weil es nur
# einmal gleichzeitig vergeben werden darf.
CARD_FLAGS = [
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

# Interner Wert (englisch) -> sichtbares Label (deutsch) fuer die Terminart.
EVENT_TYPES = [
    ("online", "Online"),
    ("in_person", "Präsenz"),
    ("in_house", "Inhouse"),
]
EVENT_TYPE_LABELS = dict(EVENT_TYPES)

# Interner Wert (englisch) -> sichtbares Label (deutsch) fuer die
# Eventkategorie (was fuer eine Veranstaltung es inhaltlich ist,
# unabhaengig von der Terminart/dem Format oben).
EVENT_CATEGORIES = [
    ("webinar", "Webinar"),
    ("trial_session", "Probe-Spielraum"),
    ("coach_certification", "Spiele Coach Qualifizierung"),
    ("workshop", "Workshop"),
]
EVENT_CATEGORY_LABELS = dict(EVENT_CATEGORIES)

DEFAULT_COL_SIZE = "col-12 col-md-6 col-lg-4"
RESIZED_IMAGE_WIDTH = 1280
RESIZED_IMAGE_HEIGHT = 715

LANDSCAPE_WIDTH = 1280
LANDSCAPE_HEIGHT = 715

PORTRAIT_WIDTH = 900
PORTRAIT_HEIGHT = 1200

app = Flask(__name__)
app.config["SECRET_KEY"] = "entwicklungs-schluessel-123"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 5 MB
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "webp"}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


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
    banner = Card.query.filter_by(is_banner=True).first()
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


def resolve_event_starts_at(form, all_day):
    # Termine haben getrennte Datum- und Uhrzeit-Felder (kein <input
    # type="datetime-local">, siehe add_event.html/edit_event.html). Bei
    # ganztaegigen Terminen wird die Uhrzeit ignoriert (Feld ist ausgeblendet,
    # wird aber trotzdem mitgesendet) und auf 00:00 gesetzt.
    date_str = form.get("starts_at_date")
    time_str = "00:00" if all_day else form.get("starts_at_time")

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


@app.template_filter("eventtypelabel")
def eventtypelabel(value):
    return EVENT_TYPE_LABELS.get(value, value)


@app.template_filter("eventcategorylabel")
def eventcategorylabel(value):
    return EVENT_CATEGORY_LABELS.get(value, value)


GERMAN_MONTH_ABBR = {
    1: "Jan", 2: "Feb", 3: "Mär", 4: "Apr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Dez",
}


@app.template_filter("germanmonthyear")
def germanmonthyear(value):
    # Formatiert ein datetime als "<dt. Monatskuerzel> <Jahr>" (z. B.
    # "Okt 2026"), unabhaengig von der Server-Locale (Docker-Images haben
    # meist keine deutsche Locale installiert).
    if value is None:
        return ""

    berlin_tz = ZoneInfo("Europe/Berlin")

    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)

    local_value = value.astimezone(berlin_tz)
    return f"{GERMAN_MONTH_ABBR[local_value.month]} {local_value.year}"


# Anzahl der Slots je Seite - reine Zahl, ohne jeden Bezug zu den
# statischen Inhalten der Seite (kein Kicker-/Titeltext, keine Kopplung an
# deren Reihenfolge oder Anzahl im Template). Slot i liegt zwischen dem i.
# und (i+1). Element auf der Seite, unabhaengig davon, was dort steht.
# Bewusst simpel gehalten, damit das auf andere Projekte uebertragbar bleibt.
PAGE_SLOT_COUNT = {
    "index": 10,
    "consulting": 3,
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
    # Fuer die Dashboard-Anzeige: pro Seite, auf der eine Sektion aktiv ist,
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
    cards = (
        Card.query
        .filter_by(on_index=True)
        .order_by(Card.order_number.asc(), Card.id.asc())
        .all()
    )
    sections_in_slot = sections_by_slot("index")
    # Alle Termine chronologisch, wie im Dashboard, aber ohne Filterung nach
    # user_id: die Indexseite ist oeffentlich und zeigt saemtliche Termine.
    events = (
        Event.query
        .order_by(Event.starts_at.asc(), Event.id.asc())
        .all()
    )
    return render_template(
        "index.html",
        cards=cards,
        sections_in_slot=sections_in_slot,
        events=events,
        banner=banner,
    )


@app.route("/stories")
def stories():
    banner = get_banner_text()
    cards = (
        Card.query
        .filter_by(on_stories=True)
        .order_by(Card.order_number.asc(), Card.id.asc())
        .all()
    )
    return render_template(
        "stories.html",
        cards=cards,
        banner=banner,
    )


@app.route("/consulting")
def consulting():
    banner = get_banner_text()
    cards = (
        Card.query
        .filter_by(on_consulting=True)
        .order_by(Card.order_number.asc(), Card.id.asc())
        .all()
    )
    sections_in_slot = sections_by_slot("consulting")
    return render_template(
        "consulting.html",
        cards=cards,
        sections_in_slot=sections_in_slot,
        banner=banner,
    )


@app.route("/academy")
def academy():
    banner = get_banner_text()
    cards = (
        Card.query
        .filter_by(on_academy=True)
        .order_by(Card.order_number.asc(), Card.id.asc())
        .all()
    )
    sections_in_slot = sections_by_slot("academy")
    return render_template(
        "academy.html",
        cards=cards,
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
    user_cards = (
        Card.query
        .filter_by(user_id=current_user.id)
        .order_by(Card.order_number.asc(), Card.id.asc())
        .all()
    )
    card_orders = (
        Card.query
        .order_by(Card.order_number.asc(), Card.id.asc())
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
        cards=user_cards,
        card_flags=CARD_FLAGS,
        banner=banner,
        card_orders=card_orders,
        sections=user_sections,
        section_flags=SECTION_FLAGS,
        transition_labels=transition_labels,
        section_slot_choices=section_slot_choices,
        events=user_events,
        event_types=EVENT_TYPES,
    )


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_card():
    if request.method == "POST":
        on_index = request.form.get("on_index") == "1"
        on_consulting = request.form.get("on_consulting") == "1"
        on_academy = request.form.get("on_academy") == "1"
        on_stories = request.form.get("on_stories") == "1"
        is_banner = request.form.get("is_banner") == "1"

        if is_banner:
            existing_banner = Card.query.filter_by(is_banner=True).first()
            if existing_banner:
                flash(
                    "Ein Banner existiert bereits und kann nicht erneut angelegt werden.",
                    "warning",
                )
                return redirect(url_for("dashboard"))
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
                return redirect(url_for("add_card"))
        order_number = int(request.form.get("order_number") or 0)
        col_size = request.form.get("col_size") or DEFAULT_COL_SIZE

        new_item = Card(
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
            col_size=col_size,
            updated_at=datetime.now(timezone.utc),
        )
        db.session.add(new_item)
        db.session.commit()
        flash("Inhalt hinzugefügt!", "success")
        return redirect(url_for("dashboard"))

    return render_template("add_card.html", card_flags=CARD_FLAGS)


@app.route("/add-event", methods=["GET", "POST"])
@login_required
def add_event():
    if request.method == "POST":
        all_day = request.form.get("all_day") == "1"
        starts_at = resolve_event_starts_at(request.form, all_day)
        event_type = request.form.get("event_type")
        category = request.form.get("category")

        if starts_at is None:
            flash("Bitte ein gültiges Datum (und, falls nicht ganztägig, eine Uhrzeit) angeben.", "warning")
            return redirect(url_for("add_event"))

        if event_type not in EVENT_TYPE_LABELS:
            flash("Bitte eine gültige Art des Termins wählen.", "warning")
            return redirect(url_for("add_event"))

        if category not in EVENT_CATEGORY_LABELS:
            flash("Bitte eine gültige Eventkategorie wählen.", "warning")
            return redirect(url_for("add_event"))

        new_event = Event(
            title=request.form.get("title"),
            event_type=event_type,
            category=category,
            all_day=all_day,
            subtitle=request.form.get("subtitle"),
            starts_at=starts_at,
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
        event_types=EVENT_TYPES,
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
        event_type = request.form.get("event_type")
        category = request.form.get("category")
        all_day = request.form.get("all_day") == "1"
        starts_at = resolve_event_starts_at(request.form, all_day)

        if starts_at is None:
            flash("Bitte ein gültiges Datum (und, falls nicht ganztägig, eine Uhrzeit) angeben.", "warning")
            return redirect(url_for("edit_event", event_id=item.id))

        if event_type not in EVENT_TYPE_LABELS:
            flash("Bitte eine gültige Art des Termins wählen.", "warning")
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

        item.event_type = event_type
        item.category = category
        item.all_day = all_day
        item.starts_at = starts_at
        item.updated_at = datetime.now(timezone.utc)

        db.session.commit()
        flash("Termin aktualisiert.", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "edit_event.html",
        event=item,
        event_types=EVENT_TYPES,
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


@app.route("/add-section", methods=["GET", "POST"])
@login_required
def add_section():
    if request.method == "POST":
        on_index = request.form.get("on_index") == "1"
        on_consulting = request.form.get("on_consulting") == "1"
        on_academy = request.form.get("on_academy") == "1"

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


@app.route("/edit/<int:card_id>", methods=["GET", "POST"])
@login_required
def edit_card(card_id):
    item = Card.query.get_or_404(card_id)

    if item.author != current_user:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        new_is_banner = request.form.get("is_banner") == "1"

        if new_is_banner:
            existing_banner = Card.query.filter(
                Card.is_banner == True,
                Card.id != item.id,
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
                return redirect(url_for("edit_card", card_id=item.id))

            delete_uploaded_image(item.image_filename)
            item.image_filename = image_filename

        db.session.commit()
        flash("Karte aktualisiert.", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "edit_card.html",
        card=item,
        card_flags=CARD_FLAGS,
        banner=get_banner_text(),
    )


@app.route("/delete/<int:card_id>", methods=["POST"])
@login_required
def delete_card(card_id):
    item = Card.query.get_or_404(card_id)

    if item.author == current_user:
        delete_uploaded_image(item.image_filename)
        db.session.delete(item)
        db.session.commit()
        flash("Karte gelöscht.", "info")

    return redirect(url_for("dashboard"))


@app.route("/imprint")
def imprint():
    banner = get_banner_text()
    return render_template("imprint.html", banner=banner)


@app.route("/privacy")
def privacy():
    banner = get_banner_text()
    return render_template("privacy.html", banner=banner)


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