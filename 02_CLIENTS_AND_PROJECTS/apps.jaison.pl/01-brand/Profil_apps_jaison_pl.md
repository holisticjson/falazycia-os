# 📱 Profil Projektu: apps.jaison.pl (Własne Aplikacje Agencji J(AI)SON)

Ten profil zawiera specyfikację techniczną, konfigurację wdrażania oraz wytyczne marketingowe dla własnych produktów programistycznych i SaaS agencji J(AI)SON, hostowanych na subdomenie `app.jaison.pl` (lub w chmurze Google Cloud Platform).

## 🛠️ Główne Produkty w Portfolio:

### 1. 💬 Jaison Komunikator (`jaison_komunikator`)
*   **Cel:** Zaawansowana bramka i most komunikacyjny integrujący systemy CRM, n8n oraz agenty konwersacyjne z wieloma platformami (Telegram, WhatsApp, SMS).
*   **Architektura:** Lekki backend w FastAPI połączony z bazami SQLite/PostgreSQL, uruchamiany bezpośrednio jako demon tła na instancji GCP. Współdzieli stan z centralnym Hermes Agentic OS.
*   **Integracje:** webhook_api.py, telegram_bridge.py, automatyczne powiadomienia i pipeline'y n8n.

### 2. 🎙️ Vojsik AI (`vojsik_ai`)
*   **Cel:** System automatycznego klonowania głosu, transkrypcji notatek głosowych (np. z Omi / Voice Notes) oraz autonomicznego prowadzenia cold-callingu i rozmów handlowych.
*   **Technologia:** Integracja z modelami Gemini, ElevenLabs API, GCP Text-to-Speech i Speech-to-Text.
*   **Zastosowanie:** Obsługa modułu Voice & Audio Clone w dashboardzie agencji oraz zasilanie systemów oddzwaniania u klientów lokalnych (np. gabinetów stomatologicznych czy salonów piękności).

---

## 🚀 Standardy Wdrażania (Deploy Setup)
*   **Domena Główna:** `jaison.pl`
*   **Subdomena Aplikacji:** `app.jaison.pl` / `apps.jaison.pl`
*   **Serwer i Chmura:** Google Cloud Platform (GCP Compute Engine), zintegrowane przez serwer Nginx jako odwrócone proxy na maszynie wirtualnej Hermes.
*   **Baza Danych:** Wspólny lokalny silnik SQLite (`local_crm.db`) oraz zintegrowane repozytoria Kanban (`kanban.json`).
*   **Klucze API:** Zabezpieczone w centralnym pliku `.env` na serwerze GCP, brak kluczy w kodzie źródłowym.
