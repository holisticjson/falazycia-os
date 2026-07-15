# 🧠 HERMES AGENT OS — BAZA WIEDZY OPERACYJNEJ
### Holistic AIDHD × Hermes × ADHD4Life Community

*Skompilowane z 11 blueprintów tutorialowych (Alex Finn, Julian Goldie, Nate Herk, ZSecurity, Higgsfield i inne)*  
*Wersja: v1.0 — 28 maja 2026*

---

## 📌 SEKCJA 1: CZYM JEST HERMES AGENT OS

### Definicja
Hermes Agent to **open-source'owy agent AI** (projekt Nous Research, licencja MIT) działający na własnej infrastrukturze (VPS, Mac mini, laptop, Docker, Android/Termux). To NIE jest chatbot — to **osobisty system operacyjny dla agentów AI** z:
- trwałą pamięcią (pliki `.md` na dysku)
- proceduralnymi playbokami (skills)
- zdefiniowaną osobowością (soul)
- autonomicznymi harmonogramami (cron jobs)
- pętlą samodoskonalenia (self-improving loop)

### Kluczowa różnica wobec zwykłego LLM
| Zwykły LLM / Chatbot | Hermes Agent OS |
|---|---|
| Zapomina po sesji | Pamięta między sesjami |
| Reaguje tylko na pytania | Działa proaktywnie (cron, /goal) |
| Jeden model | Wiele profili i modeli |
| Brak struktury zadań | Kanban + Orchestrator |
| Musisz pisać od zera | Skille = reużywalne procedury |
| Brak harmonogramu | Cron jobs w języku naturalnym |

### Kiedy używać Hermesa, a kiedy Claude Code / Codex
| Używaj Hermesa gdy... | Używaj Claude Code / Codex gdy... |
|---|---|
| Zadania operacyjne i organizacyjne | Ciężkie sesje programistyczne |
| Research, dokumenty, pliki | Duże aplikacje z testami e2e |
| Praca mobilna, przez Telegram | Kompleksowe debugowanie kodu |
| Zadania powtarzalne (cron, skill) | Debugowanie samego Hermesa |
| Praca „on the go" | Refaktoryzacje całych projektów |
| Proaktywne automatyzacje | |

---

## 📌 SEKCJA 2: PIĘĆ FILARÓW (Nate Herk)

### Filar 1: MEMORY — Trwała Pamięć
Hermes budzi się **bezstanowy (stateless)** — bez plików pamięci nie pamięta nic między sesjami.

| Plik | Zawartość | Czego unikać |
|---|---|---|
| `user.md` | Tożsamość, styl pracy, preferencje, czego nie lubi | Sekrety, chwilowe taski |
| `memory.md` | Projekty, środowiska, relacje, kontekst biznesowy | Chwilowe statusy, szczegóły |
| `soul.md` | Osobowość, ton, styl odpowiedzi, vibe | Instrukcje proceduralne |
| `skill.md` | Kroki wykonania, kryteria, wzorzec działania | Tożsamość użytkownika |
| `agents.md` / `claude.md` | Lokalny kontekst projektu, scope, struktura | Globalna pamięć użytkownika |

**Zasada:** Gdy agent zachowuje się dziwnie → najpierw sprawdź `memory.md`. To najczęstsza przyczyna anomalii.

### Filar 2: SKILLS — Proceduralna Pamięć
Skills = powtarzalne playbooki opisujące jak wykonać zadanie dobrze i spójnie.

**Zasady tworzenia skills:**
- Skill = opis powtarzalnego sposobu wykonania zadania (nie jednorazowa odpowiedź)
- Skill musi mieć jasny **trigger w YAML front matter** (agent wie kiedy go wywołać)
- **Zasada "drugi raz = skill"**: jeśli dajesz tę samą instrukcję drugi raz → zrób z niej skill
- Jeśli agent nie uruchamia skilla → popraw YAML front matter i warunki wywołania
- Hermes może sam budować i patchować skills na podstawie realnej pracy

### Filar 3: SOUL — Osobowość Agenta
`soul.md` kształtuje ton, sposób odpowiadania i ogólny "vibe" agenta.

**Ważne:** Jeśli agent odpowiada źle (zbyt długo, nie w tonie) → problem często leży w soul, nie w logice zadania.

### Filar 4: CRONS — Automatyzacje Harmonogramowe
Crony zamieniają Hermesa z systemu **reaktywnego** w **proaktywny**.

