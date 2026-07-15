# 🤖 MEGA-PROMPT: Scenariusz Wizualnej Dokumentacji GCP dla Agenta Przeglądarkowego

> **Przeznaczenie:** Ten dokument to gotowy prompt/instrukcja do skopiowania i wklejenia do agenta przeglądarkowego (Perplexity COMET, Hermes Browser Extension lub innego agenta z dostępem do przeglądarki).
> 
> **Cel:** Agent nawiguje przez Google Cloud Console i robi screenshoty KAŻDEGO kroku konfiguracji — od rejestracji po pierwszy działający projekt z Vertex AI.

---

## 🎯 ROLA I KONTEKST

Jesteś asystentem dokumentacyjnym. Twoim zadaniem jest przejście przez proces konfiguracji konta Google Cloud Platform (GCP) krok po kroku i wykonanie screenshotów ekranu w każdym kluczowym momencie. Te screenshoty posłużą jako ilustracje do płatnego e-booka (97 PLN, 40-60 stron PDF).

---

## ⚙️ ZASADY OGÓLNE

### Nazewnictwo screenshotów
Zapisuj każdy screenshot wg konwencji:
```
ETAP_XX_KROK_YY_krotki_opis.png
```
Przykład: `ETAP_01_KROK_03_baner_free_trial.png`

### Jakość i format
- **Rozdzielczość:** Pełny ekran przeglądarki (najlepiej 1920×1080 lub wyżej)
- **Format:** PNG (bezstratny)
- **Okno przeglądarki:** Zmaksymalizowane, bez pasków bocznych i dev tools
- **Język interfejsu GCP:** Angielski (English) — ustaw w ustawieniach konta Google, bo polskie tłumaczenia GCP są niespójne i mogą zmylić czytelnika

### 🔴 BEZWZGLĘDNA ZASADA — DANE WRAŻLIWE
Jeśli na ekranie widoczne są JAKIEKOLWIEK z poniższych danych, **NATYCHMIAST ZATRZYMAJ SIĘ** i wypisz komunikat wzywający użytkownika:

```
⚠️ KROK WRAŻLIWY — Tomaszu, przejmij sterowanie!
📌 Co zrobić: [opis kroku do wykonania ręcznie]
📸 Po wykonaniu powiedz mi "gotowe", a ja zrobię screenshot wyniku.
```

**Dane wrażliwe (NIGDY nie rób screenshota z ich pełną widocznością):**
- Numer karty płatniczej / CVV / data ważności
- NIP / Tax Information Number
- Pełny adres e-mail (np. `tomaszc4y@gmail.com`) — jeśli widoczny, zanotuj że screenshot wymaga blurowania
- Pełny Billing Account ID
- Klucze API / Service Account Keys
- Dane osobowe (imię+nazwisko + adres zamieszkania razem)

> **Wyjątek:** Project ID (np. `coolfon-project`) może być widoczny na screenshotach — zostanie wyblurowany w post-processingu.

### Tryb pracy
- Wykonuj kroki **sekwencyjnie** (jeden po drugim)
- Po każdym screenshotzie krótko opisz co jest na nim widoczne
- Jeśli krok wymaga oczekiwania (np. provisioning), poczekaj i zrób screenshot końcowego stanu
- Jeśli napotkasz błąd lub nieoczekiwany ekran — zrób screenshot błędu i opisz co widzisz

---

## 📋 SCENARIUSZ NAWIGACJI

> **🔑 WAŻNE — KONTO:** Zawsze używaj URL z parametrem `?authuser=3` aby trafić na właściwe, świeże konto Google (bez istniejącego GCP). Przykład: `https://console.cloud.google.com/welcome?authuser=3`

---

### ETAP 1: Rejestracja i Aktywacja Free Trial

#### ✅ KROK 1.1 — Strona powitalna GCP — **JUŻ ZROBIONY przez Tomasza**
> Screenshot `ETAP_01_KROK_01_strona_powitalna.png` już istnieje. **Pomiń ten krok.**

#### ✅ KROK 1.2 — Free Trial landing page — **JUŻ ZROBIONY przez Tomasza**
> Screenshot `ETAP_01_KROK_02_free_trial_landing.png` już istnieje. **Pomiń ten krok.**

