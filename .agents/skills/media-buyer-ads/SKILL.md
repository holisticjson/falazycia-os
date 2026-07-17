---
name: media-buyer-ads
description: Specjalista ds. Platnego Ruchu (Media Buyer / Traffic Acquisition). Zarzadza, audytuje i optymalizuje kampanie reklamowe Meta Ads, Google Ads i TikTok Ads w duchu Low-Cost / High-ROI.
---

# 🎯 SOP: Specjalista ds. Płatnego Ruchu (Media Buyer / Traffic Acquisition)

Ten dokument to standard operacyjny (SOP) dla kampanii płatnych w systemie **J(AI)SON OS**. Integruje on techniczne możliwości API z zaawansowaną psychologią NLP Copywritingu w celu generowania konwertującego ruchu dla agencji oraz jej klientów B2B.

---

## 👥 1. META ADS (Facebook & Instagram Ads) — Standard "Andromeda"

### A. Struktura Kampanii i Alokacja Budżetów (CBO vs ABO)
Algorytm **Andromeda** wymusza ścisłe dostosowanie struktury kampanii do wielkości dziennego budżetu:

*   **Budżety Wysokie (Powyżej 1000 zł / dzień) ➔ Obowiązkowo CBO (Campaign Budget Optimization):**
    *   CBO przy wysokich budżetach działa jako "maszynka do drukowania gotówki" (ROAS rzędu 3x - 4x). Optymalnie działa od min. 30 kreacji reklamowych.
    *   **Zasada Zestawów Reklamowych (Ad Sets):**
        *   **Grafiki/Obrazki:** Wrzucaj w 1 zestaw reklamowy dokładnie **4 grafiki reklamowe** powiązane z 1 grupą docelową (np. `01_Broad`). Algorytm zacznie samodzielnie żonglować grafikami i dobierać odpowiedni obrazek pod odpowiedniego odbiorcę.
        *   W kolejnym zestawie (np. `02_LAL`) dajesz kolejne 4 grafiki.
        *   **Wideo:** Zawsze wrzucaj wideo w osobnym, dedykowanym zestawie reklamowym (1 zestaw = wideo).
    *   **Struktura Lejka CBO:** Dobrze, aby w kampanii CBO ruch był kierowany na 3 typy stron:
        1.  `PDP` - Strona z produktem / ofertą.
        2.  `Wpis blogowy (Advertorial)` - Edukacyjny artykuł.
        3.  `VSL Page` - Strona z wideo sprzedażowym (Video Sales Letter).
        *   *Test:* Kierowanie "Od razu do koszyka" + remarketing porzuconych koszyków.

*   **Budżety Niskie (Poniżej 1000 zł / dzień) ➔ Obowiązkowo ABO (Ad Set Budget Optimization):**
    *   CBO bardzo słabo sobie radzi na małych budżetach. 
    *   Stosuj strukturę: **1 zestaw reklamowy + 1 reklama** (grafika lub wideo) + budżet dzienny przypisany do zestawu.

### B. Hipotezy Emocjonalne i Targetowanie (Kryteria Rynku)
Zamiast strzelać na oślep w grupy docelowe i liczyć na łut szczęścia algorytmu, buduj kampanie na twardych hipotezach emocjonalnych:
1.  **Wybór Emocji:** Wybierz jedną dominującą emocję z kryteriów rynku (np. "złość", "frustracja", "lęk", "chęć ulgi").
2.  **Mapowanie na Niszę:** Zmapuj emocję na swój ICP (np. Nisza: Mamy ➔ Target: *Wkurzone Mamy*).
3.  **Kreacja i Nagłówek:** Nagłówek musi bezpośrednio odzwierciedlać tę emocję, np.: *"Oto sposób na XYZ, które wkurzone Mamy zastosowały, aby ich Dziecko zaczęło zdobywać lepsze oceny w szkole, nawet jeżeli próbowały już wszystkiego. Szybka 7-minutowa strategia."*
4.  **Protokół Testowy:** Zainwestuj 100-200 zł na test wybranej emocji. Zbierz dane i przeanalizuj nagrania sesji użytkowników w **Microsoft Clarity** (pod kątem mobile).
5.  **Decyzja:** Skaluj zwycięską emocję lub zmień hipotezę na inną emocję.

