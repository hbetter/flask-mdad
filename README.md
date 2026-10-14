# MENSCH DENK AN DICH® – Playful Future (flask-mdad)

Flask-Website für MENSCH DENK AN DICH® mit Bedienfeld zur Pflege von Karten, Sektionen und Terminen. Die Inhalte der öffentlichen Seiten sind teils fest in den Templates, teils werden sie über das Bedienfeld aus der Datenbank gespeist.

## Start mit Docker

PostgreSQL-Container (`db`, Postgres 15) und App-Container (`web`). Die App ist unter http://127.0.0.1:5001 erreichbar (Host-Port 5001 → Container-Port 5000).

```bash
$ docker build -t flask-mdad:latest .
$ docker compose up -d
# debug mode, uses docker-compose.yml and docker-compose.override.yml

$ docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
# production mode (gunicorn)

$ docker compose exec web python init_db.py
```

Im Debug-Modus wird der Projektordner in den Container eingebunden (`.:/app`), Änderungen an Code und Templates sind daher ohne Neubau sofort wirksam.

`init_db.py` legt bei einer leeren Datenbank alle Tabellen an und erzeugt den Nutzer `admin` mit dem Passwort `pw`. Nur einmal bei einer frischen Datenbank ausführen – ein zweiter Aufruf scheitert, weil es den Nutzer `admin` dann schon gibt. `change_pw.py` setzt das Passwort von `admin` wieder auf `pw` zurück.

Die Datenbank liegt in `data/postgres`, hochgeladene Bilder in `static/uploads`. Beide Ordner sind nicht im Git-Repository.

Ohne gesetzte `DATABASE_URL` (also beim Start ohne Docker mit `python app.py`) verwendet die App eine lokale SQLite-Datei `app.db`.

DB backup and restore:

```bash
$ docker compose exec db pg_dump --clean --if-exists -U flaskuser -d flaskdb > dump.sql
$ cat dump.sql | docker compose exec -T db psql -U flaskuser -d flaskdb
```

## Schemaänderungen

Flask-Migrate ist installiert und eingebunden, ein Ordner `migrations/` existiert aber noch nicht. Bisher liefen Schemaänderungen über einmalige Skripte im `web`-Container oder über einen kompletten Neuaufbau der Datenbank (Datenbank löschen, `init_db.py` ausführen). `db.create_all()` legt nur fehlende Tabellen an und verändert keine bestehenden.

Für eine echte Migration:

```bash
$ docker compose exec web flask db init
$ docker compose exec web flask db migrate -m "xyz"
$ docker compose exec web flask db upgrade
```

Vor jeder Schemaänderung ein Backup ziehen (siehe oben).

## Aufbau

- `app.py`: Startpunkt, importiert die App aus `views.py`.
- `views.py`: Konfiguration, alle Routen, Bild-Upload und -Zuschnitt, Jinja-Filter sowie die Konstanten für Seiten-Tickboxen, Terminkategorien, Icons und Formular-Modals.
- `models.py`: SQLAlchemy-Modelle `User`, `Card`, `Section`, `Event`.
- `csv_transfer.py`: CSV-Import und -Export für Karten, Sektionen und Termine (siehe unten), auch als Kommandozeilenwerkzeug.
- `templates/`: Jinja-Templates. `base.html` enthält Navbar, Footer und die zentralen ActiveCampaign-Formular-Modals; `_cards_list.html` und `_sections_list.html` sind die wiederverwendeten Listen-Partials.
- `static/`: `bootstrap.min.css`, `custom.css`, `ac-formulare.css`/`ac-formulare.js` (Styling und Skript der AC-Formulare), Bilder, Favicon sowie `uploads/` für Bilder aus dem Bedienfeld. Bootstrap Icons und die Schrift Open Sans werden aus dem Internet geladen.
- `docs/`: Dokumentation der Indexseite (Inhalt und Stil) und Sicherung der Erfolgsgeschichten-Texte.
- `equipe-pq/` und `nginx/`: eigenständige statische Landingpage für equipe-pq.playfulfuture.de samt Nginx-Konfiguration (siehe unten).
- `logos_download/`: Hilfsskripte zum Herunterladen der „Bekannt aus"-Logos und zum Erzeugen des Logo-Banners.

### Namenskonvention

