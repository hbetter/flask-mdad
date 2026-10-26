# Inhalte der Lexikonseite (/lexicon, templates/lexicon.html) und des
# Lexikon-Modals (/lexicon/<slug>/preview).
#
# Die Begriffe stehen in content/lexicon.md und werden hier eingelesen.
# Aufbau der Datei: siehe Kommentar am Anfang von content/lexicon.md.
# Die Datei wird bei jeder Aenderung (Aenderungszeit) neu eingelesen, ein
# Neustart des Servers ist nicht noetig.
#
# Pruefen der Datei auf der Kommandozeile:
#   python lexicon_data.py
#
# Jeder Eintrag wird zu einem Dictionary mit den Schluesseln
#   slug, term, aliases, category, short, body, points, body_after, related
# (points als Liste von (Stichwort, Text)-Paaren, related als Liste von Slugs) -
# dieselbe Form wie frueher die Python-Liste, die Templates bleiben unveraendert.

import logging
import os
import re
import unicodedata


LEXICON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content", "lexicon.md")

logger = logging.getLogger(__name__)

# Feldnamen in der Liste unter "## Begriff" -> interner Schluessel
_META_FIELDS = {
    "slug": "slug",
    "kategorie": "category",
    "auch": "aliases",
    "kurz": "short",
    "siehe auch": "related",
}
_LIST_FIELDS = {"aliases", "related"}  # durch Semikolon getrennt

_SECTION_CATEGORIES = "kategorien"
_SECTION_QUICK = "häufig gesucht"
_SECTION_TERMS = "begriffe"

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_META_RE = re.compile(r"^-\s+([A-Za-zÄÖÜäöüß ]+?)\s*:\s*(.*)$")
_POINT_RE = re.compile(r"^-\s+\*\*(.+?):\*\*\s*(.*)$")
_KEY_VALUE_RE = re.compile(r"^-\s+([^:]+?)\s*:\s*(.+)$")
_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def _split_list(value):
    return [part.strip() for part in value.split(";") if part.strip()]


def _blocks(lines):
    """Zeilen in Bloecke aufteilen (getrennt durch Leerzeilen)."""
    block = []
    for line in lines:
        if line.strip():
            block.append(line.rstrip())
        elif block:
            yield block
            block = []
    if block:
        yield block


def _list_items(block):
    """Listeneintraege eines Blocks; eingerueckte Folgezeilen gehoeren zum Eintrag davor."""
    items = []
    for line in block:
        if line.startswith("- "):
            items.append(line)
        elif items:
            items[-1] += " " + line.strip()
        else:
            return None
    return items


def _key_values(lines, section_name, warnings):
    """Zeilen "- schluessel: Wert" eines Abschnitts als Liste von Paaren."""
    pairs = []
    for line in lines:
        match = _KEY_VALUE_RE.match(line.strip())
        if match:
            pairs.append((match.group(1).strip(), match.group(2).strip()))
        elif line.strip():
            warnings.append(f"Abschnitt „{section_name}“: Zeile „{line.strip()}“ nicht verstanden")
    return pairs


def _parse_term(heading, lines, category_keys, category_by_label, warnings):
    term = {
        "term": heading,
        "aliases": [],
        "body": [],
        "points": [],
        "body_after": [],
        "related": [],
    }
    for block in _blocks(lines):
        items = _list_items(block) if block[0].startswith("- ") else None
        if items is None:
            paragraph = " ".join(line.strip() for line in block)
            (term["body_after"] if term["points"] else term["body"]).append(paragraph)
            continue
        for item in items:
            point = _POINT_RE.match(item)
            if point:
                term["points"].append((point.group(1).strip(), point.group(2).strip()))
                continue
            meta = _META_RE.match(item)
            key = _META_FIELDS.get(meta.group(1).strip().lower()) if meta else None
            if key is None:
                warnings.append(f"„{heading}“: unbekannte Zeile „{item}“ (erwartet z. B. „- Slug: …“ oder „- **Stichwort:** Text“)")
                continue
            value = meta.group(2).strip()
            term[key] = _split_list(value) if key in _LIST_FIELDS else value

    # Kategorie darf als Schluessel oder als Anzeigename angegeben werden
    category = term.get("category", "")
    if category not in category_keys:
        category = category_by_label.get(category.casefold(), category)
    term["category"] = category

    problems = []
    if not _SLUG_RE.match(term.get("slug", "")):
        problems.append("Slug fehlt oder enthält ungültige Zeichen")
    if category not in category_keys:
        problems.append(f"unbekannte Kategorie „{term.get('category', '')}“")
    if not term.get("short"):
        problems.append("Kurzdefinition („- Kurz: …“) fehlt")
    if problems:
        warnings.append(f"„{heading}“ wird übersprungen: " + "; ".join(problems))
        return None
    return term


