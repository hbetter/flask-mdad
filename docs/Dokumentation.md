# CMS flask-mdad – Funktionsweise und Dokumentation

Oct 26, 2026 · @Irene

## Überblick

Das CMS von playfulfuture.de ist eine Flask-Anwendung (Repository `flask-mdad`), mit der Admins Beiträge, Termine und Sektionen der öffentlichen Seiten pflegen und Mitglieder ihr eigenes Profil im Community-Bereich verwalten. Die Seiten sind teils fest in Templates geschrieben, teils werden sie aus der Datenbank befüllt.

Diese Dokumentation hat zwei Teile:

- **Teil A – Anwender:** Bedienung der Administration und des Nutzerbereichs, ohne Programmierkenntnisse.
- **Teil B – Entwickler:** Architektur, Datenmodell, Routen, Templates und Arbeitsregeln.

Stand: 26.10.2026, Commit `24e6e9a`; alle beschriebenen Funktionen sind committet. Der Nutzerbereich kam mit `38b402c`, Nutzermenü und Passwort-Richtlinie mit `5e22e74`, Import/Export der Nutzer mit `730bc4f`, Community-Untertitel, sortierbare Nutzertabelle und Bearbeiten-Stift mit `5dd1ca5`, Textfilter, Testmail-Hinweise und die Umbenennung „Bedienfeld“ → „Administration“ mit `24e6e9a`. Grundlage sind die README, die Übergabedatei `flask-mdad-uebergabe.md` und der Quellcode.

| Begriff in der Oberfläche | Im Code | CSV-Datei |
| --- | --- | --- |
| Beitrag (früher „Karte“) | `Article` | `articles.csv` |
| Sektion | `Section` | `sections.csv` |
| Termin | `Event` | `events.csv` |
| Profil | `Profile` | – |
| Administration (früher „Bedienfeld“ bzw. „Dashboard“) | Route `/dashboard` | – |

## A1 Anmelden und Administration

Die Anmeldung läuft für alle über `/login`; danach landen Admins in der Administration (`/dashboard`) und Mitglieder auf ihrer Profilseite (`/account/profile`).

**Anmelden**

1. `/login` aufrufen.
2. Admins geben ihren Nutzernamen ein (z. B. `admin`), Mitglieder ihre E-Mail-Adresse.
3. Passwort eingeben. Nach zu vielen Fehlversuchen (10 pro Minute, 30 pro Stunde) sperrt die Seite vorübergehend weitere Versuche.
4. Abmelden über das Nutzermenü → „Abmelden“; es sendet ein Formular, ein einfacher Link reicht nicht. Den Link „Anmelden“ gibt es im Footer jeder Seite.

**Die Navigationsleiste** passt sich an: Gäste sehen rechts den Button „Gratis spielen“, der das Spiele-Event-Formular öffnet. Angemeldete sehen dort stattdessen das **Nutzermenü**: ihr Profilfoto bzw. ihre Initialen mit einem Aufklappmenü.

| Eintrag im Nutzermenü | Für wen |
| --- | --- |
| Mein Profil | alle |
| Öffentliche Ansicht (Profil, wie es in der Community erscheint) | alle mit Profil |
| Passwort ändern | alle |
| Administration | nur Admins |
| Abmelden | alle |

Auf dem Handy steht das Nutzermenü als eigener Block im aufgeklappten Hauptmenü.

**Die Administration** hat oben die Reiter Inhalte, Nutzer, Einladungen und Portalkonfiguration. Unter „Inhalte“ gibt es drei Reiter: **Beiträge**, **Termine** und **Sektionen**. Jeder Reiter hat einen eigenen Button zum Hinzufügen; daneben stehen **Export** und **Import**.

- Der zuletzt gewählte Reiter wird gemerkt und lässt sich direkt verlinken: `/dashboard#articles`, `#events`, `#sections`.
- Ein Klick auf eine Kachel öffnet ein Schnellbearbeitungs-Fenster für die Platzierung auf den öffentlichen Seiten (Tickboxen, Reihenfolge, Slot).
- Die Administration zeigt nur die Einträge, die der angemeldete Admin selbst angelegt hat. Export und öffentliche Seiten umfassen dagegen alle Einträge.
- Über die Leiste oben (Inhalte · Nutzer · Einladungen · Portalkonfiguration) erreicht der Admin außerdem **Nutzer**, **Einladungen** und **Portalkonfiguration** (siehe A5).

Mitglieder haben keinen Zugang zur Administration; sie erhalten dort die Fehlerseite 403.

## A2 Beiträge

Ein Beitrag ist eine Kachel im Raster einer Seite; er kann gleichzeitig auf mehreren Seiten erscheinen und hat optional ein Bild und einen „Weiterlesen“-Text.

**Beitrag anlegen:** Administration → Inhalte → Reiter Beiträge → Hinzufügen. Die Felder:

| Feld | Wirkung |
| --- | --- |
| Indexseite / Beratung / Akademie / Erfolgsgeschichten | Unabhängige Tickboxen: auf welchen Seiten der Beitrag erscheint |
| Banner | Macht den Beitrag zum Banner. Höchstens ein Banner gleichzeitig; ein zweiter wird abgelehnt |
| Titel | Pflicht |
| Text | Pflicht. Mit `##` wird der Anreißer abgetrennt (siehe unten) |
| Beschreibung | Kurzbeschreibung, höchstens 300 Zeichen |
| Reihenfolge | Ganze Zahl; kleinere Zahlen stehen weiter vorne. 10er-Schritte lassen Platz für spätere Beiträge |
| Breite | Normal (ein Drittel), Doppelt (zwei Drittel) oder Volle Breite |
| Bild | PNG, JPG, GIF oder WebP, höchstens 16 MB |
| Bilddarstellung | Automatisch, Füllend (`cover`), Vollständig (`contain`) oder Unscharfer Hintergrund (`blur`) |

**Anreißer mit `##`:** Nur der Text vor `##` steht auf der Kachel; der vollständige Text erscheint nach Klick auf „Weiterlesen“ in einem Fenster. Ohne `##` steht der ganze Text auf der Kachel. Tipp: `##` nach ein bis drei Sätzen setzen.

