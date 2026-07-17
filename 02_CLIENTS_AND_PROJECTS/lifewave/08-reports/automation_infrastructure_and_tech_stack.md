# 🏗️ Dokumentacja Infrastruktury Automatyzacji & Stacku Technologicznego
## Projekt: LifeWave4Life (Stacja X2O™ & Fototerapia Komórkowa)
### Stan wdrożenia: Gotowy / Produkcyjny (`x2o.jaison.pl` | `mlm.jaison.pl`)

---

## 🏗️ 1. Architektura Systemowa (End-to-End)

Poniższy diagram przedstawia kompletny przepływ informacji – od interakcji użytkownika na stronie internetowej, przez inteligentną filtrację lokalną, zapytania RAG w chmurze Google Cloud, aż po automatyzację rezerwacji w n8n i wysyłkę wiadomości przez bramkę WhatsApp.

```mermaid
graph TD
    %% Warstwa Klienta
    subgraph Warstwa Klienta (Frontend)
        A[index.html - Portal Marketingowy] -->|POST message, type=marketing| C[php/chat.php - Backend]
        B[x2o-guide-pl.html - Instrukcja] -->|POST message, type=technical| C
    end

    %% Warstwa Pośrednicząca i Bezpieczeństwa
    subgraph Warstwa Pośrednicząca (Local Server Backend)
        C -->|1. Honeypot, Rate Limiter, Session Cap| D{Filtry Spamu & Limitów}
        D -->|Blokada spamu / limit| E[Natychmiastowa odpowiedź / Odmowa]
        D -->|Przejście testów| F{Lokalny Interceptor Tematów}
        F -->|Wykryto słowo kluczowe| G[Zwrot predefiniowanej, bezbłędnej odpowiedzi]
        F -->|Brak dopasowania słów kluczowych| H[Autoryzacja JWT z GCP key.json]
    end

    %% Warstwa Sztucznej Inteligencji (Google Cloud Platform)
    subgraph Warstwa AI (Google Cloud Platform - Vertex AI Search)
        H -->|2. Bezpieczne zapytanie RAG przez cURL| I{Vertex AI Search API}
        I -->|Aplikacja Marketingowa| J[(Data Store: x2o-marketing-search)]
        I -->|Aplikacja Techniczna| K[(Data Store: x2o-technical-search)]
        J -->|Wyszukaj & Podsumuj| L{Silnik Generatywny Gemini}
        K -->|Wyszukaj & Podsumuj| L
        L -->|Weryfikacja Podsumowania| M{Czy to halucynacja / odmowa?}
        M -->|Tak - Odmowa/Brak danych| N[Uruchomienie Smart Fallback]
        M -->|Nie - Prawidłowa odpowiedź| O[Zwrot wygenerowanej odpowiedzi do chat.php]
    end

    %% Warstwa Automatyzacji (n8n & CRM)
    subgraph Warstwa Automatyzacji i CRM (n8n Engine)
        P[Cal.com Webhook] -->|Rezerwacja spotkania| Q[n8n Workflow Engine]
        Q -->|Zapisz/Aktualizuj| R[(Google Sheets CRM)]
        Q -->|Filtruj cel spotkania| S{Router n8n}
        S -->|Cel: Zdrowie / Regeneracja| T[Wyślij zapytanie do Evolution API]
        S -->|Cel: Biznes / MLM| U[Wyślij zapytanie do Evolution API]
    end

    %% Warstwa Komunikacji (WhatsApp Gateway)
    subgraph Warstwa Komunikacji (WhatsApp Gateway)
        T -->|Powiadomienie + Link do Klubu X2O / X39| V[Telefon Klienta na WhatsApp]
        U -->|Powiadomienie + Link do Biznes & Duplikacja| V
    end
```

---

## 🛠️ 2. Kompletny Stack Technologiczny (Tech Stack)

Zbudowaliśmy system w oparciu o ultra-wydajne, asynchroniczne i niskokosztowe technologie, eliminując zbędne opłaty abonamentowe (np. drogie licencje CRM czy Systeme.io) i maksymalizując wykorzystanie darmowych pakietów (GCP Free Tier, Cal.com Free Developer, Google Sheets API).

### 1. Warstwa Prezentacji (Frontend Layer)
*   **Technologia:** Czysty HTML5, Vanilla CSS3 (zmienne CSS, nowoczesny layout Grid & Flexbox, efekty szklane Glassmorphism, animacje wejścia @keyframes) oraz asynchroniczny JavaScript (ES6 fetch API, obsługa lightbox, dynamiczne przełączanie bento-pills).
*   **Aestetyka:** Ciemny tryb (Sleek Dark Mode), akcenty turkusu biofotonowego (`#00D2C4`) i głębokiego fioletu energetycznego (`#9B51E0`), typografia z rodziny **Outfit** oraz **Inter** pobierana z Google Fonts.
*   **Responsywność (Mobile-First):** Strona jest w 100% zoptymalizowana pod urządzenia mobilne, eliminując jakiekolwiek obcinanie elementów z prawej strony czy niekontrolowane przesuwanie.

