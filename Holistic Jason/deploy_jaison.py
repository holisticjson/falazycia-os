# -*- coding: utf-8 -*-
"""
🚀 deploy_jaison.py — Oficjalny Skrypt Wdrożeniowy Agencji Jaison (jaison.pl / app.jaison.pl)
Uruchamia kompilację i wdrożenie kontenera Streamlit (Hermes OS) na Google Cloud Run.
"""

import os
import subprocess
import sys

PROJECT_ID = "holistic-dashboard-dev"
REGION = "europe-central2"  # Warszawa — najniższe opóźnienia
SERVICE_NAME = "holistic-ceo"
IMAGE_TAG = f"gcr.io/{PROJECT_ID}/{SERVICE_NAME}:latest"
SA_KEY_FILE = "holistic-dashboard-dev-dea2c872139e.json"

def run_command(cmd, desc=None):
    if desc:
        print(f"\n📌 {desc}...")
    print(f"Executing: {cmd}")
    
    # Run command and pipe output in real-time
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            
    rc = process.poll()
    if rc != 0:
        print(f"❌ Error executing command. Exit code: {rc}")
        return False
    return True

def main():
    # Force UTF-8 encoding on Windows to prevent UnicodeEncodeError
    if sys.platform.startswith('win'):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    print("🧠 ===============================================")
    print("🚀 DEPLOY AGENCJI JAISON — GOOGLE CLOUD RUN (Streamlit)")
    print("🧠 ===============================================")

    # Krok 0: Autoryzacja Service Account
    if os.path.exists(SA_KEY_FILE):
        desc = "Krok 0: Autoryzacja za pomocą pliku klucza Service Account"
        auth_cmd = f"gcloud auth activate-service-account --key-file={SA_KEY_FILE}"
        if not run_command(auth_cmd, desc):
            print("⚠️ Autoryzacja przez Service Account nie powiodła się. Próba użycia domyślnej sesji gcloud...")
    else:
        print(f"\n⚠️ Brak pliku klucza '{SA_KEY_FILE}' w katalogu głównym.")
        print("Używam domyślnej autoryzacji Twojego konta gcloud (upewnij się, że jesteś zalogowany).")

    # Krok 1: Ustawienie projektu GCP
    if not run_command(f"gcloud config set project {PROJECT_ID}", "Krok 1: Ustawienie aktywnego projektu GCP"):
        print("❌ Nie udało się ustawić projektu GCP.")
        sys.exit(1)

    # Krok 2: Włączenie wymaganych usług API (na wypadek ich braku)
    apis_cmd = (
        f"gcloud services enable "
        f"run.googleapis.com "
        f"cloudbuild.googleapis.com "
        f"artifactregistry.googleapis.com "
        f"aiplatform.googleapis.com"
    )
    if not run_command(apis_cmd, "Krok 2: Aktywacja wymaganych usług API GCP"):
        print("❌ Nie udało się aktywować wymaganych API.")
        sys.exit(1)

    # Krok 3: Kompilacja i wysłanie obrazu Docker do Artifact Registry przez Cloud Build
    # Budujemy na podstawie Dockerfile w roocie (który kopiuje pliki z 02-os-jaison)
    build_cmd = f"gcloud builds submit --tag {IMAGE_TAG} ."
    if not run_command(build_cmd, "Krok 3: Budowanie obrazu kontenera na Google Cloud Build"):
        print("❌ Błąd podczas budowania obrazu w chmurze.")
        sys.exit(1)

    # Krok 4: Wdrożenie na Google Cloud Run
    deploy_cmd = (
        f"gcloud run deploy {SERVICE_NAME} "
        f"--image {IMAGE_TAG} "
        f"--platform managed "
        f"--region {REGION} "
        f"--allow-unauthenticated "
        f"--memory 1Gi "
        f"--cpu 1 "
        f"--min-instances 0 "
        f"--max-instances 2 "
        f"--timeout 300 "
        f"--set-env-vars \"APP_PASSWORD=holistic2026,GCP_PROJECT={PROJECT_ID},GCP_LOCATION=us-central1\" "
        f"--service-account \"holistic-dashboard@{PROJECT_ID}.iam.gserviceaccount.com\""
    )
    if not run_command(deploy_cmd, "Krok 4: Wdrażanie kontenera na Google Cloud Run"):
        print("❌ Wdrożenie na Cloud Run zakończyło się błędem.")
        sys.exit(1)

    # Krok 5: Wyświetlenie wyników
    print("\n" + "=" * 50)
    print("🎉 WDROŻENIE ZAKOŃCZONE SUKCESEM!")
    print("=" * 50)
    print(f"🔗 Strona główna agencji: https://jaison.pl")
    print(f"📊 Panel Streamlit OS:    https://app.jaison.pl")
    print(f"🔑 Hasło panelu Streamlit: holistic2026")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()
