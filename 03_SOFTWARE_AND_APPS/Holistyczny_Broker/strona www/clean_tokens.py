import os
import glob
import re

for filepath in glob.glob("*.html"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    # Remove chatbase script block
    # Szukamy całego tagu <script> zawierającego chatbase
    content = re.sub(r'<script>\s*\(function\(\)\{if\(!window\.chatbase.*?</script>', '', content, flags=re.DOTALL)
    
    # Replace Make.com webhook with localhost:8501/api/lead
    content = re.sub(r'https://hook\.eu1\.make\.com/[a-zA-Z0-9_]+', 'http://localhost:8501/api/lead', content)
    # Replace Airtable URL with localhost:8501 equivalents if any (should be caught by grep, but just in case)
    # the grep didn't find api.airtable.com or pat* anymore, which is great!
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned {filepath}")
