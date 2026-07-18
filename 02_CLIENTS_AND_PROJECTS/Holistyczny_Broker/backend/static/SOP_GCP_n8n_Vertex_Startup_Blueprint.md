# Standard Operating Procedure (SOP) — Blueprint wdrożeniowy GCP + n8n + Vertex AI + LiteLLM + Startups program

> **Cel dokumentu:** Przewodnik krok po kroku (od A do Z) służący do replikacji kompletnego, taniego i bezpiecznego środowiska sztucznej inteligencji (AI/LLM) dla startupów i projektów biznesowych. Architektura łączy autonomiczne kontenery (n8n na VPS) z bezpieczną chmurą obliczeniową Google Cloud (Vertex AI) oraz warstwą proxy (LiteLLM) do zarządzania kredytami.

---

## 🏛️ Schemat architektury hybrydowej

```mermaid
flowchart TD
    subgraph Klienci / Agenty programistyczne
        AG[AntiGravity IDE] --> |Protokół OpenAI| LLM[LiteLLM Router]
        H[Hermes Agentic OS] --> |Protokół OpenAI| LLM
    end

    subgraph Serwer VPS / Maszyna VM
        LLM --> |Zarządzanie kluczami i routing| N8N[Kontener n8n]
        N8N --> |Zapis transakcji| DB[(PostgreSQL)]
    end

    subgraph Google Cloud Platform
        LLM --> |Autoryzacja przez Service Account| VTX[Vertex AI / Gemini API]
        VTX --> |Wykorzystanie Kredytów| CR[Kredyty Free Trial / Startups]
    end
```

---

## 📑 Krok 1: Konfiguracja GCP i Aktywacja Środków

Weryfikatorzy Google wymagają posiadania profesjonalnej tożsamości biznesowej, ale sam proces konfiguracji chmury możesz rozpocząć bezkosztowo. Masz do wyboru dwie ścieżki:

### 1.1 Ścieżki konfiguracji konta GCP (Opcja Bezkosztowa vs Workspace)

*   **Opcja A: Bezkosztowa (Nasz Case Study — Rekomendowana na start) ⚡**
    1.  Załóż lub użyj zwykłego, darmowego konta **`twójprojekt@gmail.com`**.
    2.  Zaloguj się nim do Konsoli GCP i przejdź do konfiguracji zasobów. Twój projekt będzie działał w trybie **„Brak organizacji” (standalone)**. Jest to w 100% wystarczające do wdrożenia n8n, LiteLLM i modeli AI.
    3.  **Ważny warunek:** Nie musisz od razu kupować subskrypcji Google Workspace. Jedyne, o co musisz zadbać, to posiadanie skrzynki w domenie (np. `kontakt@twojadomena.pl` postawionej na dowolnym tańszym hostingu) dopiero w momencie składania wniosku o grant (Krok 5). Podasz ten adres biznesowy w formularzu jako kontaktowy, co potwierdzi Twoją tożsamość przed Google.
*   **Opcja B: Korporacyjna (Zasób Organizacji)**
    1.  Kupujesz subskrypcję Google Workspace dla domeny (np. `kontakt@twojadomena.pl`).
    2.  Logujesz się tym adresem do Google Cloud. GCP automatycznie utworzy formalny zasób **Organizacji** (np. `twojadomena-org`), co pozwala na centralne zarządzanie strukturą projektów i uprawnieniami pracowników.

### 1.2 Aktywacja Darmowych Środków Trial i Gen AI App Builder
Po podpięciu karty płatniczej do nowego Konta Rozliczeniowego (Billing Account) Google automatycznie przyznaje:
1. **$300 USD (ok. 1200 PLN) Free Trial:** Ważne przez 90 dni na wszystkie usługi GCP.
2. **$1000 USD (ok. 3900 PLN) Gen AI App Builder credits (Ważne przez 1 ROK):** Przyznawane automatycznie w celach testowania modeli językowych na platformie Vertex AI (Search, Conversation oraz Gemini API). Kredyty te są ważne przez pełne **12 miesięcy (rok)** i są rozliczane automatycznie w pierwszej kolejności, odciążając Twój budżet przed środkami z karty płatniczej i tradycyjnym trialem.

---

## 📑 Krok 2: Bezpieczne Połączenie VPS z GCP (IAM & Service Account)

NIGDY nie wystawiaj kluczy głównego administratora w kodzie ani w n8n. Komunikacja musi odbywać się przez konto usługowe z zasadą najmniejszych uprawnień.

