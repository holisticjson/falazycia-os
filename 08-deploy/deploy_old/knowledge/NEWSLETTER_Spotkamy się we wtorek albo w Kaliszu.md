Oto notatka przygotowana na podstawie otrzymanego newslettera, zawierająca wyłącznie konkretne treści techniczne i merytoryczne:

***

# ŹRÓDŁO: Newsletter - Spotkamy się we wtorek? (albo w Kaliszu?)

## Narzędzia i Techniki
*   **Google Gemini (generowanie plików):** Model umożliwia teraz bezpośrednie generowanie i pobieranie plików (Doc, PDF, Excel, CSV, Markdown). 
    *   *Pro tip:* W prompcie należy definiować strukturę, np. "Excel z 3 arkuszami: dane / podsumowanie / wykres" lub "Markdown z Table of Contents (TOC)".
*   **Claude Code (workflow: Build + Review):** Zastosowanie dwóch instancji Claude Code w osobnych terminalach zwiększa jakość kodu.
    *   Terminal A: Generuje draft/plan (zapis do pliku).
    *   Terminal B: Pełni rolę recenzenta, analizuje plik pod kątem błędów logicznych i brakujących perspektyw.
    *   *Zaleta:* Eliminuje problem niezdolności LLM do krytyki własnego outputu.
*   **Claude Code (Update):** Anthropic podwoił limity (rate limits) dla użytkowników planów Pro/Max dzięki zwiększeniu mocy obliczeniowej (GPU).

## Trendy i Rynek
*   **Chrome / Gemini Nano:** Przeglądarka Chrome pobiera lokalnie model Gemini Nano (~4GB, ścieżka: `OptGuideOnDeviceModel/weights.bin`). Działa to domyślnie w tle.
    *   *Uwaga:* Możliwość wyłączenia tej funkcji znajduje się w `chrome://flags`. Model jest dostępny dla programistów przez API `window.ai`.
*   **Koszty agentów AI (Stanford Research):** Agenty autonomiczne zużywają do 1000× więcej tokenów niż standardowe czaty. Koszty wykonania tego samego zadania mogą różnić się nawet 30-krotnie, co stanowi wyzwanie przy przewidywalności budżetu.
*   **AI Act:** Kluczowe regulacje wchodzą w życie 2 sierpnia 2026 r. Przy ubieganiu się o dofinansowania (np. PARP), konieczne jest uwzględnienie dokumentacji dotyczącej zgodności z AI Act już na etapie wniosku.
*   **Rynek modeli:** DeepSeek V4 oraz Qwen 3.6 zdobyły łącznie ok. 15% udziału w rynku, co wskazuje na silną pozycję modeli open-source wobec rozwiązań komercyjnych.

## Automatyzacja (Case studies – kontekst operacyjny)
*   **B2B Sales:** Automatyczne tworzenie profilu klienta na bazie transkryptu spotkania.
*   **Transport:** Wykorzystanie OCR do automatyzacji kalkulacji kosztów w rozliczeniach per kierowca.
*   **Produkcja/Dokumentacja:** Przetwarzanie masowe plików (np. 3000 plików PDF kierowanych do kolejki produkcyjnej).
*   **Księgowość:** Automatyzacja obiegu faktur (pobieranie z maila -> automatyczne księgowanie).