**Textformat:** Zeilenumbrüche bleiben erhalten. HTML wie `<strong>`, `<em>` und `<a href="…">` wird dargestellt.

**Bilder** werden nicht zugeschnitten, nur auf höchstens 1600 px verkleinert und als WebP gespeichert; Transparenz bleibt erhalten. Die Bilddarstellung lässt sich jederzeit ändern:

- **Füllend (`cover`):** Das Foto füllt die Kachel; der Ausschnitt sitzt leicht oberhalb der Mitte, wo meist Gesichter sind.
- **Vollständig (`contain`):** für Logos und Grafiken. Einfarbige oder transparente Ränder werden entfernt, damit das Logo nicht zu klein wirkt.
- **Unscharfer Hintergrund (`blur`):** Foto vollständig vor einer unscharfen Fassung desselben Bildes, für Hochkant- und quadratische Fotos.
- **Automatisch (Standard):** Logo oder Grafik (Transparenz, einfarbiger Rand, wenige Farben oder Dateiname mit „logo“, „award“, „preis“) → `contain`; Foto, das beim Zuschneiden mehr als 40 % verlöre → `blur`; sonst `cover`.

**Bearbeiten und löschen:** Kachel anklicken für die schnelle Platzierung, oder über das Bearbeiten-Formular alle Felder ändern. Beim Löschen wird auch das Bild aus `data/uploads` entfernt.

## A3 Sektionen

Eine Sektion ist ein Abschnitt in voller Breite, der zwischen die festen Inhalte einer Seite eingeschoben wird – an einem nummerierten Platz, dem „Slot“.

Sektionen gibt es nur auf drei Seiten:

| Seite | Anzahl Slots |
| --- | --- |
| Indexseite (`/`) | 10 |
| Beratung (`/consulting`) | 4 |
| Akademie (`/academy`) | 3 |

**So funktionieren Slots:** Slot 1 liegt zwischen dem 1. und 2. festen Abschnitt der Seite, Slot 2 zwischen dem 2. und 3. und so weiter. Ist ein Slot leer, gibt es in der Auswahl nur „Slot 3“. Stehen dort schon Sektionen, bietet die Auswahl jede mögliche Einfügeposition an: „Slot 3a“ (davor), „Slot 3b“ (dahinter) usw. Beim Speichern werden die Positionen im Slot lückenlos neu durchnummeriert.

**Felder einer Sektion:**

- Seiten-Tickboxen Indexseite, Beratung, Akademie, je mit eigenem Slot.
- Kicker (kleine Zeile über der Überschrift), Titel (Pflicht), Text (Pflicht), Beschreibung.
- Bild mit **Bildformat** beim Hochladen: Querformat (zugeschnitten auf 1280 × 715 px) oder Hochformat (900 × 1200 px).
- **Bildposition:** links oder rechts vom Text, unabhängig vom Bildformat.

In der Administration zeigt jede Sektionskachel, wo sie steht, z. B. „Indexseite: Slot 2b“. Ein Klick auf die Kachel öffnet die Schnellplatzierung mit denselben Slot-Optionen wie im vollständigen Formular.

Anders als Beiträge haben Sektionen kein Banner, keine Erfolgsgeschichten-Seite und keine Spaltenbreite.

## A4 Termine

Termine erscheinen chronologisch auf der Indexseite; jeder Termin hat eine Kategorie, die Symbol und Anmeldeformular bestimmt.

**Felder:** Titel, Untertitel, Kategorie, Ort (Pflicht), Start und Ende. Mit „ganztägig“ entfallen die Uhrzeiten. Alle Zeiten gelten in deutscher Ortszeit.

**Kategorien:**

| Kategorie (Anzeige) | Interner Wert | Symbol | „Platz sichern“ öffnet |
| --- | --- | --- | --- |
| Webinar | `webinar` | Videokamera | Webinar-Formular (AC 22) |
| Probe Spielraum | `inhouse` | Haus | Sprung zum Kontaktbereich |
| Spiele Coach Zertifizierung | `certification` | Auszeichnung | Spiele-Coach-Formular (AC 8) |
| Spiele Event | `trial` | Würfel | Spiele-Event-Formular (AC 11) |

Das Symbol steht dezent im Hintergrund der Terminkarte; ein farbiges Kategorie-Etikett gibt es auf den öffentlichen Karten nicht mehr. Beim **Anlegen** wird der Titel daher automatisch mit der gewählten Kategorie vorbelegt, solange noch kein eigener Titel eingetragen ist. Beim Bearbeiten passiert das nicht.

**Datumsanzeige:** Die Seite fasst Start und Ende lesbar zusammen, z. B. „12.11.2026, 10:00 – 11:30“ am selben Tag oder „12.11.2026 – 14.11.2026“ bei mehrtägigen ganztägigen Terminen.

**Vergangene Termine löschen:** Im Reiter Termine zeigt ein Button die Zahl der abgelaufenen Termine und löscht sie alle auf einmal.

## A5 Nutzerbereich, Profile und Community

Mitglieder kommen nur über den Admin ins Portal (per Einladung oder direkt angelegt), pflegen dort ihr eigenes Profil und erscheinen im öffentlichen Community-Bereich, sobald sie ein Profilfoto hochgeladen haben.

### Rollen

| Rolle | Darf |
| --- | --- |
| **Admin** | Website pflegen (Administration), Nutzer verwalten, Einladungen verschicken, Portalkonfiguration ändern, jedes Profil ansehen und bearbeiten |
| **Mitglied** | Nur das eigene Profil, Foto und Passwort ändern und das eigene Konto löschen |

### Ablauf vom Einladen bis zum sichtbaren Profil

