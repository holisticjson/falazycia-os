import os
import sys
import time
import hashlib
import re
import fnmatch
import requests
import urllib3
from pathlib import Path
from google.oauth2 import service_account
import google.auth.transport.requests

# Wymuszenie kodowania UTF-8 dla konsoli (zapobiega UnicodeEncodeError na Windowsie)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Wylaczenie ostrzezen SSL o braku weryfikacji certyfikatu
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Ścieżki
BASE_DIR = Path(r"C:\Aplikacje MVP")
WORKSPACE_DIR = BASE_DIR / "Holistic Jason"
KNOWLEDGE_BASE_DIR = BASE_DIR / "02_knowledge_base"
SYNTHESIZED_DIR = KNOWLEDGE_BASE_DIR / "synthesized"
RAW_DIR = KNOWLEDGE_BASE_DIR / "raw"
ENV_PATH = WORKSPACE_DIR / ".env"
IGNORE_PATH = WORKSPACE_DIR / ".antigravityignore"
SA_KEY_PATH = WORKSPACE_DIR / "holistic-broker-sa.json"

# Kategorie docelowe
CATEGORIES = {
    "video_i_kreacja": "Materiały dotyczące wideo, montażu, scenariuszy, rolek (reels), YouTube, haków (hooks), transkrypcji wideo, grafiki i kreacji marketingowych.",
    "marketing_ads_i_lejki": "Strategie marketingowe, kampanie reklamowe (FB ads, Google ads), lejki sprzedażowe, copywriting, UX/UI stron, SEO lokalne i generowanie leadów.",
    "produkty_cyfrowe": "E-booki, kursy online, pomysły na biznes cyfrowy, monetyzacja wiedzy, nisze, zarabianie online i produkty cyfrowe pod własną marką.",
    "adhd": "Materiały o ADHD, skupieniu, organizacji pracy, zarządzaniu dopaminą, produktywności, habitach i systemach wspierających osoby neuronietypowe.",
    "wiedza_o_zdrowiu": "Ogólna wiedza o zdrowiu, biohacking, optymalizacja snu, regeneracja, poziom energii i nawyki zdrowotne.",
    "nieruchomosci": "Analizy rynku nieruchomości komercyjnych i mieszkaniowych w Polsce i Europie, inwestowanie, flirty, pośrednictwo i rynek budowlany.",
    "ai_i_technologia": "Sztuczna inteligencja, Prompt Engineering, automatyzacje (n8n, make), nowinki technologiczne, skille Claude, narzędzia online i programowanie."
}

def load_env_key(key_name):
    """Wczytuje klucz z pliku .env."""
    if not ENV_PATH.exists():
        print(f"[OSTRZEZENIE] Brak pliku .env pod sciezka {ENV_PATH}")
        return os.environ.get(key_name, "")
    
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith(key_name):
                parts = line.strip().split("=", 1)
                if len(parts) == 2:
                    return parts[1].strip()
    return os.environ.get(key_name, "")

