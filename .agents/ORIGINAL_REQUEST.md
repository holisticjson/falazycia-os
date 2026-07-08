# Original User Request

## Initial Request — 2026-06-19T14:48:32Z

Przeprowadzenie kompleksowego testu, audytu i autonomicznego debugowania aplikacji Streamlit (Holistic JSON AI Agency Dashboard). Celem jest weryfikacja i naprawa integracji z Hermes Agentic OS, zapewnienie przesyłania lejków do Systeme.io oraz poprawne działanie bazy wiedzy (RAG) z uwzględnieniem rozróżnienia na wiedzę statyczną i notatki typu "Brain Dump". Agenci mają uprawnienia do uruchamiania środowiska testowego i samodzielnego aplikowania poprawek w kodzie.

Working directory: c:\Aplikacje MVP\Holistic Jason\
Integrity mode: development

## Requirements

### R1. Weryfikacja i Autonomiczna Naprawa Streamlit (UI/Moduły)
Uruchomienie aplikacji w środowisku testowym. Agenci must zidentyfikować błędy ukryte w prototypowych modułach z paska bocznego (sidebar) i samodzielnie zaaplikować poprawki (bug fixing) w kodzie, aby zapewnić stabilne działanie jak na profesjonalną agencję przystało (brak błędów typu 502, 404, czy traceback w UI).

### R2. Integracja Hermes OS i Systeme.io (CI/CD i Lejki)
Walidacja pełnego cyklu życia leadów i operacji marketingowych. Usunięcie jakichkolwiek aktywnych powiązań operacyjnych z GoHighLevel i wdrożenie lub naprawienie komunikacji kierującej leady/dane do Systeme.io (np. za pomocą webhooków). Weryfikacja ciągłości przesyłu poleceń do Hermesa.

### R3. Dualny System Bazy Wiedzy ("Czacha" RAG vs Brain Dump)
Dopracowanie logiki zapytań dla głównego asystenta. Architektura musi rozróżniać, kiedy zapytanie powinno czerpać z twardej, zweryfikowanej bazy wiedzy (GCS), a kiedy z luźnych inspiracji, pomysłów i zrzutów myśli zapisywanych w sekcji "Brain Dump".

### R4. Kontrolowane środowisko wykonywania testów
Zabrania się uruchamiania produkcyjnych kampanii lub wysyłania publicznych maili z testowych środowisk. Agenci muszą przeprowadzać operacje na lokalnych mockach lub na własnym testowym hoście (np. localhost:8501).

## Acceptance Criteria

### Weryfikacja Działania Modułów
- [ ] Aplikacja Streamlit uruchamia się lokalnie bez rzucania wyjątków (traceback) na ekranie startowym.
- [ ] Każdy z głównych prototypowych modułów w panelu bocznym może zostać "kliknięty" (lub symulowany skryptem) bez krytycznego błędu.

### Integracje i Lejki
- [ ] Istnieje skrypt testowy (`verify_integrations.py` lub w ramach frameworka testowego), który weryfikuje poprawne formowanie requestu webhooka do Systeme.io.
- [ ] System logów poświadcza poprawną wymianę komunikatów z Hermes Agentic OS na dedykowanym lokalnym porcie/API.

### Baza Wiedzy (RAG)
- [ ] Zbudowano zautomatyzowany test (np. `pytest`), podający do "Czachy" dwa różne zapytania: jedno czysto faktograficzne (wymagające odwołania do GCS) i jedno kreatywne/inspiracyjne.
- [ ] Test jednoznacznie loguje prawidłowe przekierowanie zapytań do odpowiednich wektorów (Brain Dump vs standardowe dokumenty).

---
*Next: when approved → delegate via invoke_subagent (see Delegation Protocol)*

## 2026-06-24T07:00:28Z

Implementacja i integracja infrastruktury promptów oraz checklist od Mirka Burnejko (Akademia.pl) w dashboardzie Streamlit, unifikacja i synchronizacja SOP-ów/skilli dla Hermesa i lokalnego AntiGravity, wdrożenie testów E2E, utworzenie dedykowanego promptu automatyzacji dla asystenta przeglądarkowego COMED oraz zdefiniowanie alternatywnej architektury niskokosztowej (zamiast JAMStack i AWS Bedrock).

Working directory: c:\Aplikacje MVP\Holistic Jason
Integrity mode: development

## Requirements

### R1. Audyt, Testy E2E i Stabilizacja Aplikacji Streamlit (app.py)
1. **Uruchomienie Testów:** Przetestować aplikację locally i na serwerze GCP za pomocą `pytest`. Zweryfikować, czy wszystkie moduły i webhooki działają poprawnie (w tym integracja Systeme.io API v2).
2. **Obsługa Błędów:** Dodać przejrzyste komunikaty ostrzegawcze (Złota Zasada 6) w przypadku braku kluczy API, zamiast rzucania wyjątkami w Pythonie.