1. **Portal einrichten (einmalig, Admin):** Administration → Portalkonfiguration.
   - **Mailversand:** SMTP-Server, Port, Verschlüsselung (STARTTLS, meist Port 587, oder SSL/TLS, meist Port 465), Benutzername, Passwort, Absenderadresse und -name eintragen, speichern und mit „Testmail“ prüfen. Bleibt der Port leer, wird beim Speichern der übliche Port der Verschlüsselung eingetragen (587, bei SSL 465). Solange SMTP-Server, Port oder Absenderadresse fehlen, nennt die Testmail-Karte die fehlenden Angaben statt des Buttons. Ohne Mailversand gibt es keine Einladungen, keine Links zum Passwortsetzen und kein „Passwort vergessen“.
   - **Passwort-Richtlinie:** Mindestlänge (frei wählbar ab 1 Zeichen, Standard 10) und optional je mindestens ein Kleinbuchstabe, Großbuchstabe, eine Ziffer, ein Sonderzeichen. Gilt für jedes neu gesetzte Passwort; bestehende Passwörter bleiben gültig. Die Hinweistexte an allen Passwortfeldern folgen automatisch der Richtlinie.
2. **Zugang schaffen (Admin)**, auf einem von zwei Wegen:
   - **Einladung:** Administration → Einladungen → E-Mail-Adresse und optional eine persönliche Notiz eingeben. Der Link ist **14 Tage** gültig und nur **einmal** nutzbar. Eine neue Einladung an dieselbe Adresse ersetzt eine noch offene; offene Einladungen lassen sich widerrufen. Die Person füllt ihr Profil selbst aus.
   - **Direkt anlegen:** Administration → Nutzer → „Nutzer anlegen“. Der Admin trägt Login-E-Mail, Rolle, Sperre und das Profil ein und wählt, wie das Passwort entsteht: ein selbst festgelegtes **Startpasswort** (auf sicherem Weg weitergeben) oder ein **Link zum Passwortsetzen per Mail** (14 Tage gültig).
3. **Einladung annehmen (Mitglied):** Link öffnen, Pflichtfelder ausfüllen (Vorname, Nachname, Ort), Passwort nach Richtlinie zweimal eingeben. Die E-Mail-Adresse steht durch die Einladung fest. Danach ist das Mitglied angemeldet und landet auf „Mein Profil“. Wer direkt angelegt wurde, meldet sich mit dem Startpasswort an oder setzt sein Passwort über den zugeschickten Link.
4. **Profilfoto hochladen (Mitglied oder Admin):** Erst mit Foto erscheint das Profil unter `/community`. Wird das Foto entfernt, verschwindet das Profil wieder.

### Das eigene Profil (`/account/profile`)

| Feld | Pflicht | Hinweis |
| --- | --- | --- |
| Vorname, Nachname | ja |  |
| Ort | ja |  |
| E-Mail-Adresse | ja | ist zugleich der Anmeldename |
| Anzeigename | nein | ersetzt öffentlich „Vorname Nachname“ |
| Organisation, Position | nein |  |
| Funktion | nein | Mehrfachauswahl: „Spiele Coach“, „MitarbeiterIn SMEO GmbH“ |
| Telefon, Bio, Website | nein | `https://` wird bei der Website ergänzt, falls es fehlt |
| Foto | nein | wird quadratisch auf 600 × 600 px zugeschnitten |

**Sichtbarkeit:** Für E-Mail, Telefon und Bio wählt das Mitglied je Feld, wer sie sieht. Alle anderen Felder sind im Community-Bereich immer öffentlich.

| Einstellung | Gäste | Eingeloggte Mitglieder | Admins |
| --- | --- | --- | --- |
| „Für alle Portalbesucher“ | sichtbar | sichtbar | sichtbar |
| „Nur für eingeloggte Mitglieder“ (Standard) | verborgen | sichtbar | sichtbar |

Über Nutzermenü → **„Öffentliche Ansicht“** sieht das Mitglied sein Profil so, wie es im Community-Bereich erscheint.

**Passwort ändern:** Nutzermenü → „Passwort ändern“ (`/account/password`), aktuelles Passwort plus neues Passwort nach Richtlinie zweimal.

**Konto löschen:** Auf der Profilseite mit dem Passwort bestätigen. Konto, Profil und Foto werden endgültig gelöscht. Admin-Konten können sich nicht selbst löschen.

**Passwort vergessen:** Auf der Login-Seite den Link „Passwort vergessen“ wählen und die E-Mail-Adresse eingeben. Der zugeschickte Link ist **2 Stunden** gültig und wird ungültig, sobald ein neues Passwort gesetzt ist. Die Seite antwortet immer gleich, damit niemand herausfinden kann, welche Adressen ein Konto haben.

### Community-Bereich (`/community`, öffentlich)

- Zeigt Kacheln aller aktiven Mitglieder **mit Foto**, sortiert nach Nachname. Jede Kachel zeigt Foto, Name, den Untertitel „Position, Organisation“, Ort und Funktionen.
- Ein Klick öffnet das Profil als Fenster; `/community/<id>` ist die eigene Detailseite des Profils. Erst dort erscheinen E-Mail, Telefon und Bio, je nach Sichtbarkeit und Betrachter (auf den Kacheln nicht, damit sie schmal bleiben).
- Gesperrte Konten und Profile ohne Foto erscheinen nicht.
- Admins sehen im Fenster und auf der Detailseite unten rechts einen Stift, der direkt zur Bearbeiten-Seite des Nutzers führt.

### Nutzerverwaltung (Admin)

Unter Administration → **Nutzer** listet der Admin alle Konten und legt über „Nutzer anlegen“ neue an. Die Tabelle lässt sich per Klick auf eine Spaltenüberschrift sortieren (Name nach vollem Namen, ein zweiter Klick dreht die Reihenfolge um) und über das Suchfeld darüber filtern: Jedes eingegebene Wort muss irgendwo in der Zeile vorkommen, z. B. „anna admin“ oder „gesperrt“. Ein Klick auf eine Zeile öffnet die Detailansicht; dorthin führt auch der Stift im Community-Fenster und auf der Profil-Detailseite. Dort kann er:

