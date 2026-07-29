# PRD: System Agentowy Jaison MLM OS dla społeczności Klub Fala Życia

Ten dokument określa wymagania biznesowe i techniczne (Product Requirements Document) dla inteligentnego systemu agentowego **Jaison MLM OS**, przeznaczonego do wsparcia i automatyzacji działań rekrutacyjnych oraz operacyjnych dla Partnerów Biznesowych (Brand Partners) grupy **Klub Fala Życia**.

---

## 1. Cel i wizja projektu (Executive Summary)

Tradycyjny marketing sieciowy (MLM) cierpi na wysokie tarcie operacyjne, chaos informacyjny, prokrastynację oraz brak powtarzalnej duplikacji. Nowi partnerzy gubią się w procedurach, tracą motywację po pierwszych odmowach i wymagają stałej, bezpośredniej asysty liderów (upline), co ogranicza skalowalność.

**Jaison MLM OS** rozwiązuje te problemy, działając jako **Asynchroniczny Cyfrowy Trener i Asystent** bezpośrednio w komunikatorze **WhatsApp**. 
System przejmuje 90% powtarzalnej pracy operacyjnej:
1. **Dba o biologię i energię partnera** od świtu (naukowy biohacking).
2. **Eliminuje pozorowanie pracy** poprzez podawanie gotowych, precyzyjnych szablonów rekrutacyjnych NLP.
3. **Zastępuje fizycznego sponsora (upline)**, dając natychmiastowe odpowiedzi merytoryczne i techniczne 24/7.
4. **Zarządza kalendarzem spotkań i CRM** w tle, zapobiegając utracie leadów.
5. **Integruje się z systemami automatyzacji (n8n/Cal.com)** i Kanałem Nadawczym WhatsApp.

---

## 2. Grupa docelowa (User Personas)

*   **Nowy Partner (Novice Partner):** Osoba bez doświadczenia w MLM, która obawia się odrzucenia, brakuje jej wiedzy merytorycznej o fototerapii i hydratacji X2O, łatwo ulega prokrastynacji i potrzebuje prowadzenia krok po kroku.
*   **Lider / Administrator Grupy (Upline Leader):** Doświadczona osoba budująca strukturę, której brakuje czasu na ciągłe szkolenie nowych partnerów i odpowiadanie na te same podstawowe pytania produktowe i techniczne.
*   **Tomasz / Właściciel Ekosystemu:** Wizjoner orkiestrujący całą architekturę, optymalizujący konwersję i automatyzujący przepływy danych.

---

## 3. Architektura Systemu (Core Architecture)

System opiera się na stabilnej, modularnej strukturze chmurowej:
*   **Silnik Bazowy:** **Hermes Agentic OS** (wyspecjalizowany system operacyjny dla agentów chmurowych).
*   **Mechanizm Klonowania (CloneJobs):** Wykorzystanie platformy **Kili** do uruchamiania i synchronizacji niezależnych instancji agenta dla każdego Partnera Biznesowego (pełna duplikacja profilu i wiedzy).
*   **Główny interfejs (UI/UX):** **WhatsApp API** (asynchroniczny, dwukierunkowy czat tekstowo-głosowy).
*   **Integracje Zewnętrzne:** 
    *   **Cal.com / Cal.eu:** Rezerwacja spotkań i kwalifikacji biznesowych.
    *   **n8n Automation:** Przepływy danych o leadach, powiadomienia o webinarach i wydarzeniach.
    *   **Google Cloud Storage / Firestore:** Przechowywanie stanów, logów rozmów oraz plików spersonalizowanych profili.

---

## 4. Kluczowe Funkcjonalności i Wymagania

### Filar A: Orkiestracja Dnia i Biologia (Protokół V2)
*   **06:30 rano - Zapłon Biologiczny:** Agent wysyła powiadomienie zapobiegające bezmyślnemu scrollowaniu social mediów. Wymaga raportu z wykonania procedury: szklanka wody X2O z solą kłodawską, 15 sekund tlenowego pobudzenia, zimny prysznic. Wykonanie podnosi poziom dopaminy o +250% i aktywuje energię do działania.
*   **Wsparcie Kryzysowe 24/7:** W przypadku spadku motywacji, zmęczenia lub prokrastynacji partner pisze do bota. Bot nie wysyła pustych motywacyjnych sloganów, lecz diagnozuje biologię (oddechy, nawodnienie, zmiana fizjologii).

