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

    # Wczytywanie zmiennych środowiskowych z .env do wstrzyknięcia do Cloud Run
    env_vars = {}
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        print(f"\n📌 Wczytywanie konfiguracji z pliku .env: {env_path}")
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    # Usunięcie ewentualnych cudzysłowów
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    
                    if key in ["GCP_SERVICE_ACCOUNT_JSON", "GCP_PROJECT_AGENCY", "VERTEX_ENGINE_AGENCY"]:
                        env_vars[key] = val
                        print(f"✅ Wykryto zmienną: {key}")

    # Przygotowanie pliku YAML ze zmiennymi środowiskowymi (eliminuje problemy z ucieczką znaków w CLI)
    env_vars_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_env_vars.yaml")
    
    try:
        if env_vars:
            print(f"📌 Tworzenie tymczasowego pliku konfiguracyjnego YAML: {env_vars_file}")
            with open(env_vars_file, "w", encoding="utf-8") as f:
                for k, v in env_vars.items():
                    # Ucieczka pojedynczych cudzysłowów w standardzie YAML
                    escaped_v = v.replace("'", "''")
                    f.write(f"{k}: '{escaped_v}'\n")

        # Krok 4: Wdrożenie na Google Cloud Run
        deploy_cmd = (
            f"gcloud run deploy {SERVICE_NAME} "
            f"--image {IMAGE_TAG} "
            f"--platform managed "
            f"--region {REGION} "
            f"--port 8080 "
            f"--allow-unauthenticated"
        )
        
        if env_vars and os.path.exists(env_vars_file):
            deploy_cmd += f' --env-vars-file="{env_vars_file}"'

        if not run_command(deploy_cmd, "Krok 4: Wdrażanie kontenera na Google Cloud Run"):
            print("❌ Wdrożenie na Cloud Run zakończyło się błędem.")
            sys.exit(1)
            
    finally:
        # Bezpieczne sprzątanie i usunięcie tymczasowego pliku
        if os.path.exists(env_vars_file):
            print("🧹 Sprzątanie: Usuwanie tymczasowego pliku konfiguracyjnego YAML...")
            try:
                os.remove(env_vars_file)
            except Exception as e:
                print(f"⚠️ Nie udało się usunąć pliku tymczasowego: {e}")



    # Krok 5: Wyświetlenie wyników
    print("\n" + "=" * 50)
    print("🎉 WDROŻENIE STRONY ZAKOŃCZONE SUKCESEM!")
    print("=" * 50)
    print(f"🔗 Strona główna agencji: https://jaison.pl")
    print(f"🔗 URL tymczasowy Cloud Run: https://holisticjson-website-771359551342.europe-west1.run.app")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()
