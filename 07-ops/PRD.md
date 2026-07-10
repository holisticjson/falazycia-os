# 📄 Project Requirements Document (PRD) — J(AI)SON OS & Agency Portal
## 🔮 Domena Główna: jaison.pl & os.jaison.pl (Senior Architect Edition)

---

## 🎯 1. Cel Biznesowy i Wizja Projektu
**J(AI)SON** to autonomiczny ekosystem (strona usługowa `jaison.pl` + asystent Vertex AI + panel sterowania i system operacyjny Streamlit `os.jaison.pl` z agentami AI: Hermes, Viktor, Ghost v2) zaprojektowany dla twórców internetowych, przedsiębiorców B2B oraz osób z ADHD.

### Główne cele:
1.  **Redukcja Chaosu (ADHD Guardrails):** Przekształcanie surowych myśli (Brain Dump) w konkretne plany, nawyki i posty za pomocą asynchronicznej komunikacji tekstowo-głosowej.
2.  **Maksymalna Automatyzacja (Zero Cost Base):** Wykorzystanie samo-hostowanych narzędzi na własnym VPS (n8n, SQLite) oraz darmowych pakietów (Systeme.io, GCP Free Trial $300) w celu wyeliminowania stałych opłat abonamentowych.
3.  **Wiarygodność B2B (Social Proof Live):** Demonstracja technologii bezpośrednio na stronie głównej poprzez interaktywny kalkulator ROI i zasilany wiedzą czat asystencki.

---

## 🛠️ 2. Specyfikacja Techniczna i Święta Trójca
*   **Strona Główna (`jaison.pl`):** Responsywny frontend skompilowany w Vite i serwowany przez **Google Cloud Run** połączony z **Cloudflare** DNS.
*   **Panel Sterowania & Backend OS (`os.jaison.pl`):** Aplikacja Streamlit (`app.py`) na dedykowanej maszynie VPS (Port `9119`) zabezpieczona przez Nginx reverse proxy i certyfikat Let's Encrypt SSL.
*   **Centrala Automatyzacji (Self-Hosted `n8n`):** Kontener Docker na VPS pełniący rolę "mózgu" integracji, obsługujący webhooki, zapis leadów i dystrybucję zasobów.
*   **Dostarczalność Maili (`Systeme.io`):** Wykorzystanie darmowego planu (do 2000 kontaktów) wyłącznie do masowej wysyłki newsletterów, eliminując ryzyko spamu i banów domenowych.

---

## 🤖 3. Wyszukiwanie Semantyczne & Wirtualny Zarząd

### A. Wyszukiwanie Semantyczne Vertex AI Agent Builder (RAG)
*   **Baza Wiedzy (Data Store):** Crawler automatycznie indeksujący strony `jaison.pl` i `os.jaison.pl` oraz repozytorium dokumentów PDF/SOP z bezpiecznego kubka Google Cloud Storage (`gs://jaison-knowledge-base/`).
*   **Bezpieczne API Proxy:** Endpoint `/api/assistant/chat` na VPS autoryzowany kluczem Service Account na GCP, zapobiegający wyciekom kluczy API na frontendzie.
*   **Pływający Chat Widget:** Szklany, animowany widget na stronie głównej z opcją syntezy mowy (Web Speech API) do odsłuchiwania odpowiedzi głosem.

### B. Wirtualny Zarząd Agencji (C-Level):
*   **CEO AI:** Zarządzanie celami, codzienny ADHD Briefing.
*   **CMO & CCO AI:** Strategia marketingowa, pisanie postów/scenariuszy (Ghostwriter).
*   **CFO AI:** Budżety chmurowe, kalkulatory ROI, rentowność wdrożeń.
*   **CTO AI:** Deploy systemowy, n8n, zarządzanie Dockerem i integracje API.
*   **COO AI:** Przepływy n8n, harmonogramy Cron i redukcja tarcia operacyjnego.

---

## ⚡ 4. Wymagania Funkcjonalne n8n & Systeme.io (Obejście Limitów)

### A. Architektura Przepływu Leadów (Lead routing):
1. Użytkownik przesyła formularz na `jaison.pl` (zapis na ebook / audyt / kontakt).
2. Formularz wysyła zapytanie POST na bezpieczny webhook w **n8n na VPS-ie**.
3. n8n zapisuje dane leada w lokalnej bazie **SQLite** z pełną historią i tagowaniem (np. segment="ebook_neuro").
4. n8n wysyła do użytkownika maila powitalnego/ebooka przez SMTP Gmail (100% za darmo, bez obciążania limitów Systeme.io).
5. n8n przesyła kontakt do Systeme.io za pomocą API, mapując segment do pola niestandardowego `jaison_segment` i nadając jeden globalny tag `jaison_lead_all`.
6. Przy masowej wysyłce, Tomasz filtruje kontakty po wartości pola niestandardowego, omijając ograniczenie 1 darmowego tagu.

### B. Habit Verification Engine (COO/Cron):
* n8n na VPS wyzwala zadanie (Cron) pytające klienta na Slacku/Telegramie o wykonanie nawyków. Zapis wyników do SQLite i renderowanie wykresów w Streamlicie.
