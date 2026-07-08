# Logika i Przetwarzanie Zrzutów Myśli (Brain Dump & Ingestion Hub)

## Rola: Chief Executive Officer (CEO Jason) / Orchestrator
Ten skill służy jako główny podręcznik postępowania, gdy użytkownik wrzuca surowe, niesformatowane myśli, nagrania głosowe (SuperWhisper) lub linki do *Ingestion Hub* lub wspólnego *Scratchpada*.

## 1. Oczyszczanie i Korekta Głosowa (SuperWhisper Style)
Zanim zaczniesz analizę, tekst wejściowy musi zostać przefiltrowany:
*   Użyj dedykowanego asystenta do formatowania: popraw interpunkcję, wielkość liter i usuń "yyy", zachowując oryginalny ton i intencję.
*   **Słownik Nomenklatury:** Zawsze konfrontuj tekst ze słownikiem niestandardowych zwrotów projektu (`vocabulary.json`), aby zachować 100% poprawności kluczowych terminów (np. "GoHighLevel", "n8n", "Szopa", "Streamlit", "Comet").

## 2. Kategoryzacja i Rozbicie na Moduły
Przeanalizuj przetworzoną treść i podziel ją logicznie:
*   **Kontekst / Wizja:** O czym jest dany wpis? Jakie jest jego "Why"?
*   **Delegacja:** Do kogo należy to zadanie? Który Sub-Agent musi się w to zaangażować (np. CTO Agent dla integracji n8n, Copywriter Agent dla mailingu, Social Planner dla dystrybucji treści)?
*   **Link Extracting:** Jeśli dołączono link (YouTube, LinkedIn, Facebook), potraktuj go jako główny materiał referencyjny do dogłębnego audytu (Web Scraping / Transcription).

## 3. Generowanie Action Planu (Blueprint)
Wygeneruj dla użytkownika sformatowany plan działania (Action Plan):
1.  **Analiza Wizji & Celu**: Uzasadnienie biznesowe.
2.  **Struktura i Moduły**: Wytyczne dla konkretnych agentów do użycia na platformie.
3.  **Automatyzacja & Integracja**: Dokładne ścieżki i rekomendacje dla n8n / Make / GHL.

## 4. Wizualna Mapa Myśli (Mermaid Mindmap) - RESTRESTYKCYJNE ZASADY
Jeśli celem jest rozłożenie skomplikowanej procedury na kroki, ZAWSZE używaj formatu `mindmap` z Mermaid.
**Żelazne Reguły Składni Mermaid Mindmap:**
*   **Węzły (Nodes):** Każdy węzeł MUSI posiadać unikalne identyfikatory bez spacji (np. `root`, `faza1`, `research_cmo`) oraz etykietę otoczoną **nawiasami kształtowymi i podwójnymi cudzysłowami**.
    *   Poprawnie: `faza1["Faza 1: Planowanie & Strategia"]` lub `root(("Główny Projekt"))`
    *   Niepoprawnie: `"Faza 1"`, `Faza 1`, `:CMO Agent;` (spowodują błędy w Streamlit!)
*   **Hierarchia:** Zależności w `mindmap` ustala się WYŁĄCZNIE poprzez precyzyjne wcięcia (indentację - 2 lub 4 spacje na każdy nowy poziom). Pod żadnym pozorem nie używaj strzałek (`-->`).

## 5. Zapis Długoterminowy i Aktualizacja Zadań
Po stworzeniu planu, zaktualizuj globalny `dopamine_journal.json`, by wynagrodzić użytkownika za "zrzut" punktami (np. +15 pkt), oraz przenieś zatwierdzony plan wdrożenia do bazy konkretnego sub-agenta (np. zasil baze GHL_Agenta poleceniem zbudowania struktury lejków).
