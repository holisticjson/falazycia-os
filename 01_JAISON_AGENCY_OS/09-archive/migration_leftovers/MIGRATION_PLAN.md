# 🗺️ PLAN MIGRACJI ARCHITEKTURY SYSTEMOWEJ: HOLISTIC SILOS v2.0 (GLOBAL)
> **Rola:** Główny Architekt Infrastruktury (C-Level)
> **Zasada Nadrzędna:** ZERO RYZYKA UTRATY DANYCH (Zero Data-Loss Protocol)
> **Faza:** 1 - GLOBALNY AUDYT I PLANOWANIE (Do akceptacji przed wykonaniem)

Niniejszy plan rozszerza poprzednie założenia na **całą przestrzeń roboczą `C:\Aplikacje MVP\`**. Wszystkie dotychczasowe, płasko rozproszone katalogi (klienci, systemy SaaS, agencja, technologia) zostają zorganizowane w trzy absolutnie bezpieczne silosy dewelopersko-biznesowe, eliminując zjawisko przeciążenia poznawczego (*Context Overload*).

Kluczowa decyzja architektoniczna: **Baza wiedzy `02_knowledge_base` pozostaje nienaruszona na swoim dotychczasowym miejscu w głównym roocie.**

---

## 🏗️ 1. Docelowa Struktura Silosów (Global Target Tree)

Wszystkie zasoby w `C:\Aplikacje MVP\` zostaną zreorganizowane według poniższego, zunifikowanego drzewa docelowego:

```text
C:\Aplikacje MVP/
│
├── 📁 01_JAISON_AGENCY_OS/           # SILOS A: Wszystko dotyczące agencji i operacji własnych
│   ├── 📄 README.md                  # Reguły deweloperskie dla Silosu A (Local RAG)
│   ├── 📁 brand_and_identity/        # Stary 'Holistic Jason/01-jaison-core' (Branding, offers, ghostwriter)
│   ├── 📁 dashboard_and_core/        # Stary 'Holistic Jason/02-os-jaison' (Kod Streamlit, backend, silnik AI)
│   ├── 📁 content_factory/           # Stary 'Holistic Jason/03-social-media-factory' (Wideo pipeline)
│   ├── 📁 virtual_board/             # Stary 'Holistic Virtual Board' (Pliki i SOP-y dyrektorów AI)
│   ├── 📁 personal_finance/          # Stary 'Personal Finance Dashboard' (Zarządzanie finansami agencji)
│   ├── 📁 agency_knowledge/          # Stary 'Holistic Jason/06-knowledge' (RAG agencji)
│   ├── 📁 ops_and_tasks/             # Stary 'Holistic Jason/07-ops' (Zadania agencji i backlogi)
│   ├── 📁 deploy_and_infra/          # Stary 'Holistic Jason/08-deploy' (Deployment agencji)
│   └── 📁 archive/                   # Stary 'Holistic Jason/09-archive' (Archiwum agencji)
│
├── 📁 02_CLIENTS_AND_PROJECTS/       # SILOS B: Scentralizowani klienci zewnętrzni (Izolacja danych)
│   ├── 📄 README.md                  # Reguły deweloperskie dla Silosu B (Local RAG)
│   ├── 📁 Szablon_Projektu/          # Zunifikowany szablon onboardingowy
│   │   ├── 📄 README.md              # Reguły wdrażania u nowych klientów
│   │   ├── 📁 02_website/            # Strona www klienta, SEO, backupy
│   │   ├── 📁 04_assets/             # Logotypy, grafiki, multimedia klienta
│   │   ├── 📁 06_crm/                # Dane leadów, CRM, marketing klienta
│   │   └── 📁 07_deploy/             # Wdrożenia na hosting, DNS i FTP
│   ├── 📁 coolfon/                   # Przeniesiony klient Coolfon GSM
│   ├── 📁 kurczakujasia/             # Przeniesiony klient Bar Jaś (kurczakujasia.pl)
│   ├── 📁 smartrade_client/          # Przeniesiony klient Smartrade (z Holistic Jason/04-clients/smartrade)
│   ├── 📁 viptransporter/            # Przeniesiony klient VIP Transporter
│   ├── 📁 lifewave/                  # Przeniesiony klient Lifewave
│   ├── 📁 kantor_lombard_oranzada/   # Przeniesiony klient Kantor Lombard Oranżada
│   ├── 📁 vojsik_ai/                 # Przeniesiony zewnętrzny projekt 'Vojsik AI'
│   └── 📁 vojsik_mvp/                # Przeniesiony zewnętrzny projekt 'Vojsik MVP'
│
├── 📁 03_SOFTWARE_AND_APPS/          # SILOS C: Tworzone własne systemy, SaaS-y i oprogramowanie
│   ├── 📄 README.md                  # Reguły deweloperskie dla Silosu C (Local RAG)
│   ├── 📁 Hermes_Agentic_OS/         # Stary 'Hermes Agentic OS' (Serce Twojego AI OS)
│   ├── 📁 hermes-browser-extension/  # Stara wtyczka przeglądarki do Hermes OS
│   ├── 📁 hermes-web-ui/             # Stary interfejs webowy Hermes OS
│   ├── 📁 Amazon_Bedrock/            # Stary 'Amazon_Bedrock' (Integracje z AWS Bedrock)
│   ├── 📁 Android/                   # Stary 'Android' (Rozwiązania mobilne deweloperskie)
│   ├── 📁 GitHub/                    # Stary 'GitHub' (Wtyczki i kody deweloperskie)
│   ├── 📁 Holistyczny_Broker/        # Stary 'Holistyczny Broker' (Asynchroniczny broker danych)
│   ├── 📁 Smartrade_SaaS/            # Stary 'Smartrade' (Kod źródłowy aplikacji giełdowej SaaS)
│   └── 📁 Speech-to-Text/            # Placeholder na systemy transkrypcji mowy (Inkubator SaaS)
│
├── 📁 02_knowledge_base/             # Zewnętrzna baza wiedzy (POZOSTAJE NIENARUSZONA - Decyzja C-Level)
├── 📁 11_digital_product/            # Globalne cyfrowe produkty agencji (Zasada 6 - Pozostaje w roocie)
└── 📁 .agents/                       # Konfiguracje i reguły agentów AI (Antigravity/Roo)
```

---

## 📊 2. Globalne Mapowanie Migracji (Źródło ➔ Cel)

Poniższa tabela przedstawia bezpieczną ścieżkę relokacji każdego katalogu deweloperskiego na dysku `C:\Aplikacje MVP\`:

| Lp. | Obecny folder / plik | Docelowa lokalizacja w silosach | Rationale / Wyjaśnienie |
| :--- | :--- | :--- | :--- |
| **1** | `02_knowledge_base/` | `02_knowledge_base/` (**BEZ ZMIAN**) | Baza wiedzy i integracje GAS pozostają w roocie. |
| **2** | `Amazon_Bedrock/` | `03_SOFTWARE_AND_APPS/Amazon_Bedrock/` | Deweloperskie integracje z AWS trafiają do Silosu C. |
| **3** | `Android/` | `03_SOFTWARE_AND_APPS/Android/` | Środowisko mobilne trafia do Silosu C. |
| **4** | `GitHub/` | `03_SOFTWARE_AND_APPS/GitHub/` | Narzędzia deweloperskie lądują w Silosie C. |
| **5** | `Hermes Agentic OS/` | `03_SOFTWARE_AND_APPS/Hermes_Agentic_OS/` | Główny system AI OS trafia do Silosu C. |
| **6** | `Holistic Virtual Board/` | `01_JAISON_AGENCY_OS/virtual_board/` | SOP-y Wirtualnego Zarządu trafiają do Silosu A. |
| **7** | `Holistyczny Broker/` | `03_SOFTWARE_AND_APPS/Holistyczny_Broker/` | Broker danych jako aplikacja systemowa trafia do Silosu C. |
| **8** | `Personal Finance Dashboard/`| `01_JAISON_AGENCY_OS/personal_finance/` | Pulpit finansowy CFO zasila Silos A. |
| **9** | `Smartrade/` | `03_SOFTWARE_AND_APPS/Smartrade_SaaS/` | Kod źródłowy aplikacji giełdowej SaaS trafia do Silosu C. |
| **10** | `Vojsik AI/` | `02_CLIENTS_AND_PROJECTS/vojsik_ai/` | Dedykowany system klienta trafia do Silosu B. |
| **11** | `Vojsik MVP/` | `02_CLIENTS_AND_PROJECTS/vojsik_mvp/` | Dedykowany MVP klienta ląduje w Silosie B. |
| **12** | `hermes-browser-extension/` | `03_SOFTWARE_AND_APPS/hermes-browser-extension/` | Wtyczka deweloperska trafia do Silosu C. |
| **13** | `hermes-web-ui/` | `03_SOFTWARE_AND_APPS/hermes-web-ui/` | Kod panelu webowego ląduje w Silosie C. |
| **14** | `Holistic Jason/01-jaison-core/` | `01_JAISON_AGENCY_OS/brand_and_identity/`| Marka agencji zasila Silos A. |
| **15** | `Holistic Jason/02-os-jaison/` | `01_JAISON_AGENCY_OS/dashboard_and_core/`| Kod Streamlit Dashboardu agencji zasila Silos A. |
| **16** | `Holistic Jason/03-social-media-factory/`| `01_JAISON_AGENCY_OS/content_factory/`| Produkcja wideo agencji zasila Silos A. |
| **17** | `Holistic Jason/04-clients/` | `02_CLIENTS_AND_PROJECTS/` | Wszyscy dotychczasowi klienci trafiają do Silosu B. |
| **18** | `Holistic Jason/04-clients/smartrade/` | `02_CLIENTS_AND_PROJECTS/smartrade_client/`| Zmiana nazwy klienta, aby uniknąć konfliktu z SaaS. |

---

## 🔒 3. Globalne Protokoły Bezpieczeństwa "Zero Data-Loss"
Podczas wykonywania skryptu migracji zostaną zachowane rygorystyczne środki ostrożności:
1. **Transakcyjność przenoszenia:** Pliki są przenoszone bezpiecznie w blokach try-except. Logi są zapisywane w czasie rzeczywistym do `C:\Aplikacje MVP\migration_execution.log`.
2. **Ignorowanie plików systemowych:** Środowiska wirtualne `.venv` deweloperskie i konfiguracje systemowe nie ulegną uszkodzeniu.
3. **Pliki konfiguracyjne w root:** Pliki `.env`, `.gitignore`, `requirements.txt`, `WORKSPACE_MEMORY.md` zostają nienaruszone, aby zachować ciągłość działania.
4. **Rozdzielenie konfliktów nazw (Smartrade):** Klient `smartrade` zyskuje nazwę `smartrade_client` w Silosie B, natomiast kod autorskiego projektu giełdowego ląduje pod nazwą `Smartrade_SaaS` w Silosie C.

---

## 📐 4. Pliki README.md (Zasady Local RAG)
README wewnątrz silosów określają restrykcyjne reguły pracy pod-agentów AI (patrz plik [README.md](file:///C:/Aplikacje%20MVP/01_JAISON_AGENCY_OS/README.md) po migracji).
