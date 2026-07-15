# Blueprint systemowy: Hermes Agent jako autonomiczny system pracy, pamięci i orkiestracji

## Streszczenie operacyjne
Ten materiał pokazuje Hermes Agent nie jako pojedynczy chatbot, ale jako całodobowego agenta operacyjnego, który ma działać jak osobisty chief of staff, pracownik wykonawczy i druga pamięć użytkownika jednocześnie [page:3, {ts:108}][page:3, {ts:339}]. Systemowy model wynikający z tutorialu opiera się na pięciu osiach: pamięć trwała, samodoskonalące się skille, komunikacja przez kanał wiadomości, harmonogram zadań cyklicznych oraz dashboard sterujący agentami i pracą [page:3, {ts:129}][page:3, {ts:173}][page:3, {ts:925}][page:3, {ts:1085}].

Z perspektywy architektury najważniejsza idea jest prosta: użytkownik nie powinien za każdym razem „używać AI od zera”, tylko budować system, który zapamiętuje kontekst, ulepsza procedury i przejmuje część codziennych zadań [page:3, {ts:1793}][page:3, {ts:1826}]. Hermes jest w tym modelu warstwą sterowania i wykonania dla powtarzalnej pracy osobistej, operacyjnej i prototypowej, a nie głównym narzędziem do ciężkiego, głębokiego developmentu dużych aplikacji [page:3, {ts:339}][page:3, {ts:425}].

## Czym jest opisywany system / metoda / framework
Opisywany system to personal agent operating layer: warstwa agentowa, która żyje tam, gdzie żyje użytkownik, działa 24/7 i jest dostępna przez komunikatory takie jak Telegram, Discord, WhatsApp czy iMessage [page:3, {ts:149}][page:3, {ts:751}]. Ma pełnić funkcję autonomicznego pracownika, który zna użytkownika, jego cele, aktualne projekty i sposób pracy, a następnie na tej podstawie wykonuje zadania proaktywne i reaktywne [page:3, {ts:129}][page:3, {ts:894}].

Sedno frameworku polega na tym, że pamięć i skille są lokalne, audytowalne i ewoluują po każdym zadaniu, ponieważ agent zapisuje, co zrobił, co zadziałało i jak ma to wykonać lepiej następnym razem [page:3, {ts:1793}][page:3, {ts:1863}]. W praktyce Hermes jest połączeniem drugiego mózgu, harmonogramu, warstwy automatyzacji, interfejsu wykonawczego i środowiska orkiestracji dla wielu profili agentowych [page:3, {ts:1673}][page:3, {ts:1224}].

## Główne filary / komponenty / warstwy
### 1. Warstwa tożsamości i kontekstu użytkownika
Pierwszym filarem jest wprowadzenie do systemu informacji o użytkowniku: kim jest, nad czym pracuje i jakie ma cele oraz ambicje [page:3, {ts:862}][page:3, {ts:894}]. Ten blok informacji nie jest onboardingową formalnością, tylko fundamentem całej późniejszej proaktywności Hermesa [page:3, {ts:899}].

### 2. Warstwa pamięci trwałej
Hermes zapisuje wspomnienia i skille w plikach Markdown na komputerze użytkownika, dzięki czemu pamięć nie jest czarną skrzynką ukrytą w chmurze [page:3, {ts:1793}][page:3, {ts:1807}]. Ta warstwa obejmuje zarówno długoterminowe informacje o użytkowniku, jak i zapis procedur oraz wcześniejszych interakcji [page:3, {ts:1813}].

### 3. Warstwa samodoskonalenia
Najważniejszą cechą systemu jest self-improvement: po wykonaniu zadania agent analizuje, jak je zrobił, zapisuje najlepszą ścieżkę i wykorzystuje ją przy podobnych zadaniach w przyszłości [page:3, {ts:1826}][page:3, {ts:1890}]. To sprawia, że Hermes nie jest statycznym narzędziem, lecz systemem, którego jakość rośnie wraz z użyciem [page:3, {ts:1905}].

