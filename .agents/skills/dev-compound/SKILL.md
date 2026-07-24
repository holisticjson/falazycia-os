---
name: dev-compound
description: Pamięć przyrostowa, samo-ulepszanie skilli (Microsoft SkillOpt) i uczenie się na błędach. Po naprawieniu błędu lub ukończeniu sprintu deweloperskiego, rejestruje wzorce rozwiązań i wyciągnięte wnioski w pliku pamięci, zapobiegając ich powtórzeniu w przyszłości.
---

# 🧠 Skill: Dev-Compound (Pamięć Wzorców, SkillOpt & Samodoskonalenie)

Ten skill odpowiada za wyciąganie nauk z każdego rozwiązanego problemu, automatyczną optymalizację własnych skilli (w oparciu o wzorzec **Microsoft SkillOpt**) oraz czystą organizację warstw mediów i kodu.

---

## 📋 Procedura Dev-Compound & SkillOpt:

Po zakończeniu prac lub rozwiązaniu błędu deweloperskiego:

1. **Analiza Przyczyny Głównej (Root Cause Analysis):**
   - Co było pierwotną przyczyną błędu (np. błąd kodowania unicode w Windows, zapomniana zmienna środowiskowa, brak importu)?
2. **Refaktoryzacja Skilli (SkillOpt Feedback Loop):**
   - Jeśli błąd wynikał ze słabej wytycznej w jakimś pliku `SKILL.md`, agent **samoczynnie zaktualizuje** odpowiedni plik w `.agents/skills/`, ulepszając jego treść dla przyszłych sesji!
3. **Rejestracja Wzorca:**
   - Agent zwięźle zapisuje rozwiązany wzorzec w ustrukturyzowanym rejestrze w pliku:
     [`C:\Aplikacje MVP\.agents\MEMORY_COMPOUND.md`](file:///C:/Aplikacje%20MVP/.agents/MEMORY_COMPOUND.md)
4. **Zasada 0 Powtórzeń & Low-Memory Harness (`jcode`):**
   - Przed rozpoczęciem pisania nowego kodu, agent przeszukuje plik `MEMORY_COMPOUND.md`.
   - Do mikrozadań kodowania na GCP VM używamy harnessu **`jcode` (Rust)** dającego ~14ms startu i zużycie RAM poniżej 150 MB.

---

## 🎨 Podział Warstw Mediów & AI w Jaison OS (Bez Dublowania):

1. **fal.ai (Flux LoRA Studio):** Trening modeli twarzy/zdjęć i generowanie statycznych fotomontaży w wysokiej rozdzielczości.
2. **Higgsfield AI (Generative Video & Motion Control):** Generowanie surowych klipów B-Roll AI, animowanych avatarów oraz ujęć kinowych (Sora 2, Kling 1.5, Veo 2).
3. **Remotion.dev (React MP4 Engine):** Programistyczny montaż końcowy. Układa napisy, logo, kolory marki i skleja wygenerowany B-Roll z lektorem.
4. **Composio.dev (MCP OAuth):** Automatyczna publikacja gotowych materiałów na konta społecznościowe.

---

## Format Zapisu Wzorca:

```markdown
### 💡 Wzorzec #[ID]: [Krótki Opis Błędu]
* **Data:** YYYY-MM-DD
* **Symptom:** [Jak objawiał się błąd]
* **Przyczyna:** [Trzon problemu]
* **Rozwiązanie:** [Sposób naprawy — poprawny kod]
```