- **Konto:** Login-E-Mail, Rolle (Admin/Mitglied) und Sperre ändern. Ein gesperrtes Konto kann sich nicht anmelden, verliert eine laufende Sitzung und verschwindet aus der Community.
- **Profil** bearbeiten und **Profilfoto** hochladen oder entfernen.
- **Passwort:** ein neues Passwort setzen (auf sicherem Weg weitergeben) oder einen Link zum Passwortsetzen per Mail schicken (14 Tage gültig).
- **Konto löschen**, samt Profil und Foto.

Grenzen: Das eigene Konto kann ein Admin nicht sperren, herabstufen oder löschen, damit sich der letzte Admin nicht aussperrt. Konten, die Beiträge, Sektionen oder Termine verfasst haben, lassen sich nicht löschen, nur sperren.

### Nutzername und ID

Beides vergibt das System beim Anlegen automatisch; keins von beiden lässt sich direkt bearbeiten.

|  | Nutzername | ID |
| --- | --- | --- |
| Was | Login-E-Mail-Adresse in Kleinbuchstaben (auch bei Einladung und CSV-Import) | fortlaufende Nummer der Datenbank, rein intern |
| Wo sichtbar | Nutzerliste, Spalte „E-Mail / Login“ | nur in der Adresszeile der Bearbeiten-Seite, z. B. `/admin/users/39`, und in der Spalte `id` des CSV-Exports |
| Ändern | indirekt: Wird die Login-E-Mail geändert (Nutzerverwaltung → Konto oder vom Mitglied im eigenen Profil), ändert sich der Nutzername mit | nicht möglich; beim CSV-Import wird die Spalte `id` ignoriert und neu vergeben |

- **Ausnahme:** Der Admin aus `init_db.py` heißt `admin` und behält diesen Nutzernamen, auch wenn er eine E-Mail-Adresse bekommt. Nur wenn Nutzername und E-Mail verschieden sind, zeigt die Bearbeiten-Seite unter „Konto“ die Zeile „Nutzername“.
- **Profil-ID:** Das Profil hat eine eigene, unabhängige ID. Die Community-Detailseite nutzt sie (z. B. `/community/12`); sie stimmt nicht unbedingt mit der Nutzer-ID überein.

## A6 Formulare, Lexikon, Export und Import

### ActiveCampaign-Formulare

Fünf Anmeldeformulare von ActiveCampaign (AC) sind als Fenster in jede Seite eingebunden und lassen sich von überall öffnen:

| Formular | AC-Nr. | Modal-ID |
| --- | --- | --- |
| Probe-Spielraum | 16 | `#spielraumModal` |
| Spiele Coach | 8 | `#spieleCoachModal` |
| Spiele Event | 11 | `#spieleEventModal` |
| Newsletter | 14 | `#newsletterModal` |
| Webinar | 22 | `#webinarModal` |

Der Button „Platz sichern“ bei einem Termin öffnet automatisch das Formular seiner Kategorie (Tabelle in A4). Die Formularinhalte selbst werden in ActiveCampaign gepflegt, nicht im CMS.

### Lexikon (`/lexicon`)

Die Lexikonseite listet Begriffe zu Gesundheit, Resilienz und Wandel alphabetisch, mit Kategorien und einer Liste „Häufig gesucht“. Die Inhalte stehen nicht in der Datenbank, sondern in der Datei `content/lexicon.md`; Änderungen dort sind nach dem Speichern sofort sichtbar. Der Aufbau ist am Anfang der Datei beschrieben: je Begriff ein Abschnitt `## Begriff` mit den Feldern Slug, Kategorie, Auch, Kurz und Siehe auch, danach der Text. Verweise im Fließtext öffnen den Eintrag als Fenster.

### Export und Import

Beiträge, Termine, Sektionen und **Nutzer mit Profil** lassen sich als CSV-Dateien sichern und wieder einspielen, etwa vor einem Neuaufbau der Datenbank oder zwischen Entwicklung und Produktion. Nicht enthalten sind Einladungen und die Portalkonfiguration (SMTP-Daten, Passwort-Richtlinie).

- **Export:** Nach einer Rückfrage mit der Anzahl der Beiträge, Sektionen, Termine und Nutzer lädt die Administration ein ZIP mit `articles.csv`, `sections.csv`, `events.csv`, `users.csv`, allen Bildern und Profilfotos. Fehlende Dateien stehen in `export_hinweise.txt`. **Das ZIP enthält personenbezogene Daten und die Passwort-Hashes aller Nutzer – sicher aufbewahren und nicht weitergeben.**
- **Import:** Einen ganzen Ordner (CSV-Dateien und Bilder) oder ein Export-ZIP auswählen, höchstens 16 MB. Bei Fehlern öffnet sich das Fenster erneut mit den Meldungen.

Regeln beim Import:

- Beiträge, Sektionen und Termine werden immer **neu** angelegt; ein zweiter Import erzeugt Duplikate.
- **Alles oder nichts:** Ein Fehler in einer Zeile verhindert den ganzen Import; die Meldung nennt Datei und Zeile.
- Pflichtspalten: `title` und `body` bei Beiträgen und Sektionen; `title`, `category`, `starts_at`, `ends_at`, `location` bei Terminen; `username` und `email` bei Nutzern (Mitglieder brauchen eine E-Mail-Adresse).
- Format: Semikolon als Trenner, UTF-8 mit BOM, Ja/Nein als `1`/`0`, Zeiten als `JJJJ-MM-TT HH:MM` in deutscher Ortszeit.
- Reihenfolgenummern der Beiträge werden in 10er-Schritten neu vergeben; importierte Beiträge stehen hinter den vorhandenen.
- Höchstens ein Banner, und nur wenn noch keiner existiert.
- HTML im Text wird bereinigt: Nur Fett, Kursiv und Links bleiben; Absätze und Listen werden zu Zeilenumbrüchen.
- **Nutzer** (`users.csv`, eine Zeile je Konto mit Profil):
  - Neue Konten werden mit `role`, `is_active` und `password_hash` aus der CSV angelegt; die bisherigen Passwörter gelten also weiter. Ist `password_hash` leer, setzt die Person ihr Passwort über „Passwort vergessen“.
  - Gibt es schon ein Konto mit gleichem Nutzernamen oder gleicher E-Mail-Adresse (z. B. `admin` nach `init_db.py`), bleiben Rolle, Sperre und Passwort unverändert; nur das Profil wird übernommen. Ein wiederholter Import legt daher keine doppelten Konten an.
  - Profilspalten sind optional; wenn ausgefüllt, sind `first_name`, `last_name` und `city` Pflicht. `functions` = Schlüssel mit Komma getrennt (`coach,smeo_staff`), `*_visibility` = `public` oder `members`.
  - Profilfotos werden wie beim Upload quadratisch zugeschnitten und nach `data/uploads/avatars/` übernommen.

