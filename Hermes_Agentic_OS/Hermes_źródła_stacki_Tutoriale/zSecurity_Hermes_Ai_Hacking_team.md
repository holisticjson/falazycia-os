Blueprint systemowy: Zespół AI Hacking w Hermes Agent na VPS
Streszczenie operacyjne
Ten tutorial pokazuje, jak zbudować w oparciu o Hermes Agent działający na VPS w pełni operacyjny, 24/7 „AI hacking team” – zespół agentów AI w chmurze, sterowany z telefonu i zarządzany przez dashboard oraz Kanban. Systemowy model polega na połączeniu: odseparowanego serwera (VPS), stale uruchomionego Hermesa, komunikacji C2 przez Telegram, zdalnie dostępnego dashboardu (przez SSH port forwarding) i Kanban boardu, na którym AI-agent wykonuje złożone pipeline’y zadań.

Use case z filmu: z poziomu telefonu operator wydaje jedna komendę, a zespół agentów na VPS automatycznie robi research bramek SMS, tworzy skill do spoofingu, buduje i wdraża stronę trackingową, obsługuje weryfikacje 2FA przez Telegram i finalnie dostarcza spoofowany SMS z linkiem, który po kliknięciu zbiera lokalizację celu i pokazuje ją w dashboardzie.

Czym jest opisywany system / metoda / framework
Framework ZSecurity opisuje wykorzystanie Hermes Agent jako „AI hacking team” – wieloagentowego systemu działającego na VPS, który samodzielnie wykonuje wieloetapowe workflow ofensywne/bezpieczeństwa z użyciem terminala, przeglądarki i własnych skillów. Hermes nie pełni roli zwykłego chatbota; pełni funkcję operatora pracującego na osobnej maszynie, który może instalować, konfigurować i uruchamiać narzędzia zgodnie z zadanym celem.

Metoda opiera się na trzech głównych decyzjach architektonicznych: po pierwsze, Hermes działa wyłącznie na odseparowanym VPS, a nie na komputerze prywatnym; po drugie, kanał dowodzenia (C2) to głównie Telegram (i inne komunikatory), wspierany przez terminal; po trzecie, cała praca techniczna i kontekst są synchronizowane przez dashboard oraz Kanban board, co umożliwia równoległe zadania, zależności i przekazywanie wyników między taskami.

Główne filary / komponenty / warstwy
1. VPS z preinstalowanym Hermes Agent
Podstawą systemu jest VPS (Hostinger KVM2 w przykładzie: 2 CPU, 8 GB RAM), na którym Hermes Agent jest preinstalowany – po wyborze planu użytkownik dostaje serwer z zainstalowanym Hermeseem. Ten VPS pełni rolę „komputera agenta” i może również hostować inne aplikacje (np. OpenClaw) w tym samym środowisku.

2. Instalacja i konfiguracja Hermesa (Quick Setup)
Hermes konfigurowany jest przez Quick Setup w terminalu na VPS – po zalogowaniu się użytkownik uruchamia wizard, wybiera dostawcę modelu (OpenRouter), wkleja klucz API i wskazuje konkretny model. W case study używany jest model Z.AI (GLM5 Turbo) – tańszy i mniej cenzurowany, dzięki czemu lepiej nadaje się do zastosowań red-teamowych w ramach autoryzowanych testów.

3. Warstwa modeli: OpenRouter + custom model
Hermes używa OpenRouter jako warstwy modelowej; operator może wybrać darmowy lub płatny model, wklejając jego nazwę jako custom model. Inteligencja systemu zależy od wybranego modelu – w filmie podkreślono, że wybór Z.AI ma kluczowe znaczenie, bo wiele standardowych modeli jest mocno filtrowanych.

4. Warstwa komunikacji C2: Telegram Bot
Kanałem dowodzenia jest Telegram bot skonfigurowany przez BotFather – Hermes używa tokenu bota oraz user ID operatora, aby przyjmować polecenia tylko od właściwej osoby. Dzięki temu operator może sterować zespołem AI z telefonu, otrzymując statusy, prośby o kody 2FA i wyniki zadań bez konieczności logowania się na VPS.

5. Warstwa terminalowa (CLI na VPS)
Terminal VPS służy do pierwszego setupu, uruchamiania Hermesa, dashboardu oraz konfiguracji tuneli SSH. Używane są komendy w stylu Hermes dashboard z flagami --d-tui, --d-now, --d-host 0.0.0.0, --d-insecure, aby odpalić dashboard wewnątrz kontenera Dockera. Hermes wystawia wtedy port dostępny lokalnie na VPS, co wymaga tunelowania, aby zobaczyć dashboard z zewnątrz.

