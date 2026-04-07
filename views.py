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

from models import db, User, Content


CONTENT_TYPES = {
    "draft": "Entwurf",
    "index_card": "Karteikarte auf Indexseite",
    "journal": "Journalbeitrag",
    "banner": "Bannertext",
}

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
    banner = Content.query.filter_by(c_type="banner").first()
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    banner = get_banner_text()
    index_cards = (
        Content.query
        .filter_by(c_type="index_card")
        .order_by(Content.order_number.asc(), Content.id.asc())
        .all()
    )
    return render_template(
        "index.html",
        index_cards=index_cards,
        content_types=CONTENT_TYPES,
        banner=banner,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")
        user = User.query.filter_by(username="admin").first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Falsches Passwort.", "danger")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    banner = get_banner_text()
    user_content = (
        Content.query
        .filter_by(user_id=current_user.id)
        .order_by(Content.order_number.asc(), Content.id.asc())
        .all()
    )
    index_card_orders = (
        Content.query
        .filter_by(c_type="index_card")
        .order_by(Content.order_number.asc(), Content.id.asc())
        .all()
    )
    return render_template(
        "dashboard.html",
        contents=user_content,
        content_types=CONTENT_TYPES,
        banner=banner,
        index_card_orders=index_card_orders,
    )


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_content():
    if request.method == "POST":
        c_type = request.form.get("c_type")

        if c_type == "banner":
            existing_banner = Content.query.filter_by(c_type="banner").first()
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
                return redirect(url_for("add_content"))
        order_number = int(request.form.get("order_number") or 0)
        if c_type != "index_card":
            order_number = 0

        col_size = request.form.get("col_size") or DEFAULT_COL_SIZE
        if c_type != "index_card":
            col_size = DEFAULT_COL_SIZE

        new_item = Content(
            c_type=c_type,
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

    return render_template("add.html", content_types=CONTENT_TYPES)


@app.route("/edit/<int:content_id>", methods=["GET", "POST"])
@login_required
def edit_content(content_id):
    item = Content.query.get_or_404(content_id)

    if item.author != current_user:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        new_type = request.form.get("c_type")

        if new_type == "banner":
            existing_banner = Content.query.filter(
                Content.c_type == "banner",
                Content.id != item.id,
            ).first()
            if existing_banner:
                flash("Ein Banner existiert bereits.", "warning")
                return redirect(url_for("dashboard"))

        item.c_type = new_type

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
                return redirect(url_for("edit_content", content_id=item.id))

            delete_uploaded_image(item.image_filename)
            item.image_filename = image_filename

        db.session.commit()
        flash("Karte aktualisiert.", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "edit.html",
        content=item,
        content_types=CONTENT_TYPES,
        banner=get_banner_text(),
    )


@app.route("/delete/<int:content_id>", methods=["POST"])
@login_required
def delete_content(content_id):
    item = Content.query.get_or_404(content_id)

    if item.author == current_user:
        delete_uploaded_image(item.image_filename)
        db.session.delete(item)
        db.session.commit()
        flash("Karte gelöscht.", "info")

    return redirect(url_for("dashboard"))


@app.route("/impressum")
def impressum():
    banner = get_banner_text()
    return render_template("impressum.html", banner=banner)


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

    return render_template("sitemap.xml", pages=pages)