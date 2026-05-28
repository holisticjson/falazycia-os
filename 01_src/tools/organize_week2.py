import os
import re
from pathlib import Path

def format_course_list():
    path = Path(r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Kursy_i_Szkolenia\Umiejętności_Jutra_3.0 - tydzień_2\TYDZIEŃ 2 — Pełna lista zasobów wideo i materiałów.md")
    if not path.exists():
        return
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add a bit more style to the table (bold titles, status icons)
    content = content.replace("| Lekcja |", "| 🎥 Lekcja (Tytuł i Czas) |")
    
    # Ensure specific directory structure for transcripts
    transcripts_dir = path.parent / "02_Transkrypcje"
    materials_dir = path.parent / "03_Materialy"
    transcripts_dir.mkdir(exist_ok=True)
    materials_dir.mkdir(exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"File formatted and directories created at: {path.parent}")

if __name__ == "__main__":
    format_course_list()
