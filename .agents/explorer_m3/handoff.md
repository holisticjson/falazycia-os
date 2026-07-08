# Raport Analizy Walidacji Kluczy i Obsługi Błędów (Milestone 3)

## 1. Observation (Obserwacje)

Podczas read-only audytu repozytorium zidentyfikowałem następujące pliki konfiguracyjne, moduły i pliki źródłowe powiązane z poświadczeniami zewnętrznych API:

### Plik `.env` (Lokalizacja: `c:\Aplikacje MVP\Holistic Jason\.env`)
Zawiera klucze API i zmienne środowiskowe, m.in.:
* `PEXELS_API_KEY` (Linia 1)
* `AWS_ACCESS_KEY_ID` (Linia 4), `AWS_SECRET_ACCESS_KEY` (Linia 5), `AWS_REGION` (Linia 6)
* `OPENROUTER_API_KEY` (Linia 8)
* `TAVILY_API_KEY` (Linia 9)
* `SERPER_API_KEY` (Linia 10)
* `HUNTER_API_KEY` (Linia 11)
* `REDDIT_CLIENT_ID` (Linia 12), `REDDIT_CLIENT_SECRET` (Linia 13)
* `HOSTIDO_FTP_HOST` (Linia 17), `HOSTIDO_FTP_USER` (Linia 18), `HOSTIDO_FTP_PASS` (Linia 19)
* `SYSTEME_IO_API_KEY` (Linia 21), `SYSTEME_IO_MCP_KEY` (Linia 22)
* `GCP_PROJECT_AGENCY` (Linia 25), `VERTEX_ENGINE_AGENCY` (Linia 26)
* `GCP_PROJECT_BROKER` (Linia 28), `VERTEX_ENGINE_BROKER` (Linia 29)
* `SYSTEME_IO_WEBHOOK_URL` (Linia 32)
* `PIXABAY_API_KEY` (Linia 35)

### Inne poświadczenia / pliki kluczy w workspace:
* Pliki Google Sheets / Gmail OAuth: `token_brokerholistic.pickle` oraz `token_holisticjason.pickle`
* Plik uwierzytelniania Google Cloud Service Account (GCP SA): `holistic-dashboard-dev-dea2c872139e.json` lub `holistic-broker-sa.json`
* Tokeny Social Media (wpisywane w UI i zapisywane do `.env`): `LINKEDIN_ACCESS_TOKEN`, `FACEBOOK_PAGE_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`, `TIKTOK_ACCESS_TOKEN`.

---

### Analiza obsługi błędów i brakujących kluczy w modułach:

#### A. GCP Vertex Proxy (`gcp_vertex_proxy.py`)
W liniach 120–124 następuje bezpośrednia próba wczytania klucza konta usługowego GCP:
```python
120:             if creds is None:
121:                 creds = service_account.Credentials.from_service_account_file(
122:                     SA_KEY_PATH,
123:                     scopes=['https://www.googleapis.com/auth/cloud-platform']
124:                 )
```
**Błąd:** Jeśli plik JSON nie istnieje, `SA_KEY_PATH` wynosi `None` (linia 91), co powoduje rzucenie wyjątku `TypeError` i w konsekwencji błąd HTTP 500 zwracany do systemu agentycznego/LiteLLM. Brak jest uprzedniego przechwycenia i przyjaznego komunikatu o brakującym pliku JSON.

#### B. Weryfikacja e-maili Hunter.io (`01_src\tools\hunter_client.py` i `app.py`)
Gdy brak klucza `HUNTER_API_KEY`, funkcja zwraca błąd tekstowy:
```python
16:     if not key:
17:         return {"success": False, "error": "Missing HUNTER_API_KEY in .env"}
```
W `app.py` w linii 5857 błąd ten jest wypisywany użytkownikowi jako surowy, czerwony komunikat Streamlit:
```python
5857:                             st.error(f"Błąd: {res['error']}")
```
**Błąd:** Komunikat `Missing HUNTER_API_KEY in .env` jest kryptotyczny i narusza Złotą Zasadę 6 (Zero Zagadek). Użytkownik nie otrzymuje instrukcji jak wygenerować ten klucz ani gdzie go wpisać.

