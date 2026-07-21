# 🎵 Szablon Rebrandingu: TikTok Profile

Ten dokument to szablon wdrożeniowy konfiguracji profesjonalnego profilu na TikToku (konto biznesowe / twórcy) dla marki **{{BRAND_NAME}}**.

---

## 🛠️ KROK 1: Podstawowa Identyfikacja Konta
1.  **Nazwa Użytkownika (Username):** Unikalny identyfikator bez spacji (np. `@{{BRAND_HANDLE}}` lub `@{{OWNER_HANDLE}}`).
2.  **Nazwa Profilu (Name):** Wyświetlana tłustym drukiem u góry (Max 30 znaków):
    > `{{TIKTOK_DISPLAY_NAME}}` (np. `{{OWNER_NAME}} | AI Architect`)

---

## 📸 KROK 2: Wizualia Profilu (Avatar i Styl Wideo)

### 👤 A. Zdjęcie Profilowe (Avatar)
*   **Format:** `1:1` (Kwadrat, przycinany do koła).
*   **Silnik:** `{{AVATAR_ENGINE}}`
*   **Zasada:** Ponieważ TikTok to platforma dynamiczna i wideo, Twój awatar musi przyciągać wzrok. Może być nieco bardziej dynamiczny lub ukazywać postać w akcji / w futurystycznym techwear ułatwiającym zapamiętanie.
*   **Prompt do wygenerowania:**
    > `{{TIKTOK_AVATAR_PROMPT}}`

---

## ✍️ KROK 3: Pozycjonowanie i Treść (TikTok Bio)

> [!IMPORTANT]
> **Sztywny limit Bio na TikToku wynosi zaledwie 80 znaków ze spacjami!** Musisz zmieścić całą esencję marki i wezwanie do działania w jednym, genialnym zdaniu. Nie ma miejsca na ozdobniki.

*Skopiuj wygenerowany krótki tekst i wklej do sekcji Opis:*

```text
{{TIKTOK_BIO_TEXT}}
```

*   **Link w profilu (Website Link):** `{{WEBSITE_URL}}` (Uwaga: funkcja aktywnego linku w profilu na TikToku wymaga konta biznesowego lub zebrania minimum 1000 obserwujących. Jeśli nie masz aktywnego linku, napisz go jako zwykły tekst w Bio lub skieruj ruch na Instagram/YouTube).

---

## 📹 KROK 4: Struktura i Format Wideo (TikTok Grid)
TikTok to platforma w 100% oparta na pionowym formacie wideo (`9:16` / `1080x1920 px`).
*   **Haczyk (Hook):** Każde wideo musi mieć mocny wizualny lub tekstowy hook w pierwszych **1.5 do 2 sekundach** filmu.
*   **Okładki filmów (Video Covers):** Używaj spójnego stylu tekstu na okładkach postów w siatce profilu, aby ułatwić użytkownikom przeglądanie Twoich serii (np. *"Automatyzacja B2B"*, *"Sztuczki n8n"*, *"GCP Tutorial"*).
