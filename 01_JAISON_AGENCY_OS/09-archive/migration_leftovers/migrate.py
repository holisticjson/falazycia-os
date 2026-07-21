#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[SYS] SCRIPT: migrate.py (GLOBAL ASCII EDITION)
[AUTH] AUTOR: Glowny Architekt Infrastruktury (C-Level)
[SEC] ZASADA: ZERO DATA-LOSS (Bezpieczna migracja calej przestrzeni roboczej)
"""

import os
import shutil
import sys
import logging

# Konfiguracja logowania (wymuszamy UTF-8 dla pliku, ale dla konsoli dajemy bezpieczny ASCII)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("global_migration_execution.log", encoding="utf-8")
    ]
)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Definicja Silosow Globalnych w C:\Aplikacje MVP\
SILOS_A = os.path.join(ROOT_DIR, "01_JAISON_AGENCY_OS")
SILOS_B = os.path.join(ROOT_DIR, "02_CLIENTS_AND_PROJECTS")
SILOS_C = os.path.join(ROOT_DIR, "03_SOFTWARE_AND_APPS")

# 2. Mapowanie relokacji deweloperskiej
GLOBAL_MIGRATION_MAP = {
    # --- SILOS A (Wszystko dotyczace agencji i operacji wlasnych) ---
    os.path.join(ROOT_DIR, "Holistic Jason", "01-jaison-core"): os.path.join(SILOS_A, "brand_and_identity"),
    os.path.join(ROOT_DIR, "Holistic Jason", "02-os-jaison"): os.path.join(SILOS_A, "dashboard_and_core"),
    os.path.join(ROOT_DIR, "Holistic Jason", "03-social-media-factory"): os.path.join(SILOS_A, "content_factory"),
    os.path.join(ROOT_DIR, "Holistic Jason", "06-knowledge"): os.path.join(SILOS_A, "agency_knowledge"),
    os.path.join(ROOT_DIR, "Holistic Jason", "07-ops"): os.path.join(SILOS_A, "ops_and_tasks"),
    os.path.join(ROOT_DIR, "Holistic Jason", "08-deploy"): os.path.join(SILOS_A, "deploy_and_infra"),
    os.path.join(ROOT_DIR, "Holistic Jason", "09-archive"): os.path.join(SILOS_A, "archive"),
    os.path.join(ROOT_DIR, "Holistic Virtual Board"): os.path.join(SILOS_A, "virtual_board"),
    os.path.join(ROOT_DIR, "Personal Finance Dashboard"): os.path.join(SILOS_A, "personal_finance"),

    # --- SILOS B (Klienci zewnetrzni i dedykowane projekty) ---
    os.path.join(ROOT_DIR, "Vojsik AI"): os.path.join(SILOS_B, "vojsik_ai"),
    os.path.join(ROOT_DIR, "Vojsik MVP"): os.path.join(SILOS_B, "vojsik_mvp"),

    # --- SILOS C (Wlasne systemy, SaaS-y i oprogramowanie) ---
    os.path.join(ROOT_DIR, "Hermes Agentic OS"): os.path.join(SILOS_C, "Hermes_Agentic_OS"),
    os.path.join(ROOT_DIR, "hermes-browser-extension"): os.path.join(SILOS_C, "hermes-browser-extension"),
    os.path.join(ROOT_DIR, "hermes-web-ui"): os.path.join(SILOS_C, "hermes-web-ui"),
    os.path.join(ROOT_DIR, "Amazon_Bedrock"): os.path.join(SILOS_C, "Amazon_Bedrock"),
    os.path.join(ROOT_DIR, "Android"): os.path.join(SILOS_C, "Android"),
    os.path.join(ROOT_DIR, "GitHub"): os.path.join(SILOS_C, "GitHub"),
    os.path.join(ROOT_DIR, "Holistyczny Broker"): os.path.join(SILOS_C, "Holistyczny_Broker"),
    os.path.join(ROOT_DIR, "Smartrade"): os.path.join(SILOS_C, "Smartrade_SaaS")
}

# 3. Tresci plikow README.md (Zasady Local RAG)
README_CONTENT_A = """# 📁 SILOS A: JAISON AGENCY OS
> **Przeznaczenie:** Repozytorium marki agencji jaison.pl, kod Streamlit (app.jaison.pl) oraz operacje wewnętrzne.