#### C. Fakturowanie Fakturownia / Infakt (`app.py`)
Domyślny token to `demo_sandbox_token_123`. Gdy użytkownik klika przycisk wystawienia faktury z domyślnym tokenem, aplikacja w przypadku niepowodzenia (kod HTTP inny niż 200/201) wypisuje w linii 4049:
```python
4049:                     except Exception as ex:
4050:                         st.info("Tryb demonstracyjny: Wystawiono fakturę w trybie offline.")
4051:                         st.code(json.dumps(payload, indent=4, ensure_ascii=False), language="json")
4052:                         st.success("Test KSeF OK! Faktura przygotowana do wysłania do Krajowego Systemu e-Faktur.")
```
**Błąd:** Brak jest uprzedniego ostrzeżenia (amber warning card) informującego o tym, że system działa w trybie demonstracyjnym/offline ze względu na użycie klucza sandboxowego.

#### D. B-Roll Video Maker (`app.py` i `01_src\faceless_generator.py`)
Gdy brak kluczy Pexels i Pixabay, aplikacja rzuca błąd w linii 2429:
```python
2429:                                 st.error("❌ Brak kluczy API Pexels oraz Pixabay w pliku .env! Uzupełnij PEXELS_API_KEY lub PIXABAY_API_KEY.")
```
**Błąd:** Czerwony komunikat o błędzie zatrzymuje działanie i nie instruuje użytkownika jak pozyskać darmowe klucze do wyszukiwania wideo.

---

## 2. Logic Chain (Łańcuch Logiczny)

1. Aplikacja posiada wiele rozproszonych integracji z zewnętrznymi API (OpenRouter, Google Cloud Platform, Hunter.io, Reddit, Systeme.io, Fakturownia, platformy Social Media).
2. Brak scentralizowanego mechanizmu walidacji stanów kluczy powoduje, że błędy ich braku lub niepoprawności są zgłaszane dopiero w momencie uruchomienia danej funkcji (runtime), często w postaci surowych czerwonych kart `st.error` lub cichych fallbacków (jak w przypadku Fakturowni/Reddit).
3. Niektóre komponenty (np. serwer proxy w `gcp_vertex_proxy.py`) są podatne na awarie (TypeError / HTTP 500) w przypadku braku pliku konta usługowego JSON, co destabilizuje łączność z LLM.
4. Zgodnie z **Złotą Zasadą 6 (Zasada Proaktywnej Weryfikacji - Zero Zagadek)**, aplikacja powinna przed uruchomieniem potencjalnie wadliwej operacji zweryfikować obecność i poprawność klucza i zamiast surowego błędu wyświetlić estetyczną, żółtą kartę ostrzegawczą (Amber Warning Card) z instrukcją krok po kroku.
5. Aby zachować architektoniczną czystość i modularność, należy wdrożyć helper `01_src/tools/keys_validator.py`, który będzie zawierał pełną logikę walidacji i szablony kart instruktażowych w HTML/CSS (używających istniejących w `app.py` klas `.custom-card` oraz `.card-amber`).

---

## 3. Caveats (Zastrzeżenia)

* **Zakres testowania:** Nie wykonywano fizycznych połączeń do API w celu weryfikacji poprawności kluczy (aktywności sieciowej), ponieważ agent działa w trybie tylko do odczytu (read-only) i w sieciowym trybie `CODE_ONLY`.
* **Klucz ElevenLabs:** W pliku `.env` znajduje się wpis `ELEVENLABS_API_KEY`, ale po przeanalizowaniu kodu źródłowego potwierdzono, że nie jest on wykorzystywany w żadnym pliku `.py` (wykorzystywany jest darmowy `edge-tts` lub `gcp-tts`). W związku z tym klucz ten został zaklasyfikowany jako nieaktywny/niepotrzebny.

---

## 4. Conclusion (Plan Wdrożenia i Propozycja Zmian)

### Propozycja utworzenia nowego modułu: `01_src/tools/keys_validator.py`
Moduł ten będzie odpowiadał za:
1. Sprawdzanie obecności kluczy w pliku `.env` oraz ich weryfikację pod kątem wartości testowych (`mock`, `simulated`, `test`, `demo_sandbox_token_123`).
2. Sprawdzanie obecności wymaganych plików fizycznych (`.json` konta GCP, `.pickle` autoryzacji Gmail).
3. Definiowanie i renderowanie dedykowanych kart ostrzegawczych w HTML/CSS dla każdego modułu.

