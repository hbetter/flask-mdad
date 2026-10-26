from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone

db = SQLAlchemy()

def _utcnow():
    return datetime.now(timezone.utc)


# Rollen: "admin" pflegt die Website (Administration, Nutzerverwaltung,
# Portalkonfiguration), "member" hat nur Zugriff auf das eigene Profil.
ROLE_ADMIN = "admin"
ROLE_MEMBER = "member"
ROLES = [(ROLE_ADMIN, "Admin"), (ROLE_MEMBER, "Mitglied")]


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Mitglieder melden sich mit ihrer E-Mail-Adresse an; username ist fuer
    # sie identisch mit der E-Mail-Adresse bei der Einladung. Der Admin aus
    # init_db.py meldet sich weiterhin mit "admin" an.
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True)
    role = db.Column(db.String(20), nullable=False, default=ROLE_MEMBER)
    # Gesperrte Konten (is_active=False) koennen sich nicht anmelden und
    # erscheinen nicht im Community-Bereich. Ueberschreibt UserMixin.is_active.
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=_utcnow)
    last_login_at = db.Column(db.DateTime)
    articles = db.relationship('Article', backref='author', lazy=True)
    sections = db.relationship('Section', backref='author', lazy=True)
    events = db.relationship('Event', backref='author', lazy=True)
    password_hash = db.Column(db.String(255), nullable=False)
    # 1:1 - jeder Nutzer hat hoechstens ein Profil (Admins brauchen keins).
    profile = db.relationship(
        'Profile', backref='user', uselist=False, cascade='all, delete-orphan'
    )

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN


# Sichtbarkeit der Felder E-Mail, Telefon und Bio im Community-Bereich.
VISIBILITY_PUBLIC = "public"    # alle Portalbesucher
VISIBILITY_MEMBERS = "members"  # nur eingeloggte Mitglieder
VISIBILITY_CHOICES = [
    (VISIBILITY_PUBLIC, "Für alle Portalbesucher"),
    (VISIBILITY_MEMBERS, "Nur für eingeloggte Mitglieder"),
]

# Funktion im Profil (Mehrfachauswahl). Gespeichert werden nur die
# Schluessel; eine neue Option ist eine neue Zeile hier, ohne
# Datenbankaenderung.
PROFILE_FUNCTIONS = {
    "coach": "Spiele Coach",
    "smeo_staff": "SMEO GmbH Team",
    "friend": "FreundIn",
}


# Persoenliches Profil eines Mitglieds. Erscheint im oeffentlichen
# Community-Bereich nur, wenn ein Foto hochgeladen ist (photo_filename).
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    display_name = db.Column(db.String(120))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(200))
    job_title = db.Column(db.String(200))
    functions = db.Column(db.JSON, nullable=False, default=list)
    city = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(60))
    bio = db.Column(db.Text)
    website = db.Column(db.String(300))
    photo_filename = db.Column(db.String(255))
    email_visibility = db.Column(db.String(10), nullable=False, default=VISIBILITY_MEMBERS)
    phone_visibility = db.Column(db.String(10), nullable=False, default=VISIBILITY_MEMBERS)
    bio_visibility = db.Column(db.String(10), nullable=False, default=VISIBILITY_MEMBERS)
    updated_at = db.Column(db.DateTime, nullable=False, default=_utcnow, onupdate=_utcnow)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def name(self):
        return self.display_name or self.full_name

    @property
    def function_labels(self):
        return [PROFILE_FUNCTIONS[k] for k in (self.functions or []) if k in PROFILE_FUNCTIONS]


# Einladungslinks: gespeichert wird nur ein Hash des Tokens, der Link selbst
# steht ausschliesslich in der versendeten Mail. Einmal nutzbar (used_at).
class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    token_hash = db.Column(db.String(64), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=_utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime)
    invited_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    invited_by = db.relationship('User', foreign_keys=[invited_by_id])