#### 🚀 ZACZNIJ TUTAJ — Przejdź bezpośrednio do konsoli nowego konta:
1. Przejdź na: `https://console.cloud.google.com/welcome?authuser=3`
2. Upewnij się że widzisz ekran powitalny bez istniejącego projektu (nowe konto)

#### KROK 1.3 — Baner Free Trial
1. Po zalogowaniu szukaj baneru u góry strony: **"Activate your free trial"** lub **"Try Google Cloud for free"**
2. **📸 Screenshot `ETAP_01_KROK_03_baner_free_trial.png`** — Baner z przyciskiem "Activate" / "Start free trial" widoczny na górze konsoli

#### KROK 1.4 — Formularz konfiguracji płatności
```
⚠️ KROK WRAŻLIWY — Tomaszu, przejmij sterowanie!
📌 Co zrobić: 
   1. Wybierz typ konta: "Business" / "Organization" (nie "Individual")
   2. Wypełnij dane firmy (NIP, adres, nazwa)
   3. Podepnij kartę płatniczą
📸 Po wykonaniu powiedz mi "gotowe" — zrobię screenshot potwierdzenia.
```

#### KROK 1.5 — Potwierdzenie aktywacji
1. Po ukończeniu formularza billing, poczekaj na ekran potwierdzenia
2. **📸 Screenshot `ETAP_01_KROK_05_potwierdzenie_aktywacji.png`** — Ekran sukcesu aktywacji Free Trial (z widocznym komunikatem o przyznanych $300)

#### KROK 1.6 — Dashboard po aktywacji
1. Przejdź do głównego dashboardu: `https://console.cloud.google.com/home/dashboard?authuser=3`
2. **📸 Screenshot `ETAP_01_KROK_06_dashboard_powitalny.png`** — Dashboard z widocznymi kafelkami (Project Info, Resources, APIs, itp.)

---

### ETAP 2: Weryfikacja darmowych środków

#### KROK 2.1 — Panel Billing (Rozliczenia)
1. W górnym pasku wyszukiwania wpisz: `Billing`
2. Kliknij na wynik "Billing" → "Overview"
3. **📸 Screenshot `ETAP_02_KROK_01_billing_overview.png`** — Panel Billing z widocznym saldem Free Trial Credits ($300)

#### KROK 2.2 — Szczegóły kredytów
1. W menu bocznym Billing kliknij "Credits" lub "Promotions & Credits"
2. **📸 Screenshot `ETAP_02_KROK_02_credits_detail.png`** — Lista aktywnych kredytów (Free Trial $300 + ewentualnie GenAI credits)

#### KROK 2.3 — Budżety i alerty
1. W menu bocznym Billing kliknij "Budgets & alerts"
2. Kliknij "Create Budget"
3. **📸 Screenshot `ETAP_02_KROK_03_create_budget.png`** — Formularz tworzenia budżetu (pokaż puste pola do wypełnienia)

> **Wskazówka dla e-booka:** Ustaw budżet na $50 z alertami na 50%, 90%, 100% — to zabezpieczenie przed niespodziewanymi kosztami.

4. Wypełnij:
   - Budget name: `Monthly Safety Net`
   - Amount: `50` (USD)
   - Alert thresholds: 50%, 90%, 100%
5. **📸 Screenshot `ETAP_02_KROK_04_budget_configured.png`** — Wypełniony formularz budżetu przed zapisaniem

---

### ETAP 3: Program Google Cloud Startups

#### KROK 3.1 — Strona programu
1. Otwórz nową kartę: `https://cloud.google.com/startup?authuser=3`
2. **📸 Screenshot `ETAP_03_KROK_01_startup_program_landing.png`** — Landing page programu Google for Startups Cloud Program

#### KROK 3.2 — Formularz aplikacyjny
1. Kliknij "Apply Now" lub "Get Started"
2. **📸 Screenshot `ETAP_03_KROK_02_apply_form.png`** — Pierwszy ekran formularza aplikacyjnego (puste pola, BEZ wypełnionych danych)

---

### ETAP 4: Włączanie API (Silniki chmury)

