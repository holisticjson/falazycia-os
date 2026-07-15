import os
import sys
import pickle
import urllib3
import requests
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Wymuszenie kodowania UTF-8 dla konsoli Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Wyłączenie ostrzeżeń SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_drive_service(token_path):
    with open(token_path, "rb") as f:
        creds = pickle.load(f)

    # Odświeżenie tokenu OAuth (bez SSL)
    if creds.expired and creds.refresh_token:
        print("[INFO] Token wygasł. Odświeżanie sesji...")
        session = requests.Session()
        session.verify = False
        request = Request(session=session)
        creds.refresh(request)

    # Budowa serwisu Drive API (omijamy weryfikację certyfikatu w żądaniach biblioteki)
    # googleapiclient używa httplib2 lub custom requests transport. 
    # Aby wymusić brak certyfikacji najprościej wyłączyć weryfikację globalnie w sesji lub os.environ
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    
    # Tworzymy customowy HTTP client dla googleapiclient, który nie weryfikuje SSL
    import google_auth_httplib2
    import httplib2
    http = google_auth_httplib2.AuthorizedHttp(creds, http=httplib2.Http(disable_ssl_certificate_validation=True))
    
    return build('drive', 'v3', http=http)

def find_folder_id(service, folder_name):
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    if not files:
        return None
    return files[0]['id']

def list_files_in_folder_recursive(service, folder_id, current_path=""):
    drive_files = []
    query = f"'{folder_id}' in parents and trashed = false"
    page_token = None
    
    while True:
        results = service.files().list(
            q=query, 
            fields="nextPageToken, files(id, name, mimeType, size)",
            pageToken=page_token
        ).execute()
        
        files = results.get('files', [])
        for file in files:
            file_name = file['name']
            file_id = file['id']
            mime_type = file['mimeType']
            size = file.get('size', '0')
            
            full_path = os.path.join(current_path, file_name) if current_path else file_name
            
            if mime_type == 'application/vnd.google-apps.folder':
                # Rekurencyjnie wchodzimy do podfolderu
                drive_files.extend(list_files_in_folder_recursive(service, file_id, full_path))
            else:
                drive_files.append({
                    'name': file_name,
                    'path': full_path,
                    'id': file_id,
                    'mimeType': mime_type,
                    'size': int(size)
                })
                
        page_token = results.get('nextPageToken')
        if not page_token:
            break
            
    return drive_files

