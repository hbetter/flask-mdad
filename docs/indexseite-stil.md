# Indexseite – Stil & grafische Elemente

Dokumentation des visuellen Erscheinungsbilds der aktuellen Flask-Indexseite (`templates/index.html` + `templates/base.html`, Stand dieser Sitzung), damit die Seite als eigenständige statische HTML-Seite nachgebaut werden kann. Reine Stilangaben – Texte/Inhalte stehen in `indexseite-inhalt.md`. Der Bereich „Weitere Beiträge" (datenbankgetriebene Karten aus dem Dashboard) ist bewusst ausgeklammert, da er dynamisch ist und für eine statische Seite ohnehin entfällt.

## Technische Basis

- **Framework:** Bootstrap 5 (`bootstrap.min.css` + `bootstrap.bundle.min.js`)
- **Icon-Font:** Bootstrap Icons 1.11.3, per CDN (`cdnjs.cloudflare.com/.../bootstrap-icons.min.css`)
- **Schriftart:** „Open Sans", Google Fonts, Schnitte 400 / 600 / 700 / 800 (`fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800`)
- **Grundraster:** durchgehend Bootstrap-Grid (`container`, `row`, `col-*`), jede Seitensektion ist als eine `.card` verpackt

## Farbpalette (CSS-Variablen)

| Variable | Wert | Verwendung |
|---|---|---|
| `--brand-red` / `--sm-maroon-bright` | `#e30613` | Hover-Zustand von Maroon-Buttons, große Stat-Zahlen, Kicker, Trennlinie unter Navbar (als Basis von `--sm-maroon`) |
| `--brand-red-dark` / `--sm-maroon` | `#9C0E17` | Haupt-Akzentfarbe: Kicker-Text, Buttons „btn-maroon", Termin-Datum, Tabellen-Überschriften, Navbar-Trennlinie |
| `--sm-dark` | `#281351` | Überschriften h1–h3, Navbar-Text/-Logo-Schrift, Fußzeilen-Icons in Tooltip-Überschrift, `.btn-outline-dark-sm` |
| `--sm-purple` | `#43367B` | Termin-Format-Badge (Pille), Video-Platzhalter-Farbe/-Icon, Kartentechnik-Akzent |
| `--sm-pink` | `#CC3366` | Anführungszeichen-Icon in Testimonial-Karten |
| `--sm-bg` | `#F1F2F8` | (aktuell nicht als Flächenfarbe genutzt, nur Variable vorhanden) |
| `--sm-bg-nested` | `#F7F7FB` | Hintergrund von Karten-in-Karten (`.card .card-sm`, `.card .termin-card`) |
| `--sm-bg-soft` | `#FCFCFC` | Seitenhintergrund (`body`) |
| `--sm-ink` | `#33373D` | Fließtext-Grundfarbe |
| `--sm-line` | `#DADFE8` | Trennlinien (Tabellen, Footer-`<hr>`, Karten-in-Karten-Rand) |
| `--sm-muted` | `#6b7078` | Gedämpfter Text (Untertitel, Footer-Tagline, Quellenangaben) |

## Typografie

- **Body:** Open Sans, Grundfarbe `--sm-ink`, Seitenhintergrund `--sm-bg-soft`
- **Überschriften h1–h3:** Open Sans, Farbe `--sm-dark`, `font-weight: 800`
  - h1 nutzt Bootstrap-Klasse `display-3`, h2 durchgängig `display-5`
- **Kicker** (kleine Vorzeile über jeder Sektions-Überschrift): Großbuchstaben (`text-transform: uppercase`), `letter-spacing: .08em`, `font-size: .8rem`, `font-weight: 700`, Farbe `--sm-maroon`
- **Untertitel/Lead-Absätze:** meist `fs-4`/`fs-5`, teils Farbe `--sm-purple` (Klasse `.text-purple`, z. B. Hero-Untertitel)
- **Kartentitel** (`.card-title`, z. B. bei datenbankgetriebenen Karten): Farbe `--sm-dark`, `font-weight: 600`, `line-height: 1.4`
- **Modal-Titel** (`.modal-title`): Farbe `--brand-red` (abweichend von `.card-title`, betrifft nicht die statische Indexseite, da dort keine Modals vorkommen)