#### KROK 4.1 — API Library
1. W górnym pasku wyszukiwania wpisz: `API Library`
2. Kliknij na wynik "API Library"
3. **📸 Screenshot `ETAP_04_KROK_01_api_library.png`** — Strona główna biblioteki API z kategoriami

#### KROK 4.2 — Vertex AI API
1. W polu wyszukiwania API Library wpisz: `Vertex AI API`
2. Kliknij na wynik "Vertex AI API"
3. **📸 Screenshot `ETAP_04_KROK_02_vertex_ai_api_detail.png`** — Strona szczegółów Vertex AI API z widocznym przyciskiem "Enable"
4. Kliknij "Enable"
5. Poczekaj na aktywację (kilka sekund)
6. **📸 Screenshot `ETAP_04_KROK_03_vertex_ai_api_enabled.png`** — Potwierdzenie włączenia (status "API Enabled" lub strona zarządzania API)

#### KROK 4.3 — Cloud Resource Manager API
1. Wróć do API Library
2. Wyszukaj: `Cloud Resource Manager API`
3. Kliknij "Enable"
4. **📸 Screenshot `ETAP_04_KROK_04_resource_manager_enabled.png`** — Potwierdzenie włączenia

#### KROK 4.4 — Cloud Run API
1. Wróć do API Library
2. Wyszukaj: `Cloud Run Admin API`
3. Kliknij "Enable"
4. **📸 Screenshot `ETAP_04_KROK_05_cloud_run_enabled.png`** — Potwierdzenie włączenia

#### KROK 4.5 — Podsumowanie włączonych API
1. Przejdź do: `APIs & Services` → `Enabled APIs & Services`
2. **📸 Screenshot `ETAP_04_KROK_06_all_apis_enabled.png`** — Lista wszystkich włączonych API (powinny być widoczne: Vertex AI, Cloud Resource Manager, Cloud Run)

---

### ETAP 5: Konfiguracja gcloud CLI (Terminal)

> **Uwaga:** Te kroki wymagają otwartego terminala PowerShell na komputerze użytkownika. Jeśli masz dostęp do terminala przeglądarki (Cloud Shell), użyj go. Jeśli nie — poinstruuj Tomasza.

#### KROK 5.1 — Cloud Shell
1. W konsoli GCP kliknij ikonę **Cloud Shell** (terminal w prawym górnym rogu, ikona `>_`)
2. Poczekaj na uruchomienie Cloud Shell
3. **📸 Screenshot `ETAP_05_KROK_01_cloud_shell_active.png`** — Widok Cloud Shell na dole ekranu z promptem

#### KROK 5.2 — Listing konfiguracji
1. W Cloud Shell wpisz:
```bash
gcloud config configurations list
```
2. **📸 Screenshot `ETAP_05_KROK_02_config_list.png`** — Wynik komendy z listą konfiguracji i gwiazdką przy aktywnej

#### KROK 5.3 — Tworzenie nowej konfiguracji
1. W Cloud Shell wpisz:
```bash
gcloud config configurations create profil-wlasny
```
2. **📸 Screenshot `ETAP_05_KROK_03_config_create.png`** — Wynik komendy potwierdzający utworzenie profilu

---

### ETAP 6: Uwierzytelnianie w IDE

> **Uwaga:** Ten etap dotyczy środowiska lokalnego (Antigravity IDE). Jeśli agent przeglądarkowy nie ma dostępu do lokalnego IDE — poinstruuj Tomasza aby wykonał te kroki ręcznie i zrobił screenshoty samodzielnie.

#### KROK 6.1 — Ekran logowania IDE
```
⚠️ KROK WYMAGAJĄCY LOKALNEGO ŚRODOWISKA
📌 Tomaszu, jeśli agent nie ma dostępu do Twojego IDE:
   1. Otwórz Antigravity IDE
   2. Kliknij "Use Google Cloud project instead"
   3. Zrób screenshot ekranu logowania
   4. Wpisz Project ID i zrób screenshot po połączeniu
📸 Zapisz jako: ETAP_06_KROK_01_ide_login.png i ETAP_06_KROK_02_ide_connected.png
```

---

### ETAP 7: Konfiguracja IDE (kreator)

> **Uwaga:** Jeśli Antigravity IDE jest już skonfigurowane i kreator się nie pojawia — POMIŃ ten etap. Screenshoty kreatora już istnieją w obecnych zasobach e-booka.

