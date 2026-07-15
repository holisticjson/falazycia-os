# Hermes Agent OS — Blueprint Systemowy

## Streszczenie operacyjne

Tutorial przedstawia pięć konkretnych przypadków użycia Hermes Agent wykraczających daleko poza podstawowe promptowanie w terminalu. Wynikający z niego model systemowy to: **agentowy system operacyjny z trwałą pamięcią, zautomatyzowanymi workflow'ami i pętlą autonomicznego działania**. Kluczowe przesunięcie myślowe: Hermes nie jest chatbotem — jest środowiskiem wykonawczym dla agentów, który wymaga architektury, nie tylko promptów.

---

## Czym jest opisywany system / metoda / framework

Hermes Agent OS to lokalne środowisko agentowe zbudowane wokół kilku warstw:

1. **Rdzeń wykonawczy** — Hermes Agent jako orchestrator (zastępuje klasyczne używanie CLI / terminala)
2. **Warstwa pamięci** — Obsidian + Infinite Context Engine (permanentna, przeszukiwalna baza wiedzy o użytkowniku, jego projektach i priorytetach)
3. **Warstwa skilli** — rozszerzalne moduły (np. Hyperframes do generowania wideo, Goal Mode do autonomicznych zadań)
4. **Warstwa dashboardu** — własny Agent Operating System (AOS) zamiast terminala: historia, podgląd, Kanban, orkiestracja wielu agentów
5. **Warstwa integracji** — zewnętrzne API i narzędzia (OpenRouter, Omi, Indexceptional, Claude, OpenClaude/OpenClod, Gemini, Obsidian)

Filozofia: **każda sesja agentowa powinna startować z kontekstem, nie od zera.** System buduje się raz, a potem sam się wzbogaca.

---

## Główne filary / komponenty / warstwy

### 1. Generowanie wideo — Skill Hyperframes
- Otwarto-źródłowy skill `Hyperframes` wbudowany w Hermes
- Konwertuje opisy tekstowe na HTML → następnie renderuje do animowanego wideo
- Możliwość wstawienia AI avatara
- Darmowe API: **Owl Alpha** przez **OpenRouter** (1 milion tokenów kontekstu, bezpłatne)
- Output trafia bezpośrednio do workspace Hermes — brak przełączania narzędzi

### 2. Pamięć długoterminowa — Infinite Context Engine (ICE)
- Baza: **Obsidian** (lokalna aplikacja, notatki jako plain .md files)
- Hermes automatycznie zapisuje każdą sesję do Obsidian vault
- Każda kolejna sesja ładuje kontekst z vault — system „zna" użytkownika bez re-wprowadzania kontekstu
- Uzupełnienie: **Omi** (open source) — automatycznie zbiera codzienne notatki i wpycha do Obsidian bez pisania
- Po kilku tygodniach działania vault wie o użytkowniku więcej niż on sam o sobie
- Kluczowa właściwość: **pamięć rośnie automatycznie — pasywnie**

### 3. Automatyzacja SEO / treści — Content Machine
- Hermes pobiera kontekst z ICE (case studies, persona, wyniki klienta)
- Generuje optymalizowany artykuł pod konkretne słowo kluczowe
- Deployuje artykuł bezpośrednio na stronę (automatyczne wdrożenie)
- Integracja z **Indexceptional API** → artykuł zaindeksowany i rankujący w ciągu ~4 dni
- Przewaga nad generycznym AI: treść zawiera prawdziwe case studies i doświadczenia — co Google 2026 premiuje jako „first-hand experience"

### 4. Agent Operating System (AOS) — Dashboard Centralny
- Własny dashboard na lokalnej maszynie (generowany przez Hermes/Claude na żądanie)
- Zawiera: historia wszystkich sesji, podgląd outputów, przełączanie między agentami (Hermes, Claude, OpenClaude, Gemini)
- **Kanban board** — zadania drop-in → automatyczny podział na subtasks → przypisanie do właściwego agenta → oznaczenie jako done
- Orkiestrator automatycznie zarządza rozbiciem zadania i routingiem do agentów
- Jeden ekran = pełna kontrola nad całym ekosystemem agentów