### 4. Warstwa komunikacji
Kanałem operacyjnym nie jest aplikacja webowa jako taka, tylko przede wszystkim komunikator, z którego użytkownik rzeczywiście korzysta na co dzień [page:3, {ts:149}][page:3, {ts:751}]. Najmocniej rekomendowanym kanałem jest Telegram, ponieważ według materiału najlepiej wspiera scenariusze agentowe, rozmowy między agentami i organizację komunikacji [page:3, {ts:757}][page:3, {ts:778}].

### 5. Warstwa harmonogramu i automatyzacji
Hermes posiada cron jobs, czyli zadania cykliczne definiowane prostym językiem naturalnym, bez konieczności ręcznego programowania harmonogramu [page:3, {ts:925}][page:3, {ts:939}]. Dzięki temu agent może wykonywać pracę w tle, np. każdej nocy o 2:00 budować mały użyteczny artefakt wspierający cele użytkownika [page:3, {ts:963}][page:3, {ts:1032}].

### 6. Warstwa dashboardu
Dashboard służy do zarządzania modelami, cronami, skillami, pluginami, profilami agentów i Kanbanem zadań [page:3, {ts:1085}][page:3, {ts:1101}]. Nie jest obowiązkowy do codziennej komunikacji, ale pełni funkcję panelu administracyjnego i operacyjnego dla systemu [page:3, {ts:1113}].

### 7. Warstwa pracy zadaniowej: Kanban
Kanban jest centralną warstwą przepływu pracy, gdzie zadania przechodzą przez statusy triage, to-do, ready, in progress, blocked i done [page:3, {ts:1276}]. Szczególnie istotny jest status triage, bo zadanie wrzucone do tej kolumny może zostać automatycznie rozbite na podzadania i przypisane subagentom [page:3, {ts:1284}][page:3, {ts:1294}].

### 8. Warstwa wieloagentowa
Hermes wspiera wiele profili agentowych, czyli logicznie odrębnych agentów działających obok siebie [page:3, {ts:1224}]. Ta warstwa jest przydatna wtedy, gdy użytkownik potrzebuje różnych person, zakresów pracy lub zestawów skilli dla różnych typów zadań [page:3, {ts:1236}].

### 9. Warstwa pluginów i narzędzi wykonawczych
System można rozszerzać o pluginy i dodatkowe zdolności, takie jak browser automation, browser crawling, image generation, video generation i computer use [page:3, {ts:1167}][page:3, {ts:1194}][page:3, {ts:1921}]. To warstwa, która zwiększa zakres tego, co agent realnie może zrobić na urządzeniach i w sieci [page:3, {ts:1954}].

### 10. Warstwa mission control
Mission control to własny, niestandardowy interfejs zbudowany przez samego agenta, zawierający specjalistyczne narzędzia potrzebne użytkownikowi [page:3, {ts:2074}][page:3, {ts:2197}]. W przykładzie obejmuje content pipeline, memory wiki, widok dokumentów i wizualizację aktywności agentów [page:3, {ts:2117}][page:3, {ts:2132}][page:3, {ts:2160}].

## Architektura logiki
### Co jest pamięcią
Pamięcią są lokalne pliki Markdown przechowujące wspomnienia i skille oraz pełne logi sesji, które pozwalają odtworzyć wszystko, co było omawiane z agentem [page:3, {ts:1673}][page:3, {ts:1793}]. Pamięć obejmuje zarówno dane deklaratywne o użytkowniku, jak i pamięć proceduralną, czyli wiedzę o tym, jak wykonywać zadania [page:3, {ts:1863}].

### Co jest procedurą
Procedurą są skille oraz zapisane ścieżki działania, które agent wypracował podczas wykonywania wcześniejszych zadań i potem odtwarza przy kolejnych podobnych poleceniach [page:3, {ts:1863}][page:3, {ts:1898}]. Procedury mogą być również uruchamiane jako zadania cykliczne lub jako workflow w Kanbanie [page:3, {ts:925}][page:3, {ts:1284}].

### Co jest sterowaniem
Sterowanie odbywa się przez dwa kanały: naturalny język w komunikatorze oraz panel dashboardu [page:3, {ts:939}][page:3, {ts:1085}]. Model sterowania jest celowo prosty: użytkownik opisuje rezultat i termin, a nie sekwencję kliknięć czy kroków technicznych [page:3, {ts:1045}].

