import os
import sys
import json
import time
import requests
from bs4 import BeautifulSoup

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "https://piotrlotniczy.elms.pl"
TRAINING_URL = f"{BASE_URL}/next/public/training/2"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "FLIGHT_HACKING_MASTER.md")

def extract_course_data(session_cookie=None):
    print("=" * 60)
    print("✈️ EKSTRAKTOR KURSU PIOTRA LOTNICZEGO DO BAZY WIEDZY RAG")
    print("=" * 60)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    cookies = {}
    if session_cookie:
        cookies["PHPSESSID"] = session_cookie
        
    session = requests.Session()
    session.headers.update(headers)
    if cookies:
        session.cookies.update(cookies)
        
    print(f" Pobieranie strony szkolenia: {TRAINING_URL}...")
    res = session.get(TRAINING_URL)
    
    if "Logowanie" in res.text or "header-btn-login" in res.text:
        print("\n [UWAGA] Wymagane zalogowanie na platformie eLMS!")
        print("Aby pobrać niepubliczną treść lekcji:")
        print("1. Zaloguj się w przeglądarce na https://piotrlotniczy.elms.pl/next/public/login")
        print("2. Otwórz narzędzia deweloperskie (F12 -> Application -> Cookies)")
        print("3. Skopiuj wartość ciasteczka 'PHPSESSID' i uruchom skrypt:")
        print("   python extract_elms_course.py <twoje_ciasteczko_PHPSESSID>\n")
        
    soup = BeautifulSoup(res.text, "html.parser")
    
    modules_data = []
    
    # Skanowanie struktury lekcji / modułów
    modules = soup.find_all(["div", "section", "li"], class_=lambda c: c and ("module" in c or "training" in c or "lesson" in c))
    
    print(f" Znaleziono elementów struktury: {len(modules)}")
    
    # Dodatkowe parsowanie linków do lekcji
    links = soup.find_all("a", href=True)
    lesson_links = [l["href"] for l in links if "/next/public/lesson/" in l["href"] or "/next/public/training/" in l["href"]]
    lesson_links = list(set(lesson_links))
    
    print(f"🔗 Znaleziono unikalnych odnośników do lekcji: {len(lesson_links)}")
    
    content_md = f"""# ✈️ EKSPERT LOKALIZATOR & KURS LOTÓW W KLASIE BIZNES ZA PUNKTY | AKADEMIA FALA ŻYCIA

> Podręcznik Bazy Wiedzy RAG dla Agenta AI **Biznes Klasa Advisor** oraz modułu Akademii Wiedzy na portalu `fala-zycia.pl`.
> Wyekstrahowano automatycznie z platformy: `{TRAINING_URL}`
> Data pobrania: {time.strftime('%Y-%m-%d %H:%M:%S')}

---

## 📚 1. STRUKTURA I MODUŁY KURSU PIOTRA LOTNICZEGO

"""

    if lesson_links:
        for idx, link in enumerate(lesson_links, 1):
            full_link = BASE_URL + link if link.startswith("/") else link
            print(f" Skanowanie lekcji {idx}/{len(lesson_links)}: {full_link}")
            try:
                l_res = session.get(full_link)
                l_soup = BeautifulSoup(l_res.text, "html.parser")
                title = l_soup.find("h1") or l_soup.find("h2") or "Lekcja " + str(idx)
                title_text = title.get_text(strip=True) if hasattr(title, "get_text") else str(title)
                
                # Tekst opisowy lekcji
                desc = l_soup.find(["div", "article"], class_=lambda c: c and ("description" in c or "content" in c or "lesson" in c))
                desc_text = desc.get_text(separator="\n", strip=True) if desc else "Brak opisu tekstowego (materiał wideo/PDF)."
                
                content_md += f"### 🎬 Lekcja {idx}: {title_text}\n"
                content_md += f"**URL:** [{full_link}]({full_link})\n\n"
                content_md += f"{desc_text}\n\n---\n\n"
            except Exception as e:
                print(f"⚠️ Błąd przy pobieraniu {full_link}: {e}")
    else:
        content_md += "_(Struktura modułów oczekuje na sesję użytkownika PHPSESSID)_\n"

    # Zapis do pliku
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content_md)
        
    print(f"\n Zapisano zaktualizowany plik bazy wiedzy: {OUTPUT_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    cookie = sys.argv[1] if len(sys.argv) > 1 else None
    extract_course_data(cookie)
