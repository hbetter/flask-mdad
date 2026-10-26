"""Rollen und Zugriffsschutz.

admin_required schuetzt alle Seiten, die nur der Admin sehen darf
(Bedienfeld, Nutzerverwaltung, Portalkonfiguration). Nicht angemeldete
Besucher landen wie bei login_required auf der Login-Seite, angemeldete
Mitglieder bekommen 403.
"""

from functools import wraps

from flask import abort
from flask_login import current_user, login_required

MIN_PASSWORD_LENGTH = 10


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)

    return wrapped


def password_problem(password, confirm):
    """Liefert eine Fehlermeldung oder None, wenn das Passwort passt."""
    if len(password or "") < MIN_PASSWORD_LENGTH:
        return f"Das Passwort muss mindestens {MIN_PASSWORD_LENGTH} Zeichen lang sein."
    if password != confirm:
        return "Die beiden Passwörter stimmen nicht überein."
    return None