## B1 Architektur und Betrieb

Die App ist eine einzelne Flask-Anwendung mit zwei Blueprints, PostgreSQL 15 als Datenbank und Nginx als vorgeschaltetem Webserver; alles läuft per Docker Compose.

&#91;embedded content: Architektur von flask-mdad · Nginx, Flask-App mit drei Modulen, Datenablagen\]

Die Flask-App liest und schreibt die Datenbank und den Upload-Ordner, verschickt Mails über SMTP und liest das Lexikon aus einer Markdown-Datei.

### Module

| Datei | Aufgabe |
| --- | --- |
| `app.py` | Startpunkt, importiert `app` aus `views.py` |
| `views.py` | Konfiguration, öffentliche Seiten, Administrations-Routen, Bild-Upload, Jinja-Filter, Konstanten; registriert die Blueprints |
| `members.py` | Blueprint `members`: eigenes Profil, Foto, Passwort, Einladung annehmen, Passwort vergessen, Community |
| `admin.py` | Blueprint `admin` (Präfix `/admin`): Nutzer, Einladungen, Portalkonfiguration |
| `auth.py` | Decorator `admin_required`, Passwort-Richtlinie (`password_policy`, `describe_policy`, `password_problem`) aus der Portalkonfiguration |
| `extensions.py` | `CSRFProtect` und `Limiter`, getrennt angelegt, damit die Blueprints sie ohne Zirkelimport nutzen |
| `mailer.py` | SMTP-Versand, Fernet-Verschlüsselung des SMTP-Passworts |
| `models.py` | SQLAlchemy-Modelle |
| `images.py` | Beitragsbilder: Verkleinern, Logo-Erkennung, Wahl von `image_fit` |
| `csv_transfer.py` | CSV-Import/-Export von Beiträgen, Sektionen, Terminen und Nutzern mit Profil, auch als Kommandozeilenwerkzeug |
| `lexicon_data.py` | liest `content/lexicon.md` ein (neu bei jeder Änderungszeit der Datei) |
| `init_db.py` / `change_pw.py` | Tabellen und Nutzer `admin`/`pw` anlegen bzw. Passwort zurücksetzen |

### Abhängigkeiten

Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, Flask-Migrate, Flask-WTF (CSRF), Flask-Limiter, Pillow, cryptography (Fernet), gunicorn in Produktion. Bootstrap 5 liegt lokal in `static/`; Bootstrap Icons und Open Sans kommen aus dem Internet.

### Starten

```bash
# Entwicklung (docker-compose.yml + docker-compose.override.yml, FLASK_DEBUG=1)
docker build -t flask-mdad:latest .
docker compose up -d

# Produktion (gunicorn, ein Worker)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

# Einmalig bei leerer Datenbank: Tabellen + Nutzer admin/pw
docker compose exec web python init_db.py
```

- Die App läuft unter http://127.0.0.1:5001 (Host 5001 → Container 5000). In Produktion ist der Port nur lokal offen; erreichbar ist sie nur über Nginx (`nginx/playfulfuture.de.conf`). `ProxyFix` übernimmt die `X-Forwarded-*`-Header, damit externe URLs mit `https://` erzeugt werden.
- Im Debug-Modus ist der Projektordner eingebunden (`.:/app`); Code- und Template-Änderungen wirken ohne Neubau.
- Ohne `DATABASE_URL` nutzt die App eine lokale SQLite-Datei `app.db`.

### Konfiguration und Geheimnisse

- `SECRET_KEY` kommt aus der Umgebung (in Produktion aus `.env`, per `.gitignore` ausgeschlossen). Ohne Schlüssel startet die App nur im Debug-Modus. Er signiert die Sitzungs-Cookies, die Passwort-Reset-Links und ist Grundlage der SMTP-Passwort-Verschlüsselung. **Ein neuer Schlüssel meldet alle ab und macht das gespeicherte SMTP-Passwort unlesbar**; es muss dann neu eingegeben werden.
- Sitzungs-Cookie: `SameSite=Lax`, in Produktion nur über HTTPS. CSRF-Token gilt für die ganze Sitzung (`WTF_CSRF_TIME_LIMIT = None`).
- Uploads: `data/uploads` (Profilfotos in `data/uploads/avatars/`), ausgeliefert über `/uploads/<pfad>` bzw. in Produktion direkt von Nginx. Höchstens 16 MB pro Anfrage.
- Cache-Busting: Jede `url_for('static', …)`-Adresse bekommt die Änderungszeit der Datei als `?v=` angehängt, weil Nginx `static/` sieben Tage cachen lässt.

### Datensicherung

```bash
docker compose exec db pg_dump --clean --if-exists -U flaskuser -d flaskdb > dump.sql
cat dump.sql | docker compose exec -T db psql -U flaskuser -d flaskdb
```

Der Dump enthält nur Bild-Dateinamen; `data/uploads` muss separat gesichert werden. Der CSV-Export enthält Inhalte, Bilder, Nutzer, Profile und Profilfotos, aber keine Einladungen und keine Portalkonfiguration, und ersetzt daher kein vollständiges Backup.

## B2 Datenmodell (`models.py`)

Sieben Tabellen: `User` steht im Zentrum; jedes `Article`, `Section` und `Event` gehört einem Autor, jedes Mitglied hat höchstens ein `Profile`. Zeitstempel werden naiv in UTC gespeichert.

