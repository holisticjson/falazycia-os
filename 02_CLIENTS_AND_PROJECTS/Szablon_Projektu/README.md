# 📁 [NAZWA KLIENTA] - OS PROJEKTU
> **Właściciel:** Jaison Agency | **Status:** 🟢 Aktywny / 🟡 Onboarding / 🔴 Wstrzymany
> 
> *Ten plik README służy jako nawigacja GPS dla Ciebie (ADHD-friendly) oraz dla agentów AI AntiGravity.*

---

## 📊 STATUS PROJEKTU (Szybki Podgląd)
*Zaznacz `[x]` kiedy etap jest gotowy, aby zachować jasność umysłu.*
- [ ] **00-admin:** Audyt 21 pytań przeprowadzony i przeanalizowany.
- [ ] **00-admin:** Umowa podpisana, brief wypełniony, dostępy zebrane.
- [ ] **01-brand:** Archetyp marki określony, kolory i logo wgrane.
- [ ] **02-website:** Strona WWW / Dashboard Streamlit postawiony i zoptymalizowany.
- [ ] **03-social:** Kanały społecznościowe założone i połączone.
- [ ] **05-automation:** n8n zintegrowane (CRM -> Strona -> Powiadomienia).
- [ ] **06-crm:** Baza leadów działa, e-mail marketing (np. Systeme.io) ustawiony.

---

## 🗂️ STRUKTURA PROJEKTU (10 Zunifikowanych Silosów)

*Struktura numeryczna wymusza idealne sortowanie alfabetyczne i usuwa paraliż decyzyjny typu "gdzie zapisać ten plik".*

### [00-admin](file:///C:/Aplikacje%20MVP/02_CLIENTS_AND_PROJECTS/Szablon_Projektu/00-admin) — Administracja, Brief & Audyt 21 Pytań
- `21_questions_audit_template.md` — Obowiązkowy audyt biznesowy branży/niszy klienta przed startem prac deweloperskich.
- Notatki ze spotkań i wideorozmów (Call meetings).
- `credentials.md` (Zabezpieczone hasła i dostępy do hostingu, domen, WordPressa, GCP).

### [01-brand](file:///C:/Aplikacje%20MVP/02_CLIENTS_AND_PROJECTS/Szablon_Projektu/01-brand) — Tożsamość i Voice
- `tone_of_voice.md` — Instrukcje copywritingu, archetyp marki i zakazane sformułowania.
- Palety kolorów (HEX/HSL), wytyczne typograficzne.
- Logotypy w krzywych (SVG/PNG) oraz księga znaku (Brandbook).

### [02-website](file:///C:/Aplikacje%20MVP/02_CLIENTS_AND_PROJECTS/Szablon_Projektu/02-website) — Pliki i Kod Strony (WWW lub Dashboard Streamlit)
- **Dla projektów Streamlit:** Pełna modularna struktura aplikacji Pythona:
  - `app.py` — Główny punkt wejścia i wizualizacja Pętli Pamięci Agentów (`WORKSPACE_MEMORY.md`).
  - `pages/` — Wielostronicowe podstrony dashboardu (Multipage setup).
  - `components/` — Wizualne komponenty i niestandardowy kod HTML/CSS (Glassmorphism).
  - `core/` — Logika biznesowa, autoryzacja GCP, integracja Vertex AI i zapytania DB.
  - `utils/` — Funkcje pomocnicze, parsery, obliczenia matematyczne.
  - `data/` — Lokalne przechowywanie danych (np. plik bazy SQLite `clients.db` lub pliki JSON).
  - `.streamlit/` — Wizualna konfiguracja (`config.toml` - luksusowy dark mode) oraz sekrety lokalne (`secrets.toml` - klucze API chmury GCP).
  - `requirements.txt` — Lista pakietów Pythona.
- **Dla klasycznych stron:** Kod źródłowy (HTML/CSS/JS, Next.js) lub kopia zapasowa WordPressa.
- `seo_audit.md` — Raporty optymalizacji pod wyszukiwarki i roboty AI (GEO/AEO).

### [03-social](file:///C:/Aplikacje%20MVP/02_CLIENTS_AND_PROJECTS/Szablon_Projektu/03-social) — Media Społecznościowe
- Plany publikacji (Harmonogramy postów).
- Gotowe teksty i wątki (Threads) na LinkedIn, Twitter/X, Threads, FB.
- Scenariusze dynamicznych rolek (Reels), Shorts i wideo.

### [04-assets](file:///C:/Aplikacje%20MVP/02_CLIENTS_AND_PROJECTS/Szablon_Projektu/04-assets) — Biblioteka Mediów & Kreacji
- Surowe zdjęcia, grafiki, nagrania lektorskie i podkłady muzyczne.
- Gotowe kreacje reklamowe i materiały B-Roll.

### [05-automation](file:///C:/Aplikacje%20MVP/02_CLIENTS_AND_PROJECTS/Szablon_Projektu/05-automation) — Automatyzacje i Boty (n8n / Python)
- Eksporty JSON przepływów n8n (workflows).
- Skrypty botów konwersacyjnych, definicje webhooków i integracje API.
- Instrukcje integracji Cal.com, powiadomień WhatsApp, SMS czy systemów CRM.

