import os
import shutil
import sys
from pathlib import Path

# Wymuszenie UTF-8 dla konsoli Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

RAW_DIR = Path(r"C:\Aplikacje MVP\02_knowledge_base\raw")
DEST_DIR = Path(r"C:\Aplikacje MVP\02_knowledge_base\technical_and_excluded")

SUPPORTED_EXTENSIONS = {'.pdf', '.md', '.docx', '.txt', '.html'}
CODE_EXTENSIONS = {'.py', '.js', '.sh', '.bats', '.json', '.yml', '.yaml', '.cjs', '.css', '.template'}

def main():
    print("=" * 80)
    print("SURGICAL CLEANUP: MOVING INCOMPATIBLE FILES OUT OF RAW BASE")
    print("=" * 80)
    print(f"Źródło: {RAW_DIR}")
    print(f"Cel (nowe miejsce): {DEST_DIR}")
    print("=" * 80)

    if not RAW_DIR.exists():
        print("[BŁĄD] Katalog źródłowy nie istnieje!")
        return

    moved_count = 0
    errors_count = 0

    for root, dirs, files in os.walk(RAW_DIR, topdown=False):
        for file in files:
            full_path = Path(root) / file
            rel_path = full_path.relative_to(RAW_DIR)
            ext = full_path.suffix.lower()
            size = full_path.stat().st_size

            # Warunki wykluczenia:
            # 1. Puste / malutkie pliki < 150B
            # 2. Skrypty i pliki kodu technicznego
            # 3. Nieobsługiwane formaty (PNG, MP4 itp.)
            is_tiny = size < 150
            is_code = ext in CODE_EXTENSIONS
            is_unsupported = ext not in SUPPORTED_EXTENSIONS

            if is_tiny or is_code or is_unsupported:
                dest_path = DEST_DIR / rel_path
                # Utwórz katalog docelowy jeśli nie istnieje
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    # Przenieś plik
                    shutil.move(str(full_path), str(dest_path))
                    moved_count += 1
                except Exception as e:
                    print(f"[BLAD] Nie udało się przenieść {rel_path}: {e}")
                    errors_count += 1

        # Usuń puste foldery w raw po przeniesieniu plików
        for d in dirs:
            dir_path = Path(root) / d
            try:
                if dir_path.exists() and not any(dir_path.iterdir()):
                    dir_path.rmdir()
            except Exception:
                pass

    print("-" * 80)
    print(f"📊 PODSUMOWANIE OCZYSZCZANIA:")
    print(f"  ✅ Pomyślnie przeniesiono: {moved_count} plików do {DEST_DIR}")
    print(f"  ❌ Błędy podczas przenoszenia: {errors_count}")
    
    # Liczymy pozostałe pliki w raw
    remaining_files = sum(len(files) for _, _, files in os.walk(RAW_DIR))
    print(f"  📦 Pozostałe czyste pliki w 'raw': {remaining_files}")
    print("=" * 80)

if __name__ == "__main__":
    main()
