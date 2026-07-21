import os
import re

ROOT_DIR = "c:/Aplikacje MVP/02_knowledge_base/raw/Google Umiejętności Jutra 3.0"
TRANSCRIPTS_DIR = os.path.join(ROOT_DIR, "Transkrypcje")
WEEK5_DIR = os.path.join(ROOT_DIR, "Obsidian_Knowledge_Base", "Tydzień 5 - Transformacja i zarządzanie projektami Ai w organizacji")

mapping = {
    "Samoświadomość": "zadh9LUq3uQ",
    "Proaktywność - fotografia dnia pracy na wybranym przykładzie": "ZUNLTm8NktY",
    "Zarządzanie zmianą w praktyce – model ADKAR": "DL06B_6IuGU",
    "Planowanie wdrożenia AI – identyfikacja wyzwań i ryzyka": "rc2qf__-qp0",
    "Lider AI w akcji – komunikacja, prowadzenie i utrwalanie zmian": "VgOiv0InI4s"
}

def get_transcript(video_id):
    txt_path = os.path.join(TRANSCRIPTS_DIR, f"{video_id}.txt")
    if os.path.exists(txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def update_md(lesson_name, video_id):
    # Find the file in WEEK5_DIR
    for root, dirs, files in os.walk(WEEK5_DIR):
        for file in files:
            # removing special chars that might have been removed during creation
            safe_lesson = lesson_name.replace(":", "").replace("/", "-").replace("?", "")
            if file == f"{safe_lesson}.md":
                file_path = os.path.join(root, file)
                
                transcript = get_transcript(video_id)
                if transcript:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # replace the placeholder
                    new_content = re.sub(r'Transkrypcja niedostępna .*', transcript, content)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"✅ Zaktualizowano i wstrzyknięto: {file}")
                else:
                    print(f"❌ BRAK TRANSKRYPCJI dla: {file} (ID: {video_id})")

for lesson, vid in mapping.items():
    update_md(lesson, vid)