### 2.1 Tworzenie Konta Usługowego (Service Account)
1. W konsoli GCP przejdź do sekcji **IAM & Admin -> Service Accounts**.
2. Kliknij **Create Service Account**. Nazwij je np. `n8n-vertex-agent`.
3. W kroku nadawania ról przypisz rolę:
   * **`Vertex AI User`** (pozwala na odpytywanie modeli Gemini).
4. Kliknij w utworzone konto, przejdź do zakładki **Keys -> Add Key -> Create new key (format JSON)**.
5. Pobierz plik klucza na dysk. Plik ten zawiera bezpieczne poświadczenia dostępowe.

### 2.2 Przesłanie klucza na serwer VPS
1. Zapisz plik na serwerze w bezpiecznym katalogu, do którego dostęp ma wyłącznie kontener dockera (np. `/opt/n8n-broker/gcp-sa-key.json`).
2. Ustaw uprawnienia dostępu:
   ```bash
   chmod 600 /opt/n8n-broker/gcp-sa-key.json
   chown 1000:1000 /opt/n8n-broker/gcp-sa-key.json
   ```

---

## 📑 Krok 3: Wdrożenie n8n na serwerze VPS (Docker Compose + SSL)

Dla zachowania pełnej poufności danych i braku limitów operacji (Zero Data Leakage), n8n jest wdrażany jako kontener na serwerze VPS za reverse proxy.

### 3.1 Plik `docker-compose.yml`
Utwórz plik konfiguracyjny w katalogu `/opt/n8n-broker/`:

```yaml
version: '3.8'

services:
  n8n-postgres:
    image: postgres:16-alpine
    container_name: n8n-postgres
    restart: always
    environment:
      - POSTGRES_USER=n8n_admin
      - POSTGRES_PASSWORD=TWOJE_SILNE_HASLO
      - POSTGRES_DB=n8n_database
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
    ports:
      - "127.0.0.1:5432:5432"

  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    container_name: n8n
    restart: always
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=n8n-postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n-database
      - DB_POSTGRESDB_USER=n8n_admin
      - DB_POSTGRESDB_PASSWORD=TWOJE_SILNE_HASLO
      - N8N_HOST=n8n.twojadomena.pl
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://n8n.twojadomena.pl/
      - N8N_TRUST_PROXY=true
    volumes:
      - ./n8n_data:/home/node/.n8n
      - /opt/n8n-broker/gcp-sa-key.json:/home/node/gcp-sa-key.json:ro
    ports:
      - "127.0.0.1:5678:5678"
    depends_on:
      - n8n-postgres
```

### 3.2 Zabezpieczenie SSL (Nginx + Certbot)
Skonfiguruj Nginx jako reverse proxy na porcie 80/443 i przekieruj ruch na `127.0.0.1:5678`. Uruchom certbot w celu wygenerowania darmowego certyfikatu SSL Let's Encrypt:
```bash
sudo certbot --nginx -d n8n.twojadomena.pl
```

---

## 📑 Krok 4: Wdrożenie i konfiguracja LiteLLM Router

**LiteLLM** służy jako centralny router i proxy, który:
* Tłumaczy zapytania w standardzie OpenAI na format Vertex AI (Gemini).
* Umożliwia agentycznym środowiskom programistycznym (takim jak **AntiGravity** w IDE) oraz autonomicznym agentom (np. **Hermes**) na bezpośrednie korzystanie z modeli GCP z darmowych kredytów.

### 4.1 Instalacja i uruchomienie LiteLLM
LiteLLM można uruchomić jako usługę systemową lub w kontenerze Dockera.

1. Utwórz plik konfiguracyjny `/opt/litellm/config.yaml`:
```yaml
model_list:
  - model_name: gemini-2.5-flash
    litellm_params:
      model: vertex_ai/gemini-2.5-flash
      vertex_project: ID_TWOJEGO_PROJEKTU_GCP
      vertex_location: us-central1
      vertex_credentials: "/home/node/gcp-sa-key.json"

  - model_name: gemini-2.5-pro
    litellm_params:
      model: vertex_ai/gemini-2.5-pro
      vertex_project: ID_TWOJEGO_PROJEKTU_GCP
      vertex_location: us-central1
      vertex_credentials: "/home/node/gcp-sa-key.json"
```