| Modell | Wichtige Felder | Beziehungen und Regeln |
| --- | --- | --- |
| `User` | `username` (unique), `email` (unique), `password_hash` (bcrypt), `role` (`admin`/`member`, Standard `member`), `is_active`, `created_at`, `last_login_at` | 1:1 `profile` (cascade delete-orphan); 1:n `articles`, `sections`, `events`. `is_active` überschreibt `UserMixin.is_active`; `is_admin` ist eine Property. Bei Mitgliedern ist `username` = E-Mail |
| `Profile` | `first_name`, `last_name`, `city` (Pflicht), `display_name`, `organization`, `job_title`, `functions` (JSON-Liste von Schlüsseln), `phone`, `bio`, `website`, `photo_filename`, `email_/phone_/bio_visibility` (`public`/`members`, Standard `members`), `updated_at` | `user_id` unique. Properties `full_name`, `name` (Anzeigename oder voller Name), `function_labels` |
| `Invitation` | `email`, `token_hash` (SHA-256, unique), `created_at`, `expires_at`, `used_at`, `invited_by_id` | Nur der Hash des Tokens wird gespeichert; der Klartext steht nur in der Mail |
| `PortalSettings` | `smtp_host`, `smtp_port`, `smtp_security` (`starttls`/`ssl`/…), `smtp_username`, `smtp_password_encrypted`, `mail_from_address`, `mail_from_name`, `password_min_length` (Standard 10), `password_require_lower`, `password_require_upper`, `password_require_digit`, `password_require_special` (je Standard aus) | Genau ein Datensatz (id 1) |
| `Article` | `on_index`, `on_consulting`, `on_academy`, `on_stories`, `is_banner`, `title`, `body`, `description` (300), `image_filename`, `image_fit` (`cover`/`contain`/`blur`), `order_number`, `col_size` | Autor über `user_id`. Höchstens ein `is_banner` (in den Views geprüft, nicht per Constraint) |
| `Section` | `on_index`, `on_consulting`, `on_academy`, `kicker`, `title`, `body`, `description`, `image_filename`, `image_position` (`left`/`right`), `slot_index_<seite>`, `slot_position_<seite>` für index, consulting, academy | `None` im Slot = nicht auf dieser Seite platziert |
| `Event` | `title`, `category`, `all_day`, `subtitle`, `starts_at`, `ends_at`, `location` | Autor über `user_id` |

**Erweiterungspunkte ohne Schemaänderung:** neue Profilfunktion = neue Zeile in `PROFILE_FUNCTIONS` (`models.py`); neue Terminkategorie = Einträge in `EVENT_CATEGORIES`, `EVENT_CATEGORY_ICONS` und ggf. `EVENT_CATEGORY_MODAL` (`views.py`).

**Kein persistiertes Feld:** `image_orientation` ist nur ein Formularwert beim Sektions-Upload und bestimmt den Zuschnitt.

### Schemaänderungen

Flask-Migrate ist eingebunden, ein Ordner `migrations/` existiert aber noch nicht. `db.create_all()` legt nur fehlende Tabellen an und verändert keine bestehenden. Die neuen Tabellen `Profile` und `Invitation` entstehen so automatisch; die **neuen Spalten in `User`** (`email`, `role`, `is_active`, `created_at`, `last_login_at`) und in **`PortalSettings`** (Passwort-Richtlinie) aber nicht. Laut Commits muss die Datenbank deshalb neu aufgebaut werden: Backup und CSV-Export ziehen, DB löschen, `init_db.py`, CSV-Import (der jetzt auch Nutzer und Profile zurückholt). Alternativ eine echte Migration:

```bash
docker compose exec web flask db init
docker compose exec web flask db migrate -m "Nutzerbereich"
docker compose exec web flask db upgrade
```

## B3 Routen, Zugriffsschutz und Sicherheit

Jede Route hat genau eine von drei Schutzstufen: öffentlich, `login_required` (jedes Konto) oder `admin_required` (nur Admins; Gäste werden zum Login umgeleitet, Mitglieder bekommen 403).

| Route | Methode | Schutz | Datei / Funktion |
| --- | --- | --- | --- |
| `/`, `/consulting`, `/academy`, `/stories` | GET | öffentlich | `views.py` |
| `/lexicon`, `/lexicon/<slug>/preview` | GET | öffentlich | `views.py` |
| `/imprint`, `/privacy`, `/sitemap.xml`, `/uploads/<pfad>` | GET | öffentlich | `views.py` |
| `/login` | GET, POST | öffentlich, Limit 10/min, 30/h | `views.login` |
| `/logout` | POST | – | `views.logout` |
| `/dashboard` | GET | Admin | `views.dashboard` |
| `/add-article`, `/edit-article/<id>`, `/delete-article/<id>` | GET/POST | Admin | `views.py` |
| `/add-section`, `/edit-section/<id>`, `/delete-section/<id>` | GET/POST | Admin | `views.py` |
| `/add-event`, `/edit-event/<id>`, `/delete-event/<id>`, `/delete-past-events` | GET/POST | Admin | `views.py` |
| `/export`, `/import` | GET/POST | Admin | `views.py` |
| `/account/profile`, `/account/password` | GET, POST | Login | `members.py` |
| `/account/photo`, `/account/photo/delete`, `/account/delete` | POST | Login | `members.py` |
| `/invite/<token>` | GET, POST | öffentlich, Limit 10/min | `members.accept_invitation` |
| `/password-reset`, `/password-reset/<token>` | GET, POST | öffentlich, Limit 5/min + 20/h bzw. 10/min | `members.py` |
| `/community`, `/community/<id>` (`?modal=1` liefert nur den Fensterinhalt) | GET | öffentlich | `members.py` |
| `/admin/users`, `/admin/users/new` | GET, POST | Admin | `admin.users`, `admin.user_new` |
| `/admin/users/<id>` (Formular-`action`: `profile`, `account`, `password`, `send_link`) | GET, POST | Admin | `admin.user_detail` |
| `/admin/users/<id>/photo`, `/admin/users/<id>/photo/delete`, `/admin/users/<id>/delete` | POST | Admin | `admin.py` |
| `/admin/invitations`, `/admin/invitations/<id>/revoke` | GET, POST | Admin | `admin.py` |
| `/admin/settings`, `/admin/settings/test-mail` | GET, POST | Admin | `admin.py` |

