"""Nutzerbereich: eigenes Profil, Profilfoto, Passwort, Einladung annehmen,
Passwort vergessen und der oeffentliche Community-Bereich.

Rechte:
- /account/...      nur angemeldet, immer das EIGENE Profil (keine ID in
                    der URL, sondern current_user)
- /invite/..., /password-reset...  ohne Anmeldung, per Token-Link
- /community...     oeffentlich; welche Felder sichtbar sind, entscheidet
                    visible_fields() je nach Betrachter
"""

import hashlib
import os
import re
from datetime import datetime, timezone
from uuid import uuid4

from flask import (
    Blueprint, abort, current_app, flash, redirect, render_template, request, url_for,
)
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from PIL import Image, ImageOps

import mailer
from auth import password_problem
from extensions import limiter
from models import (
    db, Invitation, Profile, User, ROLE_MEMBER,
    PROFILE_FUNCTIONS, VISIBILITY_CHOICES, VISIBILITY_MEMBERS, VISIBILITY_PUBLIC,
)

bp = Blueprint("members", __name__)

AVATAR_SIZE = 600
AVATAR_SUBFOLDER = "avatars"
ALLOWED_PHOTO_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
PASSWORD_RESET_MAX_AGE = 2 * 3600  # Sekunden
# Link zum ersten Passwortsetzen fuer ein vom Admin angelegtes Konto
ACCOUNT_SETUP_MAX_AGE = 14 * 24 * 3600  # Sekunden
VISIBILITY_VALUES = {key for key, _ in VISIBILITY_CHOICES}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
# Felder mit waehlbarer Sichtbarkeit; alle anderen Profilfelder sind immer
# oeffentlich.
VISIBILITY_FIELDS = ("email", "phone", "bio")


# ---------------------------------------------------------------------------
# Hilfsfunktionen (auch von admin.py genutzt)
# ---------------------------------------------------------------------------

def hash_token(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def now_utc():
    # Naiv in UTC, wie die Spalten in der Datenbank (DateTime ohne Zeitzone).
    return datetime.now(timezone.utc).replace(tzinfo=None)


def avatar_path(filename):
    return os.path.join(current_app.config["UPLOAD_FOLDER"], AVATAR_SUBFOLDER, filename)


def save_avatar(file_storage):
    """Schneidet das Foto quadratisch zu, entfernt dabei EXIF-Daten (z. B.
    GPS-Koordinaten) durch Neukodieren und speichert es als WebP.
    Liefert den Dateinamen (relativ zu UPLOAD_FOLDER) oder wirft ValueError."""
    name = file_storage.filename or ""
    if "." not in name or name.rsplit(".", 1)[1].lower() not in ALLOWED_PHOTO_EXTENSIONS:
        raise ValueError("Bitte ein Bild im Format JPG, PNG, GIF oder WebP hochladen.")
    try:
        img = Image.open(file_storage.stream)
        img.load()
        img = ImageOps.exif_transpose(img).convert("RGB")
    except Exception:
        raise ValueError("Die Datei konnte nicht als Bild gelesen werden.")
    img = ImageOps.fit(img, (AVATAR_SIZE, AVATAR_SIZE), Image.LANCZOS, centering=(0.5, 0.4))
    filename = f"{uuid4().hex}.webp"
    img.save(avatar_path(filename), "WEBP", quality=85, method=6)
    return f"{AVATAR_SUBFOLDER}/{filename}"


def delete_avatar(stored_name):
    if not stored_name:
        return
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], stored_name)
    if os.path.exists(path):
        os.remove(path)


def visible_profiles_query():
    """Profile, die im Community-Bereich erscheinen: aktives Konto und Foto."""
    return (
        Profile.query.join(User)
        .filter(User.is_active.is_(True), Profile.photo_filename.isnot(None))
        .order_by(Profile.last_name.asc(), Profile.first_name.asc(), Profile.id.asc())
    )


def viewer_level(viewer=None):
    viewer = viewer if viewer is not None else current_user
    if getattr(viewer, "is_authenticated", False):
        return "admin" if viewer.is_admin else VISIBILITY_MEMBERS
    return VISIBILITY_PUBLIC


