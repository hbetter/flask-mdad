"""Admin-Bereich: Nutzerverwaltung, Einladungen und Portalkonfiguration.
Alle Routen nur fuer die Rolle "admin" (admin_required)."""

import secrets
from datetime import timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_bcrypt import generate_password_hash
from flask_login import current_user

import mailer
from auth import (
    CHARACTER_RULES, SPECIAL_CHARACTERS_HINT, admin_required, password_problem,
)
from members import (
    ACCOUNT_SETUP_MAX_AGE, EMAIL_PATTERN, apply_profile_form, delete_avatar, email_taken,
    hash_token, now_utc, password_link, save_avatar,
)
from models import db, Invitation, Profile, User, ROLES, ROLE_MEMBER

bp = Blueprint("admin", __name__, url_prefix="/admin")

INVITATION_VALID_DAYS = 14
ROLE_VALUES = {key for key, _ in ROLES}


# ---------------------------------------------------------------------------
# Nutzerverwaltung
# ---------------------------------------------------------------------------

@bp.route("/users")
@admin_required
def users():
    all_users = User.query.order_by(User.role.asc(), User.email.asc(), User.username.asc()).all()
    return render_template("admin/users.html", users=all_users, roles=dict(ROLES))


def _account_email_problem(email, user_id=None):
    if not EMAIL_PATTERN.match(email):
        return "Bitte eine gültige E-Mail-Adresse angeben."
    if email_taken(email, exclude_user_id=user_id):
        return "Diese E-Mail-Adresse wird bereits von einem anderen Konto verwendet."
    return None


