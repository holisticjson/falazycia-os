import glob
import re

for filepath in glob.glob("*.html"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Błąd czytania {filepath}: {e}")
        continue
    
    original = content
    
    # Zmiana adresów webhooków - łapiemy wszystkie warianty localhost:8501/api/lead
    content = re.sub(r'const webhookUrl\s*=\s*["\']http://localhost:8501/api/lead[^"\']*["\'];', 'const webhookUrl = "http://localhost:8000/api/lead";', content)

    # Wstaw tworzenie payloadu w skryptach formularzy
    if 'const data = Object.fromEntries(formData.entries());' in content and 'const payload =' not in content:
        payload_js = """const data = Object.fromEntries(formData.entries());
            
            // Zbudowanie payloadu zgodnie z wymaganiami backendu
            const payload = {
                "project": "broker",
                "name": data.Klient || data.Inwestor || data.Agent || data.Nazwisko || "Brak imienia",
                "contact": data.Kontakt || data.Telefon || data.Email || "Brak kontaktu",
                "budget": data.Budzet || "Opcjonalnie",
                "investment_type": data.Cel || data.Temat || data.Kategoria_Aktywa || data.Kategoria || "Opcjonalnie",
                "source": window.location.pathname.split('/').pop() || "Strona główna"
            };"""
        content = content.replace('const data = Object.fromEntries(formData.entries());', payload_js)
        
        # Zmiana co jest stringowane
        content = content.replace('JSON.stringify(data)', 'JSON.stringify(payload)')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Zaktualizowano formularze w: {filepath}")
