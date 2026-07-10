# 📝 Lista zadań: Integracja WordPress z Wirtualnym Zarządem

Ten plik zawiera checklistę i architekturę połączenia stron klientów na WordPressie z agentami AI.

---

## 🤖 Jaki Agent obsługuje WordPressa?

Wdrożenie realizujemy w układzie dwu-agentowym:
1.  **CTO Agent (Techniczny Operator):**
    *   Odpowiada za bezpieczne nawiązanie połączenia z REST API WordPressa.
    *   Weryfikuje klucze autoryzacji (Application Passwords) i poprawność SSL.
    *   Tworzy i utrzymuje scenariusze integracyjne (np. webhooki w n8n).
2.  **CMO / CCO Agent (Content & SEO Operator):**
    *   Generuje zoptymalizowane pod kątem **AEO/GEO** wpisy blogowe.
    *   Poprawia meta-opisy, tytuły i strukturę nagłówków `<h1>`-`<h3>` na istniejących stronach.
    *   Monitoruje komentarze i przygotowuje wersje robocze odpowiedzi (human-in-the-loop).

---

## 🛠️ Krok po kroku: Konfiguracja połączenia

### Krok 1: Generowanie haseł aplikacji w WordPress
Dla każdej z 4 domen (`coolfon.pl`, `viptransporter.pl`, `smartrade.pl`, `kurczakujasia.pl`) wykonaj:
- [ ] Zaloguj się do panelu administratora WP (`/wp-admin`).
- [ ] Przejdź do: **Użytkownicy -> Profil** (Users -> Profile).
- [ ] Zjedź na sam dół do sekcji **Hasła aplikacji** (Application Passwords).
- [ ] Wpisz nazwę klucza: `Holistic OS Agent`.
- [ ] Kliknij **Dodaj nowe hasło aplikacji** i skopiuj wygenerowany kod (np. `xxxx xxxx xxxx xxxx xxxx`).

### Krok 2: Konfiguracja pliku `.env` w Holistic OS
- [ ] Dodaj dane logowania do pliku `.env` na serwerze i lokalnie w następującym formacie:
  ```env
  # WordPress API Credentials
  WP_COOLFON_USER="twoj-login-lub-email"
  WP_COOLFON_PASS="xxxx xxxx xxxx xxxx xxxx"
  WP_COOLFON_URL="https://coolfon.pl"

  WP_VIPTRANSPORTER_USER="twoj-login"
  WP_VIPTRANSPORTER_PASS="xxxx xxxx xxxx xxxx xxxx"
  WP_VIPTRANSPORTER_URL="https://viptransporter.pl"

  WP_SMARTRADE_USER="twoj-login"
  WP_SMARTRADE_PASS="xxxx xxxx xxxx xxxx xxxx"
  WP_SMARTRADE_URL="https://smartrade.pl"

  WP_KURCZAKUJASIA_USER="twoj-login"
  WP_KURCZAKUJASIA_PASS="xxxx xxxx xxxx xxxx xxxx"
  WP_KURCZAKUJASIA_URL="https://kurczakujasia.pl"
  ```

### Krok 3: Wdrożenie noda WordPress w n8n lub skryptu Python
- [ ] Skonfiguruj przepływ n8n (lub skrypt w Pythonie `01_src/wordpress_sync.py`), który będzie autoryzował się za pomocą Basic Auth (użytkownik + hasło aplikacji) i wykonywał zapytania do endpointów REST API:
  *   Listowanie stron/postów: `GET /wp-json/wp/v2/posts` lub `/wp-json/wp/v2/pages`
  *   Tworzenie wpisów (jako wersje robocze - draft): `POST /wp-json/wp/v2/posts`
  *   Aktualizacja treści: `POST /wp-json/wp/v2/posts/<id>`

---

## 🎯 Cele operacyjne dla agentów w WordPressie

- [ ] **Audyt Treści:** Przeskanowanie istniejących stron i zidentyfikowanie braków pod kątem AEO (brak słów kluczowych, słaba struktura nagłówków).
- [ ] **Automatyczny Blog:** Konfiguracja n8n do pobierania trendów z branży GSM/Car Rental/E-commerce/Gastro i automatycznego generowania 1 draftu posta tygodniowo przez AI do akceptacji w panelu WP.
- [ ] **Baza Opinii (Social Proof):** Integracja komentarzy z WP z mailem/SMS w celu szybkiej moderacji i odpowiedzi na recenzje klientów.
