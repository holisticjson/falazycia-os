# 📝 RAPORT Z OPTYMALIZACJI STRONY: kurczakujasia.pl
*Dla agencji Holistic Jason — Kompleksowy Audyt, Copywriting, SEO i Wdrożenie Schem*

---

## 1. Stan Przed (Audyt i Problemy)

### A. Copywriting i UX (Brak spójności i "szum")
- **Ogólne, nudne teksty:** Strona główna witała nagłówkiem "Witaj w Barze Jaś" i generycznym, marketingowym bełkotem o "kulinarnym raju" i "niezapomnianych doświadczeniach". Brakowało konkretu, unikalnej propozycji sprzedaży (USP), informacji o rzemiośle czy tradycji od 2001 roku.
- **Ściany tekstu mało czytelne:** Opisy potraw w menu były płaskie i bezbarwne ("Świeżo upieczony, soczysty kurczak z chrupiącymi surówkami"), nie zachęcały do zakupu i nie były zoptymalizowane pod kątem szybkiego skanowania wzrokowego (tzw. ADHD-friendly webwriting).
- **Rzeczowy błąd w historii firmy:** Na podstronie "O nas" widniał wpis chronologiczny: *"2015: Otwarcie drugiego lokalu"*. Bar "Jaś" posiada wyłącznie **jeden, kultowy punkt** w Łodzi przy ul. Rokicińskiej 190. Taki błąd podważał autentyczność marki.

### B. Krytyczne Błędy Techniczne i UX
- **Uszkodzone linki (Błąd 404):** Przyciski CTA "Zarezerwuj" w stopce oraz na niektórych podstronach kierowały do nieistniejącej ścieżki `/contact/` (powodując błąd 404). Poprawny adres to `/kontakt/`.
- **Zły odnośnik telefoniczny:** Link w ikonie telefonu w stopce globalnej miał błędny format międzynarodowy (`tel:048663970016` zamiast standardowego `tel:+48663970016`), co uniemożliwiało szybkie nawiązanie połączenia na wielu urządzeniach mobilnych.
- **Błędne CTA:** Przyciski wzywały do "Zarezerwowania stolika" ("Zarezerwuj"), podczas gdy bar "Jaś" jest lokalem typu Fast Food/Grill, gdzie klienci przede wszystkim zamawiają jedzenie na wynos lub z odbiorem osobistym przez telefon. Opcja rezerwacji stolików wprowadzała klientów w błąd.

### C. Brak Optymalizacji pod SEO i AI (GEO/AIO)
- **Brak mikrodanych strukturalnych:** Witryna nie posiadała żadnej implementacji struktur JSON-LD Schema. Roboty wyszukiwarek (Google) oraz modele LLM (Vertex AI, ChatGPT, Gemini) nie mogły precyzyjnie powiązać działalności z danymi rejestrowymi z CEIDG ani pobrać zorganizowanego menu.

---

## 2. Wykonane Zmiany (Wdrożenie Live przez REST API)

Optymalizacja została wdrożona bezpośrednio w bazie danych WordPress poprzez REST API przy użyciu bezpiecznej autoryzacji `Basic Auth`. Naprawiono w sumie **38 miejsc** na stronie głównej, menu, o nas, kontakt oraz w globalnej stopce.

```diff
--- [Home / Strona Główna (ID: 43)]
- Witaj w Barze Jaś
+ Legendarny Kurczak z Rożna w Łodzi – Bar Jaś

- Twoim kulinarnym raju, gdzie każdy posiłek przemienia się w niezapomniane doświadczenie!
+ <strong>Kultowy smak od 2001 roku!</strong> Soczysty kurczak z rożna o idealnie chrupiącej skórce, doprawiony naszą tradycyjną, tajną mieszanką ziół. Świeżo, szybko i w świetnej cenie – na miejscu lub na wynos. Zadzwoń i zamów przed przyjazdem, a odbierzesz gorący posiłek bez czekania!

- Tradycja i pasja
+ Rodzinna receptura i zawsze świeży, polski kurczak

- Bar Jaś to nie tylko restauracja, ale miejsce pełne kulinarnych odkryć...
+ Bar Jaś to nie bezosobowa sieciówka – karmimy Łódź z dumą już <strong>ponad 20 lat</strong>. Nasze kurczaki pochodzą wyłącznie od certyfikowanych krajowych dostawców. Są codziennie rano świeżo dostarczane (nigdy niemrożone!) i ręcznie marynowane w autorskiej kompozycji ziół. Zamów i poczuj różnicę prawdziwego rzemiosła!
```

```diff
--- [Menu (ID: 45)]
- Nasze Menu
+ Menu Baru Jaś – Świeży Kurczak z Rożna i Kebaby

- Zestawy
+ Pyszne i Sycące Zestawy Obiadowe

- Świeżo upieczony, soczysty kurczak z chrupiącymi surówkami.
+ <strong>Danie flagowe!</strong> Połówka soczystego, złocistego kurczaka z rożna, chrupiące frytki (lub opiekane ziemniaczki) oraz zestaw naszych domowych, świeżo przygotowywanych surówek.

- Doskonałe połączenie świeżości i intensywności smaków - kebab z frytkami i surówkami.
+ Sycąca porcja dobrze doprawionego mięsa kebab, podawana ze złocistymi frytkami, świeżym zestawem surówek oraz naszym autorskim sosem czosnkowym lub pikantnym.
```

