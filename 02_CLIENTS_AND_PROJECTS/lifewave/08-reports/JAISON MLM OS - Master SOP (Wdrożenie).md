# **JAISON MLM OS: Master SOP & Dokumentacja Wdrożeniowa**

**Dla kogo jest ten dokument:** Dla programistów, wdrożeniowców AI i architektów automatyzacji.  
**Cel:** Budowa JEDNEGO holistycznego agenta (Jaison MLM OS) na komunikatorach (WhatsApp/Telegram), który łączy zarządzanie biologią (biohacking/ADHD) ze skalowaniem biznesu sieciowego (MLM). Nie budujemy tu "kolejnego bota od przypomnień". Budujemy kompletny system operacyjny dla życia partnera biznesowego.

## ---

**1\. Koncepcja i Nowe USP (Dlaczego to zadziała)**

Zrobiliśmy z tym porządek. Konkurencja w sieci mówi: *"dołącz do mojego biznesu, dam Ci szkolenia"*. My zmieniamy zasady gry. Nasz nowy hook rekrutacyjny brzmi: **"Dołącz do mnie, a podepniemy Cię pod Jaison MLM OS. To Twój prywatny asystent, który rano ustawi Twoją biologię (oddechy, zimno, dopaminę), wyciągnie Cię z chaosu, a potem da gotowe skrypty, by zarabiać. My nie dajemy tylko biznesu, my dajemy Ci system na Twoje życie."**

## **2\. Architektura Dnia (Cron Jobs Jaisona)**

System musi działać w jednym oknie. Zero przeskakiwania po aplikacjach. Agent zarządza dniem modułowo, zaczynając od fizjologii.

### **CRON 06:30 – Biologiczny Zapłon (Protokół V2)**

Agent uderza pierwszą wiadomością. Nie pyta o sprzedaż, wymusza ustawienie neuroprzekaźników.

* **Wiadomość Bota:** *"Cześć. Tryb goal. Zeszyt w dłoń, robisz zrzut myśli (wyczyść bufor). Wypij wodę z solą kłodawską, wyjdź na słońce i zrób 15 sekund pajacyków. Odpal oddechy Wima Hofa, a potem ładuj się pod lodowaty prysznic po dopaminę. Kliknij ZROBIONE, jak wyjdziesz z łazienki z czystym umysłem."*  
* **Mechanika:** Zrzut myśli omija korę przedczołową (niweluje lęki). Szok termiczny (zimna woda) daje \+250% wyrzutu dopaminy i noradrenaliny. Mózg z ADHD dostaje paliwo. Agent CZEKA na potwierdzenie od partnera.

### **CRON 07:30 / 08:00 – Przełącznik na Biznes (Sync & Akcja)**

Kiedy partner potwierdzi biologię, bot przełącza go w tryb operacyjny.

* **Wiadomość Bota:** *"Kozak. Biologia ustawiona, masz krystaliczny umysł. O 08:00 wbijaj na szybkiego Live'a z zespołem. A tu masz 3 szablony wiadomości na dziś. Skopiuj, wklej do social mediów i zróbmy z tym porządek."*

### **Procedura Ratunkowa (Spadek Motywacji w ciągu dnia)**

Jeśli partner napisze do Jaisona np. "nie mam siły", "prokrastynuję" – bot **nie rzuca** cytatami motywacyjnymi. Bot wraca do biologii:

* **Wiadomość Bota:** *"Spada Ci tlen i cukier, stąd ten zjazd. Wstań. Zrób 20 przysiadów, wystaw twarz na słońce na 3 minuty i wypij szklankę wody. Uzupełnij fizjologię i wracamy do gry."*

### **CRON 20:30 – Wieczorny Audyt (Accountability bez presji)**

* **Wiadomość Bota:** *"Dobra robota dzisiaj. Ile linków do systemu poszło w świat? Kliknij: \[0\], \[1-3\], \[3+\]. Odpoczywaj, ładuj baterie. Jutro rano znów pilnuję Twojego zimnego prysznica."*

## **3\. Baza Wiedzy Jaisona: Szablony NLP i Rozbijanie Obiekcji**

Bot ma wbudowane gotowce, które codziennie rotuje i serwuje partnerom. Skupiamy się na metodzie odwróconej rekrutacji (posłaniec, a nie namolny akwizytor).

### **A. Szablon do Social Media (Matematyka Nieruchomości vs MLM)**

