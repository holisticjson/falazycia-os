# HERMES MULTI-AGENT WORKFLOW
## Pełna dokumentacja implementacyjna dla agentów Anti-Gravity & Hermes
> Źródło: Film "I Built the Ultimate Multi-Agent Workflow w/ Hermes Agent Kanban Board" — Tonbi's AI Garage
> Repozytorium: https://github.com/tonbistudio/hermes-multi-agent-workflow
> Data analizy: 12 czerwca 2026

---

## 1. IDEA SYSTEMU — CZYM JEST TEN WORKFLOW

Hermes Multi-Agent Workflow to szkielet (skeleton) autonomicznego pipeline'u opartego na flocie agentów Hermes, który wykonuje następujące kroki:
sources → intake → dedup → score → research (parallel) → route
│
┌────────────────────┬──────────┴──────────┐
path A path B shelve
(prep) (prep) (auto)
└──────────┬────────────┘
── HUMAN GATE ──
approve · shelve · modify
┌──────────┴───────────┐
fulfill fulfill
└──────────┬───────────┘
deliver

text

**Kluczowa zasada:** Kształt pipeline'u jest stały. Tym, co przez niego przepływa, jest Twoja domena.
Wszystko co domenowo-specyficzne żyje w jednym pliku: `triage.yaml`.

---

## 2. PROBLEM, KTÓRY ROZWIĄZUJE — DLACZEGO KANBAN

### Problem bez Kanban Board:
- Agenci "ścigają się" i wykonują duplikaty tej samej pracy
- Marnotrawstwo tokenów i pieniędzy
- Brak wspólnej pamięci o postępie
- Jeden crash traci wszystko
- Brak koordynacji między agentami

### Rozwiązanie z Kanban Board:
- Każda jednostka pracy = karta (card)
- Agent "przejmuje" kartę (claim), pracuje na niej, przekazuje dalej
- Stan pozostaje na planszy — przeżywa restart
- Tablica = jedyne źródło prawdy (single source of truth)
- Brak czatowania między agentami — tylko tablica jako bus komunikacyjny
- Jeden plik SQLite = cała warstwa koordynacji + log audytu

---

## 3. ARCHITEKTURA AGENTÓW — KTO ROBI CO

### Pełna flota agentów (wszystkie to profile w Hermes Agent na jednej maszynie):

| Agent | Model | Zadanie |
|-------|-------|---------|
| **X Scout** | `gemini-2.5-flash` | Research na platformie X (Twitter) — szuka skarg/pain pointów (Vertex AI) |
| **Web Research Scout** | `gemini-2.5-flash` | Research na Reddit, YouTube, Web (Vertex AI) |
| **Orchestrator** | `anthropic.claude-sonnet-4`| Centralny pipeline — sędzia i sterownik; dedup, scoring, routing (AWS Bedrock) |
| **Researcher (x3)** | `gemini-2.5-flash` | Weryfikacja źródeł, kontekst, istniejące rozwiązania (równolegle) |
| **Analyst** | `gemini-2.5-pro` | Synteza informacji i szczegółowe opracowanie pomysłu BUILD |
| **Builder** | `anthropic.claude-sonnet-4`| Buduje prototyp narzędzia/skryptu |
| **Tester** | `anthropic.claude-sonnet-4`| Testuje zbudowane narzędzie |
| **Video Producer** | `gemini-2.5-pro` | Research i szkic outlineu dla wideo |

> **Uwaga:** Każdy agent to osobny profil w Hermes. Możesz użyć dowolnego modelu per profil. Dla modeli z rodziny Gemini profil powinien używać providera `openai` skierowanego na lokalny port Proxy LiteLLM (`http://127.0.0.1:4000`), a dla Claude — providera `bedrock` (`eu-central-1`).

---

## 4. PEŁNY PIPELINE — KROK PO KROKU

### FAZA 1: SCOUTS — Zbieranie danych (co 1-2h lub cron)

**Dwa skauty działają równolegle:**