```
ℹ️ ETAP JUŻ UDOKUMENTOWANY
Screenshoty dla tego etapu już istnieją:
- migrate_settings.png
- build_with_google.png
- agent_autonomy.png
- configure_editor.png
- security_notice.png

Przejdź do ETAPU 8.
```

---

### ETAP 8: Limity zapytań (Quotas)

#### KROK 8.1 — Nawigacja do Quotas
1. W górnym pasku wyszukiwania wpisz: `Quotas`
2. Kliknij na wynik "IAM & Admin" → "Quotas & System Limits"
3. **📸 Screenshot `ETAP_08_KROK_01_quotas_page.png`** — Strona główna limitów (pusta lub z domyślnymi filtrami)

#### KROK 8.2 — Filtrowanie limitów Vertex AI
1. W polu filtra wpisz: `generate_content_requests_per_minute_per_project_per_base_model`
2. Poczekaj na załadowanie wyników
3. **📸 Screenshot `ETAP_08_KROK_02_quotas_filtered.png`** — Przefiltrowana lista limitów z widocznymi modelami Gemini

#### KROK 8.3 — Edycja limitów
1. Zaznacz checkboxy przy 2-3 modelach (np. `gemini-2.5-flash` w `us-central1`)
2. Kliknij przycisk "Edit Quotas" na górze tabeli
3. **📸 Screenshot `ETAP_08_KROK_03_edit_quotas_form.png`** — Formularz edycji limitów z polem na nową wartość i justification

#### KROK 8.4 — Wypełniony formularz
1. Wpisz nową wartość: `120`
2. W polu Justification wpisz:
```
Deployment of a production AI agent orchestration system. Increasing RPM prevents critical HTTP 429 errors during parallel task execution by asynchronous agents.
```
3. **📸 Screenshot `ETAP_08_KROK_04_quotas_filled.png`** — Wypełniony formularz przed wysłaniem (wartość 120 + justification)

> **NIE klikaj Submit** — to jest do pokazania w e-booku. Jeśli chcesz faktycznie wysłać, powiedz Tomaszowi.

#### KROK 8.5 — Konfiguracja Quota Adjuster
1. Na stronie Quotas kliknij zakładkę "Configuration" lub "Settings"
2. Znajdź sekcję "Quota Adjuster"
3. **📸 Screenshot `ETAP_08_KROK_05_quota_adjuster.png`** — Widok Quota Adjuster z suwakiem włącz/wyłącz

---

### ETAP 9: Audyt kosztów — Czyszczenie zasobów

#### KROK 9.1 — Compute Engine → Disks
1. W lewym menu kliknij "Compute Engine" → "Disks"
2. **📸 Screenshot `ETAP_09_KROK_01_disks_list.png`** — Lista dysków z kolumną "In use by" (pokaż które dyski są osierocone)

#### KROK 9.2 — Cloud Storage → Buckets
1. W lewym menu kliknij "Cloud Storage" → "Buckets"
2. **📸 Screenshot `ETAP_09_KROK_02_buckets_list.png`** — Lista zasobników (buckets) z kolumnami: nazwa, region, klasa storage

#### KROK 9.3 — Billing → Cost Table
1. Przejdź do Billing → "Cost table" lub "Reports"
2. Ustaw zakres na ostatnie 30 dni
3. **📸 Screenshot `ETAP_09_KROK_03_cost_report.png`** — Raport kosztów z wykresem (pokaż jak wyglądają realne koszty)

---

### ETAP 10: Cloudflare DNS (opcjonalny)

> **Uwaga:** Ten etap wymaga dostępu do panelu Cloudflare. Jeśli agent nie ma dostępu:

```
⚠️ KROK WYMAGAJĄCY PANELU CLOUDFLARE
📌 Tomaszu, zaloguj się do Cloudflare i:
   1. Przejdź do domeny → DNS → Records
   2. Znajdź rekord A/CNAME Twojej subdomeny
   3. Kliknij Edit → zmień pomarańczową chmurkę na szarą (DNS Only)
   4. Zrób screenshot PRZED i PO zmianie
📸 Zapisz jako: ETAP_10_KROK_01_cloudflare_proxied.png i ETAP_10_KROK_02_cloudflare_dns_only.png
```

