# 🧵 Szablon Rebrandingu: Threads Profile

Ten dokument to szablon wdrożeniowy konfiguracji profesjonalnego profilu na platformie Threads (by Instagram) dla marki **{{BRAND_NAME}}**.

---

## 🛠️ KROK 1: Podstawowa Identyfikacja Konta
Ponieważ Threads jest bezpośrednio połączone z Twoim kontem na Instagramie, najprostszą i najbardziej zalecaną metodą jest import danych profilowych z Instagrama jednym kliknięciem. Możesz też edytować je niezależnie:
1.  **Nazwa Użytkownika (Handle):** Identyczna jak na Instagramie (np. `@{{BRAND_HANDLE}}` lub `@{{OWNER_HANDLE}}`).
2.  **Nazwa Profilu (Display Name):** (Max 30 znaków):
    > `{{THREADS_DISPLAY_NAME}}` (np. `{{OWNER_NAME}} | AI Systems Architect`)

---

## 📸 KROK 2: Wizualia Profilu (Avatar)

### 👤 A. Zdjęcie Profilowe (Avatar)
*   **Format:** `1:1` (Kwadrat, przycinany do małego koła).
*   **Zasada:** Zaleca się zaimportowanie tego samego awatara co na Instagramie/LinkedIn w celu zachowania maksymalnej spójności wizualnej w całym ekosystemie internetowym.
*   **Prompt do wygenerowania (jeśli robisz to niezależnie):**
    > `{{THREADS_AVATAR_PROMPT}}`

### ⚠️ Ważna uwaga techniczna dotycząca baneru:
> **Platforma Threads NIE POSIADA tradycyjnych banerów w tle (header banners)** na profilach użytkowników (w przeciwieństwie do LinkedIn czy Twittera/X). Profil na Threads ma minimalistyczny, czysty, tekstowy układ. Cały nacisk pozycjonowania spoczywa na Twoim **Avatarze** oraz **Bio**.

---

## ✍️ KROK 3: Pozycjonowanie i Treść (Threads Bio)

> [!IMPORTANT]
> **Sztywny limit Bio na Threads wynosi 150 znaków ze spacjami!** Styl Threads jest z założenia bardziej swobodny, bezpośredni i konwersacyjny niż na LinkedIn czy X. Ludzie szukają tu autentyczności, luźniejszych dyskusji oraz "kuchni" powstawania projektów (Building in Public).

*Skopiuj poniższy tekst i wklej do sekcji Bio na Threads:*

```text
{{THREADS_BIO_TEXT}}
```

*   **Link w Bio:** `{{WEBSITE_URL}}`
