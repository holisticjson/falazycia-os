# 👥 Szablon Rebrandingu: Facebook Page (Fanpage)

Ten dokument to szablon wdrożeniowy konfiguracji profesjonalnej strony biznesowej (Fanpage) na Facebooku dla marki **{{BRAND_NAME}}**.

---

## 🛠️ KROK 1: Podstawowe Pozycjonowanie i Kategoria
1.  **Nazwa Strony (Page Name):** Reprezentuje Twoją markę i rolę:
    > `{{FACEBOOK_PAGE_NAME}}` (np. `{{BRAND_NAME}} — Automatyzacje AI & n8n`)
2.  **Nazwa Użytkownika Strony (Username/@tag):** Krótki, czysty identyfikator do oznaczania:
    > `@{{BRAND_HANDLE}}` (np. `@jaison.agency.os`)
3.  **Kategoria Strony:** Zaznacz pozycje budujące właściwy wizerunek:
    *   `Doradca ds. IT (IT Consultant)`
    *   `Agencja marketingowa (Marketing Agency)`
    *   `Usługi biznesowe (Business Service)`

---

## 📸 KROK 2: Wizualia Strony (Avatar i Baner w Tle)

### 👤 A. Zdjęcie Profilowe (Avatar)
*   **Format:** `1:1` (Kwadrat, min. `170 x 170 px`).
*   **Silnik:** `{{AVATAR_ENGINE}}`
*   **Zasada:** Identyczne lub bardzo zbliżone do awatara z LinkedIn dla zachowania spójności twarzy i marki.
*   **Prompt do wygenerowania:**
    > `{{FACEBOOK_AVATAR_PROMPT}}`

### 🖼️ B. Zdjęcie w Tle (Facebook Cover Banner)
*   **Wymiary rekomendowane:** `1640 x 924 px` (Proporcje 16:9, bezpieczne kadrowanie na komputerach i telefonach).
*   **Zasada bezpiecznych marginesów:** 
    *   Na telefonach boki baneru są lekko przycinane.
    *   Na komputerach góra i dół są lekko przycinane.
    *   **Zasada:** Umieść slogan, logo i CTA wyłącznie w centralno-prawej części baneru.
*   **Slogan na banerze:** `{{MOTTO}}`
*   **CTA na banerze:** `{{CTA}}`
*   **Prompt do wygenerowania tła:**
    > `{{FACEBOOK_BANNER_PROMPT}}`

---

## ✍️ KROK 3: Pozycjonowanie i Treść (Facebook Copywriting)

### 📝 1. Krótkie Bio (Biogram)
*Maksymalnie skondensowany opis wyświetlany bezpośrednio pod awatarem (Max 255 znaków!):*

```text
{{FACEBOOK_SHORT_BIO}}
```

### 📖 2. Szczegółowy Opis (O Stronie / Informacje)
*Pełny tekst opisujący historię, misję oraz ofertę marki, który wkleisz w sekcji "Informacje" -> "Szczegółowy opis":*

```text
{{FACEBOOK_LONG_DESCRIPTION}}
```

---

## ⚙️ KROK 4: Konfiguracja Przycisku Akcji (CTA Button)
Skonfiguruj główny przycisk akcji na swoim Fanpage'u, aby kierował ruch na zewnątrz lub do bezpośredniej konwersji:
*   **Typ przycisku:** `Więcej informacji (Learn More)` lub `Wyślij wiadomość (Send Message)`.
*   **Adres docelowy (dla "Więcej informacji"):** `{{WEBSITE_URL}}`
*   **Automatyczna wiadomość powitalna w Messengerze:** 
    > *"Cześć! Tu {{BRAND_NAME}}. W czym mogę pomóc w Twoim biznesie? Jeśli chcesz bezpłatny audyt AI/AEO, kliknij tutaj: {{WEBSITE_URL}}"*