def visible_fields(profile, viewer=None):
    """E-Mail, Telefon und Bio, soweit der Betrachter sie sehen darf
    (sonst None). Einzige Stelle, an der die Sichtbarkeitsregel steht."""
    level = viewer_level(viewer)
    values = {"email": profile.user.email, "phone": profile.phone, "bio": profile.bio}
    result = {}
    for field in VISIBILITY_FIELDS:
        visibility = getattr(profile, f"{field}_visibility")
        allowed = (
            level == "admin"
            or visibility == VISIBILITY_PUBLIC
            or (level == VISIBILITY_MEMBERS and visibility == VISIBILITY_MEMBERS)
        )
        result[field] = values[field] if allowed and values[field] else None
    return result


def normalize_website(value):
    value = (value or "").strip()
    if value and not re.match(r"^https?://", value, re.I):
        value = "https://" + value
    return value


def email_taken(email, exclude_user_id=None):
    query = User.query.filter(db.or_(User.email == email, User.username == email))
    if exclude_user_id is not None:
        query = query.filter(User.id != exclude_user_id)
    # Kein Autoflush: das Formular kann gerade halb befuellte, noch nicht
    # gespeicherte Objekte (neues Profil) in der Sitzung haben.
    with db.session.no_autoflush:
        return query.first() is not None


def apply_profile_form(profile, user, form, email=None):
    """Uebernimmt die Profilfelder aus dem Formular. Liefert eine Liste von
    Fehlermeldungen; bei Fehlern bleiben die Objekte unveraendert (der
    Aufrufer committet nur ohne Fehler). email: feste Adresse statt des
    Formularfelds (bei der Einladung)."""
    errors = []
    get = lambda key: (form.get(key) or "").strip()  # noqa: E731

    first_name, last_name, city = get("first_name"), get("last_name"), get("city")
    email = (email or get("email")).lower()
    if not first_name:
        errors.append("Bitte einen Vornamen angeben.")
    if not last_name:
        errors.append("Bitte einen Nachnamen angeben.")
    if not city:
        errors.append("Bitte einen Ort angeben.")
    if not EMAIL_PATTERN.match(email):
        errors.append("Bitte eine gültige E-Mail-Adresse angeben.")
    elif email_taken(email, exclude_user_id=user.id):
        errors.append("Diese E-Mail-Adresse wird bereits von einem anderen Konto verwendet.")
    website = normalize_website(get("website"))
    if website and " " in website:
        errors.append("Die Website-Adresse darf keine Leerzeichen enthalten.")
    if errors:
        return errors

    profile.first_name = first_name[:100]
    profile.last_name = last_name[:100]
    profile.city = city[:120]
    profile.display_name = get("display_name")[:120] or None
    profile.organization = get("organization")[:200] or None
    profile.job_title = get("job_title")[:200] or None
    profile.phone = get("phone")[:60] or None
    profile.bio = get("bio") or None
    profile.website = website[:300] or None
    profile.functions = [key for key in PROFILE_FUNCTIONS if key in form.getlist("functions")]
    for field in VISIBILITY_FIELDS:
        value = form.get(f"{field}_visibility")
        setattr(profile, f"{field}_visibility",
                value if value in VISIBILITY_VALUES else VISIBILITY_MEMBERS)

    user.email = email
    # Mitglieder melden sich mit der E-Mail-Adresse an; der Nutzername wird
    # mitgefuehrt, damit er nicht mit spaeteren Einladungen kollidiert.
    if not user.is_admin:
        user.username = email
    return []


# Zwei Arten von Passwort-Links mit unterschiedlicher Gueltigkeit:
# "password-reset" (Passwort vergessen, 2 Stunden) und "account-setup"
# (vom Admin angelegtes Konto, 14 Tage). Beide fuehren zur selben Seite.
TOKEN_PURPOSES = {"password-reset": PASSWORD_RESET_MAX_AGE, "account-setup": ACCOUNT_SETUP_MAX_AGE}


def _reset_serializer(purpose="password-reset"):
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt=purpose)


def make_password_reset_token(user, purpose="password-reset"):
    # Enthaelt einen Teil des aktuellen Passwort-Hashes: nach dem Setzen
    # eines neuen Passworts ist der Link damit automatisch ungueltig.
    return _reset_serializer(purpose).dumps({"u": user.id, "p": user.password_hash[-16:]})


def load_password_reset_token(token):
    for purpose, max_age in TOKEN_PURPOSES.items():
        try:
            return _reset_serializer(purpose).loads(token, max_age=max_age)
        except (SignatureExpired, BadSignature):
            continue
    return None


