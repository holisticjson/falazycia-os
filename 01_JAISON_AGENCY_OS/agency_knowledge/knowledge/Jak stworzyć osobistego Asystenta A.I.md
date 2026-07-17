Poniżej przedstawiam destylowaną wiedzę z dostarczonego materiału:

### 1. Główne zasady / ramy logiczne (Frameworki)

#### **Czym jest Osobisty Asystent AI?**
*   Inteligentny agent, który działa obok Ciebie, ma dostęp do Twoich plików i projektów, pamięta kontekst rozmów i wykonuje zadania automatycznie.
*   Działa 24/7, nie wymaga urlopu.

#### **Poziomy Asystenta AI:**
*   **Poziom 0 (Status quo):**
    *   Dużo ręcznej pracy, brak kontekstu, brak dostępu do plików.
    *   Ograniczenie do narzędzi takich jak ChatGPT/Claude/Gemini bez integracji z ekosystemem użytkownika.
    *   Praca oparta na ciągłym kopiuj-wklej.
*   **LEVEL 1 - Lokalny:**
    *   Wykorzystuje **Obsidian + Claude Code**.
    *   Działa lokalnie na Twoim komputerze.
    *   Integruje się z Twoimi osobistymi danymi i notatkami.
*   **LEVEL 2 - W chmurze:**
    *   Wykorzystuje **Open Claw + VPS**.
    *   Działa online, dostępny z telefonu i innych urządzeń.
    *   Oferuje szersze możliwości integracji i automatyzacji.

#### **Dlaczego Obsidian jest rekomendowany (dla LEVEL 1)?**
*   Służy jako centralne miejsce na notatki i dokumenty, wszystko przechowywane lokalnie na komputerze (brak chmury domyślnie).
*   Zero konfiguracji, zero płatnych wtyczek, działa od razu.
*   Konsoliduje zadania, projekty, wpisy na social media, notatki ze spotkań, konsultacje – zastępuje wiele aplikacji jednym folderem.
*   Agent AI ma dostęp do tych samych plików, rozumiejąc kontekst Twojej pracy, celów i stylu komunikacji.

#### **OPENCLAW - Zasady działania zaawansowanego agenta AI (LEVEL 2):**
1.  **Autonomia:** Działa samodzielnie, bez ciągłego nadzoru. Wysyła poranne podsumowania.
2.  **Prywatność Danych:** Wszystkie dane pozostają na Twoim serwerze (VPS), bez dostępu firm trzecich.
3.  **Wielokanałowość:** Jeden agent obsługuje wiele kanałów komunikacji (WhatsApp, Discord, mail, Twitter).
4.  **Pamięć Kontekstowa:** Pamięta wszystko, co robiliście, ma dostęp do plików z wiedzą o Tobie i biznesie.
5.  **Optymalizacja Kosztów:** Wykorzystuje tańsze modele AI do prostych zadań, mocniejsze do złożonych.
6.  **Zespół Agentów:** Główny agent deleguje zadania do wyspecjalizowanych pomocników (np. researcher, copywriter, koder).
7.  **Konfiguracja Tekstem:** Nauka i rozbudowa agenta odbywa się za pomocą pisania instrukcji, bez programowania.
8.  **Przeglądanie Internetu:** Agent potrafi otwierać strony, klikać, wypełniać formularze, zbierać dane.

#### **Główne Funkcjonalności Osobistego Asystenta AI (podsumowanie):**
*   Zbieranie źródeł (X, YT, Reddit, Voice Ink).
*   Pisanie w Twoim stylu (Voice of Tone).
*   Usuwanie artefaktów AI (AI Patterns).
*   Generowanie grafik i publikacja (np. na LinkedIn).
*   Transkrypcja spotkań i generowanie listy zadań.
*   Automatyzacja komunikacji (maile, DM).
*   Organizacja plików i danych (drugi mózg).
*   Monitorowanie postępów i celów.
*   Research i analiza (konkurencji, rynku, treści).
*   Zarządzanie czasem i zadaniami (kalendarz, przypomnienia, daily brief, weekly check-in).
*   Tworzenie i edycja dokumentów/plików (w tym kodu).
*   Działanie w tle (gdy śpisz), walidacja pomysłów biznesowych.