### Filar B: Rekrutacja bez Stresu i Szablony NLP
*   **08:00 rano - Kopiuj-Wklej NLP:** Agent podaje dokładnie 3 wysoce konwertujące szablony marketingowe/rekrutacyjne na dany dzień, dostosowane do platform (LinkedIn, Facebook, WhatsApp). Partner kopiuje, wysyła i zamyka rekrutację w kilka minut.
*   **Zasada Posłańca:** Agent uczy partnerów unikania samodzielnego prezentowania marki przed kwalifikacją (co powoduje "wyciekanie" leadów do wyszukiwarek). Partner jest tylko lekarzem stawiającym diagnozę i podającym właściwy film/prezentację systemową.

### Filar C: Kalendarz i Mobilny CRM z WhatsAppa
*   **Integracja CRM:** Partner może dodawać, kategoryzować i monitorować status potencjalnych partnerów (leadów) bezpośrednio na czacie WhatsApp (np. wpisując komendę lub w asynchronicznym dialogu).
*   **Zarządzanie Spotkaniami:** Jaison integruje się z osobistym kalendarzem partnera na Cal.com/Cal.eu. Wysyła automatyczne powiadomienia o nadchodzących rozmowach rekrutacyjnych, webinarach, spotkaniach zespołowych i webinarach produktowych.
*   **Kanał Nadawczy:** Bezpośrednie połączenie z oficjalnym kanałem WhatsApp grupy **Klub Fala Życia** w celu dystrybucji kluczowych ogłoszeń i aktualizacji.

### Filar D: Personalizacja, Uczenie i Plik GHOST
*   **Uczenie Nawyków i Problemów:** Jaison stale analizuje wyzwania, z jakimi mierzy się partner (np. blokady psychiczne, brak czasu, trudne pytania od klientów) i dostosowuje do nich ton oraz podawane porady.
*   **Generowanie Pliku GHOST:** Agent tworzy i stale aktualizuje plik konfiguracyjny `.ghost` dla każdego partnera. Plik ten precyzyjnie definiuje jego styl komunikacji, unikalny ton marki osobistej, preferencje oraz mocne strony. Dzięki temu asystent pisze wiadomości dokładnie tak, jak napisałby je dany człowiek.

### Filar E: Zastępstwo Sponsora (Upline 24/7)
*   **Kompletna Baza Wiedzy:** Agent ma wbudowany dostęp do pełnej wiedzy Klubu Fala Życia, badań naukowych o fototerapii (np. działanie peptydów GHK-Cu, technologia X39, X2O) oraz struktur biznesowych.
*   **Asysta w Rozmowie:** Jeśli potencjalny klient zada trudne pytanie, partner przesyła je do Jaisona na WhatsAppie i natychmiast otrzymuje profesjonalną, naukowo poprawną i zgodną z NLP odpowiedź do wklejenia.

---

## 5. Metryki Sukcesu i KPIs (Key Performance Indicators)

*   **Retencja Partnerów (Retention Rate):** Wzrost odsetka partnerów aktywnych po 30, 60 i 90 dniach od rejestracji (zapobieganie rezygnacjom dzięki stałemu prowadzeniu przez Jaisona).
*   **Duplikowalność (Duplication Velocity):** Skrócenie czasu od rejestracji nowego partnera do wysłania przez niego pierwszych 3 prezentacji wideo (cel: poniżej 24 godzin).
*   **Wydajność Czasowa (Time Efficiency):** Zmniejszenie o 80% czasu, jaki liderzy muszą poświęcać na odpowiadanie na pytania merytoryczne i techniczne w strukturze.
*   **Konwersja Spotkań (Booking Conversion):** Procent zaplanowanych i pomyślnie przeprowadzonych rozmów kwalifikacyjnych z kalendarza Cal.eu.

---

## 6. Harmonogram i Fazy Wdrożenia

1.  **Faza 1 (Aktualna):** Przygotowanie stron landing page (`x2o.jaison.pl` oraz `mlm.jaison.pl`) zapowiadających start i oferujących szybką kwalifikację biznesową przez Cal.eu.
2.  **Faza 2:** Konfiguracja n8n oraz integracja bazowa z WhatsApp Business API.
3.  **Faza 3:** Wdrożenie bazy wiedzy o fototerapii i planu kompensacyjnego Klubu Fala Życia do silnika Hermesa.
4.  **Faza 4:** Uruchomienie testowych instancji CloneJobs dla administratorów i zbieranie pierwszych plików Ghost.
5.  **Faza 5:** Pełny Product Launch dla całej społeczności Klub Fala Życia.homienie testowych instancji CloneJobs dla administratorów i zbieranie pierwszych plików Ghost.
5.  **Faza 5:** Pełny Product Launch dla całej społeczności Klub Fala Życia.