def _send_account_mail(user, template, subject, **context):
    """Schickt einen Link zum Passwortsetzen. Liefert eine Fehlermeldung oder None."""
    body = render_template(template, user=user,
                           link=password_link(user, "account-setup"),
                           days=ACCOUNT_SETUP_MAX_AGE // 86400, **context)
    try:
        mailer.send_mail(user.email, subject, body)
    except mailer.MailError as e:
        return str(e)
    return None


@bp.route("/users/new", methods=["GET", "POST"])
@admin_required
def user_new():
    smtp_ready = mailer.is_configured()
    if request.method == "POST":
        form = request.form
        email = (form.get("account_email") or "").strip().lower()
        role = form.get("role")
        password_mode = form.get("password_mode")
        errors = []
        problem = _account_email_problem(email)
        if problem:
            errors.append(problem)
        if role not in ROLE_VALUES:
            errors.append("Bitte eine Rolle auswählen.")
        if password_mode == "set":
            problem = password_problem(form.get("password"), form.get("password_confirm"))
            if problem:
                errors.append(problem)
        elif password_mode == "mail":
            if not smtp_ready:
                errors.append("Für den Link per Mail bitte zuerst den Mailversand in der Portalkonfiguration einrichten.")
        else:
            errors.append("Bitte auswählen, wie das Passwort gesetzt wird.")

        user = User(username=email, email=email, role=role if role in ROLE_VALUES else ROLE_MEMBER,
                    is_active=form.get("is_active") == "1", password_hash="")
        profile = Profile(user=user, first_name="", last_name="", city="")
        if not errors:
            errors = apply_profile_form(profile, user, form, email=email)
        if errors:
            db.session.rollback()
            for message in errors:
                flash(message, "danger")
            return render_template("admin/user_new.html", form=form, roles=ROLES,
                                   smtp_ready=smtp_ready), 400

        if password_mode == "set":
            user.password_hash = generate_password_hash(form["password"]).decode("utf-8")
        else:
            # Unbekanntes Zufallspasswort, bis die Person ueber den Link ein eigenes setzt.
            user.password_hash = generate_password_hash(secrets.token_urlsafe(32)).decode("utf-8")
        db.session.add(user)
        db.session.commit()

        if password_mode == "mail":
            problem = _send_account_mail(user, "mail/account_created.txt",
                                         "Dein Zugang zur MENSCH DENK AN DICH® Community")
            if problem:
                flash(f"Konto angelegt, aber die Mail wurde nicht verschickt: {problem} "
                      "Den Link kannst du hier erneut senden.", "warning")
            else:
                flash(f"Konto angelegt. {email} hat einen Link zum Passwortsetzen bekommen.", "success")
        else:
            flash("Konto angelegt. Bitte das Passwort auf sicherem Weg weitergeben.", "success")
        return redirect(url_for("admin.user_detail", user_id=user.id))

    return render_template("admin/user_new.html", form=None, roles=ROLES, smtp_ready=smtp_ready)


@bp.route("/users/<int:user_id>", methods=["GET", "POST"])
@admin_required
def user_detail(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)
    is_self = user.id == current_user.id

    def render(form=None, profile=None, status=200):
        return render_template(
            "admin/user_detail.html", user=user, profile=profile or user.profile, form=form,
            roles=ROLES, is_self=is_self, smtp_ready=mailer.is_configured(),
            owned_content=_owned_content_count(user),
        ), status

    if request.method == "POST":
        action = request.form.get("action")
        if action == "profile":
            profile = user.profile
            if profile is None:
                profile = Profile(user=user, first_name="", last_name="", city="")
                db.session.add(profile)
            # Die Login-Adresse wird im Kontobereich geaendert, nicht im Profil.
            errors = apply_profile_form(profile, user, request.form, email=user.email or "")
            if errors:
                db.session.rollback()
                for message in errors:
                    flash(message, "danger")
                return render(form=request.form, profile=profile, status=400)
            db.session.commit()
            flash("Profil gespeichert.", "success")
        elif action == "account":
            role = request.form.get("role")
            active = request.form.get("is_active") == "1"
            email = (request.form.get("account_email") or "").strip().lower()
            problem = _account_email_problem(email, user.id) if (email or not user.is_admin) else None
            if is_self and (role != user.role or not active):
                # Sonst kann sich der letzte Admin selbst aussperren.
                flash("Die eigene Rolle und Sperre kannst du nicht ändern.", "warning")
            elif role not in ROLE_VALUES:
                flash("Unbekannte Rolle.", "danger")
            elif problem:
                flash(problem, "danger")
            else:
                user.role = role
                user.is_active = active
                user.email = email or None
                # Wer sich mit der E-Mail-Adresse anmeldet, behaelt sie als
                # Nutzernamen; ein Nutzername wie "admin" bleibt unveraendert.
                if email and "@" in user.username:
                    user.username = email
                db.session.commit()
                flash("Konto gespeichert.", "success")
        elif action == "password":
            problem = password_problem(request.form.get("password"), request.form.get("password_confirm"))
            if problem:
                flash(problem, "danger")
            else:
                user.password_hash = generate_password_hash(request.form["password"]).decode("utf-8")
                db.session.commit()
                flash("Neues Passwort gesetzt. Bitte auf sicherem Weg weitergeben.", "success")
        elif action == "send_link":
            if not user.email:
                flash("Für dieses Konto ist keine E-Mail-Adresse hinterlegt.", "warning")
            else:
                problem = _send_account_mail(user, "mail/password_link.txt", "Passwort für dein Konto setzen")
                if problem:
                    flash(f"Die Mail wurde nicht verschickt: {problem}", "danger")
                else:
                    flash(f"Link zum Passwortsetzen an {user.email} verschickt.", "success")
        return redirect(url_for("admin.user_detail", user_id=user.id))

    return render()


@bp.route("/users/<int:user_id>/photo", methods=["POST"])
@admin_required
def user_photo(user_id):
    """Profilfoto eines Nutzers hochladen bzw. ersetzen (wie /account/photo)."""
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)
    profile = user.profile
    file = request.files.get("photo")
    if profile is None:
        flash("Bitte zuerst die Pflichtfelder des Profils speichern.", "warning")
    elif not file or not file.filename:
        flash("Bitte ein Foto auswählen.", "warning")
    else:
        try:
            new_name = save_avatar(file)
        except ValueError as e:
            flash(str(e), "danger")
        else:
            old_name = profile.photo_filename
            profile.photo_filename = new_name
            db.session.commit()
            delete_avatar(old_name)
            flash("Foto gespeichert." + (" Das Profil erscheint jetzt im Community-Bereich."
                                         if user.is_active else ""), "success")
    return redirect(url_for("admin.user_detail", user_id=user_id))


