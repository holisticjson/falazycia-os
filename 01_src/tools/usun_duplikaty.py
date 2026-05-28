import os
import hashlib
from collections import defaultdict

# Ścieżki do przeszukania
DIRECTORIES = [
    r"G:\Mój dysk\Kursy Szkolenia Marketing WWW A.I. APLIKACJE",
    r"G:\Mój dysk\Prompty AI_GPT'S"
]

def get_file_hash(filepath):
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as afile:
            buf = afile.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(65536)
        return hasher.hexdigest()
    except Exception:
        return None

def main():
    print("="*50)
    print("[SYSTEM] ROZPOCZYNAM BEZPIECZNE USUWANIE DUPLIKATOW...")
    print("="*50)
    
    hashes = defaultdict(list)
    
    print("Trwa ponowne skanowanie i parowanie plikow...")
    for directory in DIRECTORIES:
        if not os.path.exists(directory):
            continue
            
        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                
                # Ignorujemy bezpiecznie pliki systemowe (.ini) i linki Google Docs
                ext = os.path.splitext(file)[1].lower()
                if ext in ['.gdoc', '.gsheet', '.gslides', '.gform', '.ini']:
                    continue
                    
                file_hash = get_file_hash(filepath)
                if file_hash:
                    hashes[file_hash].append(filepath)

    duplicates_removed = 0
    bytes_freed = 0
    
    for h, paths in hashes.items():
        if len(paths) > 1:
            # Sortujemy sciezki, upewniajac sie, ze najkrotsza/najbardziej glowna sciezka zostaje jako oryginal
            paths.sort(key=len)
            original = paths[0]
            to_delete = paths[1:]
            
            for filepath in to_delete:
                try:
                    size = os.path.getsize(filepath)
                    os.remove(filepath)
                    duplicates_removed += 1
                    bytes_freed += size
                    print(f"[-] Usunieto: {os.path.basename(filepath)}")
                except Exception as e:
                    print(f"[BLAD] Nie udalo sie usunac {filepath}: {e}")
                    
    print("\n[SUKCES] CZYSZCZENIE ZAKONCZONE!")
    print(f"Usunieto plikow: {duplicates_removed}")
    print(f"Odzyskano miejsca: {bytes_freed / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
