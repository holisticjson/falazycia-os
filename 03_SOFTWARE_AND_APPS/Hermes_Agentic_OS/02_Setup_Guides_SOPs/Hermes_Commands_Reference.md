# 📚 Katalog Komend Hermesa (Hermes Agentic OS)

Ten dokument stanowi pełny wykaz komend systemowych i skilli (umiejętności) dostępnych w bocie Telegram Hermesa. Jest to referencja do wykorzystania w projektach "Holistic" oraz instrukcja dla agentów (np. Ghosta, CTO), z jakich narzędzi mogą korzystać w ramach Hermesa.

---

## 🛠️ Komendy Systemowe i Zarządzanie Sesją

*   **/new [name]** -- Rozpoczyna nową sesję (nowy ID sesji + czysta historia) (alias: /reset)
*   **/topic [off|help|session-id]** -- Włącza lub zarządza sesjami w oparciu o "Tematy" (Topics) na Telegramie
*   **/retry** -- Ponawia ostatnią wiadomość do agenta
*   **/undo** -- Cofa (usuwa) ostatnią wymianę zdań między użytkownikiem a asystentem
*   **/title [name]** -- Ustawia tytuł dla obecnej sesji
*   **/branch [name]** -- Rozgałęzia aktualną sesję, aby zbadać inną ścieżkę konwersacji (alias: /fork)
*   **/compress [focus topic]** -- Ręczna kompresja kontekstu konwersacji
*   **/rollback [number]** -- Wyświetla lub przywraca punkty kontrolne (checkpoints) systemu plików
*   **/stop** -- Zatrzymuje wszystkie działające procesy w tle
*   **/approve [session|always]** -- Akceptuje oczekującą niebezpieczną komendę
*   **/deny** -- Odrzuca oczekującą niebezpieczną komendę
*   **/background <prompt>** -- Uruchamia prompt w tle (alias: /bg, /btw)
*   **/agents** -- Pokazuje aktywne agenty i zadania w tle (alias: /tasks)
*   **/queue <prompt>** -- Kolejkuje prompt na następną turę (bez przerywania obecnej) (alias: /q)
*   **/steer <prompt>** -- Wstrzykuje wiadomość po następnym wywołaniu narzędzia bez przerywania

## 🎯 Cele i Tryby Pracy

*   **/goal [text | pause | resume | clear | status]** -- Ustawia nadrzędny cel dla Hermesa, nad którym pracuje w wielu turach aż do jego realizacji
*   **/subgoal [text | remove N | clear]** -- Dodaje lub zarządza dodatkowymi kryteriami aktywnego celu
*   **/status** -- Pokazuje informacje o sesji
*   **/whoami** -- Pokazuje uprawnienia dostępu (admin / user)
*   **/profile** -- Pokazuje aktywną nazwę profilu i katalog domowy
*   **/sethome** -- Ustawia ten czat jako kanał domowy (alias: /set_home)
*   **/sessions** -- Przegląd ostatnich sesji (lista interaktywna) (alias: /ss)
*   **/resume [name]** -- Wznawia wcześniej nazwaną sesję
*   **/continue** -- Wznawia najnowszą sesję (alias: /c)
*   **/model [model] [--provider name] [--global]** -- Zmienia model AI dla obecnej sesji (alias: /provider)
*   **/codex_runtime [auto|codex_app_server]** -- Przełącza środowisko uruchomieniowe Codex dla modeli OpenAI
*   **/personality [name]** -- Ustawia predefiniowaną osobowość bota
*   **/footer [on|off|status]** -- Włącza/wyłącza stopkę z metadanymi bramki
*   **/yolo** -- Włącza tryb YOLO (pomija wszystkie zatwierdzenia niebezpiecznych komend)

## ⚙️ Zaawansowane i Konfiguracja

*   **/reasoning [level|show|hide]** -- Zarządza poziomem logiki i rozumowania modeli
*   **/fast [normal|fast|status]** -- Włącza tryb Fast (priorytetowe przetwarzanie dla OpenAI/Anthropic)
*   **/voice [on|off|tts|status]** -- Włącza tryb głosowy
*   **/bundles** -- Wyświetla paczki skilli
*   **/curator [subcommand]** -- Konserwacja skilli w tle
*   **/kanban [subcommand]** -- Tablica współpracy wielu profili (zadania, linki)
*   **/reload_mcp** -- Przeładowuje serwery MCP z konfiguracji
*   **/reload_skills** -- Skanuje ponownie folder `~/.hermes/skills/` w poszukiwaniu nowych skilli
*   **/commands [page]** -- Przegląd wszystkich komend
*   **/help** -- Wyświetla listę komend pomocy
*   **/restart** -- Płynny restart bramki (gateway) po zakończeniu aktywnych zadań
*   **/usage** -- Pokazuje zużycie tokenów i limity dla aktualnej sesji
*   **/insights [days]** -- Analiza zużycia tokenów
*   **/update** -- Aktualizuje system Hermes Agent do najnowszej wersji

## 🧠 Skille (Narzędzia Specjalistyczne)

*Lista najpopularniejszych skilli (kompletna lista liczy ponad 100 pozycji)*:

*   **/14_email_marketing_global** — Automatyzacja email marketingu (welcome series, nurture sequences)
*   **/airtable** — Obsługa bazy Airtable przez API
*   **/architecture_diagram** — Generowanie diagramów architektury (SVG/HTML)
*   **/arxiv** — Wyszukiwanie publikacji naukowych
*   **/claude_code** — Delegowanie zadań programistycznych do Claude Code CLI
*   **/comfyui** — Generowanie obrazów, wideo i audio przy użyciu ComfyUI
*   **/content_writing** — Copywriting i standardy pisania tekstów na strony WWW
*   **/email_marketing** — Strategie kampanii email, segmentacja i automatyzacja
*   **/gcp_vertex_ai_migration** / **/gcp_vertex_ai_proxy_setup** — Skille związane z Google Cloud Vertex AI i proxy modeli
*   **/goal_mode_autonomy** — Wykonywanie wielu zadań autonomicznie, aż do osiągnięcia 100% celu
*   **/hermes_agent** — Konfiguracja i rozwój środowiska Hermes Agent
*   **/lead_gen_pipeline** — Zautomatyzowany rurociąg generowania leadów (B2B, CRM)
*   **/model_routing** — Instrukcje inteligentnego wyboru modelu w środowisku wielomodelowym
*   **/money_strategy** — Tworzenie strategii biznesowych i finansowych (Pricing, GTM, badanie rynku)
*   **/node_inspect_debugger** — Debuggowanie aplikacji Node.js
*   **/notion** — Integracja z API Notion
*   **/project_planning** — Planowanie projektów, zarządzanie sprintami i zasobami
*   **/sales_calendly** — Konfiguracja i automatyzacje dla platformy Calendly
*   **/sales_crm_selection** — Strategia i selekcja systemów CRM (HubSpot, Salesforce itp.)
*   **/sales_outreach** — Sekwencje cold outreach i szablony dla B2B
*   **/seo_content_optimizer** — Pisanie i optymalizacja tekstów pod SEO
*   **/systeme_io_integration** — Integracja platformy Systeme.io
*   **/virtual_board_ceo** (oraz CCO, CFO, CMO, COO, CSO, CTO) — Skille Wirtualnego Zarządu (SOPy i instrukcje zachowań dla zarządu AI)
*   **/writing_plans** — Pisanie planów wdrożeniowych i podział na zadania

---
*Dokument wygenerowany w celu integracji z Holistic AIDHD OS.*