# Portalkonfiguration (genau ein Datensatz, id=1): SMTP fuer Einladungs- und
# Passwort-Mails sowie die Passwort-Richtlinie. Das SMTP-Passwort liegt verschluesselt
# vor (mailer.py), abgeleitet vom SECRET_KEY.
class PortalSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    smtp_host = db.Column(db.String(255))
    smtp_port = db.Column(db.Integer)
    smtp_security = db.Column(db.String(10), nullable=False, default="starttls")
    smtp_username = db.Column(db.String(255))
    smtp_password_encrypted = db.Column(db.Text)
    mail_from_address = db.Column(db.String(255))
    mail_from_name = db.Column(db.String(255))
    # Passwort-Richtlinie (auth.py): gilt fuer jedes neu gesetzte Passwort,
    # bestehende Passwoerter bleiben gueltig.
    password_min_length = db.Column(db.Integer, nullable=False, default=10)
    password_require_lower = db.Column(db.Boolean, nullable=False, default=False)
    password_require_upper = db.Column(db.Boolean, nullable=False, default=False)
    password_require_digit = db.Column(db.Boolean, nullable=False, default=False)
    password_require_special = db.Column(db.Boolean, nullable=False, default=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=_utcnow, onupdate=_utcnow)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    on_index = db.Column(db.Boolean, nullable=False, default=False)
    on_consulting = db.Column(db.Boolean, nullable=False, default=False)
    on_academy = db.Column(db.Boolean, nullable=False, default=False)
    on_stories = db.Column(db.Boolean, nullable=False, default=False)
    is_banner = db.Column(db.Boolean, nullable=False, default=False)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(300))
    image_filename = db.Column(db.String(255))
    # Darstellung des Bildes in der Kachel: "cover" (fuellend zugeschnitten),
    # "contain" (vollstaendig, fuer Logos) oder "blur" (vollstaendig vor
    # unscharfem Hintergrund). Siehe images.py.
    image_fit = db.Column(db.String(10), nullable=False, default="cover")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    order_number = db.Column(db.Integer, nullable=False, default=0)
    col_size = db.Column(db.String(50), nullable=False, default="col-12 col-md-6 col-lg-4")


# Wie Article, aber für ganze Sektionen (statt Beitragkarten in einem Grid) auf den drei
# Seiten Indexseite, Beratung und Akademie. Kein Banner- oder Erfolgsgeschichten-
# Häkchen (dort gibt es keine Sektionen) und keine Breite der Beitragkarten (col_size), da
# jede Sektion ohnehin die volle Breite einnimmt.
class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    on_index = db.Column(db.Boolean, nullable=False, default=False)
    on_consulting = db.Column(db.Boolean, nullable=False, default=False)
    on_academy = db.Column(db.Boolean, nullable=False, default=False)
    kicker = db.Column(db.String(200))
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(300))
    image_filename = db.Column(db.String(255))
    # Auf welcher Seite des Textes das Bild steht (nur relevant, wenn ein
    # Bild vorhanden ist) - unabhaengig vom Bildformat (image_orientation
    # beim Hochladen bestimmt nur den Bildausschnitt, nicht die Position).
    image_position = db.Column(db.String(10), nullable=False, default="right")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    # Platzierung pro Seite ueber durchnummerierte Slots zwischen den
    # statischen Abschnitten (Slot 1 = zwischen dem 1. und 2. statischen
    # Abschnitt usw., siehe PAGE_STATIC_KICKERS/PAGE_SLOT_COUNT in views.py).
    # slot_position_* ordnet mehrere Sektionen im selben Slot (1, 2, ...).
    # None bedeutet: nicht auf dieser Seite platziert.
    slot_index_index = db.Column(db.Integer)
    slot_position_index = db.Column(db.Integer)
    slot_index_consulting = db.Column(db.Integer)
    slot_position_consulting = db.Column(db.Integer)
    slot_index_academy = db.Column(db.Integer)
    slot_position_academy = db.Column(db.Integer)


# Termine (Events): eigenstaendiges Modell, unabhaengig von Article/Section, da
# Termine keine Platzierung auf den statischen Seiten haben, sondern ueber
# Titel, Art, Untertitel, Zeitpunkt und Ort verwaltet werden.
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    all_day = db.Column(db.Boolean, nullable=False, default=False)
    subtitle = db.Column(db.String(300))
    starts_at = db.Column(db.DateTime, nullable=False)
    ends_at = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
