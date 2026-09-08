from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    cards = db.relationship('Card', backref='author', lazy=True)
    sections = db.relationship('Section', backref='author', lazy=True)
    events = db.relationship('Event', backref='author', lazy=True)
    password_hash = db.Column(db.String(255), nullable=False)

class Card(db.Model):
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    order_number = db.Column(db.Integer, nullable=False, default=0)
    col_size = db.Column(db.String(50), nullable=False, default="col-12 col-md-6 col-lg-4")


# Wie Card, aber für ganze Sektionen (statt Karten in einem Grid) auf den drei
# Seiten Indexseite, Beratung und Akademie. Kein Banner- oder Erfolgsgeschichten-
# Häkchen (dort gibt es keine Sektionen) und keine Kartenbreite (col_size), da
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


# Termine (Events): eigenstaendiges Modell, unabhaengig von Card/Section, da
# Termine keine Platzierung auf den statischen Seiten haben, sondern ueber
# Titel, Art, Untertitel, Zeitpunkt und Ort verwaltet werden.
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    all_day = db.Column(db.Boolean, nullable=False, default=False)
    subtitle = db.Column(db.String(300))
    starts_at = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
