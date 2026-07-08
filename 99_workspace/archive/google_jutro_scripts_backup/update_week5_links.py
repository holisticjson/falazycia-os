import os
import json
import re

user_input = """
AI w firmach i produktach digitalowych:
Powody wdrażania AI w firmach - https://www.youtube.com/watch?v=9X-VtNbMp_4
5 poziomów dojrzałości w firmie - https://www.youtube.com/watch?v=t8NTb5ZUUGM
Gdzie szukać okazji na AI w firmie? - https://www.youtube.com/watch?v=Ha-k2LcJ2xg
Architektura rozwiązań AI w produktach - https://www.youtube.com/watch?v=UG5EXIUJIew
Kiedy AI się opłaca - mierzenie sukcesu - https://www.youtube.com/watch?v=jYgjl_GRBqI

Zarządzanie projektami AI:
Wprowadzenie - https://www.youtube.com/watch?v=KGZHbgkg-HI
Cykl życia projektu AI: Zdefiniuj problem - https://www.youtube.com/watch?v=rByKtgGt23w
Cykl życia projektu AI: Znajdź dane - https://www.youtube.com/watch?v=5d4_fbHAeps
Cykl życia projektu AI: Spróbuj bez AI - https://www.youtube.com/watch?v=oiXLcORXdB0
Cykl życia projektu AI: Utwórz siatkę bezpieczeństwa - https://www.youtube.com/watch?v=TW10AvKWZUA
Cykl życia projektu AI: Wytrenuj model - https://www.youtube.com/watch?v=AKDnYSs2cGQ
Cykl życia projektu AI: Zdobądź feedback - https://www.youtube.com/watch?v=3EvCGTgpQEM
Cykl życia projektu AI: Monitoruj - https://www.youtube.com/watch?v=wsun-5yIqSw

AI Case Study: Jak zarządzać zmianą i zbudować w zespole nawyk pracy z AI?
Zarządzanie zmianą: Jak zbudować nawyk pracy z AI w zespole? - https://www.youtube.com/watch?v=M1pVvCk5K9c

Tworzenie wartości w firmie:
Skąd się bierze wartość - https://www.youtube.com/watch?v=y4SFoNUdLBo
Orientacja strategiczna - https://www.youtube.com/watch?v=zu0tHVSTGd0
Transformacja operacyjna - https://www.youtube.com/watch?v=urEYRzjK8gs

Wdrażanie zmian w perspektywie indywidualnej:
Samoświadomość - https://www.youtube.com/watch?v=zadh9LUq3uQ
Proaktywność - fotografia dnia pracy na wybranym przykładzie - https://www.youtube.com/watch?v=ZUNLTm8NktY

Wdrażanie AI w organizacji (Nieobowiązkowe):
Zarządzanie zmianą w praktyce – model ADKAR - https://www.youtube.com/watch?v=DL06B_6IuGU
Planowanie wdrożenia AI – identyfikacja wyzwań i ryzyka - https://www.youtube.com/watch?v=rc2qf__-qp0
Lider AI w akcji – komunikacja, prowadzenie i utrwalanie zmian - https://www.youtube.com/watch?v=VgOiv0InI4s
"""

base_dir = "C:/Aplikacje MVP/02_knowledge_base/raw/Google Umiejętności Jutra 3.0/Obsidian_Knowledge_Base/Tydzień 5 - Transformacja i zarządzanie projektami Ai w organizacji"

courses_dirs = {
    "AI w firmach i produktach digitalowych:": "AI w firmach i produktach digitalowych",
    "Zarządzanie projektami AI:": "Zarządzanie projektami AI",
    "AI Case Study: Jak zarządzać zmianą i zbudować w zespole nawyk pracy z AI?": "AI Case Study Jak zarządzać zmianą i zbudować w zespole nawyk pracy z AI",
    "Tworzenie wartości w firmie:": "Tworzenie wartości w firmie",
    "Wdrażanie zmian w perspektywie indywidualnej:": "Wdrażanie zmian w perspektywie indywidualnej",
    "Wdrażanie AI w organizacji (Nieobowiązkowe):": "Wdrażanie AI w organizacji (Nieobowiązkowe)"
}

links = []
current_course_dir = None
for line in user_input.split('\n'):
    line = line.strip()
    if not line or line.startswith('NOWE LEKCJE'): continue
    
    if line in courses_dirs:
        current_course_dir = courses_dirs[line]
    elif ' - https' in line:
        parts = line.split(' - https')
        title = parts[0].strip()
        url = 'https' + parts[1].strip()
        yt_id = url.split('v=')[-1]
        
        if not any(l['title'] == title for l in links):
            links.append({
                'title': title,
                'url': url,
                'yt_id': yt_id,
                'dir': current_course_dir or "AI w firmach i produktach digitalowych"
            })

updated_files = 0
created_files = 0
missing_files_data = []

for item in links:
    mod_dir = os.path.join(base_dir, item['dir'])
    os.makedirs(mod_dir, exist_ok=True)
    
    clean_title = item['title'].replace('–', '-').split('-')[-1].strip()
    clean_title = clean_title.split(':')[-1].strip().replace('?', '')
    
    found_file = None
    for f in os.listdir(mod_dir):
        if not f.endswith('.md'): continue
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

with open('missing_files_week5.json', 'w', encoding='utf-8') as f:
    json.dump(missing_files_data, f, ensure_ascii=False, indent=2)

print(f"Zaktualizowano {updated_files} plików, utworzono {created_files} nowych plików.")
print(f"Zapisano {len(missing_files_data)} linków do pobrania dla Tygodnia 5.")
