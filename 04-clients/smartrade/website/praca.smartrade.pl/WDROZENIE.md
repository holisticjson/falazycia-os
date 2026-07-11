# Instrukcja Wdrożenia: praca.smartrade.pl 🚀

Kompletne pliki Twojego landing page zostały wygenerowane i przygotowane do wdrożenia. Poniżej znajduje się krótka i czytelna instrukcja, jak uruchomić stronę na serwerze i połączyć ją z Gemini API w Google AI Studio.

---

## 🛠️ KROK 1: Konfiguracja klucza Gemini API (Google AI Studio)

1. Wejdź na stronę **[Google AI Studio](https://aistudio.google.com/)** (zaloguj się swoim kontem Google).
2. Kliknij niebieski przycisk **"Get API key"** (jak na zrzucie ekranu, który przesłałeś).
3. Kliknij **"Create API Key"**, a następnie wybierz lub utwórz nowy projekt Google Cloud.
4. Skopiuj wygenerowany klucz API (zaczyna się zazwyczaj od `AIzaSy...`).
5. Otwórz plik [api/config.php](file:///c:/Aplikacje%20MVP/Holistic%20Jason/04-clients/smartrade/website/praca.smartrade.pl/api/config.php) na swoim komputerze i wklej skopiowany klucz w linii:
   ```php
   'gemini_api_key' => 'TUTAJ_WKLEJ_TWÓJ_KLUCZ_API',
   ```
6. Zapisz plik. Twój chatbot jest już w pełni bezpieczny (klucz jest ukryty na serwerze PHP i nikt nie podejrzy go z przeglądarki!).

---

## 📂 KROK 2: Przesłanie plików przez FTP

Posiadasz już aktywne konto FTP dla domeny `smartrade.pl` (zgodnie z danymi ze zrzutu ekranu):
*   **Serwer/Host:** `smartrade.pl` (lub IP hostingu)
*   **Logowanie / Użytkownik:** `deploy@smartrade.pl`
*   **Hasło:** `Kosmos!!1234`
*   **Katalog docelowy na serwerze dla subdomeny `praca.smartrade.pl`:** `/domains/praca.smartrade.pl/public_html`

### Jak wgrać pliki?
1. Pobierz darmowy program FTP, np. **FileZilla** lub **WinSCP**.
2. Połącz się za pomocą powyższych danych logowania.
3. Przejdź do folderu `/domains/praca.smartrade.pl/public_html` (jeśli folder `praca.smartrade.pl` lub `public_html` jeszcze nie istnieje, utwórz go w zakładce `domains`).
4. Przeciągnij i upuść **całą zawartość** lokalnego folderu:  
   `c:\Aplikacje MVP\Holistic Jason\04-clients\smartrade\website\praca.smartrade.pl\`  
   bezpośrednio do katalogu `public_html` na serwerze FTP.

---

## 🧪 KROK 3: Testowanie działania

1. Wejdź w przeglądarce pod adres: `https://praca.smartrade.pl`
2. Zobaczysz piękny, słoneczny landing page.
3. Przewiń na dół do sekcji rekrutacyjnej, zaznacz zgodę RODO i kliknij **"Uruchom NabiewBota"**.
4. Przeprowadź z nim krótką rozmowę testową.
5. Spróbuj przejść kwalifikację (podaj imię, glazurnik, doświadczenie, potwierdź brak nałogów). 
6. Bot powinien pogratulować Ci przejścia rekrutacji i wyświetlić zielony przycisk **"Przejdź do rozmowy z Jurkiem na WhatsApp"**.
7. Po kliknięciu zostaniesz przekierowany do aplikacji WhatsApp z gotową, wygenerowaną przez bota wiadomością streszczającą Twój wywiad kwalifikacyjny!

---

## 📣 KROK 4: Kampania w Social Mediach

Pliki z kompletnymi postami reklamowymi oraz profesjonalnym scenariuszem wideo dla Jurka znajdziesz w folderach:
*   📝 **Posty i Karuzela:** [marketing/social_posts.md](file:///c:/Aplikacje%20MVP/Holistic%20Jason/04-clients/smartrade/website/praca.smartrade.pl/marketing/social_posts.md)
*   🎬 **Skrypt Rolki Instagram:** [marketing/reel_script.md](file:///c:/Aplikacje%20MVP/Holistic%20Jason/04-clients/smartrade/website/praca.smartrade.pl/marketing/reel_script.md)

*Powodzenia z rekrutacją! Jurek ma świetną okazję do dowożenia najlepszych ludzi z Polski i wschodu bezpośrednio do pięknej Gandii!* 🌴☀️
