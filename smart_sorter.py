import os
import json
import urllib.request
import urllib.error
import ssl
import sys
from google.cloud import storage

BUCKET_NAME = "holistic_kubelek"

# Silosy docelowe
SILOS_CEO = "silos-ceo"
SILOS_CMO = "silos-cmo"
SILOS_CTO = "silos-cto"
TRASH = "trash"

IGNORED_PREFIXES = {
    f"{SILOS_CEO}/", 
    f"{SILOS_CMO}/", 
    f"{SILOS_CTO}/", 
    f"{TRASH}/", 
    "trash-box/",
    "wiedza/" # np. folder RAG z wrzutni
}

# Twarde reguły segregacji dla głównych folderów systemowych
STATIC_OVERRIDES = {
    "01-offer-positioning/": SILOS_CEO,
    "02-hooks-patterns/": SILOS_CMO,
    "03-video-scripts/": SILOS_CMO,
    "04-editing-retention/": SILOS_CMO,
    "05-platform-native/": SILOS_CMO,
    "06-proof-assets/": SILOS_CEO,
    "07-constraints-policies/": SILOS_CEO,
    "08-newsletters-mail-intel/": SILOS_CMO,
    "raw/": SILOS_CMO
}

def safe_print(msg):
    """Wypisuje tekst na konsolę, zapobiegając błędom kodowania na Windows (CP1250/UnicodeEncodeError)."""
    try:
        print(msg)
    except UnicodeEncodeError:
        try:
            print(msg.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
        except Exception:
            print(msg.encode('ascii', errors='replace').decode('ascii'))

def get_gcs_client():
    """Tworzy klienta GCS z wyłączoną weryfikacją SSL, aby zapobiec zawieszaniu na Windows."""
    import google.auth
    from google.auth.transport.requests import AuthorizedSession
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    credentials, project = google.auth.default()
    session = AuthorizedSession(credentials)
    session.verify = False # Pominięcie sprawdzania certyfikatu SSL (blokada AVG)
    
    return storage.Client(credentials=credentials, project=project, _http=session)

def get_top_level_folders():
    """Pobiera listę pierwszorzędnych katalogów z bucketu GCS."""
    storage_client = get_gcs_client()
    bucket = storage_client.bucket(BUCKET_NAME)
    
    # delimiter='/' grupuje obiekty w wirtualne foldery (prefixes)
    blobs = bucket.list_blobs(delimiter='/')
    # Consumujemy iterator, by prefixes zostały załadowane do obiektu blobs
    list(blobs) 
    
    prefixes = list(blobs.prefixes)
    folders = [f for f in prefixes if f not in IGNORED_PREFIXES]
    return folders

def call_llm(prompt):
    """Wywołuje model Gemini 2.5 Flash bezpośrednio przez Vertex AI REST API z obejściem SSL."""
    import google.auth
    from google.auth.transport.requests import Request
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Wyłączamy weryfikację SSL dla google-auth (błąd certyfikatu w tle)
    old_request = requests.Session.request
    def new_request(*args, **kwargs):
        kwargs['verify'] = False
        return old_request(*args, **kwargs)
    requests.Session.request = new_request
    
    try:
        credentials, project = google.auth.default()
        credentials.refresh(Request())
        token = credentials.token
    except Exception as e:
        raise RuntimeError(f"Błąd autoryzacji GCP (ADC): {e}. Uruchom w PowerShell: gcloud auth application-default login")
    finally:
        requests.Session.request = old_request

    location = "us-central1"
    model = "gemini-2.5-flash"
    url = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/publishers/google/models/{model}:generateContent"
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json"
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )

    try:
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        if hasattr(e, "read"):
            err_details = e.read().decode('utf-8')
            raise RuntimeError(f"Błąd REST API Vertex: {e}. Szczegóły: {err_details}")
        raise RuntimeError(f"Błąd komunikacji z Vertex API: {e}")

def clean_json_response(content):
    """Czyści surowy tekst z LLM, aby wyodrębnić prawidłowy JSON."""
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]
    if content.endswith("```"):
        content = content[:-3]
    return json.loads(content.strip())

