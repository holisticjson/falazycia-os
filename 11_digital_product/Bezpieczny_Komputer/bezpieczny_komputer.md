COVER PAGE E-book & Poradnik Praktyczny

# Bezpieczny Komputer

Prywatna Twierdza: Jak skutecznie zabezpieczyć, odciążyć i zoptymalizować system Windows bez zbędnych programów obciążających RAM i procesor

Tomasz | J(AI)SON — ADHD-friendly systems architect

 INTRO 

## Wstęp: Iluzja ochrony, która pożera Twój sprzęt

Słyszysz głośny szum wentylatora? Widzisz ten wskaźnik myszy kręcący się w nieskończoność? Czujesz narastającą frustrację, gdy proste otwarcie nowej karty w przeglądarce trwa wieczność, a system informuje Cię o braku wolnej pamięci RAM?

Większość użytkowników Windowsa w dobrej wierze instaluje zewnętrzne "tarcze ochronne" i "optymalizatory". Zewnętrzne pakiety antywirusowe oraz programy czyszczące obiecują bezpieczeństwo i porządek. Rzeczywistość jest jednak brutalna: te programy same często zachowują się jak pasożyty. Stale działają w tle, wysyłają gigabajty telemetrii, bombardują powiadomieniami reklamowymi i pożerają cenne zasoby procesora oraz pamięci RAM.

**Ten e-book zmieni wszystko.** Pokażę Ci, jak przywrócić komputer do stanu pełnej wydajności, budując wokół niego "Prywatną Twierdzę" – bez ciężkich programów i bez wydawania złotówki. Uwolnisz zablokowany RAM, odciążysz procesor, zaszyfrujesz połączenie sieciowe ultralekkim tunelem i zablokujesz reklamy u samego źródła. Wszystko za pomocą wbudowanych systemowo mechanizmów i lekkich narzędzi Open Source.

 CHAPTER 1 

## Rozdział 1: Wielkie odgracanie, czyli pożegnanie z antywirusowym bloatware

Pierwszym krokiem do odzyskania wydajności komputera jest usunięcie zewnętrznego oprogramowania, które dubluje funkcje systemowe. Współczesne systemy Windows 10 i 11 posiadają już wbudowane, doskonałe i całkowicie bezpłatne rozwiązanie ochronne.

### Dlaczego ciężkie programy ochronne i optymalizatory w tle to pułapka?

* **Dublowanie procesów:** Zewnętrzny pakiet antywirusowy walczy o te same zasoby i uprawnienia co wbudowane zabezpieczenia systemowe, co wywołuje mikrozacięcia systemu.
* **Zbędny start:** Programy czyszczące instalują usługi monitorujące, które stale sprawdzają pliki w tle, bezustannie zużywając pamięć RAM.
* **Telemetria i reklamy:** Tego typu oprogramowanie często rejestruje Twoją aktywność sieciową i wysyła raporty, obciążając łącze oraz wyświetlając irytujące powiadomienia zachęcające do zakupu wersji płatnej.

                Instrukcja: Bezpieczne odinstalowanie zbędnych programów
            

Aby trwale usunąć zbędne oprogramowanie antywirusowe i optymalizacyjne z komputera:

1. Naciśnij na klawiaturze skrót **Windows + R**, wpisz appwiz.cpl i kliknij Enter.
2. Na liście zainstalowanych aplikacji znajdź programy ochronne lub czyszczące firm trzecich, których chcesz się pozbyć.
3. Kliknij na niego prawym przyciskiem myszy i wybierz **Odinstaluj**.
4. Postępuj zgodnie z instrukcjami deinstalatora. Jeśli zostaniesz zapytany o powód, wybierz dowolną opcję. Na koniec **zrestartuj komputer**.

![Ekran odinstalowania programów w Windows](deinstalacja_programow.png)

Rys. 1. Klasyczny panel usuwania zbędnych aplikacji w systemie Windows.

### Co w zamian? Zabezpieczenia Windows (Defender)

Po odinstalowaniu zewnętrznego antywirusa, system Windows automatycznie aktywuje wbudowane **Zabezpieczenia Windows (Windows Defender)**. Jest to rozwiązanie klasy enterprise, które regularnie wygrywa w niezależnych testach bezpieczeństwa (np. AV-TEST).