#### Proponowany kod helpera `keys_validator.py`:
```python
import os
from dotenv import load_dotenv
import streamlit as st

def check_credential_status(key_name, is_file=False, default_mock_values=None):
    """
    Zwraca status klucza/pliku: 'VALID', 'MOCK', lub 'MISSING'
    """
    load_dotenv()
    if is_file:
        paths = [
            os.path.join(os.getcwd(), key_name),
            os.path.expanduser(f"~/.hermes/keys/{key_name}"),
            os.path.expanduser(f"~/.hermes/{key_name}")
        ]
        if any(os.path.exists(p) for p in paths):
            return "VALID"
        return "MISSING"

    val = os.environ.get(key_name) or os.getenv(key_name)
    if not val:
        return "MISSING"
        
    mocks = ["simulated", "mock", "test", "your_", "placeholder"]
    if default_mock_values:
        mocks.extend(default_mock_values)
        
    if any(m in val.lower() for m in mocks):
        return "MOCK"
        
    return "VALID"

def render_warning_card(title, description, steps, link=None, link_text="Dokumentacja"):
    """
    Renderuje piękną, ADHD-friendly bursztynową kartę ostrzegawczą w stylu .custom-card .card-amber
    """
    steps_html = "".join([f"<li style='margin-bottom: 6px;'>{step}</li>" for step in steps])
    link_html = f"<p style='margin-top: 12px;'><a href='{link}' target='_blank' style='color: #38BDF8; font-weight: bold; text-decoration: none;'>🔗 {link_text}</a></p>" if link else ""
    
    st.markdown(f"""
    <div class="custom-card" style="border-left: 5px solid #F59E0B; background-color: #1E1B10; padding: 22px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);">
        <h4 style="color: #F59E0B; margin-top: 0; font-family: 'Outfit', sans-serif; display: flex; align-items: center; gap: 8px;">
            ⚠️ {title}
        </h4>
        <p style="color: #CBD5E1; font-family: 'Atkinson Hyperlegible', sans-serif; font-size: 0.95rem; line-height: 1.6;">
            {description}
        </p>
        <div style="background-color: #0F172A; padding: 15px; border-radius: 8px; border: 1px solid rgba(245, 158, 11, 0.2); margin-top: 12px;">
            <strong style="color: #E2E8F0; font-size: 0.9rem;">Instrukcja konfiguracji krok po kroku:</strong>
            <ol style="color: #94A3B8; font-size: 0.85rem; margin-top: 8px; padding-left: 20px; font-family: 'Atkinson Hyperlegible', sans-serif;">
                {steps_html}
            </ol>
        </div>
        {link_html}
    </div>
    """, unsafe_allow_html=True)
```

---

### Projekty i Makiety Kart Bursztynowych (Amber Cards):

#### 1. Karta dla Brakującego Pliku GCP Service Account (RAG / TTS / OCR)
* **Wyzwalacz:** Brak plików `.json` z kluczami konta usługowego w projekcie.
```python
def show_gcp_sa_warning():
    render_warning_card(
        title="Brak pliku uwierzytelniającego GCP Service Account JSON",
        description="Funkcje Google Cloud (Vertex AI Search, Text-to-Speech, OCR) wymagają pliku klucza konta usługowego w formacie JSON do poprawnego uwierzytelnienia połączeń.",
        steps=[
            "Zaloguj się do <b>Google Cloud Console</b>.",
            "Przejdź do zakładki <b>IAM & Admin -> Service Accounts</b>.",
            "Wybierz lub utwórz konto usługowe (np. <code>holistic-broker-sa</code>).",
            "Nadaj mu wymagane role, w tym <b>Vertex AI Agent Builder Admin</b> oraz <b>Storage Admin</b>.",
            "W zakładce <b>Keys</b> kliknij <b>Add Key -> Create new key</b> i wybierz typ <b>JSON</b>.",
            "Pobierz plik i zapisz go w głównym katalogu projektu jako: <code style='color:#38BDF8;'>holistic-dashboard-dev-dea2c872139e.json</code>."
        ],
        link="https://console.cloud.google.com",
        link_text="Przejdź do konsoli Google Cloud"
    )
```

