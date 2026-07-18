Blueprint systemowy: Hermes Premium Mission Control — 5 wyspecjalizowanych agentów, Discord, pełny content pipeline i dashboard
Streszczenie operacyjne
Ten materiał rozwiązuje fundamentalny problem AI setupów: brak transparentności. Operator nie wie, co agent robi w środku, który model jest używany, które zadanie zostało zakończone i gdzie trafił output. Rozwiązaniem jest wieloagentowy system Hermes z pięcioma trwałymi agentami (Orchestrator, Scout, Scribe, Reach, Dev), dashboardem mission control, integracją Discord z dedykowanymi kanałami per agent, pełnym content pipeline'm przekazującym pracę między agentami oraz osobistym task trackerem i widokiem aktywności.

Kluczowa różnica w stosunku do standardowego setupu Hermesa: każdy agent ma własną tożsamość, własną pamięć, własny workspace i własne role boundaries. Agenci wiedzą, kto co robi, i przekierowują zadania do właściwego specjalisty zamiast próbować robić wszystko.

Czym jest opisywany system / metoda / framework
Framework to 5-agentowy, trwały Agent OS z warstwą koordynacyjną (Orchestrator) i warstwą komunikacji (Telegram + Discord). Architektura przypomina prawdziwy zespół biurowy: każdy pracownik ma swoją rolę, pamięta poprzednie rozmowy, zna kolegów i wie, kiedy przekazać zadanie dalej.

Sedno systemu: persistent agents z izolowaną pamięcią i shared team awareness. Każdy agent nie tylko wykonuje zadania, ale buduje własną tożsamość, własną historię i własny kontekst pracy — bez cross-contamination z innymi agentami.

Główne filary / komponenty / warstwy
1. Infrastruktura VPS (Contabo lub Racknet)
Dwa rekomendowane VPS do Hermesa:

Contabo (opcja elastyczna):

Plan miesięczny: $7/miesiąc, roczny: ~$5.6/miesiąc

Region: EU (bezpłatny, bez dopłaty)

Storage: SSD 200 GB (więcej miejsca) lub NVMe (szybszy odczyt)

OS: Ubuntu 24.04

Opcja backup za $2/miesiąc (snapshot dzienny — rekomendowane przy rozbudowanych setupach)

Racknet (opcja roczna):

$60/rok za 3 CPU, 60 GB SSD, 4 GB RAM

Credentials dostarczane mailem (IP, username, hasło)

Bez dopłat za lokalizację

Połączenie przez SSH: ssh root@[IP_VPS], Windows PowerShell lub Mac Terminal — te same komendy na obu systemach. Ważne: w PowerShell kopiowanie = Ctrl+Shift+C, NIE Ctrl+C (Ctrl+C zabija proces).

2. Model językowy: OpenAI Codex przez ChatGPT Paid
Zamiast API key — autoryzacja przez link URL z kodem z terminala. Metoda działa z aktywną subskrypcją ChatGPT ($20/miesiąc). Model: GPT-5.5 lub nowszy dostępny w momencie konfiguracji. Pozwala używać subskrypcji ChatGPT bezpośrednio w Hermesie bez osobnego klucza API.

3. Kanały komunikacyjne: Telegram + Discord (dual-channel setup)
Telegram — główny kanał C2 operatora:

Bot tworzony przez BotFather

Token API bota → wklejany w setup Hermesa

User ID pobierany przez userinfobot → ograniczenie bota do jednego operatora

Gateway uruchamiany jako usługa systemowa (pseudo na VPS, user: root)

Discord — dedykowane kanały per agent:

Osobny Discord server dla agentów: jeden serwer, wiele kanałów

Bot Discord tworzony w discord.com/developers/applications

Wymagane uprawnienia bota: Presence Intent, Server Members Intent, Message Content Intent, Administrator (bot permissions)

Każdy agent ma swój kanał — operator może rozmawiać z Scout bezpośrednio, z Dev bezpośrednio, bez mieszania kontekstów

4. Pięć trwałych agentów z izolowaną tożsamością
Każdy agent jest tworzony jako persistent Hermes profile z własnym workspace, własną pamięcią i własnym system promptem:

Agent	Rola	Zakres pamięci	Role boundary
Orchestrator	System coordinator, dispatcher, top-level coordinator	Reguły operacyjne, routing, team awareness	Nie wykonuje pracy domenowej, tylko koordynuje
Scout	Deep research specialist	Źródła, tematy, dane badawcze	Tylko research, nie pisze contentu
Scribe	Content writer	Drafty, style guide, poprzednie teksty	Tylko pisanie, nie robi researchu
Reach	Marketing i social media	Strategie promocji, tone of voice	Tylko marketing, nie pisze długich treści
Dev	Developer	Kod, techniczne decyzje, narzędzia	Tylko dev, nie pisze content marketingowy
Kluczowa zasada: każdy agent zna pozostałych agentów i ich role (shared team awareness), ale nie czyta ich pamięci i nie wykonuje ich pracy.

5. Orchestrator jako dispatcher i router
Orchestrator to centralny agent zarządzający resztą. Jego konfiguracja obejmuje:

Reguły operacyjne operatora: breakowanie pracy na kroki, żądanie zatwierdzenia przy złożonych działaniach, raportowanie postępu (np. „krok 2 z 6")

Router cheat sheet: slash komendy na Telegramie (/scout [task], /dev [task] itp.) — Orchestrator automatycznie routuje do właściwego agenta

Shared team awareness: Orchestrator informuje wszystkich agentów o rolach pozostałych

Full content pipeline: predefiniowany przepływ Scout → Scribe → Reach

6. Full Content Pipeline
Predefiniowany przepływ pracy uruchamiany jedną komendą:

text
Scout (research) → Scribe (content writing) → Reach (social/marketing)
Uruchomienie: Run full pipeline on [topic]

Pipeline realizuje:

Scout szuka materiałów źródłowych i danych o temacie

Scribe bierze output Scoutu i pisze pełny content (np. artykuł, skrypt)

Reach bierze output Scribe'a i tworzy strategię promocji + posty social media

Reach dostarcza finalny plan z prośbą o zatwierdzenie przed implementacją

7. Mission Control Dashboard
Dashboard Hermesa z widokiem:

Activity logs — każda akcja każdego agenta jest zapisana

Który model AI jest używany

Liczba ukończonych tasków danego dnia

Content tab — dedykowany podgląd długich dokumentów produkowanych przez agentów

Personal task tracker (To-Do, Doing, Done)

Cron job overview

Live activity feed

8. Personal Operating Rules (reguły operatora)
Zestaw trwałych reguł wstrzykiwanych do Orchestratora i wszystkich agentów przy onboardingu:

Rozbijanie złożonych zadań na kroki z widocznymi numerami (np. krok 3 z 6)

Żądanie zatwierdzenia przed ważnymi akcjami

Raportowanie statusu przy długich operacjach

Przekierowywanie zadań do właściwego agenta, jeśli zadanie jest poza rolą

Architektura logiki
Co jest pamięcią
Każdy agent ma izolowaną pamięć (osobny workspace, osobne pliki pamięci Hermesa). Orchestrator przechowuje: reguły operacyjne, routing rules, team awareness. Scout: źródła i dane. Scribe: drafty i styl. Reach: strategie i ton. Dev: kod i decyzje techniczne. Brak cross-contamination jest fundamentalnym wymogiem architektury.

Co jest procedurą
Procedurami są:

Full content pipeline (Scout → Scribe → Reach): predefiniowany, uruchamiany jedną komendą

Personal operating rules: trwałe reguły stylu pracy wstrzyknięte przy setupie

Role boundaries: każdy agent wie, kiedy odmówić i przekierować do właściwego kolegi

Self-improvement skill: Orchestrator automatycznie tworzy skill do samodoskonalenia (bez pytania)

Co jest sterowaniem
Sterowanie jest trójpoziomowe:

Telegram — główny C2 operatora; slash komendy routują do agentów

Discord — kanały per agent dla bezpośredniej komunikacji z konkretnym specjalistą

Dashboard — widok stanu całego systemu, tasków i aktywności

Co jest harmonogramem
Harmonogram to cron jobs konfigurowane z poziomu dashboardu lub Telegrama. W tym setupie nie są szczegółowo opisane, ale dashboard ma osobną sekcję cron job overview.

Co jest warstwą wykonawczą
Warstwą wykonawczą jest pięć agentów: Scout (research), Scribe (content), Reach (marketing), Dev (kod), przy koordynacji Orchestratora. Każdy agent ma dostęp do narzędzi swojego domeny.

Co jest warstwą bezpieczeństwa
Izolacja VPS od sieci domowej

Ograniczenie Telegram bota do jednego user ID

Izolowana pamięć agentów (bez cross-contamination)

Role boundaries jako guard rails dla każdego agenta

Zatwierdzanie przez operatora przed ważnymi akcjami

Co jest warstwą integracji
OpenAI Codex przez ChatGPT Paid (autoryzacja URL)

Telegram (C2 + routing)

Discord (per-agent channels)

Dashboard Hermesa (monitoring)

Workflow wdrożeniowy
Kup VPS (Contabo lub Racknet), wybierz Ubuntu 24.04, ustaw hasło, opcjonalnie włącz daily backup.

Połącz się przez SSH: ssh root@[IP], zaakceptuj fingerprint, wklej hasło (prawym klikiem w PowerShell).

Wklej one-line install command z oficjalnej strony Hermesa, poczekaj na instalację zależności.

W Quick Setup wybierz OpenAI Codex, autoryzuj przez link URL (skopiuj kod przez Ctrl+Shift+C, nie Ctrl+C).

Wybierz model GPT-5.5 (lub nowszy), backend: Local.

Skonfiguruj Telegram: stwórz bota przez BotFather, skopiuj token, pobierz user ID przez userinfobot, ustaw home channel.

Włącz usługę systemową (gateway as background service, pseudo, user: root), potwierdź uruchomienie.

Przetestuj: wpisz hermes w terminalu, napisz "hi", sprawdź odpowiedź. Potem sprawdź Telegram bota.

Onboarding Orchestratora przez Telegram — wyślij kolejno:

Prompt 1: Przedstaw się i nadaj agentowi nazwę Orchestrator + swoją jako właściciel

Prompt 2: Personal operating rules (kroki, zatwierdzanie, raportowanie)

Prompt 3: Stwórz 4 persistent agents (Scout, Scribe, Reach, Dev) z opisem ról — zatwierdź plan

Prompt 4: System prompty dla każdego agenta — ich tożsamość i specjalizacja

Prompt 5: Pamięć i role boundaries per agent

Prompt 6: Router cheat sheet + slash komendy na Telegramie

Prompt 7: Shared team awareness — wszyscy agenci znają pozostałych

Prompt 8: Full content pipeline (Scout → Scribe → Reach)

Przetestuj pipeline: Run full pipeline on [temat], obserwuj kroki i zatwierdzaj wyniki.

Skonfiguruj Discord: stwórz aplikację w discord.com/developers, wygeneruj bot token, włącz intenty, dodaj bota do własnego serwera.

Połącz Discord z Hermesem, stwórz kanały per agent, przetestuj komunikację.

Otwórz dashboard mission control i sprawdź: activity logs, content tab, task tracker, cron overview.

Zasady operacyjne
Orchestrator nigdy nie wykonuje pracy domenowej — tylko koordynuje, routuje i pilnuje reguł.

Każdy agent ma role boundary — jeśli zadanie jest poza jego kompetencją, musi odmówić i wskazać właściwego agenta.

Pamięci agentów są izolowane — Dev nie czyta pamięci Scribe'a, Scout nie czyta pamięci Reach'a.

Slash komendy na Telegramie (/scout, /dev, /scribe, /reach) używaj zamiast opisywać odbiorców — to eliminuje błędne routowanie.

Personal operating rules wstrzykuj na samym początku i traktuj jako trwałe — nie jako jednorazowy prompt.

Przy złożonych operacjach Orchestrator pyta o zatwierdzenie (Approved wystarczy) — nie blokuj tego flow.

Gdy agent startuje długą operację, powinien raportować postęp krokami (krok X z Y) — to sygnał działania, nie milestone.

Discord używaj gdy chcesz izolować konwersacje per domain — Telegram gdy chcesz ogólne C2.

Dashboard content tab jest miejscem odczytu długich dokumentów — nie przeglądaj ich przez Telegram.

Best practices
Persistent agents zamiast tymczasowych
Tworzenie agentów jako persistent profiles (nie jednorazowych sesji) jest kluczowe dla budowania tożsamości, pamięci i spójności zachowania w czasie. Agent, który nie pamięta poprzednich rozmów, nie może się doskonalić.

Shared team awareness jako warstwa koordynacji
Każdy agent powinien wiedzieć, kto jest w zespole i co robi. Bez tej warstwy agenci próbują obsługiwać zadania poza swoją domeną albo nie wiedzą, do kogo przekazać pracę