@bp.route("/users/<int:user_id>/photo/delete", methods=["POST"])
@admin_required
def user_photo_delete(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)
    if user.profile and user.profile.photo_filename:
        old_name = user.profile.photo_filename
        user.profile.photo_filename = None
        db.session.commit()
        delete_avatar(old_name)
        flash("Foto entfernt. Das Profil erscheint nicht mehr im Community-Bereich.", "info")
    return redirect(url_for("admin.user_detail", user_id=user_id))


def _owned_content_count(user):
    return len(user.articles) + len(user.sections) + len(user.events)


@bp.route("/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def user_delete(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)
    if user.id == current_user.id:
        flash("Das eigene Konto kannst du hier nicht löschen.", "warning")
        return redirect(url_for("admin.user_detail", user_id=user.id))
    if _owned_content_count(user):
        flash("Dieses Konto ist Autor von Beiträgen, Sektionen oder Terminen und kann nicht gelöscht "
              "werden. Stattdessen sperren.", "warning")
        return redirect(url_for("admin.user_detail", user_id=user.id))
    name = user.profile.full_name if user.profile else (user.email or user.username)
    photo = user.profile.photo_filename if user.profile else None
    Invitation.query.filter_by(invited_by_id=user.id).update({"invited_by_id": None})
    db.session.delete(user)
    db.session.commit()
    delete_avatar(photo)
    flash(f"Konto von {name} gelöscht.", "info")
    return redirect(url_for("admin.users"))


# ---------------------------------------------------------------------------
# Einladungen
# ---------------------------------------------------------------------------

@bp.route("/invitations", methods=["GET", "POST"])
@admin_required
def invitations():
    settings = mailer.get_settings()
    smtp_ready = mailer.is_configured(settings)

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        if not smtp_ready:
            flash("Bitte zuerst den Mailversand in der Portalkonfiguration einrichten.", "warning")
        elif not EMAIL_PATTERN.match(email):
            flash("Bitte eine gültige E-Mail-Adresse angeben.", "danger")
        elif email_taken(email):
            flash("Für diese E-Mail-Adresse gibt es bereits ein Konto.", "warning")
        else:
            # Offene Einladungen an dieselbe Adresse werden ersetzt.
            Invitation.query.filter_by(email=email, used_at=None).delete()
            token = secrets.token_urlsafe(32)
            invitation = Invitation(
                email=email, token_hash=hash_token(token), invited_by_id=current_user.id,
                expires_at=now_utc() + timedelta(days=INVITATION_VALID_DAYS),
            )
            db.session.add(invitation)
            link = url_for("members.accept_invitation", token=token, _external=True)
            body = render_template("mail/invitation.txt", link=link, days=INVITATION_VALID_DAYS,
                                   note=(request.form.get("note") or "").strip())
            try:
                mailer.send_mail(email, "Einladung zur MENSCH DENK AN DICH® Community", body)
            except mailer.MailError as e:
                db.session.rollback()
                flash(f"Die Einladung wurde nicht verschickt: {e}", "danger")
            else:
                db.session.commit()
                flash(f"Einladung an {email} verschickt.", "success")
        return redirect(url_for("admin.invitations"))

    items = Invitation.query.order_by(Invitation.created_at.desc()).all()
    return render_template("admin/invitations.html", invitations=items, smtp_ready=smtp_ready,
                           now=now_utc(), valid_days=INVITATION_VALID_DAYS)


@bp.route("/invitations/<int:invitation_id>/revoke", methods=["POST"])
@admin_required
def revoke_invitation(invitation_id):
    invitation = db.session.get(Invitation, invitation_id)
    if invitation and invitation.used_at is None:
        db.session.delete(invitation)
        db.session.commit()
        flash("Einladung widerrufen, der Link ist ungültig.", "info")
    return redirect(url_for("admin.invitations"))


# ---------------------------------------------------------------------------
# Portalkonfiguration
# ---------------------------------------------------------------------------

@bp.route("/settings", methods=["GET", "POST"])
@admin_required
def settings():
    config = mailer.get_settings()

    def render(form=None, status=200):
        return render_template("admin/settings.html", portal=config, form=form,
                               security_choices=mailer.SMTP_SECURITY_CHOICES,
                               smtp_ready=mailer.is_configured(config),
                               character_rules=CHARACTER_RULES,
                               special_hint=SPECIAL_CHARACTERS_HINT), status

    if request.method == "POST" and request.form.get("action") == "password_policy":
        length = (request.form.get("password_min_length") or "").strip()
        # Keine Ober- oder Untergrenze ausser: ein Passwort hat mindestens 1 Zeichen
        if not (length.isdigit() and int(length) >= 1):
            flash("Die Mindestlänge muss eine ganze Zahl ab 1 sein.", "danger")
            return render(form=request.form, status=400)
        config.password_min_length = int(length)
        for field, _, _ in CHARACTER_RULES:
            setattr(config, field, request.form.get(field) == "1")
        db.session.commit()
        flash("Passwort-Richtlinie gespeichert. Sie gilt für alle ab jetzt gesetzten Passwörter.", "success")
        return redirect(url_for("admin.settings"))

    if request.method == "POST":
        get = lambda key: (request.form.get(key) or "").strip()  # noqa: E731
        port = get("smtp_port")
        security = get("smtp_security")
        from_address = get("mail_from_address").lower()
        errors = []
        if port and not (port.isdigit() and 0 < int(port) < 65536):
            errors.append("Der Port muss eine Zahl zwischen 1 und 65535 sein.")
        if security not in {key for key, _ in mailer.SMTP_SECURITY_CHOICES}:
            errors.append("Bitte eine Verschlüsselung auswählen.")
        if from_address and not EMAIL_PATTERN.match(from_address):
            errors.append("Die Absenderadresse ist keine gültige E-Mail-Adresse.")
        if errors:
            for message in errors:
                flash(message, "danger")
            return render(form=request.form, status=400)
        config.smtp_host = get("smtp_host") or None
        config.smtp_port = int(port) if port else None
        config.smtp_security = security
        config.smtp_username = get("smtp_username") or None
        config.mail_from_address = from_address or None
        config.mail_from_name = get("mail_from_name") or None
        password = request.form.get("smtp_password") or ""
        if request.form.get("clear_password") == "1":
            config.smtp_password_encrypted = None
        elif password:
            # Leeres Feld = bisheriges Passwort bleibt
            config.smtp_password_encrypted = mailer.encrypt_secret(password)
        db.session.commit()
        flash("Mailversand gespeichert.", "success")
        return redirect(url_for("admin.settings"))
    return render()


@bp.route("/settings/test-mail", methods=["POST"])
@admin_required
def send_test_mail():
    to = (request.form.get("to") or "").strip()
    if not EMAIL_PATTERN.match(to):
        flash("Bitte eine gültige Empfängeradresse für die Testmail angeben.", "danger")
        return redirect(url_for("admin.settings"))
    try:
        mailer.send_mail(to, "Testmail aus der Portalkonfiguration",
                         "Diese Testmail bestätigt, dass der Mailversand funktioniert.\n")
    except mailer.MailError as e:
        flash(f"Testmail fehlgeschlagen: {e}", "danger")
    else:
        flash(f"Testmail an {to} verschickt.", "success")
    return redirect(url_for("admin.settings"))
