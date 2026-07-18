# Hermes Agent — Blueprint Systemowy: 6 Przypadków Użycia jako Architektura Autonomicznego Agenta

## Streszczenie operacyjne

Tutorial prezentuje sześć wzorców użycia Hermes Agent, które razem tworzą spójną architekturę 24/7 autonomicznego asystenta operacyjnego. Model myślenia autora: nie chodzi o użycie agenta jako lepszego chatbota — chodzi o delegowanie całych kategorii pracy do równolegle działających, wyspecjalizowanych instancji agenta. [page:1] Człowiek nadaje kierunek, agent wykonuje, uczy się i raportuje. Kluczowy wynik: autor prowadzi pięć różnych instancji Hermes działających jednocześnie w osobnych zadaniach. [page:1]

## Czym jest opisywany system / metoda / framework

Hermes Agent to autonomiczny agent AI działający lokalnie lub w chmurze, zdolny do długotrwałego działania bez nadzoru (tryb `/goal` — ponad 24h), kontrolowania przeglądarki i systemu operacyjnego oraz zarządzania zadaniami przez wbudowany Kanban. [page:1] Buduje i utrzymuje własną pamięć długoterminową oraz może działać przez prywatną sieć na wielu urządzeniach jednocześnie. [page:1] Fundamentalna różnica wobec innych agentów (np. OpenClaw) polega na tym, że Hermes ma natywny Kanban, tryb `/background`, tryb `/goal` oraz wbudowany system pamięci, co daje mu autonomię strukturalną, a nie tylko autonomię pojedynczego zadania. [page:1]

## Główne filary / komponenty / warstwy

### 1. `/goal` — Tryb długoterminowego zadania

Tryb `/goal` umożliwia uruchomienie agenta na wielogodzinne lub kilkudniowe zadania bez nadzoru. [page:1] Kluczowym warunkiem jest meta-promptowanie, czyli wygenerowanie szczegółowego prompta przez AI przed wywołaniem `/goal`. [page:1] Bez meta-prompta `/goal` zachowuje się jak zwykła rozmowa, co znacząco obniża skuteczność. [page:1]

### 2. Kanban Board — Centrum dowodzenia dniem

Kanban jest wbudowanym panelem zarządzania zadaniami, dostępnym po wywołaniu `hermes dashboard` w terminalu i otwarciu odpowiedniego adresu URL. [page:1] Zadania wrzucane do kolumny Triage są automatycznie przypisywane do agentów i podagentów, tworząc codzienny interfejs operacyjny między człowiekiem a agentem. [page:1]

### 3. Memory Wiki — Zewnętrzna pamięć długoterminowa

Memory Wiki to generowana przez agenta strona internetowa, która zawiera listę wszystkich tematów rozmów oraz dzienne logi działań. [page:1] Użytkownik może klikać w poszczególne tematy i logi, aby drążyć szczegóły, dzięki czemu wiki pełni rolę zarówno pamięci dla człowieka, jak i bazy kontekstowej dla samego agenta. [page:1]

### 4. Technical Research Mode — Wywiad technologiczny o konkurencji

W trybie research agent otwiera przeglądarkę, nawiguje do wskazanego serwisu, analizuje konsolę deweloperską i zbiera informacje o bibliotekach oraz stacku technologicznym. [page:1] Wynikową analizę zapisuje w formie raportu markdown, który można wprost podać innemu agentowi budującemu produkt. [page:1]

### 5. Computer Administrator (Tailscale) — Sieć urządzeń

Po zainstalowaniu Tailscale na wszystkich urządzeniach Hermes uzyskuje dostęp do całej prywatnej sieci użytkownika, obejmującej komputer główny, laptop, tablet czy telefon. [page:1] Dzięki temu może pobierać pliki, instalować LLM-y i testować aplikacje hostowane lokalnie na innym urządzeniu, nawet gdy użytkownik jest poza domem. [page:1]

### 6. Morning Priority Prompt — Pętla samorozwoju

Codzienny prompt poranny sprawia, że o określonej godzinie (np. 9:00) agent proaktywnie pyta użytkownika o priorytet dnia. [page:1] Na podstawie odpowiedzi generuje listę zadań, które może wykonać samodzielnie, oraz aktualizuje swoją pamięć na temat użytkownika, tworząc ciągłą pętlę uczenia. [page:1]

## Architektura logiki

