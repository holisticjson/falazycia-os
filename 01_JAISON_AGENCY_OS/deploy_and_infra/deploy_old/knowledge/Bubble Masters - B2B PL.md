## Destylacja Wiedzy z Kursu "Bubble Masters"

### I. Główne zasady / ramy logiczne (Frameworki)

*   **Strategia Produktowa:**
    *   **Szukanie nisz produktowych i pomysłów.**
    *   **Walidacja z użytkownikami** (zadawanie właściwych pytań).
    *   Decyzja o użyciu **gotowych design-systemów dla Bubble** (np. Atomicfusion, Frames, Deezign, Framify) lub projektowanie od "0".
    *   Podejście **"API first"** w budowaniu produktu.
    *   Zrozumienie **możliwości modeli AI i inteligentnych asystentów** w produktach.
    *   **Asystent AI jako wyróżnik** produktu.
    *   Zasady działania i **obecne ograniczenia modeli AI**.
*   **Architektura Aplikacji Bubble:**
    *   **Projektowanie produktu i prototypowanie** (papier - Figma - Bubble).
    *   **Łączenie logiki Bubble i back-endu** z produktem.
    *   Wykorzystanie **baz danych w Bubble** (jako alternatywa dla Airtable).
    *   Wykorzystanie **Workflows w Bubble** (jako alternatywa dla Make i Zapier).
    *   Implementacja **Kont użytkowników w Bubble**.
    *   **Wydajność aplikacji Bubble**: Zrozumienie Workflow Units, analizowanie Server log.
    *   **Bezpieczeństwo**: Stosowanie privacy rules jako sposób ograniczania dostępu.
    *   **Skalowanie**: Wykorzystanie API Connector i SQL connector, XANO, multiple frontends i jeden wspólny backend.
*   **Dobre Praktyki:**
    *   **Projektowanie Front-end:**
        *   Nazewnictwo elementów.
        *   Single page applications.
        *   Reużywalne komponenty (i ich ograniczenia).
        *   Stosowanie stylów.
    *   **Logika Aplikacji:**
        *   Wykorzystanie option sets.
        *   Katalogowanie workflows.
        *   Debugowanie + logi aplikacji.
    *   **Integracje API:**
        *   Bezpieczeństwo API.
        *   Katalogowanie i dokumentowanie endpointów.
    *   **Integracja AI:**
        *   Jak pisać prompty.
        *   Jak zabezpieczać dane.
        *   Jak komunikować wykorzystanie AI dla użytkowników.
    *   **Skalowanie i Rozbudowa:**
        *   Wykorzystanie skryptów do optymalizacji workflow units.
        *   Różne sposoby komunikacji z backend.
        *   Tworzenie skalowalnej architektury aplikacji.

### II. Gotowe schematy, prompty lub szablony (1:1 do skopiowania)

*   **Projektowanie Produktu (Szkic):**
    *   **★ Przygotowanie szkicu produktu:** Podstawowe założenia, nazwa, logo, projekt landing page.
*   **Lista Narzędzi:**
    *   **Lista najpopularniejszych pluginów w Bubble, które "musisz" mieć.** (Zawartość listy do uzyskania w kursie).
    *   **Źródła ogólnodostępnych API do wykorzystania w twojej aplikacji.** (Lista źródeł do uzyskania w kursie).
*   **Podręczniki / Zasoby:**
    *   **Podręcznik/eBook "Bezpieczeństwo w Bubble" ✔.**

### III. Konkretne instrukcje "Krok po Kroku"

*   **Faza 1: Koncepcja i Prototypowanie**
    1.  **"Wymyślanie" nazwy + logo z AI.**
    2.  **Tworzenie landing page bez kodowania.**
    3.  **Projektowanie produktu i prototypowanie** (papier - Figma - Bubble).
*   **Faza 2: Budowa Interfejsu (Front-end)**
    1.  **Projektowanie responsywnego interfejsu** w Edytorze Bubble.
    2.  Konfigurowanie **układu strony, komponentów layoutu, formularzy.**
    3.  Integracja **pluginów front-endowych.**
    4.  **Przenoszenie komponentów z Figmy do Bubble** lub z Webflow.
    5.  **Pierwszy projekt dashboardu**: menu, nawigacja, formularz i workflows.
    6.  **Budowa dashboardu aplikacji** z formularzem do wprowadzania danych.
    7.  **★ Rozbudowa formularza** o dodatkowe pola i kategorie.
