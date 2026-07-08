import os
import json
import re

user_input = """
Kurs 1: Wprowadzenie do agentów AI

Kiedy agenty AI mają sens?: https://www.youtube.com/watch?v=JkLWdRyPQd0
Bezpieczeństwo w pracy z AI: automatyzacje i agenty: https://www.youtube.com/watch?v=B553yDhYOio

Kurs 2: Automatyzacja jako umiejętność jutra na przykładzie Make.com

Wprowadzenie do automatyzacji bez programowania: https://www.youtube.com/watch?v=0a4Vn_tNStY
Scenariusz #1: Automatyczna obsługa formularzy kontaktowych: https://www.youtube.com/watch?v=hiMWqY8jbMQ
Scenariusz #2: Automatyczne wysyłanie zbiorczych maili: https://www.youtube.com/watch?v=EA3UIyII-f4
Scenariusz #3: Dodaj AI do swoich automatyzacji: https://www.youtube.com/watch?v=VH-2x47lPpU

Kurs 3: Budowa Agentów AI na przykładzie n8n (Nieobowiązkowe)

Wstęp o platformie n8n: https://www.youtube.com/watch?v=P7WMWDhhxtw
Case 1: Faktury: https://www.youtube.com/watch?v=Z9VZ94n36pE
Case 2: Tworzenie Agenta AI: https://www.youtube.com/watch?v=dBoCM82AcJM

Kurs 4: Budowa głosowego agenta AI w ElevenLabs (Nieobowiązkowe)

Budowa głosowego agenta AI w ElevenLabs: https://www.youtube.com/watch?v=hqoHp0w0Eow

Kurs 5: Automatyzacja w pracy w ekosystemie Google (Nieobowiązkowe)

Wprowadzenie: https://www.youtube.com/watch?v=5Dq6avM20KA
Gemini w Gmail - opanuj skrzynkę w Sidepanelu i Workspace Studio: https://www.youtube.com/watch?v=AaxVyw1kRAA
Meet i Calendar - automatyczne przygotowanie do spotkań: https://www.youtube.com/watch?v=GxyNN0XNUKM
Canvas w Google Sheets - analiza danych bez formuł: https://www.youtube.com/watch?v=QgbEpI7imss
Gemini Enterprise - część 1.: https://www.youtube.com/watch?v=7sY-4gX8gRk
Gemini Enterprise - część 2.: https://www.youtube.com/watch?v=YNp-4w9pF_I

Kurs 6: Praktyczne przykłady automatyzacji z AI - część 1. (Nieobowiązkowe)

AI w pracy Office Managera: budowa agenta głosowego: https://www.youtube.com/watch?v=tXgCR0n_C9k
AI w finansach: automatyzacja obiegu dokumentów: https://www.youtube.com/watch?v=ABloX6nnjp8
AI w marketingu: fabryka contentu: https://www.youtube.com/watch?v=LTtR0oQE214
AI w marketingu: asystent do analizy trendów i tworzenia treści: https://www.youtube.com/watch?v=UwVre8oYEfs

Kurs 7: Praktyczne przykłady automatyzacji z AI - część 2. (Nieobowiązkowe)

Automatyzacja generowania grafik z wykorzystaniem n8n i Vertex AI: https://www.youtube.com/watch?v=20lvFD1VQgY
"""

base_dir = "C:/Aplikacje MVP/02_knowledge_base/raw/Google Umiejętności Jutra 3.0/Obsidian_Knowledge_Base/Tydzień 3 - Automatyzacja pracy z asystentami i agentami AI"

courses_dirs = {
    "Kurs 1": "Moduł 1 - Wprowadzenie do agentów AI",
    "Kurs 2": "Moduł 2 - Automatyzacja jako umiejętność jutra na przykładzie Make.com",
    "Kurs 3": "Moduł 3 - Budowa Agentów AI na przykładzie n8n (Nieobowiązkowe)",
    "Kurs 4": "Moduł 5 - Budowa głosowego agenta AI w ElevenLabs (Nieobowiązkowe)",
    "Kurs 5": "Moduł 4 - Automatyzacja w pracy w ekosystemie Google (Nieobowiązkowe)",
    "Kurs 6": "Moduł 6 - Praktyczne przykłady automatyzacji z AI - część 1. (Nieobowiązkowe)",
    "Kurs 7": "Moduł 7 - Praktyczne przykłady automatyzacji z AI - część 2. (Nieobowiązkowe)"
}