| Warstwa                | Opis                                                                 |
|------------------------|----------------------------------------------------------------------|
| Pamięć                 | Memory Wiki (długoterminowa) oraz aktualizacje z Morning Prompt     |
| Procedura              | `/goal` z meta-promptem jako szczegółowy opis wieloetapowego zadania|
| Sterowanie             | Kanban Triage jako miejsce delegowania zadań do agenta             |
| Harmonogram            | Morning Priority Prompt jako codzienny trigger o stałej godzinie   |
| Warstwa wykonawcza     | Równoległe instancje Hermes, każda pracująca nad innym zadaniem     |
| Warstwa bezpieczeństwa | Tailscale jako prywatna sieć oraz świadome nadawanie uprawnień      |
| Warstwa integracji     | Handoff: Hermes → Claude Code / Codex po generowaniu kodu           |

Pamięć opiera się na Memory Wiki, która przechowuje długoterminowe logi oraz listę tematów, oraz na bieżących aktualizacjach wynikających z porannych priorytetów. [page:1] Procedury są odzwierciedlone w meta-promptach używanych z `/goal`, które opisują szczegółowe wieloetapowe zadania. [page:1] Sterowanie pracą odbywa się przez Kanban, w którym człowiek wrzuca zadania do Triage, a agent je podejmuje autonomicznie. [page:1]

Harmonogram wyznacza Morning Priority Prompt, który codziennie o ustalonej godzinie inicjuje interakcję. [page:1] Warstwa wykonawcza to wiele równoległych instancji Hermes, każda przypisana do innej kategorii pracy lub projektu. [page:1] Warstwa bezpieczeństwa opiera się na Tailscale jako prywatnej sieci oraz na świadomym udzielaniu pozwoleń przez użytkownika przy działaniach systemowych. [page:1] Warstwa integracji obejmuje przekazywanie wyników generowania (kod, raporty) do wyspecjalizowanych narzędzi takich jak Claude Code czy Codex. [page:1]

## Workflow wdrożeniowy

### Krok 1 — Instalacja i konfiguracja podstawowa

Najpierw należy zainstalować i skonfigurować Hermes Agent zgodnie z instrukcją autora w osobnym materiale. [page:1] Autor zaleca, aby nie wdrażać wszystkich przypadków użycia jednocześnie, lecz zacząć od jednego lub dwóch. [page:1]

### Krok 2 — Pierwszy `/goal` z meta-promptem

Przed uruchomieniem `/goal` użytkownik powinien poprosić AI o wygenerowanie idealnego prompta dla danego zadania, np. prosząc: „Pomóż mi zbudować idealny prompt do /goal, bo chcę zrobić X w taki i taki sposób”. [page:1] Wygenerowany meta-prompt należy skopiować i wkleić jako wejście do `/goal`, dopuszczając dodatkowe pytania agenta przed startem jako element kalibracji. [page:1]

### Krok 3 — Uruchomienie Kanban jako rutyny porannej

Po uruchomieniu `hermes dashboard` w terminalu i wejściu na wskazany adres URL użytkownik otwiera zakładkę Kanban. [page:1] Każdego ranka wpisuje do kolumny Triage zadania, które agent może wykonać autonomicznie, a następnie przechodzi do własnej pracy, by później wrócić i odebrać rezultaty. [page:1]

### Krok 4 — Budowa Memory Wiki

Aby zbudować Memory Wiki, użytkownik wkleja konkretny prompt opisujący wymagania wobec tej strony, np. prośbę o witrynę zawierającą listę tematów i dzienne logi, z możliwością drążenia szczegółów. [page:1] Agent tworzy stronę, która staje się dziennikiem współpracy oraz źródłem kontekstu dla kolejnych sesji. [page:1]

### Krok 5 — Konfiguracja Tailscale na wszystkich urządzeniach

Zainstalowanie Tailscale na każdym urządzeniu użytkownika pozwala Hermesowi widzieć całą prywatną sieć i operować na plikach oraz usługach z dowolnego miejsca. [page:1] Dzięki temu agent może np. pobierać pliki z innego komputera, instalować modele na maszynie domowej czy testować aplikacje hostowane lokalnie. [page:1]

### Krok 6 — Aktywacja Morning Priority Prompt

Użytkownik definiuje prompt, który sprawi, że każdego ranka o określonej godzinie agent zapyta o priorytet dnia, wygeneruje listę zadań i zaktualizuje swoje wspomnienia. [page:1] Ten nawyk buduje pętlę ciągłego uczenia agenta na temat użytkownika i jego priorytetów. [page:1]

### Krok 7 — Włączenie Technical Research jako stałego workflow

