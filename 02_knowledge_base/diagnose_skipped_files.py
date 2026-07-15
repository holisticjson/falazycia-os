import os
import sys
import pickle
import google.auth
from google.auth.transport.requests import Request
import requests

def main():
    token_path = r"C:\Aplikacje MVP\Holistic Jason\token_holisticjason.pickle"
    if not os.path.exists(token_path):
        print(f"BŁĄD: Brak pliku tokenu pod ścieżką: {token_path}")
        return

    print("Wczytywanie tokenu autoryzacji dla konta holisticjason@gmail.com...")
    with open(token_path, "rb") as f:
        creds = pickle.load(f)

    # Odświeżenie tokenu jeśli wygasł, omijając weryfikację SSL na Windows
    if creds.expired and creds.refresh_token:
        print("Token wygasł. Odświeżanie (z pominięciem SSL)...")
        session = requests.Session()
        session.verify = False
        request = Request(session=session)
        creds.refresh(request)

    print("Token aktywowany pomyślnie.")
    
    # Próbujemy znaleźć powiązane projekty lub listę bucketów
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }

    # Pobieramy listę projektów GCP
    print("\nPobieranie projektów GCP dostępnych dla tego tokenu...")
    projects_url = "https://cloudresourcemanager.googleapis.com/v1/projects"
    try:
        res = requests.get(projects_url, headers=headers, verify=False)
        if res.status_code == 200:
            projects = res.json().get("projects", [])
            print(f"Znaleziono {len(projects)} projektów:")
            for p in projects:
                print(f"  - Projekt: {p.get('name')} (ID: {p.get('projectId')})")
                
                # Dla każdego projektu sprawdzamy buckety GCS
                list_buckets(p.get('projectId'), headers)
        else:
            print(f"Nie udało się pobrać projektów: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"Błąd podczas pobierania projektów: {e}")

def list_buckets(project_id, headers):
    print(f"  --> Szukanie bucketów GCS w projekcie {project_id}...")
    url = f"https://storage.googleapis.com/storage/v1/b?project={project_id}"
    try:
        res = requests.get(url, headers=headers, verify=False)
        if res.status_code == 200:
            buckets = res.json().get("items", [])
            print(f"      Znaleziono {len(buckets)} bucketów:")
            for b in buckets:
                print(f"        * gs://{b.get('id')}")
                # Listujemy pliki w znalezionym buckecie
                list_bucket_objects(b.get('id'), headers)
        else:
            print(f"      Brak dostępu lub błąd (HTTP {res.status_code})")
    except Exception as e:
        print(f"      Błąd: {e}")

def list_bucket_objects(bucket_name, headers):
    print(f"      --> Listowanie zawartości gs://{bucket_name}...")
    url = f"https://storage.googleapis.com/storage/v1/b/{bucket_name}/o"
    try:
        res = requests.get(url, headers=headers, verify=False)
        if res.status_code == 200:
            items = res.json().get("items", [])
            print(f"          W tym buckecie jest {len(items)} obiektów.")
            extensions = {}
            for item in items:
                ext = os.path.splitext(item.get('name'))[1].lower()
                extensions[ext] = extensions.get(ext, 0) + 1
            print(f"          Typy plików na GCS: {extensions}")
        else:
            print(f"          Nie można wylistować zawartości (HTTP {res.status_code})")
    except Exception as e:
        print(f"          Błąd: {e}")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    main()