Działa bezpośrednio w jądrze systemu, dzięki czemu nie wymaga uruchamiania ciężkich procesów nakładkowych. Uruchamia się w tle tylko podczas zapisu/odczytu plików i nie wpływa negatywnie na płynność pracy.

 CHAPTER 2 

## Rozdział 2: Sieciowa tarcza bez obciążenia: Cloudflare WARP i DNS

Gdy Twój system jest już czysty, czas zabezpieczyć ruch internetowy. Zamiast instalować ciężkie VPN-y, które dławią przepustowość łącza i obciążają procesor ciągłym szyfrowaniem, wdrożymy ultralekkie rozwiązanie sieciowe.

Przed wyborem odpowiedniej metody warto zrozumieć fundamentalną różnicę w działaniu obu tych usług od Cloudflare. Poniższa tabela wyjaśnia, jak działają i kiedy z nich korzystać:

FunkcjaCloudflare WARP (Aplikacja)Ręczna zmiana DNS (1.1.1.2)**Szyfrowanie ruchu**TAK (cały ruch z Twojego komputera jest w pełni szyfrowany)NIE (tylko same zapytania o adresy stron są zabezpieczone)**Maskowanie adresu IP**TAK (strony www widzą adres serwera Cloudflare zamiast Twojego)NIE (strony internetowe nadal widzą Twój prawdziwy adres IP)**Filtrowanie Malware**TAK (automatyczna blokada zagrożeń)TAK (blokuje złośliwe domeny u samego źródła zapytań)**Obciążenie sprzętu**Minimalne (działa jako bardzo lekka usługa systemowa w tle)Zerowe (czysta konfiguracja Windowsa, brak aplikacji w tle)

### 1. Cloudflare WARP (1.1.1.1) — Szybki i darmowy tunel

**Cloudflare WARP** to aplikacja, która chroni Twoją prywatność w sieci poprzez przekierowanie ruchu przez globalną, zoptymalizowaną sieć Cloudflare przy użyciu nowoczesnego, ultralekkiego protokołu **WireGuard**. Szyfruje Twoje dane, chroniąc Cię np. w publicznych sieciach Wi-Fi, nie powodując przy tym zauważalnego zużycia procesora i pamięci RAM. Oficjalną aplikację możesz pobrać bezpośrednio ze strony **1.1.1.1**.

                Jak uruchomić Cloudflare WARP na Windows krok po kroku:
            

1. Otwórz przeglądarkę internetową, wpisz w pasku adresu **1.1.1.1** i przejdź na stronę.
2. Kliknij przycisk **Windows**, aby pobrać instalator dla swojego systemu.
3. Uruchom pobrany plik i przejdź przez standardowy proces instalacji.
4. Po zainstalowaniu i pierwszym uruchomieniu programu, na ekranie powitalnym wybierz opcję po lewej stronie: **Przeglądanie prywatne** (Nie wymaga rejestracji) i kliknij przycisk **Akceptuj warunki i kontynuuj**.
5. Następnie, w prawym dolnym rogu paska zadań (obok zegarka) kliknij ikonę szarej chmurki Cloudflare i kliknij suwak, aby połączyć się z siecią. Gdy ikona zmieni kolor na pomarańczowy, a status wskaże **Połączono** – Twoje połączenie i adres IP zostaną w pełni zabezpieczone.

![Rys. 2a. Wpisanie adresu 1.1.1.1](warp_step1.png)

![Rys. 2b. Pobieranie wersji dla Windows](warp_step2.png)

![Rys. 2c. Akceptacja warunków w aplikacji](warp_step3.png)

![Rys. 2d. Cloudflare WARP Połączono](warp_connected_win.png)

Rys. 2a-2d. Proces instalacji, konfiguracji i uruchomienia Cloudflare WARP na systemie Windows.📊 Wpływ Cloudflare WARP na prędkość łącza — czego się spodziewać?

Korzystanie z szyfrowania i tunelowania ruchu (jak w każdym VPN) wiąże się z narzutem technologicznym. Choć Cloudflare WARP jest jednym z najszybszych rozwiązań na rynku, musisz liczyć się z nieznacznym obniżeniem niektórych parametrów sieci.

Oto przykład rzeczywistego testu na szybkim łączu światłowodowym:

