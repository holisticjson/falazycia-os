# 🕵️‍♂️ Raport: Inwentaryzacja Wiedzy i Detektor Chaosu

Witaj! Zgodnie z poleceniem, nie dotykałem, nie modyfikowałem, ani nie usuwałem jeszcze żadnych plików. Zeskanowałem strukturę Twojego katalogu `C:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw` i kilku okolicznych miejsc, aby przygotować diagnozę aktualnego stanu bazy wiedzy. Przeanalizowałem też Twój stary folder `Baza_Wiedzy`. 

Oto raport z mojego audytu:

---

## 1. INWENTARYZACJA I MAPA WIEDZY (Co my tu mamy?)

Twoja baza wiedzy zawiera sporo świetnych materiałów, ale wygląda na zrzut ekranu wszystkiego, co gromadziłeś przez ostatni czas. System bazuje na folderze `02_knowledge_base\raw` i składa się z:

### 🎓 Twórcy i Autorzy (Zidentyfikowani po folderach)
1. **Mirek Burnejko / AI Biznes Lab** - Pliki z dysku Google (np. *Mój AI CTO wywalił się na plecy* z maja).
2. **Jan Szopa / Akademia Zdalnej Agencji Marketingowej** - Duży zrzut z kursem o sprzedaży i psychologii, w tym transkrypcje bonusów.
3. **Adrian Kilar Motion** - Tematy montażu, AI, napisów i transkrypcji (znalazłem m.in. transkrypcje dla kursu AI MASTER).
4. **Google (Umiejętności Jutra 3.0)** - Duża i aktualna baza (częściowo już przez nas ogarniana wizualnie w formacie map myśli).
5. **Alex Hormozi** - Wiedza ogólna o biznesie (prawdopodobnie transkrypcje, notatki, prompty lub e-booki).
6. **Dan Koe** - Materiały skupiające się na Psychologii Sprzedaży i Marketingu.
7. **Iman Gadzhi** - Make Money Challenge (widziałem sporo workbooków).
8. **Jacek Wiśniowski (sukces_pl)**
9. **Klaudia Stawiarska**
10. **Dariusz Kowalski**
11. **Marcin Skiba**
12. **Michał Pietraś** - E-Commerce 1 produkt oraz "Zakazany Długopis".
13. **Mirek Skwarek**

### 🧠 Technologie i Narzędzia
- **GHL_University** - Wiedza stricte powiązana z GoHighLevel (plus Twoje stare skrypty w `Baza_Wiedzy` jak `ghl_library_extractor.js` czy `diagnostyka_ghl.js`).
- **Claude_Skills** - Całe repozytoria AI-Toolkit z GitHuba, dużo plików Markdown (`SKILL.md`).
- **Prompty & LLM** - Folder z bazami promptów i np. informacjami o AWS Bedrock (logi błędów *4279_Service_Quotas*).
- **Gemini_API_omówienia**

### 📂 Obszary Biznesowe / Pozostałe Szuflandie
- **Raporty / Raporty Rynkowe Analizy**
- **Pisanie E-booków**
- **Sztuczna Inteligencja Inspiracje Prompty Skille**
- **Agenci A.I.** / **Biznes AI - Pomysły Inspiracje**
- **ADHD** (Posiadasz m.in. `dopamine_journal.json`, `vocabulary.json`, `scratchpad.md`).
- **Localo_Wiedza**

---

## 2. DETEKTOR CHAOSU I DUPLIKATÓW

Znalazłem obszary, gdzie panuje bałagan i duplikaty. Ze względu na zrzucanie plików prawdopodobnie pobieranych kilkukrotnie (Chrome potrafi tworzyć duplikaty `(1)`, `(2)`), system zawiera powtórzenia:

*   **Zduplikowane pliki PDF/MD:**
    *   `1.1_Opis kursu.md` występuje w systemie aż **21 razy** (zapewne wygenerowany przez nas/skrypt przy pobieraniu lekcji z Google Umiejętności Jutra).
    *   Pliki z kursów Jana Szopy/Mireka Skwarka (np. `Lekcja_1___Sztuczna_Inteligencja.md`, `Dzień_1.md`) występują po **2 razy**.
    *   Wiele ogólnych dokumentów ma duplikaty (np. `Viralowe Hooki.md`, `PDF Masterclass - Nisze.md`, `Prompty Dłuższe Teksty do Social Media.md`).
*   **Stare, "zombiakowe" foldery:**
    *   Istnieje stary katalog `C:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy`. Obecnie zawiera parę starych skryptów JS (`diagnostyka_ghl.js`, `saas_operational_auditor.js`) i starą sub-kategorię ADHD. Prawdopodobnie powinniśmy te skrypty przenieść do `99_workspace/scratch`, a całą resztę zunifikować w głównym `02_knowledge_base`.