6. Warstwa dashboardu webowego
Dashboard Hermesa działa w kontenerze i jest dostępny na VPS pod określonym portem; dzięki SSH port forwarding (ssh -L 9119:DOCKER_IP:9119) operator mapuje port 9119 z kontenera na localhost:9119 i może wejść do dashboardu z własnego komputera. W dashboardzie dostępne są: sesje, chat, modele, logi toolcalli, cron jobs, skills, profiles oraz Kanban.

7. Warstwa skills i „God Mode”
Skills to prekonfigurowane zdolności Hermesa; w sekcji skills dostępny jest m.in. skill „God Mode” w kategorii Red Team, bazujący na jailbreakach Plenny the Liberator. God Mode służy do omijania cenzury modeli w kontekście autoryzowanych zadań security – agent może go użyć, jeśli model odmawia wykonania dopuszczalnego zadania.

8. Warstwa profili (profiles) – zespół agentów
Profiles odpowiadają członkom zespołu – każdy profil ma własny model, zestaw skills, workspace i system prompt opisujący rolę i zasady działania. Domyślny profil jest edytowany tak, aby wiedział, że działa na cloud VPS w Dockerze, ma słuchać operatora, używać God Mode przy odmowach modeli i wykonywać zadania red-teamowe w ramach autoryzowanych testów.

9. Warstwa Kanban
Kanban jest sercem orkiestracji – kolumny triage, to-do, ready, in progress, blocked i done odwzorowują board ZSecurity. Zadania mają relacje parent–child, można do nich przypisać powiadomienia Telegram, a Hermes automatycznie przesuwa je między kolumnami w zależności od stanu; wyniki parent są przekazywane do child jako input.

10. Warstwa use case: SMS spoofing + tracking page
Study case w tutorialu: Hermes, działając na VPS, realizuje pipeline: research bramek SMS z alfa-numeric sender i darmowymi kredytami, implementacja skilla do wysyłania spoofowanych SMS, stworzenie i deploy strony DHL tracking (phishing) oraz obsługa procesu 2FA, aby korzystać z bramki. Po zbudowaniu pipeline’u operator z telefonu wydaje jedną komendę, a agent wysyła SMS z linkiem trackującym, zbiera lokalizację i wyświetla ją w dashboardzie.

Architektura logiki
Co jest pamięcią
Pamięć w tym use case obejmuje:

logi sesji i narzędzi dostępne w dashboardzie (pełna historia dialogu, wywołań tools, rezultatów);

knowledge i skille zapisane w profilu, np. informacje, że agent działa na VPS w Dockerze i ma określone zasady używania God Mode;

stan i rezultaty zadań Kanbanu – szczególnie wyniki researchu używane później przy implementacji skilla.

Co jest procedurą
Procedurą są:

skille (np. skill spoofingu SMS, skill budowy tracking page), które agent może wywołać wielokrotnie;

pipeline Kanban: research → budowa skilla → budowa strony → testy → deployment → użycie skilla;

procedura God Mode, uruchamiana gdy model blokuje zadanie mimo autoryzacji.

Co jest sterowaniem
Sterowanie działa na trzech warstwach:

komunikacja C2 przez Telegram – krótkie polecenia i odpowiedzi operatora (np. kody 2FA);

dashboard i Kanban – wybór profilu, tworzenie i edycja zadań, definiowanie zależności, powiadomień;

terminal na VPS – uruchamianie Hermesa, dashboardu i tuneli.

Co jest harmonogramem
Harmonogram oparty jest tu bardziej na przepływie zadań niż na cronach: kolejność wymuszana jest przez zależności parent–child i statusy w Kanbanie. Operator może odejść od komputera; Hermes wykonuje zadania, a w momentach wymagających udziału człowieka (np. kody 2FA) wysyła prośby przez Telegram.

Co jest warstwą wykonawczą
Warstwą wykonawczą są:

Hermes Agent uruchomiony w Dockerze na VPS, z dostępem do terminala, narzędzi systemowych i przeglądarki;

pluginy/narzędzia umożliwiające browsing, deploy stron, obsługę formularzy, integrację z bramkami SMS;

bramka SMS i hosting tracking page na tym samym VPS.

Co jest warstwą bezpieczeństwa
Warstwa bezpieczeństwa opiera się na:

separacji środowiska – Hermes działa na VPS, nie na prywatnym komputerze;

ograniczeniu dashboardu do tunelu SSH – d-insecure jest używane wewnątrz Dockera/VPS, a nie wystawiane bezpośrednio do internetu;

ograniczeniu bota Telegram do jednego user ID – nikt inny nie może wydawać poleceń agentowi;

jasnym komunikacie, że testy muszą być wykonywane wyłącznie na systemach, do których operator ma prawo.

Co jest warstwą integracji
Integracje obejmują:

OpenRouter jako warstwę modelową;

