import os
import json
import re

user_input = """
Kurs 1: Budowa judgmentu i strategiczne planowanie wdrożeń AI

Budowa judgmentu - System WIZJA: Budowa judgmentu i strategiczne planowanie wdrożeń AI: https://www.youtube.com/watch?v=QFnrCZ0EpvI

Kurs 2: Matryca Decyzyjna jako kompas we wdrożeniach AI

Wprowadzenie: Jak zmapować zadania gotowe na wdrożenie AI?: https://www.youtube.com/watch?v=-dmmUp2CX8s
Matryca Decyzyjna jako kompas we wdrożeniach AI - kiedy i co stosować?: https://www.youtube.com/watch?v=ev16wcNlBdY

Kurs 3: O myśleniu analitycznym w erze AI (Nieobowiązkowe)

O myśleniu analitycznym w erze AI: https://www.youtube.com/watch?v=hapAv4XJcGs

Kurs 4: Specjalizacja Analiza danych w erze AI (Nieobowiązkowe)

Historia Marketing Managera: https://www.youtube.com/watch?v=hrz18PgiFqE
Hurtownia danych - co to właściwie jest?: https://www.youtube.com/watch?v=ypIx9IqHxU4
Czy potrzebuję hurtowni danych?: https://www.youtube.com/watch?v=RiX9ofnnOoM
Jak stworzyć hurtownię danych?: https://www.youtube.com/watch?v=KGooRomfvjA
Na co zwrócić uwagę przy wyborze narzędzia do hurtowni danych: https://www.youtube.com/watch?v=e40G5Z3L1_A
Mam hurtownię danych - co dalej?: https://www.youtube.com/watch?v=BifZC3J0v-w
Czy potrzebuję SQL i Google BigQuery: https://www.youtube.com/watch?v=v_54mCdanoc
Przygotowanie środowiska: https://www.youtube.com/watch?v=9QzOxZ4C9wc
Pisanie zapytań SQL z AI: https://www.youtube.com/watch?v=uKlotiHaW_s
Gemini w Google BigQuery: https://www.youtube.com/watch?v=cbwKf_A656I
"""

base_dir = "C:/Aplikacje MVP/02_knowledge_base/raw/Google Umiejętności Jutra 3.0/Obsidian_Knowledge_Base/Tydzień 4 -Decyzje oparte na danych i planowanie wdrożeń AI"

courses_dirs = {
    "Kurs 1": "1 Budowa judgmentu i strategiczne planowanie wdrożeń AI",
    "Kurs 2": "2 Matryca Decyzyjna jako kompas we wdrożeniach AI Jak wybierać właściwe narzędzia do swojego zadania",
    "Kurs 3": "3 O myśleniu analitycznym w erze AI (Nieobowiązkowe)",
    "Kurs 4": "4 Specjalizacja Analiza danych w erze AI (Nieobowiązkowe)"
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
    clean_title = clean_title.split(':')[0].strip().replace('?', '')
    
    found_file = None
    for f in os.listdir(mod_dir):
        if not f.endswith('.md'): continue
        # Dopasowanie nazwy pliku
        if clean_title.lower() in f.lower() or item['title'].replace('?', '').lower() in f.lower() or clean_title[:15].lower() in f.lower():
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

with open('missing_files_week4.json', 'w', encoding='utf-8') as f:
    json.dump(missing_files_data, f, ensure_ascii=False, indent=2)

print(f"Zaktualizowano {updated_files} plików, utworzono {created_files} nowych plików.")
print(f"Zapisano {len(missing_files_data)} linków do pobrania dla Tygodnia 4.")
