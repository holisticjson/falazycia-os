import os
import json
import re

user_input = """
TYDZIEŃ 2 – Tworzenie treści i rozwój biznesu z AI

KURS 1: Pisanie skutecznych treści z pomocą AI

Wprowadzenie – trzy etapy pisania: https://www.youtube.com/watch?v=xlG3SRkIzRQ
Kwiat lotosu: https://www.youtube.com/watch?v=rSJ9rBpA7kc
Insight konsumencki i persona: https://www.youtube.com/watch?v=uw6NhiSjH1I
Pisanie, zero-shot, AIDA: https://www.youtube.com/watch?v=e5uf2ivI60k
DELTA Prompt i meta-promptowanie: https://www.youtube.com/watch?v=drPA56jNl6k
Twoja witryna internetowa i SPICE: https://www.youtube.com/watch?v=SCktuf0HDMk
PAS i Google Ads: https://www.youtube.com/watch?v=mjpeIdBwAv0
FAB i blank page – opisy produktów: https://www.youtube.com/watch?v=aCKTrG072Ts
FAB i macierz treści: https://www.youtube.com/watch?v=3F3U7SKOsyg
Storytelling, interaktywny prompt i strona „O nas": https://www.youtube.com/watch?v=htb_33GPKI8
Redakcja, archetypy, Gemy: https://www.youtube.com/watch?v=g7i6nY_QzqU
Rytualizacja marki: https://www.youtube.com/watch?v=SNhTV63IS8Y

KURS 2: Tworzenie treści wizualnych i audio z AI

Tworzenie grafik z AI: https://www.youtube.com/watch?v=WoeR_R9QQMQ
Generowanie wideo z AI: https://www.youtube.com/watch?v=S7UGV-MYmeE
Jak tworzyć treści audio w ElevenLabs: https://www.youtube.com/watch?v=kiqvXlj9qFQ

KURS 3: Od pomysłu do MVP: tworzenie produktów z AI

Miro jako narzędzie w procesie produktowym: https://www.youtube.com/watch?v=evD8Is2eDN8
Od informacji po prototypowanie: https://www.youtube.com/watch?v=7LHTAMdNk3s
Prototypowanie z AI – Lovable (od pomysłu do MVP we frameworku F.R.A.M.E.): https://www.youtube.com/watch?v=W1eYd2QCRiY

KURS 4: Przykłady zastosowań: AI w sprzedaży (Nieobowiązkowe)

Wprowadzenie – czym sprzedaż różni się od copywritingu: https://www.youtube.com/watch?v=3fXmk5_u-2M
Research klienta – Gemini przeszukuje internet: https://www.youtube.com/watch?v=Ku41fAbijmg
Kwalifikacja leada – BANT i MEDDIC: https://www.youtube.com/watch?v=Ohdhv8gtj9w
Pitch sprzedażowy – Value Proposition Canvas: https://www.youtube.com/watch?v=y199AcvY0r0
Rozmowa sprzedażowa – SPIN Selling + symulacja: https://www.youtube.com/watch?v=Du-Mu5WcoWA
Obiekcje – model LAER + NotebookLM: https://www.youtube.com/watch?v=73BGpWX3T28
Follow-up – sekwencje i timing (v2): https://www.youtube.com/watch?v=LoXYgdZbVlQ
Negocjacje – BATNA, ZOPA i anchoring: https://www.youtube.com/watch?v=-9Ufut-0s7A
Lejek sprzedaży i prognozowanie: https://www.youtube.com/watch?v=IPQQSaHEa_8
Social selling – prospecting na LinkedIn: https://www.youtube.com/watch?v=3e-dwvKpUo0

KURS 5: Przykłady zastosowań: AI w marketingu i analizie danych (Nieobowiązkowe)

Performance marketing z AI: https://www.youtube.com/watch?v=PpC03bN_7ME
Wstęp do optymalizacji treści pod SEO z wykorzystaniem AI: https://www.youtube.com/watch?v=CG2DSRXT1Wo
Sekcja FAQ wspierana AI: https://www.youtube.com/watch?v=UtOxANtChPU
Ulepszanie tytułów i opisów stron z AI: https://www.youtube.com/watch?v=vMXi-KFoLx4
Demokratyzacja analityki: https://www.youtube.com/watch?v=9vGJBQKDeCA
Zasady pracy z AI i danymi: https://www.youtube.com/watch?v=KX97x1JxZ6o
Pułapki analizy danych z AI: https://www.youtube.com/watch?v=gmGXfKfMHwQ
AI w pracy z Google Analytics 4: https://www.youtube.com/watch?v=lAriMS_8ZC4
AI w pracy z arkuszami kalkulacyjnymi: https://www.youtube.com/watch?v=Xzr8EbQ5TMs

KURS 6: Przykłady zastosowań: NotebookLM w obsłudze klienta (Nieobowiązkowe)

Wykorzystanie NotebookLM w obsłudze klienta: https://www.youtube.com/watch?v=kTP4pDaIqWg
"""

