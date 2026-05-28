import os
import time
import shutil
import unicodedata
from google import genai

# KONFIGURACJA API - WPISZ TEN SAM KLUCZ CO W YT PROCESSORZE
GEMINI_API_KEY = "AIzaSyAKAGMrkXjM5U01crqdB1QtodQXiNA5PK0"

# Skąd pobieramy i gdzie zapisujemy
SOURCE_DIRS = [
    r"G:\Mój dysk\Kursy Szkolenia Marketing WWW A.I. APLIKACJE",
    r"G:\Mój dysk\Prompty AI_GPT'S",
    r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy"
]
OUTPUT_DIR = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Syntetyczna"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def distill_pdf(client, filepath, filename):
    print(f"\n[INFO] Analiza pliku: {filename}")
    
    # Krok 1: Wgrywamy plik do pamieci Gemini
    print("   [1/3] Wgrywanie do systemu Gemini...")
    
    # Naprawa polskich znakow (Google API wyrzuca błąd przy ścieżkach zawierających polskie litery,
    # dlatego tworzymy tymczasowy plik pod bezpieczną nazwą)
    safe_name = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    temp_filepath = "temp_upload.pdf"
    
    try:
        shutil.copy2(filepath, temp_filepath)
        uploaded_file = client.files.upload(file=temp_filepath, config={'display_name': safe_name})
    except Exception as e:
        print(f"   [BLAD] Błąd wgrywania: {e}")
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        return None
    finally:
        # Zawsze sprzątamy tymczasowy plik
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

    # Krok 2: Czekamy az plik bedzie gotowy do analizy (duze PDFy wymagaja kilku sekund na serwerach Google)
    print("   [2/4] Przetwarzanie pliku przez AI (to moze chwile potrwac)...")
    try:
        while True:
            file_info = client.files.get(name=uploaded_file.name)
            state_str = str(file_info.state).upper()
            if "PROCESSING" in state_str:
                time.sleep(3)
            elif "FAILED" in state_str:
                print("   [BLAD] Plik odrzucony przez Google (prawdopodobnie zaszyfrowany hasłem lub uszkodzony).")
                client.files.delete(name=uploaded_file.name)
                return None
            else:
                break
    except Exception as e:
        print(f"   [BLAD] Błąd podczas sprawdzania statusu pliku: {e}")
        return None

    # Krok 3: Generowanie tresci
    print("   [3/4] Destylacja wiedzy (usuwanie marketingowego szumu)...")
    
    prompt = """
Jesteś Głównym Architektem Systemów. Wgrałem Ci właśnie plik szkoleniowy / PDF ze skryptami biznesowymi lub marketingowymi.
Twoim zadaniem jest "destylacja" tej wiedzy. Odrzuć całe lanie wody, wstępy, marketingowe obietnice i autopromocję autora.

Wyciągnij i zwróć TYLKO:
1. Główne zasady / ramy logiczne (Frameworki).
2. Gotowe schematy, prompty lub szablony, które można skopiować 1:1.
3. Konkretne instrukcje "Krok po Kroku".

Sformatuj to jako bardzo przejrzysty dokument w formacie Markdown (używaj list wypunktowanych, pogrubień dla kluczowych pojęć i bloków kodu ``` dla promptów).
Nie pisz żadnego wstępu od siebie, od razu podaj zdestylowaną wiedzę.
"""
    try:
        # Używamy nowoczesnego modelu gemini-2.5-flash (najszybszy i najlepszy do dużych dokumentów w nowym API)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[uploaded_file, prompt]
        )
        result_text = response.text
    except Exception as e:
        print(f"   [BLAD] Błąd generowania: {e}")
        result_text = None

    # Krok 4: Czyszczenie pamieci
    print("   [4/4] Usuwanie pliku z pamieci chmurowej...")
    try:
        client.files.delete(name=uploaded_file.name)
    except Exception as e:
        pass # Ignoruj błędy usuwania

    return result_text

def main():
    print("="*50)
    print("[SYSTEM] HOLISTIC JASON: DESTYLATOR WIEDZY (PDF -> MD) - WERSJA 2.0")
    print("="*50)
    
    if GEMINI_API_KEY == "WPISZ_TUTAJ_SWOJ_KLUCZ_API":
        print("[BLAD] ZATRZYMANO: Wpisz najpierw swój klucz Gemini API w linii 6!")
        return

    # Inicjalizacja nowego, oficjalnego klienta Google GenAI
    client = genai.Client(api_key=GEMINI_API_KEY)
    processed_count = 0

    for directory in SOURCE_DIRS:
        if not os.path.exists(directory):
            continue
            
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    # Sprawdzamy czy juz tego nie zrobilismy wczesniej
                    base_name = os.path.splitext(file)[0]
                    output_file = os.path.join(OUTPUT_DIR, f"{base_name}.md")
                    
                    if os.path.exists(output_file):
                        print(f"   [POMINIETO] Pomijam: {file} (już zdestylowany)")
                        continue
                        
                    filepath = os.path.join(root, file)
                    distilled_content = distill_pdf(client, filepath, file)
                    
                    if distilled_content:
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(distilled_content)
                        print(f"   [SUKCES] Zapisano: {output_file}")
                        processed_count += 1
                        
                        # Zabezpieczenie przed limitami API (czekamy chwile)
                        time.sleep(5) 

    print("="*50)
    print(f"[SUKCES] DESTYLACJA ZAKOŃCZONA! Zoptymalizowano {processed_count} plików.")
    print(f"Wszystkie czyste pliki znajdziesz w: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