### Co jest harmonogramem
Harmonogramem są cron jobs oraz rytm pracy Kanbanu, w którym zadania trafiają do triage, są rozbijane i podejmowane przez subagentów [page:3, {ts:925}][page:3, {ts:1284}]. Harmonogram może być stały, jak zadanie nocne o 2:00, albo reaktywny, wynikający z porannego zrzutu zadań do triage [page:3, {ts:963}][page:3, {ts:1324}].

### Co jest warstwą wykonawczą
Warstwą wykonawczą są same profile Hermesa, subagenci, pluginy, narzędzia browser/computer use oraz generatory assetów takich jak obrazy czy wideo [page:3, {ts:1224}][page:3, {ts:1921}][page:3, {ts:2004}]. To ta warstwa tworzy dokumenty, przenosi pliki, czyta transkrypcje, generuje media i buduje mikroaplikacje [page:3, {ts:1552}][page:3, {ts:1849}].

### Co jest warstwą bezpieczeństwa
Warstwa bezpieczeństwa w tym materiale nie jest budowana przez izolację infrastruktury, lecz przez zakres poleceń, osąd operatora i kontrolę nad tym, co agent faktycznie ma zrobić [page:3, {ts:2392}][page:3, {ts:2456}]. Dodatkowym elementem bezpieczeństwa i kontroli jest lokalność pamięci oraz audytowalność plików Markdown [page:3, {ts:1793}][page:3, {ts:1813}].

### Co jest warstwą integracji
Warstwę integracji tworzą modele, komunikatory, pluginy, narzędzia systemowe oraz sieć urządzeń spinanych np. przez Tailscale [page:3, {ts:571}][page:3, {ts:751}][page:3, {ts:1590}]. Integracje te nie są dodatkami kosmetycznymi, tylko sposobem rozszerzenia zasięgu agenta na realne środowisko pracy użytkownika [page:3, {ts:1610}].

## Workflow wdrożeniowy
1. Zainstaluj Hermesa przez komendę z oficjalnej strony i przejdź przez quick setup [page:3, {ts:510}][page:3, {ts:560}].
2. Jeśli masz OpenClaw, zdecyduj świadomie, czy importować pamięć i skille; materiał sugeruje, że czysty start często jest lepszy niż pełna migracja [page:3, {ts:532}][page:3, {ts:549}].
3. Wybierz model według budżetu i jakości: Anthropic jako wariant premium, OpenAI jako poziom średni, portal/XAI jako opcje tańsze [page:3, {ts:571}][page:3, {ts:619}][page:3, {ts:688}].
4. Skonfiguruj kanał komunikacyjny, preferencyjnie Telegram, i połącz go tokenem z Hermesem [page:3, {ts:751}][page:3, {ts:805}].
5. Na początku przekaż agentowi trzy bloki kontekstu: kim jesteś, nad czym pracujesz i jakie masz cele [page:3, {ts:845}][page:3, {ts:907}].
6. Następnie zdefiniuj pierwsze zadanie cykliczne, które ma działać proaktywnie i przynosić użyteczne artefakty zgodne z Twoimi ambicjami [page:3, {ts:918}][page:3, {ts:963}].
7. Otwórz dashboard przez komendę terminalową i sprawdź modele, crony, skille, pluginy, profile i Kanban [page:3, {ts:1085}][page:3, {ts:1101}].
8. Włącz potrzebne pluginy, szczególnie browser automation, computer use i ewentualnie image generation [page:3, {ts:1173}][page:3, {ts:1194}][page:3, {ts:1942}].
9. Zacznij codziennie rano wrzucać zadania do triage w Kanbanie, aby agent rozbijał je na podzadania i przejmował część dnia roboczego [page:3, {ts:1276}][page:3, {ts:1324}].
10. Buduj własne mission control dopiero po uruchomieniu podstawowego obiegu pracy, tak aby mieć miejsce na custom tools, pamięć, dokumenty i widok pipeline'ów [page:3, {ts:2074}][page:3, {ts:2235}].
11. Jeśli Hermes napotka problemy techniczne, otwórz jego folder w Claude Code lub Codex i użyj ich jako warstwy debugowania [page:3, {ts:2278}][page:3, {ts:2307}].

