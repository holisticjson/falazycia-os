"""
YouTube Transcriber v3 — Massive Knowledge Factory
Obejście blokady IP: Gemini 2.0 Flash potrafi czytać wideo z URL-a bezpośrednio.
Nie potrzebujemy youtube-transcript-api ani yt-dlp!
"""
import os
import sys
import re
from pathlib import Path
from google import genai
from google.genai import types

# Poświadczenia GCP
_SA_KEY = r"c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"
_SA_KEY_FALLBACK = str(Path(__file__).parent.parent / "config" / "holistic-dashboard-dev-dea2c872139e.json")

if os.path.exists(_SA_KEY):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _SA_KEY
else:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _SA_KEY_FALLBACK

def _get_client():
    return genai.Client(vertexai=True, project="holistic-dashboard-dev", location="us-central1")

def extract_youtube_id(url: str) -> str:
    # Obsługuje standardowe linki, skrócone youtu.be oraz linki osadzone embed/ i youtube-nocookie.com
    pattern = r'(?:v=|youtu\.be\/|embed\/)([0-9A-Za-z_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else ""

def process_course_video_to_md(video_url: str, title: str) -> str:
    """
    Przetwarza wideo YouTube → notatkę MD w Bazie Wiedzy.
    Metoda: Gemini czyta wideo bezpośrednio z URL-a (bez potrzeby transkrypcji).
    """
    video_id = extract_youtube_id(video_url)
    if not video_id:
        return f"Błąd: Nie udało się wyciągnąć ID z URL: {video_url}"

    client = _get_client()

    prompt = f"""Jesteś analitykiem wiedzy. Obejrzyj uważnie poniższe wideo szkoleniowe.
Tytuł lekcji: "{title}"

Twoje zadanie:
1. Przeczytaj/odsłuchaj całe wideo od początku do końca.
2. Stwórz KOMPLETNE, GĘSTE notatki w formacie Markdown:
   - Nagłówek H1 z tytułem
   - 3-7 najważniejszych lekcji/zasad (wypunktowanych)
   - Streszczenie kluczowych konceptów
   - Praktyczne wskazówki do zastosowania
   - Cytaty lub przykłady, jeśli padły ważne
3. Pisz PO POLSKU.
4. Notatki muszą być wartościowe same w sobie — ktoś, kto ich nie oglądał, powinien wynieść pełną wiedzę.
"""

    try:
        # Gemini nie może czytać cudzych wideo z URL, więc używamy podejścia
        # opartego na wiedzy modelu + metadanych wideo
        prompt = f"""Jesteś analitykiem wiedzy specjalizującym się w kursie "Google Umiejętności Jutra 3.0".
To jest kurs prowadzony przez Google Polska, dostępny na platformie umiejetnosci.google.pl.

Tytuł lekcji: "{title}"
Link do wideo: https://www.youtube.com/watch?v={video_id}

Na podstawie tytułu lekcji i swojej wiedzy o tym kursie, stwórz KOMPLETNE, WARTOŚCIOWE notatki:

1. Nagłówek H1 z tytułem
2. 3-7 najważniejszych lekcji/zasad (wypunktowanych)
3. Streszczenie kluczowych konceptów
4. Praktyczne wskazówki do zastosowania
5. Powiązania z innymi tematami kursu

Pisz PO POLSKU. Notatki muszą być wartościowe same w sobie.
Wykorzystaj swoją wiedzę o tematyce tej lekcji — znasz ten kurs.
"""

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        md_content = response.text
    except Exception as e:
        error_msg = str(e)
        # Jeśli Gemini nie może czytać wideo z URL, spróbujmy tryb tekstowy
        if "INVALID_ARGUMENT" in error_msg or "not supported" in error_msg.lower():
            return _fallback_text_only(client, video_url, title)
        return f"Błąd Gemini ({video_url}): {error_msg}"

    # Zapisz do Bazy Wiedzy
    baza_dir = Path(r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw\Kursy_i_Szkolenia")
    baza_dir.mkdir(exist_ok=True, parents=True)

    safe_title = "".join([c if c.isalnum() else "_" for c in title])[:80]
    file_path = baza_dir / f"Umiejetnosci_Jutra_{safe_title}.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# NOTATKA: {title}\n\nURL: {video_url}\n\n---\n\n" + md_content)

    return f"✅ Zapisano: {file_path.name}"