**Scout X (Twitter/X):**
- Trigger: cron job lub ręczne uruchomienie z CLI
- Komenda CLI:
  ```bash
  hermes run x-research --skill pain_point_scout --prompt "run one X pain point sweep now following the pain point scout X skill exactly"
  ```
- Skanuje X w poszukiwaniu skarg/problemów użytkowników AI agentów
- Tworzy raport w formacie Markdown
- Po zakończeniu tworzy kartę INTAKE na Kanban Board

**Scout Web:**
- Skanuje: Reddit, YouTube, Web
- Tworzy raport z kandydatami (np. 6 kandydatów)
- Podobny format raportu Markdown

**Wynik:** Karty pojawiają się na tablicy Kanban w kolumnie READY/TODO

---

### FAZA 2: ORCHESTRATOR INTAKE — Przyjęcie raportu

- Orchestrator pobiera raport ze skautów
- Karta przechodzi: TODO → IN PROGRESS → DONE
- Raporty zapisywane jako pliki `.md` (dostępne do ręcznego przeglądu)
- Raporty ze skauta X bez kandydatów → karta od razu do DONE
- Raporty z kandydatami → przechodzą do kolejnej fazy

---

### FAZA 3: DEDUP + SCORING — Ocena przez Orchestratora

**Orchestrator wykonuje:**

1. **Deduplication:** Sprawdza, czy problem był już widziany wcześniej (similarity check)
2. **Scoring wg Rubric:**

| Kryterium | Opis |
|-----------|------|
| Frequency | Jak często ten problem jest zgłaszany? |
| Pain Intensity | Jak poważny jest problem? |
| Solvable/Explainable | Czy da się to naprawić lub wyjaśnić? |
| Solution Gap | Czy brakuje dobrego rozwiązania? |
| Strategic Fit | Pasuje do kanału/dev pracy autora? |

3. **Threshold:** Wynik < 65/100 → automatycznie SHELVED (odrzucony)
4. Kandydaci z wynikiem ≥ 65 → przechodzą do RESEARCH

---

### FAZA 4: RESEARCH — Badanie równoległe (3 agenty na problem)

Dla każdego zakwalifikowanego problemu Orchestrator uruchamia **3 Research Agenty równolegle:**

| Researcher | Zadanie |
|-----------|---------|
| Source Verifier | Weryfikacja źródeł i rzetelności zgłoszenia |
| Context Researcher | Badanie kontekstu problemu |
| Solution Researcher | Istniejące rozwiązania (lub ich brak) |

**Mechanizm fan-out/fan-in:**
- Karta ROUTE czeka na wszystkich 3 rodziców (parent tasks)
- Gdy ostatni Researcher kończy → karta ROUTE automatycznie promuje się do READY
- Brak pollingu, brak glue code — działa samo

**Przykład przy 6 kandydatach:**
- 6 problemów × 3 Researcherów = **18 agentów pracujących jednocześnie**

---

### FAZA 5: ORCHESTRATOR ROUTING — Decyzja o ścieżce

Po zebraniu raportów Researcher agentów, Orchestrator decyduje:
Wynik ≥ 65 + badanie zakończone
│
├── BUILD PATH → Analyst → Builder → Tester → Deliver (script/skill)
├── VIDEO PATH → Video Producer → Outline + Script → Deliver (slides + notes)
└── SHELVE → Karta zamknięta, idzie do DONE

text

**BUILD PATH przykład:**
- Problem: "Codex VS Code extension ignores config tunnel changes"
- Analyst tworzy szczegółowy plan
- Builder buduje skrypt Python (<500 linii)
- Tester testuje

**VIDEO PATH przykład:**
- Problem: "Claude Code sub-agents fail when many MCP tools are configured"
- Video Producer robi research istniejących rozwiązań
- Tworzy outline wideo + notatki dla prezentera

---

### FAZA 6: HUMAN GATE — Jedyna interwencja człowieka

**Delivery przez Telegram:**
4 proposals are awaiting your approval:

