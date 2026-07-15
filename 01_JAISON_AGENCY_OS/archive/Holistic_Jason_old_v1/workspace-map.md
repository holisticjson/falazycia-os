# 🗺️ Mapa Obszaru Roboczego — Holistic Jason 2.0 (Pristine Repo)

Witaj w nowym, krystalicznie czystym i w pełni zorganizowanym repozytorium **Holistic Jason**! Wszystkie pliki zostały chirurgicznie przeniesione do 10-katalogowej struktury głównej. Koniec z bałaganem w roocie i rozproszonymi skryptami.

---

## 📂 Struktura Główna (10 Root Folders)

### 📥 [00-inbox/](file:///C:/Aplikacje%20MVP/Holistic%20Jason/00-inbox/)
Miejsce na nowe, tymczasowe lub nieposortowane pobrane materiały i pliki źródłowe przed ich właściwą kwalifikacją.

### 🎯 [01-jaison-core/](file:///C:/Aplikacje%20MVP/Holistic%20Jason/01-jaison-core/)
Wszystko, co buduje Twoją markę osobistą i agencję AI **Jaison (jaison.pl)**:
*   `admin/` — Strategie wdrożenia, briefingi architektoniczne.
*   `brand/` — Pozycjonowanie marki, rebranding, identyfikacja wizualna.
*   `offers/` — Prezentacje, oferty handlowe i pitch-decki.
*   `ghost/` — Profil głosu Tomasza (Ghost v2), unikalne prompty NLP i copywriterskie.
*   `website/` — Kod źródłowy i zasoby strony agencyjnej `holisticjson.pl` / `jaison.pl`.

### 🖥️ [02-os-jaison/](file:///C:/Aplikacje%20MVP/Holistic%20Jason/02-os-jaison/)
Rdzeń technologiczny systemu **Hermes Agentic OS** oraz aplikacja Streamlit:
*   `src/` — Główne moduły, silnik AI, agenci i narzędzia asynchroniczne.
*   `dashboard/` — Interfejs graficzny Streamlit.
*   `integrations/` — Połączenia z n8n, Systeme.io, WooCommerce, WordPress.
*   `data/` — Pliki baz danych (np. `local_crm.db`).
*   `tokens/` — Tokeny autoryzacyjne OAuth, Gmail API (`token_holisticjason.pickle`).
*   `tests/` — Testy Selenium, jednostkowe, integracyjne i scenariusze.
*   **Skrypty w roocie `02-os-jaison/`:** `app.py`, `auth.py`, `webhook_api.py`, `smart_sorter.py`, `gcp_vertex_proxy.py`.

### 🎬 [03-social-media-factory/](file:///C:/Aplikacje%20MVP/Holistic%20Jason/03-social-media-factory/)
Fabryka Treści — automatyczny pipeline produkcji pionowego wideo (rolki, shorts) oraz postów social media:
*   `assets/` — Surowe materiały B-Roll, tła, ścieżki dźwiękowe.
*   `generated_media/` — Gotowe renderowania wideo, audio lektorów z GCP TTS.
*   `influencers/` — Bazy danych influencerów i profile twórców.
*   Pliki strategiczne: `social_media_strategy_and_planner.md`.

### 👥 [04-clients/](file:///C:/Aplikacje%20MVP/Holistic%20Jason/04-clients/)
Scentralizowany i odizolowany katalog obsługi wszystkich Twoich klientów:
*   `_client-template/` — **Sztywny, 10-folderowy szablon każdego nowego klienta** (`00-admin`, `01-brand`, `02-website`, `03-social`... `09-archive`).
*   `coolfon/` — Uporządkowany profil klienta Coolfon GSM.
*   `kurczakujasia/` — Pełna struktura wraz z kodem html strony Bar Jaś.
*   `smartrade/` & `viptransporter/` — Gotowe, puste i ustrukturyzowane katalogi pod onboarding.

### 📐 [05-templates/](file:///C:/Aplikacje%20MVP/Holistic%20Jason/05-templates/)
Gotowe szablony dokumentów wielokrotnego użytku pod dowożenie projektów (szablony audytów UX/SEO, brandbooków, struktur lejków Systeme.io).

### 🧠 [06-knowledge/](file:///C:/Aplikacje%20MVP/Holistic%20Jason/06-knowledge/)
Twoja centralna baza wiedzy (Brain Dump) zasilająca moduły RAG oraz Vertex AI Search:
*   `Obsidian_Vault/` — Notatki połączone semantycznie.
*   `research/` — Raporty rynkowe, analizy konkurencji, dokumentacje techniczne GCP/Vertex.

### ⚙️ [07-ops/](file:///C:/Aplikacje%20MVP/Holistic%20Jason/07-ops/)
Operacje, CRM i zarządzanie produktywnością:
*   `tasks/` — Zadania, lekcje wyciągnięte z projektów (`lessons.md`), backlogi.
*   `MASTER_GOALS.md` — Strategicze cele i kamienie milowe projektu.

### 🚀 [08-deploy/](file:///C:/Aplikacje%20MVP/Holistic%20Jason/08-deploy/)
Centrum wdrożeniowe i dokumentacja infrastruktury:
*   `deploy_old/` — Archiwalne skrypty wdrożeniowe i klucze.
*   Instrukcje GITHUB CI/CD, certyfikaty SSL, mapowanie domen i konfiguracje serwerów Nginx.

### 📦 [09-archive/](file:///C:/Aplikacje%20MVP/Holistic%20Jason/09-archive/)
Krypta historyczna: stare projekty (`Localo`), duplikaty, archiwalne wersje, eksperymenty, eksporty.

---

## 🛠️ Jak uruchamiać i wdrażać skrypty?

Trzy główne, aktywne skrypty wdrożeniowe pozostały w katalogu głównym repozytorium dla Twojej wygody:
1.  **[deploy_jason.py](file:///C:/Aplikacje%20MVP/Holistic%20Jason/deploy_jason.py)** — Wdraża stronę agencyjną na serwer FTP Hostido.
2.  **[deploy_cloud_run.py](file:///C:/Aplikacje%20MVP/Holistic%20Jason/deploy_cloud_run.py)** — Kompiluje Vite i wypycha kontener holisticjson.pl na GCP Cloud Run.
3.  **[build_and_deploy_v2.py](file:///C:/Aplikacje%20MVP/Holistic%20Jason/build_and_deploy_v2.py)** — Master build i FTP deploy dla `kurczakujasia.pl` (Bar Jaś).

*Wszystkie trzy skrypty zostały pomyślnie zaktualizowane o nowe ścieżki i zweryfikowane kompilacją.*

---

## 📜 Nowe Reguły Systemowe (Wewnątrz `.agents/rules/`)
Dodaliśmy 3 nowe, restrykcyjne reguły dla agentów AI, aby repozytorium na zawsze pozostało perfekcyjnie czyste:
1.  📄 **[folder-routing.md](file:///C:/Aplikacje%20MVP/Holistic%20Jason/.agents/rules/folder-routing.md)** — Blokuje tworzenie ad-hoc folderów w roocie.
2.  📄 **[client-isolation.md](file:///C:/Aplikacje%20MVP/Holistic%20Jason/.agents/rules/client-isolation.md)** — Wymusza 10-folderową strukturę u klientów i izolację ich danych.
3.  📄 **[safe-migration.md](file:///C:/Aplikacje%20MVP/Holistic%20Jason/.agents/rules/safe-migration.md)** — Definiuje protokół testów, kompilacji i rollbacku przy refaktoryzacji kodu.

---
*Repozytorium uporządkowane pomyślnie i przygotowane na najwyższy poziom automatyzacji AI!*