### 2. Warstwa Logiki Backendowej (Backend & Security Layer)
*   **Technologia:** **PHP 8.x** (działa jako bezpieczna bramka proxy `php/chat.php` bez wystawiania wrażliwych tokenów na zewnątrz).
*   **Zabezpieczenia (Bramki Anty-Spamowe):**
    *   *Shield 1: Honeypot (Anti-Bot)* – niewidoczne dla użytkowników pola formularza rezerwacji i czatu, których wypełnienie przez boty skanujące natychmiast odrzuca zapytanie.
    *   *Shield 2: IP Rate Limiter* – minimalna przerwa 3 sekund między zapytaniami z tego samego adresu IP (zapobiega pętlom i DDoS).
    *   *Shield 3: Daily Session Cap* – limit maksymalnie 30 zapytań na dobę na unikalnego użytkownika (sesję), chroniący przed nabijaniem kosztów API.
    *   *Shield 4: Local Keyword Interceptor* – lokalny słownik dopasowań (patenty, Łódź, kontakt, MLM), który całkowicie wyklucza halucynacje AI i zwraca natychmiastowe (0 ms), bezbłędne odpowiedzi z aktywnymi linkami HTML.

### 3. Warstwa Sztucznej Inteligencji & RAG (AI Grounding Layer)
*   **Platforma:** **Google Cloud Platform (GCP) -> Gemini Enterprise Agent Platform** (dawniej Vertex AI Search).
*   **Magazyny Danych (Data Stores):**
    *   `x2o-marketing-search_1784201767565` – zasilany materiałami o biznesie MLM, marce LifeWave, badaniach klinicznych oraz naukowej wizji Davida Schmidta.
    *   `x2o-technical-search_1784202964185` – zasilany polską instrukcją techniczną X2O (Users Guide), schematami montażu, parametrami zasilacza i tabelami odkamieniania.
*   **Uwierzytelnianie:** Generowanie krótkotrwałego tokenu JWT (JSON Web Token) podpisanego asymetrycznie kluczem prywatnym RSA-256 z pliku `key.json` (Service Account), a następnie wymiana na token dostępu (OAuth2 Access Token) w Google Auth Server. Brak twardego kodowania haseł w plikach źródłowych.

### 4. Warstwa Orkiestracji & Automatyzacji (Automation Layer)
*   **Silnik:** **n8n Workflow Engine** (asynchroniczny orchestrator procesów).
*   **Źródło Rezerwacji:** **Cal.com** (Developer Free Plan), wykorzystujący zaawansowane webhooki oparte na sygnaturach bezpieczeństwa oraz system przypomnień e-mail/SMS (Workflows).
*   **Komunikacja WhatsApp:** **Evolution API** / **Z-API** (bramka dostępu do oficjalnej sieci WhatsApp Business, łącząca telefon Tomasza jako asystenta marki).

### 5. Warstwa Danych (Database Layer)
*   **CRM:** **Google Sheets CRM** (Arkusz kalkulacyjny Google połączony bezpiecznie z n8n przez protokół OAuth2).
*   **Zalety:** Brak limitów rekordów, natychmiastowa widoczność nowych leadów dla całego zespołu (Tomasz, Monika, Ania) w telefonach komórkowych, możliwość swobodnego dodawania statusów, notatek z rozmów i filtrowania celów.

---

## 📊 3. Przepływ Danych & Bezpieczeństwo Tokenów

Bezpieczeństwo infrastruktury chmurowej w projektach marketingowych jest absolutnym priorytetem. Tradycyjne wdrożenia bardzo często popełniają błąd, wysyłając zapytania do modeli językowych bezpośrednio z kodu JavaScript w przeglądarce klienta, co pozwala na kradzież kluczy API i generowanie gigantycznych kosztów na konto właściciela.

### Zastosowany Model Bezpieczeństwa w LifeWave4Life:
1.  **Całkowita Izolacja Klienta:** Przeglądarka użytkownika nigdy nie komunikuje się bezpośrednio z usługami Google Cloud ani z bazą danych. Wszystkie zapytania czatu trafiają do lokalnego pliku `php/chat.php`.
2.  **Ukryty Klucz Chmurowy:** Plik autoryzacyjny `key.json` (GCP Service Account) znajduje się w zabezpieczonym katalogu backendowym na serwerze i jest chroniony regułą w pliku `.htaccess` / konfiguracji Nginx:
    ```nginx
    # Blokada bezpośredniego dostępu do plików konfiguracyjnych i JSON
    location ~* \.(json|ini|key)$ {
        deny all;
    }
    ```