**Zasady cronów:**
- Najpierw ustal co ma robić regularnie → dopiero wtedy poproś o cron
- Dla zadań istotnych: najpierw zbuduj **skill**, potem przypnij do niego cron
- Crony uruchamiają **świeżą, izolowaną sesję** → prompt musi być samowystarczalny
- Crony NIE mogą rekurencyjnie tworzyć kolejnych cronów
- Przy strefach czasowych → stosuj logikę self-check (daylight saving może psuć harmonogram)

### Filar 5: SELF-IMPROVING LOOP — Pętla Samodoskonalenia
Hermes poprawia się gdy:
1. Użyteczne doświadczenia zostają utrwalone w memory, skills i searchable history
2. Użytkownik aktywnie koryguje zachowanie i prosi o zapis do odpowiednich plików
3. Feedback loop jest świadomy — nie automatyczny

**Zasada:** Gdy agent pomyli się drugi raz w tej samej rzeczy → popraw natychmiast i zaktualizuj skill lub memory.

---

## 📌 SEKCJA 3: ARCHITEKTURA SYSTEMU

### Warstwy Hermes Agent OS
```
┌─────────────────────────────────────────────────────┐
│                  KANAŁY STEROWANIA                  │
│    Telegram (C2/mobilny) ↔ Discord (per-agent)     │
│              Dashboard / CLI (admin)                │
├─────────────────────────────────────────────────────┤
│              MISSION CONTROL DASHBOARD               │
│   Sesje │ Kanban │ Crony │ Skills │ Activity Feed   │
├─────────────────────────────────────────────────────┤
│                WARSTWA AGENTOWA                     │
│  Orchestrator → Scout → Scribe → Reach → Dev       │
│         (lub: jeden główny Hermes na start)         │
├─────────────────────────────────────────────────────┤
│              SHARED MEMORY LAYER                    │
│  user.md │ memory.md │ soul.md │ kanban.json        │
│  Obsidian Vault / SQLite / GitHub (backup)          │
├─────────────────────────────────────────────────────┤
│              WARSTWA INFRASTRUKTURY                 │
│    VPS (Ubuntu 24.04) │ Docker │ Tailscale          │
│    OpenRouter / model API │ GitHub (source of truth) │
└─────────────────────────────────────────────────────┘
```

### Model Wieloagentowy C-Suite (Julian Goldie)
Gdy system dojrzeje → wyspecjalizowane role:

| Agent | Rola | Pamięć |
|---|---|---|
| **Orchestrator** | Koordynator, dispatcher | Reguły operacyjne, routing, team awareness |
| **Scout** | Deep research | Źródła, dane, tematy |
| **Scribe** | Content writer | Drafty, style guide, wcześniejsze teksty |
| **Reach** | Marketing & social | Strategie promocji, tone of voice |
| **Dev** | Developer | Kod, decyzje techniczne |

**Zasada C-Suite:** Każdy agent zna pozostałych (shared team awareness), ale nie czyta ich pamięci i nie wykonuje ich pracy. Cross-contamination = niedopuszczalne.

**Full Content Pipeline:** `Scout (research)` → `Scribe (writing)` → `Reach (marketing)` — uruchamiane jedną komendą: *"Run full pipeline on [topic]"*

---

## 📌 SEKCJA 4: MODELE LLM — REKOMENDACJE I KOSZTY

### Ranking modeli dla Hermesa (od najlepszego do najtańszego)

| Model | Provider | Koszt | Kiedy używać |
|---|---|---|---|
| **Claude Sonnet 4.6 / 4.x** | Anthropic / OpenRouter | $$$ | Produkcja, złożone zadania, stabilne narzędzia |
| **Claude Haiku 3.5** | Anthropic / OpenRouter | $$ | Szybkie operacyjne taski, mobilny C2 |
| **GPT-4o / GPT-5.5** | OpenAI / ChatGPT Paid | $$$ | Wersja z autoryzacją przez link URL (bez API key) |
| **Nous Hermes** / **Nous models** | OpenRouter | $ | Specjalizacja: instruction following, otwarte |
| **GLM5 Turbo (Z.AI)** | OpenRouter | $ | Mniej cenzurowany, red-team, autoryzowane testy |
| **Owl Alpha** | OpenRouter | **FREE** | 1M tokenów kontekstu, darmowy — na start |
| **Qwen 2.5 / 3** | OpenRouter | $ | Dobry do coding, długi kontekst |
| **Gemma 3 / Llama 4** | Lokalne / OpenRouter | Free/$ | Offline, bez kosztów API |