def get_ai_sorting_plan(folders):
    """Wysyła listę folderów do klasyfikacji przez AI z uwzględnieniem twardych reguł."""
    plan = {}
    need_ai = []
    
    # Najpierw przypisujemy foldery zdefiniowane na sztywno
    for f in folders:
        if f in STATIC_OVERRIDES:
            plan[f] = STATIC_OVERRIDES[f]
        else:
            need_ai.append(f)
            
    # Jeśli nie ma innych folderów do posortowania, zwracamy plan
    if not need_ai:
        return plan
        
    prompt = f"""
    Jesteś Głównym Architektem Informacji w systemie Holistic Agentic OS.
    Twoim zadaniem jest przypisanie surowych nazw folderów z Cloud Storage do jednego z 4 silosów.
    
    ZASADY PRZYDZIAŁU:
    1. silos-ceo (Strategia, Biznes, Oferta, Skalowanie agencji, High-Ticket, Modele Biznesowe, Case Studies, Cenniki)
    2. silos-cmo (Psychologia, ADHD, Neuroatypowość, Marketing, Treść, Copywriting, Social Media, Wideo, Skrypty, Edycja, Montaż, Newslettery)
    3. silos-cto (Technologia, Automatyzacje, n8n, Kod, Web development, API, GHL, Systeme.io, Serwery, Integracje)
    4. trash (Materiały przestarzałe, kursy niezwiązane bezpośrednio z naszą automatyzacją lub marketingiem, szum informacyjny)
    
    Oto lista folderów do przeanalizowania:
    {json.dumps(need_ai, indent=2)}
    
    Zwróć wyłącznie czysty obiekt JSON bez dodatkowych komentarzy i bez markdownu.
    Kluczem w JSON ma być dokładnie nazwa folderu (np. "Akademia/"), a wartością docelowy silos ("silos-ceo", "silos-cmo", "silos-cto" lub "trash").
    """
    
    raw_response = call_llm(prompt)
    ai_plan = clean_json_response(raw_response)
    plan.update(ai_plan)
    return plan

def execute_server_side_move(sorting_plan):
    """Przenosi pliki po stronie serwera GCS (błyskawiczne przenoszenie metadanych)."""
    storage_client = get_gcs_client()
    bucket = storage_client.bucket(BUCKET_NAME)
    
    for source_folder, target_silos in sorting_plan.items():
        if target_silos not in [SILOS_CEO, SILOS_CMO, SILOS_CTO, TRASH]:
            safe_print(f"[WARN] Nieprawidłowa nazwa silosu: {target_silos} dla {source_folder}. Pomijam.")
            continue
            
        safe_print(f"\n[MOVE] Rozpoczynam przenoszenie: {source_folder} -> {target_silos}/{source_folder}")
        
        # Pobranie wszystkich blobów z danym prefiksem
        blobs_to_move = list(bucket.list_blobs(prefix=source_folder))
        
        if not blobs_to_move:
            safe_print(f"[INFO] Folder {source_folder} jest pusty lub nie istnieje.")
            continue
            
        for blob in blobs_to_move:
            new_name = f"{target_silos}/{blob.name}"
            safe_print(f"  [-] Kopiuję metadane: {blob.name} -> {new_name}")
            
            # rename_blob wykonuje server-side copy + delete
            try:
                bucket.rename_blob(blob, new_name)
            except Exception as e:
                safe_print(f"  [ERROR] Błąd przenoszenia pliku {blob.name}: {e}")
                
        safe_print(f"[OK] Ukończono przenoszenie dla: {source_folder}")

if __name__ == "__main__":
    safe_print("==================================================")
    safe_print("HOLISTIC SMART SORTER - Organizacja Bucketu GCS")
    safe_print("==================================================")
    
    try:
        safe_print("[GET] Pobieram aktualną strukturę z GCS...")
        folders = get_top_level_folders()
        
        if not folders:
            safe_print("[INFO] Brak folderów do posortowania (lub wszystkie zostały już uporządkowane).")
            exit(0)
            
        safe_print(f"[GET] Znaleziono {len(folders)} folderów do klasyfikacji:")
        for f in folders:
            safe_print(f"  - {f}")
            
        safe_print("\n[AI] Analizuję foldery za pomocą AI...")
        sorting_plan = get_ai_sorting_plan(folders)
        
        print("\n[PLAN] PROPONOWANY PLAN SEGREGACJI:")
        print(json.dumps(sorting_plan, indent=2, ensure_ascii=False))
        
        print("\n[WARN] PRZECZYTAJ UWAŻNIE POWYŻSZĄ LISTĘ!")
        potwierdzenie = input("Czy ten podział jest prawidłowy? Wpisz 'TAK', aby rozpocząć migrację: ")
        
        if potwierdzenie.strip().upper() == "TAK":
            execute_server_side_move(sorting_plan)
            safe_print("\n[SUCCESS] Buckety zostały pomyślnie zreorganizowane pod chmurowy RAG!")
        else:
            safe_print("\n[CANCEL] Operacja anulowana przez użytkownika.")
            
    except Exception as e:
        safe_print(f"\n[ERROR] Wystąpił krytyczny błąd: {e}")
