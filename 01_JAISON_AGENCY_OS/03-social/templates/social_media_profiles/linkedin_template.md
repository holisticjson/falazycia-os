# 📘 Szablon Rebrandingu: LinkedIn Profile

Ten dokument to szablon wdrożeniowy konfiguracji profesjonalnego profilu osobistego oraz Strony Usług na LinkedIn dla marki **{{BRAND_NAME}}**. 

---

## 🛠️ KROK 1: Konfiguracja Podstawowa i Szybkie Poprawki
1.  **Imię i Nazwisko:** Upewnij się, że wpisane są wyłącznie Twoje dane (np. `{{OWNER_NAME}}`). Wszelkie dopiski, nazwy marek czy pseudonimy usuń z pola nazwiska (częsty błąd to wpisywanie marki w pole nazwiska rodowego).
2.  **Nagłówek (Headline):** (Max 220 znaków). Wklej wygenerowany tekst:
    > `{{LINKEDIN_HEADLINE}}`

---

## 📸 KROK 2: Wizualia Profilu (Awatary i Banery)

### 👤 A. Zdjęcie Profilowe (Avatar)
*   **Format:** `1:1` (Kwadrat)
*   **Silnik:** `{{AVATAR_ENGINE}}`
*   **Prompt do wygenerowania:**
    > `{{LINKEDIN_AVATAR_PROMPT}}`

### 🖼️ B. Zdjęcie w Tle (Baner LinkedIn)
*   **Wymiary:** `1584 x 396 px` (Proporcje ok. 4:1)
*   **Zasada:** Tekst, motto i CTA muszą znajdować się wyłącznie po prawej stronie baneru, aby zdjęcie profilowe ich nie zasłoniło.
*   **Slogan na banerze:** `{{MOTTO}}`
*   **CTA na banerze:** `{{CTA}}`
*   **Prompt do wygenerowania tła:**
    > `{{LINKEDIN_BANNER_PROMPT}}`

---

## ✍️ KROK 3: Pozycjonowanie i Treść

### 📖 1. Sekcja "O mnie" (About)
*Skopiuj poniższy wygenerowany tekst i wklej do sekcji "O mnie" na LinkedIn:*

```text
{{LINKEDIN_ABOUT_TEXT}}
```

---

## 💼 KROK 4: Konfiguracja Strony Usług (Services Page)

To kluczowa podstrona na LinkedIn, która decyduje o pozyskiwaniu leadów B2B.

### 📝 1. Omówienie Usług (Services Description)
*Kliknij "Edytuj stronę" na stronie usług i zastąp stary tekst tym skondensowanym opisem (Max 500 znaków!):*

```text
{{LINKEDIN_SERVICES_DESCRIPTION}}
```

### 🏷️ 2. Wybór kategorii usług:
Zaznacz z listy LinkedIn najbardziej pasujące kategorie:
*   `{{LINKEDIN_SERVICE_CATEGORY_1}}`
*   `{{LINKEDIN_SERVICE_CATEGORY_2}}`
*   `{{LINKEDIN_SERVICE_CATEGORY_3}}`
*   `{{LINKEDIN_SERVICE_CATEGORY_4}}`

### 📂 3. Załączniki i Linki (Multimedia)
Dodaj w sekcji multimediów na stronie usług:
1.  **Link 1:** `{{WEBSITE_URL}}` (Podpis: *{{BRAND_NAME}} — Strona Główna & Darmowe Blueprinty*)
2.  **Link 2:** `{{APP_URL}}` (Podpis: *Aplikacja {{BRAND_NAME}} OS — Panel Narzędziowy*)
3.  **Grafika 1:** Certyfikat potwierdzający kompetencje.
4.  **Grafika 2:** Schemat działania / Case study wdrożenia automatyzacji.

---

## 🎓 KROK 5: Certyfikaty i Projekty

### 📜 1. Sekcja "Licencje i certyfikaty"
Dodaj nową licencję/certyfikat na swoim profilu:
*   **Nazwa\*:** `Wykorzystanie AI w rozwoju firmy (Google & SGH)`
*   **Instytucja wydająca\*:** `Google`
*   **Data wydania:** `{{CERTIFICATE_DATE}}`
*   **Adres URL poświadczenia:** Link do certyfikatu na Dysku Google lub Twojej stronie.

### 💻 2. Sekcja "Projekty"
Dodaj nowy projekt:
*   **Nazwa projektu:** `{{BRAND_NAME}} Operating System`
*   **Czas trwania:** `Od 2024 - obecnie`
*   **Opis:**
    > `{{LINKEDIN_PROJECT_DESCRIPTION}}`
*   **Strona projektu:** `{{WEBSITE_URL}}`