W sytuacjach, gdy potrzebny jest wywiad technologiczny lub analiza konkurencji, użytkownik zleca Hermesowi pełny breakdown techniczny wybranego serwisu lub produktu. [page:1] Rezultat w postaci raportu markdown trafia do innych agentów jako dane wejściowe przy budowaniu lub planowaniu produktów. [page:1]

## Zasady operacyjne

### Kiedy używać `/goal`

Tryb `/goal` należy stosować do złożonych, długotrwałych zadań, takich jak budowa aplikacji od zera lub wieloetapowe projekty dokumentacyjne. [page:1] Sprawdza się również przy pracach wymagających modyfikacji wielu plików i etapów, gdzie człowiek nie chce ręcznie koordynować każdego kroku. [page:1]

### Kiedy nie używać `/goal` bez meta-prompta

Nie należy uruchamiać `/goal` bez wcześniejszego meta-prompta, bo wówczas agent działa jak zwykły chatbot i nie wykorzystuje pełni swoich możliwości. [page:1] Każde dłuższe zadanie powinno być poprzedzone generowaniem szczegółowego, przewodniego prompta. [page:1]

### Kiedy używać Kanban

Kanban jest przeznaczony do codziennych zadań, które agent może wykonać autonomicznie, takich jak research, organizacja informacji czy przygotowanie draftów. [page:1] Zadania, które wymagają osobistej obecności lub uprawnień człowieka (np. płatności bankowe), nie powinny trafiać do Kanbana. [page:1]

### Kiedy przekazywać pracę dalej (handoff)

Po wygenerowaniu kodu lub materiału przez `/goal` warto przekazać go do wyspecjalizowanego narzędzia, np. Claude Code lub Codex, na etapie dopracowania i testowania. [page:1] Hermes pełni wówczas rolę generatora pierwszej wersji, a narzędzie specjalistyczne odpowiada za polishing i debugowanie. [page:1]

### Jak utrzymywać system

System utrzymuje się poprzez regularne odpowiadanie na Morning Priority Prompt oraz przegląd Memory Wiki w celu weryfikacji jakości pamięci. [page:1] Nowe typy zadań najlepiej najpierw testować w zwykłej rozmowie, a dopiero potem przenosić do `/goal`. [page:1]

### Jak rozwijać system w czasie

Rozwój polega na dodawaniu kolejnych instancji Hermes dla nowych kategorii pracy, zamienianiu powtarzalnych zadań w cron joby oraz poszerzaniu sieci Tailscale o nowe urządzenia. [page:1] Każde nowe zastosowanie powinno być wdrażane stopniowo, aby nie przeciążyć systemu i użytkownika. [page:1]

## Best Practices

1. **Meta-promptowanie przed każdym `/goal`** – przed długim zadaniem zawsze generuj szczegółowy prompt z pomocą AI, zamiast pisać go ręcznie. [page:1]  
2. **Równoległość instancji** – prowadź kilka instancji Hermes jednocześnie, każdą z innym zadaniem lub projektem. [page:1]  
3. **Separacja pracy ludzkiej i agentowej** – codziennie rano rozdzielaj zadania na te, które wykona agent, i te, które wymagają bezpośredniego udziału człowieka. [page:1]  
4. **Memory Wiki jako wzmocnienie pamięci** – traktuj Memory Wiki jako integralną część systemu, do której zagląda zarówno człowiek, jak i agent. [page:1]  
5. **Handoff jako architektura** – przyjmij, że generowanie i refinement to dwa różne etapy, często realizowane przez różne narzędzia. [page:1]  
6. **Dopytywanie przed startem `/goal` jako sygnał jakości** – jeśli agent zadaje pytania przed uruchomieniem długiego zadania, to symptom dobrze ustawionego systemu. [page:1]  
7. **Raport markdown jako interfejs między agentami** – wyniki researchu i analiz zapisuj jako pliki markdown i używaj ich jako wejścia do innych agentów. [page:1]  
8. **Codzienność buduje kontekst** – im częściej korzystasz z Morning Prompt, tym lepszy i bardziej spersonalizowany staje się agent. [page:1]  

## Security / ryzyka / ograniczenia

### Podejście do uprawnień

Hermes pyta o pozwolenie przy działaniach ingerujących w system, np. przy przeszukiwaniu bibliotek lokalnych czy instalacji komponentów. [page:1] Użytkownik powinien świadomie udzielać zgód, pamiętając, że agent ma dostęp do systemu operacyjnego, plików i przeglądarki. [page:1]

### Tailscale i sieć

