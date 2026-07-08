import os
import glob
import json

base_dir = "Obsidian_Knowledge_Base"
weeks = [
    "Tydzień 1 - Fundamenty AI i produktywność osobista",
    "Tydzień 2 - Tworzenie treści i rozwój biznesu z AI",
    "Tydzień 3 - Automatyzacja pracy z asystentami i agentami AI",
    "Tydzień 4 -Decyzje oparte na danych i planowanie wdrożeń AI",
    "Tydzień 5 - Transformacja i zarządzanie projektami Ai w organizacji"
]

all_files_count = 0
missing_rag = []
has_rag_count = 0
no_transcript_count = 0

for week in weeks:
    week_path = os.path.join(base_dir, week)
    if not os.path.exists(week_path):
        print(f"Brak katalogu: {week_path}")
        continue
        
    files = glob.glob(os.path.join(week_path, "**/*.md"), recursive=True)
    for file_path in files:
        # Pomiń pliki, które są wprost PDF-ami (np. skończone na .pdf.md)
        if file_path.endswith(".pdf.md"):
            continue
            
        all_files_count += 1
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content_norm = content.replace("\r\n", "\n")
        
        if "## Zoptymalizowane Notatki (RAG)" in content_norm:
            has_rag_count += 1
        else:
            if "## Transkrypcja" in content_norm or "<details>" in content_norm:
                # Sprawdź czy ma transkrypcję
                parts = content_norm.split("## Transkrypcja")
                if len(parts) >= 2:
                    raw = parts[1].strip()
                    if "Transkrypcja niedostępna" in raw or not raw:
                        no_transcript_count += 1
                    else:
                        missing_rag.append(file_path)
                else:
                    no_transcript_count += 1
            else:
                no_transcript_count += 1

print(f"PODSUMOWANIE CAŁEJ BAZY WIEDZY RAG:")
print(f" - Łączna liczba analizowanych plików lekcji: {all_files_count}")
print(f" - Pliki z poprawnie wygenerowanymi notatkami RAG: {has_rag_count} ({has_rag_count / all_files_count * 100:.1f}%)")
print(f" - Pliki bez notatek RAG (do przetworzenia): {len(missing_rag)}")
print(f" - Pliki bez transkrypcji (pomocnicze / brak wideo): {no_transcript_count}")

if missing_rag:
    print("\nBRAKUJĄCE PLIKI:")
    for f in missing_rag:
         print(f"  * {f}")
else:
    print("\n[SUKCES] Wszystkie lekcje z transkrypcjami w tygodniach 1-5 mają już wygenerowane notatki RAG!")