## Zasady operacyjne
- Używaj Hermesa jako general-purpose chief of staff do pracy operacyjnej, researchu, prototypów, dokumentów, administracji plikami i zadań codziennych [page:3, {ts:339}][page:3, {ts:353}].
- Nie używaj Hermesa jako głównego narzędzia do ciężkiej, długiej sesji budowy dużego produktu software'owego; do tego lepsze są Claude Code i Codex [page:3, {ts:425}][page:3, {ts:446}].
- Jeśli chcesz zwiększać jakość wyniku w czasie, kieruj proces do Hermesa, bo jego przewaga polega na self-improvement i pamięci proceduralnej [page:3, {ts:402}][page:3, {ts:1890}].
- Jeśli zależy Ci na szybkim, okazjonalnym prototypie z telefonu lub w ruchu, Hermes jest właściwym wyborem [page:3, {ts:373}][page:3, {ts:380}].
- Gdy zadanie można delegować agentowi, wrzucaj je do triage w Kanbanie zamiast wykonywać ręcznie [page:3, {ts:1324}][page:3, {ts:1365}].
- Jeśli zadanie ma się powtarzać, zamień je na cron zamiast pamiętać o nim samodzielnie [page:3, {ts:925}][page:3, {ts:1032}].
- Jeśli system zaczyna być zbyt manualny, zbuduj mission control i warstwę custom tools, ale dopiero na bazie realnych potrzeb [page:3, {ts:2074}][page:3, {ts:2235}].
- Jeżeli chcesz odzyskać dawny kontekst, użyj session recall zamiast odtwarzać historię ręcznie [page:3, {ts:1673}][page:3, {ts:1721}].
- Jeżeli agent ma działać dobrze, karm go kontekstem osobistym i celami; bez tego jego proaktywność będzie płytka [page:3, {ts:894}][page:3, {ts:900}].

## Best practices
### Wprowadzenie pełnego kontekstu na starcie
Dobrą praktyką jest świadome przekazanie agentowi informacji o tożsamości, projektach i celach przed rozpoczęciem właściwej pracy [page:3, {ts:845}][page:3, {ts:907}]. Dzięki temu proaktywne działania i późniejsze rekomendacje nie są ogólne, tylko zakotwiczone w rzeczywistych priorytetach [page:3, {ts:894}].

### Proaktywność przez cykliczne zadania
Zamiast używać agenta wyłącznie reaktywnie, warto od razu zaplanować zadanie nocne lub poranne, które codziennie dostarcza mały użyteczny efekt [page:3, {ts:963}][page:3, {ts:1040}]. To przekształca Hermesa z narzędzia „na wezwanie” w realną warstwę pracy w tle [page:3, {ts:982}].

### Telegram jako domyślny interfejs operacyjny
Materiał jednoznacznie wskazuje Telegram jako najlepszy główny kanał pracy z agentem, ponieważ najlepiej wspiera przyszłe scenariusze agentowe i komunikację między agentami [page:3, {ts:757}][page:3, {ts:778}]. To praktyka ważna nie tylko z powodu wygody, ale też przyszłej skalowalności kanału [page:3, {ts:784}].

### Triage poranny w Kanbanie
Bardzo praktyczną zasadą jest codzienne poranne wrzucanie do Kanbanu wszystkich zadań, które może obsłużyć AI, zanim użytkownik zacznie własną pracę [page:3, {ts:1324}][page:3, {ts:1365}]. Taki rytuał zmniejsza obciążenie poznawcze i pozwala agentowi zacząć działać równolegle z użytkownikiem [page:3, {ts:1345}].

### Audytowalna pamięć lokalna
Przechowywanie pamięci i skilli w lokalnych plikach Markdown jest ważną dobrą praktyką, bo umożliwia inspekcję, korekty i zrozumienie tego, co agent faktycznie wie [page:3, {ts:1793}][page:3, {ts:1813}]. To przewaga nad systemami, w których pamięć jest ukryta w chmurze i nieprzejrzysta [page:3, {ts:1807}].

