# Architektura Skanera Nieruchomości & Silnik Transakcyjny (Blok 13 MVP)

Ten dokument opisuje architekturę systemu automatycznego skanowania rynku oraz strukturę floty agentów operacyjnych dla projektu **Holistyczny Broker**. Rozwiązanie łączy logikę agentyczną z otwartymi API baz danych w Polsce i systemami automatyzacji transakcyjnej w duchu polityki *Low-Friction* i *Low-Cost*.

---

## 🏗️ 1. Architektura Skanera Nieruchomości (Deal Sourcing Core)

Agent Skanera to automatyczny moduł w systemie Hermes, który przeszukuje polskie rejestry państwowe i mapy katastralne w poszukiwaniu gruntów i pozwoleń budowlanych o wysokim potencjale komercyjnym.

```text
  [ RWDZ (GUNB) ]
        | (Pozwolenia budowlane)
        v
[ Geoportal (ULDK API) ] ---> [ Wstępny Triage (Hermes) ] ---> [ Weryfikacja EKW ] ---> [ Raport PDF ]
        | (MPZP i chłonność)     (Filtry powierzchni i PUM)      (Właściciel / Księga)
        v
  [ GCS Bucket ]
```

### 📂 A. Wykorzystywane Polskie Źródła Danych (API & Scraping):
1.  **RWDZ (Główny Urząd Nadzoru Budowlanego - wyszukiwarka.gunb.gov.pl):**
    - **Jak działa:** Portal rejestruje każdy wniosek o pozwolenie na budowę, decyzję i zgłoszenie w Polsce.
    - **Integracja:** Hermes cyklicznie odpytuje wyszukiwarkę (poprzez API lub kontrolowany web scraping), pobierając dane o nowych wnioskach dotyczących hal produkcyjnych, magazynów, osiedli mieszkaniowych i obiektów komercyjnych w wybranych powiatach.
2.  **Geoportal.gov.pl & ULDK (Usługa Lokalizacji Działek Katastralnych):**
    - **Jak działa:** Otwarte, darmowe API rządowe.
    - **Integracja:** Na podstawie numeru działki z RWDZ, Hermes odpytuje ULDK API w celu pobrania dokładnych granic działki, jej powierzchni geometrycznej, a także przeznaczenia w Miejscowym Planie Zagospodarowania Przestrzennego (MPZP).
3.  **Księgi Wieczyste (EKW - ekw.ms.gov.pl):**
    - **Jak działa:** Oficjalny portal posiada zabezpieczenia CAPTCHA utrudniające automatyzację.
    - **Integracja:** System wykorzystuje komercyjne, tanie wrappery API (np. `ksiegiwieczyste.pl` / `geo-portal`), które pozwalają bezdotykowo po numerze działki wyciągnąć numer KW, a z niego strukturę własnościową (np. spółki skarbu państwa, firmy prywatne, osoby fizyczne).

### ⚙️ B. Przepływ pracy modułu (Cron Job):
- Raz w tygodniu skrypt cykliczny odpytuje RWDZ o nowe wpisy.
- Pobiera numery działek i weryfikuje ich parametry przez Geoportal ULDK API.
- Wykonuje wstępny **Triage** (odrzuca działki o małej powierzchni, wyszukuje wyłącznie tereny o konkretnym PUM - Powierzchni Użytkowej Mieszkalnej/Uługowej).
- Tworzy raport markdown/PDF: *"Okazje inwestycyjne tygodnia + dane wnioskodawców"* i wysyła powiadomienie na Telegram.

---

## 🤖 2. Flota Agentów Transakcyjnych (SOP & Zadania)

Rozbijamy proces pośrednictwa inwestycyjnego na wyspecjalizowane agenty współpracujące w tle w systemie Hermes.

### 🔍 13A — Skauting Okazji Rynkowych (Deal Sourcing)
- **Zadanie agenta:** Monitorowanie portali ogłoszeniowych i przetargów.
- **Źródła skanowania:** 
  - *Portalu ogólne:* Otodom.pl, Nieruchomosci-online.pl, Gratka.pl.
  - *Przemysłowe i B2B:* PropertyStock, ProperGate, BiznesOkazje.
  - *Agencje sieciowe:* CBRE Polska, JLL Polska, Savills.
  - *Przetargi i windykacja:* e-licytacje.pl (aukcje komornicze), BZP (Biuletyn Zamówień Publicznych), TED (Tenders Electronic Daily UE), oferty syndyków.
- **Częstotliwość:** Skanowanie portali ogłoszeniowych co 1 godzinę, rejestrów przetargowych co 24 godziny.
- **Monitorowanie sprzedaży firm:** Agent przeszukuje Bizneski.pl, sprzedajbiznes.pl, ogłoszenia w MSiG (Monitor Sądowy i Gospodarczy) oraz zmiany własnościowe w KRS. Ocenia wiarygodność na podstawie spójności danych finansowych, wieku domeny firmy i historii KRS.

