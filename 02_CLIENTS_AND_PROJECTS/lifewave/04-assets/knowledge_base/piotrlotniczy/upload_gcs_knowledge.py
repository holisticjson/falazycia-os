"""
================================================================================
  AUTOMATYCZNY SKRYPT ZASILANIA BUCKETU GCS NOTATKAMI RAG (PROJECT: falazycia-os)
================================================================================
  Konto: lifelifewave@gmail.com
  Projekt GCP: falazycia-os
  Bucket GCS: gs://falazycia-os-piotrlotniczy-knowledge
  Lokalizacja: europe-central2 (Warszawa)
================================================================================
"""

import os
import sys
import glob
import subprocess

PROJECT_ID  = "falazycia-os"
BUCKET_NAME = "falazycia-os-piotrlotniczy-knowledge"
BUCKET_URI  = f"gs://{BUCKET_NAME}"
REGION      = "europe-west1"

NOTES_DIR   = r"C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\lifewave\04-assets\knowledge_base\piotrlotniczy\obsidian_notes"
MOC_FILE    = r"C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\lifewave\04-assets\knowledge_base\piotrlotniczy\00_FLIGHT_HACKING_MOC_OBSIDIAN.md"

def run_cmd(cmd):
    print(f"🚀 Uruchamianie: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"  ✅ Sukces: {res.stdout.strip()[:200]}")
        return True, res.stdout
    else:
        print(f"  ⚠️ Uwaga / Błąd: {res.stderr.strip()[:300]}")
        return False, res.stderr

def main():
    print("=" * 80)
    print(f" 📦 TWORZENIE I ZASILANIE BUCKETU GCS: {BUCKET_URI} (Projekt: {PROJECT_ID})")
    print("=" * 80)

    # 1. Ustawienie aktywnego projektu gcloud
    run_cmd(f"gcloud config set project {PROJECT_ID}")

    # 2. Aktywacja usług API
    run_cmd(f"gcloud services enable storage.googleapis.com discoveryengine.googleapis.com --project={PROJECT_ID}")

    # 3. Utworzenie bucketu GCS
    run_cmd(f"gcloud storage buckets create {BUCKET_URI} --location={REGION} --project={PROJECT_ID}")

    # 4. Włączenie jednolitego dostępu (UBLA)
    run_cmd(f"gcloud storage buckets update {BUCKET_URI} --uniform-bucket-level-access --project={PROJECT_ID}")

    # 5. Kopiowanie notatek Obsidian
    if os.path.exists(NOTES_DIR):
        print(f"\n 📂 Kopiowanie notatek z {NOTES_DIR}...")
        notes_pattern = os.path.join(NOTES_DIR, "*.md")
        cmd_cp_notes = f'gcloud storage cp "{notes_pattern}" {BUCKET_URI}/obsidian_notes/ --project={PROJECT_ID}'
        run_cmd(cmd_cp_notes)

    # 6. Kopiowanie MOC
    if os.path.exists(MOC_FILE):
        print(f"\n 📄 Kopiowanie MOC {MOC_FILE}...")
        cmd_cp_moc = f'gcloud storage cp "{MOC_FILE}" {BUCKET_URI}/ --project={PROJECT_ID}'
        run_cmd(cmd_cp_moc)

    # 7. Nadanie uprawnień IAM dla Discovery Engine / Agent Builder
    print("\n 🔑 Nadawanie ról IAM dla konta Discovery Engine...")
    proj_num_res = subprocess.run(f"gcloud projects describe {PROJECT_ID} --format=\"value(projectNumber)\"", shell=True, capture_output=True, text=True)
    proj_num = proj_num_res.stdout.strip()

    if proj_num:
        print(f"  ℹ️ Numer projektu {PROJECT_ID}: {proj_num}")
        sa_email = f"service-{proj_num}@gcp-sa-discoveryengine.iam.gserviceaccount.com"
        run_cmd(f"gcloud storage buckets add-iam-policy-binding {BUCKET_URI} --member=\"serviceAccount:{sa_email}\" --role=\"roles/storage.objectViewer\" --project={PROJECT_ID}")
        run_cmd(f"gcloud storage buckets add-iam-policy-binding {BUCKET_URI} --member=\"user:lifelifewave@gmail.com\" --role=\"roles/storage.admin\" --project={PROJECT_ID}")

    print("\n" + "=" * 80)
    print(" ✅ WGRYWANIE BAZY WIEDZY DLA PIOTRA ŁOTOWSKIEGO ZAKOŃCZONE!")
    print(f" 📍 Ścieżka GCS dla Data Store w Vertex AI Agent Builder: {BUCKET_URI}/*.md")
    print("=" * 80)

if __name__ == "__main__":
    main()
