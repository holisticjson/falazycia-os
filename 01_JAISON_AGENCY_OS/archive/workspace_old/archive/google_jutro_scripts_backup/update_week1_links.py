import os
import json
import re

user_input = """
Czym jest Generatywna AI: https://www.youtube.com/watch?v=KY1YATk4aVc
Funkcje generowania obrazów i wideo: https://www.youtube.com/watch?v=lL4zDqUD-BA
Canvas – Generowanie prezentacji z AI: https://www.youtube.com/watch?v=ghHZmocUj4o
Canvas – Prototypowanie prostych stron i aplikacji: https://www.youtube.com/watch?v=vloy3XXr7yQ
Jak uczyć się szybciej z AI: https://www.youtube.com/watch?v=h0bOiIhUrkw
Multimodalność, RAG i świadomy dobór modeli do zadania: https://www.youtube.com/watch?v=P7mIjg_eObw
Strategie skutecznego promptowania i tworzenie kontekstu: https://www.youtube.com/watch?v=Ji66VrVcCH8
Wprowadzenie – kiedy i do czego używać NotebookLM: https://www.youtube.com/watch?v=6N27F10rHDA
Tworzenie notatników i praca z własną bazą wiedzy: https://www.youtube.com/watch?v=YixHfSAo-jI
Organizacja danych i zarządzanie wiedzą: https://www.youtube.com/watch?v=EzQR-uIYSsI
Generowanie podcastów i podsumowań wideo: https://www.youtube.com/watch?v=qlvRxNX0q4A
Przegląd biznesowych pomysłów na wdrożenie NotebookLM: https://www.youtube.com/watch?v=3T1Bkd5qnxI
Tworzenie pierwszych asystentów AI: https://www.youtube.com/watch?v=hrKQTa3GhfM
Osobista rada nadzorcza – wsparcie strategicznych decyzji: https://www.youtube.com/watch?v=6IbjLD0L8O8
Pierwsze okazje na oszczędność czasu dzięki AI: https://www.youtube.com/watch?v=w9LXo85aq1c
Łączenie narzędzi AI w pracy: https://www.youtube.com/watch?v=SXcjSuQ1ewk
Gemini w aplikacjach Google Workspace: https://www.youtube.com/watch?v=7mu7c0DV3Dw
Wykorzystanie AI do głębokiej analizy: https://www.youtube.com/watch?v=4jUEHCkQH9I
Analiza biznesowa i wizualizacja danych z AI: https://www.youtube.com/watch?v=nJDTtMXWHX0
Wprowadzenie do Bielik AI: https://www.youtube.com/watch?v=dZMHJNZ8-5k
Najczęstsze pytania dotyczące bezpieczeństwa użytkowników: https://www.youtube.com/watch?v=D0jOM9nzAgA
Prawne aspekty pracy z AI: https://www.youtube.com/watch?v=ISNvI3KD0gk
Co poza chatbotami: https://www.youtube.com/watch?v=N19Vl1yn9RA
"""

base_dir = "C:/Aplikacje MVP/02_knowledge_base/raw/Google Umiejętności Jutra 3.0/Obsidian_Knowledge_Base/Tydzień 1 - Fundamenty AI i produktywność osobista"

mapping = {}
for line in user_input.strip().split('\n'):
    if not line.strip(): continue
    parts = line.split(': https')
    if len(parts) == 2:
        title = parts[0].strip()
        url = 'https' + parts[1].strip()
        yt_id = url.split('v=')[-1]
        mapping[title] = yt_id

updated_files = []
missing_files_data = []

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if not f.endswith('.md'): continue
        
        # Clean title by removing "X. " prefix and ".md" suffix
        clean_name = re.sub(r'^\d+\.\s*', '', f).replace('.md', '').strip()
        
        file_path = os.path.join(root, f)
        
        for k, yt_id in mapping.items():
            if k == clean_name or k in clean_name or clean_name in k:
                # We found the match! Update the file's YouTube link
                with open(file_path, 'r', encoding='utf-8') as md_file:
                    content = md_file.read()
                
                # Replace any old youtube links with the new one
                new_url = f"https://www.youtube.com/watch?v={yt_id}"
                
                # Replace the iframe or markdown link
                # Find the line with youtube.com and replace the ID
                content = re.sub(r'https://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]+', new_url, content)
                content = re.sub(r'https://youtu\.be/[a-zA-Z0-9_-]+', new_url, content)
                
                with open(file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(content)
                
                updated_files.append(f)
                
                missing_files_data.append({
                    "file": file_path.replace('\\', '/'),
                    "yt_id": yt_id
                })
                break

with open('missing_files_week1.json', 'w', encoding='utf-8') as f:
    json.dump(missing_files_data, f, ensure_ascii=False, indent=2)

print(f"Zaktualizowano plików: {len(updated_files)}")
print(f"Stworzono missing_files_week1.json z {len(missing_files_data)} pozycjami do pobrania.")