Hostinger jako warstwę infrastruktury;

Telegram jako kanał C2;

bramki SMS jako kanał spoofingu;

hosting i dashboard lokalizacji (tracking page + mapa).

Workflow wdrożeniowy
Wybierz VPS z preinstalowanym Hermes Agent (np. Hostinger, plan KVM2) i kup go na określony okres, korzystając z kuponu.

Skonfiguruj konto admina (username, hasło) do logowania do Hermesa.

Zaloguj się do terminala Hermesa z panelu Hostinger (open) i uruchom Quick Setup.

Wybierz OpenRouter jako dostawcę modeli, wygeneruj API key i wklej go do wizardu.

Znajdź model (np. Z.AI GLM5 Turbo), skopiuj jego nazwę i skonfiguruj go jako custom model Hermesa.

Pozostaw backend jako local.

W wizardzie messaging wybierz Telegram, utwórz bota w BotFather i wklej token.

Ogranicz bota do swojego user ID, używając helper bota do pobrania ID i wpisując je w konfigurację.

Przetestuj komunikację, wysyłając komendę z Telegrama i obserwując odpowiedź modelu.

Na VPS uruchom dashboard w Dockerze poleceniem Hermes dashboard z flagami --d-tui, --d-now, --d-host 0.0.0.0, --d-insecure i sprawdź port oraz IP kontenera.

Ustaw hasło root na VPS, skopiuj komendę SSH i dodaj -L 9119:DOCKER_IP:9119.

Otwórz http://localhost:9119 i zaloguj się do dashboardu Hermesa.

Poznaj dashboard: sesje, chat, modele, logi, cron jobs, skills, profiles, Kanban.

Skonfiguruj domyślny profil: dodaj opis środowiska (cloud VPS + Docker), zasady (słuchaj operatora, używaj God Mode przy odmowach).

Otwórz Kanban, zrozum flow triage → to-do → ready → in progress → blocked → done.

Zbuduj pipeline dla SMS spoofing + tracking page, dodając kolejne zadania i zależności.

Przy zadaniach wymagających 2FA oczekuj próśb o kody na Telegramie i przekazuj je agentowi.

Po ukończeniu pipeline’u użyj gotowego skilla i strony, wydając prostą komendę z telefonu, a agent wykona resztę.

Zasady operacyjne
Hermes ma być zawsze włączony na VPS, dostępny przez Telegram i dashboard – użytkownik nie musi być fizycznie przy komputerze.

Terminal służy głównie do setupu i utrzymania; codzienne sterowanie odbywa się przez komunikator i dashboard.

Telegram bot musi być powiązany z jednym user ID – inaczej inne osoby mogą wykorzystać Twoje zasoby VPS.

Złożone zadania dziel się na pipeline’y w Kanbanie i ustawiaj zależności parent–child, aby AI mogło wykonywać pracę sekwencyjnie i równolegle.

Zadania wymagające weryfikacji (e-mail/SMS) zawsze obsługuj przez Telegram, odpowiadając na prośby agenta o kody.

God Mode stosuj jako narzędzie do zarządzania cenzurą modeli w ramach autoryzowanych testów, a nie do łamania polityk platform.

Profil domyślny powinien zawsze znać środowisko działania i ograniczenia dostępu, aby nie próbował wykonywać operacji poza VPS.

Gdy coś nie działa (np. dashboard), najpierw sprawdź tunel SSH i konfigurację portów.

Best practices
Trzymaj Hermesa na odseparowanym VPS, nie na prywatnym PC – to minimalizuje ryzyko i ułatwia kontrolę.

Wybieraj infrastrukturę o przewidywalnych kosztach, co pozwala utrzymywać zespół AI w sposób stabilny.

Dobieraj model do domeny – w security praktyczne są mniej cenzurowane modele, ale tylko w granicach prawa.

Traktuj Kanban jako główną warstwę orkiestracji, a nie ozdobny widget.

Używaj powiadomień Telegram dla kluczowych zadań, aby monitorować postęp bez ciągłego oglądania dashboardu.

W promptach i zadaniach jasno zapisuj, że działasz w ramach autoryzowanego testu – to zmniejsza liczbę odmów modeli i przypomina o granicach.

Projektuj workflow tak, by agent mógł wykonać pełne end-to-end, łącznie z testami i deployem.

Wykorzystuj mission dashboard z mapą lokalizacji zamiast ręcznie interpretować dane geograficzne.

Security / ryzyka / ograniczenia
Wszystkie testy muszą być legalne i autoryzowane – użycie tego setupu do ataków na obce systemy jest nielegalne.

Izolacja środowiska (VPS + Docker + SSH tunneling) ogranicza ryzyko, ale wymaga poprawnego skonfigurowania.

