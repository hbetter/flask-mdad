from views import app
from models import db, User, Content
from flask_bcrypt import Bcrypt

with app.app_context():
    db.create_all()
    print("Datenbank-Tabellen wurden erfolgreich erstellt!")

    password_hash = bcrypt.generate_password_hash("pw").decode("utf-8")
    admin = User(username="admin", password_hash=password_hash)
    db.session.add(admin)
    db.session.commit()
    print(f"Nutzer angelegt mit ID: {admin.id}")