### ⚠️ WAŻNE zasady doboru modelu
- **Słaby model = niestabilny agent.** Lokalne modele i auto-routing często zawodzą w połączeniu z Hermesem
- Dopiero wymuszenie mocnego modelu (Claude Sonnet) zapewniło stabilne wywoływanie narzędzi
- Nie używaj auto-routingu bez testów — **wymuś konkretny model świadomie**
- Na **start i testy** → Owl Alpha przez OpenRouter (darmowy, 1M tokenów)
- Na **produkcję** → Claude Sonnet (Anthropic) przez OpenRouter lub bezpośrednio
- **Rekomendacja Nate Herk:** Claude Code jako główne narzędzie do głębokiej pracy; Hermes + Claude Haiku do mobilnych i operacyjnych zadań

### Konfiguracja modelu w Hermesie
```yaml
# ~/.hermes/config.yaml
model:
  default: anthropic/claude-sonnet-4.6   # produkcja
  # alternatywa tania: openai/o4-mini
  # alternatywa darmowa: nous/hermes-3-llama-3.1-8b (sprawdź dostępność)
  provider: openrouter
  api_mode: chat_completions
```

---

## 📌 SEKCJA 5: INFRASTRUKTURA — VPS I DOCKER

### Rekomendacje VPS (od najtańszego)

| Provider | Plan | Cena | Specs | Uwagi |
|---|---|---|---|---|
| **Racknet** | Roczny | ~$60/rok ($5/mies.) | 3 CPU, 60 GB SSD, 4 GB RAM | Tani, credentials mailem |
| **Contabo** | Miesięczny | $7/mies. ($5.6 roczny) | 2 CPU, 8 GB RAM, 200 GB SSD | Backup za $2/mies. |
| **Contabo** | Opcja NVMe | $7-10/mies. | SSD szybszy odczyt | Lepsza wydajność |
| **Hostinger KVM2** | Zmienny | $8-15/mies. | 2 CPU, 8 GB RAM | Hermes preinstalowany |
| **Google Cloud VPS** | Pay-as-you-go | Zmienne | Dowolne | Drogie przy stałym użyciu |

**System operacyjny:** Ubuntu 24.04 LTS — jedyna oficjalnie rekomendowana wersja.

### Docker vs. Root VPS
| Docker | Root VPS |
|---|---|
| Izolacja agentów (oddzielny .env per agent) | Prostszy setup na start |
| Łatwiejsze zarządzanie wieloma instancjami | Bezpośredni dostęp do zasobów |
| Lepsze śledzenie kosztów per agent | Trudniejszy restart po awarii |
| Rekomendowane przez Nate przy multi-agent | OK dla jednej instancji |

**Zasada:** Nate Herk rekomenduje Docker dla multi-agent. Na start (jeden Hermes) → root VPS wystarczy.

---

## 📌 SEKCJA 6: BEZPIECZEŃSTWO — KOMPLETNY ZESTAW REGUŁ

### 🔴 ZASADA 1: Sekrety poza rozmową
Klucze API i tokeny NIE powinny trafiać do okna konwersacji. Bezpieczniejszy wzorzec:
```bash
# W terminalu bezpośrednio na VPS:
echo 'OPENROUTER_API_KEY=sk-or-...' >> /opt/data/.env
# NIE przez chat Hermesa!
```

### 🔴 ZASADA 2: Oddzielne konta i oddzielne klucze
- Każdy agent → własne konto API, własny klucz
- Marketing agent ≠ Finance agent (inne uprawnienia, inne koszty)
- Ułatwia śledzenie kosztów i audit

### 🔴 ZASADA 3: Least Privilege
Każdy agent dostaje WYŁĄCZNIE to, co jest niezbędne do jego roli:
- credentials, scope i narzędzia tylko dla zadań agenta
- Dev nie ma dostępu do pamięci CMO
- Brak segmentacji = chaos + ryzyko

### 🔴 ZASADA 4: Hardening VPS
- Firewall → ograniczaj porty (SSH: 22, Streamlit: 8501, Dashboard: 9119)
- Zawężaj dostęp do konkretnych IP
- Telegram bot → ograniczenie do JEDNEGO user ID (Krytyczne!)

```bash
# Sprawdź user ID Telegram przez: @userinfobot
# Wklej ID do konfiguracji Hermesa — nikt inny nie ma dostępu
```

### 🔴 ZASADA 5: Dashboard TYLKO przez SSH Tunnel
NIE wystawiaj dashboardu bezpośrednio do internetu:
```bash
# Bezpieczny dostęp do dashboardu przez tunnel:
ssh -L 9119:DOCKER_IP:9119 user@VPS_IP
# Otwórz: http://localhost:9119
```

