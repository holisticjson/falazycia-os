import os
import sys
import argparse
from google.cloud import storage

# Ustawienie ścieżki do poświadczeń GCP Service Account
CREDS_PATH = r"C:\Aplikacje MVP\01_JAISON_AGENCY_OS\01-brand\admin\credentials\gcp_service_account.json"
if os.path.exists(CREDS_PATH):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDS_PATH

BUCKET_NAME = "jaison-agency-knowledge"

BASE_DIR = r"C:\Aplikacje MVP\01_JAISON_AGENCY_OS"
FOLDERS_TO_SYNC = [
    r"01-brand",
    r"11_digital_product",
    r"08-reports",
    r"..\02_CLIENTS_AND_PROJECTS\lifewave"
]

def upload_local_to_gcs():
    """Wysyła lokalne pliki z komputera/laptopa do koszyka GCP Storage."""
    print(f"=== [UPLOAD] Wysyłanie plików do gs://{BUCKET_NAME} ===")
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        if not bucket.exists():
            print(f"[INFO] Tworzenie koszyka {BUCKET_NAME} w regionie eu...")
            bucket = client.create_bucket(BUCKET_NAME, location="eu")
    except Exception as e:
        print(f"[⚠️ ERR] Brak połączenia z GCP: {e}")
        return

    synced_count = 0
    for rel_folder in FOLDERS_TO_SYNC:
        abs_folder = os.path.abspath(os.path.join(BASE_DIR, rel_folder))
        if not os.path.exists(abs_folder):
            continue
            
        print(f"[SCAN] Skanowanie folderu: {abs_folder}...")
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

    print(f"[OK SUCCESS] Wysłano {synced_count} plików z tego urządzenia do koszyka GCP!")

def download_gcs_to_local():
    """Pobiera pliki z koszyka GCP Storage na lokalny dysk komputera/laptopa."""
    print(f"=== [DOWNLOAD] Pobieranie plików z gs://{BUCKET_NAME} na dysk lokalny ===")
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blobs = list(bucket.list_blobs())
    except Exception as e:
        print(f"[⚠️ ERR] Brak połączenia z GCP: {e}")
        return

    downloaded_count = 0
    for blob in blobs:
        local_dest = os.path.join(r"C:\Aplikacje MVP", blob.name.replace("/", "\\"))
        os.makedirs(os.path.dirname(local_dest), exist_ok=True)
        try:
            blob.download_to_filename(local_dest)
            downloaded_count += 1
        except Exception as ex:
            print(f"[ERR] Błąd pobierania {blob.name}: {ex}")

    print(f"[OK SUCCESS] Pobrano {downloaded_count} plików z koszyka GCP na to urządzenie!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dwukierunkowy GCS Mirror Sync (PC <-> GCP <-> Laptop)")
    parser.add_argument("--download", action="store_true", help="Pobierz z GCS na lokalny dysk")
    parser.add_argument("--upload", action="store_true", help="Wyślij z lokalnego dysku do GCS")
    args = parser.parse_args()

    if args.download:
        download_gcs_to_local()
    elif args.upload:
        upload_local_to_gcs()
    else:
        # Domyślnie wykonuje wysłanie lokalnych zmian i sprawdza stan
        upload_local_to_gcs()