### Używanie Hermesa do budowy własnych narzędzi dla Hermesa
Jedną z ciekawszych praktyk jest wykorzystywanie Hermesa do tworzenia narzędzi, dashboardów i rozszerzeń dla samego systemu, np. mission control albo rozszerzeń Kanbanu [page:3, {ts:391}][page:3, {ts:2074}]. To wzmacnia spójność architektury, bo system rozwija narzędzia najlepiej dopasowane do własnego workflow [page:3, {ts:397}].

### Drugi mózg przez session recall
Warto kierować znaczną część idei, linków, use case'ów i dyskusji przez Hermesa, ponieważ session recall pozwala odtwarzać je później jako uporządkowany zasób wiedzy [page:3, {ts:1673}][page:3, {ts:1766}]. To praktyka budowania drugiego mózgu nie tylko z notatek, lecz z całej historii współpracy z agentem [page:3, {ts:1771}].

## Security / ryzyka / ograniczenia
### Podejście do bezpieczeństwa
Materiał przyjmuje podejście oparte na sprawczości użytkownika: agent robi to, do czego został poproszony, więc kluczowe jest rozsądne formułowanie poleceń i świadomość ich skutków [page:3, {ts:2392}][page:3, {ts:2456}]. Z tego wynika model bezpieczeństwa oparty bardziej na odpowiedzialności operatora niż na twardej izolacji środowiska [page:3, {ts:2463}].

### Ograniczanie ryzyka
Podstawową metodą ograniczania ryzyka jest unikanie poleceń destrukcyjnych, nieprzemyślanych lub zbyt szerokich, zamiast mnożenia warstw infrastrukturalnych i nowych kont [page:3, {ts:2431}][page:3, {ts:2544}]. Materiał bardzo wyraźnie odrzuca nadmiarową złożoność operacyjną, jeśli nie wynika ona z realnego zagrożenia [page:3, {ts:2506}].

### Zasady uprawnień
Chociaż nie pada formalna polityka uprawnień, z logiki materiału wynika zasada kontroli zakresu: agent wykonuje tylko zadania, do których jest skierowany, a użytkownik odpowiada za to, co uruchamia [page:3, {ts:2401}][page:3, {ts:2474}]. Oznacza to, że główną kontrolą dostępu jest dobrze sformułowane polecenie i świadome uruchamianie narzędzi [page:3, {ts:2456}].

### Sekrety i konta
W materiale nie ma rozbudowanej procedury zarządzania sekretami, ale jest wyraźne stanowisko przeciwko tworzeniu osobnych kont i osobnych środowisk bez konkretnej potrzeby [page:3, {ts:2493}][page:3, {ts:2544}]. To podejście upraszcza wdrożenie, ale wymaga dojrzałości operatora i świadomego obchodzenia się z integracjami [page:3, {ts:2512}].

### Najważniejsze ograniczenia systemu
Największym ograniczeniem nie jest sama technologia, lecz ryzyko złego dopasowania narzędzia do zadania [page:3, {ts:425}]. Hermes nie jest według materiału optymalny do najcięższych sesji programistycznych z bardzo złożonym testowaniem end-to-end, gdzie lepiej sprawdzają się Claude Code i Codex [page:3, {ts:446}][page:3, {ts:464}].

### Krytyczna uwaga
Sekcja bezpieczeństwa w tutorialu zawiera bardzo kategoryczne tezy i świadomie minimalizuje część obaw [page:3, {ts:2344}][page:3, {ts:2574}]. Jako zasada systemowa warto zachować z niej głównie ideę świadomego promptowania i kontroli zakresu działań, a nie bezrefleksyjnie kopiować pełne lekceważenie izolacji środowiska [page:3, {ts:2456}].

## Skalowanie / delegowanie / modularność
### Kiedy tworzyć osobne moduły lub agentów
Osobne profile agentowe warto tworzyć wtedy, gdy pojawia się potrzeba oddzielenia zakresów pracy, stylów działania lub zestawów skilli [page:3, {ts:1224}][page:3, {ts:1236}]. W materiale widać, że wieloagentowość jest naturalnym rozszerzeniem systemu, ale nie jest wymagana od pierwszej minuty [page:3, {ts:1015}].

