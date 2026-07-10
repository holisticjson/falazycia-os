import os

ROOT_DIR = "c:/Aplikacje MVP/02_knowledge_base/raw/Google Umiejętności Jutra 3.0"
WEEK5_DIR = os.path.join(ROOT_DIR, "Obsidian_Knowledge_Base", "Tydzień 5 - Transformacja i zarządzanie projektami Ai w organizacji")

courses = {
    "Wdrażanie zmian w perspektywie indywidualnej": [
        "Samoświadomość",
        "Proaktywność - fotografia dnia pracy na wybranym przykładzie"
    ],
    "Wdrażanie AI w organizacji (Nieobowiązkowe)": [
        "Zarządzanie zmianą w praktyce – model ADKAR",
        "Planowanie wdrożenia AI – identyfikacja wyzwań i ryzyka",
        "Lider AI w akcji – komunikacja, prowadzenie i utrwalanie zmian"
    ]
}

for course_name, lessons in courses.items():
    course_path = os.path.join(WEEK5_DIR, course_name.replace(":", ""))
    os.makedirs(course_path, exist_ok=True)
    
    for lesson in lessons:
        safe_lesson = lesson.replace(":", "").replace("/", "-").replace("?", "")
        file_path = os.path.join(course_path, f"{safe_lesson}.md")
        
        md_content = f"# {lesson}\n\n**Materiały Dodatkowe:**\nBrak\n\n## Transkrypcja\n\nTranskrypcja niedostępna (wymaga zaktualizowania pliku źródłowego MD i dodania poprawnego linku YouTube, aby skrypt powiązał go z plikiem z 3 czerwca).\n"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"Utworzono: {course_name} / {lesson}.md")
