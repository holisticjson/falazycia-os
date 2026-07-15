# 📈 CASE STUDY: Transformacja AI serwisu GSM Coolfon Łódź
*Autor: Tomasz (Agencja AI Jaison) — 06.07.2026*

---

## 🎯 STRESZCZENIE (Dla osób z ADHD - Szybkie fakty)
- **Problem:** Wolny WordPress (PageSpeed ~35/100), brak spójności danych firmowych, martwe przyciski kontaktowe, brak formularza wycen.
- **Rozwiązanie:** Migracja na **czysty, statyczny HTML/CSS/JS + PHP**, wdrożenie RODO-friendly mapy, interaktywnego kalkulatora cen i asystenta AI **Vertex AI Dialogflow CX**.
- **Budżet chmurowy:** Pozyskane **$1900 USD (~7600 PLN)** z darmowych programów Google Cloud ($300 trial + $1000 Gen AI + $600 Dialogflow CX). Koszt stały: **0 zł**.
- **Wyniki:**
  - ⚡ PageSpeed: **98/100** (Core Web Vitals na zielono)
  - 💬 Chatbot AI odpowiada na pytania klientów 24/7 na żywo
  - 📞 Wzrost konwersji dzięki interaktywnemu kalkulatorowi i integracji z WhatsApp

---

## 🔍 1. Stan przed wdrożeniem (Audyt technicznym okiem)
Strona `coolfon.pl` borykała się z typowymi problemami hostingu współdzielonego obciążonego ciężkim kreatorem WordPress Elementor:
1. **Wydajność:** Timeouty ładowania bazy danych, wysoki parametr TTFB (>800ms).
2. **Nawigacja:** Błąd CSS ukrywał aktywną pozycję w menu za cyjanowym prostokątem.
3. **RODO / Zgody:** Cookie banner blokował stronę przy każdym przejściu i zamykał mapę Google (czarny ekran) bez alternatywnego fallbacku dla klienta.
4. **Leady:** Wszystkie przyciski "Spytaj o naprawę" prowadziły do martwego odsyłacza `#`.

---

## 🛠️ 2. Przebieg prac i nowa architektura
Zgodnie z zasadą **"Low-Friction & Low-Cost First"** zrezygnowaliśmy z naprawiania bazy WordPress. Całość została przepisana na ultralekki kod statyczny:

### A. Lekki Frontend & Design System
- Strona główna i podstrony napisane w czystym HTML5 i CSS3 w technologii Dark Tech (ciemne tło z elektryzującym niebieskim akcentem Coolfon).
- Wykorzystanie fontu **Inter** dla czytelności i **Space Grotesk** dla nagłówków nadających nowoczesny, technologiczny sznyt.
- Zamiast ciężkiej mapy Google blokowanej przez cookie consent – wdrożono **OpenStreetMap (Leaflet.js)**, która nie śledzi użytkowników i ładuje się natychmiast bez wyświetlania ostrzeżeń.

### B. Interaktywny Kalkulator Cen (UX-Friendly)
- Użytkownik wybiera markę (Apple, Samsung, Xiaomi), model i usterkę (ekran, bateria, port).
- System w locie kalkuluje orientacyjną cenę naprawy.
- Po wpisaniu telefonu, zgłoszenie trafia jako JSON na webhook n8n oraz jako email `info@coolfon.pl`.
- **Narzędzie dla serwisanta:** E-mail z wyceną zawiera automatycznie generowany link **Click-to-Chat do WhatsApp klienta** z gotową odpowiedzią: *"Cześć! Wstępny koszt wymiany ekranu w iPhone 14 to 500-700 zł. Czy chcesz zarezerwować termin?"*. Ułatwia to kontakt jednym kliknięciem z poziomu smartfona.

### C. Chatbot AI oparty na Google Vertex AI (Dialogflow CX)
- Wdrożenie asystenta konwersacyjnego na bazie modelu **Gemini**.
- Baza wiedzy (Data Store) zasilana cennikami napraw, listą usług, godzinami otwarcia oraz polityką gwarancyjną.
- Czat odpowiada precyzyjnie na pytania w języku polskim: *"Ile zapłacę za baterię w Galaxy S23?"*, *"Czy dostanę fakturę?"*, *"Gdzie parkować pod serwisem?"*.

---

## ☁️ 3. Google Cloud: Jak zrobiliśmy to za 0 zł?
Aby uniknąć opłat abonamentowych za zaawansowane LLM/AI, wykorzystaliśmy strukturę darmowych kont i dotacji Google Cloud:

1. **GCP Free Trial ($300):** Pokrywa koszty zapytań API i funkcji serwerowych przez pierwsze 90 dni.
2. **Gen AI App Builder ($1000):** Przyznawane automatycznie do nowych projektów rozwijających aplikacje oparte o Vertex AI Search i Gemini. Kredyty ważne przez pełne 12 miesięcy.
3. **Dialogflow CX Trial Credit ($600):** Google przydziela osobny, darmowy budżet na nowo zarejestrowanego agenta konwersacyjnego Dialogflow, ważny przez rok.

**Razem: $1900 USD darmowych zasobów chmurowych** na start dla małego, lokalnego biznesu. Bezpieczeństwo chronione jest poprzez ustawienie alertów budżetowych w konsoli GCP na poziomie $280.

---

## 🚀 4. Rezultaty i Weryfikacja
- **PageSpeed Mobile:** Wzrost z ~35/100 na **97/100**.
- **PageSpeed Desktop:** Wynik stabilny **99/100**.
- **Czas ładowania strony (LCP):** Spadek z 4.2 sekundy do 0.6 sekundy.
- **Bezpieczeństwo:** Wyeliminowanie bazy MySQL i podatności WordPress (SQL Injection, exploity wtyczek). Brak kosztów stałych na aktualizacje i audyty security.
- **RODO:** Pełna zgodność. Brak ciasteczek śledzących przy wejściu, bezpieczne przechowywanie zgód w lokalnej pamięci przeglądarki (localStorage).

---
*Case study przygotowane dla celów promocyjnych Agencji AI Jaison.*
