import os
from pypdf import PdfReader
from google import genai

GEMINI_API_KEY = "AIzaSyAKAGMrkXjM5U01crqdB1QtodQXiNA5PK0"
client = genai.Client(api_key=GEMINI_API_KEY)

directories = [
    r"G:\Mój dysk\Kursy Szkolenia Marketing WWW A.I. APLIKACJE",
    r"G:\Mój dysk\Prompty AI_GPT'S",
    r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy"
]

target_file = None
for d in directories:
    if not os.path.exists(d): continue
    for root, dirs, files in os.walk(d):
        for f in files:
            if "Skarbiec_150_Skryptow" in f and f.endswith(".pdf"):
                target_file = os.path.join(root, f)
                break
        if target_file: break
    if target_file: break

if target_file:
    print(f"Znaleziono: {target_file}")
    
    print("Wyciąganie tekstu z PDF lokalnie (omijanie bledu wgrywania)...")
    try:
        reader = PdfReader(target_file)
        full_text = ""
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text += text + "\n"
                
        if not full_text.strip():
            print("PDF jest zbudowany ze zdjęć (brak tekstu). Gemini potrzebuje tekstu.")
            exit()
            
        print(f"Pobrano {len(full_text)} znakow. Wysylanie do Gemini...")
        
        prompt = f"""
Jesteś Głównym Architektem Systemów. Poniżej znajduje się treść dokumentu.
Wyciągnij i zwróć TYLKO:
1. Główne zasady / ramy logiczne (Frameworki).
2. Gotowe schematy, prompty lub szablony, które można skopiować 1:1.
3. Konkretne instrukcje "Krok po Kroku".
Sformatuj w Markdown.

TRESC DOKUMENTU:
{full_text}
"""
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        out_path = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Syntetyczna\Skarbiec_150_Skryptow.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"GOTOWE! Zapisano do: {out_path}")
        
    except Exception as e:
        print(f"Blad API lub odczytu: {e}")
else:
    print("Nie znaleziono pliku.")
