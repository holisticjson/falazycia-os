# Księga Postępowania (SOP): Hermes OS & Google Cloud Vertex AI

Ten dokument opisuje proces instalacji i integracji modeli LLM od Google (Gemini, Imagen, Veo) do systemu Hermes Agentic OS, wykorzystując platformę Vertex AI oraz LiteLLM jako most pośredniczący. Proces ten pozwala na ominięcie limitów, pełną kontrolę nad billingiem i bezproblemowe korzystanie z najnowszych modeli.

> [!IMPORTANT]
> **Dlaczego używamy LiteLLM?**
> Hermes domyślnie komunikuje się z API w standardzie OpenAI. Google Vertex AI posiada własny, odmienny format zapytań (SDK/REST). LiteLLM działa na serwerze Hermesa jako lokalny tłumacz na porcie 4000: odbiera standardowe zapytania od Hermesa i konwertuje je w locie na natywne wywołania Google Vertex AI autoryzowane plikiem JSON.

---

## FAZA 1: Konfiguracja Google Cloud Platform (GCP)

### 1. Przygotowanie Projektu i API
1. Zaloguj się do Google Cloud Console.
2. Utwórz nowy projekt (np. `hermes-ai-production`).
3. Aktywuj **Vertex AI API** dla tego projektu (sekcja "APIs & Services").
4. Upewnij się, że projekt ma podpięte aktywne konto bilingowe.

### 2. Utworzenie Konta Usługi (Service Account)
1. Przejdź do **IAM & Admin -> Service Accounts**.
2. Kliknij **Create Service Account**, nazwij je np. `hermes-vertex-agent`.
3. W sekcji przypisywania ról, dodaj rolę: **Vertex AI User** (`roles/aiplatform.user`).
   > [!WARNING]
   > Bez tej roli Vertex AI odrzuci wszystkie żądania z błędem `403 Forbidden` dla wszystkich modeli!
4. Po utworzeniu, kliknij w to konto -> zakładka **Keys** -> **Add Key** -> **Create new key** (wybierz typ **JSON**).
5. Pobierz plik JSON. Nikomu go nie udostępniaj — to klucz do Twojego budżetu AI.

---

## FAZA 2: Środowisko Linux (Serwer Hermesa)

Załóżmy, że Hermes OS jest już zainstalowany w katalogu domowym użytkownika (np. `/home/user/hermes-agent`).

### 1. Wgranie Klucza GCP
Prześlij pobrany wcześniej plik JSON na serwer, np. do `/home/user/gcp-sa-key.json`.

### 2. Instalacja LiteLLM i zależności Google
Hermes OS korzysta z menedżera pakietów `uv`. Musimy zainstalować serwer LiteLLM wraz z oficjalnymi bibliotekami Google'a, aby obsłużyć autoryzację.

```bash
# Wymuszenie czystej instalacji LiteLLM z dodatkiem Vertex AI
uv tool install litellm[proxy] --with google-cloud-aiplatform --force
```

> [!CAUTION]
> Jeśli pominiesz `--with google-cloud-aiplatform`, serwer Proxy w ogóle się nie uruchomi (lub wyrzuci błąd `No module named 'google'`).

### 3. Konfiguracja Routingu (litellm_config.yaml)
Utwórz plik `/home/user/litellm_config.yaml`. To tutaj "mapujemy" wewnętrzne nazwy modeli Hermesa na konkretne modele Google Cloud:

```yaml
model_list:
  # --- TEKST ---
  - model_name: hermes-fast
    litellm_params:
      model: vertex_ai/gemini-2.5-flash
      vertex_project: hermes-ai-production  # Zmień na swój ID projektu!
      vertex_location: us-central1
      vertex_credentials: /home/user/gcp-sa-key.json

  - model_name: hermes-think
    litellm_params:
      model: vertex_ai/gemini-2.5-pro
      vertex_project: hermes-ai-production
      vertex_location: us-central1
      vertex_credentials: /home/user/gcp-sa-key.json

  # --- OBRAZY ---
  - model_name: hermes-image
    litellm_params:
      model: vertex_ai/imagen-3.0-generate-001
      vertex_project: hermes-ai-production
      vertex_location: us-central1
      vertex_credentials: /home/user/gcp-sa-key.json

general_settings:
  disable_database: true
  master_key: sk-hermes-local # Lokalny klucz do komunikacji Hermes -> LiteLLM
```

---

## FAZA 3: Integracja z Hermesem

Hermes posiada własny plik konfiguracyjny w `~/.hermes/config.yaml`.
Musimy powiedzieć Hermesowi, aby **nie używał** wbudowanych fallbacków (jak OpenRouter) tylko zawsze uderzał do naszego lokalnego LiteLLM.

