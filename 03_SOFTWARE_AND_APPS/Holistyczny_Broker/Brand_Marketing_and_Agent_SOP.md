# Brand, Marketing & Agent SOP: Holistyczny Broker

Ten dokument definiuje tożsamość marki **Holistyczny Broker**, zasady pozycjonowania (Quiet Luxury) w mediach społecznościowych, konfigurację asystenta AI Concierge w Vertex AI Agent Builder, a także strategię automatyzacji marketingu przy użyciu Systeme.io oraz n8n.

---

## 🏛️ 1. Strategia Marki i Pozycjonowanie (Quiet Luxury)

Holistyczny Broker pozycjonuje się jako **elitarna agencja doradztwa inwestycyjnego na rynku nieruchomości (boutique advisory)**. Nasz styl komunikacji to **Quiet Luxury (Cichy Luksus)** – unikamy krzykliwego marketingu, operujemy twardymi danymi finansowymi, dbamy o maksymalną dyskrecję i budujemy pozycję zaufanego doradcy transakcyjnego ("Transaction Architect").

### 💼 Wytyczne dla LinkedIn (B2B, Deweloperzy, Fundusze, Family Offices):
*   **Headline (Nagłówek):**
    > Architekci Transakcji Inwestycyjnych | PropTech & AI Due Diligence | Grunty, Logistyka, Off-Market
*   **About (O nas):**
    > Nie jesteśmy kolejną agencją nieruchomości. Jesteśmy doradcami kapitałowymi i architektami transakcji na rynku premium.
    >
    > W Holistycznym Brokerze łączymy rygorystyczne modele analityczne (AI Due Diligence) z powściągliwością szwajcarskiego banku. Specjalizujemy się w dystrybucji aktywów typu Off-Market – od gruntów pod wielkoskalowe projekty logistyczne i PRS, po nieruchomości komercyjne w kluczowych hubach inwestycyjnych Polski.
    >
    > Nasz model "Inwestora Zastępczego" zdejmuje z funduszy ciężar formalności, prowadząc proces od analizy chłonności działki po prawomocne pozwolenie na budowę (PnB). Działamy cicho. Dostarczamy twarde dane.

### 📸 Wytyczne dla Social Media (Instagram / Facebook - B2C Premium):
*   **Bio (Instagram):**
    > 🏛 Holistyczny Broker
    > 💼 Architekci Nieruchomości Premium
    > 🤫 Cicha sprzedaż (Off-Market)
    > 📊 AI Due Diligence & PropTech
    > 🔗 holistycznybroker.pl
*   **Wytyczne Graficzne i Estetyczne (Dla Canvy):**
    - **Kolorystyka:** Dominacja Onyx Black (`#0B0F19`), Slate Grey (`#1E293B`) i wykończenia w zgaszonym, szampańskim złocie (`#D4AF37`).
    - **Kompozycja:** Minimalistyczne, surowe ujęcia architektury, duże marginesy (white space), brak nakładanych jaskrawych napisów promocyjnych. 
    - **Typografia:** Eleganckie fonty szeryfowe (np. Playfair Display / Cormorant Garamond) w połączeniu z prostym fontem bezszeryfowym (np. Inter / Montserrat).

---

## 🤖 2. Konfiguracja AI Concierge (Vertex AI Agent Builder)

Dedykowany cyfrowy asystent na stronie www (`holistycznybroker.pl`) oraz na WhatsApp służy do wstępnej kwalifikacji leadów.

