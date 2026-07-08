---
name: analytics-tracking
description: "Wdrażanie lekkiej, bez-ciasteczkowej analityki zdarzeń (cookieless) oraz śledzenie konwersji lejków sprzedażowych zgodne z RODO."
---

# Analytics Tracking — Standardy Analityki i Śledzenia Zdarzeń

## Cel i Przeznaczenie
Aby optymalizować konwersję i dbać o budżet marketingowy, musimy precyzyjnie mierzyć zachowania użytkowników (np. kliknięcia w przyciski pobierania e-booków, rezerwacje w kalendarzu, przejścia na subdomenę). Ten skill definiuje zasady wdrażania analityki.

## Zasady Śledzenia RODO-friendly
1. **Brak ciasteczek śledzących (Cookieless Analytics):**
   - Unikaj standardowych, inwazyjnych narzędzi śledzących bez zgody użytkownika. Do podstawowych statystyk ruchu używaj lekkich skryptów analitycznych (np. Plausible, Microanalytics), które nie zbierają danych osobowych.
2. **Śledzenie konwersji (Event Tracking):**
   - Mierz zdarzenia za pomocą wysyłania zdarzeń JavaScript na konkretne akcje (kliknięcie przycisku `Odkryj Projekt Mercury`, zapis na formularz).
   - Wszystkie leady zbierane z formularzy (imię, email) muszą być natywne przekazywane bezpiecznym protokołem HTTPS bezpośrednio do bazy danych / CRM na maszynie GCP.

## Przykładowy skrypt śledzenia zdarzenia
```javascript
function trackEvent(eventName, eventCategory) {
  if (typeof window.dataLayer !== 'undefined') {
    window.dataLayer.push({
      'event': 'custom_event',
      'event_name': eventName,
      'event_category': eventCategory
    });
  }
}
```