### 🔴 ZASADA 6: Security as Routine (Nate Herk)
Bezpieczeństwo = cykl operacyjny, nie jednorazowe wydarzenie:
- Nocny cron: audyt bezpieczeństwa logów i uprawnień
- Tygodniowy cron: sprawdzenie aktywnych kluczy API i scope'ów

### 🔴 ZASADA 7: GitHub jako Source of Truth
- Prywatne repo: backup state projektu i plików kontekstowych
- `.gitignore`: wyklucz sekrety, `.env`, credentials!
- NIE pushuj kluczy API, tokenów, haseł

### 🔴 ZASADA 8: Izolacja środowiska
- Hermes na VPS, NIE na osobistym komputerze (dla zaawansowanych use cases)
- Tailscale → prywatna sieć (silne uwierzytelnianie!)
- Przejęcie agenta + Tailscale = dostęp do całej sieci urządzeń

### 🟡 Ograniczenia odpowiedzialności
- Hermes działa na zasadzie: operator odpowiada za to co uruchamia
- Agent wykonuje to, do czego jest skierowany → świadome promptowanie to security
- Wszystkie testy na obcych systemach są nielegalne bez zgody

---

## 📌 SEKCJA 7: ZASADY OPERACYJNE — 25 KLUCZOWYCH REGUŁ

### Reguły Architektoniczne
1. **Jeden agent na start** → wyciśnij maksimum z jednego, zanim rozdzielisz role
2. **Memory first** → agent bez pamięci to chatbot; pamięć to fundament, nie dodatek
3. **Shared memory layer** → wszyscy agenci pracują na tych samych plikach danych
4. **Osobna pamięć per agent** → Dev nie czyta pamięci Scribe'a (brak cross-contamination)
5. **Złożoność warstwowo** → nie buduj wszystkiego naraz, dokładaj warstwy po stabilizacji

### Reguły Pracy Codziennej
6. **Poranny triage Kanban** → każdy ranek: co dla agenta (Triage), co dla mnie
7. **Deleguj i odejdź** → wrzuć do Kanbana, wróć i odbierz wyniki; nie pilnuj
8. **Wszystko powtarzalne = skill** → jeśli robisz coś drugi raz → zrób skill
9. **Wszystko cykliczne = cron** → jeśli masz to pamiętać co tydzień → zrób cron
10. **Agent wie kim jesteś** → trzy bloki kontekstu: kim jesteś, nad czym pracujesz, dokąd zmierzasz

### Reguły Jakości
11. **Meta-prompt przed /goal** → przed długim zadaniem poproś AI o wygenerowanie idealnego prompta
12. **Model ma znaczenie** → słaby model = niestabilny agent; wymuś mocny model świadomie
13. **Handoff jako architektura** → Hermes generuje → Claude Code/Codex dopracowuje
14. **Judge loop = QA** → Goal Mode z modelem-sędzią to wbudowany quality assurance
15. **Raport Markdown = interfejs między agentami** → wyniki researchu to dane wejściowe, nie finalne

### Reguły Bezpieczeństwa
16. **Sekrety poza czatem** → `.env`, nie okno konwersacji
17. **Bot Telegram = jeden user ID** → krytyczny punkt bezpieczeństwa
18. **Least privilege per agent** → każdy agent dostaje tylko potrzebne uprawnienia
19. **Dashboard przez SSH tunnel** → nigdy bezpośrednio do internetu
20. **GitHub z .gitignore** → backup tak, sekrety nie

### Reguły Skalowania
21. **Nowe instancje gdy** → inne uprawnienia, inna pamięć, inni odbiorcy, inny harmonogram
22. **Unikaj mega-agenta** → jeden agent ze wszystkimi API, skill, cronami = chaos i ryzyko
23. **Jedna automatyzacja tygodniowo** → kontrolowany rytm (Julian Goldie)
24. **Max jeden nowy use case tygodniowo** → nie przeciążaj systemu i siebie
25. **Uprość gdy chaos** → wróć do jednego agenta, odbuduj warstwowo

---

## 📌 SEKCJA 8: WORKFLOW WDROŻENIOWY — SEKWENCJA STARTOWA

### Faza 0: Fundament (Dzień 1-3)
```bash
# 1. Postaw VPS (Ubuntu 24.04)
# 2. Zainstaluj Hermesa
curl -fsSL https://hermes-agent.nousresearch.com/install | bash

# 3. Quick Setup
hermes setup
# → wybierz OpenRouter jako provider
# → wklej API key
# → wybierz model (start: Owl Alpha - darmowy; produkcja: claude-sonnet-4.6)

# 4. Skonfiguruj Telegram
# → BotFather → /newbot → skopiuj token
# → @userinfobot → pobierz swój user ID → ogranicz bota

# 5. Uruchom jako usługa
hermes gateway start --background
```

