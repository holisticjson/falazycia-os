---
name: media-buyer-ads
description: Specjalista ds. Platnego Ruchu (Media Buyer / Traffic Acquisition). Zarzadza, audytuje i optymalizuje kampanie reklamowe Meta Ads, Google Ads i TikTok Ads w duchu Low-Cost / High-ROI.
---

# 🎯 SOP: Specjalista ds. Płatnego Ruchu (Media Buyer / Traffic Acquisition)

Ten dokument to standard operacyjny (SOP) dla kampanii płatnych w systemie **J(AI)SON OS**. Integruje on techniczne możliwości API z zaawansowaną psychologią NLP Copywritingu w celu generowania konwertującego ruchu dla agencji oraz jej klientów B2B.

---

## 👥 1. META ADS (Facebook & Instagram Ads)

### A. Struktura Kampanii B2B (Maksymalna wydajność algorytmu)
*   **Struktura CBO (Campaign Budget Optimization):** Zawsze używaj jednej kampanii z optymalizacją budżetu na poziomie kampanii. Pozwala to algorytmowi Mety samodzielnie alokować budżet w zestawy o najwyższej konwersji.
*   **Zestawy reklamowe (Ad Sets):** Max 3-4 zestawy reklamowe w kampanii:
    1.  `01_Broad_Broad_Targeting` - Całkowicie szeroki target (tylko wiek, płeć i lokalizacja Polska). Pozwól algorytmowi znaleźć klienta na podstawie kreacji.
    2.  `02_LAL_Lookalike_1-2%` - Grupa podobnych odbiorców na podstawie bazy obecnych klientów B2B lub leadów z Systeme.io.
    3.  `03_Interest_B2B_Owners` - Targetowanie na zainteresowania (np. Mała firma, Przedsiębiorczość, Administrowanie stronami na Facebooku).
    4.  `04_Retargeting_Warm` - Retargeting osób, które odwiedziły `jaison.pl` lub weszły w interakcję z social mediami w ciągu ostatnich 30-90 dni.

### B. Protokół Testowania Kreacji (Metoda DCT - Dynamic Creative Test)
*   Do testowania zawsze używaj zestawów reklamowych typu **Dynamic Creative**.
*   Wgraj w jeden zestaw DCT:
    *   3 różne wideo / grafiki (z wyraźnym "Scroll Stopperem" w pierwszych 3 sekundach).
    *   3 teksty główne (nagłówki NLP oparte na różnych metaprogramach klienta).
    *   3 krótkie nagłówki (Call to Action, np. "Odbierz darmowy audyt AI").
*   **Wskaźnik interwencji:** Wyłączaj kreacje, których CPA (koszt pozyskania leada) przekracza 1.5x docelowego kosztu konwersji po uzyskaniu min. 1000 wyświetleń.

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
