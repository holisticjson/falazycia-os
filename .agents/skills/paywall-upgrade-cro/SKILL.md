---
name: paywall-upgrade-cro
description: "Optymalizacja lejków konwersji i przejścia użytkowników z planu darmowego (Basic) do planów płatnych PRO / PRO Plus (Conversion Rate Optimization)."
---

# Paywall Upgrade CRO — Konwersja użytkowników Freemium do PRO

## Wprowadzenie
Model biznesowy opiera się na darmowym planie Basic (budowanie zasięgu i zaufania) oraz płatnych planach PRO i PRO Plus (zarząd AI, zaawansowane integracje). Ten skill definiuje wytyczne do optymalizacji ścieżki przejścia użytkowników na płatne plany.

## Wyzwalacze Konwersji (Upgrade Triggers)
1. **Limity zużycia (Usage Limits):**
   - W darmowym planie Basic limituj liczbę zapytań lub dostęp do zaawansowanych modeli (np. max 50 zapytań miesięcznie).
   - W momencie osiągnięcia 80% limitu, wyślij powiadomienie z informacją o ułamkowych kosztach przejścia na PRO.
2. **Ekskluzywne funkcje (Value-Locked Features):**
   - Integracje z zewnętrznymi systemami (n8n, Systeme.io, Gmail API, Pipedrive) oraz autonomiczne zadania w tle (Cron Jobs) są dostępne wyłącznie w planie PRO.
   - Gdy użytkownik próbuje wywołać funkcję zastrzeżoną dla PRO, wyświetl prosty komunikat o korzyściach i oszczędnościach czasu: *"Ta funkcja wymaga wirtualnego działu operacyjnego PRO, który oszczędza średnio 10 godzin tygodniowo."*

## Zasady Prezentacji Cennika
- Zawsze pokazuj korzyść cenową płatności rocznej (np. "2 miesiące gratis").
- Przedstawiaj koszty LLM w sposób przejrzysty – brak ukrytych opłat, płatność wyłącznie za realne zużycie tokenów.
