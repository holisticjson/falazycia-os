# Hermes Agent — blueprint systemowy Nate’a Herka do wykorzystania w Antigravity

Ten dokument porządkuje cały tutorial Nate’a Herka o Hermes Agent w formę gotowego materiału referencyjnego do wykorzystania jako inspiracja dla własnego agenta, systemu operacyjnego lub warstwy instrukcyjnej w Antigravity.[cite:1]

Materiał źródłowy pokazuje Hermes jako open-source’owego agenta działającego na własnej infrastrukturze, z pamięcią, skills, osobowością, cronami i pętlą samodoskonalenia, a nie jako zwykły chatbot.[cite:1]

## Streszczenie operacyjne

Rdzeń modelu Nate’a jest prosty: agent powinien mieć trwałą pamięć o użytkowniku i projektach, proceduralne playbooki do zadań powtarzalnych, jasno zdefiniowaną osobowość, warstwę harmonogramów oraz mechanizm przekształcania doświadczenia w lepsze zachowanie w czasie.[cite:1]

Hermes nie zastępuje w jego workflow narzędzi typu Claude Code, tylko uzupełnia je jako agent operacyjny do pracy „on the go”, szczególnie przez Telegram, z silnym naciskiem na automatyzacje, backup, pamięć i delegowanie.[cite:1]

## Czym Hermes jest w tym modelu

Nate opisuje Hermes Agent jako open-source’owy projekt MIT od News Research, uruchamiany na własnej infrastrukturze: Mac mini, laptopie, VPS-ie, Dockerze, a nawet na Androidzie przez Termux.[cite:1]

Najważniejsze w jego definicji jest to, że Hermes nie jest chatbotem w przeglądarce, tylko asystentem zdolnym do używania narzędzi, zapamiętywania preferencji, tworzenia reusable skills, uruchamiania scheduled automations, przeszukiwania wcześniejszych rozmów i pracy przez kanały takie jak Telegram, Discord, Slack czy WhatsApp.[cite:1]

## Kiedy Nate używa Hermesa

Claude Code pozostaje u Nate’a głównym narzędziem do codziennej głębokiej pracy przy biurku, zwłaszcza do kodowania i knowledge worku w terminalu.[cite:1]

Hermes i OpenClaw służą mu głównie do pracy mobilnej i operacyjnej, kiedy chce na szybko ustawić cron, zlecić zadanie przez telefon, odpalić monitoring, zrobić follow-up albo ogarnąć zadanie bez siadania do pełnego środowiska developerskiego.[cite:1]

## Pięć filarów systemu

### 1. Memory

Memory to trwały kontekst przenoszony między sesjami, zbudowany przede wszystkim z plików `user.md` i `memory.md`, które są ładowane na starcie sesji, ponieważ agent budzi się stateless.[cite:1]

`user.md` przechowuje tożsamość użytkownika, styl, preferencje i rzeczy, których nie lubi, a `memory.md` opisuje środowiska, projekty i kontekst biznesowy.[cite:1]

Do pamięci powinny trafiać trwałe preferencje i fakty, a nie sekrety ani chwilowy status zadania; stare rozmowy Nate traktuje osobno, jako warstwę session search w bazie SQL.[cite:1]

### 2. Skills

Skills to procedural memory, czyli powtarzalne playbooki opisujące, jak wykonać zadanie dobrze i spójnie.[cite:1]

Każdy skill ma plik `skill.md` oraz YAML front matter, który mówi agentowi, kiedy dany skill powinien zostać przywołany, dzięki czemu pełna treść skilla nie musi być ładowana do każdej sesji z góry.[cite:1]

W modelu Nate’a skill odpowiada na pytanie „jak to zrobić ponownie”, podczas gdy memory odpowiada na pytanie „co pamiętać”.[cite:1]

### 3. Soul

`soul.md` kształtuje osobowość agenta, jego ton, sposób odpowiadania i ogólny vibe, dzięki czemu różne instancje Hermesa mogą mieć różne role i style komunikacji.[cite:1]