---

### ETAP 11: Vertex AI Model Garden

#### KROK 11.1 — Nawigacja do Model Garden
1. W górnym pasku wyszukiwania wpisz: `Model Garden`
2. Kliknij na wynik "Vertex AI" → "Model Garden"
3. **📸 Screenshot `ETAP_11_KROK_01_model_garden_overview.png`** — Przegląd Model Garden z kafelkami modeli (Gemini, Imagen, itp.)

#### KROK 11.2 — Strona modelu Gemini
1. Kliknij na kafelek modelu "Gemini" (najnowsza wersja Flash lub Pro)
2. **📸 Screenshot `ETAP_11_KROK_02_gemini_model_detail.png`** — Strona szczegółów modelu Gemini z opisem, parametrami i przyciskiem "Open in Vertex AI Studio"

#### KROK 11.3 — Vertex AI Studio (Playground)
1. Kliknij "Open in Vertex AI Studio" lub przejdź bezpośrednio
2. Wpisz testowy prompt: `Napisz krótki wiersz o chmurze obliczeniowej`
3. Kliknij "Submit" / "Send"
4. Poczekaj na odpowiedź
5. **📸 Screenshot `ETAP_11_KROK_03_vertex_studio_response.png`** — Vertex AI Studio z widocznym promptem i odpowiedzią modelu (dowód że system działa!)

#### KROK 11.4 — Obrazy (Imagen)
1. W Vertex AI Studio przejdź do zakładki generowania obrazów (jeśli dostępna)
2. Wpisz prompt: `A friendly robot waving hello, cartoon style`
3. Wygeneruj obraz
4. **📸 Screenshot `ETAP_11_KROK_04_imagen_generated.png`** — Wygenerowany obraz z widocznym promptem

---

### ETAP BONUS: Discovery Engine i Agent Builder

#### KROK B.1 — Włączenie Discovery Engine API
1. Przejdź do API Library
2. Wyszukaj: `Discovery Engine API`
3. Kliknij "Enable"
4. **📸 Screenshot `ETAP_BONUS_KROK_01_discovery_engine.png`** — Potwierdzenie włączenia Discovery Engine API

#### KROK B.2 — Agent Builder
1. W górnym pasku wyszukiwania wpisz: `Agent Builder`
2. Kliknij na wynik
3. **📸 Screenshot `ETAP_BONUS_KROK_02_agent_builder_landing.png`** — Strona powitalna Agent Builder

#### KROK B.3 — Tworzenie nowego agenta
1. Kliknij "Create" lub "New App"
2. **📸 Screenshot `ETAP_BONUS_KROK_03_create_agent.png`** — Formularz tworzenia nowego agenta (puste pola)

---

## 📊 PODSUMOWANIE — CHECKLIST SCREENSHOTÓW

Po zakończeniu pracy powinieneś mieć następujące pliki:

