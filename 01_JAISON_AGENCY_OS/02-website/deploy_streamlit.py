# -*- coding: utf-8 -*-
"""
🚀 deploy_streamlit.py — Oficjalny Skrypt Wdrożeniowy dla JAISON OS Dashboard
Kompiluje i wdraża kontener Streamlit (dashboard_and_core) na Google Cloud Run.
"""

import os
import subprocess
import sys

PROJECT_ID = "holistic-dashboard-dev"
REGION = "europe-west1"  # Belgia — wspiera bezpośrednie mapowanie domen
SERVICE_NAME = "holistic-ceo"
IMAGE_TAG = f"gcr.io/{PROJECT_ID}/{SERVICE_NAME}:latest"

def run_command(cmd, desc=None):
    if desc:
        print(f"\n📌 {desc}...")
    print(f"Executing: {cmd}")
    
    # Uruchomienie komendy i przekazywanie wyjścia w czasie rzeczywistym
    process = subprocess.Popen(
        cmd, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        text=True, 
        encoding="utf-8", 
        errors="replace"
    )
    
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            
    rc = process.poll()
    if rc != 0:
        print(f"❌ Błąd podczas wykonywania: {cmd}. Kod błędu: {rc}")
        return False
    return True

def main():
    # Wymuszenie kodowania UTF-8 na Windows
    if sys.platform.startswith('win'):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    print("🧠 ===============================================")
    print("🚀 DEPLOY JAISON OS DASHBOARD — GOOGLE CLOUD RUN")
    print("🧠 ===============================================")

    # Krok 1: Ustawienie projektu GCP
    if not run_command(f"gcloud config set project {PROJECT_ID}", "Krok 1: Ustawienie aktywnego projektu GCP"):
        print("❌ Nie udało się ustawić projektu GCP.")
        sys.exit(1)

    # Krok 2: Aktywacja wymaganych usług API (na wypadek ich braku)
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

    # Krok 3: Budowanie obrazu kontenera na Google Cloud Build
    # Budujemy na podstawie Dockerfile w bieżącym katalogu (dashboard_and_core)
    build_cmd = f"gcloud builds submit --tag {IMAGE_TAG} ."
    if not run_command(build_cmd, "Krok 3: Budowanie obrazu kontenera na Google Cloud Build"):
        print("❌ Błąd podczas budowania obrazu w chmurze.")
        sys.exit(1)

    # Krok 4: Wdrażanie kontenera na Google Cloud Run
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

    # Krok 5: Podsumowanie
    print("\n" + "=" * 50)
    print("🎉 WDROŻENIE ZAKOŃCZONE SUKCESEM!")
    print("=" * 50)
    print(f"🔗 Bezpośredni URL:       (Wypisany powyżej w logu GCP)")
    print(f"📊 Domena (os.jaison.pl): https://os.jaison.pl")
    print(f"🔑 Hasło panelu:          holistic2026")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()
