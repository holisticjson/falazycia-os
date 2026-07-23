---
name: dev-compound
description: Pamięć przyrostowa i uczenie się na błędach. Po naprawieniu błędu lub ukończeniu sprintu deweloperskiego, rejestruje wzorce rozwiązań i wyciągnięte wnioski w pliku pamięci, zapobiegając ich powtórzeniu w przyszłości.
---

# 🧠 Skill: Dev-Compound (Pamięć Wzorców & Samodoskonalenie)

Ten skill odpowiada za wyciąganie nauk z każdego rozwiązanego problemu, naprawionego błędu czy ukończonego modułu.

---

## 📋 Procedura Dev-Compound:

Po zakończeniu prac lub rozwiązaniu błędu deweloperskiego:

1. **Analiza Przyczyny Głównej (Root Cause Analysis):**
   - Co było pierwotną przyczyną błędu (np. błąd kodowania unicode w Windows, zapomniana zmienna środowiskowa, brak importu)?
2. **Rejestracja Wzorca:**
   - Agent zwięźle zapisuje rozwiązany wzorzec w ustrukturyzowanym rejestrze w pliku:
     `C:\Aplikacje MVP\.agents\MEMORY_COMPOUND.md`
3. **Zasada 0 Powtórzeń:**
   - Przed rozpoczęciem pisania nowego kodu, agent przeszukuje plik `MEMORY_COMPOUND.md`, aby upewnić się, że nie stosuje wzorca, który wcześniej rzucił wyjątkiem.

---

## Format Zpisu Wzorca:

```markdown
### 💡 Wzorzec #[ID]: [Krótki Opis Błędu]
* **Data:** YYYY-MM-DD
* **Symptom:** [Jak objawiał się błąd]
* **Przyczyna:** [Trzon problemu]
* **Rozwiązanie:** [Sposób naprawy — poprawny kod]
```