To jest osobna warstwa od pamięci i osobna od skills, a Nate podkreśla, że jeśli agent mówi źle, zbyt rozwlekle lub nie w odpowiednim tonie, problem często leży właśnie w soul, a nie w logice zadania.[cite:1]

### 4. Crons

Crony zamieniają Hermesa z systemu reaktywnego w system proaktywny, ponieważ agent może otrzymywać naturalnojęzykowe polecenia typu „codziennie o 6 rano rób X” i sam zamieniać je w harmonogram wykonywany w osobnej, izolowanej sesji.[cite:1]

Nate pokazuje, że crony są jedną z największych przewag Hermesa w jego własnym workflow, bo pozwalają utrzymywać codzienne automatyzacje bez konieczności ciągłego siedzenia przy terminalu.[cite:1]

### 5. Self-improving loop

Hermes ma poprawiać się wtedy, gdy użyteczne doświadczenia zostają utrwalone jako memory, skills i searchable history, a użytkownik aktywnie koryguje zachowanie agenta oraz prosi o zapis ważnych rzeczy do odpowiednich plików.[cite:1]

Nate bardzo mocno zaznacza, że automatyzacja nie oznacza magii: pętla działa najlepiej wtedy, gdy użytkownik świadomie daje feedback i pozwala agentowi przerabiać złożoną pracę na lepsze instrukcje systemowe oraz playbooki.[cite:1]

## Dodatkowa warstwa: plik projektu

Poza pięcioma filarami Nate wskazuje jeszcze warstwę lokalnego kontekstu projektu, np. `agents.md` lub `claude.md`, która opisuje ogólny cel i strukturę konkretnego przedsięwzięcia, ale nie jest globalną pamięcią użytkownika.[cite:1]

To oznacza, że architektura systemowa może być rozumiana jako podział na pamięć globalną użytkownika, pamięć projektu, procedury, ton oraz harmonogramy.[cite:1]

## Reguły architektury pamięci do Antigravity

Poniższy podział dobrze odtwarza logikę Nate’a i nadaje się do wdrożenia w systemie agentowym lub warstwie sterowania:

| Warstwa | Funkcja | Co tam trafia | Czego unikać |
|---|---|---|---|
| `user.md` | Tożsamość i preferencje użytkownika | styl pracy, preferencje, język, ograniczenia, sposób komunikacji [cite:1] | sekrety, tymczasowe taski [cite:1] |
| `memory.md` | Kontekst świata pracy | projekty, środowiska, relacje, procesy, kontekst biznesowy [cite:1] | chwilowe statusy, hałaśliwe szczegóły [cite:1] |
| `soul.md` | Osobowość i ton | styl odpowiedzi, vibe, poziom bezpośredniości [cite:1] | instrukcje proceduralne i sekrety [cite:1] |
| `skill.md` | Procedura | kroki wykonania, kryteria, wzorzec działania [cite:1] | długoterminowe preferencje użytkownika [cite:1] |
| `agents.md` / `claude.md` | Lokalny kontekst projektu | cel projektu, scope, struktura folderów, zasady lokalne [cite:1] | globalna tożsamość użytkownika [cite:1] |

## Reguły tworzenia skills

Na podstawie tutoriala Nate’a można zapisać bardzo czytelne zasady projektowania skills.

- Skill powinien opisywać powtarzalny sposób wykonania zadania, nie jednorazową odpowiedź.[cite:1]
- Skill powinien mieć jasny trigger w YAML front matter, tak aby agent wiedział, kiedy go wywołać.[cite:1]
- Jeżeli użytkownik daje tę samą instrukcję drugi raz, to jest to sygnał, że trzeba z niej zrobić skill.[cite:1]
- Jeżeli agent nie uruchamia skilla, który powinien się uruchamiać, należy poprawić YAML front matter i warunki wywołania.[cite:1]
- Hermes może sam budować i patchować skills na podstawie realnej pracy, ale użytkownik nadal powinien aktywnie korygować kierunek.[cite:1]

## Reguły cronów

Nate pokazuje crony jako warstwę zachowania operacyjnego, a nie tylko prostą schedulację.[cite:1]

