# Plan Implementacji: Naprawa Chatbota J(AI)SON AI i Integracji RAG (Wersja 2.1)

Wersja: **2.1 (Senior Architect Edition)**  
Status: **Oczekuje na akceptację Tomasza**  
Tryb pracy: **`/goal` (Maksymalna staranność, zero kompromisów)**

Zidentyfikowaliśmy i poddaliśmy krytycznej ocenie usterkę silnika chatbota **J(AI)SON AI** na stronie głównej `jaison.pl`. Poniżej znajduje się szczegółowa analiza techniczna (Reality Check), przyczyna błędu oraz plan chirurgicznej i stabilnej naprawy architektonicznej.

---

## 🕵️ Analiza Techniczna i Główna Przyczyna (Dlaczego chatbot pisał o grow hackingu na słowo "Cześć"?)

Podczas analizy kodu backendowego strony zidentyfikowaliśmy **krytyczny błąd integracji RAG (Retrieval-Augmented Generation)**:

1. **Brak Warstwy Konwersacyjnej (LLM Brain)**: 
   Frontendowy widget czatu w `index.html` wysyła zapytania do skryptu `/php/chat.php`. Skrypt ten pobiera klucz konta usługi (Service Account) i uderza **bezpośrednio do REST API wyszukiwarki Vertex AI Search** (`default_search:search`):
   ```php
   $searchUrl = "https://{$host}/v1/projects/{$project_id}/locations/{$loc}/collections/default_collection/engines/{$engine_id}/servingConfigs/default_search:search";
   ```
2. **Ignorowanie Intencji Użytkownika (Klasyczny Błąd RAG)**:
   Vertex AI Search to silnik wyszukiwania dokumentów (RAG), a nie konwersacyjny model czatu. Gdy użytkownik wpisuje zwykłe powitanie (np. *"Cześć !"*), wyszukiwarka traktuje to jako frazę kluczową. Z powodu braku progu odcięcia (retrieval threshold), silnik dopasowuje najbliższy semantycznie fragment z wgranych materiałów (w tym przypadku nagranie szkoleniowe Tomasza zaczynające się od *"Witajcie serdecznie! Dzisiaj będzie materiał dotyczący problemów z wejściem w grow hacking..."*) i generuje surowe streszczenie tego dokumentu.
3. **Brak Stanu i Historii (Stateless)**:
   Skrypt `chat.php` nie utrzymuje historii rozmowy (history/session), co uniemożliwia realizację zapowiedzianego **Interaktywnego Audytu Systemowego (21 pytań diagnostycznych)**. Każde zapytanie jest traktowane jako zupełnie niezależne wyszukiwanie.
4. **Wyciek Gwiazdek Markdown (Zasada 13)**:
   Silnik Vertex AI Search zwraca surowy Markdown zawierający podwójne gwiazdki (`**`), co narusza nienaruszalną zasadę eliminacji śladów generowania treści przez AI w serwisach agencji.

---

## 💡 Rozwiązanie Architektoniczne (Hybrid Conversational RAG)

Wdrożymy **dwupoziomową architekturę hybrydową (Hybrid Conversational RAG)**, która łączy zalety bezpiecznego, sesyjnego backendu PHP ze stanowym modelem **Gemini 2.5 Flash** (używanym jako główny "Mózg" chatbota):

```mermaid
graph TD
    User["User (index.html)"] -->|AJAX POST| PHP["Proxy Gateway (chat.php)"]
    PHP -->|1. Klasyfikacja Zapytania| Classify{"Czy to powitanie/odpowiedź na audyt?"}
    
    Classify -->|TAK| GeminiOnly["Wywołaj bezpośrednio Gemini 2.5 Flash (bez wyszukiwania)"]
    Classify -->|NIE (Pytanie merytoryczne)| RAG["Odpytaj Vertex AI Search (Retrieval)"]
    
    RAG -->|Zwróć Snippet bazy wiedzy| Context["Wstrzyknij Snippet do System Promptu Gemini"]
    Context --> GeminiRAG["Wywołaj Gemini 2.5 Flash z Groundingiem"]
    
    GeminiOnly -->|Odpowiedź w HTML| Clean["Oczyszczenie z Markdown (Zasada 13)"]
    GeminiRAG -->|Odpowiedź w HTML| Clean
    
    Clean -->|Zapisz w $_SESSION| Session["Zapisz Turn w historii sesji"]
    Session -->|Zwróć czysty HTML| User
```

