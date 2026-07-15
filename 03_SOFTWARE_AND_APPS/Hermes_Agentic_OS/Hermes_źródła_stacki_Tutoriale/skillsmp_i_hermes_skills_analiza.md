# SkillsMP Marketplace — Analiza + Inwentarz Hermes Skills
**Data:** 2026-06-02 | Anti-Gravity

---

## 1. Co to jest SkillsMP.com?

**SkillsMP NIE jest repozytorium GitHub.** To **niezależna platforma-marketplace** (Next.js, własna infrastruktura) z REST API do przeszukiwania bazy skillów.

### Kluczowe fakty

| Parametr | Wartość |
|---|---|
| Baza skillów | **1,5 miliona** skills indeksowanych |
| Kompatybilność | Claude Code, Codex CLI, ChatGPT, **Hermes Agent** |
| Dostęp do bazy | REST API + interfejs WWW |
| Model biznesowy | API key wymagany do wyszukiwania programatycznego |
| Sponsor / partner | **Manus.im** (widoczne logo na górze strony) |

### "Manus" przy górze — co to?

To baner sponsorski od **Manus.im** — chińskiego agentowego AI (bezpośredni konkurent ChatGPT). Manus jest głównym sponsorem SkillsMP i oferuje możliwość "uruchamiania Skills jednym kliknięciem" przez ich platformę. **Nie ma to wpływu na same skille** — możesz je importować do Hermesa niezależnie od Manusa. SkillsMP działa jak App Store, a Manus jest tam głównym wystawcą.

### Czy skille są darmowe?

**Tak — w 99%.** Skille to pliki SKILL.md (Markdown) — open source. Płacisz wyłącznie za API key do przeszukiwania marketplace (sama baza wiedzy jest bezpłatna do pobrania po znalezieniu).

### Jak działa API SkillsMP?

```
Base URL: https://skillsmp.com/api/v1

Endpoint wyszukiwania:
GET /skills/search?q={query}&category={cat}&limit=20

Autentykacja: Bearer Token (API Key z konta na skillsmp.com)
```

W Hermes Studio podpinasz przez: **Settings → Integrations → SkillsMP API Key**

---

## 2. Hermes Agent — 101 zainstalowanych Skills (pełny inwentarz)

### [AUTONOMOUS-AI-AGENTS] 7 skills — kluczowe dla systemu
- `claude-code` — integracja z Claude Code
- `codex` — OpenAI Codex CLI
- `goal-mode-autonomy` — tryb autonomiczny (długie zadania bez przerw)
- `hermes-agent` — dokumentacja własnego agenta
- `hermes-gcp-integration` — GCP + Hermes bridge
- `kanban-codex-lane` — Kanban dla Codexa
- `opencode` — open source coding agent

### [SOFTWARE-DEVELOPMENT] 13 skills — baza inżynieryjna CTO AI
- `systematic-debugging` ← **priorytet dla CTO AI**
- `test-driven-development`
- `subagent-driven-development`
- `requesting-code-review`
- `hermes-agent-skill-authoring` ← **do tworzenia nowych skillów!**
- `writing-plans`, `plan`, `spike`
- `node-inspect-debugger`, `python-debugpy`
- `hermes-s6-container-supervision`
- `streamlit-ops`, `debugging-hermes-tui-commands`

### [PRODUCTIVITY] 9 skills — COO, CMO, CFO
- `google-workspace` ← Gmail, Calendar, Drive, Docs, Sheets
- `notion` ← zarządzanie bazą wiedzy
- `airtable` ← CRM/tracking tabelaryczny
- `linear` ← zarządzanie projektami (jak Jira)
- `ocr-and-documents` ← ekstrakcja tekstu z PDF/skanów
- `powerpoint` ← generowanie prezentacji .pptx
- `maps`, `nano-pdf`, `teams-meeting-pipeline`

### [DEVOPS] 6 skills — infrastruktura CTO
- `nginx-reverse-proxy` ← **właśnie go używamy!**
- `streamlit-nginx-deployment`
- `webhook-subscriptions` ← **potencjalnie dla Systeme.io!**
- `gcp-vertex-ai-migration`
- `kanban-orchestrator`, `kanban-worker`

