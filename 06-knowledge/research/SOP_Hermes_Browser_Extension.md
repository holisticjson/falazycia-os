# 🌐 SOP: Integracja i Obsługa Hermes Browser Extension v2

Ta procedura opisuje standardy instalacji, bezpieczeństwa oraz zarządzania profilami Chrome przy użyciu wtyczki **Hermes Browser Extension v2**. Wtyczka ta pozwala lokalnemu lub zdalnemu agentowi Hermes OS na bezpośrednią interakcję z przeglądarką użytkownika w trybie na żywo.

---

## 🛠️ 1. Instrukcja Instalacji (Krok po Kroku)

Ponieważ wtyczka jest otwartoźródłowa i nie ma jej jeszcze w oficjalnym Chrome Web Store, instalujemy ją lokalnie jako rozszerzenie deweloperskie:

1.  **Pobierz kod źródłowy:**
    Otwórz PowerShell i sklonuj repozytorium do wybranego katalogu na swoim komputerze:
    ```bash
    git clone https://github.com/abundantbeing/hermes-browser-extension.git
    ```
2.  **Zainstaluj zależności i zbuduj projekt:**
    Wejdź do katalogu projektu i uruchom proces budowania:
    ```bash
    cd hermes-browser-extension
    npm install
    npm run build
    ```
    *Po zakończeniu budowania w katalogu projektu pojawi się podkatalog `dist` zawierający skompilowane pliki rozszerzenia.*
3.  **Załaduj wtyczkę w Chrome:**
    *   Wpisz w pasku adresu przeglądarki: `chrome://extensions/`
    *   Włącz **Tryb dewelopera** (Developer mode) w prawym górnym rogu.
    *   Kliknij przycisk **Załaduj rozpakowane** (Load unpacked) w lewym górnym rogu.
    *   Wybierz folder **`dist`** z nowo sklonowanego projektu.

---

## 👥 2. Zarządzanie Profilami Chrome (Izolacja Klientów)

**Tak, to ma kluczowe znaczenie i jest to ogromna zaleta architektoniczna!**

Chrome pozwala na uruchamianie wielu profili (np. *Tomasz Prywatny*, *Jaison Agencja*, *Klient X*). Profile te są od siebie w 100% odizolowane na poziomie systemu plików i pamięci:
*   **Instalacja na każdym profilu:** Musisz zainstalować rozszerzenie osobno dla każdego profilu Chrome, na którym chcesz korzystać z pomocy Hermesa.
*   **Brak wycieku ciasteczek (Cookies):** Rozszerzenie w profilu *Jaison Agencja* widzi wyłącznie sesje i konta zalogowane na tym profilu. Nie ma fizycznej możliwości, by Hermes pomylił sesje i opublikował post z konta prywatnego na profilu klienta.
*   **Indywidualny Gateway:** W ustawieniach wtyczki na każdym profilu możesz podać ten sam adres bramy (`https://os.jaison.pl`) lub skierować go do innej instancji (np. lokalnego Hermesa deweloperskiego).

---

## 🔒 3. Bezpieczeństwo, Sesje i Ochrona przed Blokadami (Anti-Bot)

Wielką zaletą **Hermes Browser Extension v2** jest to, że **omyka ona wszelkie zapory anty-botowe** (Cloudflare, Google, LinkedIn CAPTCHA):

*   **Brak konieczności podawania haseł:** Agent nie potrzebuje Twoich haseł ani kluczy 2FA do portali społecznościowych. 
*   **Działanie na aktywnych ciasteczkach (Active Cookies):** Wtyczka działa jako "nakładka" na Twoją przeglądarkę. Skoro jesteś już zalogowany w danym profilu Chrome, agent korzysta z Twojej autoryzowanej sesji. Wszystkie polecenia (np. pobranie kodu strony, wysłanie formularza) wyglądają dla serwerów jako wykonane przez prawdziwego człowieka.
*   **Wymagany kontekst:** Hermes potrzebuje wyłącznie:
    1.  Adresu url Gatewaya: `https://os.jaison.pl`
    2.  Klucza API: `API_SERVER_KEY` z Twojego pliku `.env` (nagłówek `X-API-Key`) w celu autoryzacji komunikacji między rozszerzeniem a serwerem.

---

## 🔑 4. Dostęp i Logowanie do Dashboardu (os.jaison.pl)

*   **Brak haseł w interfejsie:** Dashboard na [os.jaison.pl](https://os.jaison.pl) to lekka i dynamiczna aplikacja frontendowa (HTML + JS), która komunikuje się bezpośrednio z backendem FastAPI na serwerze GCP. 
*   **Nginx Reverse Proxy:** Panel jest w pełni dostępny publicznie bez okna logowania, ponieważ służy do wizualizacji procesów i tablicy Kanban. 
*   **Autoryzacja zapytań API:** Każda realna operacja modyfikująca dane (np. wysłanie leada z formularza, wywołanie wtyczki skanującej) przesyła w tle nagłówek `X-API-Key` z kluczem serwera:
    `88db32a9a20e5830d23a01c9c0b82f11696e888c1f251ad631fbbabde6b47d31`
    *(Klucz ten jest zapisany w konfiguracji Twojej wtyczki i plikach systemowych, nie musisz wpisywać go ręcznie na stronie).*
