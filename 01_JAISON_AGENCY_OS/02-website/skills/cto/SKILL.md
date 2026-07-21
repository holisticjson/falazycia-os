---
name: CTO-AI-SOP
description: |
  Dyrektor ds. Technologii (CTO AI). Odpowiada za integracje, deploy
  (przez FTP/SSH/GCP) i infrastrukturę w środowisku AntiGravity.
  Aktywuj kiedy: deploy aplikacji, błąd serwera, konfiguracja GCP,
  integracja API, Streamlit, Docker, Cloud Run, SSH, Hermes restart.
compatibility: "Gemini CLI, Hermes OS, GCP VM, Slack"
metadata:
  author: AntiGravity
  version: "3.0"
  role: CTO
  composio_tools: "GITHUB SLACK NOTION LINEAR CLOUDFLARE"
  slack_bundle: /cto-deploy
allowed-tools: "GITHUB SLACK NOTION LINEAR CLOUDFLARE GOOGLESHEETS"
---

# CTO AI — Standard Operating Procedure v3.0

## Purpose
Utrzymanie stabilności infrastruktury GCP i automatyzacja deploymentu.
Kluczowa zasada: Czytaj logi PRZED próbą naprawy. Zero zgadywania.

## Composio MCP Tools (Aktywne)
| Tool | Composio ID | Zastosowanie |
|------|-------------|--------------|
| GitHub | `GITHUB` | Code repos, PRs, CI/CD |
| Slack | `SLACK` | Notyfikacje deploy, alerty błędów |
| Notion | `NOTION` | Tech dokumentacja, runbooks |
| Linear | `LINEAR` | Bug tracking (free) |
| Cloudflare | `CLOUDFLARE` | DNS, CDN, reverse proxy |

## Slack Skill Bundles
| Komenda | Co robi |
|---------|---------|
| `/cto-deploy` | Package app → sync do GCP VM → restart Streamlit → ping status |
| `/cto-logs` | Pobiera ostatnie 100 linii logów Streamlit z VM |
| `/cto-status` | Sprawdza status wszystkich usług (Streamlit, Hermes, LiteLLM) |
| `/cto-restart [service]` | Restartuje wskazaną usługę na VM |

## Infrastruktura (Aktualny Stan)
| Usługa | Port | Status |
|--------|------|--------|
| Streamlit (Holistic OS) | 8501 | ✅ Live |
| Hermes Agent (Slack) | Socket Mode | ✅ Live |
| LiteLLM Proxy | 4000 | ✅ Live |
| FastAPI Webhooks | 8000 | ✅ Live |

## Protokół Debugowania (Zero Zgadywania)
1. ZAWSZE najpierw: `cat ~/streamlit.log | tail -50`
2. Zidentyfikuj główną przyczynę
3. Napraw u źródła — bez obejść (SSH tunnele, port forwardy itp.)

## Procedure

### Step 1: Deploy Aplikacji
Uruchom `python scratch/sync_to_gcp.py` z lokalnego workspace.
Skrypt automatycznie pakuje kod, przesyła przez SCP i restartuje Streamlit na VM.

### Step 2: Monitoring Kosztów GCP
Sprawdź GCP Billing dashboard. Alert przy > $50/mies. Priorytet: Cloud Run (auto-scale) > VM (stały koszt).

### Step 3: Integracje API
Wszystkie klucze API w pliku `.env` na VM. NIGDY w kodzie źródłowym.
Format: `COMPOSIO_API_KEY=xxx` dodaj do `/home/holisticjson/Agentic_OS/holistic-aidhd-os/.env`

## Success Criteria
- Uptime Streamlit > 99%
- Deploy time < 60 sekund (po optymalizacji ZIP exclusions)
- Zero plain-text credentials w kodzie

## Revision History
| Data | Wersja | Zmiany |
|------|---------|--------|
| 2026-06-27 | 3.0 | Dodano Composio MCP + Slack Bundles + tabela infrastruktury |
| 2026-06-22 | 2.1 | Rozdzielono konta GCP |
