import glob
import sys
import re

if len(sys.argv) < 2:
    print("[BLAD] Podaj nowy adres URL backendu Cloud Run.")
    print("Przyklad: python update_endpoint.py https://broker-backend-xxxxxx.run.app")
    sys.exit(1)

new_url = sys.argv[1].strip()

# Automatycznie upewniamy sie, ze adres konczy sie na /api/lead
if not new_url.endswith("/api/lead"):
    if new_url.endswith("/"):
        new_url += "api/lead"
    else:
        new_url += "/api/lead"

print(f"Rozpoczynanie aktualizacji endpointow na: {new_url}")

count = 0
# Przeszukujemy wszystkie pliki HTML w tym folderze
for filepath in glob.glob("*.html"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Blad czytania {filepath}: {e}")
        continue
    
    original = content
    
    # Wyrazenie regularne wyszukuje przypisania zmiennej webhookUrl
    content = re.sub(
        r'const webhookUrl\s*=\s*["\']https?://[^"\']+/api/lead["\']\s*;', 
        f'const webhookUrl = "{new_url}";', 
        content
    )
    # Obsluga localhost:8000
    content = re.sub(
        r'const webhookUrl\s*=\s*["\']http://localhost:8000/api/lead["\']\s*;', 
        f'const webhookUrl = "{new_url}";', 
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Pomyslnie zaktualizowano: {filepath}")
        count += 1

print(f"\n[SUKCES] Zakonczono! Zaktualizowano endpoint w {count} plikach HTML.")