### Faza 1: Pamięć i Kontekst (Dzień 3-7)
1. Wgraj pliki pamięci do `~/.hermes/`:
   - `user.md` — kim jesteś, styl pracy, preferencje
   - `memory.md` — projekty, środowiska, cele
   - `soul.md` — osobowość agenta
2. Przetestuj przez Telegram: *"Przeczytaj swoje pliki user.md i memory.md. Powiedz mi, co wiesz o mnie i moich projektach."*
3. Połącz z GitHub: pierwsze prywatne repo + nightly sync cron

### Faza 2: Pierwsze Skills i Crony (Tydzień 2)
W Hermesie przez Telegram lub CLI:
```
Stwórz skill o nazwie "nightly-github-sync" który każdej nocy o 2:00 
robi git pull i git push plików z ~/Agentic_OS/ do prywatnego repo.
Użyj tokenu z .env (GITHUB_TOKEN).
```
```
Stwórz cron "morning-priority-prompt" który każdego dnia o 9:00 
pyta mnie o priorytet dnia i generuje listę zadań dla agenta.
```

### Faza 3: Kanban i Dashboard (Tydzień 2-3)
```bash
hermes dashboard        # uruchom dashboard
# Otwórz: http://localhost:PORT
```
- Ustaw flow Kanbana: Triage → To-Do → Ready → In Progress → Blocked → Done
- Każdy ranek: wrzuć zadania do Triage
- Agent rozbija na podzadania i podejmuje

### Faza 4: Mission Control (Miesiąc 2+)
- Zleć Hermesowi budowę niestandardowego dashboardu (Streamlit lub inny)
- Dodaj kolejnych agentów (Scout, Scribe, Reach) gdy jeden Hermes nie wystarczy
- Full content pipeline uruchamiany jedną komendą

---

## 📌 SEKCJA 9: ANTYWZORCE — CZEGO NIE ROBIĆ

| Antywzorzec | Problem | Rozwiązanie |
|---|---|---|
| Używanie terminala jako głównego interfejsu | Brak historii, outputy znikają | Dashboard + Workspace |
| Każda sesja startuje od zera | Strata czasu, agent nie zna kontekstu | ICE / user.md + memory.md |
| /goal bez meta-promptu | Agent działa jak chatbot, nie autonomicznie | Najpierw wygeneruj idealny prompt |
| Wklejanie kodu przez SSH browser | Buffer się przepełnia, pliki uszkodzone | GitHub + git pull na serwerze |
| Jeden długi prompt jako zadanie | Agent traci focus, niska jakość | Kanban + subtasks |
| Słaby model lub auto-routing | Niestabilne wywołania narzędzi | Wymuś Claude Sonnet |
| Mega-agent z wszystkimi kluczami | Chaos, ryzyko, trudne debugowanie | Separacja per agent |
| Bot Telegram bez user ID | Ktoś przejął bota | user ID = obowiązkowy filtr |
| Sekrety w historii czatu | Wyciek danych | .env, nigdy chat |
| Dashboard bez SSH tunnel | Publiczny dostęp do panelu | Zawsze tunnel SSH |
| Dashboard zanim rdzeń działa | Ozdobnik bez funkcji | Najpierw jeden działający agent |
| Wiele agentów na starcie | Chaos zanim zrozumiesz mechanikę | Najpierw jeden Hermes |
| Automatu bez przetestowania | Masowe złe outputy | Najpierw ręczny test pipeline |

---

## 📌 SEKCJA 10: USE CASES DLA HOLISTIC AIDHD I ADHD4LIFE

### Pasujące Use Cases z Tutoriali → Twoje Projekty

#### Use Case 1: Morning Priority Prompt (Cron)
**Źródło:** Tutorial "6 use cases" + Nate Herk
```
Codziennie o 9:00 agent pyta:
"Jaki jest Twój priorytet na dzisiaj?"
→ Generuje listę zadań dla agenta (Kanban/Triage)
→ Aktualizuje memory.md o priorytety
→ Wysyła przez Telegram
```
**Dla ADHD:** Idealne. Jeden trigger, zero decyzji rano. Agent przejmuje zarządzanie dniem.