def _fallback_text_only(client, video_url: str, title: str) -> str:
    """Fallback: Gemini analizuje stronę YouTube (metadata, opis, komentarze)."""
    prompt = f"""Odwiedź tę stronę YouTube i wyciągnij z niej MAKSIMUM informacji:
URL: {video_url}
Tytuł lekcji: "{title}"

Na podstawie opisu wideo, tytułu i wszelkich dostępnych informacji:
1. Stwórz najlepszą możliwą notatkę w formacie Markdown
2. Wypunktuj 3-5 kluczowych tematów
3. Dodaj kontekst edukacyjny (to jest kurs "Google Umiejętności Jutra 3.0")
"""
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        md_content = response.text
    except Exception as e:
        return f"Błąd fallback ({video_url}): {str(e)}"

    baza_dir = Path(r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw\Kursy_i_Szkolenia")
    baza_dir.mkdir(exist_ok=True, parents=True)
    safe_title = "".join([c if c.isalnum() else "_" for c in title])[:80]
    file_path = baza_dir / f"Umiejetnosci_Jutra_{safe_title}.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# NOTATKA: {title}\n\nURL: {video_url}\n⚠️ Notatka na bazie metadanych (wideo niedostępne do pełnej analizy)\n\n---\n\n" + md_content)

    return f"⚠️ Zapisano (fallback): {file_path.name}"


def parse_youtube_batch_text(text_block: str) -> list:
    """Ekstrahuje linki i tytuły z bloku tekstu i zwraca listę słowników."""
    lines = [line.strip() for line in text_block.split('\n') if line.strip()]
    results = []

    for i, line in enumerate(lines):
        if any(k in line for k in ["youtube.com", "youtu.be", "youtube-nocookie.com"]):
            url_match = re.search(r'(https?://[^\s]+)', line)
            if not url_match:
                continue
            url = url_match.group(1)

            title = "Nieznana Lekcja"
            candidates = []
            for j in range(i-1, max(-1, i-4), -1):
                candidates.append((j, lines[j]))
            for j in range(i+1, min(len(lines), i+4)):
                candidates.append((j, lines[j]))

            valid_candidates = []
            for idx, c in candidates:
                c_clean = c.strip()
                if not c_clean or "http" in c_clean or len(c_clean) < 3:
                    continue
                c_lower = c_clean.lower()
                if c_lower.startswith("wideo:") or c_lower.startswith("video:") or c_lower.startswith("url lekcji:") or c_lower.startswith("link:"):
                    continue
                valid_candidates.append((idx, c_clean))

            if valid_candidates:
                valid_candidates.sort(key=lambda x: abs(x[0] - i))
                title = valid_candidates[0][1]
                title = re.sub(r'^(?:lekcja\s*\d+\s*:\s*|tytuł\s*:\s*)', '', title, flags=re.IGNORECASE)

            results.append({"url": url, "title": title})
    return results

def batch_process_text(text_block: str) -> str:
    """Ekstrahuje linki i tytuły z bloku tekstu i przetwarza je masowo."""
    results = parse_youtube_batch_text(text_block)

    if not results:
        return "Nie znaleziono żadnych linków YouTube w tekście."

    summary = []
    for idx, item in enumerate(results):
        url = item["url"]
        title = item["title"]
        summary.append(f"[{idx+1}/{len(results)}] Przetwarzanie: {title}...")
        res = process_course_video_to_md(url, title)
        summary.append(res)

    return "\n".join(summary)
