from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    cards = db.relationship('Card', backref='author', lazy=True)
    sections = db.relationship('Section', backref='author', lazy=True)
    password_hash = db.Column(db.String(255), nullable=False)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    on_index = db.Column(db.Boolean, nullable=False, default=False)
    on_beratung = db.Column(db.Boolean, nullable=False, default=False)
    on_akademie = db.Column(db.Boolean, nullable=False, default=False)
    on_erfolgsgeschichten = db.Column(db.Boolean, nullable=False, default=False)
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
    on_beratung = db.Column(db.Boolean, nullable=False, default=False)
    on_akademie = db.Column(db.Boolean, nullable=False, default=False)
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
    order_number = db.Column(db.Integer, nullable=False, default=0)