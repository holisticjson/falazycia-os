import os
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

# Zbuduj słownik z mapowaniami
mapping = {}
for line in user_input.strip().split('\n'):
    if not line.strip(): continue
    parts = line.split(': https')
    if len(parts) == 2:
        title = parts[0].strip()
        url = 'https' + parts[1].strip()
        mapping[title] = url

html_path = r"C:/Aplikacje MVP/02_knowledge_base/raw/Google Umiejętności Jutra 3.0/Tydzień 1 - Fundamenty AI i produktywność osobista/mindmap_tydzien1.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Prosta wymiana - szukamy kawałków, które pasują z grubsza do tytułów lekcji w HTML
updated_count = 0
lines = content.split('\n')
for i, line in enumerate(lines):
    if "url:'https://www.youtube.com" in line or 'url:"https://www.youtube.com' in line:
        for title, correct_url in mapping.items():
            # Szukamy czy jakikolwiek fragment tytułu z Cometa pasuje do tekstu {t:'...'}
            # Trzeba uważać na znaki specjalne i polskie litery, więc sprawdzamy proste zawieranie słów kluczowych
            clean_title = title.replace('–', '-').split('-')[-1].strip() # bierzemy końcówkę tytułu dla bezpieczeństwa
            if len(clean_title) < 5: 
                clean_title = title
                
            if clean_title.lower() in line.lower() or title.lower() in line.lower():
                # Zamieniamy stary URL na nowy
                lines[i] = re.sub(r"url:\s*['\"]https://www\.youtube\.com/watch\?v=[^'\"]+['\"]", f"url:'{correct_url}'", line)
                updated_count += 1
                break

content = '\n'.join(lines)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Zaktualizowano {updated_count} linków w pliku mindmap_tydzien1.html")