### 5. Goal Mode — Autonomiczne wykonanie zadań
- Wbudowany skill Hermes: tryb celowy (`goal mode`)
- Użytkownik wpisuje cel (np. „napisz i opublikuj 5 artykułów")
- Po każdej turze **lekki model-sędzia** ocenia: czy cel jest osiągnięty? Tak → koniec. Nie → Hermes generuje kolejny prompt i kontynuuje
- Domyślnie: **20 tur** przed zatrzymaniem i prośbą o check-in
- Tryb „idź spać, wróć rano — praca jest zrobiona"

---

## Architektura logiki

| Warstwa | Komponent | Rola |
|---------|-----------|------|
| **Pamięć** | Obsidian Vault (ICE) | Trwały kontekst użytkownika, projekty, case studies, historia sesji |
| **Pamięć pasywna** | Omi | Automatyczne zbieranie codziennych notatek → Obsidian |
| **Procedura** | Skill Hyperframes | Konwersja tekstu → HTML → wideo |
| **Procedura** | Content Machine | Keyword + kontekst → artykuł → deploy → indeksowanie |
| **Sterowanie** | Agent OS Dashboard | Routing zadań, historia, podgląd, koordynacja agentów |
| **Sterowanie** | Orchestrator (Kanban) | Automatyczny podział zadania na subtasks, przypisanie agentów |
| **Harmonogram** | Goal Mode (Judge Loop) | Pętla do 20 tur, autonomiczne iterowanie aż do ukończenia celu |
| **Warstwa wykonawcza** | Hermes, Claude, OpenClaude, Gemini | Wykonanie konkretnych zadań przypisanych przez orchestrator |
| **Warstwa bezpieczeństwa** | Judge Model | Ocena postępu i decyzja o kontynuacji lub zatrzymaniu |
| **Warstwa integracji** | OpenRouter (Owl Alpha API), Indexceptional, Omi | Zewnętrzne API łączące komponenty systemu |

---

## Workflow wdrożeniowy

### Etap 0 — Instalacja i środowisko (przed jakimkolwiek użyciem)
1. Zainstaluj Hermes Agent
2. Podłącz darmowe API Owl Alpha przez OpenRouter (1M token context, bezpłatne)
3. Zainstaluj Obsidian na lokalnej maszynie

### Etap 1 — Budowanie pamięci (ICE)
4. Skonfiguruj Hermes tak, żeby po każdej sesji zapisywał rozmowę do Obsidian vault
5. Opcjonalnie: zainstaluj Omi → automatyczne codzienne notatki → Obsidian
6. Daj systemowi działać 1-2 tygodnie → vault zaczyna być użyteczny

### Etap 2 — Agent Operating System
7. Wejdź do Hermes lub Claude i opisz dashboard jaki chcesz (agenci, layout, potrzeby)
8. Hermes generuje kod dashboardu i uruchamia go lokalnie
9. Dashboard zawiera: historię sesji, Kanban, przełącznik agentów, podgląd outputów

### Etap 3 — Skille i integracje
10. Włącz skill `Hyperframes` → możliwość generowania wideo z promptu
11. Skonfiguruj integrację Indexceptional API → automatyczne indeksowanie treści
12. Podłącz agenta SEO: keyword + ICE kontekst → artykuł → auto-deploy

### Etap 4 — Goal Mode
13. Przejdź do Goal Mode w Hermes
14. Wpisz duże zadanie jako cel
15. Ustaw limit tur (domyślnie 20), odejdź — system pracuje autonomicznie

---

## Zasady operacyjne

### Kiedy używać terminala
- **Nie używaj terminala jako podstawowego interfejsu** — nie ma historii, nie ma podglądu, outputy znikają
- Terminal = wyłącznie diagnostyka lub jednorazowe szybkie testy
- Do pracy produkcyjnej: zawsze przez AOS Dashboard

### Kiedy używać Goal Mode
- Przy dużych, wieloetapowych zadaniach (pisanie artykułów, budowanie funkcji, kampanie)
- Gdy możesz odejść od komputera na ≥30 minut
- Gdy zadanie jest dobrze zdefiniowane i nie wymaga interaktywnych decyzji po drodze
- **Nie używaj** dla zadań, które wymagają Twojej decyzji w połowie procesu

### Kiedy aktualizować ICE (pamięć)
- System aktualizuje się automatycznie po każdej sesji
- Ręczna aktualizacja: gdy zmieniają się priorytety, klienci, projekty
- Zasada: im więcej kontekstu w vault → tym lepsze outputy agenta

### Kiedy tworzyć nowy skill vs. używać istniejącego
- Istniejący skill: zadania powtarzalne, dobrze zdefiniowane (wideo, SEO, indeksowanie)
- Nowy skill: gdy powtarzasz te same sekwencje promptów więcej niż 3 razy
- Modularyzuj wcześnie — łatwiej przebudować jeden skill niż cały workflow

### Jak rozpoznać, że system wymaga naprawy
- Agent zaczyna pytać o rzeczy, które powinien wiedzieć z kontekstu → ICE nie działa / nie jest ładowany
- Outputy są generyczne, bez personalnej wiedzy → vault jest pusty lub nie podłączony
- Zadania w Kanban nie są kończone → orchestrator nie rozbija zadań lub zły routing

---

## Best practices

### 1. Context-first zawsze
Przed każdym zadaniem zasilaj agenta kontekstem z ICE. Nigdy nie zakładaj, że agent „pamięta" — weryfikuj, że vault jest załadowany do sesji.

### 2. Workspace zamiast terminala
Każdy output powinien lądować w workspace Hermes / dashboardzie — możliwy do przejrzenia, wyszukania, wznowienia. Terminal = czarna dziura.

### 3. Pasywna budowa pamięci
Nie buduj pamięci manualnie. Ustaw automatyczny zapis sesji + Omi do codziennych notatek. Vault powinien rosnąć bez Twojego wysiłku.

### 4. Treść = tożsamość + wyniki
W content machine: zawsze ładuj case studies i własne wyniki do kontekstu przed generowaniem artykułu. Generic AI = generic content. Kontekstowy AI = treść z „first-hand experience" = lepsza widoczność w Google 2026.

### 5. Kanban jako system przydziału zadań
Nie dawaj agentom jednego długiego promptu. Wrzuć zadanie do Kanbana → orchestrator rozbija je na subtasks → każdy subtask trafia do właściwego agenta. Mniejsze zadania = wyższa jakość outputów.

### 6. Judge loop jako mechanizm jakości
Goal Mode z modelem-sędzią to wbudowany QA. Nie musisz sprawdzać każdej tury — system sam ocenia czy cel jest osiągnięty. Ustaw cel precyzyjnie → sędzia działa lepiej.

### 7. Modularność narzędzi
System jest modularny z założenia: Hermes + Claude + OpenClaude + Gemini = różne agenty do różnych zadań. Nie zmuszaj jednego agenta do wszystkiego.

### 8. Darmowe API jako point of entry
Owl Alpha (OpenRouter) + Obsidian (free, lokalny) + Omi (open source) = pełny stack wejściowy bez kosztów. Nie płać za stack, dopóki nie udowodnisz wartości systemu.

---

## Security / ryzyka / ograniczenia

### Podejście do bezpieczeństwa
- Obsidian vault jest lokalny (plain files na maszynie) — dane nie wychodzą do chmury
- Omi jako open source — weryfikuj samodzielnie co zbiera i dokąd wysyła
- OpenRouter jako pośrednik API — sprawdź warunki przechowywania zapytań

### Ograniczenia systemu
- **Goal Mode: 20 tur** — duże zadania mogą wymagać re-startu; planuj zadania na ≤20 kroków lub dziel na etapy
- **Context window Owl Alpha: 1M tokenów** — przy bardzo dużych vaultach możliwy overflow; regularnie archiwizuj stare notatki
- System nie jest „samonaprawiający się" — jeśli orchestrator źle rozbije zadanie, trzeba zainterweniować manualnie

### Zasady uprawnień
- Agent AOS działa lokalnie — ogranicz dostęp do zewnętrznych systemów (np. auto-deploy na stronę) do konkretnych, skonfigurowanych integracji
- Indexceptional API: klucz przechowuj w bezpiecznym miejscu, nie w promptach ani vault

### Obchodzenie się z danymi
- Nie wkładaj do vault danych wrażliwych (hasła, klucze API, dane klientów bez zgody)
- Vault jest źródłem kontekstu agenta — wszystko co tam jest, trafia do modelu

---

## Skalowanie / delegowanie / modularność

### Decision tree: kiedy zostać przy jednym agencie, kiedy rozdzielić

```
Zadanie jednorodne (np. jeden artykuł, jedna analiza)?
  └─ TAK → jeden agent (Hermes lub Claude)
  └─ NIE → Kanban + orchestrator → wiele agentów

Zadanie wymaga specyficznej wiedzy domenowej?
  └─ TAK → dedykowany agent z załadowanym kontekstem domenowym
  └─ NIE → generyczny agent z ICE

Zadanie ma >5 kroków lub zajmuje >20 minut?
  └─ TAK → Goal Mode (20 tur) lub podział na etapy
  └─ NIE → bezpośredni prompt

Zadanie powtarza się regularnie?
  └─ TAK → zamień w skill / SOP / playbook
  └─ NIE → ad-hoc prompt
```

### Jak myśleć o wzroście złożoności
- **Poziom 1** (start): Hermes + Obsidian ICE + jeden skill
- **Poziom 2** (po 2-4 tygodniach): AOS Dashboard + Kanban + Goal Mode
- **Poziom 3** (po miesięcy): multi-agent workflow z dedykowanymi rolami (SEO agent, video agent, content agent, orchestrator)
- Zasada: dodawaj warstwę dopiero gdy aktualna staje się bottleneckiem — nie wcześniej

### Kiedy tworzyć osobne moduły
- Gdy jeden agent robi ≥3 różne typy zadań → rozdziel na wyspecjalizowane agenty
- Gdy vault zaczyna mieszać tematy → stwórz osobne vault'y lub sekcje per projekt/klient
- Gdy Goal Mode nie kończy zadania w 20 turach → zadanie jest za duże → podział na etapy jako osobne cele

---

## Antywzorce i błędy

| Antywzorzec | Dlaczego to problem | Rozwiązanie |
|-------------|---------------------|-------------|
| Praca wyłącznie w terminalu | Brak historii, brak podglądu, outputy znikają | Używaj AOS Dashboard |
| Każda sesja startuje od zera | Marnowanie czasu na re-introdukcję kontekstu | Ustaw ICE + auto-zapis sesji |
| Jeden długi prompt jako zadanie | Agent traci focus, niska jakość | Kanban + subtasks + orchestrator |
| Generowanie treści bez kontekstu | Generyczna treść, słaba w SEO 2026 | Zawsze ładuj case studies i ICE przed generowaniem |
| Ręczne budowanie pamięci | Nietrwałe, nie skaluje się | Omi + automatyczny zapis sesji |
| Używanie jednego agenta do wszystkiego | Brak specjalizacji, gorsze wyniki | Multi-agent AOS z routingiem zadań |
| Goal Mode bez precyzyjnego celu | Sędzia nie może ocenić ukończenia | Definiuj konkretny, mierzalny cel przed uruchomieniem |
| Brak indeksowania po deploy | Treść rankuje wolno lub wcale | Zawsze integruj Indexceptional po publikacji |

---

## Reguły do przeniesienia do mojego systemu

Gotowe zasady systemowe do wklejenia do Antigravity / agenta / knowledge base:

```
REGUŁA 1 — CONTEXT-FIRST
Każda sesja agentowa musi startować z załadowanym kontekstem z bazy wiedzy.
Nigdy nie zakładaj, że agent pamięta poprzednią sesję.

REGUŁA 2 — NO TERMINAL PRODUCTION
Praca produkcyjna odbywa się wyłącznie przez dashboard z historią i podglądem.
Terminal = tylko diagnostyka i testy jednostkowe.

REGUŁA 3 — PASYWNA PAMIĘĆ
System pamięci buduje się automatycznie po każdej sesji.
Manualne zarządzanie pamięcią jest antywzorcem — automatyzuj zapis.

REGUŁA 4 — ZADANIA W KANBANIE
Każde złożone zadanie (>2 kroki) trafia do Kanbana.
Orchestrator rozbija je na subtasks i przypisuje do właściwych agentów.

REGUŁA 5 — TREŚĆ = TOŻSAMOŚĆ
Przed każdym generowaniem treści: załaduj case studies, własne wyniki,
kontekst klienta. Treść bez kontekstu = treść generyczna = niska wartość.

REGUŁA 6 — GOAL MODE DLA DUŻYCH ZADAŃ
Zadania wieloetapowe (>5 kroków, >20 min) uruchamiaj w Goal Mode.
Definiuj precyzyjny, mierzalny cel. Ustaw limit tur. Wróć po wynik.

REGUŁA 7 — MODULARNOŚĆ AGENTÓW
Jeden agent = jedna specjalizacja.
Gdy agent robi >3 typy zadań → rozdziel na wyspecjalizowane role.

REGUŁA 8 — DARMOWY STACK NA START
Buduj na bezpłatnych komponentach (Owl Alpha / OpenRouter, Obsidian, Omi)
dopóki nie udowodnisz wartości systemu w praktyce.

REGUŁA 9 — INDEKSOWANIE PO KAŻDEJ PUBLIKACJI
Każda opublikowana treść → natychmiastowe zgłoszenie do indeksowania (Indexceptional lub odpowiednik).
Bez tego rankujesz tygodniami zamiast dniami.

REGUŁA 10 — JUDGE LOOP JAKO QA
System autonomiczny musi mieć mechanizm oceny jakości.
Goal Mode z modelem-sędzią = wbudowany QA bez Twojego udziału.
```

---

## Blueprint wdrożeniowy

### Od czego zacząć (Dzień 1)
1. Zainstaluj Hermes Agent i skonfiguruj z darmowym API Owl Alpha przez OpenRouter
2. Zainstaluj Obsidian na maszynie lokalnej

### Co skonfigurować najpierw (Tydzień 1)
3. Ustaw Hermes: „po każdej rozmowie zapisz sesję do mojego Obsidian vault"
4. Zainstaluj Omi → automatyczne codzienne notatki → Obsidian
5. Daj systemowi działać 7 dni zbierając kontekst

### Co przenieść do pamięci (ICE)
6. Twoje projekty i priorytety (raz, manualnie na start)
7. Najważniejsze case studies i wyniki (baza do content machine)
8. Profil klientów / nisz (np. ADHD community, produkty cyfrowe)
9. Preferowane workflow'y i style pracy

### Co zamienić w playbooki / skills / SOP-y
10. SEO content machine → skill: keyword + ICE → artykuł → deploy → Indexceptional
11. Video generation → skill: prompt → Hyperframes → workspace
12. Onboarding nowego projektu → SOP: załaduj kontekst projektu do vault → utwórz sekcję w Kanbanie → przypisz agenty

### Co automatyzować później (Miesiąc 2+)
13. Multi-agent AOS Dashboard z routingiem zadań między Hermes / Claude / Gemini
14. Goal Mode dla kampanii content (np. „napisz i opublikuj 10 artykułów w tygodniu")
15. Orchestrator automatycznie rozdzielający typy zadań między specjalizowane agenty

### Jak nie przesadzić ze złożonością
- **Nie buduj wszystkiego naraz** — jeden komponent tygodniowo
- Waliduj każdą warstwę zanim dodasz kolejną
- Jeśli nie masz 2 tygodni kontekstu w vault → nie uruchamiaj content machine
- Jeśli nie masz AOS → nie uruchamiaj multi-agent workflow
- Złożoność dodawaj reaktywnie (gdy aktualna warstwa staje się bottleneckiem), nie prewencyjnie

---

*Dokument wygenerowany na podstawie materiału: „5 FREE Use Cases for Hermes Agent!" — Julian Goldie SEO, 27 maja 2026.*