- Najpierw ustal, co agent ma robić regularnie, dopiero potem poproś o cron.[cite:1]
- Dla zadań istotnych i cyklicznych najpierw zbuduj skill, potem przypnij do niego cron.[cite:1]
- Crony uruchamiają świeżą, izolowaną sesję, więc prompt musi być samowystarczalny.[cite:1]
- Crony nie mogą rekurencyjnie tworzyć kolejnych cronów, więc nie należy opierać ich logiki na łańcuchowym generowaniu następnych zadań.[cite:1]
- Przy zadaniach zależnych od strefy czasowej warto stosować logikę self-check zamiast sztywnego przeliczenia UTC, bo daylight saving może psuć harmonogram.[cite:1]

## Praktyczny wzorzec wdrożenia po Nate’owemu

Sekwencja wdrożenia Hermesa w tutorialu jest bardzo klarowna i nadaje się do przeniesienia jako standard operacyjny.[cite:1]

1. Postaw VPS i wybierz środowisko uruchomieniowe, najlepiej Ubuntu 24.04 LTS.[cite:1]
2. Zdecyduj, czy agent ma działać na root VPS czy w Dockerze; Nate wybiera Docker ze względu na prostotę i izolację.[cite:1]
3. Przejdź onboarding, wybierz provider oraz model, a następnie połącz kanał komunikacyjny, np. Telegram.[cite:1]
4. Dodaj trwały kontekst użytkownika i projektu, rozmawiając z agentem o celach, zespole, środowisku i potrzebach.[cite:1]
5. Podłącz prywatne repozytorium GitHub jako backup stanu projektu i plików agenta.[cite:1]
6. Zbuduj pierwszy skill i pierwszy cron, najlepiej nightly backup lub GitHub sync.[cite:1]

## VPS i Docker — reguły infrastrukturalne

Nate wyjaśnia, że VPS to po prostu wynajęty komputer w chmurze z własnym IP i dostępem SSH, a Docker pozwala odseparować od siebie różne instancje agentów wewnątrz tego samego serwera.[cite:1]

W jego modelu Docker jest wygodniejszy od instalacji bezpośrednio na root VPS, bo ułatwia izolację agentów, rozdzielanie kluczy, zarządzanie środowiskiem `.env` i późniejsze skalowanie do wielu instancji.[cite:1]

## Onboarding i warstwa komunikacyjna

W tutorialu onboarding obejmuje wybór inference providera, modelu i kanału komunikacyjnego, a przykład pokazany przez Nate’a używa OpenAI Codex z autoryzacją przez konto ChatGPT oraz kanału Telegram.[cite:1]

Bardzo ważne jest ograniczenie dostępu do bota tylko do dozwolonych użytkowników przez wskazanie Telegram user ID, co jest pierwszym prostym krokiem ograniczającym ryzyko nieautoryzowanego dostępu.[cite:1]

## GitHub jako source of truth

Pierwszy praktyczny priorytet Nate’a po uruchomieniu agenta to połączenie Hermesa z prywatnym repozytorium GitHub, aby w razie awarii VPS lub uszkodzenia środowiska można było wznowić pracę na nowej instancji bez utraty stanu.[cite:1]

Repozytorium ma być prywatne, z odpowiednio ustawionym `.gitignore`, tak aby backupować stan projektu i pliki kontekstowe, ale nie wypychać sekretów ani wrażliwych danych.[cite:1]

## Reguły bezpieczeństwa

W tej części tutorial Nate przechodzi od konfiguracji do myślenia o ryzyku, a jego zasady dają się przekształcić w bardzo czytelny zestaw polityk systemowych.[cite:1]

### Zasada 1: sekrety poza rozmową

Klucze API i tokeny nie powinny trafiać do okna konwersacji, jeśli można tego uniknąć, ponieważ wtedy zostają w historii rozmowy.[cite:1]

Nate pokazuje bezpieczniejszy wzorzec: ustawianie sekretów bezpośrednio w `.env` przez komendy konfiguracyjne agenta lub przez terminal środowiska, a nie przez zwykły chat.[cite:1]

### Zasada 2: oddzielne konta i oddzielne klucze

