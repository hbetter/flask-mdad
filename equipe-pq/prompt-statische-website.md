# Prompt: Statische Website aus dem MENSCH DENK AN DICH®-Portal erzeugen

Erzeuge aus dem lokal laufenden Flask-Portal (http://localhost:5001) eine schlanke statische Website. Nutze dafür meinen Chrome-Browser und schreibe die Ergebnisse direkt in den Ordner `equipe-pq/` im Repo `flask-mdad` (`~/Docker/flask-mdad/equipe-pq/`).

## Seiten
- `/` → `index.html`
- `/imprint` → `impressum.html`
- `/privacy` → `datenschutz.html`

Basis ist jeweils das vom Server ausgelieferte HTML (nicht das gerenderte DOM), damit die Dateien schlank bleiben.

## Einbindung von Ressourcen
- **Bootstrap 5.3.8 (CSS + JS)** und **Bootstrap Icons 1.11.3** per CDN über **cdnjs.cloudflare.com** verlinken (passt zur Datenschutzerklärung). Google Fonts (Open Sans) bleibt wie im Original verlinkt.
- **`custom.css`** aus `/static/css/` als eigene Datei in den Zielordner legen und relativ verlinken (`href="custom.css"`).
- **Alle Bilder** aus `/static/img/` (inkl. Favicon) in den Zielordner kopieren und nur mit Dateinamen verlinken (`src="logo_maroon.png"`), keine Pfade, keine Data-URIs.
- Keine Styles oder Scripts inline einbetten. Einzige Ausnahme: der kurze JSON-LD-Block (schema.org) bleibt im `<head>`.
- `<link rel="canonical">` (zeigt auf localhost) entfernen.

## Kopfzeile (alle Seiten)
- Menüpunkte Beratung, Akademie, Erfolgsgeschichten, Termine, Kontakt entfernen (`#mainNav` komplett) sowie den Hamburger-Button (`.navbar-toggler`).
- Button-Gruppe mit `ms-auto` rechts ausrichten, sodass nur Logo und Button „Probe Spielraum buchen“ bleiben.
- Logo verlinkt auf der Startseite auf `#`, auf den Unterseiten auf `index.html`.
- Direkt neben dem MENSCH DENK AN DICH®-Logo das Partner-Logo von https://equipe-pq.com/ einfügen (Datei `equipe-logo.png` im Zielordner, Höhe wie das Hauptlogo über Klasse `navbar-logo`), verlinkt auf https://equipe-pq.com/ (neuer Tab). In `custom.css`: `.navbar-partner { display:flex; align-items:center; padding-left:1rem; border-left:1px solid rgba(0,0,0,.12); }`

## Startseite: Sektionen entfernen
- „Hinterfragt / Fragen und Antworten“ (FAQ)
- „Wissenschaftlich fundiert“
- „Shorts / Einblicke“
- „Termine / Risikofrei starten“

## Buttons und Links
- Jeder Button (`a.btn`, außer dem Skip-Link „Zum Inhalt springen“) wird zu
  `mailto:hey@mensch-denk-an-dich.de?subject=<Button-Text>` (URL-kodiert). Bei „Probe Spielraum buchen / Buchen“ die lange Beschriftung als Betreff verwenden.
- Footer-Links: `/imprint` → `impressum.html`, `/privacy` → `datenschutz.html`.

## Versionierung
- Die aktuellen Dateien heißen immer `index.html`, `impressum.html`, `datenschutz.html`.
- Vor jeder Änderung die bisherige Fassung nach `alte-versionen/` kopieren, mit fortlaufender Versionsnummer (`index-v1.html`, `index-v2.html`, …).

## Abschlussprüfung
- Alle drei Seiten im Browser ansehen (Layout, Schrift, Icons, Bilder).
- Prüfen, dass jede per `src`/`href` referenzierte lokale Datei im Ordner existiert und die drei Seiten sich gegenseitig korrekt verlinken.
- Kurz melden, welche Links noch auf Portal-Unterseiten zeigen (z. B. `/login`).