### 👤 13B — Budowanie Bazy Inwestorów i Profilowanie
- **Identyfikacja Inwestorów (HNWI & Instytucje):** Agent przeszukuje LinkedIn (sygnały statusu majątkowego), listy Forbes PL, bazy funduszy PE/VC (PFR, PSIK) oraz REIT-y aktywne w Polsce.
- **Mapowanie decydentów:** Wyciąganie danych zarządu (CEO, CFO, Dyrektor Inwestycji) przez KRS, LinkedIn Sales Navigator API, Clearbit oraz Hunter.io.
- **Analiza Sentymentu Preferencji:** Agent analizuje wywiady prasowe i posty decydentów na LinkedIn. Określa preferowaną klasę aktywów, ticket size (wartość transakcji), oczekiwaną stopę zwrotu (yield) oraz poziom tolerancji na ryzyko. Dane zapisuje jako ustrukturyzowany profil inwestora w HubSpot/Pipedrive przez API.

### 📄 13C — Przetwarzanie Dokumentacji i Tworzenie Ofert
- **Ekstrakcja RAG (Unstructured PDF/Skan):** Wykorzystanie Azure Document Intelligence lub Claude Vision jako skilla do odczytu operatów szacunkowych, wypisów z MPZP i pozwoleń na budowę.
- **Ekstrakcja Finansowa:** Automatyczne wyciąganie wskaźników NOI, Cap Rate, IRR, DSCR i generowanie uproszczonego modelu DCF (Discounted Cash Flow) w Google Sheets.
- **Generowanie Teasera / IM (Information Memorandum):** Agent kompiluje zdjęcia, mapy, analizę chłonności i dane prawne w profesjonalną ofertę PDF (język polski i angielski) dostosowaną do standardów RICS/MSCI.
- **Due Diligence Gaps:** Raport o brakach w dokumentach (np. brak zaświadczenia o dostępie do drogi publicznej, obciążenia w dziale III/IV KW).

### 🎯 13D — Silnik Matchingu (Matching Engine)
- **Algorytm dopasowania:** Scoring podobieństwa (od 0 do 100) między parametrami nowej oferty w bazie a zapisanymi preferencjami inwestorów.
- **Dynamiczne alerty:** Gdy nowa oferta ma matching >80% z danym funduszem, system natychmiast generuje spersonalizowaną zajawkę i wysyła powiadomienie do brokera (Telegram) oraz inwestora (WhatsApp/E-mail).

### 🚀 13E — Outreach, Cold Email i Budowanie Relacji
- **Zimne Kampanie (Instantly.ai / Lemlist):** Automatyczne dodawanie zweryfikowanych kontaktów do kampanii mailowych. Wiadomości są wysoce spersonalizowane (agent wplata wzmiankę o ostatniej transakcji funduszu lub ich publicznej strategii w Polsce).
- **RODO Compliance (Rynek PL):** Agent zarządza bazą opt-out. Wysyłka opiera się na prawnie uzasadnionym interesie B2B (art. 6 ust. 1 lit. f RODO). Każda kampania posiada automatyczny mechanizm usuwania danych na żądanie (Right to be Forgotten).

### 🚪 13I — Human Gate (Bariera Kontrolna)
Aby zapobiec kosztownym pomyłkom prawnym lub wizerunkowym, system działa w trybie **Human-in-the-Loop**:
1. Agent przygotowuje draft oferty (IM), listę dopasowanych inwestorów oraz treść wiadomości.
2. Wysyła komplet do zatwierdzenia na Telegramie brokera.
3. Broker klika **Approve** (Wyślij) lub **Modify** (np. *"zmniejsz cenę o 5%"*). Agent wykonuje poprawki i dopiero wtedy triggeruje kampanię.

---

## 🛠️ 3. Matryca Scoringowa Okazji (Scoring Rubric)

Wszelkie pobrane oferty są oceniane według poniższych wag (skala 1-100), dostosowanych do typu aktywów:

| Kryterium Oceny | Nieruchomości Komercyjne | Grunty Deweloperskie | Hale Przemysłowe | Gotowe Biznesy |
| :--- | :--- | :--- | :--- | :--- |
| **Lokalizacja i dojazd** | 30% | 20% | 35% | 15% |
| **Cena vs Wartość Rynkowa**| 25% | 25% | 20% | 30% |
| **Stan prawny (KW, MPZP/WZ)**| 15% | 30% | 15% | 15% |
| **Potencjał Yield / PUM** | 20% | 15% | 20% | 25% |
| **Infrastruktura i media** | 10% | 10% | 10% | 15% |
