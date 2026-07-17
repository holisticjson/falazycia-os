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

## 🔍 2. GOOGLE ADS (Search & Performance Max) — Strategia Uśmierzania Bólu

### A. Kampanie w sieci wyszukiwania (Google Search) jako Detektor "Problemu TERAZ"
Wyszukiwarka Google to najdokładniejszy na świecie barometr natychmiastowego bólu klienta. Wykorzystaj to:
*   **Słowa kluczowe "Problemu TERAZ":** Koncentruj się na frazach o wysokiej intencji zakupowej oraz bezpośrednio opisujących bieżący ból z obecnej sekundy (np. `"jak zautomatyzować fakturowanie"`, `"narzędzie do automatycznego odpisywania klientom"`). Używaj wyłącznie **Dopasowania Ścisłego (Exact Match)** i **Dopasowania do Wyrażenia (Phrase Match)** (np. `[automatyzacja biura bez programisty]`).
*   **Kategoryczny zakaz:** Nie używaj dopasowania przybliżonego (Broad Match) bez podpiętej rygorystycznej listy wykluczających słów kluczowych (Negative Keywords). Zapobiega to przepalaniu budżetu na zapytania ogólne (np. "co to jest ai").
*   **Nagłówki oparte na Prawie 97%:** Nagłówki reklam muszą bezlitośnie uderzać w eliminację kompromisu i wysiłku energetycznego, którego klient boi się u konkurencji (np. *"Automatyzuj Bez Kodowania"*, *"Agencja AI bez stałych opłat i bez zatrudniania programistów"*).

### B. Kampanie Performance Max (PMax) B2B & Proces Ewaluacji
*   **Zabezpieczenie budżetu (Brand Safety):** Zawsze wykluczaj słowa kluczowe związane z własną marką (`Jaison`, `Jaison Agency`) z kampanii PMax, by nie przypisywać zasług płatnym kampaniom za ruch organiczny.
*   **Kierowanie na Proces Ewaluacji:** Assety wizualne i tekstowe w PMax muszą kierować ruch na strony zawierające silne, surowe uwiarygodnienie zewnętrzne (artykuły z recenzjami, surowe wideo od Tomasza, autentyczne case studies), ponieważ odbiorcy z PMax przechodzą przez min. 7-dniowy proces porównywania nas z rynkiem.

---

## 🎵 3. TIKTOK ADS (Lead Generation) — Emocje i Ruch Mobilny

*   **UGC z 18 Kątów Emocjonalnych:** Wideo UGC na TikToku nie może być zwykłą prezentacją funkcji. Pisz skrypty wideo, wybierając jedną emocję z kryteriów rynku (np. złość na marnowanie czasu) i ubieraj ją w 18 dynamicznych kątów (np. *Red Flags*, *Contrarian*, *Before/After*, *Comparative*). Wideo ma wyglądać jak surowy, autentyczny, niemontowany u profesjonalisty post.
*   **Formularze błyskawiczne (Instant Forms):** Używaj formularzy z opcją "Wyższa intencja" (dodatkowy krok weryfikacji), aby odsiać przypadkowe kliknięcia.
*   **Standard 3-5 Scrolli na Mobile:** Ponieważ TikTok generuje w 100% ruch mobilny, landing page powiązany z reklamą musi być perfekcyjnie zoptymalizowany pod telefony. Pierwsze **3-5 swipe'ów (scrolli) w dół** muszą bezlitośnie dostarczyć tożsamość obietnicy z reklamy.

---

## 📊 4. RAPORTOWANIE, METRYKI I KOORDYNACJA (Liaison CFO/CMO/Clarity)

Dane z API są automatycznie pobierane do Streamlit za pomocą n8n w celu wyliczenia twardych wskaźników finansowych i jakościowych:

### A. Metryki Finansowe (Standard CFO/CMO)
1.  **CAC (Customer Acquisition Cost):** Rzeczywisty koszt pozyskania jednego płacącego klienta.
2.  **CPL (Cost Per Lead):** Koszt pozyskania jednego zapytania/e-maila.
3.  **ROAS (Return on Ad Spend):** Przychód z kampanii podzielony przez koszty reklamowe.
4.  **MER (Marketing Efficiency Ratio):** Całkowity przychód agencji podzielony przez całkowity budżet marketingowy (organiczny + płatny). Zdrowy MER dla agencji B2B to min. **4x - 6x**.

### B. Metryki Jakościowe Ruchu Mobilnego (Standard Clarity)
*   **mCR (Mobile Conversion Rate):** Współczynnik konwersji wyłącznie dla użytkowników telefonów.
*   **Mobile Bounce/Swipe Ratio:** Procent użytkowników mobilnych opuszczających stronę przed wykonaniem min. 3 scrolli w dół. 
    *   *Interpretacja:* Jeśli ten wskaźnik przekracza 50%, oznacza to drastyczny **Misfit** (brak dopasowania) między emocjonalną obietnicą z kreacji reklamowej a pierwszym widokiem (hero section) na telefonie. Media Buyer musi wtedy natychmiast skorygować kreację lub skonsultować z CMO przebudowę pierwszego widoku mobilnego strony.