def password_link(user, purpose="password-reset"):
    return url_for("members.password_reset", token=make_password_reset_token(user, purpose), _external=True)


@bp.app_context_processor
def inject_member_helpers():
    return {
        "visible_fields": visible_fields,
        "profile_functions": PROFILE_FUNCTIONS,
        "visibility_choices": VISIBILITY_CHOICES,
    }


# ---------------------------------------------------------------------------
# Eigenes Profil
# ---------------------------------------------------------------------------

@bp.route("/account/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = current_user._get_current_object()
    profile = user.profile
    if request.method == "POST":
        if profile is None:
            # Admins haben anfangs kein Profil; es entsteht beim ersten Speichern.
            profile = Profile(user=user, first_name="", last_name="", city="")
            db.session.add(profile)
        errors = apply_profile_form(profile, user, request.form)
        if errors:
            db.session.rollback()
            for message in errors:
                flash(message, "danger")
            return render_template("account/profile.html", profile=profile, form=request.form), 400
        db.session.commit()
        flash("Profil gespeichert.", "success")
        return redirect(url_for("members.profile"))
    return render_template("account/profile.html", profile=profile, form=None)


@bp.route("/account/photo", methods=["POST"])
@login_required
def upload_photo():
    profile = current_user.profile
    if profile is None:
        flash("Bitte zuerst die Pflichtfelder des Profils speichern.", "warning")
        return redirect(url_for("members.profile"))
    file = request.files.get("photo")
    if not file or not file.filename:
        flash("Bitte ein Foto auswählen.", "warning")
        return redirect(url_for("members.profile"))
    try:
        new_name = save_avatar(file)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("members.profile"))
    old_name = profile.photo_filename
    profile.photo_filename = new_name
    db.session.commit()
    delete_avatar(old_name)
    flash("Foto gespeichert. Dein Profil erscheint jetzt im Community-Bereich.", "success")
    return redirect(url_for("members.profile"))


@bp.route("/account/photo/delete", methods=["POST"])
@login_required
def delete_photo():
    profile = current_user.profile
    if profile and profile.photo_filename:
        old_name = profile.photo_filename
        profile.photo_filename = None
        db.session.commit()
        delete_avatar(old_name)
        flash("Foto entfernt. Dein Profil erscheint nicht mehr im Community-Bereich.", "info")
    return redirect(url_for("members.profile"))


