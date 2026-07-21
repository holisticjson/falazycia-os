import os
import re
import json
import shutil

ROOT_DIR = "c:/Aplikacje MVP/02_knowledge_base/raw/Google Umiejętności Jutra 3.0"
TRANSCRIPTS_DIR = os.path.join(ROOT_DIR, "Transkrypcje")
OBSIDIAN_DIR = os.path.join(ROOT_DIR, "Obsidian_Knowledge_Base")

WEEKS = {
    1: {"html": "mindmap_tydzien1.html", "folder": "Tydzień 1 - Fundamenty AI i produktywność osobista"},
    2: {"html": "mindmap_tydzien2.html", "folder": "Tydzień 2 - Tworzenie treści i rozwój biznesu z AI"},
    3: {"html": "mindmap_tydzien3.html", "folder": "Tydzień 3 - Automatyzacja pracy z asystentami i agentami AI"},
    4: {"md": "Tydzień 4 -Decyzje oparte na danych i planowanie wdrożeń AI/Opis i linki -Decyzje oparte na danych i planowanie wdrożeń AI.md", "folder": "Tydzień 4 -Decyzje oparte na danych i planowanie wdrożeń AI"},
    5: {"md": "Tydzień 5 - Transformacja i zarządzanie projektami Ai w organizacji/Opis i linki - Transformacja i zarządzanie projektami AI w organizacji.md", "folder": "Tydzień 5 - Transformacja i zarządzanie projektami Ai w organizacji"}
}

if not os.path.exists(OBSIDIAN_DIR):
    os.makedirs(OBSIDIAN_DIR)

pdf_links = []

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def get_transcript(video_id):
    txt_path = os.path.join(TRANSCRIPTS_DIR, f"{video_id}.txt")
    if os.path.exists(txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Transkrypcja niedostępna (wymaga ręcznego dodania z powodu weryfikacji CAPTCHA YouTube)."

# Parse Week 1-3 from HTML
for week in [1, 2, 3]:
    html_path = os.path.join(ROOT_DIR, WEEKS[week]["html"])
    if not os.path.exists(html_path):
        continue
        
    week_folder_obsidian = os.path.join(OBSIDIAN_DIR, WEEKS[week]["folder"])
    os.makedirs(week_folder_obsidian, exist_ok=True)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract modules block
    # Note: parsing JS from HTML with regex is brittle, but sufficient here
    modules_match = re.search(r'const modules = \[(.*?)\];', content, re.DOTALL)
    if not modules_match:
        continue
        
    modules_str = modules_match.group(1)
    
    # We will use regex to find each module title, description, lessons, and pdfs
    # This regex is an approximation
    module_blocks = re.findall(r"\{.*?title:'(.*?)'.*?desc:'(.*?)'.*?lessons:\[(.*?)\].*?pdfs:\[(.*?)\]", modules_str, re.DOTALL)
    
    for module_idx, (title, desc, lessons_str, pdfs_str) in enumerate(module_blocks, 1):
        mod_dir = os.path.join(week_folder_obsidian, f"Moduł {module_idx} - {sanitize_filename(title)}")
        os.makedirs(mod_dir, exist_ok=True)
        
        # Parse lessons
        lessons = re.findall(r"\{t:'(.*?)',\s*url:'(.*?)'\}", lessons_str)
        for les_idx, (les_t, les_url) in enumerate(lessons, 1):
            vid_id = ""
            if 'youtube.com/watch?v=' in les_url:
                vid_id = les_url.split('v=')[-1][:11]
                
            transcript = get_transcript(vid_id) if vid_id else "Brak wideo / transkrypcji."
            
            md_content = f"# {les_t}\n\n**Moduł:** {title}\n**Opis:** {desc}\n**URL:** {les_url}\n\n## Transkrypcja\n\n{transcript}\n"
            
            file_path = os.path.join(mod_dir, f"{les_idx}. {sanitize_filename(les_t)}.md")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
                
        # Parse PDFs
        # Usually pdfs are just strings: 'url' or {name, url}
        # In these files they seem to be strings: 'Name - url' or just plain text
        pdf_items = re.findall(r"'(.*?)'", pdfs_str)
        for p in pdf_items:
            pdf_links.append(f"Tydzień {week} | Moduł: {title} | PDF: {p}")

# Parse Week 4-5 from MD
for week in [4, 5]:
    md_rel = WEEKS[week]["md"]
    md_path = os.path.join(ROOT_DIR, md_rel)
    if not os.path.exists(md_path):
        continue
        
    week_folder_obsidian = os.path.join(OBSIDIAN_DIR, WEEKS[week]["folder"])
    os.makedirs(week_folder_obsidian, exist_ok=True)
    
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    current_course = "Ogólne"
    current_lesson = ""
    current_vid = ""
    current_mats = []
    
    # Simple state machine to parse markdown
    for line in lines:
        if line.startswith("# KURS"):
            current_course = line.replace("# KURS", "").replace(":", "").strip()
            os.makedirs(os.path.join(week_folder_obsidian, sanitize_filename(current_course)), exist_ok=True)
        elif line.startswith("## LEKCJA:"):
            # Save previous
            if current_lesson:
                mod_dir = os.path.join(week_folder_obsidian, sanitize_filename(current_course))
                transcript = get_transcript(current_vid) if current_vid else "Transkrypcja niedostępna."
                mats_str = "\n".join(current_mats)
                
                md_content = f"# {current_lesson}\n\n**Materiały Dodatkowe:**\n{mats_str}\n\n## Transkrypcja\n\n{transcript}\n"
                
                file_path = os.path.join(mod_dir, f"{sanitize_filename(current_lesson)}.md")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)
            
            current_lesson = line.replace("## LEKCJA:", "").strip()
            current_vid = ""
            current_mats = []
        elif "youtube.com/watch?v=" in line:
            match = re.search(r'v=([a-zA-Z0-9_-]{11})', line)
            if match:
                current_vid = match.group(1)
        elif "http" in line and "youtube" not in line and "szkolenia." not in line:
            # Catch potential PDF/Drive links
            match = re.search(r'\[(.*?)\]\((.*?)\)', line)
            if match:
                name, link = match.groups()
                current_mats.append(f"- [{name}]({link})")
                pdf_links.append(f"Tydzień {week} | Kurs: {current_course} | Lekcja: {current_lesson} | Plik: [{name}]({link})")
                
    # Save the last lesson
    if current_lesson:
        mod_dir = os.path.join(week_folder_obsidian, sanitize_filename(current_course))
        os.makedirs(mod_dir, exist_ok=True)
        transcript = get_transcript(current_vid) if current_vid else "Transkrypcja niedostępna."
        mats_str = "\n".join(current_mats)
        
        md_content = f"# {current_lesson}\n\n**Materiały Dodatkowe:**\n{mats_str}\n\n## Transkrypcja\n\n{transcript}\n"
        
        file_path = os.path.join(mod_dir, f"{sanitize_filename(current_lesson)}.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

# Generate PDF report
with open(os.path.join(ROOT_DIR, "Materiały_Dodatkowe_PDF.md"), "w", encoding='utf-8') as f:
    f.write("# Lista Materiałów Dodatkowych do Pobrania (PDF, Drive)\n\n")
    for link in pdf_links:
        f.write(f"- {link}\n")

print("Obsidian Knowledge Base generated successfully.")
print(f"Found {len(pdf_links)} external materials.")
