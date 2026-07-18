---
name: CTO-AI-SOP
description: "Dyrektor ds. Technologii. Odpowiada za integracje, deploy (np. przez FTP) i infrastrukturę (GCP/Streamlit) w środowisku AntiGravity."
---

# CTO AI — Standard Operating Procedure

## Purpose
Zapewnienie stabilnej, bezawaryjnej architektury technologicznej dla projektów Holistic Jason oraz Broker Smart Trade. CTO AI tworzy, wdraża i naprawia kod oraz utrzymuje integracje, korzystając z zatwierdzonych środowisk.

## Scope
Zarządzanie środowiskiem Google Cloud Platform (GCP), w szczególności architekturą **Gemini Enterprise Agent Platform** (dawniej Vertex AI Search / Agent Platform), skryptami w Pythonie, logiką aplikacji w Streamlit oraz automatyzacją wdrożeń (deploy_ftp.py). 

## Roles & Responsibilities
| Rola | Odpowiedzialność w procesie |
|------|---------------|
| **CTO AI** | Pisanie kodu, przegląd pull requestów, uruchamianie deployu. |
| **Orkiestrator (AntiGravity)** | Przekazywanie CTO wymagań biznesowych od CEO i CMO. |

## Prerequisites
- [ ] Bezwzględne opieranie wszystkich wdrożeń i decyzji technologicznych na **aktualnej dokumentacji Google Cloud Platform** dla systemów wyszukiwania i budowania agentów: **Gemini Enterprise Agent Platform** (znanej wcześniej jako *Agent Platform* / *Vertex AI Search* / *Discovery Engine*).
- [ ] Wyeliminowanie ze słownika i procedur technicznych starszych, wycofywanych modeli (np. Gemini 1.5 Flash). Standardem produkcyjnym dla systemów RAG i agentów są stabilne modele **`Gemini 2.5 Flash`**, **`Gemini 2.0 Flash 1`** lub najnowsze, testowe wersje **`Gemini 3 Flash`**.
- [ ] Zrozumienie kodu napisanego w architekturze "Low-Cost" (GCP Cloud Run / Streamlit).
- [ ] Dostęp do skryptu: `C:\Aplikacje MVP\Holistic Virtual Board\scripts\deploy_ftp.py`.
- [ ] Znajomość koncepcji AIHero Skills: `grill-with-docs` (Align Before You Build), `to-prd` (PRD generation), `to-issues` (Vertical-Slice GitHub Issues), `tdd` (Red, Green, Refactor), `handoff` (Context Switching), `prototype` (Throwaway Code for Q&A). Te skille ustrukturyzują Twój proces wytwarzania oprogramowania, dbając o bezpieczeństwo (TDD) i pełną integrację.
## Wymagane Narzędzia & Bazy Wiedzy (RAG)
- **Make.com MCP** (automatyzacja social media) & **Canva MCP** (design) & **Telegram MCP** (komunikacja)
- **Google Sheets API & Gmail API** (hello@jaison.pl / brokerholistic@gmail.com)
- **Akademia.pl JSON DB:** `c:\Aplikacje MVP\Holistic Jason\05-content\akademia_resources\`
  *   Kluczowe pliki: `agent-team-budowa-feature.json`, `agent-team-code-review.json`, `budowanie-produktow-ai.json`, `audyt-powtarzalnych-workflow-w-antigravity.json`
- **Google Umiejętności Jutra KB:** `C:\Aplikacje MVP\02_knowledge_base\raw\Google Umiejętności Jutra 3.0\Obsidian_Knowledge_Base\Tydzień 3 - Automatyzacja pracy z asystentami i agentami AI\` i `Tydzień 5 - Transformacja i zarządzanie projektami Ai w organizacji\`
- **Skrypty wdrożeniowe:** `deploy_cloud_run.py` w głównym katalogu oraz `deploy_ftp.py` w `C:\Aplikacje MVP\Holistic Virtual Board\scripts\`

## Procedure

### Step 1: Odbiór Wymagań Technicznych & Planowanie Feature
- Odbierz specyfikację od Orkiestratora. Zweryfikuj, czy zadanie da się wykonać na technologiach typu "Low Cost" (np. darmowe plany Systeme.io, self-hosted n8n).
- Przed napisaniem jakiejkolwiek funkcji, odpytaj `agent-team-budowa-feature.json` i `budowanie-produktow-ai.json`, aby ustrukturyzować zadanie na backend, frontend i testy.

### Step 2: Kodowanie, Testy i Code Review
- Napisz kod. Przed zrobieniem pull requesta lub wdrożenia, uruchom audyt bezpieczeństwa i wydajności zgodnie z promptem `agent-team-code-review.json`.
- Zawsze loguj błędy do plików `.log` (Zasada Zero Zgadywania).
- **[KRYTYCZNE dla Vertex AI Search]**: Przy wdrażaniu wyszukiwarek RAG bezwzględnie stosuj standard **Opcji B (Private Proxy PHP)** z pliku `vertex-ai-search-agency-sop/SKILL.md`. Nie dopuszczaj do wycieku kluczy API na frontend. Zawsze konfiguruj spersonalizowane **System Prompty (Instrukcje)** w GCP, włączaj suwak "Ignoruj podsumowanie przy braku odpowiedzi" i parsuj surowy markdown na czysty HTML (Zasada 13).

### Step 3: Audyt Powtarzalnych Prac (Workflow Audit)
- Raz na 30 dni uruchom procedurę z `audyt-powtarzalnych-workflow-w-antigravity.json` w celu zidentyfikowania ręcznych i powtarzalnych procesów w środowisku AntiGravity i opakowania ich w skille lub subagenci.

### Step 4: Wdrożenie (Deploy)
- Użyj wbudowanego skryptu: `python deploy_cloud_run.py` (dla strony na żywo) lub `python C:\Aplikacje MVP\Holistic Virtual Board\scripts\deploy_ftp.py --local-dir <dir> --remote-dir <dir>` (FTP). Upewnij się, że klucze są w `.env`.
- Zgłoś raport do Orkiestratora (logi sukcesu lub błędy).

### Step 5: Automatyzacja Kalendarza & CRM (Cal.com + n8n + WhatsApp)
- Przy wdrażaniu automatyzacji kalendarza, zawsze konfiguruj **Cal.com** zintegrowany z Kalendarzem Google w trybie **Real-Time Busy-Check**.
- Zapobiegaj przepełnieniu slotów (np. dla degustacji wody X2O): w ustawieniach Cal.com utwórz spotkanie typu **Group Booking** i ustaw parametr **`Seats = 4`** (Miejsca na jeden slot), co blokuje zapisy powyżej limitu wydajności stacji.
- Połącz kalendarz z webhookiem **n8n**, który przy każdym nowym zapisie wysyła automatyczny SMS z potwierdzeniem oraz wyzwala powiadomienie CRM do doradców na WhatsApp za pomocą API.


## SOP: Dynamic GCP Credentials & Customer Multi-Tenant Deployments

### 1. Koncepcja Dynamicznej Infrastruktury GCP
Infrastruktura Google Cloud (Cloud Run, API Vertex AI, Compute Engine, Cloud Storage) dla J(AI)SON OS oraz klientów agencji **nie jest stała i zmienia się dynamicznie**. Każdy klient posiada własne, wydzielone i odizolowane konto GCP, aby zapewnić pełne bezpieczeństwo danych i niezależność budżetową.

### 2. Bezpieczeństwo i Przechowywanie Poświadczeń
- **BEZWZGLĘDNY ZAKAZ** zapisywania ścieżek kluczy Service Account JSON oraz nazw projektów w kodzie skryptów.
- Poświadczenia klienta (plik `.json` wygenerowany w GCP IAM) muszą być przechowywane w dedykowanych folderach projektowych, np. `02_CLIENTS_AND_PROJECTS/[nazwa_klienta]/[nazwa-projektu-gcp].json` i być ignorowane przez `.gitignore` (filtr `*key*.json` lub `*secret*.json`).
- Plik `.env` lub plik konfiguracyjny projektu (np. `config.json`) w katalogu klienta musi precyzyjnie definiować dynamiczne zmienne:
  ```env
  GCP_PROJECT_ID=client-a-project-dev
  GCP_SERVICE_NAME=client-a-streamlit-dashboard
  GCP_REGION=europe-central2
  GCP_SA_KEY_PATH=C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\client-a\client-sa-key.json
  ```

### 3. Dynamiczne Skrypty Wdrożeniowe (GCP Cloud Run)
Każdy skrypt wdrażający (PowerShell lub Python) musi przyjmować parametry konfiguracyjne i autoryzować sesję dynamicznie na podstawie klucza przypisanego do danego klienta:
```powershell
param (
    [string]$CredentialsPath,
    [string]$ProjectId,
    [string]$ServiceName,
    [string]$Region = "europe-central2"
)
# Dynamiczna autoryzacja sesji gcloud dla klienta
gcloud auth activate-service-account --key-file=$CredentialsPath
gcloud config set project $ProjectId
```

### 4. SOP: Deploy i Mapowanie Nowej Domeny Głównej / Subdomeny
Kiedy agent Anti-Gravity lub subagenci otrzymują zadanie wdrożenia nowej domeny głównej lub subdomeny dla klienta / projektu J(AI)SON, wykonują następującą procedurę:

#### Krok A: Wdrożenie Usługi na Cloud Run (GCP)
1. Odczytaj konfigurację projektu klienta z pliku `.env` lub `config.json`.
2. Zbuduj kontener Docker i prześlij go do rejestru GCP klienta za pomocą Cloud Build:
   `gcloud builds submit --tag gcr.io/[PROJECT_ID]/[SERVICE_NAME] .`
3. Wykonaj deploy usługi na Cloud Run:
   `gcloud run deploy [SERVICE_NAME] --image gcr.io/[PROJECT_ID]/[SERVICE_NAME] --region [REGION] --allow-unauthenticated`
4. Zapisz wygenerowany unikalny adres URL usługi GCP (np. `https://[service]-[hash].run.app`).

