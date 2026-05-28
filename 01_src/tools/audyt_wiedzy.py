import os
import hashlib
from collections import defaultdict
from datetime import datetime

# Ścieżki do przeszukania na Twoim Dysku Google (zmapowanym na G:)
DIRECTORIES = [
    r"G:\Mój dysk\Kursy Szkolenia Marketing WWW A.I. APLIKACJE",
    r"G:\Mój dysk\Prompty AI_GPT'S"
]

OUTPUT_FILE = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Raport_Audytu_Wiedzy.md"

def get_file_hash(filepath):
    """Zwraca skrót MD5 pliku, co pozwala w 100% wykryć identyczne pliki niezależnie od ich nazwy"""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as afile:
            buf = afile.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(65536)
        return hasher.hexdigest()
    except Exception:
        # Pomiń pliki, do których nie mamy uprawnień z poziomu systemu (np. natywne Google Docs .gdoc)
        return None

def main():
    print("="*50)
    print("[SYSTEM] ROZPOCZYNAM AUDYT BAZY WIEDZY NA DYSKU G...")
    print("="*50)
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    total_size = 0
    file_count = 0
    extensions = defaultdict(int)
    hashes = defaultdict(list)
    
    for directory in DIRECTORIES:
        if not os.path.exists(directory):
            print(f"[BLAD] Nie znaleziono folderu: {directory}")
            continue
            
        print(f"[SKAN] Skanowanie folderu: {directory}")
        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                
                try:
                    size = os.path.getsize(filepath)
                except Exception:
                    continue
                    
                total_size += size
                file_count += 1
                
                ext = os.path.splitext(file)[1].lower()
                extensions[ext] += 1
                
                # Ignoruj pliki Google Docs (to są tylko linki na komputerze, a nie fizyczne pliki)
                if ext not in ['.gdoc', '.gsheet', '.gslides', '.gform']:
                    file_hash = get_file_hash(filepath)
                    if file_hash:
                        hashes[file_hash].append(filepath)

    # Szukamy grup, w których dany hash powtarza się więcej niż raz (czyli są to te same pliki)
    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    
    print("\n[INFO] Generowanie raportu końcowego...")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Raport z Audytu Bazy Wiedzy (Google Drive)\n\n")
        f.write(f"**Data wykonania:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("> [!NOTE]\n> Ten raport pokazuje fizyczny stan Twojej wiedzy. Pokazuje ile jest powtórzeń (balastu) i z jakich formatów korzystasz najczęściej.\n\n")
        
        f.write("## 1. Podsumowanie Statystyczne\n")
        f.write(f"- **Skanowane foldery:**\n")
        for d in DIRECTORIES:
            f.write(f"  - `{d}`\n")
        f.write(f"- **Przeskanowane pliki:** {file_count}\n")
        f.write(f"- **Całkowity rozmiar (fizyczny):** {total_size / (1024*1024):.2f} MB\n")
        f.write(f"- **Znalezionych grup duplikatów:** {len(duplicates)} \n\n")
        
        f.write("## 2. Typy Plików (Formaty Wiedzy)\n")
        f.write("Z jakich formatów składa się Twój system?\n\n")
        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
            ext_name = ext if ext else "Brak rozszerzenia"
            f.write(f"- **{ext_name}**: {count} plików\n")
            
        f.write("\n## 3. Dokładne Duplikaty (Do usunięcia/złączenia)\n")
        f.write("Poniższe pliki są fizycznie identyczne co do bajta (nawet jeśli mają inne nazwy). Tracisz na nie miejsce i czas.\n\n")
        if not duplicates:
            f.write("*Hurra! Nie znaleziono żadnych dokładnych duplikatów plików!*\n")
        else:
            for i, (h, paths) in enumerate(duplicates.items(), 1):
                f.write(f"\n### 🗑️ Duplikat #{i}\n")
                for p in paths:
                    f.write(f"- `{p}`\n")
                    
    print(f"\n[SUKCES] AUDYT ZAKONCZONY!")
    print(f"Raport zapisany w: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
