---
name: churn-prevention
description: "Algorytmy i taktyki zapobiegania rezygnacjom użytkowników (churn) oraz budowanie retencji w planach abonamentowych SaaS (Mercury Pro/Pro Plus)."
---

# Churn Prevention — Standardy Operacyjne Retencji SaaS

## Cel i Przeznaczenie
Utrzymanie klienta w planie abonamentowym (retencja) jest tańsze niż pozyskanie nowego. Ten skill definiuje zasady monitorowania i zapobiegania rezygnacjom użytkowników w systemie abonamentowym JaSon Pro / Pro Plus.

## Procedura Monitorowania
1. **Identyfikacja uśpionych kont (Silent Churn):**
   - Jeśli użytkownik nie wywołał żadnego asystenta / zapytania w komunikatorze przez 7 kolejnych dni, oznacz konto jako "uśpione".
   - Wyślij dyskretną, asynchroniczną wiadomość o wysokiej wartości (np. *"Cześć, Twój wirtualny dyrektor marketingu przygotował dzisiaj krótką listę 3 pomysłów na posty dla Twojej branży. Chcesz je zobaczyć?"*).
2. **Reakcja na anulowanie subskrypcji (Active Churn):**
   - W momencie kliknięcia "rezygnuj", natychmiast przekieruj użytkownika do dynamicznej ankiety (maksymalnie 3 pytania) badającej główny powód.
   - Zaproponuj automatycznie alternatywę: "Zmień na tańszy plan Basic" lub "Zawieś subskrypcję na 30 dni bez utraty danych".

## Główne Metryki
- Miesięczny wskaźnik rezygnacji (Churn Rate) - cel: poniżej 3% miesięcznie.
- Średnia żywotność klienta (LTV - Lifetime Value).
