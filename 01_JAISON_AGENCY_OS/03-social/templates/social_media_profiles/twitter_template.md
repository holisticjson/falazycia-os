# 🐦 Szablon Rebrandingu: Twitter / X Profile

Ten dokument to szablon wdrożeniowy konfiguracji profesjonalnego profilu na platformie Twitter/X dla marki **{{BRAND_NAME}}**.

---

## 🛠️ KROK 1: Podstawowa Identyfikacja Konta
1.  **Nazwa Użytkownika (Handle/@tag):** Twój unikalny adres (np. `@{{BRAND_HANDLE}}` lub `@{{OWNER_HANDLE}}`). Powinien być krótki i łatwy do wpisania z telefonu.
2.  **Nazwa Wyświetlana (Display Name):** (Max 50 znaków). Najlepiej połączyć imię z niszą lub marką:
    > `{{TWITTER_DISPLAY_NAME}}` (np. `{{OWNER_NAME}} | AI Systems Architect`)

---

## 📸 KROK 2: Wizualia Profilu (Avatar i Baner w Tle)

### 👤 A. Zdjęcie Profilowe (Avatar)
*   **Format:** `1:1` (Kwadrat, przycinany do koła, min. `400 x 400 px`).
*   **Silnik:** `{{AVATAR_ENGINE}}`
*   **Zasada:** Ponieważ X to platforma dyskusyjna, Twój awatar musi wyglądać jak twarz żywego, autentycznego człowieka o silnych kompetencjach technologicznych. Unikaj zbytnio "przerysowanych" grafik AI – postaw na realizm.
*   **Prompt do wygenerowania:**
    > `{{TWITTER_AVATAR_PROMPT}}`

### 🖼️ B. Zdjęcie w Tle (Twitter/X Banner)
*   **Wymiary:** `1500 x 500 px` (Dokładne proporcje 3:1).
*   **Zasada:** Zdjęcie profilowe na X nakłada się na lewą dolną część baneru i może zasłonić tekst. Wszystkie elementy tekstowe i slogan muszą znajdować się wyłącznie po prawej stronie!
*   **Slogan na banerze:** `{{MOTTO}}`
*   **CTA na banerze:** `{{CTA}}`
*   **Prompt do wygenerowania tła:**
    > `{{TWITTER_BANNER_PROMPT}}`

---

## ✍️ KROK 3: Pozycjonowanie i Treść (Twitter/X Bio)

> [!IMPORTANT]
> **Sztywny limit Bio na Twitterze/X wynosi 160 znaków ze spacjami!** Tekst musi być dynamiczny, profesjonalny i ukierunkowany na branżę technologiczną/AI. Dobrze sprawdzają się krótkie wypunktowania oddzielone pionową kreską `|` lub emotikonami.

*Skopiuj poniższy krótki tekst i wklej do sekcji Bio:*

```text
{{TWITTER_BIO_TEXT}}
```

*   **Lokalizacja (Location):** `Polska` lub `Asynchronicznie / Google Cloud` (Max 30 znaków).
*   **Strona internetowa (Website):** `{{WEBSITE_URL}}`

---

## 📌 KROK 4: Przypięty Post (Pinned Tweet)
Pierwszy post, który widzi każdy wchodzący na Twój profil na X. Powinien to być tzw. "Value Thread" (wątek edukacyjny) lub bezpośrednia oferta:
*   **Treść przypiętego posta:** 
    > *"Buduję systemy agentowe AI B2B na Google Cloud, które odzyskują 15+ godzin tygodniowo. Bez drogich abonamentów, bez szkolenia zespołu, sterowane z WhatsApp. Chcesz bezpłatny audyt AI dla swojej firmy? Wejdź na {{WEBSITE_URL}} i odbierz darmowe blueprinty! 🚀🧵"*
