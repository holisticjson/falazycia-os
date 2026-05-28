import os
import time
import json
import re
from google import genai

GEMINI_API_KEY = "AIzaSyAKAGMrkXjM5U01crqdB1QtodQXiNA5PK0"

def extract_json(text):
    match = re.search(r'```json\n(.*?)```', text, re.DOTALL)
    if match:
        return match.group(1)
    match = re.search(r'\[\s*\{.*?\}\s*\]', text, re.DOTALL)
    if match:
        return match.group(0)
    return text

def main():
    print("="*60)
    print("[SYSTEM] HOLISTIC JASON: DEEP KNOWLEDGE DISTILLER v3")
    print("="*60)
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    dirs_to_scan = [
        r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw\Google Umiejętności Jutra 3.0",
        r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\synthesized"
    ]
    
    output_dir = r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\protocols"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "deep_protocols.json")
    
    all_protocols = []
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            try:
                all_protocols = json.load(f)
            except json.JSONDecodeError:
                all_protocols = []
            
    processed_files = [p.get('source_file') for p in all_protocols if 'source_file' in p]
    
    files_to_process = []
    for d in dirs_to_scan:
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith('.md'):
                    files_to_process.append(os.path.join(root, file))
                    
    files_to_process = [f for f in files_to_process if f not in processed_files][:3]
    
    if not files_to_process:
        print("Brak nowych plików do pogłębionej analizy.")
        return

    prompt = """
    Jesteś Architektem Wiedzy dla systemu Holistic CEO.
    Przeczytaj transkrypcję/notatki szkoleniowe. Zamiast streszczać to do "pigułek", zbuduj **Głęboki Protokół Operacyjny (Deep Action Protocol)**.
    Dla osoby z ADHD kluczowa jest HIERARCHIA i WIZUALIZACJA, a nie skracanie materiału. Chcemy 100% wartości szkolenia.

    Zwróć wynik jako TABLICĘ JSON (array) zawierającą 1-2 główne tematy z tekstu w poniższym formacie:
    [
      {
        "title": "Główny Temat / Moduł z tekstu",
        "category": "Kategoria (np. Strategia, AI, Marketing)",
        "mermaid_diagram": "graph TD\\n A[Temat] --> B[Koncepcja 1]\\n B --> C[Krok 1]\\n ... (Stwórz dokładny kod Mermaid obrazujący całą logikę)",
        "concepts": [
          {"name": "Nazwa konceptu", "explanation": "Głębokie wyjaśnienie teorii z kursu"}
        ],
        "action_protocol": {
          "workflow": ["Krok 1: ...", "Krok 2: ...", "Krok 3: ... (dokładne i obszerne kroki do wykonania)"],
          "best_practices": ["Praktyka 1", "Praktyka 2"],
          "examples": ["Konkretny przykład z tekstu (np. prompt, scenariusz)"]
        }
      }
    ]
    Pamiętaj o escaped nowlines (\\n) w diagramie mermaid. Odpowiedz WYŁĄCZNIE czystym formatem JSON.
    """
    
    for filepath in files_to_process:
        print(f"[Deep Scan] {os.path.basename(filepath)}...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            content = content[:15000] # Ochrona limitu
            
            response = client.models.generate_content(
                model='gemini-2.5-pro', # Używamy PRO do skomplikowanej syntezy
                contents=[prompt + "\n\nTEKST:\n" + content]
            )
            
            json_text = extract_json(response.text)
            protocols = json.loads(json_text)
            
            for prot in protocols:
                prot['source_file'] = filepath
                all_protocols.append(prot)
                
            print(f"  -> Wyciągnięto {len(protocols)} Głębokich Protokołów.")
            time.sleep(5)
        except Exception as e:
            print(f"  [BŁĄD przy {os.path.basename(filepath)}] {e}")
            
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_protocols, f, ensure_ascii=False, indent=4)
        
    print(f"\n[SUKCES] Zapisano {len(all_protocols)} Protokołów w {output_file}")

if __name__ == "__main__":
    main()