[Proposal 1] BUILD: Local Codex VS Code safety config verifier CLI
Pain point: Safety mismatch between config settings and IDE extension behavior
Sources: [GitHub links]
Why build: Frequent issue, existing solutions broken, bounded scope (<500 lines)
Proposed solution: Python script inspecting config locations (Linux/WSL/Windows)
Score: 78/100

→ Reply: approve | shelve [reason] | modify [new plan]

text

**Komendy odpowiedzi przez Telegram:**
- `approve` — zatwierdź i uruchom pipeline dalej
- `shelve` — odrzuć (opcjonalnie dodaj powód)
- `modify [nowy plan]` — zmień plan i zatwierdź

> **WAŻNE:** Telegram rezerwuje `/commands` — NIE używaj `/approve`, tylko `approve` (bez slash!)

---

### FAZA 7: FULFILL — Realizacja po zatwierdzeniu

**BUILD chain:**
[approve] → Builder Agent → prototype build
→ Tester Agent → run tests
→ Final Report → Deliver to Telegram

text

**VIDEO chain:**
[approve] → Video Producer → research pass
→ Build slides (Markdown/PPTX)
→ Write speaker script
→ Deliver to Telegram

text

**Deliverables:**
- BUILD: Python script + README + test report
- VIDEO: Slide deck + script + speaker notes + fact sheet + markdown handoff

---

### FAZA 8: SELF-HEALING — Automatyczne odtwarzanie

System posiada wbudowany mechanizm self-healing:
- Dead task → automatycznie reclaimed i respawned
- Błąd workspce (scratch dir wyczyszczony) → agent wykrywa brak plików i regeneruje do persistent directory
- Każdy claim, komentarz i zakończenie jest logowane (audit trail)

---

## 5. KANBAN BOARD — MECHANIKA TABLICY

### Kolumny tablicy:
| Kolumna | Znaczenie |
|---------|-----------|
| **TODO** | Zadanie czeka na zakończenie parent tasków |
| **READY** | Zadanie gotowe do podjęcia przez agenta |
| **IN PROGRESS** | Agent przejął zadanie (claimed) |
| **BLOCKED** | Czeka na input ludzki lub inne warunki |
| **DONE** | Zakończone |

### Struktura karty (uproszczona):
Title: [co trzeba zrobić]
Assignee: [nazwa profilu agenta — routing]
Status: [todo/ready/in_progress/blocked/done]
Parents: [ID kart-rodziców — fan-in]

text

### Dispatcher Loop:
Board ma READY task

Dispatcher claims it (atomic — dwa agenty nigdy nie wezmą tego samego)

Dispatcher spawns assigned agent w czystym workspace

Agent wykonuje pracę

Agent oznacza kartę jako DONE

Loop — każdy tick

text

### Dlaczego ten system wygrywa:
- **Durable:** Przeżywa restarty i crashe
- **Parallel:** Wiele agentów naraz, koordynowanych jedną tablicą
- **Event-driven:** Praca przepływa sama przez graph
- **Self-healing:** Martwe zadanie = reclaim + respawn
- **Auditable:** Wszystko zalogowane

---

