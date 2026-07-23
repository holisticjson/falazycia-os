---
name: gcp-startup-credits-sop
description: Standard Operacyjny (SOP) oraz checklista zgodności (Compliance Checklist) dla wniosków o środki i kredyty Google Cloud for Startups ($300 - $350k+). Zapobiega odrzuceniu aplikacji przez automatyczne i manualne filtry Google Cloud Operations.
---

# 🚀 SOP: Google Cloud Startup Program Compliance & Credit Application Guide

Niniejszy dokument stanowi kanoniczny Standard Operacyjny (SOP) agencji **Jaison** oraz projektu **Holistyczny Broker**. Określa zasady przygotowania witryny internetowej oraz procedurę składania wniosków o darmowe środki chmurowe i kredyty w ramach programu **Google Cloud for Startups** (oraz pokrewnych grantów chmurowych GCP).

---

## 🎯 1. Cel i Kluczowe Budżety Chmurowe Google

Podczas realizacji projektów własnych oraz klienckich aplikujemy o następujące pakiety wsparcia:
1. **$300 Free Trial Credit** (Startowe środki na koncie GCP).
2. **$1,000 GenAI App Builder Credit** (Darmowe środki na Vertex AI Search & RAG Engine).
3. **Google Cloud for Startups Grants** ($2,000 do $350k+ w zależności od etapu startupu).

---

## ⛔ 2. Trzy Główne Przyczyny Odrzucenia Wniosków (Google Compliance Filters)

W oparciu o oficjalne wytyczne zespołu *Startup Support Operations (Concentrix / Google Cloud)*, wniosek zostaje natychmiast odrzucony, jeśli zgłoszona domena wpada w jedną z poniższych kategorii:

### A. Niedostępność Strony (`Inaccessible`)
- Strona nie ładuje się, wypluwa błędy serwera (np. `404 Not Found`, `502 Bad Gateway`, `500 Server Error`).
- Strona jest ukryta za ekranem logowania, wymaga konta demo bez podanych danych dostępowych lub jest zablokowana hasłem deweloperskim.
- Brak aktywnego i poprawnego certyfikatu SSL (`https://`).

### B. Niekompletność / Zaślepka (`Incomplete`)
- Strona zawiera wyłącznie nagłówek i formularz *"Dołącz do listy oczekujących" (Join Waitlist)* lub *"Poproś o demo" (Request Demo)* **bez prezentacji działającego produktu**.
- Strona wygląda jak szablony typu "Coming Soon", placeholder lub generyczna wizytówka marketingowa bez konkretów.
- Brak pokazanego żywego interfejsu (Live Launched Product Showcase) – Google wymaga dowodu, że aplikacja/usługa faktycznie istnieje i działa.

### C. Brak Możliwości Weryfikacji Zespołu i Firmy (`Unverifiable`)
- Brak dedykowanej sekcji *"O nas / Zespół"* z autentycznymi informacjami o założycielach i kluczowych pracownikach.
- Brak linków do zweryfikowanych profili biznesowych (np. LinkedIn założyciela).
- Brak oficjalnych danych rejestrowych firmy w stopce (KRS / NIP / REGON, oficjalny adres rejestrowy).
- Brak wymaganych podstron prawnych: Polityka Prywatności (Privacy Policy) oraz Regulamin (Terms of Service) z checkboxami GDPR/RODO.

---

## 📋 3. Checklista Przed-Zgłoszeniowa (Pre-Flight Audit Checklist)

Przed wysłaniem wniosku o kredyty startupowe dla jakiejkolwiek domeny (własnej lub klienta), **agent ma bezwzględny obowiązek przeprowadzić poniższy audyt**:

### 🔍 Krok 1: Weryfikacja Techniczna i Dostępności
- [ ] Domena główna oraz wariant `www` ładują się szybko bez błędów.
- [ ] Certyfikat SSL jest aktywny i ważny.
- [ ] Strona jest dostępna publicznie bez konieczności wpisywania haseł.
- [ ] Działa poprawnie w trybie Incognito (przetestowane bez ciasteczek sesyjnych).

### 🖥️ Krok 2: Prezentacja Produktu (Live Product Interface)
- [ ] Na stronie głównej lub podstronie produktowej znajdują się **zrzuty ekranu, wideo demo lub interaktywne elementy** pokazujące realny panel/interfejs aplikacji.
- [ ] Przycisk akcji (CTA) prowadzi do działającego demo, darmowego okresu próbnego lub aktywnej usługi (a nie tylko do zapisu na listę oczekujących).
- [ ] Prezentacja funkcji opisuje konkretne wartości technologiczne i zastosowanie AI / GCP.

### 👤 Krok 3: Weryfikacja Tożsamości i Legal compliance
- [ ] Dedykowana sekcja *"O nas"* zawiera imię, nazwisko, zdjęcie oraz biografię założyciela (np. Tomasza) oraz kluczowych osób.
- [ ] Podane są odnośniki do profili LinkedIn.
- [ ] W stopce widnieją pełne dane rejestrowe podmiotu gospodarczego (Nazwa, NIP, REGON, KRS / CEIDG, Adres).
- [ ] Dostępne są aktywne linki do **Polityki Prywatności** i **Regulaminu**.
- [ ] Adres e-mail użyty we wniosku pochodzi z domeny firmowej (np. `hello@jaison.pl` lub `kontakt@holistycznybroker.pl`), a nie z darmowej skrzynki gmail.com.

---

## 🔄 4. Procedura Re-aplikacji po Odmowie (Re-apply Workflow)

Jeśli wniosek został wcześniej odrzucony:

1. **Wdrożenie poprawek na stronie:** Uzupełnij brakujące sekcje (opis produktu, widoki panelu, dane zespołu, KRS, regulaminy).
2. **Audyt ponowny:** Uruchom pełną checklistę z Punktu 3.
3. **Czysta Re-aplikacja:**
   - Otwórz okno prywatne/incognito przeglądarki (aby wyeliminować pamięć podręczną formularza Google).
   - Zaloguj się na oficjalne konto konsoli GCP przypisane do danej organizacji/firmy.
   - Wypełnij wniosek ponowny w portalu Google Cloud for Startups, podając adres zaktualizowanej witryny i służbowy e-mail domenowy.
