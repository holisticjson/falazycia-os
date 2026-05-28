"""Batch processor dla Umiejętności Jutra — używa nowego silnika Gemini 2.5 Flash"""
import os
import re
import sys
import time
from pathlib import Path

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"
sys.path.append(r"c:\Aplikacje MVP\Holistic Jason")
from skills.youtube_transcriber import process_course_video_to_md

def extract_links_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    links = re.findall(r"(.*?)\n(https://www\.youtube\.com/watch\?v=[\w-]+)", content)
    return links

def main():
    source_file = Path(r"C:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Kursy Szkolenia Marketing WWW A.I. APLIKACJE\Google Umiejętności Jutra 3.0\Tydzień 1 (Fundamenty AI i produktywność osobista)\Program_Linki.md.txt")

    if not source_file.exists():
        print(f"BLAD: Nie znaleziono pliku {source_file}")
        return

    links = extract_links_from_file(source_file)
    print(f"Znaleziono {len(links)} filmow do przetworzenia.")

    baza_dir = Path(r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Kursy_i_Szkolenia")
    
    for idx, (title, url) in enumerate(links):
        title = title.strip().replace("(nieobowiązkowa) ", "")
        if not title or len(title) < 3:
            title = f"Lekcja_{url[-11:]}"

        # Sprawdź czy plik już istnieje
        safe_title = "".join([c if c.isalnum() else "_" for c in title])[:80]
        target_file = baza_dir / f"Umiejetnosci_Jutra_{safe_title}.md"
        if target_file.exists():
            print(f"[{idx+1}/{len(links)}] SKIP (istnieje): {title}")
            continue

        print(f"[{idx+1}/{len(links)}] Przetwarzanie: {title}")
        try:
            result = process_course_video_to_md(url, title)
            print(f"  -> {result[:80]}")
        except Exception as e:
            print(f"  -> BLAD: {e}")
        
        # Pauza żeby nie przekroczyć limitów API
        time.sleep(3)

if __name__ == "__main__":
    main()
