# 🎯 Plan Wdrożenia Marketingu, Analityki & Integracji Composio (Holistic 2.0)
*Strategia "Low-Cost First" i "Low-Friction" dla platformy Streamlit i Hermesa*

---

> [!IMPORTANT]
> **Zasada nadrzędna:** Maksymalizujemy darmowe plany (Free Tiers), unikamy abonamentów na start i nie budujemy własnych systemów mailingowych od zera. Do lejków i e-mail marketingu wykorzystujemy **Systeme.io (darmowy plan do 2000 kontaktów)**.

---

## 🗺️ Architektura Przepływu Danych Marketingowych
Poniższy diagram przedstawia, jak dane o ruchu, leadach i płatnościach krążą bezszumnie między platformami, lejkami i agentami AI (Streamlit + Hermes).

```mermaid
graph TD
    %% Ruch i Reklamy
    User([Odwiedzający]) -->|Kliknięcie| Ads[Google / Meta / TikTok Ads]
    User -->|Wyszukiwanie organiczne| GSC[Google Search Console]
    
    %% Strona i Analityka
    User -->|Interakcja ze Streamlit / Landing Page| GTM[Google Tag Manager]
    GTM -->|Zdarzenia| GA4[Google Analytics 4]
    GTM -->|Piksele śledzące| Pixels[Pixels: Meta & TikTok]
    GTM -->|Analityka produktowa| PostHog[PostHog (1M darmowych zdarzeń)]
    
    %% Lejek i Płatności
    User -->|Zapis na newsletter / Zakup| SIO[Systeme.io (Lejek B2B)]
    SIO -->|Procesor płatności| Stripe[Stripe (Płatności)]
    
    %% Orkiestracja AI (Composio)
    Stripe -->|Webhook| Composio[Composio (OAuth & API Broker)]
    PostHog -->|Wyzwalacz| Composio
    Composio -->|Akcje i Dane| Hermes[Hermes Agentic OS]
    Composio -->|Zapis i Powiadomienia| Sheets[Google Sheets]
    Composio -->|Powiadomienia| Slack[Slack / Telegram Bot]
    
    classDef free fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef paid fill:#f8d7da,stroke:#dc3545,stroke-width:1px;
    class SIO,PostHog,GSC,Sheets,Slack,Composio,Stripe free;
    class Ads paid;
```

---

## 🛠️ KROK 1: Checklisty Uruchomienia i Konfiguracji Marketingu

Szybkie, "bezszumne" checklisty krok-po-kroku do wyklikania w panelach. Wszystkie kody śledzące i piksele instalujemy **wyłącznie przez Google Tag Manager (GTM)**, aby nie zaśmiecać kodu aplikacji Streamlit.

### 1. Ekosystem Google (GA4, GTM, GSC, YouTube, Google Ads)
Mózg analityczny Twojego ekosystemu. Wszystko połączone pod jednym kontem Google agencji (`holisticjson@gmail.com`).