### [06-crm](file:///C:/Aplikacje%20MVP/02_CLIENTS_AND_PROJECTS/Szablon_Projektu/06-crm) — Sprzedaż i Leady
- Baza danych kontaktowych / leadów (CSV/JSON/SQLite).
- Schematy lejków sprzedażowych, tagowania w CRM i ścieżki e-mail marketingu (np. Systeme.io).
- Gotowe szablony newsletterów, sekwencji powitalnych i follow-up.

### [07-deploy](file:///C:/Aplikacje%20MVP/02_CLIENTS_AND_PROJECTS/Szablon_Projektu/07-deploy) — Infrastruktura i DNS
- Rekordy DNS (Cloudflare), dane rejestracyjne domen.
- Instrukcje wdrożeniowe (FTP, SSH, GCP Cloud Run, VPS).
- Logi deployu oraz plany backupów (Disaster Recovery).

### [08-reports](file:///C:/Aplikacje%20MVP/02_CLIENTS_AND_PROJECTS/Szablon_Projektu/08-reports) — Analityka i Raporty
- Raporty Google Analytics 4 (GA4) / Google Search Console.
- Statystyki konwersji lejków sprzedażowych, raporty z automatyzacji n8n.
- Miesięczne i kwartalne zestawienia biznesowe przygotowywane dla klienta.

### [09-archive](file:///C:/Aplikacje%20MVP/02_CLIENTS_AND_PROJECTS/Szablon_Projektu/09-archive) — Archiwum
- Stare, wyłączone wersje plików, grafik oraz zdezaktywowane przepływy n8n.

---

## 🛠️ ARCHITEKTURA BAZY I SEKRETÓW STREAMLIT (Dla projektów JaiSON)

Kiedy aplikacja lub dashboard klienta jest budowany w technologii **Streamlit**, stosujemy ścisłe wytyczne dotyczące lokalizacji bazy danych i sekretów:

1. **Przechowywanie danych (Database):**
   * **Lokalna baza SQLite:** Plik bazy danych powinien być przechowywany wyłącznie w folderze `02-website/data/` pod nazwą `clients.db` (lub podobną).
   * **Baza w chmurze GCP (AlloyDB / Cloud SQL):** Dane konfiguracyjne połączeń (host, login, port) przechowujemy w pliku `02-website/.streamlit/secrets.toml`.
2. **Przechowywanie sekretów (Credentials & API Keys):**
   * **Lokalny plik `secrets.toml`:** Wszystkie lokalne sekrety i klucze API muszą znajdować się w `02-website/.streamlit/secrets.toml`. Plik ten musi być wpisany do `.gitignore`, aby NIGDY nie trafił do publicznego repozytorium GitHub.
   * **Klucz konta usługowego GCP (Service Account):** Jeśli aplikacja integruje się z Vertex AI lub RAG Engine, klucz w formacie JSON (`gcp-sa-key.json`) przechowujemy w `01_JAISON_AGENCY_OS/deploy_and_infra/gcp-sa-key.json` lub ładujemy bezpośrednio przez mechanizm Application Default Credentials (ADC) w systemie operacyjnym Windows.

---

## 🤖 WYTYCZNE DLA AGENTÓW ANTIGRAVITY (AI-SOP)
*Drogi agencie AntiGravity, podczas pracy w tym projekcie przestrzegaj bezwzględnie poniższych zasad:*

1. **Bezwzględny Porządek:** Nigdy nie twórz plików luzem w katalogu głównym. Każdy plik musi trafić do odpowiedniego silosu `00` - `09`.
2. **Aktualizacja README:** Po zakończeniu dużej fazy projektu (np. wdrożenie automatyzacji), zaktualizuj sekcję `📊 STATUS PROJEKTU` wpisując `[x]`.
3. **Dokumentacja Zmian:** Każda nowa automatyzacja w `05-automation` lub zmiana w kodzie `02-website` musi posiadać plik instrukcji/podsumowania (np. `05-automation/README.md`), aby użytkownik z ADHD mógł go zrozumieć w 30 sekund.
4. **Praca na gałęziach roboczych:** Zawsze proponuj zmiany za pomocą `New Worktree`, nazywając gałąź zgodnie z silosem, np. `website/seo-optimization` lub `automation/crm-integration`.

---

## 🧭 ZASADY ZARZĄDZANIA WORKTREE I GAŁĘZIAMI GIT (ADHD-Friendly)

Aby uniknąć chaosu w plikach i utraty koncentracji, stosujemy prosty model pracy z systemem AntiGravity:

1. **Jeden wątek = Jedna gałąź Git:**
   * Pracujesz nad marketingiem? Uruchamiasz konwersację jako `New Worktree` bazujący na `main` o nazwie `social/linkedin-posts`. Agent generuje pliki bezpośrednio w folderze `03-social`.
   * Pracujesz nad automatyzacją? `New Worktree` -> `automation/n8n-crm`. Agent koduje w `05-automation`.
2. **Brak stresu o nadpisanie zmian:** 
   Ponieważ każdy wątek ma swój własny folder `worktree` w tle, możesz mieć uruchomione 3 zadania naraz. Gdy agent skończy, robisz szybki przegląd (Review) i scalasz do `main`.
3. **Główna gałąź `main` to Twoja "Świętość":**
   Lokalne środowisko robocze (`Local`) trzymasz zazwyczaj na stabilnej gałęzi `main`. Dzięki temu pliki w Twoim głównym edytorze są zawsze czyste, działające i wolne od rozgrzebanej pracy w tle.