@bp.route("/account/password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        if not check_password_hash(current_user.password_hash, request.form.get("current_password", "")):
            flash("Das aktuelle Passwort ist nicht korrekt.", "danger")
        else:
            problem = password_problem(request.form.get("password"), request.form.get("password_confirm"))
            if problem:
                flash(problem, "danger")
            else:
                current_user.password_hash = generate_password_hash(request.form["password"]).decode("utf-8")
                db.session.commit()
                flash("Passwort geändert.", "success")
                return redirect(url_for("members.profile"))
    return render_template("account/password.html")


@bp.route("/account/delete", methods=["POST"])
@login_required
def delete_account():
    user = current_user._get_current_object()
    if user.is_admin:
        flash("Admin-Konten können nicht selbst gelöscht werden.", "warning")
        return redirect(url_for("members.profile"))
    if not check_password_hash(user.password_hash, request.form.get("password", "")):
        flash("Das Passwort ist nicht korrekt, das Konto wurde nicht gelöscht.", "danger")
        return redirect(url_for("members.profile"))
    photo = user.profile.photo_filename if user.profile else None
    logout_user()
    Invitation.query.filter_by(invited_by_id=user.id).update({"invited_by_id": None})
    db.session.delete(user)
    db.session.commit()
    delete_avatar(photo)
    flash("Dein Konto und dein Profil wurden gelöscht.", "info")
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# Einladung annehmen
# ---------------------------------------------------------------------------

def _valid_invitation(token):
    invitation = Invitation.query.filter_by(token_hash=hash_token(token)).first()
    if invitation is None or invitation.used_at is not None or invitation.expires_at < now_utc():
        return None
    return invitation


@bp.route("/invite/<token>", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def accept_invitation(token):
    invitation = _valid_invitation(token)
    if invitation is None:
        return render_template(
            "error.html", code=410,
            message="Dieser Einladungslink ist ungültig, abgelaufen oder wurde bereits verwendet. "
                    "Bitte wende dich an die Person, die dich eingeladen hat.",
        ), 410
    if email_taken(invitation.email):
        return render_template(
            "error.html", code=409,
            message="Für diese E-Mail-Adresse gibt es bereits ein Konto. Bitte melde dich an "
                    "oder nutze „Passwort vergessen“.",
        ), 409

    # Wer noch mit einem anderen Konto angemeldet ist, wird abgemeldet,
    # damit das neue Konto nicht mit der alten Sitzung vermischt wird.
    if current_user.is_authenticated:
        logout_user()

    if request.method == "POST":
        form = request.form
        user = User(username=invitation.email, email=invitation.email, role=ROLE_MEMBER,
                    password_hash="")
        profile = Profile(user=user, first_name="", last_name="", city="")
        # Die E-Mail-Adresse steht durch die Einladung fest.
        errors = apply_profile_form(profile, user, form, email=invitation.email)
        problem = password_problem(form.get("password"), form.get("password_confirm"))
        if problem:
            errors.append(problem)
        if errors:
            db.session.rollback()
            for message in errors:
                flash(message, "danger")
            return render_template("auth/invite.html", invitation=invitation, form=form), 400
        user.password_hash = generate_password_hash(form["password"]).decode("utf-8")
        user.last_login_at = datetime.now(timezone.utc)
        invitation.used_at = now_utc()
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Willkommen! Dein Konto ist angelegt. Lade ein Foto hoch, damit dein Profil im "
              "Community-Bereich erscheint.", "success")
        return redirect(url_for("members.profile"))

    return render_template("auth/invite.html", invitation=invitation, form=None)


# ---------------------------------------------------------------------------
# Passwort vergessen
# ---------------------------------------------------------------------------

@bp.route("/password-reset", methods=["GET", "POST"])
@limiter.limit("5 per minute;20 per hour", methods=["POST"])
def password_reset_request():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        user = User.query.filter_by(email=email).first() if email else None
        if user and user.is_active:
            link = password_link(user)
            body = render_template("mail/password_reset.txt", user=user, link=link,
                                   hours=PASSWORD_RESET_MAX_AGE // 3600)
            try:
                mailer.send_mail(email, "Passwort zurücksetzen", body)
            except mailer.MailError as e:
                current_app.logger.error("Passwort-Mail an %s fehlgeschlagen: %s", email, e)
        # Immer dieselbe Antwort, damit sich nicht herausfinden laesst, welche
        # Adressen ein Konto haben.
        flash("Falls ein Konto mit dieser E-Mail-Adresse existiert, ist ein Link zum Zurücksetzen "
              "unterwegs. Bitte auch den Spam-Ordner prüfen.", "info")
        return redirect(url_for("login"))
    return render_template("auth/password_reset_request.html")


@bp.route("/password-reset/<token>", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def password_reset(token):
    data = load_password_reset_token(token)
    user = db.session.get(User, data.get("u")) if isinstance(data, dict) else None
    if user is None or not user.is_active or user.password_hash[-16:] != data.get("p"):
        return render_template(
            "error.html", code=410,
            message="Dieser Link ist ungültig, abgelaufen oder wurde bereits verwendet. "
                    "Bitte fordere einen neuen an.",
            link=url_for("members.password_reset_request"), link_label="Neuen Link anfordern",
        ), 410
    if request.method == "POST":
        problem = password_problem(request.form.get("password"), request.form.get("password_confirm"))
        if problem:
            flash(problem, "danger")
        else:
            user.password_hash = generate_password_hash(request.form["password"]).decode("utf-8")
            db.session.commit()
            flash("Neues Passwort gespeichert. Du kannst dich jetzt anmelden.", "success")
            return redirect(url_for("login"))
    return render_template("auth/password_reset.html")


# ---------------------------------------------------------------------------
# Community (oeffentlich)
# ---------------------------------------------------------------------------

@bp.route("/community")
def community():
    profiles = visible_profiles_query().all()
    return render_template("community/index.html", profiles=profiles)


@bp.route("/community/<int:profile_id>")
def community_detail(profile_id):
    profile = visible_profiles_query().filter(Profile.id == profile_id).first()
    if profile is None:
        abort(404)
    # ?modal=1: nur der Inhalt, den das Modal auf /community nachlaedt
    template = "community/_profile_view.html" if request.args.get("modal") == "1" else "community/detail.html"
    return render_template(template, profile=profile, fields=visible_fields(profile))