## 6. STRUKTURA REPOZYTORIUM
hermes-multi-agent-workflow/
│
├── triage.yaml ← GŁÓWNY CONFIG — cały pipeline tutaj
├── AGENTS.md ← Instrukcja dla AI agent adapting template
├── proposal_actions.py ← Handler human gate (approve/shelve/modify)
├── requirements.txt ← Tylko PyYAML
├── .env.example ← Template konfiguracji env
│
├── engine/ ← Generyczny silnik (rzadko edytuj)
│ ├── config.py ← Ładowanie/walidacja triage.yaml
│ ├── engine.py ← TriageEngine — cała deterministyczna logika
│ ├── scoring.py ← Scoring rubric (LLM mode + deterministic)
│ ├── routing.py ← Klasyfikacja → ścieżka
│ ├── dedup.py ← Similarity (token-cosine; embedding-ready)
│ ├── item_vault.py ← Jeden plik .md na tracked item
│ ├── kanban_store.py ← Zapis na Hermes Kanban Board
│ ├── intake_parser.py ← Parsowanie raportów skautów
│ └── frontmatter.py ← YAML frontmatter dla item files
│
├── paths/ ← Templates per ścieżka (EDYTUJ SWOBODNIE)
│ ├── rails/ ← Scope rails — granica bezpieczeństwa
│ ├── specs/ ← Formaty deliverables
│ └── proposals/ ← Formaty wiadomości gate
│
├── skills/templates/ ← SKILL.md dla skautów i orchestratora
│
├── cli/
│ └── triage.py ← validate / scaffold / init / install
│
├── scripts/
│ └── cost_report.py ← Per-item spend dla cost gate
│
├── tests/ ← 12 generycznych testów silnika
│
├── docs/
│ ├── 01-architecture.md ← Architektura fat engine / thin skill
│ ├── 02-the-board.md ← Kanban jako bus; dispatcher; fan-in
│ ├── 03-config-reference.md ← Każdy klucz triage.yaml
│ ├── 04-adapting-to-your-domain.md ← Przewodnik adaptacji krok po kroku
│ ├── 05-pipeline-stages.md ← Każdy etap + gotchas
│ ├── 06-security.md ← Trust surface, scope rails
│ └── 07-runbook.md ← Profile, board, crons, go-live
│
└── examples/
└── ai-agent-pain-points/
└── REFERENCE.md ← Pełny write-up referencyjnej implementacji

## 7. QUICKSTART — INSTALACJA I URUCHOMIENIE

### Wymagania wstępne:
- Hermes Agent zainstalowany i działający: `hermes --version`
- Python z PyYAML: `pip install -r requirements.txt`
- Konto Telegram + Bot Token (do human gate)
- Klucz do web search (Tavily / Serper / Brave) dla skautów

### Kroki instalacji:

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/tonbistudio/hermes-multi-agent-workflow
cd hermes-multi-agent-workflow

# 2. Zainstaluj zależności (tylko PyYAML)
pip install -r requirements.txt

# 3. Waliduj konfigurację przykładową
python -m cli.triage validate

# 4. Uruchom testy jednostkowe (12 testów, wszystkie generyczne)
python -m unittest discover -s tests

# 5. Wydrukuj plan setup dla Hermes (profile, board, crons)
python -m cli.triage scaffold
```

---

## 8. GO-LIVE RUNBOOK — KROK PO KROKU

### Krok 1: Utwórz tablicę Kanban
```bash
hermes kanban boards create <board_name>
# nazwa board pochodzi z triage.yaml → pole "board:"
```

### Krok 2: Utwórz profile agentów
```bash
# Jeden profil na każdą odrębną wartość w "roles:" + każdy "sources[].profile"
hermes profile create <name> --from <base_profile>

# Następnie edytuj model dla każdego profilu:
# ~/.hermes/profiles/<name>/config.yaml
# Dla modeli Vertex (Gemini 2.5 Flash/Pro):
#   provider: openai
#   model: hermes-fast (lub nazwa z litellm_config.yaml)
#   providers:
#     openai:
#       api_key: sk-hermes-local
#       base_url: http://127.0.0.1:4000
#
# Dla modeli AWS (Claude Sonnet 4):
#   provider: bedrock
#   model: anthropic.claude-sonnet-4
#   aws_region: eu-central-1
```

> **Tip:** Multi-model jest wymogiem — skaut używa superszybkiego `gemini-2.5-flash` przez Vertex, a Builder i Orchestrator korzystają z precyzyjnego `claude-sonnet-4` przez AWS Bedrock.

### Krok 3: Dodaj toolset `kanban` do profili skautów
```yaml
# ~/.hermes/profiles/<scout_profile>/config.yaml
toolsets: [hermes-cli, kanban]
```

> ⚠️ **GOTCHA #1 (krytyczne):** Skauty działają przez cron (nie dispatcher), więc kanban tools nie są auto-enabled. Bez tego skaut napisze raport ale CICHO nie utworzy karty intake. Nic nie będzie działać.

Dodatkowo — dodaj backend web search do skautu (klucz Tavily/Serper/Brave w `.env` lub wbudowany toolset `web`).

### Krok 4: Zainstaluj skills
```bash
# Skopiuj skill orchestratora do jego profilu:
cp -r skills/templates/triage-orchestrator/ ~/.hermes/profiles/<orchestrator>/skills/