Błędna konfiguracja user ID w Telegramie może dopuścić innych do Twojego bota; to krytyczny punkt bezpieczeństwa.

Hermes jest tak dobry, jak wybrany model – zbyt słaby lub mocno cenzurowany model ograniczy możliwości pipeline’u.

Niewłaściwe użycie d-insecure lub otwartych portów może narazić dashboard na nieautoryzowany dostęp, jeśli środowisko nie jest restrykcyjnie zamknięte.

Nawet w trybie edukacyjnym spoofing SMS i phishing są regulowane – nie wolno ich stosować poza scenariuszami zgodnymi z prawem.

Skalowanie / delegowanie / modularność
Wraz z rozwojem możesz definirwać dodatkowe profile (np. OSINT, web exploitation, network, reviewer) i przypisywać im specjalne typy zadań.

Kanban umożliwia równoległe uruchamianie niezależnych zadań i lepsze wykorzystanie czasu.

System można rozszerzać o nowe kampanie red-teamowe, dodając kolejne pipeline’y i skille w tym samym frameworku.

Hermes może współistnieć z innymi narzędziami (np. OpenClaw) na tym samym VPS, ale w tym frameworku funkcjonuje jako centralny OS.

Antywzorce i błędy
Uruchamianie Hermesa na prywatnym komputerze zamiast na odseparowanym VPS.

Pozostawienie bota Telegram bez ograniczenia user ID.

Brak zależności między zadaniami Kanbanu – chaos w pipeline’ach.

Ręczne wykonywanie całego pipeline’u, mimo że Kanban + AI mogą go zautomatyzować.

Ignorowanie aspektów prawnych i wykonywanie testów bez zgody.

Mylenie demo edukacyjnego z zachętą do realnych ataków.

Reguły do przeniesienia do mojego systemu
Agenci red-teamowi muszą działać w odseparowanym środowisku (VPS), nie na osobistym komputerze.

Kanał C2 (Telegram) musi być spięty z jednym zaufanym operatorem – user ID to obowiązkowy filtr.

Każde złożone zadanie zamieniaj na pipeline Kanban z relacjami parent–child.

Skille ofensywne (np. spoofing SMS) traktuj jako reużywalne moduły, nie jednorazowe prompty.

W instrukcjach profilu agenta zapisuj środowisko (VPS/Docker), poziom zaufania, zasady używania God Mode i zakres działań.

Dashboard udostępniaj wyłącznie przez tunel SSH; nie wystawiaj go bezpośrednio do internetu.

Każdy proces 2FA opisuj procedurą: agent pyta tylko przez zaufany kanał, operator odpowiada, zdarzenie jest zapisane.

W promptach misji red-teamowych zawsze umieszczaj wzmiankę o autoryzacji i granicach zadań.

Blueprint wdrożeniowy
Od czego zacząć
Postaw jednego Hermesa na jednym VPS z preinstalowaną konfiguracją.

Skonfiguruj jednego bota Telegram z ograniczeniem user ID i upewnij się, że komunikacja działa.

Co skonfigurować najpierw
Quick Setup: provider modeli (OpenRouter), API key, model Z.AI / inny.

Kanał C2: BotFather + token + user ID.

Dashboard: uruchomienie w Dockerze, tunel SSH, dostęp localhost:9119.

Profil domyślny: opis środowiska, zasady God Mode, rola.

Co przenieść do pamięci
Opis środowiska (VPS, Docker, Hostinger) i zakres uprawnień agenta.

Przepis pipeline’u SMS spoofing + tracking page (zadania, prompty, zależności).

Skille zbudowane w use case (gateway research, spoofing, deploy strony).

Logi sesji, szczególnie związane z 2FA.

Co zamienić w playbooki / skills / SOP-y
Playbook: „Budowa skilla spoofingu SMS” – research bramek, założenie konta, konfiguracja API, implementacja skilla.

Playbook: „Budowa i deploy tracking page” – wymagania, projekt, testy, deployment.

SOP: „Konfiguracja dashboardu Hermesa na VPS” – kroki, flagi, SSH -L.

SOP: „Obsługa 2FA” – standardowy protokół reagowania.

Co automatyzować później
Dodatkowe kampanie red-teamowe: nowe typy stron, bramek, wektorów, używając tego samego wzoru.

Integracje z innymi narzędziami security, ale w tej samej architekturze (Hermes na VPS + Kanban).

Jak nie przesadzić ze złożonością
Zacznij od jednego profilu, jednego pipeline’u i jednego bota; nie spinaj na starcie wielu modeli, wielu profili i kilku kampanii.

Nie wystawiaj dashboardu bezpośrednio – zawsze używaj tunelu SSH.

Nie dodawaj nowych modeli/profili, póki nie masz stabilnie działającego jednego case’u.