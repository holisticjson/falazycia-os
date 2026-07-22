
# Streamlit + Google Business Profile API — autoryzacja krok po kroku

Ten dokument pokazuje, jak poprawnie podpiąć dashboard Streamlit do Google Business Profile API w sposób zgodny z dokumentacją Google i wygodny operacyjnie dla J(AI)SON. Najbezpieczniejsza i właściwa metoda to OAuth 2.0 z kontem Google, które ma dostęp do danej wizytówki. Google wymaga OAuth 2.0 tokena do dostępu i modyfikacji danych lokalizacji. [web:145][web:146][web:157][web:141]

## 1. Dlaczego OAuth, a nie service account

Google Business Profile API działa na danych powiązanych z kontem użytkownika i profilami lokalizacji, dlatego standardową metodą jest OAuth 2.0. Dokumentacja Google opisuje konfigurację OAuth dla Business Profile APIs, a także wymagania wstępne: utworzenie projektu, włączenie API i uzyskanie dostępu. [web:145][web:146][web:157]

Service account nie jest zwykle właściwą metodą do klasycznego zarządzania GBP w imieniu właściciela wizytówki; praktycznie trzeba uwierzytelnić użytkownika Google, który ma uprawnienia do profilu. [web:145][web:158][web:149]

## 2. Co przygotować w Google Cloud

Zanim zaczniesz kodować Streamlit, przygotuj:
- projekt Google Cloud,
- włączone Business Profile APIs,
- ekran zgody OAuth,
- OAuth Client ID typu Web application,
- bezpieczne miejsce na refresh token. [web:146][web:157][web:108]

W praktyce API i zakresy powinny być minimalne, a dla edycji danych GBP potrzebujesz zakresu biznesowego opisanego w dokumentacji Google. [web:145][web:146][web:157][web:141]

## 3. Proponowana architektura

Najprostszy i czysty układ dla Twojego dashboardu:

1. **Streamlit UI** — ekran logowania i panel GBP.
2. **OAuth Handler** — logowanie Google, odbiór callbacku i zapis tokenów.
3. **GBP Client** — warstwa wywołań API.
4. **Token Store** — bezpieczne przechowywanie refresh tokena.
5. **n8n** — harmonogram pobierania recenzji, publikacji postów i raportów. [cite:5][cite:19][web:105][web:109]

## 4. Kroki w Google Cloud

### Krok 1 — utwórz projekt
W Google Cloud Console tworzysz nowy projekt dla J(AI)SON lub osobny projekt per klient. [web:146][web:157]

### Krok 2 — włącz API
Włącz Business Profile APIs wymagane do odczytu i zarządzania danymi lokalizacji, opinii i postów. [web:108][web:141][web:157]

### Krok 3 — OAuth consent screen
Skonfiguruj ekran zgody OAuth, ustaw typ aplikacji, dodaj domenę, politykę prywatności i zakresy. [web:146][web:159]

### Krok 4 — OAuth Client ID
Utwórz klienta OAuth typu **Web application** i dodaj redirect URI, który będzie obsługiwany przez Streamlit lub przez mały backend callbackowy. [web:146][web:154][web:153][web:159]

## 5. Jak zrobić login w Streamlit

Streamlit może pokazać przycisk **Zaloguj przez Google**. Po kliknięciu użytkownik trafia do Google OAuth, a po powrocie aplikacja odbiera `code`, wymienia go na access token i refresh token, a następnie zapisuje sesję. [web:159][web:145][web:146]

W praktyce warto zrobić to tak:
- frontend Streamlit generuje link logowania,
- callback może być obsłużony przez mały endpoint FastAPI albo przez dedykowany redirect handler,
- tokeny zapisujesz w bezpiecznym storage poza plikami projektu. [web:159][web:146]

## 6. Minimalny flow danych

