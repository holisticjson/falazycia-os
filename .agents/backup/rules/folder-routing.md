# Standard Routingu Katalogów (Folder Routing Standard)

Wszystkie agenty AI i skrypty automatyzujące pracujące w tym obszarze roboczym MUSZĄ bezwzględnie przestrzegać poniższego schematu 10 głównych katalogów (Root Folders). Zakazuje się tworzenia nowych, niestandardowych folderów bezpośrednio w katalogu głównym projektu.

## Schemat Root-Katalogów

```text
Holistic Jason/
├── 00-inbox/                    # Nowe, nieposortowane pliki, pobrane zasoby do przetworzenia
├── 01-jaison-core/              # Wszystko dotyczące marki Jaison (www, oferty, copywriting, social, lejek, ghostwriter)
├── 02-os-jaison/                # Kod źródłowy (Streamlit, panel, integracje, bazy sqlite, moduły LLM, testy)
├── 03-social-media-factory/     # Pipeline wideo, skrypty, grafiki, b-roll, integracje z Pexels, lektorzy
├── 04-clients/                  # Klienci zewnętrzni (np. coolfon, kurczakujasia, smartrade, viptransporter)
├── 05-templates/                # Szablony audytów, brandbooków, prezentacji, ofert handlowych
├── 06-knowledge/                # Baza wiedzy (Obsidian Vault, research, dokumenty RAG pod Vertex AI Search)
├── 07-ops/                      # Operacje wewnętrzne (zadania CRM, backlogi, checklisty, raporty finansowe CFO)
├── 08-deploy/                   # Skrypty i instrukcje wdrożeniowe, konfiguracje env, klucze API, certyfikaty SSL
└── 09-archive/                  # Archiwalne projekty, stare wersje, ukończone eksperymenty, logi asynchroniczne
```

## Zasady Tworzenia Plików (Strict Placement Rules)
1. **Brak luźnych plików w Root:** Wszystkie nowe skrypty python muszą trafiać do `02-os-jaison/` lub `08-deploy/` (jeśli dotyczą czysto deploymentu). W katalogu głównym mogą znajdować się wyłącznie pliki: `.env`, `.gitignore`, `requirements.txt`, `Dockerfile`, `WORKSPACE_MEMORY.md` oraz katalog konfiguracyjny agentów `.agents/`.
2. **Kwalifikacja Treści:** Każda generowana treść (e-book, pdf, post) musi zostać automatycznie zakwalifikowana do odpowiedniego folderu (np. lead magnet Jaison do `01-jaison-core/`, lead magnet klienta do `04-clients/<klient>/03-social/`).
3. **Pliki Cyfrowe:** Zgodnie z zasadą dystrybucji, gotowe e-booki, poradniki i lead magnety przeznaczone do sprzedaży/dystrybucji muszą być również zapisywane w dedykowanym folderze systemowym: `C:\Aplikacje MVP\Holistic Jason\11_digital_product\`.