# Skopiuj skill skauta (raz na każde źródło), zmień nazwę na sources[].skill:
cp -r skills/templates/triage-scout/ ~/.hermes/profiles/<scout>/skills/<skill_name>/
# Wklej "query" tego źródła do sekcji "What to look for" w SKILL.md
```

### Krok 5: Autoryzacja (auth)
```bash
# Zaloguj się do providera dla każdego profilu osobno (interaktywnie, ręcznie):
# OAuth token jest per profil — login w jednym profilu nie pokrywa innych!
```

### Krok 6: Skonfiguruj kanał Telegram (human gate)
```bash
# W pliku .env orchestratora ustaw:
TELEGRAM_BOT_TOKEN=<twój_token>
TELEGRAM_ALLOWED_USERS=<twoje_user_id>

# Wyślij botowi wiadomość raz (bot nie może DM do użytkownika, który nie zaczął rozmowy)

# Zweryfikuj dostarczanie:
orchestrator send --to telegram "triage engine: delivery check"
```

### Krok 7: Zarejestruj cron jobs skautów
```bash
# WAŻNE: Rejestruj w profilu GATEWAY (orchestrator), nie w profilu skauta!
# Cron ticker czyta TYLKO store profilu gateway.

orchestrator cron create '<schedule>' <scout_profile> --profile <scout_profile> --skill <skill_name>

# Sprawdź:
orchestrator cron list --all   # oba joby powinny być widoczne

# Na razie wstrzymaj (do czasu go-live):
orchestrator cron pause <job_id>
```

### Krok 8: Uruchom runtime (gateway)
```bash
# Dispatcher + cron żyją wewnątrz gateway
# Na WSL: użyj "gateway run" (foreground), NIE "gateway start" (wymaga systemd)
# Trzymaj w tmux lub screen!

orchestrator gateway run      # foreground — dispatcher obsługuje wszystkie board'y
orchestrator gateway status   # z innego shella → powinno pokazać "running"
```

### Krok 9: Smoke test — ręczne uruchomienie jednego cyklu
```bash
# Uruchom skauta ręcznie (nie czekaj na cron):
hermes chat <scout_profile> --skills <skill_name> -q "Run one sweep now, following the skill exactly."

# Obserwuj karty pojawiające się na tablicy:
hermes kanban --board <board_name> list

# Oczekiwany przepływ:
# intake → (dedup/score) → research lanes (parallel) → route → prep → propose
# → proposal DM na Telegram → odpowiedz "approve <id>" → fulfill chain → deliverable DM

# Potwierdź: pierwsza karta post-gate powinna mieć status "ready" (nie "todo")
```

### Krok 10: Go Live
```bash
# Wznów cron (zacznij od jednego skauta):
orchestrator cron resume <job_id>