Nach dem Login leitet `home_for(user)` Admins nach `/dashboard`, Mitglieder nach `/account/profile`.

### Sicherheitsmechanismen

- **CSRF:** Flask-WTF schützt alle POST-Anfragen. Jedes Formular braucht `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`. Ein fehlendes Token führt zur Fehlerseite.
- **Rate-Limit:** Flask-Limiter mit Speicher im Arbeitsspeicher (`memory://`). Das passt nur zu genau einem gunicorn-Worker; bei mehreren Workern bräuchte es Redis o. Ä.
- **Passwörter:** bcrypt. Die Richtlinie steht in `PortalSettings` und wird von `auth.password_problem()` geprüft: Mindestlänge (Standard `DEFAULT_MIN_PASSWORD_LENGTH = 10`) und optionale Zeichenklassen aus `CHARACTER_RULES`. `describe_policy()` erzeugt den Hinweistext; die Passwortfelder setzen `minlength` passend.
- **Einladungstoken:** `secrets.token_urlsafe(32)`, gespeichert nur als SHA-256-Hash, 14 Tage, einmal nutzbar.
- **Passwort-Links:** `itsdangerous.URLSafeTimedSerializer` mit zwei Zwecken (Salt): `password-reset` („Passwort vergessen“, 2 Stunden) und `account-setup` (vom Admin angelegtes Konto oder per Admin verschickter Link, 14 Tage). Beide führen zu `/password-reset/<token>`. Das Token enthält die letzten 16 Zeichen des Passwort-Hashes; nach einem Passwortwechsel ist der Link automatisch ungültig.
- **Direkt angelegte Konten mit Link** bekommen bis zum Setzen ein unbekanntes Zufallspasswort.
- **SMTP-Passwort:** Fernet-verschlüsselt, Schlüssel per SHA-256 aus dem `SECRET_KEY` abgeleitet.
- **Gesperrte Konten:** `load_user` liefert für `is_active = False` nichts zurück; eine laufende Sitzung endet damit beim nächsten Aufruf.
- **Profilfotos:** Pillow liest das Bild, dreht es nach EXIF, schneidet es auf 600 × 600 px (Ausschnitt leicht oberhalb der Mitte) und speichert es neu als WebP mit zufälligem Namen. Dabei fallen EXIF-Daten wie GPS-Koordinaten weg.
- **CSV-Export** enthält die bcrypt-Hashes aller Nutzer; das ZIP ist entsprechend zu schützen.

### Zentrale Hilfsfunktionen

| Funktion | Ort | Zweck |
| --- | --- | --- |
| `visible_fields(profile, viewer)` | `members.py` | **Einzige Stelle** der Sichtbarkeitsregel für E-Mail, Telefon, Bio |
| `visible_profiles_query()` | `members.py` | Profile für die Community: aktives Konto und Foto |
| `apply_profile_form(profile, user, form, email=None)` | `members.py` | Validiert und übernimmt Profilfelder; genutzt von Profil, Einladung und Admin |
| `slot_options`, `place_section_in_slot`, `sections_by_slot` | `views.py` | Slot-Logik der Sektionen |
| `images.save_article_image` | `images.py` | Beitragsbild speichern und `image_fit` bestimmen |
| `mailer.send_mail`, `mailer.is_configured` | `mailer.py` | Mailversand (missing\_settings nennt fehlende Angaben), wirft `MailError` |

### Jinja-Filter und Konstanten in `views.py`

- Filter: `datetimeformat`, `dateinput`, `timeinput`, `eventdaterange`, `eventcategorylabel`, `eventcategoryicon`, `eventcategorymodal`.
- Konstanten: `ARTICLE_FLAGS`, `SECTION_FLAGS`, `EVENT_CATEGORIES`, `EVENT_CATEGORY_ICONS`, `EVENT_CATEGORY_MODAL`, `PAGE_SLOT_COUNT`, Bildmaße `LANDSCAPE_*`/`PORTRAIT_*`.
- Kontextprozessor in `members.py` stellt allen Templates `password_policy`, `password_policy_text`, `visible_fields`, `profile_functions` und `visibility_choices` bereit.

## B4 Templates und statische Dateien

Alle Seiten erben von `templates/base.html`; die Listen auf den öffentlichen Seiten kommen aus wiederverwendeten Partials, die per `{% include %}` eingebunden werden.

| Template | Inhalt |
| --- | --- |
| `base.html` | Navbar („Gratis spielen“ für Gäste, sonst Nutzermenü), Footer mit „Anmelden“, fünf AC-Formular-Modals, Lexikon-Modal |
| `_user_menu.html` | Nutzermenü: Avatar bzw. Initialen mit Dropdown (Mein Profil, Öffentliche Ansicht, Passwort ändern, Administration für Admins, Abmelden); auf dem Handy als Block im aufgeklappten Menü |
| `index.html`, `consulting.html`, `academy.html`, `stories.html` | Öffentliche Seiten mit festen Abschnitten und Slots für Sektionen |
| `_articles_list.html`, `_article_tile.html` | Beitragsraster und Kachel inkl. „Weiterlesen“-Fenster (Text vor `##`) |
| `_sections_list.html` | Sektionen eines Slots |
| `_macros.html` | Makros, u. a. `lexicon_link` für Lexikon-Verweise im Text |
| `_flashes.html`, `_password_fields.html`, `_profile_form.html` | Gemeinsame Bausteine des Nutzerbereichs; die Passwortfelder zeigen den Hinweis der Richtlinie, das Profilformular teilen sich Profil, Einladung und Admin-Seiten |
| `dashboard.html`, `add_*/edit_*.html` | Administration und Formulare für Beiträge, Sektionen, Termine; Export-/Import-Fenster |
| `account/` | `profile.html`, `password.html`, `_nav.html` |
| `admin/` | `users.html`, `user_new.html`, `user_detail.html`, `_password_choice.html` (Startpasswort oder Link per Mail), `invitations.html`, `settings.html` (SMTP und Passwort-Richtlinie), `_nav.html` (Inhalte, Nutzer, Einladungen, Portalkonfiguration); die Nutzerliste sortiert und filtert per Skript im Browser |
| `auth/` | `invite.html`, `password_reset_request.html`, `password_reset.html` |
| `community/` | `index.html` (Kacheln), `detail.html`, `_profile_view.html` (Inhalt für Modal und Detailseite; liefert für Admins das Ziel des Bearbeiten-Stifts) |
| `mail/` | `invitation.txt`, `account_created.txt`, `password_link.txt`, `password_reset.txt` (reine Textmails) |
| `error.html` | Fehlerseite für 403, 409, 410, 429 und CSRF-Fehler |
| `lexicon.html`, `_lexicon_preview.html`, `_lexicon_entry_text.html` | Lexikonseite und -fenster |
| `alle_ac_formulare.html` | Sammelseite **ohne Route**, wird als Datei geöffnet; bindet CSS/JS deshalb mit relativen Pfaden statt `url_for()` ein |