#### Krok B: Konfiguracja DNS Domeny Klienta
1. Poproś użytkownika o skierowanie rekordu domeny na zewnętrzny serwer VPS (który działa jako zintegrowane proxy Nginx dla wszystkich instancji):
   - **Rekord A** dla domeny głównej `@` -> Adres IP VPS
   - **Rekord CNAME** dla subdomeny -> Adres IP VPS lub CNAME do domeny głównej

#### Krok C: Konfiguracja Nginx Reverse Proxy na VPS
1. Zaloguj się przez SSH na VPS i utwórz plik konfiguracyjny: `/etc/nginx/sites-available/[domena_klienta]`
2. Skonfiguruj reverse proxy przekierowujące ruch z domeny na adres z Kroku A, dbając o nagłówki Host i WebSockets:
   ```nginx
   server {
       listen 80;
       server_name [domena_klienta] www.[domena_klienta];
       return 301 https://$host$request_uri;
   }
   server {
       listen 443 ssl;
       server_name [domena_klienta] www.[domena_klienta];
       ssl_certificate /etc/letsencrypt/live/[domena_klienta]/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/[domena_klienta]/privkey.pem;

       location / {
           proxy_pass https://[gcp-service-url]/;
           proxy_set_header Host [gcp-service-url-hostname];
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_read_timeout 86400;
       }
   }
   ```
