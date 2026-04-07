from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    contents = db.relationship('Content', backref='author', lazy=True)
    password_hash = db.Column(db.String(255), nullable=False)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    c_type = db.Column(db.String(50))
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