**Statische Dateien (`static/`):** `bootstrap.min.css`, `bootstrap.bundle.min.js`, `custom.css` (Hausstil, Kartenoptik, `.termin-title` u. a.), `lexicon.css`, `ac-formulare.css`/`ac-formulare.js` (Styling der AC-Formulare, inkl. Ausblenden der doppelten AC-Titel im Modal; Formular 11 braucht eine eigene Regel) sowie feste Bilder in `static/img/`. Hochgeladene Bilder liegen nicht hier, sondern in `data/uploads`.

**Inhalt vs. Code:** Feste Texte der Seiten stehen in den Templates; `docs/indexseite-inhalt.md` und `docs/indexseite-stil.md` beschreiben Inhalt und Stil der Indexseite.

**Nicht Teil des CMS:** `equipe-pq/` und `mensch-pflege/` sind eigenständige statische Seiten im selben Repository, die Nginx direkt ausliefert (`nginx/*.conf`).

## B5 Konventionen und Arbeitsweise

Code-Bezeichner sind englisch, alles Sichtbare ist deutsch; geändert wird nur nach Prüfung und committet nur nach ausdrücklicher Freigabe.

- **Namen:** Template-Dateien, View-Funktionen, URL-Routen und Modellfelder englisch (`/consulting`, `academy.html`, `on_stories`). Seitentexte, UI-Labels und Code-Kommentare deutsch. Neue Seiten und Felder gleich englisch anlegen.
- **Umbenennen** von Template-Dateien nur mit `git mv`, damit die Historie erhalten bleibt.
- **Commits** nur nach ausdrücklicher Freigabe der Nutzerin, für jede einzelne Änderung. Commit-Messages deutsch, mit kurzer Begründung im Text. Veröffentlichen (`git push` nach `git@github.com:hbetter/flask-mdad.git`, Branch `main`) erfolgt vom eigenen Terminal.
- **Sicher bearbeiten:** Datei vor jeder Änderung frisch einlesen (sie wird oft zwischendurch von Hand geändert), Ersetzungen nur an eindeutigen Textstellen.
- **Neue POST-Formulare** brauchen das CSRF-Feld; neue Admin-Routen den Decorator `@admin_required`, neue Mitglieder-Routen `@login_required`.
- **Neue Sichtbarkeitsregeln** nur in `visible_fields()` ergänzen, damit es eine einzige Quelle gibt.

### Prüfen nach Änderungen

Automatisierte Tests gibt es noch nicht.

```bash
docker compose exec web python -c "import ast; [ast.parse(open(f).read()) for f in ('views.py', 'models.py', 'members.py', 'admin.py')]"
docker compose exec web python -c "from jinja2 import Environment; import glob; [Environment().parse(open(f).read()) for f in glob.glob('templates/**/*.html', recursive=True)]"
docker compose exec web python lexicon_data.py
```

Danach die geänderten Seiten unter http://127.0.0.1:5001 ansehen, auch in schmaler Fensterbreite. Zum Testen mit `admin`/`pw` anmelden, am Ende abmelden und Teständerungen zurücknehmen. Wenn der Browser alte HTML-Seiten zeigt, `?nocache=1` an die Adresse hängen.

## Offene Punkte vor dem Livegang

- [x] Nutzerbereich committen (`38b402c`, `5e22e74`).
- [x] CSV-Export/-Import für Nutzer mit Profil committen (Commit 730bc4f).
- [x] Produktionsdatenbank neu aufbauen bzw. migrieren: neue Spalten in `User` und `PortalSettings` entstehen nicht durch `db.create_all()` (siehe B2).
- [ ] Passwort-Richtlinie in der Portalkonfiguration festlegen.
- [ ] Standardpasswort `pw` des Nutzers `admin` ändern.
- [ ] Datenbank-Zugangsdaten aus `docker-compose.yml` (stehen dort im Klartext) in die `.env` verlegen.
- [ ] Datenschutzerklärung um den Community-Bereich ergänzen: Profile, Fotos, Einladungs- und Passwortmails.
- [ ] Mailversand in der Portalkonfiguration einrichten und per Testmail prüfen.
- [ ] Flask im Produktionsmodus (gunicorn) statt Debug-Modus betreiben, sobald der Server fertig ist.
- [ ] Bei mehr als einem gunicorn-Worker den Rate-Limit-Speicher von `memory://` auf Redis umstellen.
- [ ] Regelmäßige Sicherung von Datenbank-Dump **und** `data/uploads` einrichten; Export-ZIPs wegen der Passwort-Hashes geschützt ablegen.
- [ ] Automatisierte Tests für Login, Einladung, Passwort-Richtlinie, Sichtbarkeit und Slot-Logik ergänzen.

TLS übernimmt Nginx; die App selbst spricht nur HTTP.