### Kiedy zostać przy jednym systemie
Jeśli użytkownik dopiero startuje, pojedynczy Hermes z dobrą pamięcią, cronami i Kanbanem jest wystarczającym rdzeniem [page:3, {ts:821}][page:3, {ts:918}]. W tym modelu złożoność dodaje się dopiero po opanowaniu podstawowej relacji: użytkownik – jeden agent – pamięć – harmonogram – zadania [page:3, {ts:1085}].

### Jak autor myśli o wzroście złożoności
Złożoność rośnie tu modularnie: najpierw konfiguracja i kanał komunikacji, potem pamięć i proaktywność, następnie dashboard, pluginy, Kanban, profile, a na końcu mission control z custom toolingiem [page:3, {ts:510}][page:3, {ts:925}][page:3, {ts:1085}][page:3, {ts:2074}]. To ważna zasada architektoniczna: nie budować wszystkiego od razu, tylko dokładać warstwy zgodnie z dojrzałością workflow [page:3].

### Decision tree: kiedy Hermes, kiedy Claude Code / Codex
- Użyj Hermesa, gdy potrzebujesz general-purpose pracownika, administracji, researchu, dokumentów, plików, prototypów i zadań powtarzalnych [page:3, {ts:339}][page:3, {ts:367}].
- Użyj Hermesa, gdy ważna jest pamięć długotrwała, ciągłość kontekstu i samodoskonalenie procesu [page:3, {ts:173}][page:3, {ts:1890}].
- Użyj Claude Code lub Codex, gdy budujesz duży, złożony produkt software'owy i potrzebujesz głębokiego środowiska developerskiego oraz testów end-to-end [page:3, {ts:425}][page:3, {ts:459}].
- Użyj Claude Code lub Codex jako warstwy naprawczej, gdy trzeba debugować samego Hermesa [page:3, {ts:2278}][page:3, {ts:2307}].

## Antywzorce i błędy
- Traktowanie Hermesa jak kolejnego jednorazowego czatu zamiast systemu z pamięcią, cyklicznymi zadaniami i workflow [page:3, {ts:173}][page:3, {ts:925}].
- Pomijanie wprowadzenia podstawowego kontekstu o użytkowniku, projektach i celach [page:3, {ts:845}][page:3, {ts:894}].
- Używanie niewłaściwego modelu do budżetu lub jakości, bez świadomego wyboru kompromisu [page:3, {ts:571}][page:3, {ts:726}].
- Stawianie wszystkiego na jedną sesję ręcznej pracy zamiast delegowania zadań do triage i cronów [page:3, {ts:1276}][page:3, {ts:1324}].
- Oczekiwanie, że agent będzie skuteczny bez pluginów i bez włączenia narzędzi wykonawczych [page:3, {ts:1173}][page:3, {ts:1942}].
- Używanie Hermesa do pracy, do której lepiej nadaje się Claude Code lub Codex, szczególnie przy dużych aplikacjach [page:3, {ts:425}][page:3, {ts:446}].
- Trzymanie dokumentów i artefaktów w losowych folderach bez warstwy mission control lub czytelnego dostępu [page:3, {ts:2166}][page:3, {ts:2178}].
- Mylenie prostoty sterowania z brakiem dyscypliny; fakt, że polecenia wydaje się po ludzku, nie znaczy, że system nie wymaga jasnych rezultatów i terminów [page:3, {ts:939}][page:3, {ts:1045}].

