import os
import re
import datetime
import sys

# Skonfiguruj standardowe wyjście, aby poprawnie obsługiwało UTF-8 i emotikony w systemie Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Konfiguracja ścieżek
WORKSPACE_DIR = r"C:\Aplikacje MVP\Holistic Jason"
KB_DIR = os.path.join(WORKSPACE_DIR, "02_knowledge_base", "raw")
REPORT_PATH = os.path.join(WORKSPACE_DIR, "02_knowledge_base", "raw", "raport_audytu_halucynacji.md")

# Słownik reguł wykrywania anomalii
PATTERNS = {
    "placeholder": re.compile(r"\[(wstaw|insert|link|nazwa|nazwisko|url|email|telefon|twoje|tutaj|placeholder|custom|xxx|your[-_\s]name|example)\]", re.IGNORECASE),
    "fake_domain": re.compile(r"(https?://)?(www\.)?(example\.com|yourdomain\.com|xyz\.com|abc\.com|twojadomena\.pl|twojadomena\.com|twojadres\.pl|twojadres\.com)", re.IGNORECASE),
    "ai_admission": re.compile(r"(as\s+an\s+ai|jako\s+model\s+ai|nie\s+posiadam\s+dostępu|nie\s+mam\s+dostępu|przepraszam,\s+ale\s+nie|jako\s+sztuczna\s+inteligencja|as\s+a\s+large\s+language\s+model)", re.IGNORECASE),
    "todo": re.compile(r"\b(todo|do\s+zrobienia|uzupełnić|dokończyć)\b", re.IGNORECASE),
    "markdown_anomaly": re.compile(r"^(#+)\s*$", re.MULTILINE),  # puste nagłówki
}

def analyze_markdown_file(filepath):
    warnings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        lines = content.splitlines()
        for idx, line in enumerate(lines, 1):
            line_stripped = line.strip()
            if not line_stripped:
                continue
                
            # Sprawdź reguły regex
            for category, regex in PATTERNS.items():
                match = regex.search(line_stripped)
                if match:
                    snippet = line_stripped[:120] + "..." if len(line_stripped) > 120 else line_stripped
                    warnings.append({
                        "line": idx,
                        "category": category,
                        "match": match.group(0),
                        "snippet": snippet
                    })
        
        # Sprawdź parzystość bloków kodu
        unclosed_code_blocks = content.count("```") % 2 != 0
        if unclosed_code_blocks:
            warnings.append({
                "line": "Ogólne",
                "category": "broken_markdown",
                "match": "Niedomknięty blok kodu (```)",
                "snippet": "Liczba znaczników potrójnego grawisu (```) w pliku jest nieparzysta."
            })
            
    except Exception as e:
        warnings.append({
            "line": 0,
            "category": "error",
            "match": str(e),
            "snippet": "Błąd podczas próby odczytu pliku."
        })
    return warnings

def run_audit():
    print(f"🤖 Rozpoczynam audyt halucynacji w bazie wiedzy: {KB_DIR}")
    report_data = []
    
    # Foldery do przeskanowania
    target_dirs = [
        "Adrian Kilar Motion",
        "Jan Szopa - Akademia Zdalnej Agencji Marketingowej"
    ]
    
    total_files_scanned = 0
    total_warnings_found = 0
    
    for folder in target_dirs:
        folder_path = os.path.join(KB_DIR, folder)
        if not os.path.exists(folder_path):
            print(f"⚠️ Folder {folder} nie istnieje w bazie raw. Pomijam.")
            continue
            
        print(f"📁 Skanowanie folderu: {folder}...")
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.md'):
                    total_files_scanned += 1
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, KB_DIR)
                    warnings = analyze_markdown_file(full_path)
                    
                    if warnings:
                        total_warnings_found += len(warnings)
                        report_data.append({
                            "file": rel_path,
                            "warnings": warnings
                        })
                        
    # Zapisz raport Markdown
    write_markdown_report(report_data, total_files_scanned, total_warnings_found)
    print(f"✅ Audyt zakończony! Wynik zapisano w: {REPORT_PATH}")
    print(f"📈 Przeskanowano plików: {total_files_scanned}, wykryto anomalii: {total_warnings_found}")

def write_markdown_report(data, scanned, warnings_count):
    md = []
    md.append("# Raport z Audytu Halucynacji i Poprawności Wiedzy")
    md.append(f"Automatyczny audyt plików w bazie wiedzy pod kątem halucynacji modelowych, placeholderów i anomalii.\n")
    md.append(f"## 📊 Podsumowanie Statystyk")
    md.append(f"- **Data Audytu:** `{datetime.datetime.now().isoformat()}`")
    md.append(f"- **Przeskanowanych plików .md:** `{scanned}`")
    md.append(f"- **Wykrytych potencjalnych anomalii:** `{warnings_count}`")
    md.append(f"- **Status:** " + ("⚠️ Wymaga wdrożenia poprawek" if warnings_count > 0 else "✅ Pliki czyste i zweryfikowane") + "\n")
    md.append("---\n")
    
    if warnings_count == 0:
        md.append("### 🎉 Brak uwag!\nWszystkie analizowane pliki szkoleniowe Adriana Kilara i Jana Szopy są wolne od placeholderów, deweloperskich notatek AI i fałszywych domen.")
    else:
        md.append("## 🔍 Szczegółowe Wyniki (Wykryte Anomalie)\n")
        md.append("Poniższa lista zawiera pliki, w których wykryto podejrzane linie tekstu. Zweryfikuj je i popraw przed udostępnieniem dla Agenta AI.\n")
        
        for item in data:
            # Tworzenie linku absolutnego kompatybilnego z systemem użytkownika
            absolute_file_url = f"file:///{os.path.join(KB_DIR, item['file']).replace(chr(92), '/')}"
            md.append(f"### 📄 [Link do pliku: {os.path.basename(item['file'])}]({absolute_file_url})")
            md.append(f"**Ścieżka relatywna:** `{item['file']}`")
            md.append("\n| Linia | Kategoria anomalii | Wykryty wzorzec | Fragment tekstu / Podgląd |")
            md.append("| :---: | :--- | :---: | :--- |")
            
            for w in item['warnings']:
                cat_desc = {
                    "placeholder": "🔴 Placeholder deweloperski",
                    "fake_domain": "🟡 Podejrzana / testowa domena",
                    "ai_admission": "🟠 Zwrot przyznania się AI do ograniczeń",
                    "todo": "🔵 Nierozwiązane TODO",
                    "broken_markdown": "⚠️ Uszkodzona struktura Markdown",
                    "error": "❌ Błąd systemu"
                }.get(w['category'], w['category'])
                
                # Zabezpieczenie przed łamaniem tabel markdown przez znak |
                clean_snippet = w['snippet'].replace('|', '\\|')
                clean_match = w['match'].replace('|', '\\|')
                md.append(f"| {w['line']} | {cat_desc} | `{clean_match}` | {clean_snippet} |")
            md.append("\n---\n")
            
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(md))

if __name__ == "__main__":
    run_audit()
