# MEMORY - lifewave (Fala Życia OS)

---

## STATUS PROJEKTU
- **Status:** Wdrożone na Cloud Run (Produkcja, Region Warszawa `europe-central2`)
- **Ostatnia aktualizacja:** 2026-07-30 przez Antigravity AI
- **Bieżący cel główny:** Interaktywny Dashboard Akademii Klubu Fala Życia z Agentem Doradcą AI (Gemini 2.5 Flash na Vertex AI) oraz zoptymalizowany pod mobile portal `fala-zycia.pl` z przezroczystym proxy dla `app.fala-zycia.pl`.

---

## ARCHITEKTURA I STACK TECHNICZNY
- **Dashboard Aplikacji:** Python 3.11 / Streamlit (`02-website/dashboard.py` & `modules/home.py`, `advisor.py`, `academy.py`, `flight_hacking.py`, `celergize.py`, `breathwork.py`, `partner.py`).
- **Portal WWW:** Nginx Alpine (`02-website/Dockerfile.web` & `nginx.conf`) z przezroczystym proxy dla `app.fala-zycia.pl`.
- **Serwery Chmurowe GCP:** 
  - `fala-zycia-dashboard` (Cloud Run `europe-central2`)
  - `fala-zycia-web` (Cloud Run `europe-central2`)
- **CI/CD Manifesty:** `02-website/cloudbuild_web.yaml` oraz `02-website/cloudbuild_dashboard.yaml`.
- **Procesor AI:** Vertex AI (`gemini-2.5-flash`, region `us-central1`).
- **Baza Wiedzy:** Obsidian `.md` w `04-assets/knowledge_base/` (w tym pełne notatki Kursu Piotra Lotniczego `MLM_DUPLICATION_MASTER.md` - 187 KB, X2O, X39).

---

## ZREALIZOWANE KAMIENIE MILOWE
- [x] **Kamień Milowy 1:** Pobranie i ustrukturyzowanie pełnej Bazy Wiedzy MLM & Flight Hacking (`MLM_DUPLICATION_MASTER.md`).
- [x] **Kamień Milowy 2:** Podpięcie klucza Service Account i uprawnień `roles/aiplatform.user` na Vertex AI.
- [x] **Kamień Milowy 3:** Usunięcie 100% sprzecznych wpisów o koralowcu i 70 minerałach, powiększenie logo (52-54px) w headerze oraz naprawienie etykiet plastrów w `lifewave-fototerapia.html`.
- [x] **Kamień Milowy 4:** Wdrożenie przezroczystego proxy Nginx dla `app.fala-zycia.pl` (URL na stałe zachowuje czystą domenę).
- [x] **Kamień Milowy 5:** Rozdzielenie manifestów Cloud Build i usunięcie zdublowanej starej usługi z regionu Belgii (`europe-west1`).

---

## AKTYWNE URL-E I NAMIARY PRODUKCYJNE
- **Aplikacja Dashboard (Natywna Subdomena):** https://app.fala-zycia.pl
- **Aplikacja Dashboard (Direct Cloud Run URL):** https://fala-zycia-dashboard-194182220831.europe-central2.run.app
- **Główny Portal WWW:** https://fala-zycia.pl
- **Repozytorium GitHub:** https://github.com/holisticjson/falazycia-os
