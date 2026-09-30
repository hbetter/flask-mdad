"""Einmaliges Migrationsskript: fuegt die neue Spalte ends_at (Enddatum/-zeit
eines Termins) zur Tabelle event hinzu. Bestehende Termine haben kein
Enddatum in der Datenbank - fuer sie wird ends_at auf den Wert von starts_at
gesetzt (Termin als Zeitpunkt ohne Dauer), damit die Spalte anschliessend
NOT NULL gesetzt werden kann (wie von den anderen Terminfeldern verlangt).

Ausfuehren mit: docker compose exec web python add_ends_at_column.py
Danach diese Datei wieder aus dem Repository entfernen (gleiche Konvention
wie bei den vorherigen Einmal-Skripten).
"""

from sqlalchemy import text

from views import app
from models import db

with app.app_context():
    db.session.execute(text("ALTER TABLE event ADD COLUMN IF NOT EXISTS ends_at TIMESTAMP"))
    db.session.execute(text("UPDATE event SET ends_at = starts_at WHERE ends_at IS NULL"))
    db.session.execute(text("ALTER TABLE event ALTER COLUMN ends_at SET NOT NULL"))
    db.session.commit()
    print("Fertig. Spalte ends_at wurde ergaenzt (bestehende Termine: ends_at = starts_at).")