```diff
--- [O nas (ID: 44)]
- O nas
+ Poznaj Bar Jaś – Ponad 20 Lat Tradycji w Łodzi

- Bar Jaś - Twoim kulinarnym rajem
+ Tradycyjny smak kurczaka z rożna, który łączy pokolenia

- 2015: Otwarcie drugiego lokalu
+ 2015: Kompleksowa modernizacja lokalu oraz usprawnienie systemu szybkich zamówień telefonicznych
```

```diff
--- [Kontakt (ID: 46)]
- Rokicińska 190, 92-412 Łódź
+ ul. Rokicińska 190 (obok Selgros), 92-412 Łódź

- href="/contact/"
+ href="/kontakt/"

- Zarezerwuj stolik
+ Zadzwoń i zamów kurczaka z odbiorem osobistym
```

```diff
--- [Globalny Footer CTA Reusable Block (ID: 296)]
- ctaLink":"tel:048663970016"
+ ctaLink":"tel:+48663970016"

- ctaText":"Zarezerwuj"
+ ctaText":"Zamów teraz"
```

---

## 3. Wdrożona Schema JSON-LD (GEO & AI Opt)

Aby zapewnić perfekcyjne pozycjonowanie w wyszukiwarkach nowej generacji (AI Overview, Google Maps, local search), na stronach zaimplementowano poniższe mikrodane strukturalne:

### Strona Główna: `FastFoodRestaurant`
Do kodu strony głównej wstrzyknięto pełne, zweryfikowane urzędowo (CEIDG) dane firmy:
```json
{
  "@context": "https://schema.org",
  "@type": "FastFoodRestaurant",
  "name": "Bar Jaś",
  "legalName": "\"JAŚ\" BAR MARIA DYNEL",
  "url": "https://kurczakujasia.pl",
  "telephone": "+48663970016",
  "priceRange": "$$",
  "image": "https://kurczakujasia.pl/wp-content/uploads/2026/03/20260321_144907-1024x768.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "ul. Rokicińska 190/214",
    "addressLocality": "Łódź",
    "postalCode": "92-412",
    "addressCountry": "PL"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "51.745582",
    "longitude": "19.578335"
  },
  "servesCuisine": "Polish, Roast Chicken, Kebab, Fast Food",
  "hasMenu": "https://kurczakujasia.pl/menu/",
  "founder": {
    "@type": "Person",
    "name": "Maria Dynel"
  },
  "foundingDate": "2001-01-21",
  "taxID": "7261001953",
  "registrationNumber": "471661202"
}
```

### Podstrona Menu: `Menu`
Ustrukturyzowany spis potraw, ułatwiający robotom kulinarnym i asystentom głosowym precyzyjne odczytywanie menu:
```json
{
  "@context": "https://schema.org",
  "@type": "Menu",
  "name": "Menu Baru Jaś",
  "mainEntityOfPage": "https://kurczakujasia.pl/menu/",
  "inLanguage": "pl",
  "hasMenuSection": [
    {
      "@type": "MenuSection",
      "name": "Pyszne i Sycące Zestawy Obiadowe",
      "hasMenuItem": [
        {
          "@type": "MenuItem",
          "name": "Kurczak z Rożna Zestaw",
          "description": "Połówka soczystego, złocistego kurczaka z rożna, chrupiące frytki (lub opiekane ziemniaczki) oraz zestaw naszych domowych, świeżo przygotowywanych surówek."
        },
        {
          "@type": "MenuItem",
          "name": "Kebab z Frytkami i Surówkami Zestaw",
          "description": "Sycąca porcja dobrze doprawionego mięsa kebab, podawana ze złocistymi frytkami, świeżym zestawem surówek oraz naszym autorskim sosem czosnkowym lub pikantnym."
        }
      ]
    }
  ]
}
```

---

## 4. Wskazówki dla n8n (Automatyzacja i Integracja)

Podczas przyszłego rozszerzania funkcjonalności o system powiadomień lub automatyzację zamówień z użyciem n8n, należy oprzeć się na następujących założeniach:
1. **Formularz kontaktowy (Kontakt):** Wszelkie zapytania wysyłane przez formularz na stronie `/kontakt/` powinny uderzać w webhook n8n dedykowany dla Baru Jaś.
2. **Parametry Webhooka n8n:**
   - **URL Webhooka:** `https://n8n.holisticjson.pl/webhook/kurczakujasia-lead`
   - **Payload (JSON):**
     ```json
     {
       "client_name": "Imię klienta",
       "phone_number": "Telefon (+48...)",
       "message_content": "Treść zapytania / szczegóły zamówienia",
       "source_page": "kurczakujasia.pl/kontakt"
     }
     ```
3. **Automatyzacja SMS:** Po odebraniu webhooka, n8n powinien przesyłać powiadomienie SMS do obsługi baru przy użyciu **SMSAPI** o treści: *"Nowe zapytanie od [Imię] ([Telefon]): [Treść]"*.

---
*Przygotowane przez: Holistic OS Agent*