## Seitenraster / Sektionsmuster

Jede inhaltliche Sektion folgt demselben Muster:

```html
<section class="py-3 py-lg-4">
  <div class="container">
    <div class="card shadow-sm">
      <div class="card-body p-4 p-lg-5">
        <p class="kicker mb-2">…</p>
        <h2 class="display-5 mb-5">…</h2>
        <!-- Sektionsinhalt -->
      </div>
    </div>
  </div>
</section>
```

- Vertikaler Abstand zwischen Sektionen: `py-3 py-lg-4` am `<section>`
- Innenabstand der Karte: `p-4` (mobil), `p-lg-5` (ab `lg`)
- Karten-Grundstil (`.card`): kein Rahmen (`border: none`), `border-radius: 12px`, sanfter Übergang (`transition: all .3s ease`)
- Karten-Hover (`.card:hover`): Schatten `0 8px 24px rgba(0,0,0,.12)`, `transform: translateY(-4px)` (Karte hebt sich leicht an)
- **Wichtig für Modals/`position: fixed`-Elemente:** Da `.card:hover` einen `transform` setzt, erzeugt jede Karte beim Hover einen neuen Containing Block für `position: fixed`-Nachfahren (z. B. Bootstrap-Modals). Modals/Fixed-Elemente dürfen daher nie als Nachfahre einer `.card` liegen, sondern müssen als Geschwister-Element direkt im `.container` stehen.

## Navigation (Navbar)

- Klasse `navbar-custom`, weißer Hintergrund (`#fff`, `!important`), untere Trennlinie `2px solid --sm-maroon`, dezenter Schatten `0 2px 10px rgba(0,0,0,.05)`, sticky (`sticky-top`)
- Vertikales Innenpolster der Navbar reduziert: `padding: 0.25rem 0` (überschreibt Bootstraps Standard-Padding)
- **Logo:** Höhe `56px` (mobil), ab `992px` Breakpoint `70px`, Breite automatisch
- **Nav-Links:** Farbe `--sm-dark`, `font-weight: 600`, `font-size: 1rem`, horizontales Padding `1rem`; Hover/aktiv-Zustand: Farbe wechselt zu `--sm-maroon`
- **CTA-Button rechts** (`.btn-maroon`, siehe Buttons unten): bei eingeloggten Nutzern „Mein Bereich" (Link zum Dashboard), sonst das eigentliche CTA (siehe Inhalts-Datei)
- **Mobiles Klappmenü** (< 992px): kein vollbreites Ausklappen mehr, sondern eine eigenständige, rechtsbündige Dropdown-Box unterhalb der Hamburger-/Button-Gruppe:
  - `position: absolute; top: 100%; right: 0; min-width: 220px; max-width: calc(100vw - 2rem)`
  - Weiße Karten-Optik: `border-radius: .6rem`, Schatten `0 8px 24px rgba(40,19,81,.15)`, Innenabstand `.75rem 1rem`, `z-index: 1030`
  - Menüpunkte darin sind **rechtsbündig** ausgerichtet (`align-items: flex-end; text-align: right` auf `.navbar-nav`)
- Unter `576px` verkleinern sich Button-Padding/Schriftgröße von CTA-Button, Hamburger-Icon und dessen Abstand weiter

## Buttons

| Klasse | Aussehen | Hover |
|---|---|---|
| `.btn-maroon` | Füllung `--sm-maroon`, weiße Schrift, `font-weight: 700`, `border-radius: .5rem` | Füllung wechselt zu `--sm-maroon-bright`, Schatten `0 4px 12px rgba(156,14,23,.3)`, hebt sich an (`translateY(-2px)`) |
| `.btn-outline-dark-sm` | Transparent, `2px solid --sm-dark`-Rahmen, Schrift `--sm-dark`, `font-weight: 700`, `border-radius: .5rem` | Füllung wird `--sm-dark`, Schrift weiß, Schatten `0 4px 12px rgba(40,19,81,.25)`, hebt sich an |
| `.btn-maroon.btn-lg` / `.btn-outline-dark-sm.btn-lg` | Größeres Padding `.45rem 1.15rem`, Schriftgröße `1.05rem` | – |

