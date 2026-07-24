import os
import sys
import glob
from google.cloud import storage

# Ustawienie ścieżki do poświadczeń GCP Service Account
CREDS_PATH = r"C:\Aplikacje MVP\01_JAISON_AGENCY_OS\01-brand\admin\credentials\gcp_service_account.json"
if os.path.exists(CREDS_PATH):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDS_PATH

BUCKET_NAME = "jaison-agency-knowledge"

# Lokalny katalog bazowy
BASE_DIR = r"C:\Aplikacje MVP\01_JAISON_AGENCY_OS"
FOLDERS_TO_SYNC = [
    r"01-brand",
    r"11_digital_product",
    r"08-reports",
    r"..\02_CLIENTS_AND_PROJECTS\lifewave"
]

def sync_to_gcs():
    print(f"=== Rozpoczęcie synchronizacji GCS Mirror Sync do gs://{BUCKET_NAME} ===")
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        if not bucket.exists():
            print(f"[INFO] Koszyk {BUCKET_NAME} nie istnieje. Tworzenie koszyka w GCP...")
            bucket = client.create_bucket(BUCKET_NAME, location="eu")
            print(f"[OK] Koszyk {BUCKET_NAME} stworzony pomyślnie!")
    except Exception as e:
        print(f"[⚠️ WARNING] Nie można połączyć z GCP Storage: {e}")
        print("[INFO] Pliki pozostają zsynchronizowane przez Git Sync z GitHub.")
        return

    synced_count = 0
    for rel_folder in FOLDERS_TO_SYNC:
        abs_folder = os.path.abspath(os.path.join(BASE_DIR, rel_folder))
        if not os.path.exists(abs_folder):
            continue
            
        print(f"[SYNC] Skanowanie folderu: {abs_folder}...")
        for root, dirs, files in os.walk(abs_folder):
            for file in files:
                if file.startswith(".") or file.endswith(".tmp") or "09-archive" in root:
                    continue
                local_path = os.path.join(root, file)
                rel_path = os.path.relpath(local_path, r"C:\Aplikacje MVP").replace("\\", "/")
                blob = bucket.blob(rel_path)
                try:
                    blob.upload_from_filename(local_path)
                    synced_count += 1
                except Exception as ex:
                    print(f"[ERR] Błąd wysyłania {rel_path}: {ex}")

    print(f"[OK] Zsynchronizowano {synced_count} plików do chmury GCS Storage!")
    print("=== Synchronizacja GCS Mirror Sync Zakończona Pomyślnie! ===")

if __name__ == "__main__":
    sync_to_gcs()
