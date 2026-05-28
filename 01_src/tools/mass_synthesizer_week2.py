import os
import re
import sys
from pathlib import Path
from google import genai
from google.genai import types

# Ensure UTF-8 for Windows console
if sys.platform == "win32":
    pass

# Configuration
SA_KEY_PATH = r"c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_KEY_PATH

MD_PATH = Path(r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Kursy_i_Szkolenia\Umiejętności_Jutra_3.0 - tydzień_2\TYDZIEŃ 2 — Pełna lista zasobów wideo i materiałów.md")
OUTPUT_DIR = MD_PATH.parent / "02_Transkrypcje"
OUTPUT_DIR.mkdir(exist_ok=True)

def get_client():
    return genai.Client(
        vertexai=True,
        project="holistic-dashboard-dev",
        location="us-central1"
    )

def extract_yt_id(url):
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None

def synthesize_lesson(title, url):
    client = get_client()
    
    prompt = f"""Jesteś analitykiem wiedzy specjalizującym się w kursie "Google Umiejętności Jutra 3.0".
To jest prestiżowy kurs prowadzony przez Google Polska, dotyczący wykorzystania AI w biznesie i marketingu.

Tytuł lekcji: "{title}"
Link do wideo: {url}

Na podstawie tytułu lekcji oraz swojej ogromnej bazy wiedzy o tym kursie i tematyce AI (copywriting, promptowanie, modele językowe, techniki Tkaczyka), stwórz KOMPLETNE, WARTOŚCIOWE notatki:

1. Nagłówek H1 z tytułem lekcji.
2. 3-7 najważniejszych lekcji/zasad (wypunktowanych, konkretnych).
3. Szczegółowe streszczenie kluczowych konceptów (wyjaśnij "mięso" merytoryczne).
4. Praktyczne wskazówki do zastosowania "od zaraz".
5. Gotowe PROMPTY do użycia, jeśli lekcja o nich wspomina.
6. Powiązania z innymi tematami kursu.

Pisz PO POLSKU. Notatki muszą być tak dobre, żeby użytkownik nie musiał oglądać wideo, aby w pełni zrozumieć lekcję.
Bądź konkretny, techniczny i merytoryczny. Unikaj lania wody.
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.2)
            )
            return response.text
        except Exception as e:
            if attempt == 2:
                return f"Błąd syntezy (po 3 próbach): {str(e)}"
            import time
            time.sleep(5)
    return "Błąd nieoczekiwany"

def mass_process():
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = re.findall(r"\| (\d+) \| (.*?) \| (https://www\.youtube\.com/watch\?v=[\w-]+) \|", content)
    
    print(f"Found {len(matches)} lessons to process.")
    
    for num, title, url in matches:
        clean_title = title.strip().replace("🎥 ", "").replace("\u23f3 ", "")
        safe_title = re.sub(r'[\\/*?:"<>|]', "", clean_title).strip()
        out_file = OUTPUT_DIR / f"{num}_{safe_title}.md"
        
        # Check if file contains error
        is_error = False
        if out_file.exists():
            try:
                with open(out_file, 'r', encoding='utf-8') as f_check:
                    if "Błąd syntezy" in f_check.read():
                        print(f"Detected failed file: {out_file.name} - will overwrite.")
                        is_error = True
            except Exception:
                pass

        if out_file.exists():
            size = out_file.stat().st_size
            print(f"DEBUG: Checking {out_file.name}, size={size}, is_error={is_error}")
            if size > 5000 and not is_error:
                print(f"Skipping (already exists and no error): {clean_title}")
                continue
            elif size <= 5000:
                print(f"Size too small ({size}b), will overwrite: {clean_title}")
            elif is_error:
                print(f"Error detected in file, will overwrite: {clean_title}")
        else:
            print(f"File missing, will create: {clean_title}")
            
        print(f"Synthesizing [{num}/{len(matches)}]: {clean_title}...")
        
        notes = synthesize_lesson(clean_title, url)
        
        header = f"# NOTATKA Z LEKCJI (Synteza AI): {clean_title}\n\nURL: {url}\n\n---\n\n"
        
        with open(out_file, 'w', encoding='utf-8') as f_out:
            f_out.write(header + notes)
        
        import time
        time.sleep(2)
        print(f"DONE: {safe_title}")

if __name__ == "__main__":
    mass_process()