def main():
    token_path = r"C:\Aplikacje MVP\Holistic Jason\token_holisticjason.pickle"
    local_raw_path = r"C:\Aplikacje MVP\02_knowledge_base\raw"
    
    print("=" * 70)
    print("DIAGNOZA BAZY WIEDZY GOOGLE DRIVE (Konto: holisticjason@gmail.com)")
    print("=" * 70)
    
    if not os.path.exists(token_path):
        print(f"[BŁĄD] Brak pliku tokenu: {token_path}")
        return
        
    try:
        service = get_drive_service(token_path)
    except Exception as e:
        print(f"[BŁĄD] Błąd uwierzytelniania: {e}")
        return

    # Krok 1: Szukanie folderu HOLISTIC_KNOWLEDGE_BASE na Dysku Google
    folder_name = "HOLISTIC_KNOWLEDGE_BASE"
    print(f"\n[1/4] Szukanie folderu '{folder_name}' na Dysku Google...")
    folder_id = find_folder_id(service, folder_name)
    
    if not folder_id:
        print(f"[INFO] Nie znaleziono folderu głównego '{folder_name}'.")
        print("Sprawdzam alternatywny folder '02_knowledge_base' lub 'Baza_Wiedzy'...")
        folder_id = find_folder_id(service, "02_knowledge_base") or find_folder_id(service, "Baza_Wiedzy")
        
    if not folder_id:
        print("[BŁĄD] Nie znaleziono żadnego folderu bazy wiedzy na Dysku Google.")
        return
        
    print(f"  --> Znaleziono folder bazy wiedzy na Dysku. ID: {folder_id}")

    # Krok 2: Pobieranie listy plików z Dysku Google
    print("\n[2/4] Pobieranie pełnej listy plików z Dysku Google (rekurencyjnie)...")
    try:
        drive_files = list_files_in_folder_recursive(service, folder_id)
        print(f"  --> Pobrano {len(drive_files)} plików z Dysku Google.")
    except Exception as e:
        print(f"[BŁĄD] Błąd pobierania plików z Dysku: {e}")
        return

    # Krok 3: Skanowanie lokalnego folderu raw
    print(f"\n[3/4] Skanowanie lokalnego katalogu: {local_raw_path}...")
    local_files = []
    for root, _, files in os.walk(local_raw_path):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, local_raw_path)
            local_files.append({
                'name': f,
                'path': rel_path,
                'size': os.path.getsize(full_path)
            })
    print(f"  --> Znaleziono {len(local_files)} plików lokalnie.")

    # Krok 4: Porównanie i diagnoza różnic
    print("\n[4/4] Analiza porównawcza (Detektor Pominięć i Konfliktów)...")
    
    drive_names = {f['name'].lower(): f for f in drive_files}
    local_names = {f['name'].lower(): f for f in local_files}
    
    missing_on_drive = []
    for lf in local_files:
        if lf['name'].lower() not in drive_names:
            missing_on_drive.append(lf)
            
    missing_locally = []
    for df in drive_files:
        if df['name'].lower() not in local_names:
            missing_locally.append(df)

    # Statystyki formatów wykluczonych (np. przez NotebookLM)
    # NotebookLM obsługuje głównie: PDF, MD, TXT, DOCX, Google Docs, Google Slides
    supported_extensions = {'.pdf', '.md', '.docx', '.txt', '.html', '.gdoc', '.gslides'}
    skipped_by_rag_rules = []
    for lf in local_files:
        ext = os.path.splitext(lf['name'])[1].lower()
        if ext not in supported_extensions:
            skipped_by_rag_rules.append(lf)

    # Raport
    print("\n" + "=" * 70)
    print("WYNIKI DIAGNOZY I DETEKCJI CHAOSU:")
    print("=" * 70)
    print(f"1. Pliki na Dysku Google (Chmura):       {len(drive_files)}")
    print(f"2. Pliki lokalnie na komputerze (raw):   {len(local_files)}")
    print(f"3. Pliki tylko lokalnie (brak na Dysku):  {len(missing_on_drive)}")
    print(f"4. Pliki tylko na Dysku (brak lokalnie):  {len(missing_locally)}")
    print(f"5. Pliki lokalne o formacie NIE-RAG*:     {len(skipped_by_rag_rules)}")
    print("   (*nieobsługiwane formaty przez NotebookLM/Vertex np. .py, .json, .sh, .xlsx)")
    print("=" * 70)

    if missing_on_drive:
        print("\n[!] PRZYKŁADOWE PLIKI LOKALNE, KTÓRYCH BRAKUJE NA DYSKU GOOGLE (Max 15):")
        for i, f in enumerate(missing_on_drive[:15]):
            print(f"  - {f['path']} ({f['size'] / 1024:.1f} KB)")
        if len(missing_on_drive) > 15:
            print(f"  ... i {len(missing_on_drive) - 15} innych.")
            
    if missing_locally:
        print("\n[!] PRZYKŁADOWE PLIKI NA DYSKU GOOGLE, KTÓRYCH BRAKUJE LOKALNIE (Max 15):")
        for i, f in enumerate(missing_locally[:15]):
            print(f"  - {f['path']} ({f['size'] / 1024:.1f} KB)")
        if len(missing_locally) > 15:
            print(f"  ... i {len(missing_locally) - 15} innych.")

    if skipped_by_rag_rules:
        print("\n[!] PLIKI O FORMATACH TECHNICZNYCH (Pominięte przez mechanizmy RAG) (Max 15):")
        for i, f in enumerate(skipped_by_rag_rules[:15]):
            print(f"  - {f['path']}")
        if len(skipped_by_rag_rules) > 15:
            print(f"  ... i {len(skipped_by_rag_rules) - 15} innych.")

    print("\n[INFO] Diagnoza zakończona pomyślnie.")

if __name__ == "__main__":
    main()