Tailscale tworzy prywatną sieć między urządzeniami użytkownika, co jest bezpieczniejsze niż publiczny dostęp, ale niesie ryzyko, że przejęcie kontroli nad agentem daje potencjalny dostęp do całej sieci. [page:1] Zaleca się stosowanie silnego uwierzytelniania oraz ograniczanie uprawnień agenta tylko do niezbędnych zasobów. [page:1]

### Modele LLM jako czynnik krytyczny

Z doświadczeń użytkowników wynika, że lokalne modele oraz auto-routing potrafią zawodzić w połączeniu z Hermesem. [page:1] Dopiero wymuszenie użycia mocnego modelu, takiego jak Claude Sonnet, zapewniło stabilne działanie i poprawne wywoływanie narzędzi. [page:1]

### Ograniczenia systemu

Hermes nie jest w stanie wykonać wszystkich zadań ludzkich, zwłaszcza tych wymagających fizycznej obecności lub specyficznych uprawnień, jak operacje bankowe. [page:1] Wyniki `/goal` mogą wymagać dopracowania i nie powinny być traktowane jako finalny produkt bez walidacji. [page:1] Jakość Memory Wiki zależy od regularności zasilania jej treścią i poprawnych meta-promptów. [page:1]

## Skalowanie / delegowanie / modularność

### Kiedy tworzyć osobne instancje agenta

Warto tworzyć osobne instancje, gdy pojawiają się kategorycznie różne typy pracy, np. research, development, komunikacja, oraz gdy pojedyncze zadania są długotrwałe i nie chcemy, by blokowały inne. [page:1] Autor działa z co najmniej pięcioma równoległymi instancjami jako standardem. [page:1]

### Kiedy zostać przy jednej instancji

Na początku wdrożenia zaleca się pracę z jedną instancją, aby opanować podstawowe use case’y, takie jak `/goal` i Kanban. [page:1] Przy prostych, jednorazowych zadaniach niewymagających specjalizacji nie ma potrzeby mnożenia instancji. [page:1]

### Model wzrostu złożoności

Najpierw wdraża się jednego agenta i podstawowe funkcje `/goal` oraz Kanban, następnie dodaje Memory Wiki, później Morning Prompt, a dopiero potem Tailscale i dodatkowe instancje oraz tryb research. [page:1] Każdy kolejny poziom zwiększa zasięg i autonomię systemu, ale wymaga poprzednich warstw jako fundamentu. [page:1]

### Zasada delegowania

Człowiek odpowiada za kierunek, priorytety i decyzje wymagające ludzkiego kontekstu, natomiast agent zajmuje się wykonaniem, researchem, generowaniem oraz raportowaniem. [page:1] Delegowanie powinno być świadome i oparte na jasnym podziale ról między człowiekiem a agentem. [page:1]

## Antywzorce i błędy

Najczęstszym antywzorcem jest używanie `/goal` bez meta-prompta, co powoduje, że agent działa jak zwykły chatbot i nie wykorzystuje pełni możliwości. [page:1] Innym błędem jest wrzucanie do Kanbana zadań wymagających człowieka, np. płatności czy decyzji o wysokim ryzyku. [page:1]

Nie należy oczekiwać perfekcyjnych wyników z pierwszego `/goal`, ponieważ wygenerowane projekty, np. gry, mają charakter „szkicu” wymagającego dopracowania. [page:1] Ignorowanie Morning Prompt prowadzi do słabszego kontekstu i mniejszej personalizacji. [page:1] Stosowanie słabych modeli LLM lub auto-routingu bez testów może powodować niestabilne działanie całego systemu. [page:1]

## Reguły do przeniesienia do mojego systemu

REGUŁA 1: PRZED KAŻDYM DŁUGIM ZADANIEM — META-PROMPT  
Zanim uruchomisz agenta w trybie autonomicznym (/goal lub odpowiednik), najpierw poproś AI o wygenerowanie szczegółowego, opinionated prompta dla tego zadania. Wklejaj ten prompt, nie swój oryginalny. [page:1]

REGUŁA 2: KANBAN = CODZIENNY INTERFEJS DELEGACJI  
Każdego ranka lista zadań → segregacja: co dla agenta (Kanban/Triage), co dla mnie. Nie wracaj do zadań agentowych — wróć i odbierz wyniki. [page:1]

REGUŁA 3: PAMIĘĆ ZEWNĘTRZNA JEST CZĘŚCIĄ SYSTEMU, NIE DODATKIEM  
Memory Wiki (lub odpowiednik) to nie gadżet. To warstwa pamięci agenta. Agent powinien sam zaglądać do logów przed każdą sesją kontekstową. [page:1]