### 2. Gotowe schematy, prompty lub szablony

*   **Prompt-Persona.md** (szablon do zdefiniowania osobowości agenta)
*   **Prompt-Soul.md** (szablon do zdefiniowania "duszy" agenta, jego głównych wartości/celów)
*   **Skill-/reflect** (prawdopodobnie szablon do definiowania umiejętności i procesów refleksji agenta, np. `skill_reflect.md`)
*   **Ralph TUI:** Terminal User Interface dla agentów AI, dostępny na GitHub.
    ```
    https://github.com/subsy/ralph-tui
    ```

### 3. Konkretne instrukcje "Krok po Kroku"

#### **Jak zbudować Osobistego Asystenta AI (LEVEL 1):**
1.  **Instalacja:** Zainstaluj Obsidian + Claude Code.
2.  **Konfiguracja Katalogu:** Ustaw katalog projektowy w Obsidian.
3.  **Dodanie Wiedzy:** Dodaj wiedzę o sobie i swoich projektach do Obsidian (pliki tekstowe, notatki).
4.  **Dodanie Umiejętności:** Dodaj "skill'e" (instrukcje/zasady działania) dla agenta, a następnie pracuj nad jego rozwojem.

#### **Workflow przykład (LEVEL 1):**
1.  **Polecenie:** Wydajesz polecenie w Claude Code.
2.  **Akcja:** Claude Code tworzy lub edytuje plik (np. kod, tekst).
3.  **Widoczność:** Zmiana lub nowe zadanie jest widoczne/zintegrowane w Obsidian.

#### **Typowe scenariusze użycia Open Claw (LEVEL 2):**
1.  **Morning Briefing:** Codziennie rano (np. 7:00) otrzymujesz na telefon podsumowanie najważniejszych informacji/zadań, które agent "ogarnął".
2.  **Tygodniowy Research:** Co poniedziałek agent przeszukuje Reddit, YouTube i X (Twitter) w Twojej branży, dostarczając istotne informacje.
3.  **Auto-Reply na DM:** Agent automatycznie odpowiada na wiadomości prywatne (np. o 3 w nocy), wysyła materiały i zbiera kontakty.
4.  **Agent jako Pracownik:** Agent otrzymuje własny adres e-mail, kalendarz i dostęp do narzędzi, funkcjonując jako członek zespołu.

#### **Jak uruchomić Asystenta AI (LEVEL 2):**
*   **Opcja 1: Serwer VPS (rekomendowane):**
    *   **Wynajem:** Wynajmij serwer w chmurze (np. Hostinger) za około 7-8 USD/miesiąc (ok. 30 PLN).
    *   **Konfiguracja:** Uruchom i skonfiguruj Open Claw na VPS.
    *   **Korzyści:** Działa 24/7, nie zajmuje miejsca na biurku, nie zużywa Twojego prądu/internetu. Agent działa nawet jeśli padnie Twoje domowe Wi-Fi.
*   **Opcja 2: Własny sprzęt:**
    *   **Wymagania:** Stary laptop lub komputer z minimum 6-8 GB RAM.
    *   **Warunki:** Musi być włączony 24/7 i podłączony do internetu.
    *   **Uwaga:** Nie zaleca się kupowania nowego sprzętu (koszt ok. 3000 PLN) – stary laptop lub VPS są wystarczające i bardziej ekonomiczne.

#### **Źródła i narzędzia:**
*   **Claude Code by Anthropic:** AI Coding Agent, Terminal, IDE.
*   **Obsidian:** Aplikacja do notatek, baza wiedzy.
*   **Hostinger:** Przykładowy dostawca usług VPS.