### C. Protokół Prostej Obsługi i Skalowania
*   **No target (Szeroko):** Ustaw targetowanie szerokie ➔ Budżet: **50% kosztu produktu** na zestaw reklamowy dziennie.
*   **Rotacja:** Puszczaj 5 reklam obrazkowych dziennie. Codziennie bezlitośnie wyłączaj to, co nie sprzedało.
*   **Wideo:** Kreacje wideo trzymaj i testuj przez 2-3 dni przed podjęciem decyzji o wyłączeniu.
*   **Skalowanie:** Zwycięskie zestawy skaluj co 2-3 dni, podnosząc budżet o **100%**.
*   **AI Ads Automation:** Wykorzystuj systemy AI (Claude + Higgsfield.ai + Meta MCP) do masowej generacji obrazków i wideo (Duży Angle + Duży Wolumen = Duży Ruch).

### D. Standard Mobile-First (Konwersja 80%)
*   Pamiętaj, że ponad 80% ruchu zakupowego pochodzi z urządzeń mobilnych (telefony).
*   Główny nacisk optymalizacji kieruj na to, jak strona wygląda i ładuje się na telefonach. Kluczowe dla konwersji są pierwsze **3 do 5 swipe’ów (scrolli) w dół**! Sprawdzaj zachowania użytkowników na Clarity pod tym kątem.

---

## 🔍 2. GOOGLE ADS (Search & Performance Max)

### A. Kampanie w sieci wyszukiwania (Google Search)
*   **Słowa kluczowe:** Używaj wyłącznie **Dopasowania Ścisłego (Exact Match)** i **Dopasowania do Wyrażenia (Phrase Match)** dla fraz o wysokiej intencji zakupowej B2B (np. `[automatyzacje procesów biznesowych]`, `"agencja ai warszawa"`).
*   **Kategoryczny zakaz:** Nie używaj dopasowania przybliżonego (Broad Match) bez podpiętej zaawansowanej listy wykluczających słów kluczowych (Negative Keywords). Zapobiega to przepalaniu budżetu na frazy typu "co to jest ai" lub "darmowe automatyzacje".
*   **Strategia ustalania stawek:** Rozpocznij od *Maksymalizuj liczbę kliknięć* (w celu zebrania pierwszych danych), a po uzyskaniu min. 15-30 konwersji przejdź na *Maksymalizuj liczbę konwersji (tCPA)*.

### B. Kampanie Performance Max (PMax) B2B
*   **Zabezpieczenie budżetu (Brand Safety):** Zawsze wykluczaj słowa kluczowe związane z własną marką (`Jaison`, `Jaison Agency`) z kampanii PMax. Pozwala to uniknąć sytuacji, w której Google przypisuje kampanii płatnej konwersje, które i tak wpadłyby organicznie.
*   **Sygnały dotyczące odbiorców (Audience Signals):** Jako sygnał wejściowy dla PMax wgraj bazę e-mailową zebraną z Systeme.io oraz ruch z Twojej witryny.

---

## 🎵 3. TIKTOK ADS (Lead Generation)

*   **Format:** Wykorzystuj wyłącznie formaty pionowe (9:16) oparte na trendach UGC (User Generated Content) – wideo ma wyglądać jak naturalny post na TikToku, a nie jak profesjonalna reklama telewizyjna.
*   **Formularze błyskawiczne (Instant Forms):** Używaj wbudowanych formularzy TikToka z opcją "Wyższa intencja" (dodatkowy krok weryfikacji danych przez klienta przed wysłaniem), aby odsiać przypadkowe kliknięcia dzieci i nastolatków.
*   **Integracja n8n:** Każdy lead z TikToka musi w czasie rzeczywistym wpadać przez webhook n8n bezpośrednio do Systeme.io i bazy danych!

---

## 📊 4. RAPORTOWANIE, METRYKI I KOORDYNACJA (Liaison CFO/CMO)

Wszystkie kampanie płatne są audytowane pod kątem twardych wskaźników finansowych. Dane z API Mety i Google Ads są pobierane przez n8n do Twojego dashboardu Streamlit w celu wyliczenia:

1.  **CAC (Customer Acquisition Cost):** Rzeczywisty koszt pozyskania jednego płacącego klienta agencji.
2.  **CPL (Cost Per Lead):** Koszt pozyskania jednego zapytania/e-maila.
3.  **ROAS (Return on Ad Spend):** Przychód wygenerowany z kampanii podzielony przez koszty reklamowe.
4.  **MER (Marketing Efficiency Ratio):** Całkowity przychód agencji podzielony przez całkowity budżet marketingowy (organiczny + płatny). Zdrowy wskaźnik MER dla agencji B2B to min. **4x - 6x**.
