"""Einmaliges Migrationsskript: entfernt die nicht mehr genutzte Spalte
event_type aus der Tabelle event (das Feld wurde aus dem Portal entfernt,
Terminart wird nicht mehr erfasst).

Ausfuehren mit: docker compose exec web python drop_event_type_column.py
Danach diese Datei wieder aus dem Repository entfernen (gleiche Konvention
wie bei den vorherigen Einmal-Skripten).
"""

from sqlalchemy import text

from views import app
from models import db

with app.app_context():
    db.session.execute(text("ALTER TABLE event DROP COLUMN IF EXISTS event_type"))
    db.session.commit()
    print("Fertig. Spalte event_type wurde aus der Tabelle event entfernt.")