### [INTEGRATIONS] 3 skills — nasza baza
- `hermes-gcp-vertex-ai` ← Tier 1 gotowy
- `mcp-stdio-integration`
- `systeme-io-integration` ← **właśnie przez nas utworzony** ✅

### [MLOPS] 10 skills
- `gcp-vertex-ai-proxy-setup` ← **konfiguracja Tier 1!**
- `serving-llms-vllm`, `llama-cpp` — lokalne LLM
- `huggingface-hub`, `weights-and-biases`
- `dspy`, `evaluating-llms-harness`
- `audiocraft-audio-generation`, `segment-anything-model`
- `obliteratus`

### [CREATIVE] 20 skills — dla CCO AI
- `claude-design`, `excalidraw`, `sketch`, `architecture-diagram`
- `manim-video`, `ascii-art`, `ascii-video`, `p5js`
- `songwriting-and-ai-music`, `pixel-art`, `comfyui`
- `baoyu-infographic`, `baoyu-comic`, `baoyu-article-illustrator`
- `ideation`, `humanizer`, `design-md`
- `popular-web-designs`, `pretext`, `touchdesigner-mcp`

### [RESEARCH] 5 skills — CEO, CSO AI
- `arxiv` — szukanie papers naukowych
- `llm-wiki` — interlinked knowledge base (Karpathy style)
- `polymarket` — rynki predykcji / prognozy
- `blogwatcher` — monitoring RSS i blogów
- `research-paper-writing`

### [GITHUB] 7 skills — CTO AI
- `github-pr-workflow`, `github-code-review`
- `github-issues`, `github-repo-management`
- `codebase-inspection`, `github-auth`, `nightly-github-sync`

### [SOCIAL-MEDIA] 1 skill — CMO/CCO AI
- `xurl` — X/Twitter via CLI (posty, wyszukiwanie, DM, media v2 API)

### [MEDIA] 5 skills
- `spotify` ← kontrola muzyki przez CLI
- `youtube-content` ← transkrypcje YouTube → posty/blogi
- `gif-search`, `heartmula` (generowanie muzyki), `songsee`

### Pozostałe
- **[APPLE]** 5 — iMessages, Notes, Reminders, FindMy, macOS Computer Use
- **[NOTE-TAKING]** 1 — `obsidian`
- **[DATA-SCIENCE]** 1 — `jupyter-live-kernel`
- **[EMAIL]** 1 — `himalaya`
- **[SMART-HOME]** 1 — `openhue` (Philips Hue!)
- **[GAMING]** 2 — Minecraft modpack server, Pokemon player
- **[RED-TEAMING]** 1 — `godmode`
- **[MCP]** 1 — `native-mcp`

---

## 3. Rekomendacje: Co warto zainstalować z SkillsMP dla Virtual Board

### Priorytet WYSOKI

| Skill (szukaj w SkillsMP) | Dla kogo | Dlaczego |
|---|---|---|
| `google-business-profile` lub `gbp-automation` | Agency Boutique | Kluczowy moduł B2B |
| `email-sequence` / `email-outreach` | CSO AI | Follow-upy i sekwencje sprzedażowe |
| `crm-analysis` | CSO, CFO | Dane CRM + analiza pipeline |
| `social-media-scheduler` | CMO, CCO | Harmonogram i kolejkowanie postów |
| `financial-report` / `invoice-generator` | CFO | Raporty i faktury |

### Priorytet ŚREDNI

| Skill | Dla kogo |
|---|---|
| `seo-optimizer` | CMO, CCO |
| `competitor-research` | CSO, CEO |
| `linkedin-outreach` | CSO |
| `content-calendar` | CMO, CCO |

### Jak aktywować SkillsMP w Hermes Studio

1. Załóż darmowe konto na [skillsmp.com](https://skillsmp.com)
2. Pobierz API key ze swojego profilu
3. W Hermes Studio: **Settings → Integrations → SkillsMP API Key**
4. W zakładce **Marketplace** w Skills Browser wyszukuj i instaluj jednym kliknięciem

> **UWAGA:** Skille z SkillsMP to zwykłe pliki SKILL.md — taki sam format jak te, które już mamy. Możesz je też pobrać ręcznie i wrzucić do `~/.hermes/skills/{kategoria}/{nazwa}/SKILL.md`.
