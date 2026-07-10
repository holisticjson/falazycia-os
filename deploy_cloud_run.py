# -*- coding: utf-8 -*-
"""
🚀 deploy_cloud_run.py — Oficjalny Skrypt Wdrożeniowy Strony Jaison (jaison.pl)
Kompiluje projekt Vite oraz wdraża obraz kontenera Nginx na Google Cloud Run (europe-west1).
"""

import os
import subprocess
import sys

PROJECT_ID = "holistic-dashboard-dev"
REGION = "europe-west1"
SERVICE_NAME = "holisticjson-website"
IMAGE_TAG = f"gcr.io/{PROJECT_ID}/holisticjson-site:latest"

def run_command(cmd, desc=None, cwd=None):
    if desc:
        print(f"\n📌 {desc}...")
    print(f"Executing: {cmd}")
    
    # Run command and pipe output in real-time
    process = subprocess.Popen(
        cmd, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        text=True, 
        cwd=cwd, 
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
    print("🚀 DEPLOY STRONY JAISON.PL — GOOGLE CLOUD RUN (Vite + Nginx)")
    print("🧠 ===============================================")

    # Ścieżka do projektu Vite
    vite_dir = os.path.join(os.getcwd(), "01-jaison-core", "website", "site")
    if not os.path.exists(vite_dir):
        print(f"❌ Błąd: Nie znaleziono katalogu Vite: {vite_dir}")
        sys.exit(1)

    # Krok 1: Budowanie projektu Vite
    if not run_command("npm run build", "Krok 1: Kompilacja statycznej strony (Vite build)", cwd=vite_dir):
        print("❌ Błąd podczas budowania projektu Vite.")
        sys.exit(1)

    # Krok 2: Ustawienie projektu GCP
    if not run_command(f"gcloud config set project {PROJECT_ID}", "Krok 2: Ustawienie aktywnego projektu GCP"):
        print("❌ Nie udało się ustawić projektu GCP.")
        sys.exit(1)

    # Krok 3: Kompilacja i wysłanie obrazu Docker do Artifact Registry przez Cloud Build
    build_cmd = f"gcloud builds submit --tag {IMAGE_TAG} ."
    if not run_command(build_cmd, "Krok 3: Budowanie obrazu kontenera na Google Cloud Build", cwd=vite_dir):
        print("❌ Błąd podczas budowania obrazu w chmurze.")
        sys.exit(1)

    # Krok 4: Wdrożenie na Google Cloud Run
    deploy_cmd = (
        f"gcloud run deploy {SERVICE_NAME} "
        f"--image {IMAGE_TAG} "
        f"--platform managed "
        f"--region {REGION} "
        f"--port 80 "
        f"--allow-unauthenticated"
    )
    if not run_command(deploy_cmd, "Krok 4: Wdrażanie kontenera na Google Cloud Run"):
        print("❌ Wdrożenie na Cloud Run zakończyło się błędem.")
        sys.exit(1)

    # Krok 5: Wyświetlenie wyników
    print("\n" + "=" * 50)
    print("🎉 WDROŻENIE STRONY ZAKOŃCZONE SUKCESEM!")
    print("=" * 50)
    print(f"🔗 Strona główna agencji: https://jaison.pl")
    print(f"🔗 URL tymczasowy Cloud Run: https://holisticjson-website-771359551342.europe-west1.run.app")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()
