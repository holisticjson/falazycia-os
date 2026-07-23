# 🧠 Memory Compound: Rejestr Rozwiązanych Wzorców & Błędów

Ten plik gromadzi wiedzę z rozwiazywanych problemów i błędów deweloperskich w środowisku Jaison OS. Żaden agent nie ma prawa powtórzyć błędu zarejestrowanego w tym rejestrze.

---

### 💡 Wzorzet #001: Windows Console Unicode Emoji Print Exception
* **Data:** 2026-07-23
* **Symptom:** `UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f9e0'` podczas uruchamiania skryptów Python z wiersza poleceń Windows.
* **Przyczyna:** Konsola Windows (cp1250 / cp852) nie potrafi zdekodować znaków emoji bez wymuszenia kodowania UTF-8 na `sys.stdout`.
* **Rozwiązanie:** Na samym początku każdego skryptu CLI w Pythonie wstawiamy rekonfigurację kodowania:
  ```python
  import sys
  if hasattr(sys.stdout, 'reconfigure'):
      sys.stdout.reconfigure(encoding='utf-8')
  ```

---

### 💡 Wzorzet #002: Remotion CLI Entry Point Registration
* **Data:** 2026-07-23
* **Symptom:** `Error: You passed Root.tsx as your entry point, but this file does not contain 'registerRoot'`
* **Przyczyna:** Remotion CLI wymaga pliku wejściowego (np. `src/index.ts`), który jawnie wywołuje `registerRoot(RemotionRoot)`.
* **Rozwiązanie:** Tworzymy dedykowany `src/index.ts` z `registerRoot(RemotionRoot)` i przekazujemy go do polecenia `npx remotion render src/index.ts JaisonReel out.mp4`.
