# 🥩 ROAST PROPOZYCJI YOUTUBE & MULTI-PROFILE CONTENT AUTOPILOT (JAISON OS)

---

## 🥩 1. Roast Propozycji YouTube & Social Media Automation

> [!WARNING] ZAUWAŻONE DZIURY LOGICZNE, FIKCYJNE ZAŁOŻENIA API & MIT CHMURY:
> 1. **Fikcja Tworzenia Kanałów YouTube przez API (Brak `createChannel`):**  
>    Oficjalny brak metody w YouTube Data API v3 uniemożliwia programistyczne tworzenie nowych kanałów YouTube. Użytkownik musi wykonać 1-razowe kliknięcie w panelu `m.youtube.com/create_channel`, dopiero po czym agent obejmuje 100% kontroli nad brandingiem i uploadem.
> 2. **Zastąpienie Numerów Telefonicznych Bezpośrednim WhatsAppem & Discordem (Low-Friction):**  
>    Podawanie surowego numeru telefonu w botach czatowych generuje tarcie. Przepięcie CTAs bezpośrednio na bezpłatny link **WhatsApp Direct (`https://wa.me/48791636644`)** lub **Discord (`#agency-leads`)** natychmiast konwertuje ruch.
> 3. **Skalowalność na Wielu Profilach Klienckich (Multi-Tenant Pipeline):**  
>    Ręczne ustawianie kanałów dla każdego klienta (Jaison Agency, Fala Życia, Coolphon, Barjaś, Holistyczny Broker) to pułapka czasowa. Wymagana jest jednolita tabela **`ContentJobs`** sterująca autonomicznie blogiem i social mediami dla wszystkich marek z jednego miejsca!

---

## 🛠️ 2. Zintegrowana Architektura Autopilota Treści & SEO (AEO Engine)

```mermaid
graph TD
    subgraph 🕵️ RESEARCHER VIRALNY (Trend Scraper Agent)
        A1["🔍 Firecrawl / YouTube / Reddit / Facebook Scraper"] --> A2["🧠 Gemini Flash Filter (Wykrycie Hot-Topiców)"]
    end

    subgraph 📂 BAZA DANYCH CONTENTJOBS (Single Source of Truth)
        B1["📋 Tabela ContentJobs (SQLite / GCS / Sheets)"]
        B2["🎛️ Tryby Autopilota: Manual / Semi-Auto / Full-Autopilot"]
    end

    subgraph 🚀 WYDAWNICTWO MULTI-PROFILE (Multi-Tenant Engine)
        C1["🏢 Jaison Agency B2B"] --- C2["🌿 Fala Życia MLM"] --- C3["📱 Coolphon Service"] --- C4["🍗 Barjaś"]
        C1 & C2 & C3 & C4 --> D1["🌐 Blog WWW (Generowanie Artykułów SEO/AEO)"]
        C1 & C2 & C3 & C4 --> D2["📲 Social Media (Composio MCP / TikTok MCP)"]
    end

    A2 --> B1 --> C1
```

---

## 🎛️ 3. Tryby Autopilota Publikacji (Model Smart Routing)

1. **`MANUAL_REVIEW` (Dla Własnych MarekWysokiego Ryzyka - Jaison Agency B2B):**  
   Każdy artykuł i wideo przechodzi akceptację Tomasza na Telegramie / Discordzie 1-kliknięciem.
2. **`SEMI_AUTONOMOUS` (Paczki Tygodniowe):**  
   Agent przygotowuje 7-dniową paczkę postów i shortów. Tomasz klika "Approve Batch" raz w tygodniu.
3. **`FULL_AUTOPILOT` (Faceless Kanały Niszowe & Posty Blogowe SEO/AEO):**  
   Agent autonomicznie generuje skrypty, grafiki, posty blogowe i publikuje je bezpośrednio przez API/Composio.