def parse_ignore_patterns():
    """Wczytuje i parsuje reguly z .antigravityignore."""
    patterns = []
    if not IGNORE_PATH.exists():
        print(f"[OSTRZEZENIE] Brak pliku ignore pod sciezka {IGNORE_PATH}")
        return patterns
    
    with open(IGNORE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
    return patterns

def is_ignored(filepath, patterns):
    """Sprawdza, czy plik pasuje do jakiejkolwiek reguly ignorowania."""
    # Konwertujemy na relatywna sciezke dla latwiejszego dopasowania
    try:
        rel_path = Path(filepath).relative_to(KNOWLEDGE_BASE_DIR).as_posix()
    except ValueError:
        rel_path = Path(filepath).as_posix()

    filename = Path(filepath).name
    
    for pattern in patterns:
        # Usuwamy ewentualne slash-e na koncu katalogow w regulach
        clean_pat = pattern.rstrip("/")
        
        # Proste dopasowanie rozszerzen np. *.mp4, *.pdf
        if clean_pat.startswith("*."):
            ext = clean_pat.replace("*", "")
            if filepath.endswith(ext):
                return True
        
        # Dopasowanie nazwy pliku lub czesci sciezki
        if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(filename, pattern):
            return True
        if clean_pat in rel_path.split("/"):
            return True
            
    return False

def calculate_sha256(filepath):
    """Oblicza skrot SHA-256 pliku."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Bufor do cache-owania OAuth tokena
_cached_token = None
_token_expiry = 0

def get_vertex_oauth_token():
    """Wczytuje i odswieza token OAuth z konta serwisowego GCP."""
    global _cached_token, _token_expiry
    now = time.time()
    if _cached_token and now < _token_expiry - 60:
        return _cached_token
        
    if not SA_KEY_PATH.exists():
        raise FileNotFoundError(f"Brak pliku klucza GCP pod sciezka {SA_KEY_PATH}")
        
    creds = service_account.Credentials.from_service_account_file(
        str(SA_KEY_PATH),
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    
    session = requests.Session()
    session.verify = False
    request = google.auth.transport.requests.Request(session=session)
    creds.refresh(request)
    
    _cached_token = creds.token
    _token_expiry = now + 3600 # token jest wazny przez 1 godzine
    return _cached_token

def query_llm_with_retry(prompt, model="gemini-2.5-flash"):
    """Zadaje pytanie LLM poprzez bezpośrednie API GCP Vertex AI z obsluga Exponential Backoff."""
    project_id = "holistic-broker"
    region = "us-central1"
    url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/publishers/google/models/{model}:generateContent"
    
    max_retries = 5
    base_delay = 2
    
    for attempt in range(max_retries):
        try:
            # Opoznienie miedzy zapytaniami (jak zazadal uzytkownik)
            time.sleep(3)
            
            token = get_vertex_oauth_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": f"Jestes precyzyjnym asystentem klasyfikacji dokumentow. Odpowiadaj WYLACZNIE w formacie JSON zawierajacym klucz 'kategoria' oznaczajacy jedna z dopuszczalnych kategorii oraz klucz 'uzasadnienie' z krotkim wyjasnieniem.\n\n{prompt}"
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "responseMimeType": "application/json"
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30, verify=False)
            
            if response.status_code == 429:
                delay = base_delay * (2 ** attempt)
                print(f"[429] Otrzymano HTTP 429 (Rate Limit). Ponawianie za {delay}s (proba {attempt + 1}/{max_retries})...")
                time.sleep(delay)
                continue
                
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"[BLAD] Blad krytyczny API po {max_retries} probach: {e}")
                return None
            delay = base_delay * (2 ** attempt)
            print(f"[INFO] Blad polaczenia lub API: {e}. Ponawianie za {delay}s...")
            time.sleep(delay)
            
    return None

def analyze_file_category(filepath):
    """Czyta poczatek pliku i wysyla zapytanie do LLM o klasyfikacje."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(1500) # bierzemy pierwsze 1500 znakow
    except Exception as e:
        print(f"[BLAD] Nie mozna odczytac pliku {Path(filepath).name}: {e}")
        return None, None
        
    prompt = f"""Przeanalizuj ponizszy dokument (poczatek pliku) i dopasuj go do JEDNEJ z ponizszych kategorii:

{chr(10).join([f"- '{k}': {v}" for k, v in CATEGORIES.items()])}

Plik: {Path(filepath).name}
Tresc:
---
{content}
---

Zworc wynik wylacznie jako poprawny obiekt JSON:
{{
  "kategoria": "nazwa_kategorii",
  "uzasadnienie": "Krotkie 1-zdaniowe uzasadnienie"
}}"""

    res = query_llm_with_retry(prompt)
    if res and "candidates" in res:
        try:
            content_str = res["candidates"][0]["content"]["parts"][0]["text"]
            import json
            parsed = json.loads(content_str)
            return parsed.get("kategoria"), parsed.get("uzasadnienie")
        except Exception as e:
            print(f"[OSTRZEZENIE] Blad parsowania odpowiedzi dla {Path(filepath).name}: {e}")
    return None, None

def run_sorting(dry_run=True):
    print("=" * 80)
    print(f"LOKALNY AGENT SORTUJACY (Dry Run = {dry_run})")
    print("=" * 80)
    
    ignore_patterns = parse_ignore_patterns()
    print(f"[INFO] Zaladowano {len(ignore_patterns)} wzorcow z .antigravityignore")
    
    # Krok 1: Skanowanie plikow i semantyczna deduplikacja
    print("\n[INFO] Krok 1: Skanowanie i de-duplikacja plikow w folderze synthesized...")
    all_files = []
    hashes = {}
    duplicates = []
    
    for root, _, files in os.walk(SYNTHESIZED_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            
            # Sprawdzamy ignorowanie
            if is_ignored(full_path, ignore_patterns):
                print(f"[INFO] Ignoruje plik (zgodnie z .antigravityignore): {file}")
                continue
                
            file_hash = calculate_sha256(full_path)
            if file_hash in hashes:
                duplicates.append((full_path, hashes[file_hash]))
            else:
                hashes[file_hash] = full_path
                all_files.append(full_path)
                
    print(f"[INFO] Znaleziono {len(all_files)} unikalnych plikow i {len(duplicates)} dokladnych duplikatow.")
    
    if duplicates:
        print("\n[INFO] Wykryte dokladne duplikaty:")
        for dup, original in duplicates:
            print(f"  - DUPLIKAT: {Path(dup).name} === ORYGINAL: {Path(original).name}")
            if not dry_run:
                # Przenosimy duplikat do folderu archiwalnego
                archive_dup_dir = KNOWLEDGE_BASE_DIR / "archive" / "duplicates"
                archive_dup_dir.mkdir(parents=True, exist_ok=True)
                try:
                    os.rename(dup, archive_dup_dir / Path(dup).name)
                    print(f"    --> Przeniesiono do: {archive_dup_dir / Path(dup).name}")
                except Exception as e:
                    print(f"    --> [BLAD] Blad przenoszenia: {e}")
                    
    # Krok 2: Klasyfikacja i sortowanie
    print("\n[INFO] Krok 2: Semantyczna klasyfikacja i porzadkowanie plikow...")
    
    sorted_stats = {cat: 0 for cat in CATEGORIES}
    sorted_stats["nieznane/blad"] = 0
    
    for filepath in all_files:
        filename = Path(filepath).name
        print(f"\n[INFO] Analiza pliku: {filename}...")
        
        category, reason = analyze_file_category(filepath)
        
        if category in CATEGORIES:
            print(f"  --> Kategoria: {category}")
            print(f"  --> Uzasadnienie: {reason}")
            sorted_stats[category] += 1
            
            if not dry_run:
                dest_dir = KNOWLEDGE_BASE_DIR / "organized" / category
                dest_dir.mkdir(parents=True, exist_ok=True)
                try:
                    os.rename(filepath, dest_dir / filename)
                    print(f"  [OK] Przeniesiono do: organized/{category}/{filename}")
                except Exception as e:
                    print(f"  [BLAD] Blad przenoszenia: {e}")
        else:
            print(f"  [?] Nieznana kategoria lub blad API: {category}")
            sorted_stats["nieznane/blad"] += 1
            if not dry_run:
                dest_dir = KNOWLEDGE_BASE_DIR / "organized" / "nieznane"
                dest_dir.mkdir(parents=True, exist_ok=True)
                try:
                    os.rename(filepath, dest_dir / filename)
                except Exception as e:
                    pass

    print("\n" + "=" * 80)
    print("PODSUMOWANIE SORTOWANIA:")
    print("=" * 80)
    for cat, count in sorted_stats.items():
        print(f"  - {cat:25}: {count} plikow")
    print("=" * 80)
    print("Gotowe! Aby wykonac realne przenoszenie plikow, uruchom skrypt z parametrem --run")

if __name__ == "__main__":
    run_mode = len(sys.argv) > 1 and sys.argv[1] == "--run"
    run_sorting(dry_run=not run_mode)