base_dir = "C:/Aplikacje MVP/02_knowledge_base/raw/Google Umiejętności Jutra 3.0/Obsidian_Knowledge_Base/Tydzień 2 - Tworzenie treści i rozwój biznesu z AI"

# Tworzenie struktury katalogów na podstawie Kursów
courses_dirs = {
    "KURS 1": "Moduł 1 - Pisanie skutecznych treści z pomocą AI",
    "KURS 2": "Moduł 2 - Tworzenie treści wizualnych i audio z AI",
    "KURS 3": "Moduł 3 - Od pomysłu do MVP – tworzenie produktów z AI",
    "KURS 4": "Moduł 4 - Przykłady zastosowań – AI w sprzedaży",
    "KURS 5": "Moduł 5 - Przykłady zastosowań – AI w marketingu i analizie danych",
    "KURS 6": "Moduł 6 - Przykłady zastosowań – NotebookLM w obsłudze klienta"
}

# Parse input
links = []
current_course_dir = None
for line in user_input.split('\n'):
    line = line.strip()
    if not line or line.startswith('NOWE LEKCJE'): continue
    
    if line.startswith('KURS'):
        course_prefix = line.split(':')[0].strip()
        if course_prefix in courses_dirs:
            current_course_dir = courses_dirs[course_prefix]
            
    elif ': https' in line:
        parts = line.split(': https')
        title = parts[0].strip()
        url = 'https' + parts[1].strip()
        yt_id = url.split('v=')[-1]
        
        # Ignoruj zduplikowane nazwy z sekcji "NOWE LEKCJE"
        if not any(l['title'] == title for l in links):
            links.append({
                'title': title,
                'url': url,
                'yt_id': yt_id,
                'dir': current_course_dir or courses_dirs['KURS 1']
            })

updated_files = 0
created_files = 0
missing_files_data = []

# Najpierw stwórz brakujące pliki i aktualizuj istniejące
for item in links:
    mod_dir = os.path.join(base_dir, item['dir'])
    os.makedirs(mod_dir, exist_ok=True)
    
    clean_title = item['title'].replace('–', '-').split('-')[-1].strip()
    if len(clean_title) < 5: clean_title = item['title']
    
    found_file = None
    for f in os.listdir(mod_dir):
        if not f.endswith('.md'): continue
        if clean_title.lower() in f.lower() or item['title'].lower() in f.lower() or clean_title[:10].lower() in f.lower():
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
        # Tworzenie nowego pliku dla lekcji
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

with open('missing_files_week2.json', 'w', encoding='utf-8') as f:
    json.dump(missing_files_data, f, ensure_ascii=False, indent=2)

print(f"Zaktualizowano {updated_files} plików, utworzono {created_files} nowych plików.")
print(f"Zapisano {len(missing_files_data)} linków do pobrania dla Tygodnia 2.")

# Aktualizacja mindmap_tydzien2.html
html_path = r"C:/Aplikacje MVP/02_knowledge_base/raw/Google Umiejętności Jutra 3.0/Tydzień 2 - Tworzenie treści i rozwój biznesu z AI/mindmap_tydzien2.html"
if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    updated_html = 0
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "url:'https://www.youtube.com" in line or 'url:"https://www.youtube.com' in line:
            for item in links:
                ct = item['title'].replace('–', '-').split('-')[-1].strip()
                if len(ct) < 5: ct = item['title']
                if ct.lower() in line.lower() or item['title'].lower() in line.lower():
                    lines[i] = re.sub(r"url:\s*['\"]https://www\.youtube\.com/watch\?v=[^'\"]+['\"]", f"url:'{item['url']}'", line)
                    updated_html += 1
                    break
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Zaktualizowano {updated_html} linków w pliku HTML.")