REGUŁA 4: RÓWNOLEGŁOŚĆ INSTANCJI = PRAWDZIWA PRODUKTYWNOŚĆ  
Jeden agent na jedno zadanie. Pięć agentów na pięć kategorii pracy. Nie blokuj agenta czekając na wynik — uruchamiaj kolejne. [page:1]

REGUŁA 5: HANDOFF JEST ARCHITEKTURĄ  
Generowanie (Hermes/agent ogólny) → Refinement (Claude Code / wyspecjalizowane narzędzie). Nie oczekuj perfekcji z jednego etapu. [page:1]

REGUŁA 6: PĘTLA SAMOROZWOJU = CODZIENNY KONTEKST  
Codzienne pytanie agenta o priorytet dnia + aktualizacja pamięci = rosnąca personalizacja. Im więcej danych wejściowych, tym lepsze rekomendacje i propozycje zadań. [page:1]

REGUŁA 7: PRYWATNA SIEĆ URZĄDZEŃ = ROZSZERZENIE ZASIĘGU AGENTA  
Narzędzie typu Tailscale pozwala agentowi działać na wszystkich urządzeniach. Włącz je gdy potrzebujesz cross-device workflow — nie wcześniej. [page:1]

REGUŁA 8: RESEARCH AGENTA = WEJŚCIE DO INNEGO AGENTA  
Raport z analizy konkurencji (markdown) → wklejony do agenta budującego produkt. Wyniki researchu to dane wejściowe, nie dokumentacja końcowa. [page:1]

REGUŁA 9: MODEL MA ZNACZENIE  
Słaby model = niestabilny agent. Wymagaj Claude Sonnet lub równoważnego. Nie używaj auto-routingu bez testów — wymuś mocny model świadomie. [page:1]

REGUŁA 10: ZŁOŻONOŚĆ WDRAŻAJ STOPNIOWO  
Krok 1: /goal + Kanban.  
Krok 2: Memory Wiki.  
Krok 3: Morning Prompt.  
Krok 4: Tailscale.  
Krok 5: Nowe instancje.  
Nigdy wszystkiego naraz. [page:1]

## Blueprint wdrożeniowy

### Od czego zacząć

Na początek zainstaluj i skonfiguruj Hermes Agent według podstawowej instrukcji, a następnie uruchom pierwszą sesję z `/goal` dla prostego, konkretnego zadania z użyciem meta-prompta. [page:1] Dzięki temu przetestujesz cały pipeline bez nadmiernej złożoności. [page:1]

### Co skonfigurować najpierw

W pierwszej kolejności skonfiguruj Kanban jako główny interfejs delegowania zadań oraz zbuduj Memory Wiki, korzystając z gotowego prompta. [page:1] Te dwa elementy zapewnią ci zarówno operacyjne zarządzanie zadaniami, jak i podstawową pamięć długoterminową. [page:1]

### Co przenieść do pamięci / knowledge base

Do swojej bazy wiedzy przenieś wszystkie dziesięć reguł operacyjnych, gotowe prompty do `/goal`, Memory Wiki i Morning Priority Prompt oraz wzorzec handoff między Hermesem a narzędziami typu Claude Code. [page:1] Staną się one fundamentem twojego własnego systemu agentowego. [page:1]

### Co zamienić w playbooki / SOP-y

Zamień w formalne SOP-y między innymi: rutynę poranną z użyciem Kanbana, procedurę tworzenia nowych zadań `/goal`, scenariusz researchu konkurencyjnego oraz proces onboardingu nowych urządzeń do Tailscale. [page:1] Dzięki temu każdy z tych procesów będzie powtarzalny i łatwy do delegowania. [page:1]

### Co automatyzować później

Na późniejszym etapie możesz automatyzować raporty cykliczne (np. cotygodniowe) jako cron joby, automatyczne zasilanie Memory Wiki z zewnętrznych źródeł oraz pipeline research → analiza → brief → wykonanie przez innego agenta. [page:1] Te automatyzacje warto wdrażać dopiero po ustabilizowaniu podstawowych use case’ów. [page:1]

### Jak nie przesadzić ze złożonością

Aby nie przesadzić ze złożonością, wprowadzaj maksymalnie jeden nowy use case tygodniowo i upewnij się, że podstawowe komponenty działają stabilnie. [page:1] Jeśli coś nie działa po dwóch próbach, najpierw sprawdź używany model LLM, zamiast bez końca poprawiać prompt. [page:1] Prosty system z dobrym modelem jest bardziej wartościowy niż skomplikowany system na słabym modelu. [page:1]