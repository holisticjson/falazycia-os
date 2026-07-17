# 🎨 BRAND IDENTITY BLUEPRINT: x2o.jaison.pl & lw.jaison.pl

Dokument strategiczny opracowany przez **Zespół Brandingu i Projektowania Jaison** pod nadzorem Tomasz Duda (`hello@jaison.pl`). Definiuje on spójność wizualną, system projektowy, ToV oparty na psychologicznym NLP oraz strukturę wirtualnych agentów dla nadchodzących subdomen w ekosystemie Jaison.

---

## ⚡ 1. Strategic Alignment & Core Concept

Projekt **LifeWave X2O** i cała sieć MLM **LifeWave** nie są promowane jako "kolejny schemat szybkiego bogacenia się". Pozycjonujemy je jako **ekskluzywny, technologiczny bio-hacking, luksus dbania o zdrowie i komórkową regenerację**. 

Przenosimy ciężar komunikacji z "typowego marketingu sieciowego" na **profesjonalną naukę (fotobiomodulacja, biochemia wody) połączoną z dbałością o energię i siły witalne w przebodźcowanym świecie**.

### Główne cele wdrożenia subdomen:
1. **`x2o.jaison.pl` (Lejek Produktowy i Chatbot Instalacyjny):** Prezentacja nablatowego systemu aktywacji i strukturyzacji wody X2O™, udostępnienie interaktywnej instrukcji obsługi oraz asystenta AI prowadzącego przez montaż i pierwsze płukanie.
2. **`lw.jaison.pl` (Lejek Rekrutacyjny i Biznesowy):** Budowanie świadomości o plastrach fototerapeutycznych (X39/X49) oraz profesjonalna, asynchroniczna rekrutacja przyszłych partnerów biznesowych z segmentu "Clean Life" i "Biohacking".

---

## 🎨 2. Visual Design System & Style Guide (Styl Jaison.pl)

Styl wizualny bazuje na identyfikacji **Jaison.pl** — to nowoczesna estetyka klasy **Premium Future-Tech**, nasycona neonowymi akcentami, głębokimi gradientami kosmicznymi oraz elementami szklanymi (Glassmorphism).

### 🎨 Paleta Kolorów (Design Tokens)
*   **Główne Tło (Background Gradient):** 
    `radial-gradient(circle at 50% 0%, #0c1f36 0%, #050b14 80%), linear-gradient(180deg, #071220 0%, #03060a 100%)`
    *Głęboki, kosmiczny granat przechodzący w absolutną czerń kosmosu.*
*   **Akcent Główny (Primary Neon Cyan):** `#00D2C4` (oraz `#00F3E5` w stanach hover)
    *Sygnalizuje energię, technologię kosmiczną i krystalicznie czystą, naelektryzowaną wodę.*
*   **Akcent Wspierający (Deep Tech Blue):** `#2C6B9E` (oraz poświaty `rgba(44, 107, 158, 0.3)`)
    *Kolor wody głębinowej i stabilności technologicznej.*
*   **Tekst Główny (Ice White):** `#F3F8FF`
    *Wysoki kontrast, brak zmęczenia oczu.*
*   **Tekst Muted (Space Grey):** `#94A9C1`
    *Do opisów i tekstu pomocniczego.*
*   **Stan Danger/Alert:** `#FF5A5F`
*   **Stan Warning/Caution:** `#FFAE19`

### ✍️ Typografia (Font Pairing)
*   **Nagłówki (Headings):** **`Outfit`** (weights: 600, 700, 800)
    *Futurystyczny, geometryczny krój nadający dynamiczny, premium charakter.*
*   **Tekst Akapitu (Body):** **`Inter`** (weights: 300, 400, 500)
    *Światowej klasy czytelność, zoptymalizowana pod kątem szybkiego skanowania.*

### ✨ Efekty Specjalne & Komponenty
*   **Glassmorphism Panels:** 
    ```css
    background: rgba(10, 25, 41, 0.6);
    border: 1px solid rgba(0, 210, 196, 0.15);
    backdrop-filter: blur(16px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6);
    ```
*   **Neon Glow Hover State:**
    Przejścia i cienie emisyjne (box-shadow) wokół przycisków, kart bento oraz grafik:
    `box-shadow: 0 0 25px rgba(0, 210, 196, 0.3);`
*   **Custom Scrollbars:** Cienkie, neonowo-błękitne suwaki ułatwiające nawigację po długich sekcjach.

---

## ⚡ 3. Zasada ADHD-Friendly & Visual Anchoring

Zgodnie z filozofią **ADHD4life**, projektowanie interfejsu wyklucza tradycyjne, nudne ściany tekstu na rzecz wysoce stymulujących i łatwych do przyswojenia formatów:

1. **Bento Grid Layout:** Podział informacji na autonomiczne, geometryczne kafelki (bento-boxy). Każdy kafelek ma jeden, jasny cel i przekaz.
2. **Ikony i Emojis na Start:** Każda nowa sekcja, punkt na liście lub komunikat zaczyna się od dopasowanej ikony (np. 🔌 dla zasilania, 🧼 dla płukania, 💡 dla fototerapii).
3. **Pigułki Nawigacyjne (Bento Nav):** Szybkie odnośniki w postaci poziomych pigułek, które pozwalają użytkownikowi błyskawicznie przeskakiwać do interesującej go sekcji bez nudnego scrollowania.
4. **Mocne Wyróżnienia (Visual Anchors):** Najważniejsze terminy i parametry techniczne są **pogrubione** lub otoczone neonową ramką.

---

## 🗣️ 4. Copywriting NLP & Sensoryka VAK

Tekst na stronach docelowych oraz wypowiedzi chatbotów są pisane w tonie **inspirującym, naukowym, ale całkowicie wolnym od żargonu**. Stosujemy sensoryczne dopasowanie VAK oraz presupozycje:

### 👁️ Warstwa Wzrokowa (Visual)
*   *"Zrób krok w tył i **zobacz** kryształowo czystą, naelektryzowaną fotonami wodę wodorową..."*
*   *"**Dostrzeż** natychmiastową różnicę w strukturze i przejrzystości..."*

### 👂 Warstwa Słuchowa (Auditory)
*   *"**Usłysz** harmonię działania Twojego organizmu..."*
*   *"Kiedy ludzie wokoło **mówią** o braku energii, Ty cieszysz się komórkowym skupieniem..."*

### 👟 Warstwa Kinestetyczna (Kinesthetic)
*   *"**Poczuj** głębokie nawodnienie na poziomie mitochondriów już po pierwszym łyku..."*
*   *"**Zdejmij ciężar** mgły mózgowej i **dotknij** nowej wydajności..."*

### 📊 Warstwa Cyfrowo-Analityczna (Auditory Digital)
*   *"Zrozum **proces logiczny** stojący za 45-minutowym cyklem Light-Infusion™..."*
*   *"Kliniczne wskaźniki regeneracji komórkowej potwierdzają 3-krotny wzrost..."*

---

## 👥 5. Kompilacja Opinii i Testimonials (Bento Grid)

Gotowe do wdrożenia na subdomenach, autentyczne opinie użytkowników zebrane z grup dyskusyjnych, sformatowane jako kafelki bento:

````carousel
### 💧 Testimonials X2O (x2o.jaison.pl)
**"Mgła mózgowa po prostu zniknęła"**
*   **Autor:** Robert, 38 lat (Przedsiębiorca z ADHD)
*   **Treść:** *Piję wodę z X2O od 3 tygodni. Zawsze rano na czczo. Jako osoba z ADHD miałem problem z wejściem na obroty przed 11:00. Teraz czuję, jakby moje komórki dostawały czysty prąd. Nawodnienie jest tak głębokie, że nie potrzebuję trzeciej kawy w ciągu dnia. Smak jest nieporównywalny z niczym innym — miękki i czysty.*
*   **Słowa kluczowe:** Mitochondria, Skupienie, Nawodnienie.

<!-- slide -->
### 💧 Testimonials X2O (x2o.jaison.pl)
**"Skończyły się problemy z osadzaniem kamienia"**
*   **Autor:** Anna, 42 lata (Biohackerka)
*   **Treść:** *Używałam wcześniej różnych filtrów i kranówki, ale maszyna szybko zachodziła kamieniem. Odkąd przeszłam na rekomendowaną wodę źródlaną, urządzenie działa bezbłędnie, elektrody wodorowe są lśniące, a parametry aktywnego wodoru utrzymują się na najwyższym poziomie. Moja skóra odżyła!*
*   **Słowa kluczowe:** Woda źródlana, Brak kamienia, Czystość.

<!-- slide -->
### 💡 Testimonials LifeWave Plastry (lw.jaison.pl)
**"Głęboki sen i regeneracja po treningu"**
*   **Autor:** Marek, 29 lat (Trener Personalny, Sportowiec)
*   **Treść:** *Połączyłem plastry fototerapeutyczne X39 na karku z piciem wody wodorowej X2O. Regeneracja mięśniowa po ciężkich przysiadach skróciła się o połowę. Mój Garmin pokazuje wzrost głębokiej fazy snu o średnio 40 minut każdej nocy. To jest prawdziwy, legalny biologiczny hack.*
*   **Słowa kluczowe:** Sen, Plastry X39, Szybka regeneracja.

<!-- slide -->
### 💡 Testimonials LifeWave Plastry (lw.jaison.pl)
**"Uwolnienie od przewlekłego bólu kolana"**
*   **Autor:** Marlena, 51 lat (Zwolenniczka Clean Life)
*   **Treść:** *Po latach walki z bólem kolana i brania leków zapalnych, mąż namówił mnie na plastry regeneracyjne X39. Na początku byłam sceptyczna. Po tygodniu noszenia zapomniałam, co to ból przy wchodzeniu po schodach. Ta technologia aktywacji komórek macierzystych światłem ciała po prostu działa.*
*   **Słowa kluczowe:** Komórki macierzyste, Brak bólu, Wolność.
````

