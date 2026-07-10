# Lessons Learned & Self-Improvement

## Złota Zasada z 19.06.2026: Zero Halucynacji Kontekstu i Czysty Stan Zrozumienia (No Context Hallucination)
- **Błąd:** Agent zasugerował "naprawę" modeli LLM (Bedrock, Vertex), opierając się na przestarzałym pliku `implementation_plan.md`, ignorując fakt, że nowa infrastruktura VM została już postawiona, sparametryzowana, a LiteLLM i nowe modele zostały w pełni i prawidłowo skonfigurowane (wnioski do AWS zostały złożone). Spowodowało to ekstremalny chaos i frustrację u użytkownika.
- **Lekcja (Self-Improvement):** NIGDY nie zgaduj statusu projektu na podstawie starych artefaktów bez weryfikacji. Zanim powiesz "zróbmy X, bo jest zepsute", upewnij się, że nie zostało to już naprawione w poprzednich krokach. Zawsze polegaj na najświeższych danych i wytycznych, jakie przekazuje użytkownik.
- **Workflow (Boris Cherny Protocol załączony):**
  1. *Verify Before Speaking:* Zanim zaproponujesz krok, sprawdź, czy nie został już wykonany.
  2. *Plan Mode Default:* Pracuj w zorganizowanym trybie, najpierw rozpisuj zadania w `tasks/todo.md`.
  3. *No Laziness / Find Root Causes:* Działaj jak Senior Developer. Jeśli coś działa (jak obecnie infrastruktura LLM), nie wymyślaj problemów na siłę.
