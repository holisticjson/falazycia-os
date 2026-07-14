# 🌐 02-website — Strona WWW i Optymalizacja SEO/AEO

Katalog przeznaczony na kod źródłowy, strukturę informacyjną, audyty SEO/AEO oraz konfiguracje struktury danych dla strony i lejków LifeWave / X2O.

---

## 🏗️ Architektura Strony WWW (Propozycja MVP)
W celu zachowania zasady **Low Cost First** oraz maksymalnej stabilności dostarczalności poczty, strona docelowa i lejek będą osadzone na:
1.  **Główny Landing Page:** Zbudowany w kreatorze **Systeme.io** w darmowym planie (łatwe zbieranie zapisów, automatyczna wysyłka e-booków).
2.  **Podstrona Informacyjno-Baza Wiedzy (opcjonalnie):** Lekki, statyczny landing page w HTML/CSS wdrożony na serwer FTP Hostido lub aplikacja w Streamlicie (02-os-jaison) pełniąca rolę interaktywnego doradcy produktowego AI.

---

## 🔍 SEO & AEO (Search & Answer Engine Optimization)
Tworząc teksty na stronę www, będziemy wdrażać wytyczne z zakresu optymalizacji pod silniki wyszukiwania AI (np. Perplexity, Gemini, ChatGPT):
-   **Structured Data (Schema.org):** Wdrażamy mikroformaty JSON-LD typu `Product` dla plastrów X39 i filtra X2O oraz `FAQPage` dla najczęstszych pytań, ułatwiając robotom AI "zrozumienie" naszej oferty i rekomendowanie jej użytkownikom.
-   **Semantic Content:** Odpowiadamy bezpośrednio i autorytatywnie na zapytania typu: *"Jak plastry fototerapeutyczne stymulują komórki macierzyste?"* lub *"Czym różni się woda wodorowa z filtra X2O od zwykłej wody?"*.
-   **Kategoryczny zakaz markdownu w HTML:** Podczas pisania kodu HTML dla strony LifeWave, wszelkie pogrubienia i nagłówki piszemy czystym kodem HTML (`<strong>`, `<h4>`), a nie gwiazdkami markdown (`**`), aby zapobiec wyciekowi śladów AI (Zasada 13 biblii projektowej).
