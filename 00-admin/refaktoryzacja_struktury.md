
# Plan Refaktoryzacji Struktury Projektu Holistic Jason

**Data:** 18.05.2026

**Autor:** Architect (Holistic Jason AI)

## 1. Diagnoza Obecnej Struktury

Obecna struktura projektu jest chaotyczna i wysoce nieefektywna. Kluczowe problemy to:

*   **Brak jasnego podziału:** Kod źródłowy, skrypty, dane, dokumentacja, pliki konfiguracyjne i zasoby multimedialne są wymieszane w głównym katalogu.
*   **Nadmiarowość i duplikacja:** Wiele plików jest zduplikowanych (np. z dopiskiem `(1)`, `_copy` lub w różnych formatach jak `.docx` i `.md`).
*   **Niespójne nazewnictwo:** Zarówno pliki, jak i foldery używają różnych konwencji nazewniczych.
*   **Brak centralnego punktu zarządzania:** Ważne skrypty i konfiguracje są rozproszone, co utrudnia zarządzanie i automatyzację.
*   **Mieszanie wiedzy surowej z przetworzoną:** Katalog `Baza_Wiedzy` zawiera zarówno oryginalne materiały, jak i ich syntetyczne podsumowania, co prowadzi do zamieszania.

## 2. Proponowana Nowa Struktura

Nowa architektura ma na celu wprowadzenie modularności, separacji odpowiedzialności (Separation of Concerns) i ułatwienie przyszłego rozwoju oraz automatyzacji.

```
/
├── 00_admin/                 # (BEZ ZMIAN) Zarządzanie projektem, raporty, dokumentacja
├── 01_src/                     # GŁÓWNY KOD ŹRÓDŁOWY APLIKACJI
│   ├── agents/                 # Definicje i logika agentów AI (np. ghl_agent, holistic_ceo)
│   ├── skills/                 # Przeniesiony i oczyszczony katalog z umiejętnościami agentów
│   ├── tools/                  # Skrypty narzędziowe i pomocnicze
│   ├── app/                    # Główny plik aplikacji (np. interfejs Streamlit, FastAPI)
│   └── config/                 # Konfiguracje, klucze API (w .env), ustawienia
├── 02_knowledge_base/          # NOWA BAZA WIEDZY
│   ├── raw/                    # Surowe, nieprzetworzone materiały (PDF, DOCX, linki)
│   ├── processed/              # Wiedza po przetworzeniu (pliki .MD), gotowa do użycia przez AI
│   └── synthesized/            # Wiedza skondensowana, raporty, kluczowe insighty
├── 03_content/                 # (BEZ ZMIAN) Materiały do generowania treści (social media, blog)
├── 04_website/                 # Zintegrowane zasoby dla strony www.holisticjson.pl
│   ├── copy/                   # Wszystkie teksty na stronę (z `07-website`)
│   ├── assets/                 # Grafiki, ikony, multimedia
│   └── site/                   # Kod źródłowy strony (np. Vite/Astro/Next.js)
├── 05_clients/                 # (BEZ ZMIAN) Dane i projekty dla konkretnych klientów
├── 06_exports/                 # (BEZ ZMIAN) Wygenerowane pliki i raporty
├── 07_archive/                 # Archiwum przestarzałych plików, skryptów i danych
└── 99_workspace/               # Pliki tymczasowe, notatki, eksperymenty (`scratch`, `temp_subs`)

```

## 3. Plan Migracji (Krok po Kroku)

1.  **Utworzenie Nowej Struktury:**
    *   Stworzenie głównych katalogów: `01_src`, `02_knowledge_base`, `04_website`, `07_archive`, `99_workspace`.
    *   Stworzenie podkatalogów wewnątrz nowych folderów.

2.  **Migracja Skryptów i Kodu (`01_src`):**
    *   Przeniesienie wszystkich plików `.py` z głównego katalogu do `01_src/tools/` (jako punkt wyjścia).
    *   Przeniesienie zawartości `skills/` do `01_src/skills/`.
    *   Identyfikacja głównych skryptów (np. `holistic_ceo.py`, `ghl_agent.py`) i przeniesienie ich do `01_src/agents/`.
    *   Przeniesienie plików konfiguracyjnych (np. `.json`, `.toml`) do `01_src/config/`, z wyjątkiem `.env`.

3.  **Reorganizacja Bazy Wiedzy (`02_knowledge_base`):**
    *   Przeniesienie całej zawartości `Baza_Wiedzy/` do `02_knowledge_base/raw/`.
    *   Identyfikacja i przeniesienie plików z `Baza_Wiedzy/Syntetyczna/` do `02_knowledge_base/synthesized/`.
    *   Uruchomienie skryptu `usun_duplikaty.py` na `raw/` w celu usunięcia oczywistych duplikatów.
    *   Uruchomienie skryptów konwertujących (np. `convert_baza_wiedzy.py`) w celu przetworzenia plików z `raw/` do formatu `.md` w `processed/`.

4.  **Konsolidacja Zasobów Strony (`04_website`):**
    *   Przeniesienie wszystkich plików z `07-website/` do `04_website/copy/`.
    *   Przeniesienie `www_holisticjson_pl/site-new/` do `04_website/site/`.
    *   Przeniesienie obrazów (`.png`, `.jpg`) i grafik związanych ze stroną do `04_website/assets/`.

5.  **Archiwizacja (`07_archive`):**
    *   Przeniesienie wszystkich przestarzałych, tymczasowych lub zduplikowanych plików (np. `*.log`, `_copy.*`, `(1).*`, `report.xml`, `view.xml`) z głównego katalogu do `07_archive/`.

6.  **Oczyszczenie Głównego Katalogu:**
    *   Usunięcie pustych już folderów (stare `skills`, `07-website`, `www_holisticjson_pl`).
    *   Weryfikacja, czy w głównym katalogu pozostały tylko niezbędne pliki (np. `Dockerfile`, `requirements.txt`, `.env`) i nowe foldery.

## 4. Oczekiwane Korzyści

*   **Zwiększona czytelność i łatwość nawigacji.**
*   **Uproszczenie procesów CI/CD i automatyzacji.**
*   **Łatwiejsze zarządzanie zależnościami i konfiguracją.**
*   **Separacja danych od logiki, co ułatwia trenowanie i ewaluację modeli AI.**
*   **Skalowalność i gotowość na przyszły rozwój projektu.**
