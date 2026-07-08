# 🔌 WYTYCZNE DLA AGENTA: OPTYMALIZACJA STRON WORDPRESS KLIENTÓW
*Dedykowany Przewodnik Delegowania Zadań — Senior Architect Edition*

---

> [!IMPORTANT]
> **ZASADA PRACY KROK PO KROKU (LOW-FRICTION & VERIFIABLE)**
> - **Połączenie Bezpieczne:** Wszystkie optymalizacje na stronach WordPress klientów agencji wykonujemy bezpośrednio przez natywne **WordPress REST API** z autoryzacją Basic Auth za pomocą wygenerowanych **Haseł Aplikacji** (Application Passwords). 
> - **Nazwa Administratora:** `Holistic OS Agent`
> - **Nazwa Klucza:** `Holistic OS Agent Key` (Hasła i klucze są generowane automatycznie za pomocą panelu DirectAdmin/Hostido lub wpisywane ręcznie przez użytkownika w pliku `.env`).
> - **Brak Modyfikacji Kodu Rdzenia:** Kategorycznie zabrania się modyfikowania plików rdzenia WordPressa oraz instalowania niezweryfikowanych wtyczek zewnętrznych. Wszelkie zmiany treści i metadanych wykonujemy przez standardowe endpointy REST API.

---

## 🎯 Cel Agenta WordPress
Twoim zadaniem jest przeprowadzenie kompleksowego audytu i optymalizacji treści (copywritingu, struktury, czytelności i SEO) dla 4 stron klienckich, tak aby stanowiły one perfekcyjne Case Studies dumni reprezentujące naszą agencję na stronie głównej `jaison.pl`.

---

## 🌐 Domene i Zakres Prac

Prace optymalizacyjne przeprowadzamy sekwencyjnie (jedna strona po drugiej) na następujących witrynach:

### 1. 🍗 `kurczakujasia.pl` (Gastronomia / Grill)
- **Cel:** Optymalizacja pod kątem wyszukiwarek AI (GEO/AIO), poprawa lokalnego SEO w Łodzi oraz integracja asystenta zamówień.
- **Zadania:**
  - Audyt i uproszczenie tekstów menu (webwriting zoptymalizowany dla osób z ADHD — szybkie skanowanie wzrokowe).
  - Wdrożenie struktur danych JSON-LD Schema (LocalBusiness, FoodEstablishment, Menu) w celu poprawy indeksowania przez roboty Google i Vertex AI.
  - Optymalizacja sekcji opinii i wezwań do działania (CTA) zachęcających do zamawiania na miejscu i online.

### 2. 📱 `coolfon.pl` (Serwis GSM / Akcesoria)
- **Cel:** Automatyzacja powiadomień o statusie napraw oraz asystent wyceny serwisu online.
- **Zadania:**
  - Optymalizacja tekstów na stronie głównej pod kątem słów kluczowych "naprawa telefonów Łódź", "serwis GSM".
  - Przygotowanie struktury strony pod kątem automatycznego wysyłania powiadomień SMS (integracja n8n + SMSAPI) po zmianie statusu zamówienia w bazie WordPress.
  - Wdrożenie asystenta wyceny (prosty formularz zintegrowany z webhookiem).

### 3. 🚗 `viptransporter.pl` (Wynajem Premium / Przewozy VIP)
- **Cel:** Całodobowe przechwytywanie i kwalifikacja zapytań o rezerwacje aut.
- **Zadania:**
  - Uproszczenie i uszlachetnienie copywritingu (styl "Quiet Luxury" — krótko, konkretnie, elitarnie).
  - Optymalizacja ścieżki rezerwacji (usuwanie tarcia, prosty formularz kontaktowy spięty przez n8n z CRM i Systeme.io).
  - Wdrożenie mikrodanych Schema (TaxiService / CarRental).

### 4. 🧘 `swiatyniaharmonii.pl` (Gabinet Masażu / Relaks)
- **Cel:** Optymalizacja rezerwacji sesji oraz asystent harmonii.
- **Zadania:**
  - Przeredagowanie oferty na styl kojący, minimalistyczny i czytelny.
  - Integracja formularza rezerwacji terminów bezpośrednio z kalendarzem n8n/Google Calendar.

---

## 🛠️ Procedura Integracji WordPress REST API (Techniczna)

Wszelkie zapytania API wykonujesz według poniższego standardu:

```python
# Przykład autoryzacji i pobierania wpisów / stron w Pythonie
import requests
import base64

wp_user = "Holistic OS Agent"
wp_app_password = "xxxx xxxx xxxx xxxx"  # Pobierz z .env

# Kodowanie nagłówka Basic Auth
credential_token = f"{wp_user}:{wp_app_password}"
encoded_credentials = base64.b64encode(credential_token.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/json"
}

# Pobranie stron do audytu
domain = "https://kurczakujasia.pl"
response = requests.get(f"{domain}/wp-json/wp/v2/pages", headers=headers)

if response.status_code == 200:
    pages = response.json()
    print("Połączenie z WordPress REST API pomyślne!")
```

## 📝 Instrukcja Raportowania Prac
Dla każdej optymalizowanej domeny stwórz i zapisz raport z wdrożenia w folderze klienta (np. `clients/kurczakujasia/opt_report.md`):
1. **Stan Przed (Audit):** Co było nie tak z copywritingiem, strukturą lub SEO.
2. **Wykonane Zmiany (Diff/Details):** Konkretne zmiany wprowadzone w tekstach lub strukturze nagłówków.
3. **Wdrożona Schema:** Gotowy kod JSON-LD, który został wstrzyknięty na stronę.
4. **Wskazówki dla n8n:** Dokładne parametry formularzy i webhooków niezbędne do zapięcia automatyzacji.