1. Użytkownik klika logowanie.
2. Google pokazuje consent screen.
3. Użytkownik zgadza się na dostęp do GBP.
4. Aplikacja dostaje `code`.
5. Backend wymienia `code` na `access_token` i `refresh_token`.
6. Token trafia do bezpiecznego storage.
7. Streamlit odpytuje GBP API przez własnego klienta. [web:145][web:146][web:157][web:159]

## 7. Struktura plików

```text
app/
  streamlit_app.py
  auth/
    google_oauth.py
    token_store.py
  clients/
    gbp_client.py
  pages/
    scanner.py
    reviews.py
    tasks.py
    competitors.py
```

## 8. Przykład kodu OAuth

Poniżej minimalny szkic logiczny, bez pełnej produkcyjnej obsługi błędów:

```python
import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/business.manage"]


def build_flow():
    return Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES,
        redirect_uri="http://localhost:8501/"
    )


def start_login():
    flow = build_flow()
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    st.link_button("Zaloguj przez Google", auth_url)


def finish_login(auth_code: str):
    flow = build_flow()
    flow.fetch_token(code=auth_code)
    creds = flow.credentials
    return creds
```

## 9. Przechowywanie tokenów

Tokeny nie powinny trafiać do repozytorium ani do zwykłego pliku tekstowego w projekcie. Dla MVP możesz użyć `.env` tylko do `client_id` i `client_secret`, a refresh token trzymać w zaszyfrowanym storage lub w bazie z szyfrowaniem po stronie aplikacji. [web:145][web:146][web:159]

Dla produkcji lepsze są:
- Google Secret Manager,
- Vault,
- zaszyfrowana kolumna w bazie,
- osobny backend auth. [cite:5][web:159]

## 10. Jak używać tokena w GBP Client

Po autoryzacji tworzysz klienta API z tokenem użytkownika i używasz go do:
- odczytu lokalizacji,
- odczytu recenzji,
- publikowania odpowiedzi,
- tworzenia postów,
- pobierania statusu odpowiedzi. [web:105][web:106][web:108][web:141]

## 11. Obsługa odświeżania

Ponieważ access token wygasa, aplikacja musi używać refresh tokena do odświeżania sesji. To jest standardowy OAuth flow i jest potrzebny, jeśli dashboard ma działać bez ciągłego ponownego logowania. [web:145][web:146][web:159]

## 12. Integracja z n8n

n8n może uruchamiać workflowy cykliczne, ale sam flow autoryzacji najlepiej zrobić w Streamlit lub w małym backendzie. n8n powinien korzystać z gotowych tokenów lub webhooków, a nie prowadzić użytkownika przez cały OAuth w środku workflowu. [cite:5][cite:19]

## 13. Najprostsza implementacja dla Ciebie

### MVP
- login Google w Streamlit,
- token zapisany w bezpiecznym miejscu,
- odczyt recenzji,
- draft odpowiedzi,
- ręczna akceptacja.

### Kolejny etap
- posty GBP,
- grid map,
- monitoring konkurencji,
- automatyczne taski,
- webhooki do n8n. [web:105][web:106][web:109][web:115][web:119]

## 14. Najważniejsze zasady

- Używaj OAuth 2.0, nie service account jako podstawy. [web:145][web:158]
- Wymagaj logowania kontem z dostępem do wizytówki. [web:109][web:141]
- Trzymaj tokeny poza repo i poza frontem. [web:146][web:159]
- Publikację odpowiedzi na opinie rób po akceptacji człowieka. [web:109][web:105][web:116]
- Zaczynaj od własnej wizytówki, potem dopiero multi-location. [web:108][web:157]

## 15. Rekomendacja końcowa

Dla J(AI)SON najlepszy pattern to: Streamlit jako panel, OAuth 2.0 jako bramka, GBP API jako źródło prawdy, n8n jako orkiestrator i Gemini jako warstwa inteligencji. To jest najprostsze, zgodne z dokumentacją i najmniej ryzykowne operacyjnie. [web:145][web:146][web:157][web:159][cite:5][cite:19]
