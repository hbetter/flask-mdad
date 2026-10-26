"""Mailversand ueber die SMTP-Daten aus der Portalkonfiguration.

Das SMTP-Passwort wird mit Fernet (cryptography) verschluesselt in der
Datenbank gespeichert. Der Schluessel wird aus dem SECRET_KEY abgeleitet:
Wird der SECRET_KEY geaendert, laesst sich das gespeicherte Passwort nicht
mehr entschluesseln und muss in der Portalkonfiguration neu eingetragen
werden.
"""

import base64
import hashlib
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr

from cryptography.fernet import Fernet, InvalidToken
from flask import current_app

from models import db, PortalSettings

SMTP_SECURITY_CHOICES = [
    ("starttls", "STARTTLS (meist Port 587)"),
    ("ssl", "SSL/TLS (meist Port 465)"),
    ("none", "Keine Verschlüsselung (nicht empfohlen)"),
]
SMTP_TIMEOUT = 20
# Ueblicher Port je Verschluesselung, wenn beim Speichern keiner angegeben ist
DEFAULT_PORTS = {"starttls": 587, "ssl": 465, "none": 25}


class MailError(Exception):
    pass


def _fernet():
    digest = hashlib.sha256(
        ("smtp-password:" + current_app.config["SECRET_KEY"]).encode("utf-8")
    ).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


def encrypt_secret(value):
    return _fernet().encrypt(value.encode("utf-8")).decode("ascii")


def decrypt_secret(token):
    if not token:
        return ""
    try:
        return _fernet().decrypt(token.encode("ascii")).decode("utf-8")
    except InvalidToken:
        raise MailError(
            "Das gespeicherte SMTP-Passwort kann nicht entschlüsselt werden "
            "(vermutlich wurde der SECRET_KEY geändert). Bitte in der "
            "Portalkonfiguration neu eintragen."
        )


def get_settings():
    """Liefert den einen Konfigurationsdatensatz und legt ihn bei Bedarf an."""
    settings = db.session.get(PortalSettings, 1)
    if settings is None:
        settings = PortalSettings(id=1)
        db.session.add(settings)
        db.session.commit()
    return settings


def missing_settings(settings=None):
    """Bezeichnungen der Pflichtangaben, die fuer den Versand noch fehlen."""
    settings = settings or get_settings()
    missing = []
    if not settings.smtp_host:
        missing.append("SMTP-Server")
    if not settings.smtp_port:
        missing.append("Port")
    if not settings.mail_from_address:
        missing.append("Absenderadresse")
    return missing


def is_configured(settings=None):
    return not missing_settings(settings)


def send_mail(to, subject, body):
    """Verschickt eine Text-Mail. Wirft MailError mit verstaendlicher Meldung."""
    settings = get_settings()
    if not is_configured(settings):
        raise MailError("Der Mailversand ist noch nicht eingerichtet (Portalkonfiguration).")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((settings.mail_from_name or "", settings.mail_from_address))
    msg["To"] = to
    msg.set_content(body)

    password = decrypt_secret(settings.smtp_password_encrypted)
    try:
        if settings.smtp_security == "ssl":
            server = smtplib.SMTP_SSL(
                settings.smtp_host, settings.smtp_port,
                timeout=SMTP_TIMEOUT, context=ssl.create_default_context(),
            )
        else:
            server = smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=SMTP_TIMEOUT)
        with server:
            if settings.smtp_security == "starttls":
                server.starttls(context=ssl.create_default_context())
            if settings.smtp_username:
                server.login(settings.smtp_username, password)
            server.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        raise MailError("Anmeldung am SMTP-Server fehlgeschlagen: Benutzername oder Passwort falsch.")
    except smtplib.SMTPException as e:
        raise MailError(f"Der SMTP-Server hat die Mail abgelehnt: {e}")
    except (OSError, ssl.SSLError) as e:
        raise MailError(
            f"Keine Verbindung zum SMTP-Server {settings.smtp_host}:{settings.smtp_port} "
            f"möglich ({e}). Server, Port und Verschlüsselung prüfen."
        )
