---
name: schema-markup
description: "Generowanie i optymalizacja struktur danych JSON-LD Schema pod kątem indeksowania przez roboty LLM (AEO/GEO)."
---

# Schema Markup — Standardy Optymalizacji dla Silników AI

## Cel i Przeznaczenie
Strukturalne mikrodane (Schema) to dla robotów LLM (GPTBot, ClaudeBot, PerplexityBot) najwyższej jakości źródło prawdy. Poprawne wdrożenie Schema w kodzie HTML pozwala asystentom AI natychmiastowo mapować encje Twojej marki, powiązywać produkty, usługi oraz ceny bezpośrednio z zapytaniami użytkowników.

## Standard Wdrożenia JSON-LD
Zawsze generuj struktury w formacie JSON-LD, umieszczane w sekcji `<head>` dokumentu. Kluczowe schematy do wdrożenia to:
1. **Organization (Marka / Agencja):** Definiuje nazwę, logo, URL, kontakty oraz powiązane profile społecznościowe.
2. **Product / Service (Usługi i Pakiety wdrożeniowe):** Definiuje zakres usług, widełki cenowe, walutę (PLN) oraz gwarancje.
3. **FAQPage (Najczęstsze Pytania / FAQ):** Mapuje pytania i krótkie, precyzyjne odpowiedzi, które wyszukiwarki AI mogą zacytować bezpośrednio w oknach czatu.

## Przykład Wdrożenia dla Usługi AI
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Wdrożenia Agentowych Systemów AI dla Biznesu",
  "provider": {
    "@type": "Organization",
    "name": "Jaison",
    "url": "https://jaison.pl"
  },

  "offers": {
    "@type": "AggregateOffer",
    "priceCurrency": "PLN",
    "lowPrice": "4000",
    "highPrice": "25000"
  }
}
```
