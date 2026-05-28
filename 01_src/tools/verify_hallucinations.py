import os
import re
from pathlib import Path
from datetime import datetime

# Ścieżki do folderów z kursami do przeskanowania
DIRECTORIES = [
    r"C:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw\Adrian Kilar Motion",
    r"C:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw\Jan Szopa - Akademia Zdalnej Agencji Marketingowej"
]

OUTPUT_REPORT = r"C:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Raport_Audytu_Halucynacji.md"

# Typowe wzorce halucynacji, placeholderów i anomalii
PATTERNS = {
    "placeholder_brackets": (re.compile(r"\[[^\]]*?(?:wstaw|link|todo|tutaj|href|insert)[^\]]*?\]", re.IGNORECASE), "Nawias kwadratowy z placeholderem (np. [Wstaw link])"),
    "draft_urls": (re.compile(r"https?://(?:example\.com|localhost|127\.0.0\.1|temp|placeholder|twojadomena)", re.IGNORECASE), "Szkicowy / fałszywy adres URL"),
    "todo_markers": (re.compile(r"\b(?:TODO|FIXME|DOCS|X_LINK)\b", re.IGNORECASE), "Znacznik TODO lub FIXME"),
    "empty_sections": (re.compile(r"^#+\s+.*?$\n+(?:^\s*$\n*)+^#+", re.MULTILINE), "Potencjalnie pusta sekcja nagłówka"),
    "suspicious_llm_meta": (re.compile(r"(?:jako model językowy|jako asystent AI|oto transkrypcja, którą|wygenerowane przez Gemini)", re.IGNORECASE), "Metatekst asystenta LLM (częsta cecha halucynacji/braku filtracji)")
}

def analyze_file(filepath):
    issues = []
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return [{"line": 0, "content": f"Blad odczytu: {e}", "type": "Blad odczytu", "match": ""}]

    lines = content.splitlines()

    # Sprawdzenie wzorców linia po linii
    for line_idx, line in enumerate(lines, 1):
        for name, (pattern, desc) in PATTERNS.items():
            if name == "empty_sections":
                continue # Sprawdzimy to całościowo poniżej
            matches = pattern.findall(line)
            if matches:
                issues.append({
                    "line": line_idx,
                    "content": line.strip()[:100].replace("|", "\\|") + ("..." if len(line) > 100 else ""),
                    "type": desc,
                    "match": str(matches).replace("|", "\\|")
                })

    # Całościowe sprawdzenie pustych sekcji
    for match in PATTERNS["empty_sections"][0].finditer(content):
        char_idx = match.start()
        line_num = content[:char_idx].count('\n') + 1
        issues.append({
            "line": line_num,
            "content": "Naglowek bez tresci",
            "type": PATTERNS["empty_sections"][1],
            "match": "Pusta sekcja"
        })

    return issues

def main():
    print("="*60)
    print("[SYSTEM] ROZPOCZYNAM AUDYT PLIKOW POD KATEM HALUCYNACJI...")
    print("="*60)

    report_lines = []
    report_lines.append("# Raport z Audytu Halucynacji i Placeholderów (Kilar & Szopa)\n")
    report_lines.append(f"**Data wykonania audytu:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append("> [!NOTE]\n> Ten raport zawiera automatycznie wykryte błędy, placeholdery, fałszywe linki oraz metateksty AI z plików bazy wiedzy.\n\n")

    total_files = 0
    files_with_issues = 0
    total_issues = 0

    for dir_path in DIRECTORIES:
        path = Path(dir_path)
        if not path.exists():
            print(f"[OSTRZEZENIE] Katalog nie istnieje: {dir_path}")
            continue

        print(f"[SKAN] Folder: {path.name}")
        report_lines.append(f"## 📁 Katalog: `{path.name}`\n")

        # Skanowanie plików md recursively
        md_files = list(path.rglob("*.md"))
        if not md_files:
            report_lines.append("*Brak plików Markdown w tym katalogu.*\n\n")
            continue

        dir_has_issues = False

        for filepath in md_files:
            total_files += 1
            issues = analyze_file(filepath)

            if issues:
                files_with_issues += 1
                total_issues += len(issues)
                dir_has_issues = True
                
                relative_path = filepath.relative_to(path)
                report_lines.append(f"### 📄 [{filepath.name}](file:///{filepath.as_posix()})\n")
                report_lines.append(f"*Ścieżka:* `{relative_path}`\n\n")
                
                # Tabela problemów
                report_lines.append("| Linia | Typ Problemu | Fragment tekstu / Match |\n")
                report_lines.append("|---|---|---|\n")
                for iss in issues:
                    report_lines.append(f"| {iss['line']} | **{iss['type']}** | `{iss['content']}` (Match: `{iss['match']}`) |\n")
                report_lines.append("\n")

        if not dir_has_issues:
            report_lines.append("*Wszystkie pliki w tym katalogu są czyste i poprawne!*\n\n")

    # Podsumowanie na początku raportu
    summary_section = []
    summary_section.append("## 📊 Podsumowanie Statystyczne\n")
    summary_section.append(f"- **Przeskanowane pliki:** {total_files}\n")
    summary_section.append(f"- **Pliki z potencjalnymi błędami/halucynacjami:** {files_with_issues}\n")
    summary_section.append(f"- **Łączna liczba wykrytych anomalii:** {total_issues}\n\n")
    summary_section.append("---\n\n")

    # Połącz raport
    final_report = report_lines[0:3] + summary_section + report_lines[3:]

    # Zapisz plik raportu (UTF-8)
    os.makedirs(os.path.dirname(OUTPUT_REPORT), exist_ok=True)
    try:
        with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
            f.writelines(final_report)
        print("="*60)
        print(f"[SUKCES] Audyt zakonczony! Wykryto {total_issues} anomalii w {files_with_issues} plikach.")
        print(f"Raport wyjsciowy zostal zapisany w:\n{OUTPUT_REPORT}")
        print("="*60)
    except Exception as e:
        print(f"[BLAD] Nie mozna zapisac raportu: {e}")

if __name__ == "__main__":
    main()