*   **Faza 3: Logika Aplikacji (Back-end i Użytkownicy)**
    1.  **Projektowanie bazy danych** dla swojego produktu.
    2.  Implementacja **Workflows** w Bubble.
    3.  Przeprowadzanie **operacji na danych i ich wyświetlanie**.
    4.  **Wizualizacja danych.**
    5.  **Zakładanie kont użytkownika** i umożliwienie logowania.
*   **Faza 4: Integracje Zewnętrzne (API)**
    1.  Rozumienie **API** (zasada działania, autoryzacja dostępu, metody REST API, JSON, Webhooks).
    2.  **Łączenie produktu z zewnętrznymi aplikacjami** za pomocą Bubble API Connector.
    3.  **Udostępnianie danych aplikacji na zewnątrz** poprzez API Bubble.
    4.  Użycie **Backend workflows udostępnianych jako API.**
    5.  Użycie **Data API i Actions API.**
    6.  Wykorzystanie **pluginów jako alternatywa do ręcznej budowy API.**
    7.  **Pobieranie danych z zewnętrznej aplikacji** i zapisywanie ich w bazie danych Bubble.
    8.  **Wyświetlanie pobranych danych w aplikacji.**
    9.  **★ Udostępnienie danych z naszej aplikacji jako zewnętrzne API.**
*   **Faza 5: Integracja AI**
    1.  **Własna integracja AI** (np. OpenAI) z Bubble.
    2.  Wykorzystanie **pluginów** do integracji AI.
    3.  Tworzenie **asystenta OpenAI w Bubble**, który korzysta z danych aplikacji.
    4.  Implementacja **przetwarzania obrazu** przez asystenta.
    5.  Implementacja **przetwarzania dźwięku** (komunikacja głosowa z aplikacją).
    6.  **Wykorzystanie danych z Bubble w OpenAI** do zapytań i generowania treści.
    7.  Konfigurowanie **odpowiedzi asystenta** i personalizowanie stylu odpowiedzi.
    8.  **Działający asystent AI** jako dodatek do aplikacji.
    9.  **★ Komunikacja głosowa z asystentem.**
*   **Faza 6: Skalowanie i Publikacja**
    1.  **Analizowanie Logów aplikacji** i wyciąganie wniosków dotyczących Workflow Units.
    2.  **Zabezpieczanie aplikacji** przed nieautoryzowanym dostępem.
    3.  Wykorzystanie **API Connector** do zewnętrznych baz danych.
    4.  Wykorzystanie **Xano Connector plugin** jako źródła danych.
    5.  **Podłączanie dwóch front-endów** do jednego back-endu w aplikacji Bubble.
    6.  **Publikowanie aplikacji**: wersja testowa, debugger, publikowanie pod własną domeną.
    7.  **Publikowanie aplikacji w wersji mobilnej** w sklepie Google i Appstore.
    8.  **Aplikacja wykorzystująca jako backend XANO.**
    9.  **★ Wersja mobilna aplikacji Bubble.**

### Warsztaty Live (dodatkowe instrukcje krok po kroku):

*   **"Bubble for rookies":** Logika działania edytora Bubble.
*   **Nocoding - Przenoszenie komponentów:** Przenoszenie komponentów z Figma do Bubble, tworzenie nawigacji, reużywalne menu, tworzenie formularza, wprowadzenie do workflows.
*   **Nocoding - Bazy danych:** Projektowanie bazy danych, zapisywanie danych do bazy, wyświetlanie danych z bazy w dashboardzie, publikowanie aplikacji.
*   **Nocoding - Integracja API:** Połączenie z zewnętrznym API, wyświetlanie danych z zewnętrznego API, zapisywanie w bazie danych z zewnętrznego API, udostępnienie danych dla innych aplikacji.
*   **Nocoding - Interfejs asystenta AI:** Połączenie z OpenAI, zapisywanie danych w bazie, wyświetlanie danych z OpenAI w aplikacji.
*   **Nocoding - Integracja XANO:** Połączenie aplikacji z zewnętrznym back-endem (XANO).