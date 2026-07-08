# 📝 RAPORT Z OPTYMALIZACJI STRONY: coolfon.pl (Kulfon GSM)
*Dla agencji Holistic Jason — Kompleksowy Audyt, Copywriting, SEO, Powiadomienia SMS i Asystent Wyceny*

---

## 1. Stan Przed (Audyt i Problemy)

### A. Copywriting i SEO (Brak pozycjonowania i struktury)
- **Słabe nasycenie lokalnymi frazami kluczowymi:** Strona główna słabo pozycjonowała się na kluczowe dla serwisu zapytania lokalne, takie jak "naprawa telefonów Łódź", "szybki serwis GSM Łódź Olechów", czy "wymiana szybki iPhone Łódź". Słowa kluczowe były rozmieszczone chaotycznie.
- **Brak optymalizacji pod skanowanie wzrokowe (ADHD):** Tekst był pisany małą literą bez silnych wyróżnień wizualnych (np. `<p>takie które sami lubimy a dla ciebie i smartfona są niezbędne</p>`). Klient szukający ratunku dla pękniętego ekranu nie widział od razu kluczowych korzyści (USP): "Naprawa do 1 godziny", "Darmowa diagnoza", "Gwarancja na usługę".
- **Chaotyczna struktura nagłówków:** Główny nagłówek Hero na stronie głównej to `<h3>` zamiast poprawnego pod kątem SEO nagłówka `<h1>` (`<h3 class="elementor-heading-title elementor-size-default">serwis pogwarancyjny twojego telefonu</h3>`). 

### B. Brak Interaktywności i Narzędzi Generowania Leadów
- **Brak formularza wyceny online:** Klienci szukający kosztów naprawy musieli dzwonić lub pisać maila. Brakowało prostego, intuicyjnego asystenta wyceny, który na podstawie wybranego modelu telefonu i usterki przesyłałby wycenę bezpośrednio do serwisu i automatycznie odpowiadał klientowi.
- **Brak systemu powiadomień o statusie naprawy:** Klienci serwisów GSM zmagają się ze stresem ("odcięci od świata"). Brakowało zautomatyzowanego informowania SMS-em o etapach naprawy ("Przyjęto", "W trakcie naprawy", "Gotowy do odbioru").

### C. Brak Optymalizacji pod SEO/AI Overview
- **Brak mikrodanych strukturalnych:** Brak wstrzykniętych danych Schema JSON-LD uniemożliwiał asystentom AI (Gemini, Vertex AI, GPT) precyzyjne odczytywanie lokalizacji, godzin otwarcia oraz oferty serwisu.

---

## 2. Planowane Zmiany (Propozycja Optymalizacji Treści)

Przygotowaliśmy precyzyjne zastąpienia tekstów dla strony głównej (ID: 26) w celu zwiększenia widoczności w wyszukiwarkach i poprawy współczynnika konwersji (CRO):

```diff
--- [Home / Strona Główna (ID: 26)]
- <p>sklep z akcesoriami telefonicznymi</p>
+ <p><strong>Ekspresowy Serwis GSM & Sklep z Akcesoriami w Łodzi</strong></p>

- serwis pogwarancyjny twojego telefonu
+ <h1 class="elementor-heading-title elementor-size-default">Szybka Naprawa Telefonów Łódź – Serwis GSM Coolfon</h1>

- W dzisiejszych czasach trudno funkcjonować bez sprawnego telefonu, dlatego zgłoś się do serwisu Coolfon a przekonasz się że naprawa Twojego Smartfona wcale nie musi być droga i czasochłonna.
+ Rozbity ekran? Zużyta bateria? <strong>Naprawimy Twój telefon nawet w 1 godzinę!</strong> Serwis GSM Coolfon to darmowa diagnoza, rzemieślnicza precyzja i oryginalne części z gwarancją. Przekonaj się, że profesjonalna naprawa smartfona w Łodzi może być szybka, bezstresowa i w uczciwej cenie. Zadzwoń lub skorzystaj z naszego kalkulatora wyceny poniżej!

- Jakie usługi i produkty oferujemy ?
+ Jakie usługi serwisowe i akcesoria oferujemy?

- takie które sami lubimy a dla ciebie i smartfona są niezbędne
+ <strong>Profesjonalny serwis smartfonów i markowe akcesoria ochronne od ręki</strong>
```