* **Opóźnienie (PING):** Wzrost jest praktycznie niezauważalny (w tym przypadku zaledwie z **9 ms** na **10 ms**), co gwarantuje błyskawiczną reakcję stron i stabilną pracę.
* **Wysyłanie (UPLOAD):** Spadek jest marginalny (z **102 Mb/s** do **91 Mb/s**).
* **Pobieranie (DOWNLOAD):** Następuje ok. 3-krotny spadek prędkości (z **569 Mb/s** do **202 Mb/s**). Wynika to z przetwarzania pakietów oraz limitów przepustowości bramek wyjściowych Cloudflare.

**Czy to problem?** Zdecydowanie nie. Prędkość na poziomie **200 Mb/s** jest nadal gigantyczna i w zupełności wystarcza do jednoczesnego oglądania kilku filmów w jakości 4K, pobierania dużych plików oraz bezproblemowej pracy programistycznej. W zamian otrzymujesz bezcenną prywatność, ochronę przed malware i pełne szyfrowanie ruchu.

![Rys. 2e. Test prędkości bez Cloudflare WARP](speedtest_without_warp.png)

![Rys. 2f. Test prędkości z aktywnym Cloudflare WARP](speedtest_with_warp.png)

Rys. 2e-2f. Porównanie prędkości łącza przed i po włączeniu usługi Cloudflare WARP.

### 2. Bezpieczny DNS chroniący przed złośliwym oprogramowaniem (1.1.1.2)

Jeśli wolisz całkowicie zrezygnować z instalowania dodatkowych aplikacji w tle, możesz skonfigurować bezpieczny serwer DNS bezpośrednio w ustawieniach sieciowych Windowsa.

Cloudflare oferuje specjalną, bezpłatną usługę DNS o nazwie **1.1.1.1 for Families**, która automatycznie blokuje znane złośliwe domeny (malware, phishing, ransomware) na poziomie sieci, zanim strona w ogóle zacznie się ładować na Twoim komputerze.

⚙️ Konfiguracja DNS w systemie Windows krok po kroku:

1. Naciśnij skrót klawiszowy **Windows + R**, wpisz w okienku polecenie ncpa.cpl i zatwierdź wciskając Enter (spowoduje to natychmiastowe przejście do klasycznego panelu połączeń sieciowych).
2. Kliknij prawym przyciskiem myszy na swoje aktywne połączenie (zazwyczaj **Wi-Fi** lub **Ethernet**) i wybierz **Właściwości**.
3. Na liście zaznaczonych składników znajdź i kliknij dwukrotnie w pozycję **Protokół internetowy w wersji 4 (TCP/IPv4)**.
4. W dolnej części okna zaznacz opcję **Użyj następujących adresów serwerów DNS**.
5. Wpisz odpowiednio adresy filtrujące:
                    
                    • Preferowany serwer DNS: 1.1.1.2
                    • Alternatywny serwer DNS: 1.0.0.2
6. Zaznacz opcję *Zatwierdź ustawienia przy wyjściu* i kliknij **OK** w obu otwartych okienkach.

![Rys. 3a. Wybór karty sieciowej](dns_step1.png)

![Rys. 3b. Właściwości karty](dns_step2.png)

![Rys. 3c. Wybór IPv4](dns_step3.png)

![Rys. 3d. Wpisanie DNS](dns_step4.png)

Rys. 3a-3d. Konfiguracja bezpiecznych serwerów DNS w protokole TCP/IPv4 krok po kroku. CHAPTER 3 

## Rozdział 3: Walka o każdy megabajt RAM-u: Usypianie nieaktywnych kart

Głównym pożeraczem pamięci RAM w nowoczesnych komputerach są przeglądarki internetowe. Każda otwarta karta (zwłaszcza z mediami społecznościowymi czy aplikacjami webowymi) potrafi zużywać od 100 MB do nawet 1 GB pamięci RAM. Jeśli masz otwartych 20-30 kart, Twój komputer szybko dostanie zadyszki.

### Krok 1: Wbudowana funkcja oszczędzania pamięci (Chrome / Edge)

Zarówno Google Chrome, jak i Microsoft Edge posiadają wbudowane mechanizmy usypiania nieaktywnych kart. Aby je aktywować w Google Chrome:

1. Kliknij **trzy pionowe kropki** w prawym górnym rogu przeglądarki i wybierz **Ustawienia**.
2. W lewym menu kliknij zakładkę **Wydajność**.
3. Włącz suwak przy opcji **Oszczegnanie pamięci** (Memory Saver).

Od teraz karty, których nie dotykałeś przez dłuższy czas, zwolnią pamięć RAM. Zostaną ponownie załadowane dopiero w momencie, gdy na nie klikniesz.

