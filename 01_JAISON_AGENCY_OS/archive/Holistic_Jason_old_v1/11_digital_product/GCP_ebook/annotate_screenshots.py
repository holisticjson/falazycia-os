"""
📸 Screenshot Annotator — Post-processing screenshotów do e-booka GCP
=====================================================================
Skrypt do batch-processingu surowych screenshotów:
1. Blur danych wrażliwych (e-mail, Project ID, billing)
2. Strzałki wskazujące elementy UI
3. Podpisy i numeracja kroków
4. Eksport w jednolitej rozdzielczości 1200px szerokości

Wymagania: pip install Pillow
Użycie:
  python annotate_screenshots.py                    # Przetwarza wszystkie z raw/ do annotated/
  python annotate_screenshots.py --file ETAP_01.png # Przetwarza konkretny plik
  python annotate_screenshots.py --blur-only        # Tylko blurowanie, bez adnotacji
"""

import os
import sys
import json
import argparse
from pathlib import Path

try:
    from PIL import Image, ImageFilter, ImageDraw, ImageFont
except ImportError:
    print("❌ Brak biblioteki Pillow. Zainstaluj:")
    print("   pip install Pillow")
    sys.exit(1)

# --- KONFIGURACJA ---
BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "screenshots" / "raw"
ANNOTATED_DIR = BASE_DIR / "screenshots" / "annotated"
CONFIG_FILE = BASE_DIR / "screenshots" / "annotations_config.json"

TARGET_WIDTH = 1200  # px — optymalna szerokość dla PDF A4
BLUR_RADIUS = 25     # Siła rozmycia danych wrażliwych
ARROW_COLOR = (220, 38, 38)   # Czerwony (#DC2626)
LABEL_BG_COLOR = (220, 38, 38, 200)  # Półprzezroczysty czerwony
LABEL_TEXT_COLOR = (255, 255, 255)    # Biały tekst
BORDER_COLOR = (59, 130, 246)  # Niebieski (#3B82F6) — ramka wokół screenshota
BORDER_WIDTH = 3


def load_config() -> dict:
    """Ładuje konfigurację adnotacji z pliku JSON."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def resize_to_target(img: Image.Image) -> Image.Image:
    """Skaluje obraz do docelowej szerokości zachowując proporcje."""
    if img.width <= TARGET_WIDTH:
        return img
    ratio = TARGET_WIDTH / img.width
    new_height = int(img.height * ratio)
    return img.resize((TARGET_WIDTH, new_height), Image.Resampling.LANCZOS)


def apply_blur_regions(img: Image.Image, regions: list[dict]) -> Image.Image:
    """Nakłada blur na zdefiniowane regiony (dane wrażliwe)."""
    for region in regions:
        x1, y1, x2, y2 = region["x1"], region["y1"], region["x2"], region["y2"]
        # Wytnij region, rozmyj, wklej z powrotem
        crop = img.crop((x1, y1, x2, y2))
        blurred = crop.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))
        img.paste(blurred, (x1, y1))
    return img


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple, end: tuple, 
               color: tuple = ARROW_COLOR, width: int = 4):
    """Rysuje linię ze strzałką."""
    import math
    draw.line([start, end], fill=color, width=width)
    
    # Grot strzałki
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    arrow_len = 20
    arrow_angle = math.pi / 6  # 30 stopni
    
    x1 = end[0] - arrow_len * math.cos(angle - arrow_angle)
    y1 = end[1] - arrow_len * math.sin(angle - arrow_angle)
    x2 = end[0] - arrow_len * math.cos(angle + arrow_angle)
    y2 = end[1] - arrow_len * math.sin(angle + arrow_angle)
    
    draw.polygon([end, (x1, y1), (x2, y2)], fill=color)


def draw_label(img: Image.Image, position: tuple, text: str, 
               font_size: int = 16) -> Image.Image:
    """Rysuje etykietę z tłem na obrazie."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except (OSError, IOError):
        font = ImageFont.load_default()
    
    bbox = draw.textbbox(position, text, font=font)
    padding = 8
    rect = (bbox[0] - padding, bbox[1] - padding, 
            bbox[2] + padding, bbox[3] + padding)
    
    draw.rounded_rectangle(rect, radius=6, fill=LABEL_BG_COLOR)
    draw.text(position, text, fill=LABEL_TEXT_COLOR, font=font)
    
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def add_border(img: Image.Image) -> Image.Image:
    """Dodaje delikatną ramkę wokół screenshota."""
    draw = ImageDraw.Draw(img)
    draw.rectangle(
        [0, 0, img.width - 1, img.height - 1], 
        outline=BORDER_COLOR, 
        width=BORDER_WIDTH
    )
    return img


