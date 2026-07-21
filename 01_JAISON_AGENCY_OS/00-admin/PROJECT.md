# Project: Holistic Jason Dashboard & Integrations (2026-06-24 Update)

## Architecture
The application runs a Streamlit dashboard (`app.py`) serving as the main UI interface for the Holistic OS.
It integrates:
- **FastAPI Webhook Server (`webhook_api.py`)**: Receives incoming leads and writes them to Google Sheets / Systeme.io.
- **FastAPI Brain Dump Server (`brain_dump_api.py`)**: Saves ideas and notes to Obsidian vault.
- **Discovery Engine (`01_src/knowledge.py`)**: Conducts semantic search on Google Cloud Storage (RAG vs Brain Dump).

Updates for the current phase:
1. **Akademia.pl Mentoring**: New interactive tab in Streamlit utilizing Gemini / LiteLLM to run Mirka Burnejko's prompts and checklists.
2. **Skill Consolidation**: Consolidating all director skills into the workspace root `skills/` and updating the GCP sync script to copy/link them to Hermes config directories on the VM.
3. **COMED Hosting Automation Prompt**: Embedding a link/copyable button for the browser automation prompt.
4. **Alternative Architecture Document**: Embedding the architectural analysis in Ghost v2 format.
5. **Error Handling (Złota Zasada 6)**: Graceful error displays in UI when API keys/credentials are missing, avoiding raw tracebacks.
6. **E2E Testing Track**: Verification of all functional requirements and integrations via `pytest`.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|---|---|---|---|
| M1 | Skill Consolidation & Sync Script | Copy all global and local director skills to `skills/` and update `sync_to_gcp.py` to copy/link them on the VM. | None | DONE |
| M2 | Akademia.pl Mentoring UI Tab | Copy prompts/checklists to `scratch/burnejko/`, create the `🎯 Akademia.pl Mentoring` tab, integrate Gemini/LiteLLM generation, and link `alternative_architecture.md` / `comed_browser_prompt.md`. | M1 | DONE |
| M3 | Error Handling & Keys Validation | Add clear, actionable warning cards (Złota Zasada 6) in the UI for missing API keys/credentials instead of raw Python exceptions. | M2 | IN_PROGRESS |
| M4 | E2E Testing Track (Parallel) | Design and implement Tier 1-4 tests (pytest), verify systems.io and hermes integrations, ensure all tests pass. | None | IN_PROGRESS |
| M5 | Final E2E Integration Pass | Verify all features against completed E2E test suite and run adversarial coverage checks (Phase 2 hardening). | M3, M4 | PLANNED |

## Interface Contracts
### Akademia.pl Mentoring Engine
- Input: Selected prompt/checklista, custom input fields (e.g. company profile, target group).
- Action: Call Gemini API (via existing proxy or LiteLLM backend) to generate mentoring feedback/copy.
- Output: Rendered Markdown with a button to copy to clipboard.

### Skill Directory Layout
- Local Workspace: `c:\Aplikacje MVP\Holistic Jason\skills\`
- VM Target folders:
  - Skills: `/home/holisticjson/.hermes/skills/`
  - Profiles: `/home/holisticjson/.hermes/profiles/`

### Error Handling Protocol (Złota Zasada 6)
- Check keys on start: `OPENROUTER_API_KEY`, Vertex credentials, etc.
- If missing, render an amber warning card in the sidebar or respective module UI with step-by-step instructions on how to set it up, rather than allowing a traceback.

## Code Layout
- `app.py`: Main Streamlit app.
- `scratch/sync_to_gcp.py`: GCP VM synchronization script.
- `skills/`: Consolidated director skills folder.
- `tasks/comed_browser_prompt.md`: Browser automation prompt for COMED.
- `docs/alternative_architecture.md`: Alternative architecture document.
- `scratch/burnejko/`: Local copy of Akademia.pl prompts and checklists.
- `tests/`: Automated unit and integration tests directory.

