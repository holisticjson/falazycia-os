import os
import subprocess
import argparse

def run_sync(bucket_name, project_id="holistic-broker"):
    sa_path = r"C:\Aplikacje MVP\Holistic Jason\holistic-broker-sa.json"
    local_raw_path = r"C:\Aplikacje MVP\02_knowledge_base\raw"

    print("=" * 60)
    print("ROZPOCZYNAM SYNC BAZY WIEDZY Z GOOGLE CLOUD STORAGE (GCS)")
    print("=" * 60)
    print(f"Lokalny katalog raw: {local_raw_path}")
    print(f"Docelowy bucket GCS:  gs://{bucket_name}")
    print(f"Projekt GCP:          {project_id}")
    print(f"Klucz autoryzacji:    {sa_path}")
    print("-" * 60)

    if not os.path.exists(sa_path):
        print(f"BLAD: Nie znaleziono pliku klucza SA pod adresem: {sa_path}")
        return

    # Krok 1: Aktywacja konta uslugowego GCP
    print("\nKrok 1: Autoryzacja i aktywacja konta uslugowego GCP...")
    activate_cmd = f'gcloud auth activate-service-account --key-file="{sa_path}"'
    try:
        subprocess.run(activate_cmd, shell=True, check=True)
        print("Konto uslugowe zostalo pomyslnie aktywowane.")
    except Exception as e:
        print(f"Blad podczas aktywacji konta uslugowego: {e}")
        return

    # Krok 2: Proba utworzenia bucketu (na wypadek gdyby nie istnial)
    print(f"\nKrok 2: Sprawdzanie / Tworzenie zasobnika gs://{bucket_name}...")
    create_bucket_cmd = f'gsutil mb -p {project_id} -l europe-west1 gs://{bucket_name}'
    try:
        ls_result = subprocess.run(f'gsutil ls gs://{bucket_name}', shell=True, capture_output=True, text=True)
        if ls_result.returncode == 0:
            print(f"Zasobnik gs://{bucket_name} juz istnieje i jest dostepny.")
        else:
            print(f"Zasobnik gs://{bucket_name} nie istnieje. Probujemy go utworzyc...")
            mb_result = subprocess.run(create_bucket_cmd, shell=True, capture_output=True, text=True)
            if mb_result.returncode == 0:
                print(f"Pomyslnie utworzono nowy zasobnik: gs://{bucket_name}")
            else:
                print(f"Nie udalo sie utworzyc bucketu (prawdopodobnie brak uprawnien do tworzenia lub nazwa zajeta globalnie).")
                print(f"Szczegoly: {mb_result.stderr.strip()}")
                print("Przechodzimy do kroku synchronizacji zakladajac, ze masz dostep do zapisu.")
    except Exception as e:
        print(f"Blad podczas weryfikacji zasobnika: {e}")

    # Krok 3: Synchronizacja plikow (rsync)
    print(f"\nKrok 3: Synchronizacja danych (rsync) z pomijaniem folderow technicznych...")
    exclude_regex = r'.*(playwright_profile|node_modules|\.git|\.venv|archive|temp).*'
    sync_cmd = f'gsutil -m rsync -r -d -x "{exclude_regex}" "{local_raw_path}" gs://{bucket_name}/raw'
    
    print(f"Wykonuje: {sync_cmd}")
    try:
        subprocess.run(sync_cmd, shell=True, check=True)
        print("\nSUKCES! Twoja baza wiedzy zostala zsynchronizowana z GCS.")
        print("-" * 60)
        print(f"Dane sa gotowe do podpiecia w Vertex AI Search pod adresem:")
        print(f"gs://{bucket_name}/raw")
        print("-" * 60)
    except Exception as e:
        print(f"\nBlad podczas synchronizacji plikow: {e}")
        print("Upewnij sie, ze konto uslugowe ma nadane uprawnienia 'Storage Object Admin' dla tego bucketu.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronizacja bazy wiedzy raw z Google Cloud Storage")
    parser.add_argument("--bucket", default="holistic-broker-knowledge-base", help="Nazwa docelowego bucketu GCS")
    args = parser.parse_args()

    run_sync(args.bucket)
