# 📸 Szablon Rebrandingu: Instagram Profile

Ten dokument to szablon wdrożeniowy konfiguracji profesjonalnego profilu na Instagramie (konto profesjonalne/twórcy) dla marki **{{BRAND_NAME}}**.

---

## 🛠️ KROK 1: Konfiguracja Nazwy i Nazwy Użytkownika
1.  **Nazwa Użytkownika (Handle):** Unikalny, prosty identyfikator (np. `@{{OWNER_HANDLE}}` lub `@{{BRAND_HANDLE}}`).
2.  **Nazwa (Name - wyświetlana pod awatarem):** (Max 30 znaków). Musi zawierać główne słowo kluczowe wyszukiwania:
    > `{{INSTAGRAM_DISPLAY_NAME}}` (np. `{{OWNER_NAME}} | AI Architect`)

---

## 📸 KROK 2: Wizualia Profilu (Avatar i Wyróżnione Relacje)

### 👤 A. Zdjęcie Profilowe (Avatar)
*   **Format:** `1:1` (Kwadrat, na profilu docelowo przycięty do koła).
*   **Silnik:** `{{AVATAR_ENGINE}}`
*   **Zasada:** Bardzo bliski kadr na twarz (super close-up) i wysoki kontrast z tłem, ponieważ na telefonie awatar na Instagramie ma zaledwie kilkanaście milimetrów!
*   **Prompt do wygenerowania:**
    > `{{INSTAGRAM_AVATAR_PROMPT}}`

### 🎨 B. Okładki Wyróżnionych Relacji (Highlight Covers)
Utrzymanie spójnej kolorystyki i ikonografii (np. neonowy błękit, ciemny grafit):
1.  **Relacja 1 (START / Poznaj mnie):** Ikona startu `🚀` lub minimalistyczny symbol.
2.  **Relacja 2 (AUTOMATYZACJE):** Ikona n8n, zębatek `⚙️` lub sieci.
3.  **Relacja 3 (BLUEPRINTS / Darmowe):** Ikona prezentu `🎁` lub dokumentu `📄`.
4.  **Relacja 4 (OPINIE / ROI):** Ikona gwiazdki `⭐` lub wykresu wzrostu `📈`.

---

## ✍️ KROK 3: Pozycjonowanie i Treść (Instagram Bio)

> [!IMPORTANT]
> **Sztywny limit Bio na Instagramie wynosi 150 znaków ze spacjami!** Tekst musi być maksymalnie skondensowany, ułożony w pionowe linijki za pomocą enterów i kończyć się jasnym wezwaniem do działania wskazującym na link poniżej.

*Skopiuj wygenerowany poniżej krótki tekst i wklej do sekcji Bio:*

```text
{{INSTAGRAM_BIO_TEXT}}
```

*   **Link w Bio (Link in Bio):** `{{WEBSITE_URL}}` lub link-tree (np. Systeme.io) łączący Twoje najważniejsze zasoby.

---

## 📅 KROK 4: Spójność Wizualna Siatki (Grid Layout)
Na Instagramie liczy się pierwsze wrażenie wizualne całego profilu (siatki 9 ostatnich postów). Zaimplementuj zasadę szachownicy lub spójnej linii kolorystycznej:
*   **Dominujące kolory:** Ciemny grafit/węgiel (`#121212`), neonowy błękit (`#00F0FF`), głęboki fiolet i biel.
*   **Fonty w grafikach:** Nowoczesne, geometryczne (np. *Inter*, *Montserrat* lub *Outfit*).
*   **Typy postów:** Karuzele edukacyjne przeplatane pionowymi wideo (Reels) oraz zdjęciami founder-lifestyle o wysokim kontraście.
