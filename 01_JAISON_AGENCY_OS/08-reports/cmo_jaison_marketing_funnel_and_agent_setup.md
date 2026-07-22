# 🚀 Raport CMO AI: Architektura Marketingowa Agencji Jaison

Dokument ten definiuje pełny model lejka marketingowego B2B, automatyzacji n8n oraz wdrożenia chatbota opartego o Vertex AI Search dla agencji Jaison (jaison.pl). Został stworzony w duchu <strong>Low-Cost First</strong> (GCP + darmowe plany) oraz zgodnie z wytycznymi <strong>Ghost v2</strong> (styl komunikacji Tomasza, brak gwiazdek w HTML, zastępowane znacznikami <strong>strong</strong>).

---

## 1. Architektura Lejka B2B w Systeme.io (Darmowy Plan)
Zgodnie z polityką agencji opieramy marketing o darmowy plan Systeme.io (subdomena <code>go.jaison.pl</code> lub <code>leads.jaison.pl</code>), gdzie dysponujemy tylko 1 tagiem i 1 regułą automatyzacji.

### 1.1. Metodologia Robin Hooda (Demaskowanie Rynku)
Zamiast agresywnego sprzedawania, edukujemy rynek poprzez demaskowanie starych układów agencyjnych:
- <strong>Ściemianie rynkowe:</strong> Tradycyjne agencje marketingowe i software house'y wyceniają wdrożenia prostej automatyzacji na kilkadziesiąt tysięcy złotych i obciążają klienta miesięcznymi abonamentami na "utrzymanie", sprzedając często powtarzalne szablony.
- <strong>Hak demaskujący:</strong> <em>"Zanim zapłacisz agencji 10 000 zł za lejek i obsługę, zobacz, jak 1 inteligentny agent AI postawiony w chmurze GCP robi to samo w 5 sekund, generując rachunek bliski zeru."</em>
- <strong>Rozwiązanie:</strong> Oferujemy bezpłatny raport / wideo demaskujące pt. <em>"Gotowa Architektura Agentów AI - Ukradnij te schematy, na których agencje zarabiają krocie"</em>.

### 1.2. Struktura Lejka (3 Kroki)
1. <strong>Strona Squeeze (Landing Page):</strong> Magnetyczny nagłówek demaskujący, minimalna forma (Email + Imię) + obietnica darmowego narzędzia (Lead Magnet). Optymalizacja pod telefony komórkowe (Clarity Rule).
2. <strong>Strona Podziękowania / VSL:</strong> Surowe, <em>ugly video</em> nagrane telefonem. Tomasz opowiada o standardzie Jaison i od razu zachęca do darmowego 15-minutowego audytu. Znajduje się tam link do <code>Cal.com</code> (asynchroniczny CRM/Booking) lub bezpośredni kontakt WhatsApp.
3. <strong>E-mail Nurturing (Kampania 3-dniowa Autoresponder):</strong>
   - <strong>Dzień 1 (Wartość):</strong> "Twoje skrypty AI są gotowe do pobrania 🎁" - budowanie szybkiego zaufania.
   - <strong>Dzień 2 (Połączenie):</strong> "Dlaczego z ADHD szukałem sposobu na 20h wolnego..." - misja i historia.
   - <strong>Dzień 3 (Akcja):</strong> "Masz 15 minut na audyt Twojej automatyzacji?" - ostra kwalifikacja i CTA do kontaktu z Tomaszem na <strong>+48 791 636 644</strong>.

### 1.3. Tagowanie i CRM
W darmowym planie przypisujemy każdemu użytkownikowi główny tag <code>holistic-contact</code>. Segmentacja odbywa się wyżej, za sprawą integracji w n8n, gdzie w polach niestandardowych (Custom Fields) dopisujemy dodatkowe parametry leada (np. budżet uzyskany w prekwalifikacji).

---

## 2. Automatyzacja Marketingu n8n (ManyChat Killer)
Na subdomenie <code>n8n.jaison.pl</code> uruchamiamy workflow zastępujący drogie aplikacje CRM/Mailingowe.

### 2.1. Social Media Engine (Generacja i Dystrybucja Ruchu)
- <strong>Trigger:</strong> Harmonogram (Cron) codziennie o 08:00.
- <strong>Wsad (Input):</strong> Scrapowanie wiadomości rynkowych (Firecrawl/TrendFinder) uziemionych o specyfikę klientów B2B.
- <strong>Filtrowanie i Tworzenie (LLM Node):</strong> Wyselekcjonowanie najważniejszego tematu przez agenta, stworzenie porywającego posta z silnym nagłówkiem (Hook) przy pomocy metodologii CCO AI.
- <strong>Akcja (Outbound):</strong> Wysyłka gotowego wpisu przez zaufany hub <strong>Composio.dev</strong> prosto na kanały takie jak LinkedIn czy X. 