Code-Bezeichner sind englisch, sichtbare Inhalte deutsch. Template-Dateinamen, View-Funktionen, URL-Routen und Modellfelder werden englisch benannt (`/consulting`, `academy.html`, `on_stories`). Seitentexte, UI-Labels und Code-Kommentare bleiben deutsch. Neue Seiten und Felder gleich englisch anlegen. Template-Dateien nur mit `git mv` umbenennen, damit die Historie erhalten bleibt.

## Datenmodell

- `User`: Benutzername und Passwort-Hash (bcrypt).
- `Card`: Titel, Text, Beschreibung, optional ein Bild, Reihenfolge (`order_number`) und Spaltenbreite (`col_size`). Unabhängige Tickboxen `on_index`, `on_consulting`, `on_academy`, `on_stories` – eine Karte kann auf mehreren Seiten erscheinen. `is_banner` markiert höchstens eine Karte als Banner.
- `Section`: wie `Card`, zusätzlich mit Kicker und Bildposition (links/rechts), aber ohne Banner, Erfolgsgeschichten und Spaltenbreite. Sektionen werden je Seite in nummerierte Plätze („Slots") zwischen den festen Inhalten eingefügt (Indexseite 10, Beratung und Akademie je 3).
- `Event`: Termin mit Titel, Untertitel, Kategorie, Ort, Start und Ende (mit Uhrzeit oder ganztägig).

Das Bildformat (Hoch- oder Querformat) wird nur beim Upload gewählt und nicht gespeichert. Es bestimmt den Zuschnitt: Querformat 1280 × 715, Hochformat 900 × 1200 Pixel. Erlaubt sind PNG, JPG, GIF und WebP bis 16 MB.

## Öffentliche Seiten

- `/` – Indexseite mit Terminen, Karten und Sektionen
- `/consulting` (Beratung) und `/academy` (Akademie) – Hero, statische Platzhaltersektionen und die jeweils markierten Karten und Sektionen
- `/stories` – Erfolgsgeschichten (Karten)
- `/imprint`, `/privacy` – Impressum, Datenschutz
- `/sitemap.xml`, `robots.txt`

## Bedienfeld

Login unter `/login`, danach `/dashboard`. Oben stehen die Buttons zum Anlegen von Karten, Terminen und Sektionen, darunter Termine, Karten und Sektionen als Kacheln. Ein Klick auf eine Kachel öffnet ein Schnellbearbeitungs-Modal für die Platzierung auf den öffentlichen Seiten.

Terminkategorien: Webinar, Probe Spielraum, Spiele Coach Zertifizierung, Spiele Event. Jede Kategorie hat ein dezentes Hintergrund-Icon auf der Terminkarte. Beim Anlegen eines Termins wird der Titel mit der Kategorie vorbelegt, sofern noch kein eigener Titel eingetragen ist.

## ActiveCampaign-Formulare

Fünf AC-Formulare sind als Bootstrap-Modals in `base.html` eingebunden und von jeder Seite aus aufrufbar: Spielraum (Formular 16), Spiele Coach (8), Spiele Event (11), Newsletter (14) und Webinar (22). Der Button „Platz sichern" auf einer Terminkarte öffnet je nach Kategorie das passende Formular. Für Kategorien ohne eigenes Formular springt er zum Kontaktbereich.

`templates/alle_ac_formulare.html` ist eine Sammelseite ohne Route, die direkt als Datei im Browser geöffnet wird. Sie bindet CSS und JS deshalb mit relativen Pfaden statt mit `url_for()` ein.

## CSV-Import und -Export

Karten, Sektionen und Termine lassen sich als CSV-Dateien exportieren und wieder importieren, etwa um Inhalte vor einem Neuaufbau der Datenbank zu sichern oder zwischen Entwicklung und Produktion zu übertragen. Die Logik steckt in `csv_transfer.py`.

Ein Export-/Importordner enthält `cards.csv`, `sections.csv` und `events.csv` sowie alle Bilder, auf die die Spalte `image_filename` verweist – im selben Ordner. Format wie in flask-crm: Semikolon als Trennzeichen, UTF-8 (mit BOM, damit Excel Umlaute korrekt zeigt). Ja/Nein-Felder als `1`/`0`, Datum und Uhrzeit in deutscher Ortszeit als `JJJJ-MM-TT HH:MM`.

Im Bedienfeld:

- **Export** zeigt zuerst eine Rückfrage mit der Anzahl der Karten, Sektionen und Termine und lädt nach Bestätigung ein ZIP mit allen drei CSV-Dateien und den Bildern herunter. Fehlt ein Bild in `static/uploads`, steht das in `export_hinweise.txt` im ZIP.
- **Import** öffnet ein Fenster, in dem ein ganzer Ordner (CSV-Dateien und Bilder) oder ein Export-ZIP ausgewählt wird. Schlägt der Import fehl, öffnet sich das Fenster erneut mit den Fehlermeldungen. Uploads sind auf insgesamt 16 MB begrenzt.

Auf der Kommandozeile (ohne Größenbegrenzung):

```bash
$ docker compose exec web python csv_transfer.py export export-ordner
$ docker compose exec web python csv_transfer.py import export-ordner [--user admin]
```

Regeln beim Import:

- Es werden immer neue Einträge angelegt, bestehende bleiben unverändert. Ein wiederholter Import erzeugt Duplikate. Die Spalte `id` dient nur zur Orientierung und wird ignoriert.
- Alles oder nichts: Enthält eine Zeile einen Fehler, wird nichts gespeichert; die Fehlermeldungen nennen Datei und Zeile.
- Pflichtspalten: `title` und `body` bei Karten und Sektionen; `title`, `category`, `starts_at`, `ends_at` und `location` bei Terminen. Alle übrigen Spalten dürfen fehlen. Fehlt eine der drei Dateien, wird sie übersprungen.
- `category` ist einer der internen Werte `webinar`, `inhouse`, `certification`, `trial`.
- Höchstens eine Karte darf `is_banner = 1` haben, und nur wenn noch kein Banner existiert.
- Sektionen werden über `slot_index_*`/`slot_position_*` in die Slots eingereiht. Sektionen, die schon im selben Slot stehen, bleiben davor.
- Bilder werden mit neuem Dateinamen nach `static/uploads` kopiert. Die optionale Spalte `image_orientation` (`landscape` oder `portrait`) schneidet das Bild wie beim Upload im Bedienfeld zu; leer lassen, um es unverändert zu übernehmen (so beim Export).
- Autor der importierten Einträge ist der angemeldete Nutzer (Kommandozeile: `--user`, Standard `admin`).

## equipe-pq

Der Ordner `equipe-pq/` enthält eine eigenständige statische Seite für equipe-pq.playfulfuture.de. Sie wird nicht von Flask, sondern direkt von Nginx ausgeliefert. Einrichtung, Rechte und HTTPS sind als Kommentar in `nginx/equipe-pq.playfulfuture.de.conf` beschrieben. Nginx gibt nur diesen Unterordner frei, der Rest des Repositorys bleibt unerreichbar.

## Datensicherung und Grenzen

Regelmäßig sichern: den Datenbank-Dump (siehe oben) und den Ordner `static/uploads`. Der Dump enthält nur die Dateinamen der Bilder, nicht die Bilder selbst. Der CSV-Export enthält Inhalte und Bilder, aber keine Nutzer und ersetzt daher kein vollständiges Backup.

Vor einem öffentlichen Betrieb zu beachten:

- `SECRET_KEY` ist fest in `views.py` eingetragen und sollte für die Produktion über eine Umgebungsvariable gesetzt werden.
- Das Standardpasswort `pw` aus `init_db.py` vor dem Livegang ändern.
- Datenbank-Zugangsdaten stehen im Klartext in `docker-compose.yml`.
- Formulare im Bedienfeld haben keinen CSRF-Schutz.
- Es gibt nur einen Nutzer und keine Rollen oder Berechtigungen.
- TLS übernimmt der vorgeschaltete Webserver; die App selbst spricht nur HTTP.

## Prüfung

Automatisierte Tests gibt es noch nicht. Nach Änderungen prüfen:

```bash
$ docker compose exec web python -c "import ast; [ast.parse(open(f).read()) for f in ('views.py', 'models.py')]"
$ docker compose exec web python -c "from jinja2 import Environment; import glob; [Environment().parse(open(f).read()) for f in glob.glob('templates/*.html')]"
```

Anschließend die geänderten Seiten im Browser unter http://127.0.0.1:5001 ansehen, auch in schmaler Fensterbreite für die Mobilansicht.