def parse_lexicon(text):
    """Markdown-Text einlesen. Gibt ein Dictionary mit categories, quick_terms,
    terms und warnings (Liste von Hinweisen zu fehlerhaften Stellen) zurueck."""
    text = _COMMENT_RE.sub("", text)
    sections = {}  # Abschnittsname -> Zeilen
    terms_raw = []  # (Ueberschrift, Zeilen)
    section = None
    for line in text.splitlines():
        if line.startswith("# "):
            section = line[2:].strip().casefold()
            sections.setdefault(section, [])
        elif line.startswith("## ") and section == _SECTION_TERMS:
            terms_raw.append((line[3:].strip(), []))
        elif section == _SECTION_TERMS and terms_raw:
            terms_raw[-1][1].append(line)
        elif section is not None:
            sections[section].append(line)

    warnings = []
    categories = _key_values(sections.get(_SECTION_CATEGORIES, []), _SECTION_CATEGORIES, warnings)
    quick_terms = _key_values(sections.get(_SECTION_QUICK, []), _SECTION_QUICK, warnings)
    category_keys = {key for key, _ in categories}
    category_by_label = {label.casefold(): key for key, label in categories}

    terms = []
    seen = set()
    for heading, lines in terms_raw:
        term = _parse_term(heading, lines, category_keys, category_by_label, warnings)
        if term is None:
            continue
        if term["slug"] in seen:
            warnings.append(f"„{heading}“ wird übersprungen: Slug „{term['slug']}“ ist doppelt vergeben")
            continue
        seen.add(term["slug"])
        terms.append(term)

    for term in terms:
        for slug in term["related"]:
            if slug not in seen:
                warnings.append(f"„{term['term']}“: Verweis „{slug}“ unter „Siehe auch“ gibt es nicht")
    for slug, _ in quick_terms:
        if slug not in seen:
            warnings.append(f"„Häufig gesucht“: Begriff „{slug}“ gibt es nicht")

    return {
        "categories": categories,
        "category_labels": dict(categories),
        "quick_terms": [(slug, label) for slug, label in quick_terms if slug in seen],
        "terms": terms,
        "warnings": warnings,
    }


_cache = {"mtime": None, "data": None}


def load_lexicon():
    """content/lexicon.md einlesen (zwischengespeichert, solange sich die
    Datei nicht aendert). Bei fehlender Datei bleibt das Lexikon leer."""
    try:
        mtime = os.path.getmtime(LEXICON_FILE)
    except OSError:
        logger.error("Lexikondatei %s nicht gefunden", LEXICON_FILE)
        return parse_lexicon("")
    if _cache["mtime"] != mtime:
        with open(LEXICON_FILE, encoding="utf-8") as handle:
            data = parse_lexicon(handle.read())
        for warning in data["warnings"]:
            logger.warning("Lexikon: %s", warning)
        _cache.update(mtime=mtime, data=data)
    return _cache["data"]


def _sort_key(text):
    """Alphabetische Sortierung ohne Umlaut-Sonderfaelle (Ä wie A usw.)."""
    text = text.replace("ß", "ss")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text.casefold()


def _letter(term):
    first = _sort_key(term)[:1].upper()
    return first if first.isalpha() else "#"


def build_lexicon():
    """Begriffe nach Anfangsbuchstaben gruppieren und Querverweise aufloesen.

    Gibt (groups, terms_by_slug) zurueck; groups ist eine sortierte Liste von
    (Buchstabe, [Eintraege]). Fehlerhafte Slugs in "related" fallen auf
    (statt einen 500er auszuloesen) einfach heraus.
    """
    data = load_lexicon()
    labels = data["category_labels"]
    terms_by_slug = {t["slug"]: t for t in data["terms"]}
    groups = {}
    for term in sorted(data["terms"], key=lambda t: _sort_key(t["term"])):
        entry = dict(term)
        entry["category_label"] = labels.get(term["category"], "")
        entry["related"] = [
            terms_by_slug[slug] for slug in term.get("related", []) if slug in terms_by_slug
        ]
        groups.setdefault(_letter(term["term"]), []).append(entry)
    return sorted(groups.items()), terms_by_slug


if __name__ == "__main__":
    data = load_lexicon()
    print(f"{LEXICON_FILE}: {len(data['terms'])} Begriffe, "
          f"{len(data['categories'])} Kategorien, {len(data['quick_terms'])} „Häufig gesucht“")
    for warning in data["warnings"]:
        print("WARNUNG:", warning)
    raise SystemExit(1 if data["warnings"] else 0)