Alle Buttons: `border-radius: 8px` als Basiswert (Bootstrap-Override), sanfte Übergänge (`transition: all .3s ease` bzw. spezifisch auf Schatten/Transform/Farbe).

## Komponenten der Indexseite im Detail

**Hero-Bild** (`.hero-media`): volle Breite/Höhe der Spalte, `min-height: 320px`, `max-height: 480px`, `object-fit: cover`, `border-radius: .6rem`.

**Awards-Karten:** Icon-Rahmen `.award-logo-frame` (Höhe `130px`, Logo zentriert), `.award-logo` (`max-height: 130px`, `object-fit: contain`), Bildunterschrift `.award-caption` (`font-size: .85rem`, `line-height: 1.45`, Farbe `--sm-ink`). Jede Award-Karte ist eine eigene `.card` im 5-spaltigen Raster (`row-cols-2 row-cols-md-3 row-cols-lg-5`).

**Statistik-Kacheln** (`.card-sm` + `.stat-inline`): kleine, weiße Karte mit Schatten (`.card-sm`: `border-radius: .75rem`, Schatten `0 6px 20px rgba(40,19,81,.08)`, Innenabstand `1.75rem 1.5rem`); die Zahl selbst (`.stat-inline`) ist groß und fett (`font-size: 1.9rem`, `font-weight: 800`, Farbe `--sm-maroon`, als Block darüber). Da diese Karten innerhalb der äußeren Sektions-Karte liegen, greift die „Karte-in-Karte"-Regel: Hintergrund `--sm-bg-nested`, kein eigener Schatten, dünner Rahmen `--sm-line`.

**Schmerzpunkt/Lösung/Wirkmechanismus-Tabelle** (`.schmerz-table`): volle Breite, `border-collapse: collapse`. Kopfzeile: kleine Versalien (`.78rem`, `uppercase`, `letter-spacing: .03em`, `font-weight: 700`, Farbe `--sm-maroon`), untere Trennlinie `2px solid --sm-line`. Zellen: Innenabstand `1.25rem`, `vertical-align: top`, dünne Trennlinie `--sm-line` (letzte Zeile ohne), je Spalte ein Drittel Breite. Das „Schmerzpunkt"-Label pro Zeile (`.painpoint`) ist als kleines Badge-artiges Label formatiert (Versalien, fett, `--sm-maroon`).

**Testimonial-Karten** (`.card-sm.testimonial-card`): Anführungszeichen-Icon (`bi-quote`) in `--sm-pink`, `font-size: 1.8rem`, gefolgt von kursivem Zitat, Name fett in `--sm-dark`, Funktion/Rolle klein und gedämpft (`text-muted`).