#### Use Case 2: Community Digest — ADHD4Life (Cron)
```
Codziennie rano: 
→ Scout zbiera nowe wiadomości ze społeczności
→ Scribe tworzy digest: "Co dziś ważnego w ADHD4Life"
→ Reach sugeruje odpowiedzi i posty moderacyjne
→ Telegram: podsumowanie dla Ciebie o 8:00
```

#### Use Case 3: Content Pipeline — Holistic AIDHD (Skill + /goal)
```
Na bazie jednego tematu / nagrania głosowego:
→ Scout: research + konkurencja
→ Scribe: artykuł, newsletter, skrypt wideo
→ Reach: karuzele IG, post LinkedIn, Twitter/X
→ Wszystko do Google Drive / Obsidian
Uruchamiane komendą: "/pipeline temat: [ADHD i planowanie dnia]"
```

#### Use Case 4: Brain Dump → Struktura (Skill)
```
User nagrywa voice note lub wpisuje chaotyczny tekst
→ Agent zamienia w:
   - Named tasks z priorytetami
   - Bloki tematyczne
   - Propozycja kolejnego kroku (jeden!)
→ Trafia do Kanbana jako Triage
```
**Dla ADHD:** Kluczowy use case. Eliminuje paraliż decyzyjny.

#### Use Case 5: Dashboard Builder — Iteracyjny (Julian Goldie + Hermes)
```
Hermes buduje i iteruje Streamlit dashboard:
"Dodaj do dashboardu moduł Daily Goals — 
 formularz 3 celów, wieczorny check-in, 
 dane w journal.json"
→ Hermes edytuje app.py
→ Restart Streamlit automatyczny
```

#### Use Case 6: Nightly GitHub Backup (Cron)
```
Codziennie o 2:00 w nocy:
→ git add ~/Agentic_OS/dashboard/
→ git commit -m "auto: nightly backup [data]"
→ git push origin main
→ Raport przez Telegram: "✅ Backup OK"
```

#### Use Case 7: Session Recall — Drugi Mózg
```
Hermes przechowuje wszystkie sesje w SQLite
→ Możliwość wyszukiwania: "Co omawialiśmy o dashboard MVP?"
→ Memory Wiki jako strona z logami sesji
→ Obsidian Vault jako long-term knowledge base
```
**Dla ADHD:** Eliminuje "gdzie to było?" i lęk przed zapomnieniem.

#### Use Case 8: Technical Research Mode
```
"Przeanalizuj dashboard julianagoldie.com — 
 jaki stack używa, jak jest zbudowany, 
 zapisz raport jako markdown"
→ Agent otwiera przeglądarkę, analizuje konsolę
→ Raport trafia do memory / Obsidian
→ Używany jako input dla Dev agenta
```

---

## 📌 SEKCJA 11: KONFIGURACJA DLA HOLISTIC AIDHD

### Starter Pack — Gotowe Pliki Pamięci

#### user.md (wgraj do ~/.hermes/)
```markdown
# user.md — Tomasz Duda | Holistic AIDHD

## Tożsamość
- Imię: Tomasz Duda
- Lokalizacja: Łódź, Polska
- Język: polski (główny), angielski (roboczy)

## Styl pracy
- Przedsiębiorca i strateg produktu cyfrowego
- Działa szybko, iteracyjnie, eksperymentalnie
- Ceni automatyzację i redukcję chaosu
- Pracuje równolegle nad strategią, contentem, community, automatyzacjami

## Preferencje komunikacyjne
- Odpowiadaj po polsku
- Pisz jasno, konkretnie, bez lania wody
- Rozbijaj złożone tematy na krótkie sekcje i kroki
- Proponuj JEDEN sensowny następny krok, nie 10 opcji naraz
- Ton: wspierający, spokojny, zadaniowy
- NIE oceniający, NIE zawstydzający
```

#### memory.md (wgraj do ~/.hermes/)
```markdown
# memory.md — Kontekst Projektów

## Projekt główny: Holistic AIDHD
Dashboard + ekosystem AI dla osób z ADHD i neuroróżnorodnych.
Stack: Streamlit (port 8501 na GCP VPS), Hermes Agent OS.
GitHub: prywatne repo holistic-aidhd-os (w konfiguracji).

## Społeczność: ADHD4Life
Community wsparcia, edukacji i praktycznych narzędzi dla ADHD.
Potrzeby: digest, moderacja, onboarding, resources.

## Użytkownicy docelowi
Osoby z ADHD i neuroatypowe: przeciążenie info, potrzeba struktury,
krótkie komunikaty, empatyczny język, widoczny next step.

## Zasady projektowe ADHD-friendly
- Minimalne tarcie poznawcze
- Małe kroki
- Czytelna hierarchia
- Ograniczenie nadmiaru opcji
- Widoczny jeden next step

## Priorytety operacyjne
- Wszystko ważne → do pamięci lub repo
- Wszystko powtarzalne → skill
- Wszystko krytyczne → backup
- System: prosty do utrzymania i skalowania
```