## Reguły do przeniesienia do mojego systemu
- Agent ma znać trzy rzeczy od początku: kim jestem, nad czym pracuję i dokąd zmierzam [page:3, {ts:894}].
- Wszystko, co powtarzalne, ma być zamieniane na cron, skill albo workflow Kanbanu [page:3, {ts:925}][page:3, {ts:1284}].
- Wszystko, co było już raz zrobione dobrze, ma zostać zapisane jako proceduralna pamięć do ponownego użycia [page:3, {ts:1863}][page:3, {ts:1898}].
- Pamięć i zasady działania muszą być audytowalne i możliwe do ręcznej korekty [page:3, {ts:1793}][page:3, {ts:1813}].
- Domyślny kanał operacyjny agenta powinien być osadzony w miejscu, gdzie użytkownik i tak żyje komunikacyjnie [page:3, {ts:149}][page:3, {ts:757}].
- Każdy poranek powinien zaczynać się od triage zadań delegowalnych do AI [page:3, {ts:1324}][page:3, {ts:1365}].
- Agent ma być rozliczany z deliverables: co ma zrobić, kiedy ma to być gotowe i w jakiej formie ma zostać dostarczone [page:3, {ts:1045}][page:3, {ts:1051}].
- Session recall ma pełnić rolę drugiego mózgu dla pomysłów, linków, eksperymentów i wcześniejszych rozmów [page:3, {ts:1673}][page:3, {ts:1771}].
- Hermesa należy używać do general-purpose operacji i prototypów, a ciężki development przenosić do Claude Code lub Codex [page:3, {ts:339}][page:3, {ts:446}].
- Mission control należy budować jako warstwę custom tools na bazie realnego workflow, nie jako ozdobny dashboard bez funkcji [page:3, {ts:2074}][page:3, {ts:2235}].
- Pluginy i computer use powinny być włączane świadomie jako realne rozszerzenie zasięgu wykonawczego agenta [page:3, {ts:1173}][page:3, {ts:1942}].
- Debugowanie agenta powinno odbywać się przez zewnętrzną warstwę naprawczą, np. Claude Code lub Codex otwierające folder Hermesa [page:3, {ts:2278}][page:3, {ts:2307}].

## Blueprint wdrożeniowy
### Od czego zacząć
Zacznij od pojedynczego Hermesa spiętego z Telegramem, a nie od złożonego systemu wielu agentów [page:3, {ts:757}][page:3, {ts:821}]. Pierwszym celem nie jest perfekcyjna automatyzacja, lecz ustanowienie relacji agent–pamięć–kanał komunikacji–harmonogram [page:3, {ts:129}][page:3, {ts:925}].

### Co skonfigurować najpierw
Najpierw ustaw model, komunikator, podstawowe pluginy, dane o sobie i pierwszy cron [page:3, {ts:571}][page:3, {ts:805}][page:3, {ts:1173}][page:3, {ts:845}][page:3, {ts:963}]. Dopiero potem wchodź w Kanban, profile wieloagentowe i mission control [page:3, {ts:1224}][page:3, {ts:1276}][page:3, {ts:2074}].

### Co przenieść do pamięci
Do pamięci przenieś opis swojej roli, aktywne projekty, cele kwartalne, preferencje pracy, ważne linki, wcześniejsze use case'y, najlepsze prompty i wyniki wykonanych zadań [page:3, {ts:845}][page:3, {ts:1713}]. Warto też przenosić transkrypcje, pomysły i wszystkie artefakty, które mają wartość długoterminową [page:3, {ts:1445}][page:3, {ts:2160}].

### Co zamienić w playbooki / skills / SOP-y
W playbooki i skille zamień powtarzalne zadania: analiza tutoriali, wydobywanie transcriptów, poranne przypomnienia edukacyjne, porządkowanie plików, tworzenie prezentacji, research i generowanie drobnych prototypów [page:3, {ts:1445}][page:3, {ts:1552}][page:3, {ts:1954}]. SOP-ami powinny zostać też procedury delegowania zadań do triage, konfiguracji nowych pluginów oraz debugowania systemu [page:3, {ts:1276}][page:3, {ts:2278}].

### Co automatyzować później
Później automatyzuj warstwę wielourządzeniową przez Tailscale, use case'y edukacyjne, generowanie assetów, content pipeline i custom mission control [page:3, {ts:1590}][page:3, {ts:2004}][page:3, {ts:2117}]. To są rozszerzenia, które mają największy sens dopiero wtedy, gdy podstawowy agent już działa stabilnie [page:3, {ts:2074}].

### Jak nie przesadzić ze złożonością
Nie zaczynaj od wielu profili, wielu integracji i niestandardowego dashboardu jednocześnie [page:3, {ts:1224}][page:3, {ts:2235}]. Najpierw zbuduj jednego użytecznego pracownika z pamięcią, cronem i Kanbanem, a każdą kolejną warstwę dodawaj tylko wtedy, gdy wynika z realnego tarcia w obecnym workflow [page:3, {ts:925}][page:3, {ts:1276}].
