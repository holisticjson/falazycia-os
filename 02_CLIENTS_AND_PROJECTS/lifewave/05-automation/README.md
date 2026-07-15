# ⚙️ 05-automation — Schematy Automatyzacji i CRM

Katalog przeznaczony na schematy automatyzacji n8n, konfigurację webhooków, integracje z Systeme.io oraz skrypty przesyłu danych leadów do CRM.

---

## 🤖 Schemat Przepływu n8n (Blueprints)
Zautomatyzowany lejek rekrutacyjny MLM będzie sterowany przez centralną instancję n8n:

1.  **Zdarzenie Wyzwalające (Trigger):** Nowy zapis na landing page'u w Systeme.io (nowy kontakt z tagiem `LifeWave_Leads`).
2.  **Akcja 1 (Segmentacja & Scoring):** Przesłanie danych przez Webhook do n8n, który analizuje odpowiedzi z ankiety kwalifikacyjnej:
    -   Jeśli lead zaznaczy: *Chcę kupić produkty* ➔ Przypisz tag `LifeWave_Product` w Systeme.io i wyślij automatyczną ofertę zakupu.
    -   Jeśli lead zaznaczy: *Interesuje mnie zarabianie/MLM* ➔ Przypisz tag `LifeWave_Business`, n8n automatycznie wyśle link do rezerwacji spotkania w kalendarzu.
3.  **Akcja 2 (Wzbogacenie Wiedzą AI):** n8n może wywołać prompt do modelu Gemini, by wygenerował spersonalizowany, krótki e-mail powitalny dopasowany do odpowiedzi z ankiety leada, opierając się na profilu Ghostwritera Tomasza.

---

> [!IMPORTANT]
> **Zasada Low-Cost:** Do zarządzania kontaktami i wysyłki maili wykorzystujemy wyłącznie darmowy plan Systeme.io (limit 2000 kontaktów). Rozwiązuje to całkowicie problemy z dostarczalnością wiadomości, SPF, DKIM oraz chroni domeny główne przed banami antyspamowymi.
