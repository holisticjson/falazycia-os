import os
import re

def verify_week_2():
    schedule_path = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Kursy_i_Szkolenia\Umiejętności_Jutra_3.0 - tydzień_2\TYDZIEŃ 2 — Pełna lista zasobów wideo i materiałów.md"
    transcripts_dir = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Kursy_i_Szkolenia\Umiejętności_Jutra_3.0 - tydzień_2\02_Transkrypcje"
    
    with open(schedule_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Znajdź wszystkie lekcje w tabelach (format: | # | Lekcja | Link YT |)
    # Wyciągamy samą nazwę lekcji
    lessons = re.findall(r'\| \d+ \| (.*?) \| https://www\.youtube\.com/watch\?v=.*? \|', content)
    
    print(f"--- Weryfikacja Tygodnia 2 ({len(lessons)} lekcji wideo) ---")
    
    files_in_dir = os.listdir(transcripts_dir)
    missing = []
    found = []
    
    for lesson in lessons:
        # Czyścimy nazwę lekcji do porównania (usuwamy ewentualne znaki specjalne)
        clean_lesson = lesson.strip()
        
        # Szukamy pliku, który zawiera tę nazwę
        match = [f for f in files_in_dir if clean_lesson in f]
        
        if match:
            # Sprawdzamy czy plik nie jest pusty lub "placeholderym"
            file_path = os.path.join(transcripts_dir, match[0])
            size = os.path.getsize(file_path)
            if size < 3000: # Zakładamy, że pełna notatka musi mieć min. 3KB
                print(f"[!] {clean_lesson} -> Znaleziono, ale plik wydaje się MAŁY ({size} bajtów). Sprawdź: {match[0]}")
            else:
                found.append(clean_lesson)
        else:
            missing.append(clean_lesson)
            
    print(f"\n--- WYNIK ---")
    print(f"Znaleziono poprawnych: {len(found)}/{len(lessons)}")
    
    if missing:
        print(f"\nBRAKUJĄCE LEKCJE ({len(missing)}):")
        for m in missing:
            print(f" - {m}")
    else:
        print("\nWSZYSTKIE LEKCJE MAJĄ SWOJE NOTATKI! 🎉")

if __name__ == "__main__":
    verify_week_2()
