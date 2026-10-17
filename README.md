# MENSCH DENK AN DICH® – Playful Future (flask-mdad)

Flask-Website für MENSCH DENK AN DICH® mit Bedienfeld zur Pflege von Beiträgen, Terminen und Sektionen. Die Inhalte der öffentlichen Seiten sind teils fest in den Templates, teils werden sie über das Bedienfeld aus der Datenbank gespeist.

## Start mit Docker

PostgreSQL-Container (`db`, Postgres 15) und App-Container (`web`). Die App ist unter http://127.0.0.1:5001 erreichbar (Host-Port 5001 → Container-Port 5000). Im Produktionsmodus ist der Port nur lokal freigegeben (`127.0.0.1:5001`); von außen ist die App ausschließlich über Nginx erreichbar (`nginx/playfulfuture.de.conf`).

```bash

## debug mode, uses docker-compose.yml and docker-compose.override.yml
$ docker build -t flask-mdad:latest .
$ docker compose up -d

## production mode (gunicorn)
$ docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

$ docker compose exec web python init_db.py

```

Im Debug-Modus wird der Projektordner in den Container eingebunden (`.:/app`), Änderungen an Code und Templates sind daher ohne Neubau sofort wirksam.

`init_db.py` legt bei einer leeren Datenbank alle Tabellen an und erzeugt den Nutzer `admin` mit dem Passwort `pw`. Nur einmal bei einer frischen Datenbank ausführen – ein zweiter Aufruf scheitert, weil es den Nutzer `admin` dann schon gibt. `change_pw.py` setzt das Passwort von `admin` wieder auf `pw` zurück.

Die Datenbank liegt in `data/postgres`, hochgeladene Bilder in `data/uploads` (ausgeliefert unter `/uploads/<dateiname>`). Beide Ordner sind nicht im Git-Repository und werden nicht ins Docker-Image kopiert (`.dockerignore`); im Produktionsmodus ist `data/uploads` als Volume eingebunden, damit Bilder Neustarts überstehen und Nginx sie direkt ausliefern kann.

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
- `models.py`: SQLAlchemy-Modelle `User`, `Article`, `Section`, `Event`.
- `images.py`: Verarbeitung der Beitragsbilder (Verkleinern ohne Zuschnitt, Logo-Erkennung, Wahl der Darstellung) – genutzt vom Bedienfeld und vom CSV-Import.
- `csv_transfer.py`: CSV-Import und -Export für Beiträge, Termine und Sektionen (siehe unten), auch als Kommandozeilenwerkzeug.
- `templates/`: Jinja-Templates. `base.html` enthält Navbar, Footer und die zentralen ActiveCampaign-Formular-Modals; `_articles_list.html` und `_sections_list.html` sind die wiederverwendeten Listen-Partials.
- `static/`: `bootstrap.min.css`, `custom.css`, `ac-formulare.css`/`ac-formulare.js` (Styling und Skript der AC-Formulare), Bilder und Favicon. Bilder aus dem Bedienfeld liegen nicht hier, sondern in `data/uploads`. Bootstrap Icons und die Schrift Open Sans werden aus dem Internet geladen.
- `docs/`: Dokumentation der Indexseite (Inhalt und Stil) und Sicherung der Erfolgsgeschichten-Texte.
- `equipe-pq/`: eigenständige statische Landingpage für equipe-pq.playfulfuture.de (siehe unten).
- `mensch-pflege/`: eigenständige statische Landingpage für das Projekt MENSCH PFLEGE! auf mensch-pflege.playfulfuture.de (siehe unten).
- `nginx/`: Nginx-Konfigurationen für die statischen Seiten und playfulfuture.de.
- `logos_download/`: Hilfsskripte zum Herunterladen der „Bekannt aus"-Logos und zum Erzeugen des Logo-Banners.

### Namenskonvention

Code-Bezeichner sind englisch, sichtbare Inhalte deutsch. Template-Dateinamen, View-Funktionen, URL-Routen und Modellfelder werden englisch benannt (`/consulting`, `academy.html`, `on_stories`). Seitentexte, UI-Labels und Code-Kommentare bleiben deutsch. Neue Seiten und Felder gleich englisch anlegen. Template-Dateien nur mit `git mv` umbenennen, damit die Historie erhalten bleibt.