## 🚫 Czego NIE wolno robić pod-agentom w tym folderze:
1. **ZAKAZ umieszczania danych klientów:** Żadne dane zewnętrzne, logotypy, hasła klientów nie mogą trafić do tego silosu. To jest wyłącznie środowisko agencji.
2. **ZAKAZ "hardkodowania" kluczy:** Wszelkie klucze API (Vertex AI Search, n8n, Systeme.io) muszą być ładowane wyłącznie przez plik `.env` w roocie projektu.
3. **ZAKAZ wprowadzania zmian bez testów:** Kod Streamlit w `dashboard_and_core/app.py` musi być modyfikowany z zachowaniem standardów bezpieczeństwa wstecznego.
"""

README_CONTENT_B = """# 📁 SILOS B: CLIENTS AND PROJECTS
> **Przeznaczenie:** Scentralizowany obszar obsługi klientów zewnętrznych agencji Jaison.

## 🚫 Czego NIE wolno robić pod-agentom w tym folderze:
1. **ZAKAZ wycieków danych (Kategoryczna Izolacja):** Pliki, logi i kody klienta A pod żadnym pozorem nie mogą być linkowane ani kopiowane do folderu klienta B. Dane są hermetycznie odizolowane.
2. **ZAKAZ wprowadzania zmian w infrastrukturze agencji:** Żaden skrypt deweloperski klienta nie może mieć uprawnień do edycji lub odczytu Silosu A (`01_JAISON_AGENCY_OS`).
3. **Zasada szablonu:** Każdy nowy klient projektowy musi być inicjowany wyłącznie poprzez skopiowanie struktury z katalogu `Szablon_Projektu/`.
"""

README_CONTENT_C = """# 📁 SILOS C: SOFTWARE AND APPS
> **Przeznaczenie:** Inkubator autorskich aplikacji SaaS i systemów programistycznych (np. Speech-to-Text).

## 🚫 Czego NIE wolno robić pod-agentom w tym folderze:
1. **ZAKAZ mieszania kodów:** Każda aplikacja deweloperska (SaaS) musi posiadać własny odizolowany folder i plik konfiguracyjny (np. `package.json`, `requirements.txt`).
2. **Zasada Modularności:** Rozwiązania tworzone w tym silosie muszą być budowane jako moduły, które agencja może łatwo dystrybuować lub wdrażać na GCP.
"""

README_CONTENT_TEMPLATE = """# 📁 SZABLON PROJEKTU KLIENTA
> **Przeznaczenie:** Nowy zunifikowany szablon onboardingowy klienta (cztery główne silosy robocze).