Agenci powinni mieć własne konta i własne klucze API, zwłaszcza wtedy, gdy mogą wykonywać akcje kosztowe lub mieć kontakt z zewnętrznymi usługami.[cite:1]

Taki podział nie tylko zwiększa bezpieczeństwo, ale też ułatwia śledzenie kosztów i powiązanie konkretnych wydatków z konkretnymi agentami.[cite:1]

### Zasada 3: least privilege

Każdy agent powinien otrzymać wyłącznie te credentials, te scope’y i te narzędzia, które są niezbędne do jego roli.[cite:1]

Marketing agent nie potrzebuje tych samych dostępów co finance agent, a brak segmentacji zwiększa zarówno ryzyko, jak i chaos poznawczy całego systemu.[cite:1]

### Zasada 4: hardening VPS

Nate zaleca korzystanie z firewalla, ograniczanie portów oraz zawężanie dostępu, np. do konkretnego IP, nawet jeśli sam nie przedstawia tego jako obszaru swojej eksperckiej specjalizacji.[cite:1]

Kluczowe jest tu podejście: nie trzeba wszystkiego wiedzieć z pamięci, ale trzeba umieć zlecić agentowi i narzędziu research oraz wdrożenie bezpieczniejszych ustawień.[cite:1]

### Zasada 5: security as routine

Security nie powinno być jednorazowym wydarzeniem po wdrożeniu, tylko cyklem operacyjnym, np. przez regularne audyty bezpieczeństwa wykonywane nocą albo co tydzień przez agenta.[cite:1]

## Reguły debugowania i utrzymania

Nate zostawia bardzo praktyczny zestaw reguł utrzymaniowych, które można bezpośrednio przekształcić w zasady pracy z własnym agentem.

- Gdy agent pomyli się drugi raz w tej samej rzeczy, trzeba poprawić go od razu i zaktualizować skill lub memory.[cite:1]
- Gdy ta sama instrukcja pojawia się drugi raz, trzeba zamienić ją w skill.[cite:1]
- Gdy odpowiedzi są zbyt rozwlekłe albo nie w tym tonie, trzeba poprawić soul.[cite:1]
- Gdy ma pojawić się nowa automatyzacja cykliczna, trzeba zbudować skill i dopiero potem zaplanować cron.[cite:1]
- Gdy zachowanie staje się dziwne, trzeba najpierw sprawdzić `memory.md`, bo stale memory jest według Nate’a najczęstszą przyczyną anomalii.[cite:1]
- W każdej chwili warto poprosić agenta, aby przeczytał własny memory file lub soul file, bo to najprostsza forma inspekcji aktualnego stanu systemu.[cite:1]

## Reguły skalowania do wielu agentów

Nate nie zachęca do szybkiego rozmnażania instancji, tylko do świadomej segmentacji, kiedy pojawi się realna potrzeba operacyjna.[cite:1]

### Kiedy zostać przy jednym agencie

Jeżeli zadanie jest jednorazowe albo główny agent nadal daje radę obsługiwać obszar pracy bez nadmiernego ryzyka i bez chaosu pamięci, lepiej zostać przy jednym głównym Hermesie.[cite:1]

To jest jego rekomendacja startowa: najpierw wycisnąć jak najwięcej z jednej instancji, bo wtedy użytkownik uczy się memory, skills, cronów i całej mechaniki systemu bez nadmiernego rozproszenia.[cite:1]

### Kiedy tworzyć nowego agenta

Nowa instancja ma sens wtedy, gdy dana rola wymaga innych uprawnień, innych sekretów, innych narzędzi, osobnej pamięci długoterminowej, własnego harmonogramu albo własnej grupy odbiorców.[cite:1]

Nate podkreśla też, że migracja jest łatwiejsza niż się wydaje, bo skills, crony i część logiki to po prostu pliki markdown, które można przenieść do nowego agenta, gdy pojawi się taka potrzeba.[cite:1]

### Jak układać architekturę wielu agentów

Najlepszy wzorzec według Nate’a to osobny Docker container na agenta, dzięki czemu każdy ma własne `.env`, własne memory, własne narzędzia i własne klucze.[cite:1]

