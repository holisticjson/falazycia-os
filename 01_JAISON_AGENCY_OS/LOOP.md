# 🔄 LOOP.md — Jaison OS Autonomous Control Loop

This file defines the master recurring control loop for Jaison OS AI agents.

## 🎯 Master Goal & Cadence
- **Goal:** Execute end-to-end agency operations, lead intake, content generation, and system self-healing for Tomasz & B2B clients.
- **Cadence:** Triggered via Telegram `Jaison Mission Control`, Discord Multi-Channel, and Streamlit Dashboard (`app.py`).

## 🛡️ Safety & Governance
- **Human Escallation:** Escalates to Tomasz on destruction risk or paid API quota breaches.
- **No-Progress Detection:** Max 3 retries on broken code before writing root cause to `MEMORY_COMPOUND.md`.
- **Least Privilege:** Tools are restricted to project workspace `01_JAISON_AGENCY_OS`.

## 📌 References
- **Constraints:** `CONSTRAINTS.md` (AGENTS.md)
- **Active State:** `STATE.md` (WORKSPACE_MEMORY.md)
- **Verification:** `VERIFY.md` (walkthrough.md)