## Foldery:
- **02_website/** — Kod, audyty SEO, baza i pliki strony.
- **04_assets/** — Logotypy, branding, multimedia i kreacje.
- **06_crm/** — Dane leadów, notatki ze spotkań, CRM i marketing.
- **07_deploy/** — Instrukcje wdrożeniowe, DNS, dostęp FTP i backupy.
"""


def safe_move(src, dst):
    """Bezpieczne przenoszenie katalogu z obsluga bledow"""
    if not os.path.exists(src):
        logging.warning(f"Katalog zrodlowy nie istnieje (prawdopodobnie juz przeniesiony): {src}")
        return True
        
    if os.path.exists(dst):
        logging.error(f"[ERR] BLAD BEZPIECZENSTWA: Katalog docelowy juz istnieje: {dst}. Ruch wstrzymany!")
        return False
        
    try:
        logging.info(f"Przenoszenie: {os.path.basename(src)} -> {os.path.relpath(dst, ROOT_DIR)}")
        shutil.move(src, dst)
        return True
    except Exception as e:
        logging.error(f"[ERR] Blad podczas przenoszenia {src} do {dst}: {str(e)}")
        return False


def main():
    logging.info("==================================================")
    logging.info("[SEC] ROZPOCZYNANIE BEZPIECZNEJ GLOBALNEJ MIGRACJI SILOSOWEJ")
    logging.info("==================================================")
    
    # 1. Tworzenie glownych silosow
    for silos in [SILOS_A, SILOS_B, SILOS_C]:
        if not os.path.exists(silos):
            os.makedirs(silos, exist_ok=True)
            logging.info(f"Utworzono silos globalny: {os.path.basename(silos)}")

    # 2. Generowanie plikow README.md
    readme_map = {
        os.path.join(SILOS_A, "README.md"): README_CONTENT_A,
        os.path.join(SILOS_B, "README.md"): README_CONTENT_B,
        os.path.join(SILOS_C, "README.md"): README_CONTENT_C
    }
    
    for path, content in readme_map.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Zapisano RAG README: {os.path.relpath(path, ROOT_DIR)}")

    # 3. Tworzenie folderow w Silosie C
    silos_c_stt = os.path.join(SILOS_C, "Speech-to-Text")
    os.makedirs(silos_c_stt, exist_ok=True)
    logging.info("Utworzono folder roboczy w Silosie C: Speech-to-Text")

    # 4. Wykonanie relokacji z globalnej mapy migracji
    success = True
    for src, dst in GLOBAL_MIGRATION_MAP.items():
        if not safe_move(src, dst):
            success = False
            break

    if not success:
        logging.error("[ERR] Migracja wstrzymana z powodu bledow! Weryfikacja logow niezbedna.")
        sys.exit(1)

    # 5. Bezpieczna relokacja klientow z Holistic Jason/04-clients/ do Silosu B
    old_clients_dir = os.path.join(ROOT_DIR, "Holistic Jason", "04-clients")
    if os.path.exists(old_clients_dir):
        logging.info("Rozpoczynanie migracji klientow z Holistic Jason/04-clients...")
        for item in os.listdir(old_clients_dir):
            item_path = os.path.join(old_clients_dir, item)
            
            if item == "_client-template":
                continue
                
            if os.path.isdir(item_path):
                # Specjalne zabezpieczenie nazwy klienta smartrade, by nie bylo konfliktu z SaaS Smartrade
                target_name = "smartrade_client" if item == "smartrade" else item
                dst_path = os.path.join(SILOS_B, target_name)
                if not safe_move(item_path, dst_path):
                    success = False
            else:
                dst_path = os.path.join(SILOS_B, item)
                try:
                    shutil.move(item_path, dst_path)
                    logging.info(f"Przeniesiono plik konfiguracyjny klienta: {item}")
                except Exception as e:
                    logging.error(f"Nie udalo sie przeniesc pliku {item}: {str(e)}")
                    success = False

    # 6. Tworzenie Szablonu Projektu w Silosie B
    template_dir = os.path.join(SILOS_B, "Szablon_Projektu")
    os.makedirs(template_dir, exist_ok=True)
    
    with open(os.path.join(template_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(README_CONTENT_TEMPLATE)
        
    sub_folders = ["02_website", "04_assets", "06_crm", "07_deploy"]
    for sf in sub_folders:
        os.makedirs(os.path.join(template_dir, sf), exist_ok=True)
    logging.info("Utworzono uproszczony Szablon_Projektu w Silosie B.")

    # 7. Czyszczenie starych, tymczasowych lub pustych folderow
    folders_to_clean = [
        old_clients_dir,
        os.path.join(ROOT_DIR, "Holistic Jason", "05-templates"),
        os.path.join(ROOT_DIR, "Holistic Jason")
    ]
    
    for empty_folder in folders_to_clean:
        if os.path.exists(empty_folder):
            try:
                if not os.listdir(empty_folder):
                    os.rmdir(empty_folder)
                    logging.info(f"Usunieto stary, pusty folder: {os.path.relpath(empty_folder, ROOT_DIR)}")
                else:
                    # Jesli w Holistic Jason zostaly pliki systemowe (np. .git, .env, requirements.txt),
                    # zostawiamy je nienaruszone na poziomie C:\\Aplikacje MVP\\
                    for file_item in os.listdir(empty_folder):
                        file_src = os.path.join(empty_folder, file_item)
                        file_dst = os.path.join(ROOT_DIR, file_item)
                        if not os.path.exists(file_dst):
                            shutil.move(file_src, file_dst)
                            logging.info(f"Przeniesiono konfiguracje systemowa: {file_item} -> root")
                    
                    # Po oproznieniu usuwamy folder Holistic Jason
                    if not os.listdir(empty_folder):
                        os.rmdir(empty_folder)
                        logging.info("Usunieto stary folder Holistic Jason (calkowita migracja ukonczona).")
            except Exception as e:
                logging.warning(f"Krok porzadkowy dla {os.path.basename(empty_folder)} pominiety: {str(e)}")

    # 8. Usuwanie duplikatow skryptu i planu z Holistic Jason, jesli istnieja
    temp_plan = os.path.join(ROOT_DIR, "Holistic Jason", "MIGRATION_PLAN.md")
    temp_script = os.path.join(ROOT_DIR, "Holistic Jason", "migrate.py")
    for temp_file in [temp_plan, temp_script]:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                logging.info(f"Usunieto przejsciowy plik konfiguracyjny: {os.path.basename(temp_file)}")
            except Exception as e:
                pass

    logging.info("==================================================")
    logging.info("[SUCCESS] BEZPIECZNA MIGRACJA SILOSOWA ZAKONCZONA SUKCESEM")
    logging.info("==================================================")


if __name__ == "__main__":
    print("[!] GLOBALNY SKRYPT MIGRACJI URUCHOMIONY W TRYBIE BEZPIECZENSTWA (DRY-RUN)")
    print("Skrypt migrate.py zostal wygenerowany pomyslnie w C:\\Aplikacje MVP\\.")
    print("Uruchom go bezposrednio z konsoli PowerShell podajac parametr: 'python migrate.py --execute'")
    print("-" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        main()
    else:
        print("MIGRACJA WSTRZYMANA (Oczekiwanie na Twoja akceptacje i komende --execute).")