## Datenmodell

- `User`: Benutzername und Passwort-Hash (bcrypt).
- Beitrag (`Article`): Titel, Text, Beschreibung, optional ein Bild, Reihenfolge (`order_number`) und Spaltenbreite (`col_size`). Unabhängige Tickboxen `on_index`, `on_consulting`, `on_academy`, `on_stories` – ein Beitrag kann auf mehreren Seiten erscheinen. `is_banner` markiert höchstens einen Beitrag als Banner.
- Sektion (`Section`): wie ein Beitrag, zusätzlich mit Kicker und Bildposition (links/rechts), aber ohne Banner, Erfolgsgeschichten und Spaltenbreite. Sektionen werden je Seite in nummerierte Plätze („Slots") zwischen den festen Inhalten eingefügt (Indexseite 10, Beratung 4, Akademie 3).
- Termin (`Event`): Titel, Untertitel, Kategorie, Ort, Start und Ende (mit Uhrzeit oder ganztägig).

**Beitragsbilder** werden nicht zugeschnitten, sondern nur auf höchstens 1600 px verkleinert und als WebP gespeichert (Transparenz bleibt erhalten). Wie ein Bild in der Kachel erscheint, legt das Feld `image_fit` fest – im Formular „Bilddarstellung“, jederzeit änderbar:

- `cover` – Foto füllt die Kachel; der Ausschnitt sitzt leicht oberhalb der Mitte, wo meist Gesichter sind.
- `contain` – Bild vollständig mit Rand, für Logos und Grafiken. Einfarbige oder transparente Ränder werden dabei entfernt, damit das Logo nicht zu klein wirkt.
- `blur` – Foto vollständig vor einem unscharfen Hintergrund aus demselben Bild, für Hochkant- oder quadratische Fotos.
- „Automatisch“ (Standard) wählt beim Speichern: Logo/Grafik (Transparenz, einfarbiger Rand, wenige Farben oder Dateiname mit „logo“, „award“, „preis“ …) → `contain`; Foto, das beim Zuschneiden mehr als 40 % verlieren würde → `blur`; sonst `cover`.

**Sektionsbilder** werden weiterhin beim Upload zugeschnitten (Querformat 1280 × 715 oder Hochformat 900 × 1200). Erlaubt sind PNG, JPG, GIF und WebP bis 16 MB.

## Öffentliche Seiten

- `/` – Indexseite mit Beiträgen, Terminen und Sektionen
- `/consulting` (Beratung) und `/academy` (Akademie) – Hero, statische Platzhaltersektionen und die jeweils markierten Beiträge und Sektionen
- `/stories` – Erfolgsgeschichten (Beiträge)
- `/imprint`, `/privacy` – Impressum, Datenschutz
- `/sitemap.xml`, `robots.txt`

## Bedienfeld

Login unter `/login`, danach `/dashboard`. Das Bedienfeld hat drei Reiter – Beiträge, Termine und Sektionen –, jeweils mit eigenem Button zum Hinzufügen; Export und Import stehen daneben. Der zuletzt gewählte Reiter wird gemerkt und lässt sich auch direkt verlinken (`/dashboard#articles`, `#events`, `#sections`). Ein Klick auf eine Kachel öffnet ein Schnellbearbeitungs-Modal für die Platzierung auf den öffentlichen Seiten.

Begriffe: Beiträge, Termine und Sektionen entsprechen im Code den Modellen `Article`, `Event` und `Section` und in den CSV-Dateien `articles.csv`, `events.csv` und `sections.csv`. In Code-Kommentaren heißen Beiträge „Beitragkarten“.

Terminkategorien: Webinar, Probe Spielraum, Spiele Coach Zertifizierung, Spiele Event. Jede Kategorie hat in der Anzeige eines Termins ein dezentes Hintergrund-Icon. Beim Anlegen eines Termins wird der Titel mit der Kategorie vorbelegt, sofern noch kein eigener Titel eingetragen ist.

## ActiveCampaign-Formulare

Fünf AC-Formulare sind als Bootstrap-Modals in `base.html` eingebunden und von jeder Seite aus aufrufbar: Spielraum (Formular 16), Spiele Coach (8), Spiele Event (11), Newsletter (14) und Webinar (22). Der Button „Platz sichern" bei einem Termin öffnet je nach Kategorie das passende Formular. Für Kategorien ohne eigenes Formular springt er zum Kontaktbereich.

`templates/alle_ac_formulare.html` ist eine Sammelseite ohne Route, die direkt als Datei im Browser geöffnet wird. Sie bindet CSS und JS deshalb mit relativen Pfaden statt mit `url_for()` ein.

## CSV-Import und -Export

Beiträge, Termine und Sektionen lassen sich als CSV-Dateien exportieren und wieder importieren, etwa um Inhalte vor einem Neuaufbau der Datenbank zu sichern oder zwischen Entwicklung und Produktion zu übertragen. Die Logik steckt in `csv_transfer.py`.

Ein Export-/Importordner enthält `articles.csv`, `sections.csv` und `events.csv` sowie alle Bilder, auf die die Spalte `image_filename` verweist – im selben Ordner. Format wie in flask-crm: Semikolon als Trennzeichen, UTF-8 (mit BOM, damit Excel Umlaute korrekt zeigt). Ja/Nein-Felder als `1`/`0`, Datum und Uhrzeit in deutscher Ortszeit als `JJJJ-MM-TT HH:MM`.

Im Bedienfeld:

- **Export** zeigt zuerst eine Rückfrage mit der Anzahl der Beiträge, Termine und Sektionen und lädt nach Bestätigung ein ZIP mit allen drei CSV-Dateien und den Bildern herunter. Fehlt ein Bild in `static/uploads`, steht das in `export_hinweise.txt` im ZIP.
- **Import** öffnet ein Fenster, in dem ein ganzer Ordner (CSV-Dateien und Bilder) oder ein Export-ZIP ausgewählt wird. Schlägt der Import fehl, öffnet sich das Fenster erneut mit den Fehlermeldungen. Uploads sind auf insgesamt 16 MB begrenzt.

Auf der Kommandozeile (ohne Größenbegrenzung):

```bash
$ docker compose exec web python csv_transfer.py export export-ordner
$ docker compose exec web python csv_transfer.py import export-ordner [--user admin]
```

Regeln beim Import:

- Es werden immer neue Einträge angelegt, bestehende bleiben unverändert. Ein wiederholter Import erzeugt Duplikate. Die Spalte `id` dient nur zur Orientierung und wird ignoriert.
- Alles oder nichts: Enthält eine Zeile einen Fehler, wird nichts gespeichert; die Fehlermeldungen nennen Datei und Zeile.
- Pflichtspalten: `title` und `body` bei Beiträgen und Sektionen; `title`, `category`, `starts_at`, `ends_at` und `location` bei Terminen. Alle übrigen Spalten dürfen fehlen. Fehlt eine der drei Dateien, wird sie übersprungen.
- `category` ist einer der internen Werte `webinar`, `inhouse`, `certification`, `trial`.
- Ordnungsnummern von Beiträgen werden in 10er-Schritten neu vergeben (10, 20, 30, …), damit dazwischen Platz für spätere Beiträge bleibt. Die Reihenfolge folgt der `order_number` in der CSV (bei Gleichstand der Zeilenreihenfolge); importierte Beiträge werden hinter die vorhandenen gestellt.
- Höchstens ein Beitrag darf `is_banner = 1` haben, und nur wenn noch kein Banner existiert.
- Sektionen werden über `slot_index_*`/`slot_position_*` in die Slots eingereiht. Sektionen, die schon im selben Slot stehen, bleiben davor.
- Texte werden bereinigt: Im Inhalt (`body`) werden `<p>`, `<br>`, `<div>`, Überschriften und Listen durch Zeilenumbrüche ersetzt (Listenpunkte als „•“), alle übrigen Tags entfernt. Erhalten bleiben nur Fett (`<strong>`), Kursiv (`<em>`) und Links (`<a href>`). Titel, Untertitel, Kicker, Beschreibung und Ort werden zu reinem Text. Das `##` für den Anreißer steht danach in einer eigenen Zeile.
- Bilder werden mit neuem Dateinamen nach `data/uploads` übernommen. Bei Beiträgen steuert die Spalte `image_fit` (`auto` bzw. leer, `cover`, `contain`, `blur`) die Darstellung wie im Formular; Bei Sektionen schneidet die optionale Spalte `image_orientation` (`landscape` oder `portrait`) das Bild wie beim Upload im Bedienfeld zu; leer lassen, um es unverändert zu übernehmen (so beim Export). Bei Beiträgen wird `image_orientation` ignoriert.
- Autor der importierten Einträge ist der angemeldete Nutzer (Kommandozeile: `--user`, Standard `admin`).

## equipe-pq

Der Ordner `equipe-pq/` enthält eine eigenständige statische Seite für equipe-pq.playfulfuture.de. Sie wird nicht von Flask, sondern direkt von Nginx ausgeliefert. Einrichtung, Rechte und HTTPS sind als Kommentar in `nginx/equipe-pq.playfulfuture.de.conf` beschrieben. Nginx gibt nur diesen Unterordner frei, der Rest des Repositorys bleibt unerreichbar.

## mensch-pflege

Der Ordner `mensch-pflege/` enthält die statische Landingpage für MENSCH PFLEGE!, ein Modellvorhaben der BARMER und der SMEO GmbH in der stationären Pflege (Laufzeit Oktober 2024 bis September 2027). Die Seite ist ursprünglich eine Kopie von `equipe-pq/`, hat inzwischen aber eigene Inhalte, ein eigenes Logo-Set und eine eigene `custom.css`. Wie equipe-pq wird sie nicht von Flask, sondern direkt von Nginx ausgeliefert; Einrichtung, Rechte und HTTPS stehen als Kommentar in `nginx/mensch-pflege.playfulfuture.de.conf`. Nginx gibt nur diesen Unterordner frei.

- Seiten: `index.html` (One-Pager), `impressum.html`, `datenschutz.html`. Navbar und Footer sind in allen drei Dateien gleich und müssen bei Änderungen in allen drei nachgezogen werden.
- Navbar: SMEO-Logo links, rundes MENSCH-PFLEGE!-Logo mittig (ragt etwa zu einem Drittel über den unteren Rand), BARMER-Logo rechts.
- Sektionen der Startseite: Hero („Worum es geht“, Fotos, Zitat Christine Witte/BARMER, Kontakt-Button an mensch.pflege@smeo-now.de), „Feedback aus den Einrichtungen“ (Kicker „Die 3 Häuser“; je Haus eine Karte mit Träger und Ort, ein Klick öffnet ein Modal mit Zitaten von Einrichtungsleitungen und Qualitätsbeauftragten), „Die Intervention“, „Eindrücke der Prozessberaterinnen“, „Die Evaluation“, „Kooperationspartnerinnen“. Jede Sektion hat darüber einen HTML-Kommentar mit Name und Aufbau.
- Bilder: Eingebunden werden nur verkleinerte Webfassungen (`*-web.jpg`, `*-web.webp`, bereinigte SVGs wie `hand-in-hand.svg`, `mp-schriftzug-claim.svg`). Große Originale (Fotos, PNGs, Inkscape-SVGs) werden nicht committet, da alles im Ordner öffentlich abrufbar ist.
- CSS-Klassen für Fotos richten sich nach dem Format: `hero-photo-portrait` (Hochformat) und `hero-photo-landscape` (Querformat); freigestellte Figuren nutzen `hero-figure`.
- Barrierefreiheit: geprüft nach WCAG 2.2 AA mit axe-core (keine Verstöße). Skip-Link, `<main>` auf allen Seiten, sichtbarer Tastaturfokus, Kontraste ≥ 4,5:1, Ankündigung neuer Fenster, `prefers-reduced-motion`. Bei Änderungen erhalten.
- Kein Build-Schritt: Bootstrap 5 und Bootstrap Icons kommen per CDN, Änderungen an HTML/CSS sind sofort wirksam.

## Datensicherung und Grenzen

Regelmäßig sichern: den Datenbank-Dump (siehe oben) und den Ordner `data/uploads`. Der Dump enthält nur die Dateinamen der Bilder, nicht die Bilder selbst. Der CSV-Export enthält Inhalte und Bilder, aber keine Nutzer und ersetzt daher kein vollständiges Backup.

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
