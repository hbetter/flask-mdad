"""Einmaliges Migrationsskript: legt Termin-Objekte (Event) mit den echten,
aktuell auf https://mensch-denk-an-dich.de/ veroeffentlichten Terminen an
(Stand: Abruf am 12.09.2026):

- Impulsworkshop, fuenf Termine (https://mensch-denk-an-dich.de/, Abschnitt
  "Offene Spieletermine")
- Spiele Coach Qualifizierung, drei Termine (Unterseite "Werde Spiele Coach")

Bereits vorhandene Termine mit gleichem Titel und Datum/Uhrzeit werden
uebersprungen, damit das Skript gefahrlos mehrfach ausgefuehrt werden kann.

Ausfuehren mit: docker compose exec web python add_real_events.py
Danach diese Datei wieder aus dem Repository entfernen (gleiche Konvention
wie bei den vorherigen Einmal-Skripten).
"""

from datetime import datetime, timezone

from views import app
from models import db, Event, User


REAL_EVENTS = [
    dict(
        title="Impulsworkshop Berlin",
        event_type="in_person",
        category="workshop",
        subtitle="Interaktives Brettspiel MENSCH DENK AN DICH® live erleben, für 6–10 Personen.",
        starts_at=datetime(2026, 9, 22, 17, 0),
        location="Berlin",
    ),
    dict(
        title="Impulsworkshop Essen",
        event_type="in_person",
        category="workshop",
        subtitle="Interaktives Brettspiel MENSCH DENK AN DICH® live erleben, für 6–10 Personen.",
        starts_at=datetime(2026, 10, 28, 16, 0),
        location="Essen",
    ),
    dict(
        title="Impulsworkshop Berlin",
        event_type="in_person",
        category="workshop",
        subtitle="Interaktives Brettspiel MENSCH DENK AN DICH® live erleben, für 6–10 Personen.",
        starts_at=datetime(2027, 1, 21, 17, 0),
        location="Berlin",
    ),
    dict(
        title="Impulsworkshop Berlin",
        event_type="in_person",
        category="workshop",
        subtitle="Interaktives Brettspiel MENSCH DENK AN DICH® live erleben, für 6–10 Personen.",
        starts_at=datetime(2027, 3, 9, 17, 0),
        location="Berlin",
    ),
    dict(
        title="Impulsworkshop Berlin",
        event_type="in_person",
        category="workshop",
        subtitle="Interaktives Brettspiel MENSCH DENK AN DICH® live erleben, für 6–10 Personen.",
        starts_at=datetime(2027, 9, 9, 17, 0),
        location="Berlin",
    ),
    dict(
        title="Spiele Coach Qualifizierung",
        event_type="in_person",
        category="coach_certification",
        subtitle="2-tägige Qualifizierung zum zertifizierten Spiele Coach. 1. Tag 09:00–18:00 Uhr, 2. Tag 09:00–16:00 Uhr.",
        starts_at=datetime(2026, 10, 23, 9, 0),
        location="SMEO GmbH, Danckelmannstr. 54, Berlin",
    ),
    dict(
        title="Spiele Coach Qualifizierung",
        event_type="in_person",
        category="coach_certification",
        subtitle="2-tägige Qualifizierung zum zertifizierten Spiele Coach. 1. Tag 09:00–18:00 Uhr, 2. Tag 09:00–16:00 Uhr.",
        starts_at=datetime(2027, 2, 12, 9, 0),
        location="SMEO GmbH, Danckelmannstr. 54, Berlin",
    ),
    dict(
        title="Spiele Coach Qualifizierung",
        event_type="in_person",
        category="coach_certification",
        subtitle="2-tägige Qualifizierung zum zertifizierten Spiele Coach. 1. Tag 09:00–18:00 Uhr, 2. Tag 09:00–16:00 Uhr.",
        starts_at=datetime(2027, 6, 25, 9, 0),
        location="SMEO GmbH, Danckelmannstr. 54, Berlin",
    ),
]


with app.app_context():
    user = User.query.first()
    if user is None:
        raise SystemExit(
            "Kein Nutzer in der Datenbank gefunden - Termine koennen ohne "
            "user_id nicht angelegt werden."
        )

    created = 0
    for data in REAL_EVENTS:
        exists = Event.query.filter_by(
            title=data["title"], starts_at=data["starts_at"]
        ).first()
        if exists:
            print(f"Bereits vorhanden, uebersprungen: {data['title']} ({data['starts_at']})")
            continue
        event = Event(
            all_day=False,
            user_id=user.id,
            updated_at=datetime.now(timezone.utc),
            **data,
        )
        db.session.add(event)
        created += 1
        print(f"Angelegt: {data['title']} ({data['starts_at']})")

    db.session.commit()
    print(f"Fertig. {created} neue(r) Termin(e) angelegt.")