### Kluczowe Elementy Nowej Architektury:
1. **Lekki Klasyfikator Zapytań (0ms narzutu)**: 
   W `chat.php` wdrożymy filtr słów kluczowych (Greetings & Audit Answers). Jeśli użytkownik wyśle powitanie (np. *"Cześć"*, *"Dzień dobry"*) lub odpowiedź do audytu (np. *"tak"*, *"nie"*, *"audyt"*, *"zacznijmy"*, liczby itp.), **całkowicie pomijamy wyszukiwanie w Vertex AI Search**. Zapytanie trafia od razu do Gemini.
2. **Sesyjna Historia Rozmowy (`$_SESSION`)**:
   Uruchomimy serwerowe sesje PHP w celu bezkonkurencyjnego i bezpiecznego przechowywania historii ostatnich 15 wypowiedzi. Dzięki temu chatbot zyskuje **pamięć podręczną** i może prowadzić użytkownika za rękę krok po kroku przez **Interaktywny Audyt (21 pytań)**, naliczając punkty w locie!
3. **Gemini 2.5 Flash jako Orchestrator**:
   Zamiast zwracać surowy wynik wyszukiwania, uderzymy bezpośrednio do API **Vertex AI Gemini 2.5 Flash** przez REST (używając istniejącego tokenu z Service Account). Gemini otrzyma pełny system prompt, historię konwersacji oraz ewentualny kontekst wyszukiwania, po czym zsyntetyzuje naturalną, ludzką odpowiedź w tonie Ghost v2 / NLP VAK.
4. **Bezwzględne Czyszczenie i Formatowanie HTML**:
   Zaimplementujemy funkcję filtrującą, która całkowicie wyeliminuje gwiazdki markdown, zastępując je tagami `<strong>` i dbając o ADHD-friendly visual anchoring.

---

## 🛠️ Proponowane Zmiany (Proposed Changes)

### Komponent: Backend PHP i Integracja (`website/site/public/php`)

#### [MODIFY] [chat.php](file:///C:/Aplikacje%20MVP/Holistic%20Jason/01-jaison-core/website/site/public/php/chat.php)
- Wdrożenie klasyfikatora zapytań `isCasualOrAudit($message)`.
- Wdrożenie stanowej sesji `$_SESSION['chat_history']` z limitem do 15 ostatnich wypowiedzi.
- Integracja z Vertex AI Gemini 2.5 Flash REST API (`generateContent`) przy użyciu tokenu autoryzacji GCP.
- Wstrzykiwanie wyników wyszukiwania Vertex AI Search jako dynamicznego kontekstu (grounding) do system promptu Gemini tylko przy pytaniach merytorycznych.
- Precyzyjne formatowanie wyjściowe (oczyszczanie z markdownu, konwersja list na tagi HTML).

---

## 🧪 Plan Weryfikacji (Verification Plan)

### Połączenie i Testy Składniowe PHP
1. Zweryfikujemy poprawność składniową PHP za pomocą polecenia lintera:
   ```powershell
   php -l "C:\Aplikacje MVP\Holistic Jason\01-jaison-core\website\site\public\php\chat.php"
   ```

### Testy Funkcjonalne Chatbota (Czarna Skrzynka)
Przetestujemy zachowanie chatbota pod kątem zidentyfikowanych problemów:
1. **Scenariusz Powitania**: Wyślemy zapytanie *"Cześć !"* i upewnimy się, że chatbot odpowiada naturalnym powitaniem J(AI)SON AI i zaprasza do audytu, zamiast wypluwać surowy artykuł o grow hackingu.
2. **Scenariusz Pytania Merytorycznego**: Wyślemy zapytanie *"Jakie macie pakiety?"* lub *"Opowiedz o wdrożeniu Coolfon"* i zweryfikujemy, czy silnik poprawnie odpytuje Vertex AI Search, po czym Gemini generuje zgrabną odpowiedź opartą na tych danych.
3. **Scenariusz Audytu**: Napiszemy *"audyt"* i sprawdzimy, czy bot rozpoczyna zadawanie pytań diagnostycznych jedno po drugim (zachowując stan i zliczając punkty w sesji).
4. **Weryfikacja Formatowania (Zasada 13)**: Upewnimy się, że w odpowiedziach nie ma ani jednej gwiazdki markdown (`**`), a tekst jest sformatowany wyłącznie tagami `<strong>` i `<p>`.