### 2.2. Auto-Response na Kanałach Zewnętrznych (DM/Wiadomości)
- <strong>Trigger:</strong> Webhook z Composio.dev nasłuchujący komentarzy u Tomasza / Jaison (tzw. "ManyChat Killer").
- <strong>Logika AI:</strong> Model w locie czyta intencje wiadomości klienta. Jeśli to zapytanie o szczegóły/ofertę:
- <strong>Akcja Wyjściowa:</strong> Bot wysyła bezpośrednią odpowiedź Ghost v2 na komunikatorze: <em>"Cześć, podrzucam link do darmowego materiału: go.jaison.pl. Jeżeli potrzebujesz konkretnej architektury dla siebie, łap mnie na WhatsApp: +48 791 636 644".</em> Zapis do Systeme.io następuje automatycznie przez webhook.

---

## 3. Vertex AI Agent Builder - Chatbot B2B Jaison ($1000 Credit)
Zapewniamy luksusowy interfejs czatu bezpośrednio na <code>jaison.pl</code> z zachowaniem zerowych kosztów utrzymania przez pierwszy rok.

### 3.1. Uziemienie Danych (Blended Search Stores)
- <strong>Website Data Store:</strong> Zaawansowana indeksacja domeny `jaison.pl/*`. 
- <strong>GCS Data Store (Wiedza Nieuporządkowana):</strong> Koszyk `gs://jaison-agency-knowledge` zawierający procedury wewnętrzne, przykłady wdrożeń, audyty SEO (AEO), ceny wdrożeń oraz wytyczne na temat optymalizacji profilu GBP. Dostęp zabezpieczony IAM (UBLA). 

### 3.2. Konfiguracja Kosztowa (GCP Console)
- <strong>Model LLM:</strong> <code>Gemini 2.5 Flash</code> (lub nowszy Flash) - idealny stosunek jakości wnioskowania do ceny.
- <strong>Ochrona kosztów:</strong> "Obraz w odpowiedziach" ustawiony na <code>Brak źródła</code>, co zabezpiecza przed drogim renderowaniem Imagen. 
- <strong>Ignoruj podsumowanie przy braku odpowiedzi:</strong> <code>True</code> (zabezpieczenie przed halucynacjami bota - w przypadku pytań odległych od wiedzy, bot przekierowuje do Tomasza).
- <strong>Metoda Autoryzacji:</strong> Rekomendowana <strong>Opcja B (Custom UI + PHP Secure Proxy)</strong>. Dzięki temu mamy potrójną Tarczę Antyspamową (Honeypot, Rate Limiter IP i dobowy limit zapytań), a autoryzacja odbywa się z serwera na klucz JSON.

### 3.3. System Prompt bota (Głos Marki)
Poniższy prompt został wpisany do konfiguracji dostrajania w konsoli Vertex AI dla jaison.pl:

<code>
Jesteś wirtualnym Dyrektorem ds. Marketingu (CMO AI) oraz ekspertem technologicznym agencji Jaison (jaison.pl), pełniącym rolę prawy ręki Tomasza Dudy. Twoim zadaniem jest audytowanie zapytań B2B oraz wsparcie firm we wdrażaniu tanich, nowoczesnych ekosystemów sztucznej inteligencji.

KIERUJ SIĘ ZASADAMI GHOST V2 (TOMASZ DUDA):
- Język musi być profesjonalny, konkretny i lekko "surowy". Unikaj pustych haseł i korporacyjnych słów (np. "innowacyjne rozwiązania", "kompleksowo"). Zwracaj się bezpośrednio ("Ty", "Zobacz", "Sprawdź").
- ZAWSZE używaj znaczników HTML <strong>tekst</strong> do wyróżniania najważniejszych fraz. Kategoryczny zakaz stosowania znaków gwiazdek ** do formatowania pogrubień!
- Bądź Robin Hoodem w branży. Ostrzegaj klientów przed przepłacaniem dziesiątek tysięcy złotych za "konsulting IT" i abonamenty w klasycznych agencjach software house, tłumacząc, że dzięki rozwiązaniom Google Cloud Platform i n8n mogą mieć stabilnego agenta pracującego za grosze lub za darmo z free trialu GCP ($300).
- ZAKAZ HALUCYNACJI: Jeśli klient zadaje specyficzne pytania prawne lub głęboko techniczne na temat architektury serwerów, których nie ma w Twojej Bazie Wiedzy (RAG), powiedz szczerze, że to wykracza poza kompetencje asystenta i skieruj go na audyt.

DOMYKANIE TRANSAKCJI / KONTAKT B2B:
Zawsze na końcu swojej odpowiedzi, jeżeli widzisz, że rozmówca myśli biznesowo, zaoferuj mu dwa rozwiązania:
- Zaproś go do pobrania bezpłatnej checklisty "Architektura Agentów AI" na stronie docelowej: <strong>go.jaison.pl</strong>.
- Zaproponuj błyskawiczny kontakt bezpośrednio do Tomasza Duda w celu 15-minutowego audytu asynchronicznego: <strong>WhatsApp / Telefon: +48 791 636 644</strong>. 
</code>

---
Raport wygenerowano pomyślnie.
CMO AI