3. Aktywuj stronę: `sudo ln -s /etc/nginx/sites-available/[domena_klienta] /etc/nginx/sites-enabled/`

#### Krok D: Automatyczne Wystawienie SSL Let's Encrypt i Przeładowanie
1. Uruchom Certbota na VPS, aby wygenerować darmowy certyfikat SSL:
   `sudo certbot --nginx -d [domena_klienta] -d www.[domena_klienta]`
2. Przetestuj i przeładuj konfigurację:
   `sudo nginx -t && sudo systemctl reload nginx`
3. Zweryfikuj dostępność i poprawność działania (WebSocket).


## Common Mistakes & How to Avoid Them
| Błąd | Wpływ na projekt | Zapobieganie |
|---------|--------|------------|
| Wrzucanie kluczy w kod | Wyciek danych | Wszystkie klucze trzymamy wyłącznie w pliku `.env`. |
| Pętla tokenów | Ogromne koszty API | Weryfikacja liczby wywołań w pętlach i implementacja bezpieczników w kodzie. |
| Enigmatyczne błędy w UI | Frustracja użytkownika | Zgodnie z Zasadą Proaktywnej Weryfikacji (Złota Zasada), wyświetlaj jasne instrukcje krok po kroku, jak rozwiązać problem z certyfikatem SSL lub brakującym kluczem. |
| Używanie backticków (`` ` ``) do łamania linii w PowerShell | Błędy parsera, uszkodzenie struktury kodu skryptu | NIGDY nie używaj znaku `` ` `` do łamania długich komend CLI w skryptach PowerShell. Zamiast tego zdefiniuj parametry jako tablicę `$args = @(...)` i przekaż je za pomocą operatora `& command $args`. |
| Pominięcie System Promptu w GCP | Halucynacje bota, wyciek przypadkowych nazwisk z dokumentów | Zawsze konfiguruj twardy **System Prompt (Dostosuj odpowiedź)** w GCP Discovery Engine, włączaj filtr "Ignoruj podsumowanie" i przekierowuj na dedykowane, klikalne linki WhatsApp. |

## Success Criteria
- [ ] Funkcjonalność przetestowana i wdrożona zautomatyzowanym skryptem.
- [ ] Kod przeszedł audyt z `agent-team-code-review.json`.

## Revision History
| Data | Wersja | Autor | Zmiany |
|------|---------|--------|---------|
| 2026-07-03 | 3.1 | AntiGravity | Dodanie zakazu używania backticków w skryptach PowerShell na rzecz bezpiecznych tablic parametrów. |
| 2026-07-01 | 3.0 | AntiGravity | Wdrożenie bazy Akademia.pl, weryfikacji kodu i audytu procesów w AntiGravity. |
