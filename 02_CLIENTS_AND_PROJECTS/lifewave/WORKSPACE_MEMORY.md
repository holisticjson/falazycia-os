# MEMORY - lifewave (Fala Życia OS)

---

## STATUS PROJEKTU
- **Status:** Wdrożone na Cloud Run (Produkcja)
- **Ostatnia aktualizacja:** 2026-07-28 przez Antigravity AI
- **Bieżący cel główny:** Interaktywny Dashboard Akademii Klubu Fala Życia z Agentem Doradcą AI (Gemini 2.5 Flash na Vertex AI).

---

## ARCHITEKTURA I STACK TECHNICZNY
- **Dashboard:** Python / Streamlit (`02-website/app.py` & `modules/advisor.py`)
- **Serwer Chmurowy:** GCP Cloud Run (`fala-zycia-dashboard` w projekcie `falazycia-os`)
- **Procesor AI:** Vertex AI (`gemini-2.5-flash`, region `us-central1`)
- **Konta GCP:**
  - `falazycia-os` (GCP Trial, Cloud Run, Cloud Build, Vertex AI)
  - `fala-zycia-agents` (Konto `holisticjson@gmail.com`, GenAI App Builder $1000 Credit)
- **Baza Wiedzy:** Obsidian `.md` w `04-assets/knowledge_base/` (w tym transkrypcja Kursu Piotra Lotniczego, X2O, X39).

---

## NAJBLIŻSZE KAMIENIE MILOWE I STATUS TODO
- [x] **Kamień Milowy 1:** Pobranie i ustrukturyzowanie pełnej Bazy Wiedzy Kursu Piotra Lotniczego (`FLIGHT_HACKING_MASTER.md`).
- [x] **Kamień Milowy 2:** Podpięcie klucza Service Account i uprawnień `roles/aiplatform.user` na Vertex AI.
- [x] **Kamień Milowy 3:** Integracja modułu Doradcy AI (`advisor.py`) z Gemini 2.5 Flash.
- [x] **Kamień Milowy 4:** Automatyczny Build & Deploy na Cloud Run via Cloud Build Trigger.
- [ ] **Kamień Milowy 5:** Mapowanie subdomeny `app.fala-zycia.pl` w panelu GCP / DNS.

---

## AKTYWNE URL-E I NAMIARY
- **Dashboard Akademii (Cloud Run):** https://fala-zycia-dashboard-zhct4l5nxa-lm.a.run.app
- **Repozytorium GitHub:** https://github.com/holisticjson/falazycia-os