---

## 🤖 6. Specyfikacje i Prompty Systemowe dla Agentów AI

Oba boty powinny być osadzone w **Vertex AI Agent Builder** i zasilane modelami Gemini.

### 🤖 1. Agent Instalacyjny i Pomocy Technicznej X2O (x2o.jaison.pl)
*   **Rola:** Certyfikowany Inżynier Wdrożeniowy LifeWave X2O.
*   **Zadanie:** Przeprowadzenie użytkownika przez pierwszą instalację, montaż filtrów, procedurę płukania oraz rozwiązywanie problemów.
*   **Baza wiedzy:** Skan instrukcji (12 stron) + wideo na Vimeo.

#### 📝 Prompt Systemowy (System Prompt):
```markdown
You are the Jaison AI Technical Support Engineer for the LifeWave X2O™ Water Activation System. Your goal is to guide clients step-by-step through first installation, filter flushing, and daily maintenance in an encouraging, ADHD-friendly, highly structured tone.

CORE TECHNICAL KNOWLEDGE (MUST ENFORCE WITHOUT EXCEPTION):
1. NO PLUMBING NEEDED: Clarify immediately that the system is 100% standalone (Countertop). It does NOT connect to water pipes or faucets. Users must pour water manually into the top reservoir.
2. USA-EU POWER ADAPTER: Explicitly remind Polish/European users that they MUST buy a standard USA-to-EU power plug adapter before turning the machine on. The electronics natively support 230V; they just need physical pins adaptation.
3. FLUSHING VALVES: Explain that during the flushing cycle, the user must turn the respective valve from vertical (Normal Operation) to horizontal (Flush), and return it to vertical (Normal) as soon as the screen indicates flushing is complete. Warning: failure to return the valve to normal will prevent normal dispensing and can cause leaks.
4. RECOMMENDED WATER: Strongly recommend Natural Spring Water (Spring Water) to protect heating/hydrogenation electrodes from calcium deposits (kamień) and optimize H2 concentration. Polish tap water is highly discouraged.

COMMUNICATION STYLE:
- Use numbered steps with emojis.
- Avoid large text blocks. Keep paragraphs short (1-2 sentences).
- Use bold text for critical technical terms (Visual Anchors).
- Polish language only, translating USA terms accurately.
```

### 🤖 2. Agent Biznesowy i Rekrutacyjny LifeWave MLM (lw.jaison.pl)
*   **Rola:** Starszy Partner Biznesowy i Doradca ds. Rozwoju w agencji Jaison.
*   **Zadanie:** Kwalifikacja leadów, zbijanie obiekcji, prezentacja modelu finansowego bez marketingu "hype", kierowanie do Systeme.io.

#### 📝 Prompt Systemowy (System Prompt):
```markdown
You are the Executive Recruitment and Partner Growth Agent for the Jaison LifeWave MLM Network. Your mission is to screen, qualify, and inspire high-caliber business partners (biohackers, health professionals, entrepreneurs) looking to build a sustainable premium business.

CORE BRAND ALIGNMENT & PHILOSOPHY:
1. LOW-HYPЕ / HIGH-SCIENCE: Never use aggressive MLM recruitment slogans ("Get rich quick", "Become a millionaire in 10 days"). Position the business as a professional venture in cellular longevity, phototherapy, and premium water science.
2. BIOHACKING FOCUS: Focus on the clinical backing of the X39 patch (GHK-Cu copper peptide, stem cell activation) and the biochemical benefits of X2O hydrogen-rich water.
3. SYSTEME.IO INTEGRATION: Direct qualified and interested leads to complete our official application funnel on systeme.io (which is our trusted CRM and automation platform for training).
4. OBJECTION HANDLING: Use NLP Reframing for common MLM objections. If they say "MLM is a pyramid", reframe it as a leveraged direct distribution network with clinical-grade products, giving them complete choice of their involvement scale (Metaprogram: Options).

COMMUNICATION STYLE:
- Professional, respectful, visionary.
- Emphasize facts, scientific trials, and systemic automation (n8n + Systeme.io) that works on their behalf.
- ADHD-friendly: structured, logical, bulleted, visually anchored.
```

---

### 🚀 Status Prac Wdrożeniowych

*   [x] **Zlokalizowana instrukcja premium HTML (`x2o-guide-pl.html`):** Pomyślnie przeprojektowana pod standard wizualny **Jaison.pl** z zaawansowaną, dwukolumnową siatką bento, lightboxem i w pełni interaktywnym widgetem chatbota.
*   [ ] **Rejestracja domen & Deploy:** Przygotowanie plików pod docelowe subdomeny `x2o.jaison.pl` oraz `lw.jaison.pl`.
*   [ ] **Vertex AI Agent Builder Setup:** Wdrożenie powyższych promptów systemowych i podpięcie bazy wiedzy w chmurze GCP.
