"""Rollen, Zugriffsschutz und Passwort-Richtlinie.

admin_required schuetzt alle Seiten, die nur der Admin sehen darf
(Administration, Nutzerverwaltung, Portalkonfiguration). Nicht angemeldete
Besucher landen wie bei login_required auf der Login-Seite, angemeldete
Mitglieder bekommen 403.

Die Passwort-Richtlinie wird in der Portalkonfiguration eingestellt
(PortalSettings.password_*) und gilt fuer jedes neu gesetzte Passwort.
"""

from functools import wraps

from flask import abort
from flask_login import current_user, login_required

DEFAULT_MIN_PASSWORD_LENGTH = 10
SPECIAL_CHARACTERS_HINT = "z. B. ! ? # % & * -"

# Zeichenklassen: Feld in PortalSettings, Pruefung, Text fuer Hinweise
CHARACTER_RULES = [
    ("password_require_lower", lambda ch: ch.islower(), "einen Kleinbuchstaben"),
    ("password_require_upper", lambda ch: ch.isupper(), "einen Großbuchstaben"),
    ("password_require_digit", lambda ch: ch.isdigit(), "eine Ziffer"),
    ("password_require_special", lambda ch: not ch.isalnum() and not ch.isspace(), "ein Sonderzeichen"),
]


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)

    return wrapped


def password_policy():
    """Aktuelle Richtlinie als dict: min_length und die geforderten
    Zeichenklassen (Liste der Texte)."""
    from mailer import get_settings  # spaet importieren (App-Kontext, kein Zirkelimport)

    settings = get_settings()
    min_length = settings.password_min_length or DEFAULT_MIN_PASSWORD_LENGTH
    required = [(field, test, text) for field, test, text in CHARACTER_RULES if getattr(settings, field)]
    return {"min_length": min_length, "rules": required}


def describe_policy(policy=None):
    """Kurzer Hinweistext, z. B. "Mindestens 12 Zeichen, davon mindestens
    eine Ziffer und ein Sonderzeichen." """
    policy = policy or password_policy()
    text = f"Mindestens {policy['min_length']} Zeichen"
    parts = [label for _, _, label in policy["rules"]]
    if parts:
        joined = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " und " + parts[-1]
        text += f", davon mindestens {joined}"
    return text + "."


def password_problem(password, confirm):
    """Liefert eine Fehlermeldung oder None, wenn das Passwort passt."""
    password = password or ""
    policy = password_policy()
    missing = [label for _, test, label in policy["rules"] if not any(test(ch) for ch in password)]
    if len(password) < policy["min_length"] or missing:
        return "Das Passwort erfüllt die Vorgaben nicht. " + describe_policy(policy)
    if password != confirm:
        return "Die beiden Passwörter stimmen nicht überein."
    return None