### R2. Integracja Narzędzi i Checklist Akademia.pl w Streamlit
1. **Baza Wiedzy:** Zaimportować prompty i checklisty z plików w `scratch/` (np. AI Skill Mentor, Ghost AI, Deep Research, Strategia Marketingu oraz checklisty sprzedażowe/lejków).
2. **Nowy Moduł UI:** Stworzyć nową zakładkę w Streamlit `🎯 Akademia.pl Mentoring`.
3. **Interaktywne Wywoływanie:** Umożliwić użytkownikowi wybór promptu/checklisty, dostosowanie pól wejściowych (np. profil firmy) i uruchomienie generowania przez skonfigurowane Gemini API / LiteLLM z bezpośrednim podglądem i kopiowaniem do schowka.

### R3. Unifikacja i Synchronizacja SOP-ów oraz Skilli
1. **Wspólny Folder:** Przenieść i skonsolidować wszystkie skille dyrektorskie (CEO, CMO, CTO, CCO, CFO, COO, CSO, Ghost, Holistic) z lokalnego katalogu wtyczek globalnych (`C:\Users\tomas_yq1b9su\.gemini\config\plugins\holistic-virtual-board\skills\`) oraz `.agents/skills/` do jednego folderu `skills/` w głównym katalogu roboczym (`c:\Aplikacje MVP\Holistic Jason\skills\`).
2. **Automatyczna Synchronizacja:** Zmodyfikować `sync_to_gcp.py` tak, aby przesyłał te skille na serwer VM i automatycznie kopiował/linkował je do folderu konfiguracyjnego Hermesa (`/home/holisticjson/.hermes/skills/` i `/home/holisticjson/.hermes/profiles/`), zapewniając tożsamość konfiguracji lokalnej i serwerowej.

### R4. Prompt dla Asystenta COMED (Automatyzacja Hostingu)
1. **Dedykowany Plik:** Plik `tasks/comed_browser_prompt.md` został utworzony. Zawiera optymalny prompt automatyzujący tworzenie e-maili i WordPress Application Passwords na Hostido.
2. **Integracja z UI:** Dodać link/przycisk do pobrania/skopiowania tego promptu w Streamlit Dashboardzie (np. w nowej podsekcji dotyczącej WordPressa lub hostingu).

### R5. Architektura Alternatywna (Low-Cost / Low-Friction)
1. **Analiza i Zamiennik:** Plik `docs/alternative_architecture.md` został utworzony. Wyjaśnia rezygnację z JAMStack i AWS Bedrock na rzecz natywnego hostingu Hostido FTP, WordPress REST API i Google Vertex AI (Gemini).

## Acceptance Criteria

### Integracja Akademia.pl
- [ ] W Streamlicie dostępna jest nowa zakładka `🎯 Akademia.pl Mentoring` z interaktywnymi promptami i checklistami od Mirka Burnejko.
- [ ] Wybrany prompt można wywołać bezpośrednio przez Gemini API/LiteLLM i pobrać wynik jako Markdown.

### Unifikacja Skilli
- [ ] Wszystkie skille dyrektorskie zostały skopiowane do folderu `skills/` w głównym katalogu roboczym.
- [ ] Zmodyfikowany plik `sync_to_gcp.py` poprawnie wdraża te skille i linkuje/kopiuje je do katalogu `/home/holisticjson/.hermes/skills/` na maszynie VM.

### Narzędzia Automatyzacji i Dokumentacja
- [ ] Plik `tasks/comed_browser_prompt.md` jest podlinkowany i dostępny do podejrzenia/skopiowania w Streamlit UI.
- [ ] Dokument `docs/alternative_architecture.md` jest wdrożony i opisany w stylu Ghost v2 (struktura pod ADHD).
- [ ] Wszystkie testy jednostkowe i integracyjne (uruchomione przez `pytest`) zwracają status PASS.

## Follow-up — 2026-06-24T07:04:38Z

Ważna wskazówka do realizacji integracji z Akademia.pl:
Ścieżka do surowych plików i checklist od Mirka Burnejko to:
`C:\Aplikacje MVP\02_knowledge_base\raw\Mirek_Burnejko_AI_Biznes_Lab\`
a nie wewnątrz folderu roboczego `c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw\Mirek_Burnejko_AI_Biznes_Lab\`. 

Użyj tej poprawnej ścieżki absolutnej do zaimportowania i wczytywania promptów w module Streamlit.