---

## 3. Planowana Schema JSON-LD (Dla coolfon.pl)

Do wstrzyknięcia na stronę główną (ID: 26) przygotowano dedykowaną, ustrukturyzowaną klasę Schema `MobilePhoneRepairShop` z pełnymi, zweryfikowanymi danymi rejestrowymi spółki z KRS:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MobilePhoneRepairShop",
  "name": "Coolfon GSM",
  "legalName": "COOLFON GSM SP. Z O.O.",
  "url": "https://coolfon.pl",
  "telephone": "+48532840877",
  "priceRange": "$$",
  "image": "https://coolfon.pl/wp-content/uploads/2021/01/coolfon_logo-removebg-preview-1.png",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "ul. Księcia Władysława Opolczyka 17 lok. C6",
    "addressLocality": "Łódź",
    "postalCode": "92-417",
    "addressCountry": "PL"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "51.744158",
    "longitude": "19.577234"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "10:00",
      "closes": "19:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "09:00",
      "closes": "15:00"
    }
  ],
  "taxID": "9820393931",
  "foundingDate": "2021-01-15",
  "sameAs": [
    "https://goo.gl/maps/ZZr5qpSs4AAFMV6u6"
  ]
}
</script>
```

---

## 4. Wskazówki Techniczne dla n8n (Automatyzacja & Powiadomienia)

### A. Asystent Wyceny i Interaktywny Kalkulator
Aby wdrożyć asystenta wyceny bez pisania wtyczek od zera, osadzimy prosty, responsywny kod formularza HTML/JS bezpośrednio w WordPressie (np. przez blok Custom HTML w Elementorze):

```html
<div class="coolfon-calc-container" style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px); color: #FFF; font-family: sans-serif; max-width: 500px; margin: 20px auto;">
  <h3 style="margin-top:0; color: #FFF; font-weight:700;">📱 Szybka Wycena Naprawy Online</h3>
  <p style="font-size:0.9rem; color: #ccc;">Wybierz model i usterkę, a nasz system prześle Ci szacowany koszt SMS-em w 2 minuty!</p>
  
  <form id="coolfon-calc-form">
    <div style="margin-bottom:15px;">
      <label style="display:block; margin-bottom:5px; font-weight:bold; font-size:0.85rem;">Marka i Model:</label>
      <select id="calc-device" required style="width:100%; padding:10px; border-radius:6px; background:#222; border:1px solid #444; color:#FFF;">
        <option value="">-- Wybierz urządzenie --</option>
        <option value="iPhone 13 / 14">Apple iPhone 13 / 14</option>
        <option value="iPhone 11 / 12">Apple iPhone 11 / 12</option>
        <option value="Samsung Galaxy S21 / S22 / S23">Samsung Galaxy S21 / S22 / S23</option>
        <option value="Samsung Galaxy A52 / A53 / A54">Samsung Galaxy A-seria (A52, A53, etc.)</option>
        <option value="Xiaomi Redmi / POCO">Xiaomi Redmi / POCO</option>
        <option value="Inny Model">Inny Model (wpisz w uwagach)</option>
      </select>
    </div>
    
    <div style="margin-bottom:15px;">
      <label style="display:block; margin-bottom:5px; font-weight:bold; font-size:0.85rem;">Rodzaj usterki:</label>
      <select id="calc-issue" required style="width:100%; padding:10px; border-radius:6px; background:#222; border:1px solid #444; color:#FFF;">
        <option value="">-- Co się stało? --</option>
        <option value="Rozbita szybka / wyświetlacz">Rozbity ekran / wymiana szybki</option>
        <option value="Słaba bateria">Wymiana baterii (krótko trzyma)</option>
        <option value="Uszkodzone gniazdo ładowania">Telefon nie ładuje się (uszkodzone USB)</option>
        <option value="Zalany telefon">Telefon po zalaniu / nie włącza się</option>
        <option value="Inny problem">Inna usterka</option>
      </select>
    </div>
    
    <div style="margin-bottom:15px;">
      <label style="display:block; margin-bottom:5px; font-weight:bold; font-size:0.85rem;">Twój Telefon (do wysłania wyceny SMS):</label>
      <input type="tel" id="calc-phone" placeholder="np. 663970016" required style="width:100%; padding:10px; border-radius:6px; background:#222; border:1px solid #444; color:#FFF;">
    </div>
    
    <button type="submit" style="width:100%; padding:12px; background:#007bff; border:none; border-radius:6px; color:#FFF; font-weight:bold; cursor:pointer; transition: background 0.2s;">Odbierz wycenę przez SMS 🚀</button>
  </form>
  <div id="calc-success-msg" style="display:none; margin-top:15px; color:#28a745; font-weight:bold; text-align:center;">Dziękujemy! Twoje zapytanie zostało wysłane. Trwa kalkulacja ceny...</div>