⚡ Wtyczka Auto Tab Discard — Agresywne uwalnianie RAM-u

Wbudowane narzędzia przeglądarek bywają mało agresywne – usypiają karty dopiero po kilku godzinach bezczynności. Aby kontrolować ten proces w 100%, zainstaluj darmowe, bezpieczne i otwartoźródłowe rozszerzenie **Auto Tab Discard** w sklepie Chrome Web Store.

Pozwala ono na:

* Ustalenie precyzyjnego czasu (np. automatyczne usypianie kart już po 3 minutach bezczynności).
* Automatyczne ignorowanie kart, na których aktualnie odtwarzany jest dźwięk, wideo lub w tle przesyłany jest formularz.
* Możliwość ręcznego uśpienia wszystkich kart jednym kliknięciem.

![Rys. 4a. Auto Tab Discard w Chrome Web Store](autotab_step1.png)

![Rys. 4b. Ustawienia czasu usypiania i favikony](autotab_step2.png)

![Rys. 4c. Zapisanie ustawień wtyczki](autotab_step3.png)

Rys. 4a-4c. Konfiguracja wtyczki Auto Tab Discard w przeglądarce krok po kroku. CHAPTER 4 

## Rozdział 4: Konserwacja bez obciążenia — BleachBit (Open Source)

Większość z nas przyzwyczaiła się do używania programów czyszczących, które stale działają w tle i natarczywie przypominają o usunięciu ciasteczek. To sprzeczność – program mający przyspieszyć system sam go spowalnia, zużywając procesor.

Rozwiązaniem jest **BleachBit** – darmowy, otwartoźródłowy (Open Source) program do czyszczenia dysku. Jest niezwykle lekki, nie instaluje żadnych usług działających w tle, nie zbiera danych telemetrycznych i uruchamia się wyłącznie wtedy, gdy sam zdecydujesz o potrzebie "posprzątania" komputera.

⚙️ Jak bezpiecznie oczyścić komputer za pomocą BleachBit

1. Wejdź na oficjalną stronę **bleachbit.org**, pobierz i zainstaluj program.
2. Uruchom BleachBit. W lewej kolumnie zobaczysz listę elementów do wyczyszczenia.
3. Zaznacz opcje takie jak: *System -> Pamięć podręczna*, *System -> Tymczasowe pliki* oraz pamięć podręczną używanych przeglądarek.
4. **Wskazówka bezpieczeństwa:** Unikaj zaznaczania opcji *Wolne miejsce na dysku* (zajmuje to bardzo dużo czasu i nie zwalnia realnie miejsca) oraz haseł w przeglądarkach, aby ich nie utracić.
5. Kliknij przycisk **Podgląd** w lewym górnym rogu, aby zobaczyć, ile miejsca zostanie zwolnione. Następnie kliknij **Wyczyść**.

![Rys. 5a. Strona główna pobierania BleachBit](bleachbit_step1.png)

![Rys. 5b. Wybór wersji na system Windows](bleachbit_step2.png)

![Rys. 5c. Proces czyszczenia systemu](bleachbit_step3.png)

Rys. 5a-5c. Proces pobierania, wyboru systemu operacyjnego oraz konfiguracji czyszczenia w aplikacji BleachBit.⚡ Podsumowanie korzyści Twojej Twierdzy

* **Odzyskany RAM:** Usunięcie ciężkich procesów działających stale w tle oraz agresywne usypianie nieaktywnych kart w przeglądarce uwalnia od 4 do nawet 8 GB pamięci operacyjnej.
* **Zwolniony procesor (CPU):** Brak nieustannego, dublującego się skanowania w tle przez zbędne programy ochronne. Twój komputer staje się cichszy i chłodniejszy.
* **Ochrona bez spowolnień:** Wbudowany antywirus systemowy chroni pliki na poziomie jądra, a Cloudflare WARP / DNS zabezpiecza połączenie sieciowe u samego źródła.
* **Brak śmieci w tle:** BleachBit czyści dysk na Twoje żądanie, nie rezerwując dla siebie ani jednego cyklu procesora podczas codziennej pracy.
 FOOTER 
            Tomasz | J(AI)SON — ADHD-friendly systems architect • E-book: Bezpieczny Komputer - Prywatna Twierdza • Wszystkie Prawa Zastrzeżone • 2026