### 📋 System Prompt dla Agenta AI:
```text
Jesteś AI Concierge dla firmy "Holistyczny Broker" - elitarnej agencji nieruchomości premium.
Twój styl to "Quiet Luxury" – jesteś powściągliwy, wysoce profesjonalny, dyskretny i elitarny. Nigdy nie narzucasz się klientowi. Operujesz wyłącznie faktami i twardymi danymi rynkowymi.

ZASADY POSTĘPOWANIA:
1. Podział Klientów: Zawsze staraj się dyskretnie zidentyfikować, czy rozmawiasz z klientem indywidualnym B2C (poszukującym rezydencji, luksusowych apartamentów) czy partnerem biznesowym B2B (fundusze inwestycyjne, deweloperzy poszukujący gruntów lub obiektów komercyjnych).
2. Segment Off-Market: Jeśli partner B2B pyta o szczegóły dotyczące gruntów inwestycyjnych, obiektów komercyjnych lub hoteli, poinformuj, że te aktywa dystrybuujemy wyłącznie w trybie Off-Market. Odmów podania precyzyjnych adresów czy cen w otwartym oknie czatu i poinformuj o konieczności przejścia procedury weryfikacji i podpisania NDA.
3. Transparentność: Na samym początku rozmowy subtelnie zasygnalizuj, że jesteś dedykowanym cyfrowym asystentem AI stworzonym, by zapewnić klientowi natychmiastową, bezpieczną i dyskretną pomoc 24/7.
4. Procedura Handoff (Przekazanie do człowieka): Jeśli klient wykazuje poważne zainteresowanie konkretną inwestycją lub chce podpisać NDA/umówić spotkanie, przekaż mu bezpośredni link do kontaktu ze Strategiem na WhatsApp: https://wa.me/48730882961. Nie podawaj innych numerów ani adresów e-mail.
5. Wynagrodzenie: Przypomnij w razie pytań, że nasze biuro operuje wyłącznie w oparciu o prowizję od sukcesu (Success Fee).

ZAKAZY:
NIGDY nie zmyślaj cen, parametrów chłonności (PUM) ani informacji o działkach. Jeśli czegoś nie ma w Twoim Data Store, grzecznie skieruj klienta do kontaktu ze Strategiem. Odpowiedzi formułuj zwięźle, unikając niepotrzebnego żargonu sprzedażowego.
```

---

## 📧 3. Integracja Systeme.io & n8n (Marketing Automation)

Zamiast wdrażać kosztowne systemy i pisać własną infrastrukturę mailingową na GCP, stosujemy podejście **Low-Friction** i integrujemy gotową platformę **Systeme.io** za pomocą scenariuszy **n8n**.

```text
               WEBHOOK                         API
[ Systeme.io ]  ---->  [ Scenariusz n8n ]  -------->  [ Hermes Agentic OS ]
  (Lead/Sale)                                           (Dalsze procesowanie)
```

### 📊 Analiza Planu Darmowego (Free Tier) w Systeme.io:
Darmowy plan Systeme.io pozwala na darmową wysyłkę e-maili i obsługę do **2000 kontaktów**, co jest idealne na start. Posiada jednak bardzo rygorystyczne limity na automatyzację:
- Maksymalnie: **1 tag, 1 reguła automatyzacji, 1 workflow, 1 kampania e-mail**.
- Przekroczenie limitu 2000 kontaktów skutkuje zablokowaniem formularzy i webhooków.

### 🛠️ Architektura integracji w celu ominięcia limitów automatyzacji:
Aby nie płacić za wyższe plany w początkowej fazie i nie ograniczać się do jednego workflow, całą logikę biznesową przenosimy na zewnątrz:
1. **Jednorazowy Tag:** W Systeme.io tworzymy jeden ogólny tag (np. `systeme_lead`).
2. **Globalny Webhook:** Ustawiamy jedyną regułę automatyzacji w Systeme.io tak, aby przy zapisie klienta lub zakupie wysyłała webhook (POST) do naszego serwera **n8n**.
3. **Logika w n8n / Hermes:**
   - Gdy n8n otrzyma payload z webhooka (zawierający e-mail, imię i szczegóły transakcji), parsuje go.
   - n8n decyduje, do jakiej kampanii przypisać użytkownika, wysyłając odpowiednie instrukcje do bazy danych lub bezpośrednio do Hermes Agentic OS.
   - W ten sposób Systeme.io służy wyłącznie jako interfejs do wysyłki e-maili i zbierania płatności, a cała inteligencja i routing kampanii są realizowane przez n8n i system agentyczny.