Edytuj `~/.hermes/config.yaml`:
```yaml
# Ważne: Zmieniamy z "custom" na "openai" aby wymusić natywny format zgodny z proxy!
provider: openai
model: hermes-fast

providers:
  openai:
    api_key: sk-hermes-local
    base_url: http://127.0.0.1:4000
```

> [!TIP]
> Dlaczego nie używamy `provider: custom`? Jeśli konfiguracja `custom` nie jest idealnie wpisana w wewnętrzny rejestr, Hermes często próbuje fallbackować zapytania do awaryjnego OpenRoutera. Podpinając się pod profil `openai`, wykorzystujemy najstabilniejszą ścieżkę kodu w Hermesie.

---

## FAZA 4: Uruchomienie i Automatyzacja

Aby system działał po restarcie maszyny, LiteLLM musi działać w tle przed uruchomieniem Hermesa.

### Prosty skrypt startowy (deploy.sh)
```bash
#!/bin/bash
# Zabijamy stary proces jeśli istnieje
pkill -f "litellm --config" || true

# Uruchamiamy LiteLLM w tle na porcie 4000
nohup uvx --python 3.12 --from litellm litellm \
    --config /home/user/litellm_config.yaml \
    --port 4000 > /home/user/litellm.log 2>&1 &

# Czekamy na załadowanie
sleep 10

# Restartujemy głównego Hermesa
systemctl --user restart hermes-gateway
```

## Troubleshooting (Rozwiązywanie problemów)

*   **Błąd 404 w LiteLLM**: Błędna nazwa modelu w `litellm_config.yaml`. Upewnij się, że korzystasz z prefiksu `vertex_ai/` oraz że dany model jest fizycznie dostępny w wybranym regionie (zazwyczaj `us-central1`).
*   **Błąd 403 Forbidden**: Wskazany klucz JSON działa, ale projekt GCP nie zezwala na dostęp. Brakuje roli `Vertex AI User` w zakładce IAM w Google Cloud Console.
*   **ACCOUNT_STATE_INVALID (401)**: Klucz JSON na serwerze nie pasuje do żadnego istniejącego konta (konto zostało usunięte w GCP lub sam klucz został unieważniony). Należy wygenerować nowy JSON.
*   **Hermes odpowiada "hermes-fast is not a valid model ID"**: Zapytanie wyciekło z serwera i trafiło do publicznego API (OpenRouter/OpenAI). Sprawdź `~/.hermes/config.yaml`, czy `base_url` na pewno wskazuje na `http://127.0.0.1:4000`.

---

## FAZA 5: Generowanie Wideo (Veo 2.0 / Vertex AI)

Ze względu na asynchroniczną naturę generowania wideo przez modele Veo (proces LRO - Long Running Operation), **nie używamy LiteLLM** do przesyłania żądań wideo. LiteLLM jest zoptymalizowany pod szybki ruch synchroniczny (tekst, obraz).

### Wykorzystanie natywnego SDK `google-genai`
Zamiast ręcznych zapytań REST API z użyciem biblioteki `requests` (co prowadziło do błędów 404 lub 403 przy próbie ręcznego odpytywania endpointów Google), system operacyjny Hermes wykorzystuje teraz **oficjalne SDK Google w środowisku Pythona (`google-genai`)** we wtyczce `vertex_media_nexus`.

### Pętla Polling (LRO)
Właściwa implementacja zakłada wywołanie asynchronicznego zadania generacji i odpytywanie Google o jego status:
1. Agent inicjuje zadanie za pomocą metody `client.models.generate_videos(...)`, która zwraca obiekt typu `Operation`.
2. Wewnątrz wtyczki działa pętla: `while not operation.done:`, odpytująca status co ok. 10 sekund.
3. Gdy `operation.done` ma status `True`, wygenerowane obiekty wideo odczytywane są ze ścieżki `operation.response.generated_videos`.
4. URI gotowego pliku (format `gs://...`) jest następnie parsowane w locie do publicznego adresu HTTPS (np. `https://storage.googleapis.com/...`), aby komunikator (np. Telegram) wyrenderował wideo jako natywny załącznik w oknie czatu, zamiast zwykłego tekstu.

> [!WARNING]
> Aktualizacje struktury obiektów Google: Dokumentacja SDK `google-genai` bywa agresywnie optymalizowana. W nowszych wersjach parametr konfiguracyjny to bezpośrednio `output_gcs_uri` jako `string` w obiekcie `GenerateVideosConfig`, a wyjściowe adresy URI czyta się pod atrybutem `.uri` (a nie `.gcs_uri`!). Wszelkie anomalie wymagają kontroli najnowszej rewizji dokumentacji paczki Pythona.
