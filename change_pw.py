from flask_bcrypt import Bcrypt
from views import app
from models import db, User

bcrypt = Bcrypt(app)

with app.app_context():
    user = User.query.filter_by(username="admin").first()
    user.password_hash = bcrypt.generate_password_hash("pw").decode("utf-8")
    print(f"Password changed")
    db.session.commit()