*   [ ] **Google Tag Manager (GTM):**
    *   Załóż darmowe konto na [tagmanager.google.com](https://tagmanager.google.com).
    *   Stwórz kontener typu **Web**.
    *   *Integracja ze Streamlit:* Wklej wygenerowany skrypt GTM do sekcji `<head>` i `<body>` szablonu Streamlita (lub użyj natywnego komponentu HTML w Streamlit).
*   [ ] **Google Analytics 4 (GA4):**
    *   Załóż usługę GA4 na [analytics.google.com](https://analytics.google.com).
    *   Utwórz **Strumień Danych (Data Stream)** dla swojej domeny.
    *   Połącz GA4 z GTM za pomocą tagu *Google Tag* (użyj ID pomiaru `G-XXXXXXXXXX`).
    *   Włącz **Enhanced Measurement** (automatyczne śledzenie przewinięć, kliknięć wychodzących i wyszukiwań).
*   [ ] **Google Search Console (GSC):**
    *   Dodaj swoją domenę na [search.google.com/search-console](https://search.google.com/search-console).
    *   *Low-Friction weryfikacja:* Wybierz weryfikację przez **Google Analytics** lub dodaj rekord TXT w konfiguracji DNS u swojego dostawcy domeny.
    *   Prześlij plik `sitemap.xml` po uruchomieniu landing page'a.
*   [ ] **YouTube & YouTube Analytics:**
    *   Upewnij się, że kanał YouTube jest powiązany z głównym kontem Google agencji.
    *   Włącz dostęp do **YouTube Data API v3** w Google Cloud Console (niezbędne, aby Hermes mógł pobierać statystyki wideo i komentarze bez scrapowania).
*   [ ] **Google Ads:**
    *   Załóż konto na [ads.google.com](https://ads.google.com) (wybierz "Tryb Eksperta", aby uniknąć automatycznych, drogich kampanii Smart).
    *   Połącz konto Google Ads z GA4 (zakładka *Połączone konta*), aby automatycznie importować konwersje.

---

### 2. Ekosystem Meta (Ads Manager, Instagram, Facebook Pixel)
Główny silnik płatnego ruchu B2B i budowania wizerunku.

*   [ ] **Meta Business Suite:**
    *   Załóż darmowe konto biznesowe na [business.facebook.com](https://business.facebook.com).
    *   Podepnij pod konto swój Fanpage na Facebooku oraz profesjonalne konto na Instagramie.
*   [ ] **Meta Pixel (Dataset):**
    *   Przejdź do *Menedżera zdarzeń (Events Manager)* -> *Połącz źródła danych* -> *Internet*.
    *   Stwórz nowy Pixel i skopiuj jego **Pixel ID**.
    *   Zainstaluj go w **GTM** za pomocą gotowego szablonu z Galerii Społeczności GTM (*Meta Pixel by facebookarchive*).
*   [ ] **Weryfikacja Domeny i RODO:**
    *   Zweryfikuj domenę w ustawieniach firmy Meta (wymóg po aktualizacji iOS 14).
    *   Ustaw priorytetowe zdarzenia konwersji (np. `Lead`, `CompleteRegistration`).

---

### 3. Ekosystem TikTok (TikTok Ads, Pixel, Creator Marketplace)
Dźwignia do wiralowego zasięgu organicznego i taniego ruchu z reklam wideo.

*   [ ] **TikTok Ads Manager:**
    *   Załóż konto reklamowe na [ads.tiktok.com](https://ads.tiktok.com).
*   [ ] **TikTok Pixel:**
    *   W sekcji *Assets* -> *Events* stwórz Web Pixel.
    *   Wybierz konfigurację przez **GTM** (TikTok posiada oficjalny tag integracyjny w GTM, instalacja zajmuje 2 minuty).
*   [ ] **TikTok Creator Marketplace (TCM):**
    *   Zarejestruj się jako marka/agencja na [creatormarketplace.tiktok.com](https://creatormarketplace.tiktok.com).
    *   Daje to darmowy dostęp do bazy twórców i zaawansowanych statystyk trendów bez opłat abonamentowych.

---

### 4. Stripe + Systeme.io (Monetyzacja i Lejki)
Zapewnienie dopływu gotówki przy zerowych kosztach stałych.

*   [ ] **Konto Stripe:**
    *   Zarejestruj się na [stripe.com](https://stripe.com).
    *   Przejdź pełną weryfikację firmy (wprowadź dane działalności i konto bankowe do wypłat).
    *   Uruchom tryb **Test Mode** (będziesz go używać do bezpiecznego testowania integracji z agentami).
*   [ ] **Integracja ze Systeme.io (Lejek MVP):**
    *   W panelu Systeme.io przejdź do: *Ustawienia* -> *Bramki płatności*.
    *   Kliknij *Połącz ze Stripe* (autoryzacja OAuth jednym kliknięciem - 100% bezpieczna).
*   [ ] **Strategia "Jednego Taga" w Systeme.io:**
    *   Zgodnie z instrukcją `ckm:systeme-io-integration`, stwórz w Systeme.io **tylko jeden tag**: `holistic-contact`.
    *   Rozróżnienie statusów (np. czy to lead z darmowego webinaru, czy płatny klient) zapisuj w **polach niestandardowych (Custom Fields)** za pomocą reguł automatyzacji w Systeme.io lub przez API.

---

## 📊 KROK 2: Analiza Integracji Composio — Darmowy Przegląd Rozwiązań

Composio to potężny broker integracyjny dla agentów AI. Posiada hojny plan darmowy dla deweloperów (Developer Free Tier), który daje **darmowe wywołania akcji** miesięcznie oraz automatyczną, darmową obsługę sesji autoryzacji OAuth. 

Poniższa tabela analizuje przydatność i darmowość integracji z listy narzędzi użytkownika pod kątem ekosystemu **Streamlit + Hermes**:

| Narzędzie | Darmowe API / Free Tier? | Integracja z Composio | Ocena i Zastosowanie w MVP |
| :--- | :--- | :--- | :--- |
| **PostHog** | **TAK** (Bardzo hojny: **1M zdarzeń/mc** + nagrania sesji za darmo!) | ✅ Dostępna | **Kluczowa (Must Have)**. Daje pełną analitykę zachowań w Streamlicie i nagrywanie sesji bez płacenia za Hotjar. |
| **Stripe** | **TAK** (Środowisko testowe 100% darmowe. Produkcja: prowizja % od obrotu). | ✅ Dostępna | **Kluczowa**. Hermes może automatycznie sprawdzać status subskrypcji i generować raporty finansowe. |
| **Google Sheets / Docs / Calendar** | **TAK** (Darmowe API z gigantycznymi limitami na kontach osobistych). | ✅ Dostępna | **Kluczowa**. Służy jako darmowa, asynchroniczna baza danych i harmonogram zadań agencji. |
| **Slack / Discord** | **TAK** (Darmowe tworzenie botów i kanałów komunikacji). | ✅ Dostępna | **Kluczowa**. Natychmiastowe powiadomienia o leadach i płatnościach wysyłane przez agenta AI. |
| **GitHub** | **TAK** (Darmowe API dla kont osobistych/organizacji). | ✅ Dostępna | **Kluczowa dla CTO/Hermesa**. Umożliwia agentowi pobieranie kodu, śledzenie wydań i automatyczny deploy. |
| **Gmail** | **TAK** (Wysokie darmowe limity API dla kont osobistych). | ✅ Dostępna | **Wysoka**. Umożliwia agentowi automatyczne wysyłanie spersonalizowanych e-maili i czytanie odpowiedzi. |
| **Notion** | **TAK** (Darmowy plan dla użytkowników indywidualnych i darmowe API). | ✅ Dostępna | **Średnia**. Przydatne do synchronizacji bazy wiedzy, ale Obsidian w lokalnym workspace jest szybszy i bezszumny. |
| **HubSpot** | **TAK** (Darmowy podstawowy CRM, darmowe limity API dewelopera). | ✅ Dostępna | **Średnia**. HubSpot bywa przytłaczający (brak ADHD-friendly). Sheets lub lokalna baza SQLite są prostsze na start. |
| **Meta Ads / Google Ads** | **TAK** (Dostęp do API raportowego i deweloperskiego jest darmowy). | ✅ Dostępna | **Średnia**. Przydatne do automatycznego raportowania kosztów reklam przez agenta, ale wymaga dłuższego setupu API. |
| **Obsidian** | **TAK** (Narzędzie lokalne na plikach Markdown). | ❌ Brak w chmurze | **Lokalny standard**. Synchronizację bazy wiedzy Obsidiana robimy lokalnie w workspace (mamy już gotowy MCP do Obsidiana!). |
| **SendGrid** | **NIE** (Tylko 100 e-maili dziennie w darmowym planie). | ✅ Dostępna | **Niska**. Kategorycznie unikamy! Do wysyłki e-maili i newsletterów używamy darmowego **Systeme.io**. |
| **Pipedrive** | **NIE** (Brak darmowego planu, tylko 14-dniowy trial). | ✅ Dostępna | **Wykluczone (High-Cost)**. Przeciwne zasadzie "Low-Cost First". |

---

## ⚡ KROK 3: Rekomendacja "Essential Minimum" dla Hermesa i Streamlita

Aby uruchomić agencję w 1 dzień z zerowymi kosztami licencyjnymi i maksymalną dźwignią AI, wdrażamy minimalistyczny zestaw integracji. Ten zestaw pozwala Hermesowi na autonomiczną pracę bez przebodźcowania użytkownika.

### Minimalistyczny Stos Integracyjny MVP:
```
[Streamlit App] + [Hermes OS] 
       │
       ├─► PostHog (Śledzenie UX, kliknięć i sesji w Streamlicie — za darmo do 1M zdarzeń)
       ├─► Google Sheets (Asynchroniczny CRM, raportowanie leadów i finansów)
       ├─► Slack / Discord (Centrum powiadomień operacyjnych: "Nowy Lead!", "Płatność OK")
       └─► Stripe Sandbox (Testowanie pełnego procesu transakcyjnego)
```

### Dlaczego ten zestaw to strzał w dziesiątkę?
1.  **Zero Opłat Stałych:** Wszystkie te narzędzia mają potężne, darmowe plany, które wystarczą na pierwsze kilka tysięcy użytkowników i leadów.
2.  **Brak Skomplikowanego Kodu:** Dzięki Composio, autoryzacja OAuth do Google Sheets i Slacka odbywa się za pomocą kilku kliknięć w przeglądarce, a agent dostaje gotowe narzędzia (Tools) do odczytu/zapisu.
3.  **Maksymalna Widoczność (PostHog):** Widzisz dokładnie, co użytkownicy robią w Twojej aplikacji Streamlit, dzięki darmowym nagraniom wideo z ich sesji.

---

## 📅 KROK 4: Harmonogram Wdrożenia (Action Plan)

> [!TIP]
> Wykonuj kroki sekwencyjnie. Nie rozpraszaj się – jeden krok na raz zapewnia szybkie wdrożenie bez zmęczenia decyzyjnego.

### Faza 1: Fundamenty (Dzień 1 - Szacowany czas: 2h)
*   [ ] Załóż brakujące konta (GTM, GA4, GSC, Stripe, PostHog, Systeme.io, Composio).
*   [ ] Skonfiguruj **Google Tag Manager** i podepnij pod niego **GA4** oraz **PostHog**.
*   [ ] Podepnij Stripe pod Systeme.io.

### Faza 2: Integracje Composio & API (Dzień 2 - Szacowany czas: 2h)
*   [ ] Połącz Google Sheets w Composio (autoryzacja OAuth). Stwórz arkusz `Holistic_Leads_CRM`.
*   [ ] Połącz Slack/Discord w Composio, aby Hermes mógł wysyłać powiadomienia na dedykowany kanał `#alerts-marketing`.
*   [ ] Przetestuj integrację Stripe Sandbox i upewnij się, że płatności testowe działają poprawnie.

### Faza 3: Uruchomienie & Test (Dzień 3 - Szacowany czas: 1h)
*   [ ] Wykonaj testowy zapis na landing page'u (Systeme.io) i upewnij się, że dane trafiają do Systeme.io z tagiem `holistic-contact`.
*   [ ] Przetestuj działanie agenta Hermesa – poproś go o odczytanie nowych leadów z Google Sheets i wysłanie podsumowania na Slacka.

---
*Plan przygotowany przez marketing_integrator — Agencja AI Holistic Jason. Wdrażaj krok po kroku i ciesz się automatyzacją!*
