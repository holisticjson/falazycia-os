# 📈 Profil Projektu: Holistyczny Broker

Karta kontrolna i mapa drogowa dla projektu **Holistyczny Broker**.

> [!IMPORTANT]
> **Zasada Priorytetu (Nienaruszalna):** Zgodnie z projektową Biblią (`AGENTS.md`), projekt **Holistic Broker** jest obecnie odłożony na później. Cały wysiłek architektoniczny idzie na konto `hello@jaison.pl` i agencji AI Jaison. Żadne prace deweloperskie nie powinny być tu prowadzone bez ostatecznej, pisemnej zgody Tomasza.

---

## 📂 Spis Ścieżek i Namiarów

*   **Katalog Projektu (Stacjonarny & Laptop):**
    `C:\Aplikacje MVP\Holistyczny Broker`
*   **Główna Domena (Planowana):**
    `holistycznybroker.pl`
*   **Repozytorium Git:**
    *(Zmapowane jako sub-część lub osobny moduł)*

---

## 📑 Cel i Opis Projektu

System automatyzacji i CRM dla nowoczesnego pośrednika nieruchomości (Holistyczny Broker). 
*   **Główna idea:** Budowa asynchronicznych lejków pozyskiwania nieruchomości (scraping portali takich jak OLX, Otodom) oraz automatyczne dopasowywanie klientów kupujących za pomocą LLM.
*   **Integracje chmurowe:** Google Cloud Platform, asynchroniczne przepływy w n8n, CRM Systeme.io.

---

## 🚀 Plan Wdrożeniowy (Deploy)

*   **Front-end:** Streamlit Dashboard lub lekki Vite React na Cloud Run.
*   **Baza Danych:** SQLite / PostgreSQL na Cloud SQL.
*   **Automatyzacja:** Konteneryzowane instancje n8n na maszynie VM lub Cloud Run.
