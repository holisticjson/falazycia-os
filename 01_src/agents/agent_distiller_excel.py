import pandas as pd
import os
import google.generativeai as genai
import time

# KONFIGURACJA
GEMINI_API_KEY = "AIzaSyBfcG1lyqbXh8jVbjONWLgwbt6vyQg4dGk"
KNOWLEDGE_BASE_DIR = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Syntetyczna"
SOURCE_FILES = [
    r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Maile Baza Wiedzy Mirek Burnejko.xlsx",
    r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Maile_Baza_Wiedzy_Marcin Skiba - ClientHustler.xlsx"

]

# Inicjalizacja Gemini 3.1 Flash Lite
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3.1-flash-lite')

def distill_content(subject, body, author):
    prompt = f"""
    Działaj jako Senior Knowledge Architect. Analizujesz newsletter od eksperta: {author}.
    TEMAT: {subject}
    TREŚĆ: {body}
    
    ZADANIE:
    1. Wyodrębnij konkretne strategie, frameworki, pomysły na automatyzację lub techniki marketingowe.
    2. Pomiń anegdoty i "sprzedażowy szum".
    3. Stwórz gęstą notatkę merytoryczną w formacie Markdown.
    4. Dodaj nagłówek: '# 💡 Wiedza Ekspercka ({author}): {subject}'.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Błąd Gemini: {e}")
        return None

def process_excel_files():
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)

    for file_path in SOURCE_FILES:
        if not os.path.exists(file_path):
            print(f"❌ Nie znaleziono pliku: {file_path}")
            continue

        print(f"🚀 Rozpoczynam przetwarzanie pliku: {os.path.basename(file_path)}")
        
        try:
            # Wczytywanie Excela
            df = pd.read_excel(file_path)
            
            # Próba automatycznego znalezienia kolumn (Temat, Treść)
            # Jeśli Twoje kolumny nazywają się inaczej, skoryguj je tutaj:
            cols = df.columns.tolist()
            subject_col = next((c for c in cols if 'temat' in c.lower() or 'subject' in c.lower()), cols[0])
            body_col = next((c for c in cols if 'treść' in c.lower() or 'body' in c.lower() or 'content' in c.lower()), cols[1])
            
            author = "Mirek Burnejko" if "Burnejko" in file_path else "Marcin Skiba"

            for index, row in df.iterrows():
                subject = str(row[subject_col])
                body = str(row[body_col])
                
                print(f"📝 Przetwarzam wiersz {index+1}/{len(df)}: {subject[:50]}...")
                
                distilled = distill_content(subject, body, author)
                
                if distilled:
                    safe_subject = "".join([c for c in subject if c.isalnum() or c==' ']).strip()
                    file_name = f"EKSPERT_{author.replace(' ', '_')}_{safe_subject[:40]}.md"
                    save_path = os.path.join(KNOWLEDGE_BASE_DIR, file_name)
                    
                    with open(save_path, "w", encoding="utf-8") as f:
                        f.write(distilled)
                    
                # Małe opóźnienie, żeby nie przeciążyć API (Free Tier)
                time.sleep(1) 

        except Exception as e:
            print(f"❌ Błąd podczas przetwarzania pliku {file_path}: {e}")

if __name__ == "__main__":
    process_excel_files()