To daje czystszą separację ról, lepsze śledzenie kosztów, łatwiejsze debugowanie i niższe ryzyko niż model jednego ogromnego systemu ze wszystkimi uprawnieniami.[cite:1]

### Czego unikać

Nate bardzo jasno ostrzega przed wzorcem mega-agenta, który ma wszystkie API keys, wszystkie skills, wszystkie crony i zbyt szeroki zakres odpowiedzialności, ponieważ taki układ zwiększa bloat, confusion, ryzyko i trudność diagnozowania problemów.[cite:1]

## Model organizacyjny do Antigravity

Poniżej znajduje się praktyczna wersja jego logiki, gotowa do użycia jako baza reguł systemowych w Twoim środowisku.

### Zasady systemowe

- Agent nie jest chatbotem, tylko operacyjnym wykonawcą i współpracownikiem.[cite:1]
- Trwałe fakty mają trafiać do pamięci, powtarzalne działania do skills, a ton do soul.[cite:1]
- Każda ważna instancja powinna mieć backup projektu i plików kontekstowych do prywatnego repozytorium.[cite:1]
- Sekrety powinny żyć poza rozmową, najlepiej w `.env`.[cite:1]
- Długoterminowa poprawa jakości ma wynikać z feedback loop, nie z jednorazowego setupu.[cite:1]

### Zasady dla projektowania agentów

- Zaczynaj od jednego głównego agenta.[cite:1]
- Rozdzielaj role dopiero przy różnicy w pamięci, uprawnieniach, harmonogramie lub audytorium.[cite:1]
- Nie dawaj wszystkim agentom tych samych kluczy i tych samych scope’ów.[cite:1]
- Nie mieszaj warstwy tożsamości użytkownika z warstwą projektu i z warstwą procedur.[cite:1]
- Nie zakładaj, że agent „sam się domyśli” bez dobrej pamięci i sensownych reguł wywoływania skills.[cite:1]

### Zasady dla codziennej pracy

- Obserwuj, jak agent wykonuje zadania, a nie tylko jaki daje wynik.[cite:1]
- Ucz go przez poprawki na bieżąco.[cite:1]
- Regularnie przeglądaj pamięć i usuwaj stale memory.[cite:1]
- Używaj cronów do rzeczy, które naprawdę powinny dziać się bez ręcznego wyzwalania.[cite:1]
- Traktuj agenta jak członka zespołu, którego trzeba wdrażać i trenować, a nie jak funkcję jednorazową.[cite:1]

## Najbardziej użyteczne wzorce do skopiowania

Z całego tutoriala szczególnie mocno nadają się do przeniesienia do Antigravity następujące wzorce:

1. Warstwowy podział na `user.md`, `memory.md`, `soul.md`, `skill.md` i lokalny plik projektu.[cite:1]
2. Reguła „drugi raz = skill”, która bardzo dobrze nadaje się na trigger proceduralizacji.[cite:1]
3. Reguła „drugi błąd = poprawka w memory lub skill”, która wspiera szybkie uczenie agenta.[cite:1]
4. GitHub jako source of truth dla backupu i przenośności stanu systemu.[cite:1]
5. Docker jako warstwa izolacji przy wielu agentach.[cite:1]
6. Least privilege i osobne klucze per agent jako domyślny model bezpieczeństwa.[cite:1]
7. Crony jako aktywna warstwa zachowania operacyjnego, a nie tylko techniczny scheduler.[cite:1]

## Wniosek wdrożeniowy

Najkrótsza i najwierniejsza wersja podejścia Nate’a brzmi następująco: zacznij od jednego dobrze skonfigurowanego agenta, nadaj mu pamięć, soul i pierwsze skills, podepnij backup do GitHub, przenieś sekrety do `.env`, zautomatyzuj pierwsze crony, a dopiero później dziel system na kolejne role i kontenery.[cite:1]

To podejście minimalizuje chaos, przyspiesza naukę mechaniki systemu i daje architekturę, którą da się rozwijać bez popadania w megasystem pełen splątanych uprawnień i nieczytelnej pamięci.[cite:1]