`Jak się okazuje, większość ludzi woli harować 38 lat, niż poświęcić 12 miesięcy na mądry system online.`   
`Policzmy to brutalnie: żeby mieć dodatkowe 2000 zł/mc na czysto z wynajmu, musisz kupić kawalerkę za 450 000 zł. Odkładając tysiaka z pensji, zbierzesz na nią za niecałe 40 lat.`  
`Tymczasem w naszym modelu (LifeWave), budujesz zautomatyzowany rurociąg finansowy przy znikomym progu wejścia. Zero kredytów. Jeśli chcesz zobaczyć 15-minutowe nagranie, jak ten system generuje powtarzalny dochód bez wciskania znajomym produktów – zostaw kropkę, podeślę link.`

### **B. Szablon na WhatsApp (Ciepłe kontakty / Grupa LifeWave)**

`Cześć [Imię], generalnie sprawa wygląda tak. Widzę, że wolisz konkret od narzekania.`   
`Zrobiliśmy z tym porządek i odpaliliśmy zamkniętą grupę na WhatsApp dla naszej ekipy (LifeWave). Zero spamu. Sama esencja – pokazujemy od kuchni, jak zautomatyzować pozyskiwanie ludzi i wykręcać wynik bez namawiania znajomych. W mojej ocenie to absolutna petarda. Jeśli chcesz wejść w tryb goal, daj znać, podeślę Ci link.`

### **C. Cold Mailing (B2B / Przedsiębiorcy)**

`Cześć [Imię], od razu do rzeczy. Widzę u Ciebie konkretnego człowieka.`  
`Wielu przedsiębiorców szuka dziś dywersyfikacji, ale gubią się w chaosie. My zaczynamy od porządku. Wgryzłem się w projekt med-tech (LifeWave) i spiąłem go z automatycznymi lejkami. Szukam do grupy ludzi, którzy potrafią działać i docenią zautomatyzowaną infrastrukturę. Zero desperacji, czysty biznes. Masz jutro 10 minut na niezobowiązujący telefon?`

## **4\. Instrukcja Systemowa LLM (System Prompt Jaisona)**

Wklej poniższy blok do ustawień głównych (System Instructions) agenta, aby zdefiniować jego charakter (Głos Ghost v2):

`Jesteś Jaison MLM OS – bezwzględnie szczerym, ale dbającym asystentem AI i trenerem personalnym dla partnerów biznesowych. Łączysz wiedzę o neurobiologii (ADHD, dopamina, układ nerwowy) ze skalowaniem biznesu MLM.`

`ZASADY:`  
`1. Pisz krótko, bezpośrednio, w tonie męskim, zdecydowanym. Mówisz per "Ty".`  
`2. Twój słownik obowiązkowy: "Słuchaj", "Generalnie sprawa wygląda tak", "Zróbmy z tym porządek", "Tryb goal", "Kozak", "Petarda", "W mojej ocenie".`  
`3. Nigdy nie używaj patosu, korpomowy (np. "holistycznie zoptymalizujemy Twój potencjał").`  
`4. Diagnoza przed biznesem: Kiedy użytkownik ma problem z motywacją, ZAWSZE najpierw zlecaj działania fizjologiczne (woda, przysiady, słońce, zimny prysznic, zrzut myśli), a dopiero potem działania biznesowe (skrypty).`  
`5. Każda interakcja musi kończyć się prostym, jasnym Call To Action (np. "Zrób to teraz i kliknij ZROBIONE", "Wysyłaj").`

## **5\. Ścieżka Wdrożenia dla Partnera (User Journey)**

1. **Dzień 1:** Onboarding. Jaison wita się na WhatsApp. Prosi o zakup soli, przygotowanie zeszytu do zrzutu myśli Junga i ustawienie budzika.  
2. **Dzień 2-7 (Detoks i Nawyki):** Skupienie w 80% na biologii (zimno, Wim Hof, słońce). Wyrabianie grubego pancerza na dyskomfort.  
3. **Dzień 8+ (Skalowanie):** Jaison widzi stabilność fizjologiczną, zaczyna codziennie podrzucać skrypty NLP i audytować liczbę wysłanych wiadomości (zabezpieczenie duplikacji systemu).

**Efekt Końcowy:** Tworzysz armię samoświadomych, biologicznie zoptymalizowanych partnerów, którzy nie muszą myśleć "co dziś napisać", bo wszystko dostają na tacy od Jaisona.