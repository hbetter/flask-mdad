"""Bildverarbeitung fuer Beitragsbilder (Article).

Beitragsbilder werden beim Speichern nicht mehr zugeschnitten, sondern nur
auf hoechstens MAX_SIDE Pixel verkleinert und als WebP gespeichert
(Transparenz bleibt erhalten). Wie das Bild in der Kachel dargestellt wird,
bestimmt das Feld Article.image_fit:

- "cover"   Foto fuellt die Kachel, Ueberstand wird abgeschnitten (per CSS,
            Ausschnitt leicht nach oben verschoben, wo meist Gesichter sind).
- "contain" Bild wird vollstaendig gezeigt, mit Rand - fuer Logos/Grafiken.
- "blur"    Foto wird vollstaendig gezeigt, vor einem unscharfen, vergroesserten
            Hintergrund aus demselben Bild - fuer Fotos, die beim Zuschneiden
            zu viel verlieren wuerden (z. B. Hochkant-Fotos).

Mit "auto" wird die Darstellung beim Speichern anhand des Bildes gewaehlt
(siehe classify_image / choose_fit). Dieselben Funktionen nutzen das
Administration (Beitrag hinzufuegen/bearbeiten) und der CSV-Import.
"""

import os
import re
from uuid import uuid4

from PIL import Image, ImageChops, ImageOps, ImageStat

MAX_SIDE = 1600
# Seitenverhaeltnis der Bildflaeche oben in den Beitragkarten
# (.card-img-top in custom.css, 1280 / 715).
TILE_RATIO = 1280 / 715
# Ab diesem Flaechenverlust beim Zuschneiden wird ein Foto statt "cover"
# vollstaendig vor unscharfem Hintergrund ("blur") gezeigt.
MAX_CROP_LOSS = 0.40

FIT_CHOICES = [
    ("auto", "Automatisch (empfohlen)"),
    ("cover", "Füllend – Foto wird passend zugeschnitten"),
    ("contain", "Vollständig – für Logos und Grafiken"),
    ("blur", "Vollständig vor unscharfem Hintergrund – für Hochkant-Fotos"),
]
FIT_VALUES = {"cover", "contain", "blur"}
FIT_LABELS = {"cover": "Füllend", "contain": "Vollständig (Logo)", "blur": "Vollständig (unscharfer Hintergrund)"}

LOGO_NAME_HINT = re.compile(r"logo|award|siegel|badge|preis|zertifikat|icon", re.I)


def _open(source):
    img = Image.open(source)
    img.load()
    # Ausrichtung aus EXIF-Daten (Handyfotos) uebernehmen
    return ImageOps.exif_transpose(img)


def _has_transparency(img):
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        alpha = img.convert("RGBA").getchannel("A").resize((64, 64))
        transparent = sum(alpha.histogram()[:250])
        return transparent / 4096 > 0.02
    return False


def _border_is_uniform(rgb):
    # Schmaler Streifen ringsum nahezu einfarbig -> Hintergrundflaeche
    w, h = rgb.size
    band = max(2, int(min(w, h) * 0.03))
    strips = [
        rgb.crop((0, 0, w, band)), rgb.crop((0, h - band, w, h)),
        rgb.crop((0, 0, band, h)), rgb.crop((w - band, 0, w, h)),
    ]
    return max(max(ImageStat.Stat(s).stddev) for s in strips) < 12


def _few_colors(rgb):
    colors = rgb.resize((64, 64)).getcolors(maxcolors=4096) or []
    return len(colors) < 600


def classify_image(img, filename=""):
    """Liefert "logo" fuer Logos/Grafiken, sonst "photo"."""
    rgb = img.convert("RGB")
    if (_has_transparency(img) or _border_is_uniform(rgb) or _few_colors(rgb)
            or LOGO_NAME_HINT.search(os.path.basename(filename or ""))):
        return "logo"
    return "photo"


def crop_loss(width, height, ratio=TILE_RATIO):
    """Anteil der Bildflaeche, der beim Zuschneiden auf ratio verloren ginge."""
    r = width / height
    return 1 - (min(r, ratio) / max(r, ratio))


def choose_fit(img, filename=""):
    if classify_image(img, filename) == "logo":
        return "contain"
    if crop_loss(*img.size) > MAX_CROP_LOSS:
        return "blur"
    return "cover"


def trim_background(img, tolerance=24):
    """Schneidet bei Logos eine einfarbige oder transparente Flaeche ringsum
    ab, damit das Logo in der Kachel nicht winzig erscheint (den Abstand zum
    Kachelrand gibt das CSS vor). Bilder ohne solche Flaeche bleiben gleich."""
    if img.mode == "RGBA" and _has_transparency(img):
        bbox = img.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    else:
        rgb = img.convert("RGB")
        if not _border_is_uniform(rgb):
            return img
        corner = rgb.getpixel((0, 0))
        diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, corner)).convert("L")
        bbox = diff.point(lambda v: 255 if v > tolerance else 0).getbbox()
    if not bbox:
        return img
    # etwas Rand stehen lassen, damit nichts angeschnitten wirkt
    w, h = img.size
    pad = int(max(bbox[2] - bbox[0], bbox[3] - bbox[1]) * 0.04)
    bbox = (max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(w, bbox[2] + pad), min(h, bbox[3] + pad))
    return img.crop(bbox)


def save_article_image(source, filename, upload_folder, fit="auto"):
    """Verkleinert das Bild (ohne Zuschnitt), speichert es als WebP in
    upload_folder und liefert (neuer_dateiname, image_fit). source ist ein
    Pfad oder ein Datei-Objekt. Loest ValueError aus, wenn es kein Bild ist."""
    try:
        img = _open(source)
    except Exception:
        raise ValueError("keine lesbare Bilddatei")

    if fit not in FIT_VALUES:
        fit = choose_fit(img, filename)

    keep_alpha = _has_transparency(img)
    img = img.convert("RGBA" if keep_alpha else "RGB")
    if fit == "contain":
        img = trim_background(img)
    img.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)

    os.makedirs(upload_folder, exist_ok=True)
    new_name = f"{uuid4().hex}.webp"
    img.save(os.path.join(upload_folder, new_name), "WEBP", quality=85, method=6)
    return new_name, fit


def fit_for_stored_image(path, filename=""):
    """"auto" fuer ein bereits gespeichertes Bild auswerten (Bearbeiten-Formular)."""
    try:
        return choose_fit(_open(path), filename)
    except Exception:
        return "cover"