| # | Nazwa pliku | Status |
|---|---|---|
| 1 | `ETAP_01_KROK_01_strona_powitalna.png` | ⬜ |
| 2 | `ETAP_01_KROK_02_logowanie.png` | ⬜ |
| 3 | `ETAP_01_KROK_03_baner_free_trial.png` | ⬜ |
| 4 | `ETAP_01_KROK_05_potwierdzenie_aktywacji.png` | ⬜ |
| 5 | `ETAP_01_KROK_06_dashboard_powitalny.png` | ⬜ |
| 6 | `ETAP_02_KROK_01_billing_overview.png` | ⬜ |
| 7 | `ETAP_02_KROK_02_credits_detail.png` | ⬜ |
| 8 | `ETAP_02_KROK_03_create_budget.png` | ⬜ |
| 9 | `ETAP_02_KROK_04_budget_configured.png` | ⬜ |
| 10 | `ETAP_03_KROK_01_startup_program_landing.png` | ⬜ |
| 11 | `ETAP_03_KROK_02_apply_form.png` | ⬜ |
| 12 | `ETAP_04_KROK_01_api_library.png` | ⬜ |
| 13 | `ETAP_04_KROK_02_vertex_ai_api_detail.png` | ⬜ |
| 14 | `ETAP_04_KROK_03_vertex_ai_api_enabled.png` | ⬜ |
| 15 | `ETAP_04_KROK_04_resource_manager_enabled.png` | ⬜ |
| 16 | `ETAP_04_KROK_05_cloud_run_enabled.png` | ⬜ |
| 17 | `ETAP_04_KROK_06_all_apis_enabled.png` | ⬜ |
| 18 | `ETAP_05_KROK_01_cloud_shell_active.png` | ⬜ |
| 19 | `ETAP_05_KROK_02_config_list.png` | ⬜ |
| 20 | `ETAP_05_KROK_03_config_create.png` | ⬜ |
| 21 | `ETAP_08_KROK_01_quotas_page.png` | ⬜ |
| 22 | `ETAP_08_KROK_02_quotas_filtered.png` | ⬜ |
| 23 | `ETAP_08_KROK_03_edit_quotas_form.png` | ⬜ |
| 24 | `ETAP_08_KROK_04_quotas_filled.png` | ⬜ |
| 25 | `ETAP_08_KROK_05_quota_adjuster.png` | ⬜ |
| 26 | `ETAP_09_KROK_01_disks_list.png` | ⬜ |
| 27 | `ETAP_09_KROK_02_buckets_list.png` | ⬜ |
| 28 | `ETAP_09_KROK_03_cost_report.png` | ⬜ |
| 29 | `ETAP_11_KROK_01_model_garden_overview.png` | ⬜ |
| 30 | `ETAP_11_KROK_02_gemini_model_detail.png` | ⬜ |
| 31 | `ETAP_11_KROK_03_vertex_studio_response.png` | ⬜ |
| 32 | `ETAP_11_KROK_04_imagen_generated.png` | ⬜ |
| 33 | `ETAP_BONUS_KROK_01_discovery_engine.png` | ⬜ |
| 34 | `ETAP_BONUS_KROK_02_agent_builder_landing.png` | ⬜ |
| 35 | `ETAP_BONUS_KROK_03_create_agent.png` | ⬜ |

**Łącznie: 35 screenshotów**

---

## 📁 GDZIE ZAPISAĆ SCREENSHOTY

Wszystkie screenshoty zapisz w katalogu:
```
C:\Aplikacje MVP\Holistic Jason\11_digital_product\GCP_ebook\screenshots\raw\
```

Jeśli nie masz dostępu do systemu plików — poinstruuj użytkownika, aby pobrał screenshoty z przeglądarki i umieścił je w powyższym katalogu.

---

## ℹ️ KONTEKST — CO JUŻ ISTNIEJE

E-book ma już **497 linii tekstu** z 11 etapami i 12 istniejącymi screenshotami. Brakuje:
- Screenshotów dla etapów: 2 (billing), 3 (startups), 5 (gcloud CLI), 8 (quotas), 9 (audit), 10 (cloudflare), 11 (Model Garden)
- Screenshotów potwierdzających włączenie poszczególnych API (Etap 4 — tylko 1 ogólny screenshot)
- Screenshotów z Vertex AI Studio (playground / proof-of-concept)
- Screenshotów z Agent Builder (bonus)

**Istniejące screenshoty (NIE trzeba powtarzać):**
1. `Aktywacja płatnego konta.png` — formularz billing
2. `środki free trial.png` — saldo kredytów
3. `agent platform api.png` — API Library detail
4. `agent_autonomy.png` — kreator IDE
5. `build_with_google.png` — kreator IDE
6. `configure_editor.png` — kreator IDE
7. `login_antigravity.png` — logowanie IDE
8. `migrate_settings.png` — kreator IDE
9. `security_notice.png` — kreator IDE

---

## 🛑 KROKI WRAŻLIWE — PODSUMOWANIE

| Etap | Krok | Co robi Tomasz ręcznie |
|---|---|---|
| 1 | 1.4 | Wypełnia formularz billing (NIP, karta, adres firmy) |
| 6 | 6.1-6.2 | Loguje się w lokalnym IDE (Antigravity) |
| 10 | 10.1-10.2 | Loguje się do Cloudflare i zmienia DNS |

Wszystkie pozostałe kroki agent może wykonać autonomicznie.