# Obserwuj pierwszy pełny cykl, potem wznów resztę
```

---

## 9. ADAPTACJA DO WŁASNEJ DOMENY — 6 KROKÓW

### Krok 0: Odpowiedz na 6 pytań (przed dotknięciem kodu)
1. **Co to jest "item"?** (zgłoszenie buga, lead sprzedażowy, ticket supportu, pomysł na content, odkrycie bezpieczeństwa…)
2. **Skąd pochodzą itemy?** (które platformy mają obserwować skauci?)
3. **Co sprawia, że item jest warty działania?** (rubric)
4. **Jaka jest decyzja routingu?** (po badaniach — co odróżnia ścieżki?)
5. **Co produkuje każda ścieżka?** (deliverable per ścieżkę)
6. **Co człowiek zatwierdza?** (gate)

> Te 6 pytań mapuje się 1:1 na bloki `triage.yaml`: sources, rubric, route, paths, gate.

### Krok 1: Przepisz `triage.yaml` — w tej kolejności:
1. `name`, `board`, `workspace_root`, `cost_gate_usd` — tożsamość podstawowa
2. `sources` — jeden wpis na skauta: `profile`, `skill`, `schedule`, precyzyjny `query`
3. `item_schema.fields` — pola emitowane przez skautów: zachowaj `title`, `claim`, `sources`; dodaj domenowe
4. `rubric` — twoje wymiary, maksima, threshold; `hint`y muszą być konkretne
5. `research_lanes` — równoległe badania przed routingiem; `classifier_lane` emituje sygnał
6. `route.map` — wartość klasyfikacji → nazwa ścieżki
7. `paths` — jedna na każdy outcome: `prep`, `fulfill`, templates, workspace, `scope_rails`, `deliverable_spec`; martwe końce oznacz `auto: true`
8. `roles` — każda rola → konkretna nazwa profilu Hermes
9. `gate` — verby do odpowiedzi (np. `approve`, `shelve`, `modify`)

> Uruchamiaj `python -m cli.triage validate` po każdym bloku!

### Krok 2: Przepisz templates ścieżek (`paths/`)
- `paths/rails/*.md` — twarde limity dla ścieżek "build/do work" — bądź restrykcyjny, to granica bezpieczeństwa
- `paths/specs/*.md` — format output dla ścieżek "produce artifact" (struktura, styl, quality bar)
- `paths/proposals/*.md` — wiadomość gate dla każdej ścieżki — musi być skimowalna

### Krok 3: Wybierz tryb scoringu
- **LLM mode (domyślny):** orchestrator scoruje każdy wymiar rubric; engine waliduje i stosuje threshold. Działa dla dowolnego rubric — bez zmian w kodzie.
- **Deterministic mode (opcjonalny):** `engine/scoring.py::score_candidate_heuristic` — scoring ze strukturyzowanych pól bez modelu. Przydatny do testów.

### Krok 4: Przepisz skills (`skills/templates/`)
- **Scout(s):** kopiuj `triage-scout/SKILL.md` raz na źródło, wklej `query` źródła do "What to look for"; synchronizuj format raportu z `item_schema` i `intake_parser.py`
- **Orchestrator:** `triage-orchestrator/SKILL.md` jest już cienki i config-driven; dostosuj tylko domenowe sformułowania (co dedup-ować, jak formułować propozycje)

### Krok 5: Walidacja i testy
```bash
python -m cli.triage validate   # konfiguracja spójna?
python -m unittest discover -s tests  # engine nadal poprawny?
```

### Krok 6: Stand it up
```bash
python -m cli.triage scaffold   # generuje komendy Hermes: board, profile, skills, crons
# → następnie postępuj wg docs/07-runbook.md
```

---

## 10. HARD-WON GOTCHAS — LISTA BŁĘDÓW, KTÓRYCH NIE POPEŁNIAJ

| # | Symptom | Przyczyna | Rozwiązanie |
|---|---------|-----------|-------------|
| 1 | Scout działa, karta nie pojawia się | Brak `kanban` toolset w profilu skauta | Dodaj `toolsets: [hermes-cli, kanban]` do `~/.hermes/profiles/<scout>/config.yaml` |
| 2 | Crons nigdy nie odpala | Joby nie są w storze profilu gateway | Utwórz je z `--profile` pod orchestratorem |
| 3 | Karta utknęła w `todo` | Ma niedokończonego parenta | Nie paruj pierwszego post-gate tasku do karty triage |
| 4 | Status ustawiony, ale brak DM | Orchestrator nie wykonał `hermes send` | Status ≠ delivery. Musi jawnie wywołać `hermes send --to telegram` |
| 5 | `/approve` → "unknown command" | Telegram rezerwuje `/` | Odpowiadaj bez slash: `approve <id>` (nie `/approve`) |
| 6 | Finalne delivery nie może znaleźć artefaktów | Stage użył scratch workspace (skasowanego) | Używaj persistent `dir` workspace dla wszystkich fulfill stages |
| 7 | `gateway start` fail na WSL | WSL brak systemd | Używaj `gateway run` (foreground) |

---

## 11. ZASADY BEZPIECZEŃSTWA

- Nigdy nie commit-uj: `.env`, `auth.json`, board `*.db`, zawartości `work/` ani `vault/`
- Sprawdź `.gitignore` przed publikacją
- Plik `paths/rails/*.md` = granica bezpieczeństwa — scope rails muszą być ścisłe
- System uruchamia kod napisany przez LLM i shell-out-uje — stąd human gate jest obowiązkowy
- Nie usuwaj human gate i nie ustawiaj auto-approve

---

## 12. WZORZEC MENTALNY — SZABLON ZDANIA

Wypełnij luki i masz swój pipeline:

> "Obserwuj **[platformę X]** w poszukiwaniu **[itemów]**.  
> Zachowaj te, które osiągną ≥ **[threshold]**  
> na **[wymiarach rubric]**.  
> Po zbadaniu **[research lanes]**, jeśli **[classifier lane]** powie  
> **[wartość]**, zrób **[ścieżka]**, co produkuje **[deliverable]**  
> — ale tylko po moim zatwierdzeniu."

Każde **pogrubione miejsce** = wartość w `triage.yaml`. Zero kodu.

---

## 13. KOMENDY OPERACYJNE — DAY-TO-DAY

```bash
# Obserwuj tablicę:
hermes kanban --board <board_name> list

# Zatwierdź propozycję przez Telegram:
approve <id>

# Odrzuć:
shelve <id>: <powód>

# Zmień plan:
modify <id>: <nowy plan>

# Odrzuć wszystkie oczekujące:
reject the rest
# lub:
python proposal_actions.py shelve-all

# Raport kosztów per item:
python scripts/cost_report.py --gate <threshold>

# Zatrzymaj runtime:
Ctrl-C  (gateway run)
```

---

## 14. LINKI I ZASOBY

| Zasób | URL |
|-------|-----|
| Repozytorium GitHub | https://github.com/tonbistudio/hermes-multi-agent-workflow |
| Hermes Agent (NousResearch) | https://github.com/NousResearch/hermes-agent |
| Film źródłowy | https://www.youtube.com/watch?v=EKVRqcpTT6s |
| Architektura | `docs/01-architecture.md` |
| Kanban Board (mechanika) | `docs/02-the-board.md` |
| Config Reference | `docs/03-config-reference.md` |
| Adaptacja domeny | `docs/04-adapting-to-your-domain.md` |
| Pipeline stages + gotchas | `docs/05-pipeline-stages.md` |
| Bezpieczeństwo | `docs/06-security.md` |
| Runbook go-live | `docs/07-runbook.md` |
| Referencyjna implementacja | `examples/ai-agent-pain-points/REFERENCE.md` |

---

## 15. BAZA WIEDZY JASONA (OBSIDIAN ZETTELKASTEN)

### Konfiguracja połączenia
Hermes używa narzędzia (skilla) MCP Obsidian. Aby Agenci (zwłaszcza Analyst i Builder) mieli dostęp do Twojej prywatnej wiedzy, ustaw zmienną środowiskową na serwerze w pliku `~/.hermes/.env`:
`OBSIDIAN_VAULT_PATH="c:/Aplikacje MVP/02_knowledge_base"`

### Jak agenci pracują z Obsidianem
1. **Zettelkasten:** Karta Kanban dla nowej funkcji uruchomi Analysta, który automatycznie przeszuka strukturę tagów i linków wewnątrz Twojego vaulta w poszukiwaniu gotowych wzorców.
2. **Dokumentowanie Postępu:** Po wykonaniu zadania (np. napisaniu specyfikacji z transkrypcji YouTube Hormoziego), Analyst może zapisać wynik bezpośrednio w pliku MD wewnątrz Twojej bazy. 
3. **Pamięć Jasona:** Zestaw zasad i tonu dla Twojego cyfrowego klona będzie na stałe przechowywany w pliku `00_JASON_SOUL.md` i każdorazowo wczytywany przez profil Jasona przed rozmową z klientem lub pisaniem skryptu.