</div>

<script>
document.getElementById('coolfon-calc-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const phone = document.getElementById('calc-phone').value;
  const device = document.getElementById('calc-device').value;
  const issue = document.getElementById('calc-issue').value;
  
  const webhookUrl = 'https://n8n.holisticjson.pl/webhook/coolfon-wycena';
  
  fetch(webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phone, device, issue })
  }).then(res => {
    document.getElementById('coolfon-calc-form').style.display = 'none';
    document.getElementById('calc-success-msg').style.display = 'block';
  }).catch(err => {
    alert('Wystąpił błąd przy wysyłaniu zapytania. Spróbuj zadzwonić: +48532840877');
  });
});
</script>
```

### B. Przepływ n8n (Kalkulator Wyceny -> SMSAPI)
1. **Webhook Trigger:** Odbiera model urządzenia, rodzaj usterki i numer telefonu z formularza.
2. **AI Node (Gemini/Vertex AI):** Na podstawie bazy cennika (pobranej z `/cennik-napraw-telefonow/`) asystent AI szacuje koszt naprawy i generuje treść SMS.
3. **SMSAPI Node:** Wysyła automatyczną wiadomość SMS o treści:
   > *"Cześć! Szacowany koszt naprawy usterki: [Usterka] w Twoim [Model] w serwisie Coolfon to ok. [Cena] zł. Naprawę wykonamy w 1h! Zapraszamy: ul. Opolczyka 17/C6."*

### C. System Powiadomień o Statusie Naprawy (WordPress -> n8n -> SMS)
Aby informować klienta o statusie naprawy, wykorzystamy zdarzenie zmiany statusu zamówienia w bazie WordPress (np. poprzez WooCommerce, wtyczkę serwisową lub zmianę metadanych pola ACF "Status naprawy"):
1. **WordPress Webhook (Wtyczka WP Webhooks lub funkcja w functions.php):** Każda aktualizacja pola `status_naprawy` o wartościach: `Przyjęte` / `W trakcie` / `Gotowy do odbioru` wysyła webhook do n8n.
2. **n8n Router:** Filtruje statusy i wysyła spersonalizowane SMS-y do klienta przez **SMSAPI**:
   - **Gotowy do odbioru:** *"Twój telefon jest już naprawiony i w pełni przetestowany! Zapraszamy po odbiór do serwisu Coolfon na ul. Opolczyka 17. Koszt: [Koszt] zł."*

---
*Przygotowane przez: Holistic OS Agent*