### Pierwsze Skills do Wdrożenia (priorytet)
1. `nightly-github-sync` — backup o 2:00 (GitHub)
2. `morning-priority-prompt` — poranny trigger 9:00
3. `brain-dump-to-kanban` — chaos voice → struktura Kanban
4. `community-digest-adhd4life` — dzienny digest społeczności
5. `content-pipeline-holistic` — jeden temat → wiele formatów

### Pierwsze Crony do Wdrożenia
```
"Codziennie o 2:00 → nightly-github-sync"
"Codziennie o 9:00 → morning-priority-prompt"
"Codziennie o 22:00 → przypomnij Tomaszowi o wypełnieniu journal wieczornego"
"Raz w tygodniu (poniedziałek 8:00) → raport: co działa / co blokuje / co dalej"
```

---

## 📌 SEKCJA 12: STACK TECHNICZNY — KOMPLETNA LISTA

### Warstwa Bazowa (wymagana)
- **Hermes Agent OS** — Nous Research (open source, MIT)
- **VPS** — Ubuntu 24.04 (min. 2 vCPU, 4 GB RAM, 20 GB SSD)
- **Model API** — OpenRouter (rekomendowane) lub Anthropic bezpośrednio
- **Telegram** — kanał C2 (BotFather + user ID)

### Warstwa Pamięci (rekomendowana)
- **GitHub** (prywatne repo) — source of truth, backup
- **Obsidian** — lokalna baza wiedzy / long-term memory
- **SQLite** (wbudowane w Hermesa) — session search

### Warstwa Komunikacji (opcjonalna)
- **Discord** — dedykowane kanały per agent (multi-agent setup)
- **Tailscale** — prywatna sieć urządzeń (cross-device workflow)

### Warstwa Integracji Treści (opcjonalna)
- **Google Drive** — repozytorium outputów
- **YouTube Analytics** — analiza treści i wyników
- **Higgsfield Supercomputer** — gotowe środowisko (droższe, bez konfiguracji)
- **Indexceptional API** — automatyczne indeksowanie treści SEO

### Warstwa Monitoring/Dashboard
- **Streamlit** — własny dashboard (budowany przez Hermesa)
- **Mission Control Dashboard** — wbudowany w Hermesa (`hermes dashboard`)

### Free Tier Stack (na start, zero kosztów)
```
Hermes Agent OS (open source, free)
+ Owl Alpha przez OpenRouter (1M tokenów, free)
+ Obsidian (lokalne, free)
+ Telegram Bot (free)
+ GitHub (prywatne repo, free)
+ Racknet VPS ($5/mies.) lub GCP Free Tier
```

---

## 📌 SEKCJA 13: DECISION TREES — KIEDY CO ROBIĆ

### Kiedy tworzyć nowego agenta?
```
Nowa rola wymaga innych uprawnień?           → TAK → nowy agent
Nowa rola wymaga innych sekretów API?        → TAK → nowy agent
Nowa rola wymaga osobnej pamięci?            → TAK → nowy agent
Nowa rola ma innych odbiorców (klientów)?   → TAK → nowy agent
Obecny agent jest stabilny i nie wystarczy? → TAK → nowy agent
Wszystko inne                                → NIE → jeden Hermes
```

### Kiedy używać /goal?
```
Zadanie ma >5 kroków?           → TAK → /goal z meta-promptem
Zadanie zajmie >20 minut?       → TAK → /goal
Możesz odejść od komputera?     → TAK → /goal
Zadanie wymaga decyzji w połowie? → NIE → nie /goal
Zadanie jest jednorazowe?        → NIE → bezpośredni prompt
```

### Kiedy robić skill?
```
Dajesz tę samą instrukcję drugi raz?    → ZRÓB SKILL natychmiast
Agent zrobił to dobrze raz?             → ZAPISZ jak procedurę
Zadanie pojawia się regularnie?         → SKILL + CRON
Wynik może być używany jako input?      → SKILL (raport markdown)
```

---

## 📌 QUICK REFERENCE — KOMENDY I PROMPTY

### Komendy CLI Hermesa
```bash
hermes setup                    # Quick Setup (provider, model, Telegram)
hermes dashboard                # Uruchom dashboard
hermes skills list              # Lista dostępnych skills
hermes model                    # Zmień model
hermes gateway start --background  # Uruchom jako usługa
```

