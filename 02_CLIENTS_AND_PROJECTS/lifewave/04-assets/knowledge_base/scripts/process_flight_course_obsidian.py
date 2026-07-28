import os
import sys
import time
import re
import json
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from google import genai
from google.genai import types

load_dotenv()

# Base directories
BASE_DIR = r"C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\lifewave\04-assets\knowledge_base"
OBSIDIAN_DIR = os.path.join(BASE_DIR, "obsidian_notes")
MOC_FILE = os.path.join(BASE_DIR, "00_FLIGHT_HACKING_MOC_OBSIDIAN.md")

os.makedirs(OBSIDIAN_DIR, exist_ok=True)

# Initialize Gemini Client with Gemini 2.5 Flash
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ BŁĄD: Brak GEMINI_API_KEY w środowisku / .env!")
    sys.exit(1)

client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-2.5-flash"

SYSTEM_PROMPT = """Jesteś Analitykiem Wiedzy i Architektem Bazy RAG dla Obsidian.
Twoim zadaniem jest przetworzenie surowej treści i transkrypcji lekcji z kursu Piotra Lotniczego "Akademia Punktów - Loty w Klasie Biznes za Punkty" na profesjonalną, przejrzystą notatkę Markdown zoptymalizowaną pod system Obsidian RAG.

ZASADY TWORZENIA NOTATKI:
1. BEZWZGLĘDNY ZAKAZ HALUCYNACJI: Opieraj się WYŁĄCZNIE na podanym tekście lekcji i transkrypcji. Nie dopisuj niepotwierdzonych reguł ani zmyślonych przeliczników.
2. STRUKTURA OBSIDIAN MARKDOWN:
   - Zacznij od nagłówka YAML (frontmatter) z tagami: #flight-hacking #biznes-klasa #punkty-milowe
   - Zastosuj czytelną hierarchię nagłówków (#, ##, ###), listy wypunktowane i pogrubienia <strong>ważnych pojęć</strong>.
   - Jeśli w tekście występują wyszukiwarki (np. Seats.aero, Roame.travel, AwardTool, Point.me) lub programy (Aeroplan, Avios, Flying Blue, Miles & More), wyodrębnij je w sekcji narzędzi.
3. JĘZYK: Polski, profesjonalny, konkretny, pozbawiony zbędnego lania wody (ADHD-friendly format).

FORMAT WYJŚCIOWY:
```markdown
---
title: "Tytuł Lekcji"
source: "Piotr Lotniczy - Akademia Punktów"
tags:
  - flight-hacking
  - biznes-klasa
  - milowe-okazje
url: "URL_LEKCJI"
date: "2026-07-28"
---

# ✈️ Tytuł Lekcji

## 🎯 Główny Cel & Założenia
[Streszczenie celu lekcji w 2-3 zdaniach]

## 🧠 Kluczowa Wiedza & Transkrypcja
[Usystematyzowane, punktowe podsumowanie treści lekcji i transkrypcji]

## 🛠️ Strategie & Formuły Flight Hacking
[Instrukcja krok po kroku / zasady przeliczania / wyszukiwania]

## 💡 Narzędzia & Programy Milowe
[Lista wspomnianych w lekcji narzędzi i linii lotniczych z podlinkowaniem lub wyjaśnieniem]
```
"""

def sanitize_filename(name):
    clean = re.sub(r'[\\/*?:"<>|]', "", name)
    clean = clean.replace(" ", "_")
    return clean[:80]

def process_lesson_with_gemini(lesson_id, title, url, raw_text):
    print(f"  🧠 Przetwarzanie lekcji w Gemini 2.5 Flash: {title}...")
    user_prompt = f"""Oto surowa treść i transkrypcja z lekcji #{lesson_id} kursu Piotra Lotniczego:

TYTUŁ: {title}
URL: {url}

SUROWA TREŚĆ I TRANSKRYPCJA:
{raw_text[:30000]}

Przygotuj kompletną notatkę Obsidian Markdown zgodną ze wskazaniami w system prompt."""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
            )
        )
        return response.text
    except Exception as e:
        print(f"  ⚠️ Błąd podczas wywoływania Gemini: {e}")
        return None