2. Dołącz LiteLLM do pliku `docker-compose.yml`:
```yaml
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    container_name: litellm
    restart: always
    volumes:
      - /opt/litellm/config.yaml:/app/config.yaml:ro
      - /opt/n8n-broker/gcp-sa-key.json:/home/node/gcp-sa-key.json:ro
    ports:
      - "127.0.0.1:4000:4000"
    command: ["--config", "/app/config.yaml", "--port", "4000"]
```

3. Wygeneruj klucz dostępowy w LiteLLM:
   * Wykorzystaj zapytanie do panelu administracyjnego LiteLLM w celu wygenerowania tokenu OpenAI-compatible (np. `sk-1234...`), który rozdziela dostęp na poszczególnych użytkowników i kontroluje zużycie budżetu.

---

## 📑 Krok 5: Aplikacja do Google for Startups Cloud Program (Start Tier)

Możesz aplikować po dodatkowy grant **$2,000 USD (ok. 8,000 PLN)** w dowolnym momencie. **NIE musisz** czekać na wyczerpanie darmowych środków próbnych ($300 + $1000) do zera. Google pozwala na łączenie (kumulowanie) tych budżetów, co daje Ci pełną ciągłość pracy bez ryzyka niespodziewanych przerw w działaniu agentów AI.

### 5.1 Kryteria kwalifikacji (Start Tier)
* **Dowolna forma działalności gospodarczej:** Do programu kwalifikują się zarówno **Jednoosobowe Działalności Gospodarcze (JDG)** zarejestrowane w CEIDG, jak i spółki prawa handlowego (np. Sp. z o.o., S.A.) zarejestrowane w KRS. Kluczowy jest wpis do oficjalnego rejestru państwowego.
* **Wiek firmy (Maksymalnie 10 lat):** Zgodnie z oficjalną polityką Google, firma może mieć **do 10 lat** od momentu rejestracji (w formularzu zaznacza się odpowiedni przedział: *3-12 miesięcy*, *1-2 lata*, *2-5 lat* lub *5-10 lat*).
* **Profesjonalny wizerunek cyfrowy:** Działająca strona WWW w języku polskim oraz angielskim (dla międzynarodowych weryfikatorów z Google).
* **Aktywne konto billingowe:** Posiadanie aktywnego, płatnego konta rozliczeniowego GCP (Upgraded Billing Account).
* Startup nie może być wcześniej beneficjentem wysokich grantów chmurowych od Google.

