import os
import shutil
from pathlib import Path

def organize_files():
    base_dir = Path(r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy")
    
    # Kategoryzacja
    categories = {
        "Newsletters": ["NEWSLETTER_", "Maile"],
        "Mirek_Burnejko_AI_Biznes_Lab": ["Mirek Burnejko", "Mirek", "AI_Biznes_Lab"],
        "Alex Hormozi Wiedza": ["Hormozi", "100M"],
        "Marcin_Skiba_Wiedza": ["Marcin Skiba", "ClientHustler"],
        "Localo_Wiedza": ["Localo"],
        "Prompty & LLM": ["Prompt", "ChatGPT", "LLM", "Claude"],
        "Raporty_Rynkowe": ["Badanie Rynku", "Raport Strategiczny"],
        "Tworcy_Wiedza": ["Twórcy", "Influencerzy", "Instagram"],
        "Social_Media": ["Social Media", "Viral", "Hooki"],
        "Kursy_i_Szkolenia": ["Kurs", "Szkolenia", "MasterClass", "Wyzwanie", "Workbook"]
    }
    
    # Utworzenie folderów
    for folder in categories.keys():
        (base_dir / folder).mkdir(exist_ok=True)
        
    moved_count = 0
    # Skanowanie plików z głównego katalogu oraz podkatalogu 'Syntetyczna'
    for file_path in list(base_dir.glob("*.*")) + list((base_dir / "Syntetyczna").glob("*.*")):
        if file_path.is_dir():
            continue
            
        file_name = file_path.name
        moved = False
        
        for folder, keywords in categories.items():
            if any(kw.lower() in file_name.lower() for kw in keywords):
                # Nie przenieś, jeśli już tam jest
                dest_path = base_dir / folder / file_name
                if file_path != dest_path:
                    try:
                        shutil.move(str(file_path), str(dest_path))
                        moved_count += 1
                        moved = True
                    except Exception as e:
                        print(f"Błąd przenoszenia {file_name}: {e}")
                break
                
        # Jeżeli plik nie pasuje do żadnej kategorii, przenieś do "Inne"
        if not moved and file_path.parent == base_dir:
            other_dir = base_dir / "Inne"
            other_dir.mkdir(exist_ok=True)
            dest_path = other_dir / file_name
            try:
                shutil.move(str(file_path), str(dest_path))
                moved_count += 1
            except Exception as e:
                pass

    print(f"✅ Uporządkowano pomyślnie {moved_count} plików!")

if __name__ == "__main__":
    organize_files()