def main():
    print("=" * 70)
    print("🚀 PROCESOR KURSU PIOTRA LOTNICZEGO -> OBSIDIAN RAG (GEMINI 2.5 FLASH)")
    print("=" * 70)

    # Lesson range to scan
    start_lesson = 2
    end_lesson = 65

    with sync_playwright() as p:
        print("\n🌐 Uruchamiam okno przeglądarki Chrome...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        first_url = f"https://piotrlotniczy.elms.pl/next/public/lesson/{start_lesson}"
        page.goto(first_url)

        print("\n👉 Zaloguj się w otwartym oknie przeglądarki, jeśli jest to wymagane.")
        print("👉 Gdy strona lekcji załaduje się poprawnie, wróć tutaj i naciśnij ENTER:\n")
        input(">>> NACIŚNIJ ENTER ABY ROZPOCZĄĆ MASOWĄ POBIERANIE & TRANSKRYPCJĘ <<< ")

        created_notes = []

        for lesson_id in range(start_lesson, end_lesson + 1):
            url = f"https://piotrlotniczy.elms.pl/next/public/lesson/{lesson_id}"
            print(f"\n📖 [{lesson_id - start_lesson + 1}/{end_lesson - start_lesson + 1}] Pobieram: {url}")

            try:
                active_page = context.pages[-1] if context.pages else page
                response = active_page.goto(url, wait_until="domcontentloaded", timeout=12000)
                
                # Check 404 or redirect
                if response and response.status >= 400:
                    print(f"  ⏩ Pomijam (kod odpowiedzi HTTP {response.status})")
                    continue

                active_page.wait_for_load_state("networkidle", timeout=5000)
                time.sleep(1)

                # Extract Title
                title = ""
                try:
                    title_elem = active_page.query_selector("h1, .lesson-title, .training-header")
                    if title_elem:
                        title = title_elem.inner_text().strip()
                except Exception:
                    pass

                if not title:
                    title = f"Lekcja {lesson_id}"

                # Extract Text / Transcript / VTT / Captions
                raw_text = ""
                try:
                    body_text = active_page.inner_text("body")
                    raw_text += body_text
                except Exception:
                    pass

                # Check for transcript containers or iframes
                try:
                    transcripts = active_page.query_selector_all(".transcript, .subtitles, .vtt-content, .video-transcript")
                    for t in transcripts:
                        raw_text += "\n\nTRANSKRYPCJA WIDEO:\n" + t.inner_text()
                except Exception:
                    pass

                if len(raw_text.strip()) < 50:
                    print("  ⏩ Pomijam lekcję (brak treści / pusta strona).")
                    continue

                # Process with Gemini 2.5 Flash
                note_content = process_lesson_with_gemini(lesson_id, title, url, raw_text)
                
                if note_content:
                    filename = f"Lekcja_{lesson_id:02d}_{sanitize_filename(title)}.md"
                    filepath = os.path.join(OBSIDIAN_DIR, filename)

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(note_content)

                    print(f"  ✅ Zapisano notatkę Obsidian: {filename}")
                    created_notes.append({"id": lesson_id, "title": title, "filename": filename, "url": url})

            except Exception as e:
                print(f"  ⚠️ Błąd podczas przetwarzania lekcji {lesson_id}: {e}")
                continue

        # Generate MOC (Map of Content) file for Obsidian
        print("\n🗺️ Generowanie Mapy Treści Obsidian (MOC)...")
        moc_lines = []
        moc_lines.append("# 🗺️ MAPA TREŚCI (MOC): Kurs Piotra Lotniczego – Akademia Punktów\n")
        moc_lines.append("> Scentralizowany indeks notatek Obsidian RAG przetworzonych przez Gemini 2.5 Flash.\n\n")
        moc_lines.append("## 📚 Wykaz Lekcji i Notatek:\n\n")

        for item in created_notes:
            moc_lines.append(f"* [[{item['filename'].replace('.md', '')}|Lekcja {item['id']}: {item['title']}]] – [Link do eLMS]({item['url']})\n")

        with open(MOC_FILE, "w", encoding="utf-8") as f:
            f.writelines(moc_lines)

        print(f"\n🎉 SUKCES! Przetworzono {len(created_notes)} lekcji.")
        print(f"📁 Folder Notatek Obsidian: {OBSIDIAN_DIR}")
        print(f"📄 Plik Główny MOC: {MOC_FILE}")

if __name__ == "__main__":
    main()