#### 2. Karta dla Brakującego/Testowego Klucza Hunter.io
* **Wyzwalacz:** Status klucza `HUNTER_API_KEY` wynosi `MISSING` lub `MOCK`.
```python
def show_hunter_warning():
    render_warning_card(
        title="Brak lub nieaktywny klucz Hunter.io API",
        description="Wyszukiwanie domenowe i weryfikacja poprawności e-maili wymagają aktywnego klucza API Hunter.io. System obecnie działa w trybie symulacji z makietami danych.",
        steps=[
            "Wejdź na stronę <b>Hunter.io</b> i zarejestruj darmowe konto (otrzymasz 25 bezpłatnych zapytań/miesiąc).",
            "Przejdź do zakładki <b>API</b> w ustawieniach konta.",
            "Wygeneruj i skopiuj swój klucz API.",
            "Wklej go w pliku <code>.env</code> w linii: <code style='color:#38BDF8;'>HUNTER_API_KEY=twój_klucz</code> lub uzupełnij w ustawieniach na dole tej strony."
        ],
        link="https://hunter.io",
        link_text="Zarejestruj się na Hunter.io"
    )
```

#### 3. Karta dla Brakującego/Testowego Tokenu Fakturownia
* **Wyzwalacz:** Status klucza `FAKTUROWNIA_TOKEN` wynosi `MISSING` lub `MOCK` (wartość `demo_sandbox_token_123`).
```python
def show_fakturownia_warning():
    render_warning_card(
        title="Aktywny tryb demonstracyjny fakturowania (REST API Fakturownia)",
        description="Obecnie używasz domyślnego tokenu demonstracyjnego. Generowane faktury będą widoczne jedynie offline i nie zostaną wysłane do Twojego systemu księgowego ani Krajowego Systemu e-Faktur (KSeF).",
        steps=[
            "Zaloguj się na swoje konto w serwisie <b>Fakturownia.pl</b>.",
            "Przejdź do menu <b>Ustawienia -> Ustawienia konta -> Integracja -> Kody API</b>.",
            "Kliknij <b>Utwórz nowy kod</b> dla integracji REST.",
            "Skopiuj wygenerowany token.",
            "Zastąp domyślną wartość w <code>.env</code>: <code style='color:#38BDF8;'>FAKTUROWNIA_TOKEN=twój_token</code> i upewnij się, że subdomena w formularzu powyżej zgadza się z adresem Twojego konta."
        ],
        link="https://fakturownia.pl",
        link_text="Zaloguj się do Fakturowni"
    )
```

---

### Propozycja zmian w `gcp_vertex_proxy.py`:
Aby zapobiec awarii serwera proxy, należy dodać weryfikację klucza przed odświeżeniem tokena OAuth:
```python
# Zmiana w gcp_vertex_proxy.py (get_token)
def get_token():
    global active_token, token_expiry, creds
    if not SA_KEY_PATH:
        logger.error("Brak pliku klucza GCP Service Account! Niemożliwe odświeżenie tokenu OAuth.")
        # Zamiast błędu TypeError, zwracamy jasny opis błędu
        raise FileNotFoundError("GCP Service Account JSON key file was not found in any of the configured paths.")
```

---

## 5. Verification Method (Metoda Weryfikacji)

1. **Uruchomienie testów lokalnych:**
   Przed i po planowanych zmianach należy uruchomić zestaw testów projektu poleceniem:
   ```powershell
   .venv\Scripts\python -m pytest tests/
   ```
   Wszystkie testy (w tym integracje webhooków i scenariusze adversarialne) muszą zakończyć się sukcesem (`passed`).

2. **Weryfikacja zachowania w Streamlit:**
   * Zmień nazwę pliku `.env` na `.env.bak` i uruchom aplikację lokalnie. Zamiast surowych tracebaków lub błędów, na kartach powiązanych z zewnętrznymi API (np. zakładki Prospecting Hub, Finance, Vertex AI) powinny wyświetlić się wyżej zdefiniowane, żółte karty ostrzegawcze HTML.