### Slash Komendy w Telegram/Chat
```
/goal [opis celu]               # Autonomiczne długie zadanie
/background [task]              # Zadanie w tle
/scout [topic]                  # Zlecenie do agenta Scout
/dev [task]                     # Zlecenie do agenta Dev
/skills                         # Lista skills
```

### Gotowe Prompty Startowe dla Hermesa
```markdown
PROMPT ONBOARDING:
Przeczytaj pliki user.md, memory.md i soul.md.
Na tej podstawie:
1. Zaproponuj 5 pierwszych skills dla projektu Holistic AIDHD
2. Zaproponuj 3 pierwsze cron jobs
3. Wskaż co dopisać do pamięci
4. Zaproponuj architekturę dashboardu MVP
5. Wskaż co backupować do GitHub
Pisz po polsku, zwięźle, ADHD-friendly.
```

```markdown
PROMPT GITHUB SETUP:
Połącz mnie z prywatnym repo GitHub "holistic-aidhd-os".
Stwórz skill "nightly-github-sync" który codziennie o 2:00:
1. git pull z ~/Agentic_OS/
2. git add pliki dashboardu i skills
3. git commit z automatyczną datą
4. git push origin main
5. Wyślij przez Telegram "✅ Backup OK [data]"
Token wgraj z .env (GITHUB_TOKEN), nie przez chat.
```

```markdown
PROMPT KANBAN MANAGER:
Gdy napiszę "dodaj zadanie: [treść]" → zapisz do kanban.json w sekcji todo.
Gdy napiszę "co mam do zrobienia" → przeczytaj kanban.json i odpowiedz.
Gdy napiszę "zrób task: [id]" → przesuń do in-progress i zacznij.
Stwórz z tego skill o nazwie "kanban-manager".
```

---

## 📌 SEKCJA 14: ZESTAWIENIE Z PLANAMI HOLISTIC AIDHD

### Mapowanie Planów na Możliwości Hermesa

| Twój Plan | Hermes Capability | Status |
|---|---|---|
| Dashboard Mission Control | Hermes buduje i iteruje Streamlit | ✅ Gotowe (po fix SSH) |
| Kanban ADHD-friendly | Hermes R/W kanban.json przez Telegram | 🔜 Faza 2 |
| Brain Dump → Struktura | Skill brain-dump-to-kanban | 🔜 Faza 2 |
| C-Suite (CMO, CEO) | Skills z kontekstem z o_mnie.md | 🔜 Faza 3 |
| Community Digest ADHD4Life | Cron + Skill community-digest | 🔜 Faza 2 |
| Content Pipeline | Scout → Scribe → Reach Pipeline | 🔜 Faza 3 |
| NotebookLM Integration | Sync audio do ~/Agentic_OS/notebooks/ | 🔜 Faza 3 |
| GitHub Backup | nightly-github-sync cron | 🔜 Faza 1 (PRIORYTET) |
| Telegram Sterowanie | Gateway aktywny ✅ | ✅ Gotowe |
| Daily Goals & Journal | Skill + journal.json + cron 22:00 | 🔜 Faza 2 |

### Dedykowane Persony Dashboard dla Użytkowników ADHD4Life

Na podstawie tutoriali: jeden Hermes OS może budować **osobne dashboardy dla różnych typów użytkowników**:

| Persona | Potrzeby | Dashboard Focus |
|---|---|---|
| **Przedsiębiorca** | Strategia, delegowanie, pipeline | C-Suite + Kanban + Content |
| **Twórca treści** | Repurposing, automatyzacja | Content Pipeline + Skills |
| **Etatowiec** | Organizacja dnia, brain dump | Morning Prompt + Kanban |
| **Osoba ADHD** | Małe kroki, jeden next step | Brain Dump + One Thing |
| **Członek społeczności** | Digest, wsparcie, zasoby | Community + Resource Library |

---

*Dokument skompilowany z: blueprint-hermes-agent-alex-finn.md, blueprint-hermes-agent-os-JulianGoldie.md, hermes-agent-blueprint-6-use-cases.md, hermes-agent-nateherk-blueprint-dla-antigravity.md, zSecurity_Hermes_Ai_Hacking_team.md, hermes_agent_os+higgsfield.md, hermes_5_Ways_to_Make_Hermes_Agent_10X_Better_blueprint.md, blueprint-hermes-premium-mission-control-5-agent-content-pipeline.md, hermes-starter-pack-holistic-adhd-adhd4life.md, Stack_Hermes_Agentic_OS.md*