*   **Chaos repów z GitHuba (Claude Skills):**
    *   Gdzieś zassałeś w całości paczki skilli na swój dysk (w folderze `Claude_Skills`). Jest to ogromny zbiór plików typu `SKILL.md` (jest ich w systemie aż **108**!), a także zduplikowane podfoldery `ai-toolkit-main`. To bardzo zaciemnia obraz dla AI (system wyszukuje kod np. w ignorowanych plikach `.npmignore` czy `CODEOWNERS`).
*   **Zduplikowane transkrypcje:**
    *   U Jana Szopy znalazłem podwójnie zapisane `Psychologia_Sprzedaży_-_Transkrypcja.md`.
    *   Ten sam plik powtarza się w folderze `Bonusy` i `Kurs Sprzedaży`.
*   **Puste / Śmieciowe Pliki:**
    *   Występują całkowicie (lub w 95%) puste pliki (np. szkielety z dysku google, puste `.md` o wielkości poniżej 100 bajtów u Jana Szopy typu *Dostęp do platformy.md* czy skopiowane `.npmignore`).

---

## 3. PROPOZYCJA STRUKTURY "WIKI" (Podział według metody Pawła Tkaczyka)

Metoda P. Tkaczyka (lub Zettelkasten/PARA) stawia na szybki dostęp do akcji, a nie gromadzenie "na zapas". Zaprojektowałem strukturę sztywnych 4 szuflad:

### 🗄️ `02_knowledge_base\00_RAW` (Poczekalnia / Zrzut)
Tutaj powinny zostać i leżeć odłogiem:
- `Twórcy_Wiedza/` (Katalog dla Jana Szopy, Burnejko, Hormozi, Gadzhi, Kilar). Trzymamy to skatalogowane tylko po nazwisku twórcy.
- `Transkrypcje/` (Wszystkie raw-teksty zrzucane z Youtube/Vimeo).
- Pliki `.json` wyciągane scraperem wtyczki (dopóki z nich nie wygenerujemy Wiki).

### 🗄️ `02_knowledge_base\01_SKILLS_PROMPTS` (Narzędziownia)
Tutaj wciągniemy rzeczy użyteczne, ułożone w logiczne kategorie (nie po nazwisku twórcy, ale po funkcji):
- `Prompty_SocialMedia/`
- `Frameworki_Sprzedazowe/` (BANT, MEDDIC, SPIN).
- Wyodrębnione czyste zasady i najlepsze `SKILL.md` (reszta plików od Claude out do kosza).

### 🗄️ `02_knowledge_base\03_WIKI\Procedury` (Tylko wiedza w działaniu)
Tutaj przeniesiemy i zsyntezujemy pliki, które mówią systemom JAK coś robić:
- `Procedura_Pozyskiwania_Leadów_GHL.md`
- `Procedura_Ingestu_Kursu.md`
- `Szkielety_Scenariuszy_n8n.md`

### 🗄️ Aktualizacja Ról w `.agents\rules` lub `.roo\rules`
Na podstawie Twoich zebranych materiałów musimy uaktualnić instrukcje agentów:
1. **GHL Architect:** Musimy wpompować w niego strukturę SaaS GHL, którą już posiadasz (baza wiedzy z University).
2. **Content Creator / Copywriter:** Zbudować go w oparciu o frameworki Hormoziego i materiały od M. Skwarka.
3. **CEO Orkiestrator:** Podpiąć w jego wiedzę `ADHD/dopamine_journal.json` i `Protokół Monk Mode`, aby pilnował harmonogramów i rytmu pracy w projektach.

---

## 4. PROPOZYCJA PIERWSZEGO KROKU (Zaczynamy od wycinka!)

Zamiast porywać się na całą wiedzę twórców naraz, sugeruję rozpocząć Ingest od najbardziej palącego i najczystszego na ten moment tematu:

**🎯 PIERWSZY CEL: Zlikwidowanie starego folderu `Baza_Wiedzy` i ogarnięcie "ADHD & Orkiestracja"**
1. Mamy folder `Baza_Wiedzy` z kilkoma JS-owymi skryptami dla GHL/Localo i folderem `ADHD`.
2. Mamy folder `02_knowledge_base\raw\ADHD`.
3. Skrypty wyciągnijmy do `99_workspace/scratch`, a wiedzę o Twoim workflow i kalibracji ADHD ułóżmy w czystą pigułkę (np. do pliku `.agents/rules/adhd_accessibility_and_style.md` lub podobnego, widziałem, że taki istnieje, ale możemy go zaktualizować na bazie notatek). 
4. Dzięki temu skasujemy z głównego katalogu starą "Bazę_Wiedzy", odświeżymy instrukcje do obsługi Twojego workflow i nabierzemy płynności do dalszego porządkowania gigantycznych paczek kursów (np. Jana Szopy).

Daj mi znać w kolejnej wiadomości, czy zgadzasz się na takie uporządkowanie małego folderu "Baza_Wiedzy" jako pierwszego kroku! Jeśli chcesz, możemy też najpierw użyć skryptu pythona, by wykasować duplikaty (pliki `*(1).md` i `*(2).md`). Co wolisz?