**Video-Bereich („Shorts"):** Videotitel als `<h3 class="video-title">` – optisch bewusst wie ein normaler Absatz gehalten (`font-size: 1rem`, `line-height: 1.5`, `color: inherit`), nicht wie eine große Überschrift. Eingebettetes Video über `.video-embed` (`border-radius: .6rem`, `overflow: hidden`, Iframe randlos). Noch nicht verlinkte Videos zeigen einen Platzhalter (`.placeholder-media.video-placeholder`): diagonales Streifenmuster (`repeating-linear-gradient(45deg, #ECEAF5, #ECEAF5 12px, #E1DEF0 12px, #E1DEF0 24px)`), gestrichelter Rahmen `2px dashed #BDB6DD`, Seitenverhältnis 16:9, Play-Icon + Text zentriert in `--sm-purple`; beim Hover über die ganze Karte (`.video-card:hover`) färben sich Rahmen/Text zu `--sm-maroon`.

**Termin-Karten** (`.termin-card`): eigenständige, weiße Karte mit Schatten (gleiche Optik wie `.card-sm`), Inhalte als Flex-Spalte mit Lückenabstand `.6rem`. Format-Badge (`.termin-format`, z. B. „Online"/„Präsenz"/„Inhouse"): kleine Pille, Versalien, weiße Schrift auf `--sm-purple`-Hintergrund, `border-radius: 999px`. Datum (`.termin-date`): große Tageszahl (`2.1rem`, fett) neben kleinerem Monat/Jahr (Versalien), beides in `--sm-maroon`. Hover: Schatten verstärkt sich, Karte hebt sich an (`translateY(-4px)`), identisch zum Verhalten von `.card-sm`.

## Footer

- Klasse `site-footer`: weißer Hintergrund, Textfarbe `--sm-ink`, obere Trennlinie `1px solid --sm-line`
- Links darin: Farbe `--sm-ink`, kein Unterstrich; Hover: Farbe `--sm-maroon`, unterstrichen
- Trennlinie vor der Copyright-Zeile: `<hr>` in `--sm-line`
- **Nachhaltigkeits-Badge** (rechts neben Copyright): Icon `greenweb-badge.svg` (32×35px) + kleiner Text (`.78rem`, `--sm-muted`); beim Hover/Fokus erscheint ein Tooltip darüber (weiße Karte, `border-radius: .6rem`, kräftiger Schatten `0 14px 34px rgba(0,0,0,.28)`, kleines Dreieck als Zeiger unten rechts, sanfte Ein-/Ausblendung über Opacity/Transform)

## Sonstige Bausteine (im aktuellen Markup vorhanden, aber ungenutzt/nur als Klasse verfügbar)

- `.ticker`: laufende Banner-Leiste ganz oben (voller Breite, `--brand-red-dark`-Hintergrund, weiße Schrift, zentriert) – aktuell für optionale Hinweistexte nutzbar
- `.dev-label`: dezente lila Kennzeichnung für Bereichs-Labels während der gemeinsamen Bearbeitung (aktuell in keiner Sektion mehr im Markup vorhanden); über `body.hide-dev-labels` ausblendbar

## Grafische Elemente (Bilder/Icons) der Indexseite

| Datei | Verwendung | Hinweis |
|---|---|---|
| `logo_maroon.png` | Logo in der Navbar | verlinkt zur Startseite |
| `collage_web.jpg` | Hero-Bild rechts | Bildunterschrift/Alt: „Impressionen aus dem Spiel MENSCH DENK AN DICH®" |
| `newwork_gold_web.jpg` | Award-Logo (2× verwendet, „Playful Leadership" und „Playful Impact") | New Work Business Award – Gold |
| `newwork_silber_web.jpg` | Award-Logo („Playful Collaboration") | New Work Business Award – Silber |
| `bdvt_web.png` | Award-Logo | Europäischer Trainingspreis (BDVT) |
| `bbgm_web.png` | Award-Logo | Innovationspreis Bundesverband BGM |
| `bekannt-aus-logo.webp` | Logo-Banner in der „Bekannt"-Sektion | volle Breite (`img-fluid w-100`) |
| `greenweb-badge.svg` | Nachhaltigkeits-Badge im Footer | 32×35px |
| `favicon.png` | Browser-Tab-Icon / Apple Touch Icon | seitenweit, nicht indexseiten-spezifisch |
| Bootstrap-Icon `bi-quote` | Anführungszeichen in Testimonial-Karten | Farbe `--sm-pink` |
| Bootstrap-Icon `bi-play-circle-fill` | Play-Symbol im Video-Platzhalter | Teil von `.placeholder-media` |

Alle Bilder werden im Flask-Original über `{{ url_for('static', filename='img/…') }}` eingebunden – für eine statische Seite entspricht das einfach einem relativen Pfad auf den jeweiligen Bilddateinamen (z. B. `img/collage_web.jpg`).