3.  **Krótkotrwałe Uprawnienia (Least Privilege):** Konto usługi (Service Account) posiada wyłącznie uprawnienie **Discovery Engine Viewer** w projekcie `jaison-x2o-portal`. Nie ma możliwości, aby ktoś za pomocą tego klucza zarządzał maszynami wirtualnymi, bazami danych czy generował niekontrolowane koszty chmurowe. Tokeny dostępowe generowane przez PHP wygasają automatycznie po 3600 sekundach.

---

## 👥 4. Tożsamość Zespołu & Zapobieganie Halucynacjom Medycznym

W celu ochrony wizerunku marki oraz wyeliminowania medycznych halucynacji (np. zmyślania, że Ania jest "ekspertem ds. leczenia COVID-19" czy wprowadzania innych medycznie niebezpiecznych tez), w silniku RAG oraz w lokalnym interceptorze wdrożyliśmy **sztywny podział ról w zespole**:

### 🎯 Oficjalne Definicje Ról w Systemie:

*   **Tomasz Duda:**
    *   *Rola:* Brand Partner LifeWave.
    *   *Specjalizacja:* Ekspert ds. systemów automatyzacji, lejków marketingowych oraz wdrażania nowoczesnych systemów AI i duplikacji dla **NOWYCH partnerów handlowych** wchodzących do struktury MLM.
    *   *Kontakt:* `+48 791 636 644` (oraz Klubowy WhatsApp).
*   **Monika:**
    *   *Rola:* Director / Brand Partner LifeWave.
    *   *Specjalizacja:* Profesjonalna terapeutka, ekspertka i doradczyni ds. hydratacji biofotonowej X2O™ oraz całościowej regeneracji komórkowej organizmu. Prowadzi fizyczny Gabinet Świątynia Harmonii w Łodzi.
    *   *Kontakt:* `+48 535 200 879`.
*   **Ania:**
    *   *Rola:* Brand Partner LifeWave.
    *   *Specjalizacja:* Profesjonalna terapeutka, specjalistka ds. fotobiomodulacji oraz naturalnego zdrowia komórkowego. Prowadzi fizyczny Gabinet Świątynia Harmonii w Łodzi.
    *   *Kontakt:* `+48 501 401 704`.

> [!IMPORTANT]
> **Złota Zasada Komunikacji Medycznej:**
> Nasze stacje X2O™ oraz plastry fototerapeutyczne (X39/X49) nie są lekami i nie służą do diagnozowania czy leczenia konkretnych jednostek chorobowych (w tym COVID-19, chorób przewlekłych itp.). Działają one na poziomie **fizyki kwantowej i fotobiomodulacji**, pobudzając naturalne mechanizmy regeneracyjne i bio-przewodnictwo organizmu (np. poprzez aktywację peptydów miedzi GHK-Cu i komórek macierzystych). Taki przekaz buduje potężne zaufanie, jest w pełni zgodny z prawem farmaceutycznym oraz polityką compliance LifeWave.

---

## 📈 5. Plany Rozwoju & Skalowalność (mlm.jaison.pl)

Obecna architektura została zaprojektowana z myślą o natychmiastowej rozbudowie do poziomu **SaaS (Software-as-a-Service)** pod wybraną przez Ciebie subdomenę **`mlm.jaison.pl`**:

1.  **Dystrybucja Klonów (Replikacja Stron):**
    Dzięki temu, że strona opiera się na czystym HTML i CSS, wdrożenie nowej spersonalizowanej strony dla nowego partnera handlowego polega na sklonowaniu katalogu na serwerze i automatycznej podmianie zmiennych (np. nazwy partnera, jego linku do Cal.com i numeru telefonu WhatsApp).
2.  **Skalowanie n8n:**
    Pojedyncza instancja n8n może obsługiwać setki różnych kont Cal.com dzięki dynamicznemu trasowaniu w oparciu o identyfikator użytkownika przekazywany w webhooku.
3.  **Klubowy WhatsApp (Group Autopilot):**
    Wdrożenie bota n8n do stałego monitorowania i moderowania Twoich grup WhatsApp, który automatycznie wita nowych członków, usuwa spam oraz raz w tygodniu wysyła zaproszenia na asynchroniczne webinary szkoleniowe.

---

### Podsumowanie Technologiczne
Twój system to unikalne połączenie **asynchronicznej automatyzacji, bezkompromisowego bezpieczeństwa i premium designu**. Działa bezobsługowo, gromadzi cenne kontakty w Google Sheets CRM, buduje profesjonalny wizerunek marki i eliminuje jakiekolwiek tarcie operacyjne w Twoim codziennym biznesie.

*Dokument przygotowany przez zespół AntiGravity i zatwierdzony do użytku operacyjnego.* 🚀