def add_step_number(img: Image.Image, step_text: str) -> Image.Image:
    """Dodaje numer kroku w górnym lewym rogu."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except (OSError, IOError):
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), step_text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    padding = 10
    
    # Tło numeru kroku
    draw.rounded_rectangle(
        [8, 8, 8 + w + 2*padding, 8 + h + 2*padding],
        radius=8,
        fill=(17, 24, 39, 220)  # Ciemnogranatowy
    )
    draw.text((8 + padding, 8 + padding), step_text, 
              fill=(255, 255, 255), font=font)
    
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def process_screenshot(filename: str, config: dict, blur_only: bool = False):
    """Przetwarza pojedynczy screenshot."""
    src = RAW_DIR / filename
    dst = ANNOTATED_DIR / filename
    
    if not src.exists():
        print(f"  ⚠️ Plik nie istnieje: {src}")
        return
    
    img = Image.open(src)
    print(f"  📐 Oryginalny rozmiar: {img.width}x{img.height}")
    
    # 1. Skalowanie
    img = resize_to_target(img)
    
    # 2. Blur danych wrażliwych
    file_config = config.get(filename, {})
    blur_regions = file_config.get("blur_regions", [])
    if blur_regions:
        img = apply_blur_regions(img, blur_regions)
        print(f"  🔒 Wyblurowano {len(blur_regions)} regionów")
    
    if not blur_only:
        # 3. Strzałki
        arrows = file_config.get("arrows", [])
        if arrows:
            draw = ImageDraw.Draw(img)
            for arrow in arrows:
                draw_arrow(draw, 
                          tuple(arrow["start"]), 
                          tuple(arrow["end"]))
            print(f"  ➡️ Dodano {len(arrows)} strzałek")
        
        # 4. Etykiety
        labels = file_config.get("labels", [])
        for label in labels:
            img = draw_label(img, tuple(label["position"]), label["text"])
        if labels:
            print(f"  🏷️ Dodano {len(labels)} etykiet")
        
        # 5. Numer kroku
        step = file_config.get("step_number")
        if step:
            img = add_step_number(img, step)
        
        # 6. Ramka
        img = add_border(img)
    
    # 7. Zapis
    img.save(dst, "PNG", optimize=True)
    print(f"  ✅ Zapisano: {dst}")


def main():
    parser = argparse.ArgumentParser(
        description="📸 Annotator screenshotów do e-booka GCP"
    )
    parser.add_argument("--file", type=str, help="Przetwórz konkretny plik")
    parser.add_argument("--blur-only", action="store_true",
                       help="Tylko blur, bez strzałek i adnotacji")
    args = parser.parse_args()
    
    ANNOTATED_DIR.mkdir(parents=True, exist_ok=True)
    config = load_config()
    
    if args.file:
        files = [args.file]
    else:
        files = sorted([f.name for f in RAW_DIR.glob("*.png")])
        if not files:
            print("📂 Brak plików PNG w katalogu screenshots/raw/")
            print(f"   Ścieżka: {RAW_DIR}")
            print("   Umieść tam surowe screenshoty i uruchom ponownie.")
            return
    
    print(f"--- Przetwarzam {len(files)} screenshotow... ---")
    print(f"   Zrodlo:  {RAW_DIR}")
    print(f"   Cel:     {ANNOTATED_DIR}")
    print()
    
    for filename in files:
        print(f"Screenshot: {filename}")
        process_screenshot(filename, config, args.blur_only)
        print()
    
    print(f"Gotowe! Przetworzone pliki w: {ANNOTATED_DIR}")


if __name__ == "__main__":
    main()
