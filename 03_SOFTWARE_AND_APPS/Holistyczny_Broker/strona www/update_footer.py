import os
import glob
import re

# Odczytanie nowej stopki z pliku temp_footer.txt
with open("temp_footer.txt", "r", encoding="utf-8") as f:
    new_footer = f.read()

# Aktualizacja wszystkich plików HTML
for filepath in glob.glob("*.html"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the <footer> block
    # Używamy re.DOTALL aby kropka dopasowywała również znaki nowej linii
    content = re.sub(r'<footer.*?</footer>', new_footer, content, flags=re.DOTALL | re.IGNORECASE)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated footer in {filepath}")