links = []
current_course_dir = None
for line in user_input.split('\n'):
    line = line.strip()
    if not line or line.startswith('NOWE LEKCJE'): continue
    
    if line.startswith('Kurs'):
        course_prefix = line.split(':')[0].strip()
        if course_prefix in courses_dirs:
            current_course_dir = courses_dirs[course_prefix]
            
    elif ': https' in line:
        parts = line.split(': https')
        title = parts[0].strip()
        url = 'https' + parts[1].strip()
        yt_id = url.split('v=')[-1]
        
        if not any(l['title'] == title for l in links):
            links.append({
                'title': title,
                'url': url,
                'yt_id': yt_id,
                'dir': current_course_dir or courses_dirs['Kurs 1']
            })

updated_files = 0
created_files = 0
missing_files_data = []

for item in links:
    mod_dir = os.path.join(base_dir, item['dir'])
    os.makedirs(mod_dir, exist_ok=True)
    
    clean_title = item['title'].replace('–', '-').split('-')[-1].strip()
    clean_title = clean_title.split(':')[0].strip()
    
    found_file = None
    for f in os.listdir(mod_dir):
        if not f.endswith('.md'): continue
        # Elastyczne wyszukiwanie
        if clean_title.lower() in f.lower() or item['title'].lower() in f.lower() or clean_title[:15].lower() in f.lower():
            found_file = os.path.join(mod_dir, f)
            break
            
    if found_file:
        with open(found_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = re.sub(r'https://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]+', item['url'], content)
        content = re.sub(r'https://youtu\.be/[a-zA-Z0-9_-]+', item['url'], content)
        
        with open(found_file, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_files += 1
        
        missing_files_data.append({"file": found_file.replace('\\', '/'), "yt_id": item['yt_id']})
    else:
        safe_title = item['title'].replace(':', ' -').replace('/', '-').replace('"', '').replace('?', '')
        new_file_path = os.path.join(mod_dir, f"{safe_title}.md")
        
        content = f"# {item['title']}\n\n"
        content += f"**Moduł:** {item['dir']}\n"
        content += f"**URL:** {item['url']}\n\n"
        content += "## Transkrypcja\n\nTranskrypcja niedostępna (wymaga ręcznego dodania z powodu weryfikacji CAPTCHA YouTube).\n"
        
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        created_files += 1
        missing_files_data.append({"file": new_file_path.replace('\\', '/'), "yt_id": item['yt_id']})

with open('missing_files_week3.json', 'w', encoding='utf-8') as f:
    json.dump(missing_files_data, f, ensure_ascii=False, indent=2)

print(f"Zaktualizowano {updated_files} plików, utworzono {created_files} nowych plików.")
print(f"Zapisano {len(missing_files_data)} linków do pobrania dla Tygodnia 3.")

html_path = r"C:/Aplikacje MVP/02_knowledge_base/raw/Google Umiejętności Jutra 3.0/Tydzień 3 - Automatyzacja pracy z asystentami i agentami AI/mindmap_tydzien3.html"
if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    updated_html = 0
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "url:'https://www.youtube.com" in line or 'url:"https://www.youtube.com' in line:
            for item in links:
                ct = item['title'].replace('–', '-').split('-')[-1].strip().split(':')[0].strip()
                if ct.lower() in line.lower() or item['title'].lower() in line.lower():
                    lines[i] = re.sub(r"url:\s*['\"]https://www\.youtube\.com/watch\?v=[^'\"]+['\"]", f"url:'{item['url']}'", line)
                    updated_html += 1
                    break
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Zaktualizowano {updated_html} linków w pliku HTML mindmap_tydzien3.html.")
