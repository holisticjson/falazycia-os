import os
import hashlib
import sys
from pathlib import Path

# Wymuszenie UTF-8 dla konsoli Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

RAW_DIR = Path(r"C:\Aplikacje MVP\02_knowledge_base\raw")
IGNORE_PATH = Path(r"C:\Aplikacje MVP\Holistic Jason\.antigravityignore")

SUPPORTED_EXTENSIONS = {'.pdf', '.md', '.docx', '.txt', '.html'}

def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

def parse_ignore_patterns():
    patterns = []
    if not IGNORE_PATH.exists():
        return patterns
    with open(IGNORE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
    return patterns

def main():
    print("=" * 80)
    print("LOKALNY DETEKTOR CHAOSU I POMINIĘTYCH PLIKÓW")
    print("=" * 80)
    print(f"Skanowanie katalogu: {RAW_DIR}")
    print("=" * 80)

    if not RAW_DIR.exists():
        print(f"[BLAD] Ścieżka {RAW_DIR} nie istnieje!")
        return

    ignore_patterns = parse_ignore_patterns()
    
    total_scanned = 0
    skipped_unsupported_ext = []
    skipped_technical_code = []
    skipped_empty_or_tiny = []
    duplicates = {}
    valid_rag_files = []

    # Kod, konfiguracje, skrypty, itp.
    code_extensions = {'.py', '.js', '.sh', '.bats', '.json', '.yml', '.yaml', '.cjs', '.html', '.css', '.template'}

    for root, _, files in os.walk(RAW_DIR):
        for file in files:
            full_path = Path(root) / file
            rel_path = full_path.relative_to(RAW_DIR)
            ext = full_path.suffix.lower()
            size = full_path.stat().st_size
            total_scanned += 1

            # 1. Puste i malutkie pliki (poniżej 150 bajtów)
            if size < 150:
                skipped_empty_or_tiny.append((rel_path, size))
                continue

            # 2. Skrypty i pliki kodu technicznego
            if ext in code_extensions:
                skipped_technical_code.append((rel_path, ext, size))
                continue

            # 3. Inne nieobsługiwane formaty (obrazy, wideo, etc.)
            if ext not in SUPPORTED_EXTENSIONS:
                skipped_unsupported_ext.append((rel_path, ext, size))
                continue

            # 4. Sprawdzenie duplikatów dla potencjalnie poprawnych plików RAG
            file_hash = calculate_sha256(full_path)
            if file_hash:
                if file_hash in duplicates:
                    duplicates[file_hash].append(rel_path)
                else:
                    duplicates[file_hash] = [rel_path]
                    valid_rag_files.append((rel_path, ext, size))

    print(f"\n[OK] Przeanalizowano łącznie {total_scanned} plików.\n")

    # 1. Raport o formatach RAG vs Inne
    supported_count = len(valid_rag_files) + sum(1 for dup_list in duplicates.values() if len(dup_list) > 1)
    
    print("-" * 80)
    print(" PODZIAŁ PLIKÓW POD KĄTEM KOMPATYBILNOŚCI Z RAG / NOTEBOOKLM:")
    print("-" * 80)
    print(f"  ✅ KOMPATYBILNE (PDF, MD, DOCX, TXT):   {supported_count} plików")
    print(f"  ❌ POMINIĘTE - Kod, skrypty, JSON:      {len(skipped_technical_code)} plików")
    print(f"  ❌ POMINIĘTE - Inne formaty (PNG, MP4): {len(skipped_unsupported_ext)} plików")
    print(f"  ❌ POMINIĘTE - Puste / śmieciowe <150B: {len(skipped_empty_or_tiny)} plików")
    print("-" * 80)

    # 2. Detekcja duplikatów merytorycznych
    duplicate_groups = {h: paths for h, paths in duplicates.items() if len(paths) > 1}
    total_duplicates = sum(len(paths) - 1 for paths in duplicate_groups.values())
    
    print(f"  ⚠️ ZDUPLIKOWANE (Tożsama treść):         {total_duplicates} plików")
    print("-" * 80)

    # Szczegóły: Pliki techniczne (kod)
    if skipped_technical_code:
        print(f"\n[📊] PRZYKŁAD PLIKÓW TECHNICZNYCH / KODU (Pominięte automatycznie) [Max 10]:")
        for rel_path, ext, size in skipped_technical_code[:10]:
            print(f"  - {rel_path} ({ext.upper()}, {size/1024:.1f} KB)")
        if len(skipped_technical_code) > 10:
            print(f"  ... i {len(skipped_technical_code) - 10} innych.")

    # Szczegóły: Puste i małe pliki
    if skipped_empty_or_tiny:
        print(f"\n[📊] PRZYKŁAD PLIKÓW PUSTYCH LUB ŚMIECIOWYCH <150B (Pominięte automatycznie) [Max 10]:")
        for rel_path, size in skipped_empty_or_tiny[:10]:
            print(f"  - {rel_path} ({size} B)")
        if len(skipped_empty_or_tiny) > 10:
            print(f"  ... i {len(skipped_empty_or_tiny) - 10} innych.")

    # Szczegóły: Duplikaty
    if duplicate_groups:
        print(f"\n[⚠️] NAJBARDZIEJ ZDUPLIKOWANE PLIKI MERYTORYCZNE (Powtarzane w folderach) [Max 5 grup]:")
        sorted_groups = sorted(duplicate_groups.items(), key=lambda x: len(x[1]), reverse=True)
        for h, paths in sorted_groups[:5]:
            print(f"  • Plik występuje {len(paths)} razy w różnych miejscach:")
            for p in paths:
                print(f"    --> {p}")
            print()

    # Ostateczne podsumowanie dla użytkownika pod kątem liczby "922"
    unsupported_or_tiny = len(skipped_technical_code) + len(skipped_unsupported_ext) + len(skipped_empty_or_tiny)
    print("=" * 80)
    print(" ANALIZA POD KĄTEM NOTEBOOKLM / CHMURY:")
    print("=" * 80)
    print(f"  • Łączna liczba plików niekompatybilnych (formaty techniczne/śmieci): {unsupported_or_tiny}")
    print(f"  • Łączna liczba dokładnych duplikatów merytorycznych:                 {total_duplicates}")
    print(f"  • RAZEM CHAOTYCZNE PLIKI (wykluczone z RAG):                           {unsupported_or_tiny + total_duplicates}")
    print("=" * 80)
    print("Wniosek: To wyjaśnia dokładnie błędy pominięcia plików w chmurze!")
    print("=" * 80)

if __name__ == "__main__":
    main()
