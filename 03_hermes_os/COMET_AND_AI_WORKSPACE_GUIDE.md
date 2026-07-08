# 🌐 Przewodnik Zarządzania Workspace: Comet Browser, AI Agents & NVIDIA NIM

Ten dokument opisuje operacyjną strukturę Twojej pracy z asystentem w przeglądarce Comet, model współpracy agentów AI (Hermes, Viktor, Antigravity) oraz integrację darmowych modeli z platformy NVIDIA NIM (`build.nvidia.com`).

---

## 📁 1. Grupy Kart (Tab Groups) w Przeglądarce Comet

Aby ułatwić zarządzanie i umożliwić asystentowi Comet automatyzację zadań na odpowiednich kontekstach, podziel swoje karty na trzy tematyczne grupy:

### 📊 Grupa A: Analityka i Piksele (Analytics & Tracking)
*   **Karty:**
    1.  **Google Tag Manager:** [tagmanager.google.com](https://tagmanager.google.com) (Zarządzanie tagami)
    2.  **Google Analytics 4:** [analytics.google.com](https://analytics.google.com) (Statystyki ruchu)
    3.  **PostHog Dashboard:** [us.posthog.com](https://us.posthog.com) (Nagrania sesji, zdarzenia użytkowników)
    4.  **Google AdSense:** [adsense.google.com](https://adsense.google.com) (Monetyzacja bloga/portalu)
*   **Przykładowe polecenia dla asystenta Comet w tym oknie:**
    *   *"Zweryfikuj, czy kod śledzenia GA4/PostHog został poprawnie dodany na mojej stronie lądowania."*
    *   *"Wyciągnij z tej zakładki identyfikator pomiaru (Measurement ID) i zapisz go do pliku txt."*

### 📢 Grupa B: Kampanie i Social Media (Ad Managers & Socials)
*   **Karty:**
    1.  **Meta Business Suite:** [business.facebook.com](https://business.facebook.com) (Zarządzanie stronami FB/Instagram, w tym Bar u Jasia, coolfon)
    2.  **Meta Ads Manager:** [adsmanager.facebook.com](https://adsmanager.facebook.com) (Kampanie reklamowe Meta)
    3.  **Google Ads Panel:** [ads.google.com](https://ads.google.com) (Kampanie reklamowe Google Search/Display)
    4.  **TikTok Ads Manager:** [ads.tiktok.com](https://ads.tiktok.com) (Kampanie TikTok Ads)
*   **Przykładowe polecenia dla asystenta Comet w tym oknie:**
    *   *"Przeanalizuj wyniki naszej kampanii reklamowej z ostatnich 7 dni i wskaż, które kreacje mają najwyższy CTR."*
    *   *"Pobierz komentarze z fanpage'a Bar u Jasia z ostatniego postu i przygotuj na nie spersonalizowane odpowiedzi."*

### ⚙️ Grupa C: Rdzeń Operacyjny AI (AI Core & Workspace)
*   **Karty:**
    1.  **Slack Web Client:** [holisticjson.slack.com](https://holisticjson.slack.com) (Czaty z Hermes OS i Viktorem)
    2.  **Composio Dashboard:** [dashboard.composio.dev](https://dashboard.composio.dev) (Zarządzanie tokenami OAuth i API)
    3.  **Holistic OS Streamlit:** [localhost:8501](http://localhost:8501) (Twój lokalny panel zarządzania)
    4.  **Stripe Dashboard:** [dashboard.stripe.com](https://dashboard.stripe.com) (Sandbox / Płatności testowe)
    5.  **NVIDIA NIM Catalog:** [build.nvidia.com](https://build.nvidia.com) (API i modele AI NIM)
*   **Przykładowe polecenia dla asystenta Comet w tym oknie:**
    *   *"Sprawdź logi w Stripe i upewnij się, czy ostatnia płatność testowa przeszła pomyślnie."*
    *   *"Pobierz klucz API z Composio/NVIDIA i zapisz go do mojego lokalnego schowka."*

---

## 🤖 2. Podział Obowiązków Agentów: Hermes vs. Viktor vs. Antigravity

Aby uniknąć dublowania pracy i optymalnie wykorzystać darmowe kredyty, systemy są podzielone na trzy wyraźne role:

```mermaid
graph TD
    User([Tomasz]) -->|Pair Programming| AG[Antigravity (Czat Local Coder)]
    User -->|Direct Message / Mentions| Slack[Slack Workspace]
    
    Slack -->|System Admin / GitHub / Local DB| Hermes[Hermes OS (GCP VM)]
    Slack -->|SaaS Integrations / PDF & Excel Generator| Viktor[Viktor.com (Cloud Sandbox)]
    
    Hermes <-->|OAuth / API Tools| Composio[Composio Broker]
    Viktor <-->|3200+ Apps native| Apps[HubSpot, Stripe, Notion...]
```

### 🧠 Hermes OS (Mózg Systemowy i Deweloperski)
*   **Gdzie działa:** Zainstalowany na maszynie wirtualnej GCP (`34.55.82.86`).
*   **Do czego służy:** To Twój administrator systemowy i programista. Obsługuje bezpośrednio kod aplikacji (`app.py`), zarządza procesami systemd na serwerze, bazą SQLite oraz synchronizacją plików z Google Cloud Storage.
*   **Integracje:** Korzysta z **Composio** do komunikacji z API zewnętrznymi za pomocą tokenów (np. Google Sheets CRM, GitHub API, Slack Gateway).
*   **Jak pobiera Skille:** Posiada folder `/agency_skills/` oraz wtyczki. Gdy Hermes napotka nieznane zadanie, analizuje te pliki i wczytuje odpowiednie procedury.

### 🤖 Viktor.com (Autonomiczny Asystent Biurowy)
*   **Gdzie działa:** Autonomiczny agent chmurowy zintegrowany ze Slackiem.
*   **Do czego służy:** To Twój cyfrowy sekretarz i analityk biznesowy. Specjalizuje się w asynchronicznym uruchamianiu własnego kodu Python w chmurze, aby generować dla Ciebie pliki (PDF, Excel, prezentacje) na podstawie danych z połączonych aplikacji.
*   **Integracje:** Posiada wbudowane natywne konektory do **3200+ aplikacji** bez konieczności kodowania bramki.
*   **Maksymalizacja Kredytów:** Podłączamy **10 darmowych narzędzi** (Google Sheets, Stripe Sandbox, Google Analytics, Search Console, Google Ads, Meta Ads, LinkedIn, YouTube, Instagram, Canva), aby zyskać **10,000 darmowych kredytów** w ramach promocji Viktor.com!

### 🔧 Antigravity (Ja - Twój Kodujący Partner AI)
*   **Gdzie działa:** Bezpośrednio w Twoim lokalnym IDE/środowisku programistycznym.
*   **Do czego służy:** Pomagam Ci pisać pliki projektów, wdrażać nową architekturę i wspólnie debugować błędy.
*   **Jak dynamicznie pobieram Skille:**
    *   Wczytuję pliki konfiguracyjne z folderów `.agents/skills/` oraz globalnego katalogu `.gemini/config/`.
    *   **Zasada Dynamicznego Pobierania Skilli:** Jeśli stwierdzę brak specjalistycznego skilla do wykonania zadania, a w repozytorium nie ma odpowiedniego pliku, mogę dynamicznie przeszukać sieć (wykorzystując `search_web`), odnaleźć oficjalną dokumentację lub zdefiniowane SOP marketingowe/deweloperskie, a następnie **trwale zapisać je** jako nowy plik `SKILL.md` w katalogu `.agents/skills/<nazwa_skilla>/`.

---

## ⚡ 3. Raport: NVIDIA NIM (build.nvidia.com) — Analiza Darmowych Możliwości

Platforma **NVIDIA Build** to świetne, darmowe źródło zasilania modeli AI dla naszej agencji.

### 📈 Limity Darmowego Planu (Free Tier):
1.  **Kredyty na start:** Każde nowe konto deweloperskie otrzymuje **1000 darmowych kredytów** na zapytania API (można rozszerzyć do 5000). Karta kredytowa nie jest wymagana.
2.  **Rate Limit (Limity zapytań):** Maksymalnie **40 zapytań na minutę (RPM)**. Przekroczenie limitu zwraca błąd `429 Too Many Requests`.
3.  **Charakter API:** API NIM jest w pełni kompatybilne z formatem **OpenAI API**. Oznacza to, że możemy bardzo łatwo podmienić base URL i klucz API w naszym orkiestratorze (LiteLLM / Streamlit).

### 🤖 Dostępne Modele (Ponad 100 modeli w katalogu):
*   **LLMs:** Najnowsze modele Llama 3, Mistral Large, Mixtral 8x22B, Phi-3, Qwen oraz zaawansowane modele DeepSeek.
*   **NVIDIA Nemotron:** Specjalnie zoptymalizowane modele od NVIDII do zadań deweloperskich i logicznych.
*   **Multimodal & Embedding:** Modele do analizy obrazów, generowania grafik oraz zaawansowanego wektoryzowania tekstu (przydatne do RAG i bazy wiedzy).

> [!TIP]
> **Rekomendacja dla Agencji:** Wykorzystamy darmowe klucze z `build.nvidia.com` jako **darmowy fallback** w konfiguracji LiteLLM. Jeśli skończą się darmowe środki na koncie Vertex AI ($300), system automatycznie przełączy się na darmowe modele NIM (np. Llama 3 / Mistral), aby aplikacja Streamlit działała bez przerwy i bez opłat.
