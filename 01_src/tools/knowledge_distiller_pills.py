import os
import time
import json
import re
from google import genai

GEMINI_API_KEY = "AIzaSyAKAGMrkXjM5U01crqdB1QtodQXiNA5PK0" # z destylator_wiedzy.py

def extract_json(text):
    match = re.search(r'```json\n(.*?)```', text, re.DOTALL)
    if match:
        return match.group(1)
    match = re.search(r'\[\s*\{.*?\}\s*\]', text, re.DOTALL)
    if match:
        return match.group(0)
    return text

def main():
    print("="*50)
    print("[SYSTEM] HOLISTIC JASON: GENERATOR PIGUŁEK WIEDZY (ADHD & AGENTS)")
    print("="*50)
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    dirs_to_scan = [
        r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw\Google Umiejętności Jutra 3.0",
        r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\synthesized"
    ]
    
    output_dir = r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\pills"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "pills.json")
    
    all_pills = []
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            all_pills = json.load(f)
            
    processed_files = [p.get('source_file') for p in all_pills if 'source_file' in p]
    
    files_to_process = []
    for d in dirs_to_scan:
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith('.md'):
                    files_to_process.append(os.path.join(root, file))
                    
    # Wybieramy tylko pierwsze 5 plików (w tym te z kursu Google, jeśli są na początku)
    # Żeby pokazać szybki efekt i nie zablokować API.
    files_to_process = [f for f in files_to_process if f not in processed_files][:5]
    
    if not files_to_process:
        print("Nie ma nowych plików do przetworzenia.")
        return

    prompt = """
    Jesteś analitykiem wiedzy dla systemu Holistic CEO. 
    Przeczytaj poniższy tekst z transkrypcji szkolenia i wyciągnij z niego od 1 do 3 najważniejszych, praktycznych "Pigułek Wiedzy".
    Każda pigułka musi być krótka, konkretna (max 3 punkty) - idealna dla osoby z ADHD oraz łatwa do wstrzyknięcia do promptu Agenta AI.
    
    ZWRÓĆ WYNIK WYŁĄCZNIE JAKO POPRAWNY JSON (tablica obiektów) wg formatu:
    [
      {
        "title": "Tytuł metody/techniki",
        "category": "Kategoria np. Prompty, Social Media, Sprzedaż",
        "bullets": ["Zasada 1", "Zasada 2", "Zasada 3"]
      }
    ]
    Nie pisz żadnego innego tekstu, tylko tablicę JSON.
    """
    
    for filepath in files_to_process:
        print(f"[Analiza] {os.path.basename(filepath)}...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Obcinamy plik do ~10k znaków, by zmieścił się szybko i bez halucynacji
            content = content[:10000]
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[prompt + "\n\nTEKST:\n" + content]
            )
            
            json_text = extract_json(response.text)
            pills = json.loads(json_text)
            
            for pill in pills:
                pill['source_file'] = filepath
                all_pills.append(pill)
                
            print(f"  -> Wyciągnięto {len(pills)} pigułek.")
            time.sleep(2) # Anty-limit
        except Exception as e:
            print(f"  [BŁĄD przy {os.path.basename(filepath)}] {e}")
            
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_pills, f, ensure_ascii=False, indent=4)
        
    print(f"\n[SUKCES] Zapisano w sumie {len(all_pills)} pigułek w {output_file}")
    print("Format jest gotowy do zaczytania w Streamlit oraz dla agentów.")

if __name__ == "__main__":
    main()
