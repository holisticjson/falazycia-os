# 🤖 PROMPT KROK po KROKU dla COMET (Część 2)

> **Zastosowanie:** Skopiuj całą poniższą zawartość i wklej do agenta przeglądarkowego COMET w nowej sesji, aby dokończyć zbieranie screenshotów.

---

Jesteś asystentem dokumentacyjnym. Twoim zadaniem jest dokończenie zbierania screenshotów do e-booka o Google Cloud Platform (GCP).

### 🔑 PUNKT STARTOWY & KONTEKST
- Jesteś zalogowany na konto z parametrem `?authuser=3`.
- Aktywny projekt to: **My First Project**
- Przejdź na: `https://console.cloud.google.com/welcome?authuser=3`

---

## 📋 PLAN DZIAŁANIA DLA COMET

### ETAP 5: Cloud Shell & gcloud CLI (Kontynuacja)
1. **Otwórz Cloud Shell** klikając ikonę `>_` w prawym górnym rogu.
2. Zobaczysz modal z napisem **"Autoryzuj Cloud Shell"** (Authorize Cloud Shell). Kliknij niebieski przycisk **"Autoryzuj"** (Authorize).
3. Poczekaj na załadowanie terminala na dole ekranu.
4. **📸 Zrób screenshot**: `ETAP_05_KROK_01_cloud_shell_active.png` (widoczny załadowany terminal na dole).
5. Wpisz w terminalu i zatwierdź Enterem:
   ```bash
   gcloud config configurations list
   ```
6. **📸 Zrób screenshot**: `ETAP_05_KROK_02_config_list.png` (wynik z tabelą konfiguracji).
7. Wpisz w terminalu i zatwierdź Enterem:
   ```bash
   gcloud config configurations create profil-wlasny
   ```
8. **📸 Zrób screenshot**: `ETAP_05_KROK_03_config_create.png` (potwierdzenie utworzenia profilu).

---

### ETAP 8: Limity zapytań (Quotas)
1. W górnym pasku wyszukiwania wpisz: `Quotas` i kliknij **"Quotas & System Limits"** (w sekcji IAM & Admin).
2. **📸 Zrób screenshot**: `ETAP_08_KROK_01_quotas_page.png` (główna strona limitów).
3. W polu filtrowania tabeli wpisz i wyszukaj:
   `generate_content_requests_per_minute_per_project_per_base_model`
4. **📸 Zrób screenshot**: `ETAP_08_KROK_02_quotas_filtered.png` (przefiltrowane limity modeli Gemini).
5. Zaznacz pole wyboru (checkbox) przy dowolnym modelu Gemini (np. `gemini-2.5-flash` w regionie `us-central1`) i kliknij przycisk **"Edit Quotas"** u góry tabeli.
6. **📸 Zrób screenshot**: `ETAP_08_KROK_03_edit_quotas_form.png` (otwarty formularz edycji po prawej stronie).
7. Wpisz w nową wartość limitu: `120` oraz w polu Justification wpisz:
   ```
   Deployment of a production AI agent orchestration system. Increasing RPM prevents critical HTTP 429 errors during parallel task execution by asynchronous agents.
   ```
8. **📸 Zrób screenshot**: `ETAP_08_KROK_04_quotas_filled.png` (formularz z wpisanymi danymi, **NIE klikaj "Submit request"**).
9. Zamknij formularz edycji. Przejdź do zakładki **"Quota Adjuster"** (lub w menu po lewej / ustawieniach).
10. **📸 Zrób screenshot**: `ETAP_08_KROK_05_quota_adjuster.png` (widok konfiguracji Quota Adjuster).

---

### ETAP 9: Audyt kosztów — Czyszczenie zasobów
1. Wyszukaj lub przejdź do: **Compute Engine** → **Disks** (Dyski).
2. **📸 Zrób screenshot**: `ETAP_09_KROK_01_disks_list.png` (lista dysków, pokazująca kolumnę "In use by").
3. Wyszukaj lub przejdź do: **Cloud Storage** → **Buckets** (Zasobniki).
4. **📸 Zrób screenshot**: `ETAP_09_KROK_02_buckets_list.png` (lista bucketów).
5. Wyszukaj lub przejdź do: **Billing** → **Cost table** (Tabela kosztów) lub **Reports** (Raporty). Ustaw filtr czasu na ostatnie 30 dni.
6. **📸 Zrób screenshot**: `ETAP_09_KROK_03_cost_report.png` (raport kosztów z wykresem).

---

### ETAP 11: Vertex AI Model Garden & Studio
1. Wyszukaj i przejdź do: **Model Garden** (Vertex AI).
2. **📸 Zrób screenshot**: `ETAP_11_KROK_01_model_garden_overview.png` (główny panel Model Garden z kafelkami).
3. Kliknij na model **"Gemini"** (np. najnowszy Gemini Flash lub Pro).
4. **📸 Zrób screenshot**: `ETAP_11_KROK_02_gemini_model_detail.png` (strona modelu Gemini z przyciskiem "Open in Vertex AI Studio").
5. Kliknij **"Open in Vertex AI Studio"** (lub "Open in multimodal playground").
6. Wpisz testowy prompt: `Napisz krótki wiersz o chmurze obliczeniowej` i kliknij **"Submit"** (Wyślij).
7. **📸 Zrób screenshot**: `ETAP_11_KROK_03_vertex_studio_response.png` (widoczny wygenerowany tekst odpowiedzi).
8. W Vertex AI Studio przejdź do zakładki generowania obrazów (Imagen / Generate Image). Wpisz prompt: `A friendly robot waving hello, cartoon style` i wygeneruj.
9. **📸 Zrób screenshot**: `ETAP_11_KROK_04_imagen_generated.png` (wygenerowany obraz w interfejsie).

---

### ETAP BONUS: Discovery Engine i Agent Builder
1. Przejdź do **API Library** (Biblioteka API), wyszukaj **Discovery Engine API** i kliknij **Enable** (Włącz), jeśli nie jest włączone.
2. **📸 Zrób screenshot**: `ETAP_BONUS_KROK_01_discovery_engine.png` (potwierdzenie włączenia).
3. Wyszukaj i przejdź do **Agent Builder**.
4. **📸 Zrób screenshot**: `ETAP_BONUS_KROK_02_agent_builder_landing.png` (ekran powitalny Agent Builder).
5. Kliknij **"Create"** (lub "New App").
6. **📸 Zrób screenshot**: `ETAP_BONUS_KROK_03_create_agent.png` (pierwszy formularz wyboru aplikacji/agenta).