### 5.2 Ścieżka wypełniania formularza aplikacyjnego
1. Przejdź do oficjalnego formularza: [Google for Startups Apply](https://cloud.google.com/startup/apply).
2. **E-mail aplikacyjny:** Zawsze używaj skrzynki w domenie firmy (np. `kontakt@twojadomena.pl`), a nie darmowej poczty Gmail.
3. **AI Startup:** Wybierz opcję **`AI startups`** — kwalifikuje to projekt do dodatkowych benefitów i bezpośredniej opieki inżynierskiej.
4. **Google Cloud Billing Account ID:** Wklej 18-znakowy identyfikator swojego aktywnego konta rozliczeniowego (np. `01C9FD-39357F-3918B8`).
5. **Funding Stage:** Zaznacz **`Bootstrapped`** (finansowanie ze środków własnych).
6. **Program Partner / Accelerators:** Wpisz **`NONE`** (jeśli nie jesteś członkiem funduszu VC z sieci Google).
7. Po wysłaniu wniosku, decyzja o przyznaniu kredytów zapada w terminie **3-5 dni roboczych**, a środki są natychmiast przypisywane do wybranego ID konta rozliczeniowego.

---

### 5.3 Poziomy i Fazy Programu Google for Startups Cloud (Tiers)

Wsparcie finansowe Google jest podzielone na przejrzyste fazy dopasowane do dojrzałości biznesowej projektu. Poniższa struktura pozwala zaplanować budżet chmurowy na każdym etapie rozwoju:

| Poziom (Tier) | Maksymalna kwota grantu | Czas ważności | Główne kryteria i warunki kwalifikacji |
| :--- | :--- | :--- | :--- |
| **Start Tier** *(Bootstrapped)* | **$2,000 USD** *(ok. 8,000 PLN)* | **1 rok** | brak finansowania zewnętrznego VC (środki własne, aniołowie biznesu, granty), wiek firmy do 10 lat, działająca domena i e-mail biznesowy. |
| **Scale Tier** *(Pre-funded / Series A)* | **$200,000 USD** *(ok. 800,000 PLN)* | **2 lata** | Posiadanie finansowania instytucjonalnego (od funduszy VC, akceleratorów partnerskich lub inkubatorów), wiek firmy do 10 lat. Kredyty pokrywają 100% kosztów w Roku 1 (do $100k) oraz 20% kosztów w Roku 2 (do $100k). |
| **AI-First Track** *(Dla liderów AI)* | **$350,000 USD** *(ok. 1,400,000 PLN)* | **2 lata** | Budowanie głównego produktu w oparciu o silniki Vertex AI lub Gemini. Oferuje do $100,000 w Roku 1, refundację w Roku 2 oraz dedykowany budżet $12,000 na wsparcie inżynierskie Google (Enhanced Support). |

#### **Jak wygląda przechodzenie między poziomami (Fazy)?**
1.  **Faza Inicjacji:** Zaczynasz jako projekt bootstrapped w **Start Tier** ($2k). To pozwala na zbudowanie MVP, uruchomienie n8n oraz integrację agentów AI bez żadnego ryzyka finansowego.
2.  **Faza Skalowania:** Gdy pozyskasz inwestora instytucjonalnego (VC / anioła z sieci partnerskiej Google), składasz wniosek o **Upgrade** do poziomu **Scale Tier**. Kredyty z pierwszego poziomu zostaną automatycznie zastąpione potężnym grantem na rozwój infrastruktury.

---

## 📑 Krok 6: Zrozumieć Google OAuth — Cel, Weryfikacja i Limity Tokenów

Ta sekcja wyjaśnia logiczne i praktyczne zasady działania bezpiecznego logowania przez Google (OAuth) w Twojej aplikacji.

### 6.1 Czym jest Google OAuth i po co go wdrażamy? (Perspektywa Sensoryczna VAK AD)

*   👁️ **Wzrokowiec (Visual):** Wyobraź sobie ten moment, gdy klient wchodzi na Twoją stronę i zamiast żmudnego przepisywania hasła widzi znajomy, elegancki przycisk **„Zaloguj przez Google”**. Po jego kliknięciu pojawia się czytelne okienko z logo Twojej firmy i prośbą o potwierdzenie. Całość wygląda spójnie, bezpiecznie i profesjonalnie.
*   👂 **Słuchowiec (Auditory):** Wycisz hałas związany z tłumaczeniem klientom kwestii bezpieczeństwa danych. Gdy system pyta: *„Czy ta aplikacja jest bezpieczna?”*, Google odpowiada harmonijnym komunikatem potwierdzającym tożsamość Twojego startupu. Zamiast zaniepokojenia, klient słyszy profesjonalny przekaz.
*   🤝 **Kinestetyk (Kinesthetic):** Poczuj głęboką ulgę i zdejmij ze swoich barków ciężar odpowiedzialności za przechowywanie haseł użytkowników. Przekazując proces autoryzacji w ręce Google, opierasz bezpieczeństwo na solidnym, globalnym fundamencie. Użytkownik czuje się bezpiecznie, a Ty masz pewność, że jego dane są chronione.
*   📊 **Analityk (Auditory Digital):** Dane logiczne są jednoznaczne. Wdrożenie protokołu OAuth 2.0 to standard branżowy, który redukuje tarcie przy rejestracji o ponad 40%. Weryfikacja w GCP polega na zmapowaniu identyfikatorów klienta (Client ID) i kluczy tajnych (Client Secret) w bezpiecznym środowisku produkcyjnym.

---

### 6.2 Dlaczego Google wymaga weryfikacji? (Ochrona przed „Czerwoną Tarczą”)

Gdy aplikacja (np. n8n lub Twój panel klienta) łączy się z kontem Google użytkownika, Google sprawdza jej wiarygodność. 

*   **Brak Weryfikacji (Stan testowy):** Jeśli aplikacja nie przejdzie weryfikacji, każdy użytkownik po próbie logowania zobaczy **niepokojącą czerwoną tarczę ostrzegawczą** z tekstem: *„Ta aplikacja nie została zweryfikowana przez Google”*. 
*   **Weryfikacja automatyczna (Bezobsługowa):** Jeśli Twoja aplikacja prosi wyłącznie o podstawowe dane użytkownika (np. adres e-mail i imię w celu utworzenia konta na platformie — tzw. *non-sensitive scopes*), Google weryfikuje aplikację **natychmiast** po uzupełnieniu podstawowych danych marki i kliknięciu *„Opublikuj aplikację”*. Nie musisz czekać ani wysyłać nagrań wideo.

---

### 6.3 Częstotliwość przyznawania tokenów OAuth (Rate Limiting)

Każde logowanie lub odpytanie API w imieniu użytkownika wymaga wygenerowania tzw. **tokenu dostępu (Access Token)**. Google domyślnie nakłada limit na częstotliwość ich generowania (standardowo do **2000 tokenów na dobę** dla całego projektu).

```
[MIEJSCE NA INFOGRAFIKĘ: Wykres przepływu żądań OAuth - od użytkownika, przez Twój serwer, do Google OAuth API, pokazujący blokadę Rate Limit przy 2000 żądań/dobę]
```

#### **Po co zwiększać ten limit?**
Gdy Twój system (np. agenty automatyzacji n8n) zacznie przetwarzać setki dokumentów na godzinę, generując automatyczne zapytania w pętli, limit 2000 zapytań dziennie może zostać szybko wyczerpany. Wtedy użytkownicy lub agenty AI napotkają **błąd 429 (Too Many Requests)**. Zwiększenie limitu zapewnia:
*   Płynność działania masowych automatyzacji bez przestojów.
*   Bezpieczną obsługę tysięcy aktywnych użytkowników jednocześnie.

#### **Jakie warunki trzeba spełnić, aby zwiększyć ten limit?**
1.  **Status Produkcyjny:** Aplikacja musi zostać opublikowana (nie może być w trybie testowym).
2.  **Uwierzytelniona domena:** Wszystkie adresy URL (Polityka Prywatności, Regulamin) muszą być aktywne i umieszczone w autoryzowanej domenie (np. `twojadomena.pl`).
3.  **Wypełnione Uzasadnienie (App Justification):** W zakładce **Centrum Weryfikacji** należy złożyć krótki wniosek opisujący cel biznesowy aplikacji (np. automatyzacja dokumentów i analityka nieruchomości), który weryfikatorzy Google zatwierdzają w ciągu kilku dni.

```
[MIEJSCE NA ZRZUT EKRANU: Konsola Google Cloud -> Platforma uwierzytelniania Google -> Przegląd -> Wykres "Częstotliwość przyznawania tokenów OAuth" z widocznym przyciskiem "Zwiększ dzienny limit tokenów"]
```

---

### 6.4 Instrukcja konfiguracji krok po kroku

1. W konsoli GCP przejdź do **Platforma uwierzytelniania Google (Google Auth Platform) -> Elementy marki**.
2. Uzupełnij wymagane adresy URL, korzystając z działających stron z domeny startupu:
   * **Strona główna:** `https://twojadomena.pl`
   * **Polityka Prywatności:** `https://twojadomena.pl/polityka-prywatnosci.html`
   * **Regulamin:** `https://twojadomena.pl/regulamin.html`
3. Dodaj domenę `twojadomena.pl` w sekcji **Autoryzowane domeny**.
4. W zakładce **Odbiorcy (Audience)** kliknij niebieski przycisk **Opublikuj aplikację (Publish app)**, aby przenieść ją ze stanu testowego w produkcyjny.
5. Przejdź do **Centrum weryfikacji** — ponieważ korzystamy wyłącznie ze standardowych uprawnień odczytu profilu/email (non-sensitive scopes), system wyświetli status: **`Weryfikacja nie jest wymagana`**, a Twoja aplikacja od razu zacznie działać produkcyjnie dla każdego klienta.

---

### 6.5 Czas oczekiwania na weryfikację marki (Branding Review Timeline)

Gdy prześlesz elementy graficzne swojej marki (logo, nazwa) do zatwierdzenia przez kliknięcie **`Zweryfikuj markę`**:

*   **Czas trwania audytu:** Pełna weryfikacja przez dedykowany zespół Google Trust & Safety trwa zazwyczaj **od 4 do 6 tygodni**.
*   **Pierwszy kontakt:** Pierwszą wiadomość zwrotną od weryfikatora (np. prośbę o doprecyzowanie, jak logo wyświetla się w aplikacji) otrzymasz na e-mail deweloperski w ciągu **3 do 5 dni roboczych**.
*   **Wpływ na ciągłość działania (Brak przestojów):** Podczas trwania weryfikacji Twoja aplikacja **działa nieprzerwanie w wersji produkcyjnej**. Google serwuje użytkownikom ostatnią zatwierdzoną wersję ekranu logowania lub wersję tekstową. Brak weryfikacji marki **nie blokuje** logowania ani operacji API.
