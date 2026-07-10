# ⚡ Szybki Start z Google Cloud: Krok po Kroku do Własnego AI i Automatyzacji
## Ilustrowany Przewodnik Wdrożeniowy (Wersja Ogólnodostępna - ADHD-friendly & NLP Copywriting)

---

> **Poczuj głęboką ulgę:** Zdejmij ze swoich barków stres związany z techniczną konfiguracją chmury. Ten ilustrowany przewodnik przeprowadzi Cię przez proces szybko, bez wysiłku i bez zbędnego chaosu informacyjnego. **Wyobraź sobie moment**, gdy Twoje lokalne środowisko agentowe połączy się bezpośrednio z potężnymi modelami Vertex AI, a Ty zyskasz pełną kontrolę nad budżetem, infrastrukturą i wszystkimi swoimi danymi. **Usłysz ten spokojny szum** działających automatyzacji, które bez Twojego zaangażowania wykonują powtarzalną pracę, dając Ci wolność i przestrzeń na to, co najważniejsze.

---

## 🎯 ETAP 1: Rejestracja bez tarcia (Od zera do pierwszego logowania)

*   [ ] **KROK 1.1:** Otwórz przeglądarkę i wejdź na oficjalną stronę: [Google Cloud Console](https://console.cloud.google.com/).
*   [ ] **KROK 1.2:** Zaloguj się na swoje konto Google. 
    *   *Sztuczka ułatwiająca życie:* **Możesz użyć zwykłego, darmowego konta Gmail!** Nie musisz na starcie kupować płatnego konta Google Workspace. Zwykły Gmail jest w 100% wystarczający do celów testowych i deweloperskich i nie generuje żadnych kosztów abonamentowych.
*   [ ] **KROK 1.3:** Zaakceptuj regulaminy i kliknij niebieski przycisk **„Aktywuj” / „Activate”** na banerze oferującym darmowy pakiet startowy (np. darmowe $300 USD na start).
*   [ ] **KROK 1.4:** **Krytyczne dla finansów (VAT) i struktury:** W oknie konfiguracji płatności przy wyborze typu konta zaznacz **„Konto organizacji / Organization”** (lub **„Firma / Business”** jeśli nie posiadasz jeszcze struktury organizacji podpiętej pod Google Workspace / Cloud Identity).
    *   *Dlaczego?* Pozwoli to na prawidłowe zarządzanie uprawnieniami w ramach Twojej domeny firmowej, a także zapobiegnie naliczeniu 23% VAT, ponieważ Google wystawi fakturę bezpośrednio na dane podatkowe Twojej firmy (NIP).

![Aktywacja płatnego konta rozliczeniowego i profilu płatności w Google Cloud Console](screenshots/annotated/ETAP_01_KROK_08_aktywuj_pelne_konto.png)

[Komentarz dla składu: Powyżej znajduje się zrzut ekranu przedstawiający formularz konfiguracji konta billingowego Google Cloud Console z zaznaczonym typem konta jako organizacja/firma i widocznym polem na wpisanie NIP-u (Tax ID).]

*   [ ] **KROK 1.5:** **Przedpłata weryfikacyjna (zależna od stażu konta):** Przy rejestracji na zupełnie nowym koncie Google (bez historii płatniczej), Google może wymagać jednorazowej przedpłaty weryfikacyjnej (która zasila Twoje saldo rozliczeniowe i nie przepada). W przypadku starszych, zaufanych kont Google, okres próbny aktywuje się zazwyczaj natychmiast, bez wnoszenia przedpłat.

[Komentarz dla składu: Tutaj warto dodać zrzut ekranu z oknem potwierdzenia udanej weryfikacji karty płatniczej w systemie Google Pay / GCP Billing.]

---

## 💰 ETAP 2: Aktywacja i zabezpieczenie darmowych środków

Po poprawnym skonfigurowaniu płatności, w Twoim panelu aktywują się dwie niezależne kasy z darmowymi środkami promocji startowej:

### 1. Pula $300 USD — ważna przez 90 dni
*   **Co to zasila?** Całą tradycyjną infrastrukturę GCP (maszyny wirtualne pod n8n/make, bazy danych SQL, pamięć dyskową Cloud Storage, aplikacje Cloud Run).
*   **Jak sprawdzić stan?** Wpisz w górnej wyszukiwarce GCP hasło **„Billing”** (Rozliczenia) i przejdź do pulpitu rozliczeń.

### 2. Pula $1000 USD (w ramach kredytów GenAI) — ważna przez 1 ROK
*   **Co to zasila?** Usługi generatywnej sztucznej inteligencji: **Vertex AI Search and Conversation** (twoje bazy wiedzy RAG) oraz powiązane z nimi inteligentne agenty.
*   **Aktywacja:** Środki te są automatycznie przypisywane do Twojego konta rozliczeniowego w momencie włączenia pierwszego API z rodziny Vertex AI.

![Wizualizacja salda darmowych środków startowych (Free Trial Credit) w panelu rozliczeniowym Google Cloud](screenshots/annotated/ETAP_02_KROK_01_billing_overview.png)

[Komentarz dla składu: Powyższy zrzut ekranu prezentuje pulpit nawigacyjny Billing w GCP Console, pokazujący pasek postępu darmowych kredytów startowych ($300).]

---

### 🛡️ Zabezpieczenie konta: Konfiguracja Budżetów i Alertów

Nie zostawiaj swoich finansów przypadkowi. Google Cloud pozwala na zdefiniowanie twardych limitów budżetowych z powiadomieniami e-mail, co chroni Cię przed niekontrolowanymi kosztami.

*   [ ] **KROK 2.3:** W menu bocznym Billing kliknij **„Budgets & alerts”** (Budżety i alerty), a następnie kliknij **„Create Budget”** (Utwórz budżet).
*   [ ] **KROK 2.4:** Nazwij budżet (np. `Monthly Safety Net`), wybierz zakres czasu (miesięczny) oraz określ kwotę (np. 200 PLN).
*   [ ] **KROK 2.5:** Skonfiguruj progi alertów (np. powiadomienie e-mail przy 50%, 90% i 100% zużycia kwoty).

![Tworzenie i konfiguracja budżetu bezpieczeństwa w panelu rozliczeniowym GCP](screenshots/annotated/ETAP_02_KROK_03_create_budget.png)

[Komentarz dla składu: Zrzut ekranu przedstawia formularz konfiguracji budżetu z wpisaną nazwą i kwotą limitu.]

![Podsumowanie skonfigurowanego budżetu z progami alertów](screenshots/annotated/ETAP_02_KROK_04_budget_configured.png)

[Komentarz dla składu: Zrzut ekranu pokazuje listę aktywnych budżetów z widocznym budżetem Monthly Safety Net i progami alertów.]

---

## 🚀 ETAP 3: Program Google Cloud Startups (Zdobądź do $100 000 USD)

Nie musisz finansować rozwoju swojej technologii z własnej kieszeni. Jako młoda firma, start-up lub agencja wdrażająca nowoczesne rozwiązania, możesz ubiegać się o gigantyczne granty chmurowe. Google bardzo chętnie wspiera projekty technologiczne, o ile spełniają one rygorystyczne warunki wejściowe.

---

### 1. Ścieżka aplikacyjna i progi darmowych środków:
*   **Poziom START ($2 000 USD):** Przeznaczony dla wczesnych pomysłów (Bootstrap). Google przyznaje te środki (ważne przez 2 lata) niemal każdemu, kto posiada **konto organizacji Google Cloud** i opisze swój planowany produkt AI w formularzu aplikacyjnym.
*   **Poziom SCALE (do $100 000 USD):** Dla zweryfikowanych start-upów z finansowaniem zewnętrznym lub pod skrzydłami akredytowanych partnerów / akceleratorów (np. Y Combinator, Techstars, fundusze VC). Pokrywa do 100% kosztów całej Twojej infrastruktury chmurowej przez rok.

---

### 2. Jak myśli weryfikator Google? (Złote Zasady Kwalifikacji)
Google chroni swoje zasoby przed nadużyciami i odrzuca wnioski niespełniające kryteriów. Aby uzyskać akceptację, Twój projekt musi pomyślnie przejść przez cztery główne filtry weryfikacyjne:

*   ⚠️ **Filtr Rodzaju Działalności (Krytyczny):** Google wspiera **wyłącznie skalowalne produkty technologiczne (SaaS, aplikacje mobilne, platformy webowe, rynki dwustronne/marketplaces)**. Program **kategorycznie odrzuca**:
    *   Agencje marketingowe, SEO i interaktywne.
    *   Software house'y i firmy konsultingowe (wykonujące usługi "szyte na miarę" dla klientów).
    *   Szkolenia, portale informacyjne i blogi.
    *   Tradycyjne e-commerce (prosta sprzedaż towarów).
*   ⚠️ **Wiek firmy i historia:** Projekt lub powiązany z nim podmiot gospodarczy nie może mieć więcej niż 5 lat, a firma nie mogła wcześniej otrzymać najwyższych grantów z programu startupowego Google.
*   ⚠️ **Zasada Google Workspace (Poczta we własnej domenie):**
    *   Jeśli Twoja domena (np. `twojadomena.pl`) posiada aktywną, płatną subskrypcję Google Workspace wykupioną w ciągu ostatnich **31 dni** przed złożeniem wniosku, **nie otrzymasz darmowego Workspace z programu** (Google dodaje 12 miesięcy Workspace Business Plus za darmo dla nowych kont).
    *   *Zasada złotego czasu:* **Zawsze wnioskuj o grant zanim kupisz płatną pocztę Google Workspace**, aby otrzymać ją w 100% bezpłatnie na cały rok dla całego zespołu!

---

### 3. Jakie cechy techniczne SaaS-u faworyzuje Google?
Projektując aplikację pod kątem akceptacji, upewnij się, że opisujesz architekturę, którą Google uwielbia:
*   **Architektura Wielo-Dzierżawcza (Multi-Tenancy):** Jeden rdzeń aplikacji obsługujący wielu niezależnych klientów (tenantów), posiadających odseparowane dane w bazach (np. poprzez schematy w PostgreSQL lub AlloyDB).
*   **Orkiestracja i Konteneryzacja (Cloud Run / GKE):** Uruchamianie aplikacji w środowiskach kontenerowych, które skalują się automatycznie od zera do tysięcy zapytań w zależności od ruchu.
*   **Głębokie wykorzystanie Vertex AI:** Integracja modeli Gemini 2.5/3.1 z bazami wiedzy RAG (Vertex AI Search) ułatwia automatyzację procesów i sprawia, że Google widzi w Tobie idealnego partnera technologicznego.

---

### 4. Trik Pozycjonowania NLP (Jak przekształcić "usługę" w "SaaS" we wniosku?)
Jeśli prowadzisz agencję lub software house, Twoja aplikacja zostanie odrzucona. Rozwiązaniem jest **spakowanie Twojej wiedzy i powtarzalnych procesów w produkt technologiczny (SaaS)** i opisanie go jako platformy automatyzacyjnej, którą będziesz dystrybuować w modelu abonamentowym.

#### 📝 Gotowy szablon opisu projektu do skopiowania i adaptacji:
> *"Projekt [Nazwa Twojej Domeny / Produktu] to innowacyjna platforma typu **SaaS (Software-as-a-Service)** oparta o chmurę Google Cloud oraz Vertex AI. Dostarczamy firmom dedykowany, wieloagentowy system operacyjny, który przy użyciu autonomicznych agentów (CMO AI, CTO AI, CSO AI) oraz silnika wyszukiwania semantycznego (Vertex AI Search / RAG Engine) automatyzuje i optymalizuje czasochłonne procesy operacyjne w MŚP. Nasza platforma działa w modelu multi-tenant, oferując użytkownikom końcowym gotowe, asynchroniczne przepływy pracy (workflows) i zaawansowaną analitykę danych. Modele Gemini wykorzystujemy do wnioskowania, analizy konkurencji i automatycznego generowania struktur lejeków marketingowych."*

*   **Jak zaaplikować:** Wejdź na stronę [Google for Startups Cloud Program](https://cloud.google.com/startup) i kliknij **Apply Now**. Podepnij swoje konto i uzupełnij formularz aplikacyjny według powyższych wskazówek.

---

## 🔌 ETAP 4: Włączanie silników chmury (Kluczowe interfejsy API)

Aby Twoje lokalne systemy, skrypty i agenty mogły komunikować się z chmurą Google, musisz włączyć w konsoli GCP cztery kluczowe usługi.

```
[WYSZUKAJ W GÓRNYM PASKU GCP] ➔ [KLIKNIJ "ENABLE" (WŁĄCZ)]
```

*   [ ] **Vertex AI API:** Główny silnik modeli językowych z rodziny Gemini, generowania obrazów Imagen oraz wideo.
*   [ ] **Vertex AI Search and Conversation API:** Serce wyszukiwarki semantycznej (RAG) i bazy wiedzy dla agentów.
*   [ ] **Cloud Resource Manager API:** Umożliwia aplikacjom zewnętrznym odpytywanie o strukturę Twoich projektów.
*   [ ] **Cloud Run API / Compute Engine API:** Potrzebne do wdrażania dynamicznych aplikacji internetowych (SaaS, komunikatory, dashboardy) oraz maszyn wirtualnych.

![Aktywacja interfejsów API w bibliotece Google Cloud Platform API Library](screenshots/annotated/ETAP_04_KROK_07_agent_platform_api.png)

[Komentarz dla składu: Powyżej znajduje się zrzut ekranu przedstawiający stronę szczegółów API Vertex AI w GCP Console, potwierdzający poprawne włączenie usługi (status „API Enabled” z niebieskim przyciskiem zarządzania API).]

---

### ⚡ Szybka Alternatywa w PowerShell (Dla Zaawansowanych)

Zamiast wyszukiwać i włączać każde API ręcznie w przeglądarce, możesz włączyć wszystkie wymagane usługi jedną komendą w terminalu PowerShell (One-Liner):

```powershell
gcloud services enable aiplatform.googleapis.com discoveryengine.googleapis.com dialogflow.googleapis.com run.googleapis.com --project=ID_TWOJEGO_PROJEKTU_GCP
```


#### 🔍 Szybki Test Połączenia i Uprawnień z poziomu terminala
Aby upewnić się, że Twój profil jest w pełni sprawny i gotowy do współpracy z agentem, wykonaj:
```powershell
gcloud auth list; gcloud config list; gcloud services list --enabled --filter="aiplatform"
```

## 🖥️ ETAP 5: Architektura Multi-Profilowa w PowerShell (Zarządzanie wieloma projektami)

Jeśli wdrażasz systemy AI dla wielu klientów lub prowadzisz równolegle kilka projektów, **kategorycznie unikaj ciągłego wylogowywania się i ponownego logowania!** Prowadzi to do chaosu i pomyłek w zasobach.

Narzędzie Google Cloud CLI posiada wbudowany, rewelacyjny mechanizm profili (`gcloud config configurations`). Pozwala on na błyskawiczne przełączanie całego kontekstu pracy (konto Google + powiązany projekt):

### 1. Tworzenie niezależnych profili:
Wpisz poniższe polecenia w terminalu (np. Windows PowerShell) jako One-Liners (w jednej linii):

```powershell
# Tworzenie profilu dla własnej firmy
gcloud config configurations create profil-wlasny

# Tworzenie profilu dla pierwszego klienta
gcloud config configurations create profil-klient-a
```

### 2. Autoryzacja i powiązanie projektu z profilem:
Przełącz się na dany profil, zaloguj się na właściwy e-mail i przypisz domyślny projekt chmurowy:

```powershell
# Konfiguracja profilu własnego
gcloud config configurations activate profil-wlasny; gcloud auth login twoj-email@gmail.com; gcloud config set project id-twojego-projektu; gcloud auth application-default login

# Konfiguracja profilu klienta
gcloud config configurations activate profil-klient-a; gcloud auth login email-klienta@gmail.com; gcloud config set project id-projektu-klienta; gcloud auth application-default login
```

### 3. Jak błyskawicznie przełączać się między projektami?
Gdy chcesz zmienić kontekst pracy i zacząć zarządzać infrastrukturą klienta, wpisujesz tylko:

```powershell
gcloud config configurations activate profil-klient-a
```
Aby wrócić do swoich zasobów:
```powershell
gcloud config configurations activate profil-wlasny
```

![Uruchomienie terminala Cloud Shell na dole konsoli GCP](screenshots/annotated/ETAP_05_KROK_01_cloud_shell_active.png)

[Komentarz dla składu: Zrzut ekranu przedstawia otwarte okno terminala Cloud Shell na dole przeglądarki w konsoli GCP.]

*   [ ] **KROK 5.1b:** Przy pierwszym uruchomieniu Cloud Shell pojawi się modal z żądaniem autoryzacji (**„Autoryzuj Cloud Shell”**). Kliknij niebieski przycisk **„Autoryzuj”** (Authorize), aby przyznać poświadczenia deweloperskie terminalowi.

![Modal z żądaniem autoryzacji Cloud Shell deweloperskiego](screenshots/annotated/ETAP_05_KROK_01b_cloud_shell_authorize.png)

[Komentarz dla składu: Zrzut ekranu prezentuje okienko modalne z zapytaniem o autoryzację Cloud Shell i niebieskim przyciskiem Autoryzuj.]

[Komentarz dla składu: Tutaj należy wstawić zrzut ekranu przedstawiający terminal z wykonaną komendą „gcloud config configurations list”, prezentujący listę zdefiniowanych konfiguracji i gwiazdkę oznaczającą aktywny profil.]

---

## 🔑 ETAP 6: Uruchomienie lokalnego logowania w Środowisku Deweloperskim

Możesz zalogować się i połączyć swoje lokalne środowisko z Google Cloud na dwa sposoby.

### Metoda A: Uwierzytelnianie przez graficzny interfejs (Zalecane) ⚡

W oknie logowania Twojego IDE lub aplikacji agentowej:
1.  **KROK 6.0 (Powitanie):** Po uruchomieniu Antigravity IDE zobaczysz ekran powitalny. Kliknij opcję logowania poprzez projekt Google Cloud (**„Use Google Cloud project instead”**).

![Ekran powitalny Antigravity IDE z opcją logowania GCP](screenshots/annotated/ETAP_06_KROK_00_welcome_antigravity.png)

[Komentarz dla składu: Zrzut ekranu ekranu powitalnego Welcome to Antigravity z zaznaczoną czerwoną strzałką na link "Use Google Cloud project instead".]

2.  Spowoduje to automatyczne otwarcie bezpiecznego okna logowania w Twojej przeglądarce.
3.  Zaloguj się na konto Google, na którym utworzyłeś projekt GCP.
4.  **KROK 6.1 (Dane projektu):** Po udanej autoryzacji wklej do aplikacji swój **Project ID** (znajdziesz go na głównym pulpicie konsoli Google Cloud) oraz wybierz strefę/lokalizację zasobów:
    *   **Lokalizacja (Location):** Standardowo wybierz **`global (default)`**. Daje to najniższe opóźnienia w routingu zapytań do modeli Vertex AI oraz maksymalną kompatybilność z modelami językowymi (niektóre nowości są wdrażane regionalnie z dużym opóźnieniem).
    *   **Kiedy zmienić na regionalną (np. europejską)?** Zmień lokalizację na regionalną (np. regiony EU) wyłącznie ze względów prawnych i wymogu przechowywania danych użytkowników w Unii Europejskiej (suwerenność danych / RODO).

![Uwierzytelnianie lokalne w edytorze przy użyciu Project ID Google Cloud](screenshots/annotated/ETAP_06_KROK_01_login_antigravity.png)

[Komentarz dla składu: Zrzut ekranu z kreatora logowania IDE z wprowadzonym przykładowym Project ID oraz domyślną lokalizacją global.]

---

### Metoda B: Uwierzytelnianie przez terminal Windows PowerShell

Otwórz Windows PowerShell i wykonaj te **trzy komendy jako One-Liners** (bez używania linuxowych znaków kontynuacji linii `\`):

*   [ ] **KROK 6.1: Logowanie globalne do chmury:**
    ```powershell
    gcloud auth login
    ```
*   [ ] **KROK 6.2: Wybór aktywnego projektu:**
    ```powershell
    gcloud config set project ID_TWOJEGO_PROJEKTU_GCP
    ```
*   [ ] **KROK 6.3: Wygenerowanie poświadczeń aplikacyjnych (ADC):**
    ```powershell
    gcloud auth application-default login
    ```

---

## 🌌 ETAP 7: Konfiguracja Środowiska Antigravity IDE od A do Z

Wdrożenie systemów agentycznych wymaga dobrze dobranych ustawień środowiska pracy. Antigravity IDE (wraz z wbudowanym asystentem Antigravity Agentic) podczas pierwszego uruchomienia prowadzi Cię przez kreator konfiguracji. Oto hierarchiczne omówienie każdego kroku w kreatorze, wyjaśnienie opcji oraz rekomendowane ustawienia.

### KROK 7.0: Bezpieczne przejście i migracja ustawień (Migrate Settings)
Podczas aktualizacji lub pierwszego uruchomienia nowej wersji IDE (np. 2.0+), na Twoim ekranie pojawi się okno dialogowe dotyczące migracji ustawień.

![Okno migracji konfiguracji, skrótów klawiszowych i rozszerzeń w IDE](screenshots/annotated/ETAP_06_KROK_02_migrate_settings.png)

[Komentarz dla składu: Powyżej znajduje się zrzut ekranu okna „Migrate Settings, Keybindings, and Extensions” z przyciskami Migrate, Copy Commands oraz Cancel.]

**Zrozum to bez stresu i poczuj spokój:** Twój edytor dba o to, byś nie stracił dotychczas wypracowanych skrótów klawiszowych oraz zainstalowanych rozszerzeń z poprzednich wersji edytora. Zamiast budować środowisko od nowa i tracić cenną energię:
*   **Wybierz „Migrate” (Zalecane) ⚡:** Kliknięcie tego przycisku spowoduje automatyczne, bezwysiłkowe skopiowanie wszystkich Twoich wcześniejszych preferencji, skrótów klawiszowych i wtyczek. Poczujesz ulgę, widząc, że środowisko jest gotowe do pracy w ułamku sekundy, dokładnie tak, jak je zostawiłeś.
*   **Wybierz „Copy Commands”:** Jeśli jesteś zaawansowanym użytkownikiem chmury i chcesz dokładnie kontrolować, jakie skrypty wykonują się w tle, skopiuj komendy migracyjne i uruchom je ręcznie w terminalu.
*   **Wybierz „Cancel”:** Kliknij tylko wtedy, gdy chcesz rozpocząć pracę z całkowicie czystą kartą (czysta konfiguracja bez starych rozszerzeń i historii).

---

### KROK 7.1: Wybór wtyczek i pakietów (Build with Google)
Na pierwszym ekranie decydujesz, jakie pakiety umiejętności (skills) oraz serwerów MCP zostaną udostępnione Twojemu agentowi AI.

![Wtyczki deweloperskie i pakiety SDK w kreatorze Build with Google](screenshots/annotated/ETAP_06_KROK_03_build_with_google.png)

[Komentarz dla składu: Powyżej znajduje się zrzut ekranu z pierwszego kroku konfiguracji wtyczek deweloperskich (Build with Google).]

*   **Modern Web Guidance (Rekomendowane):** Udostępnia agentowi skille optymalizacji kodu webowego, analityki zdarzeń oraz standardy SEO i Schema.org.
*   **Google Antigravity SDK (Krytyczne / Wymagane):** Zapewnia bezpośrednią integrację z chmurą Google Cloud, Vertex AI oraz systemem zarządzania agentami. Bez tego agent nie będzie potrafił autoryzować Twoich skryptów w GCP.
*   **Firebase (Opcjonalne):** Włącz, jeśli Twój produkt korzysta z bezserwerowych baz danych Firestore, autoryzacji Firebase Auth lub hostingu Google.
*   **Chrome DevTools (Rekomendowane):** Daje agentowi możliwość automatycznego testowania i uruchamiania przeglądarki w tle, badania struktury DOM i szybkiego poprawiania błędów frontendu.
*   **Dart and Flutter (Opcjonalne):** Niezbędne do rozwoju aplikacji mobilnych (Android/iOS) i wieloplatformowych pisanych we Flutterze.
*   **Google Maps Platform (Opcjonalne):** Umożliwia agentowi korzystanie z protokołu MCP Google Maps, co pozwala mu na geokodowanie adresów, wyszukiwanie miejsc (Places API), wyliczanie tras (Directions API) oraz generowanie interaktywnych map. Włącz to tylko wtedy, gdy Twój projekt integruje się z usługami lokalizacyjnymi i geograficznymi (dzięki temu zaoszczędzisz kontekst roboczy agenta, wyłączając go, gdy nie jest potrzebny).

---

### KROK 7.2: Tryb autonomii agenta (How do you want to use the Antigravity IDE Agent?)
Wybierasz model współpracy z agentem. Określa on, jak bardzo samodzielny będzie asystent AI podczas edycji kodu i wykonywania komend terminala.

![Wybór trybu autonomii i interakcji z agentem AI w IDE](screenshots/annotated/ETAP_06_KROK_05_agent_autonomy.png)

[Komentarz dla składu: Powyższy zrzut ekranu pokazuje ekran wyboru trybu współpracy (Strict Mode, Review-driven, Agent-driven).]

*   **Strict Mode (Tryb restrykcyjny):** Najbardziej zachowawczy. Agent pyta o zatwierdzenie niemal każdej operacji odczytu/zapisu plików i komend. Dobry dla osób stawiających pierwsze kroki w programowaniu.
*   **Review-driven development (Zalecane / Zbalansowane):** Agent przed rozpoczęciem prac tworzy w markdownie dokument `implementation_plan.md` i listę zadań `task.md`. Czeka na Twój przycisk "Zatwierdź" w UI przed wykonaniem jakichkolwiek modyfikacji kodu. Minimalizuje ryzyko niekontrolowanych zmian.
*   **Agent-driven development (W pełni autonomiczny):** Agent wykonuje komendy i modyfikuje kod w pętli bez pytania o zgodę na poszczególne kroki. 
    *   *Uwaga:* Wybierz ten tryb tylko wtedy, gdy masz włączoną kontrolę wersji (np. Git) i sprawnie zarządzasz historią commitów, aby w razie błędu łatwo cofnąć kod.
*   **Custom configuration (Własna):** Pozwala precyzyjnie zdefiniować, które operacje (np. odczyt plików, edycja kodu, uruchamianie poleceń powłoki) wymagają zgody użytkownika, a które mogą dziać się autonomicznie.

---

### KROK 7.3: Konfiguracja Edytora (Configure Your Editor)
Dopasowanie podstawowych skrótów klawiszowych i rozszerzeń językowych pod Twoje nawyki programistyczne.

![Wybór skrótów klawiszowych oraz instalacji wtyczek w edytorze](screenshots/annotated/ETAP_06_KROK_04_configure_editor.png)

[Komentarz dla składu: Zrzut ekranu przedstawiający opcje wyboru keybindings (Vim/Normal) oraz domyślnych wtyczek.]

*   **Keybindings (Skróty klawiszowe):**
    *   **Normal:** Standardowe skróty (jak w VS Code). Najlepsze dla 95% użytkowników.
    *   **Vim:** Aktywuje modalny tryb nawigacji za pomocą klawiatury dla użytkowników przyzwyczajonych do edytora Vim.
*   **Extensions (Rozszerzenia):**
    *   Wybierz opcję **Recommended**, aby automatycznie zainstalować zestaw rozszerzeń obsługujących najważniejsze języki programowania. Zapewnia to agentowi poprawny parser i lintery kodu.

---

### KROK 7.4: Prywatność i Telemetria (Security Notice & Data Use)
Ostatni etap dotyczy akceptacji ryzyka związanego z kodem generowanym przez AI oraz zbierania anonimowych danych telemetrycznych w celu poprawy algorytmów Google.

![Okienko noty prawnej oraz zgód na przetwarzanie danych telemetrii](screenshots/annotated/ETAP_06_KROK_06_security_notice.png)

[Komentarz dla składu: Zrzut ekranu przedstawiający warunki prywatności i pola wyboru zgód w kreatorze.]

*   **Zgoda na zbieranie danych interakcji (Zalecana):** Pozwala Google na analizowanie sposobu interakcji z agentem w celu ulepszania jego modeli. Nie przekazuje wrażliwych danych z plików źródłowych projektu.
*   **Zgoda na komunikację marketingową (Opcjonalna):** Otrzymywanie nowości i poradników na e-mail powiązany z kontem Google Cloud.

---



## 🛡️ ETAP 8: Limity zapytań (Quotas) — Inspekcja i podnoszenie limitów

Gdy Twoje zaawansowane systemy wieloagentowe (np. Antigravity OS) zaczną wykonywać wiele zadań równolegle, domyślne limity zapytań Vertex AI na nowym koncie mogą wywołać błąd przekroczenia limitu zapytań (`429 Resource Exhausted`).

### 1. Weryfikacja konta rozliczeniowego (Billing)
Przed zgłoszeniem prośby o zwiększenie limitów upewnij się, że Twój projekt GCP jest podpięty pod właściwe, zweryfikowane konto rozliczeniowe. Na kontach z darmowym pakietem próbnym (bez podpiętej karty) wnioski o zwiększenie limitów Vertex AI są najczęściej odrzucane.

#### Jak sprawdzić status płatności w terminalu?
Wykonaj poniższe polecenie w terminalu PowerShell (jako One-Liner):
```powershell
gcloud beta billing projects describe ID_TWOJEGO_PROJEKTU_GCP
```
*   Upewnij się, że w wyniku widnieje parametr: `billingEnabled: true`.
*   Zweryfikuj poprawność powiązanego konta w linii `billingAccountName`. Listę swoich kont rozliczeniowych sprawdzisz przez:
```powershell
gcloud billing accounts list
```

[Komentarz dla składu: Zrzut ekranu z konsoli Google Cloud przedstawiający stronę IAM -> Quotas & System Limits z zaznaczoną konkretną metryką Vertex AI API i wybranym przyciskiem "Edit Quotas".]

### 2. Jak sprawdzić aktualne limity zapytań w konsoli PowerShell?
```powershell
gcloud services consumer-quota-metrics list --service=aiplatform.googleapis.com --project=ID_TWOJEGO_PROJEKTU_GCP
```

### 3. Zwiększenie limitów za pomocą jednej komendy w PowerShell (One-Liner)
Możesz wysłać oficjalną prośbę o modyfikację limitu (tzw. Quota Preference) bezpośrednio z Cloud Shell lub lokalnego komputera, korzystając z poniższego szablonu. 

Pamiętaj o podmieniu zmiennych `ID_TWOJEGO_PROJEKTU_GCP` oraz `TWÓJ_REGION_GCP` (np. `us-central1` lub `europe-west3`) na własne wartości:

```powershell
gcloud beta quotas preferences create --project=ID_TWOJEGO_PROJEKTU_GCP --service=aiplatform.googleapis.com --quota-id=generate_content_requests_per_minute_per_project_per_base_model --preferred-value=150 --dimensions=region=TWÓJ_REGION_GCP --preference-id=increase-gemini-rpm --justification="Wdrozenie produkcyjnego systemu agentowego w chmurze organizacji. Zwiekszenie limitu zapytan na minute (RPM) zapobiega powstawaniu krytycznych bledow HTTP 429 podczas wykonywania rownoleglych zadan orkiestracyjnych przez asynchroniczne agenty."
```

### 4. Gotowe szablony uzasadnienia biznesowego (Justification)
Google automatycznie odrzuci wniosek bez podania przekonującego powodu. Oto trzy szablony uzasadnień, które możesz wykorzystać w formularzu konsoli GCP lub w powyższym parametrze `--justification`:

#### Opcja A: Wdrożenie systemu operacyjnego agentów (np. Antigravity OS / Jaison AI)
> *"Wdrożenie produkcyjnego systemu operacyjnego opartego na agentach AI (Antigravity OS) w środowisku organizacji. System realizuje asynchroniczne zadania operacyjne w tle (kodowanie, analiza, orkiestracja). Zwiększenie limitów RPM/TPM jest kluczowe dla uniknięcia blokad wątków przy równoległych zapytaniach i pętli agentowych."*

#### Opcja B: Aplikacja kliencka w czasie rzeczywistym (Real-Time Client App)
> *"Uruchomienie komercyjnej usługi asystenta AI zintegrowanego w czasie rzeczywistym z panelem użytkownika. Aplikacja kierowana jest do użytkowników biznesowych (B2B), a domyślny limit zapytań (RPM) uniemożliwia stabilną obsługę jednoczesnych sesji wielu klientów."*

#### Opcja C: Masowe przetwarzanie danych (Batch Processing)
> *"Przetwarzanie potoków danych w tle (wsadowa analiza dokumentów technicznych, raportów PDF oraz automatyczna synteza baz wiedzy). Proces wymaga krótkotrwałych, seryjnych skoków obciążenia API, a obecny limit powoduje masowe odrzucanie zapytań."*

#### Jak sprawdzić status zgłoszonego wniosku o limity?
```powershell
gcloud beta quotas preferences list --project=ID_TWOJEGO_PROJEKTU_GCP
```

### 5. Automatyzacja: Programowe wnioskowanie o limity za pomocą Pythona (Zalecane)
Jeśli Twój terminal gcloud CLI nie ma zainstalowanych komponentów beta (co jest częste na nowo konfigurowanych komputerach/laptopach), próba uruchomienia komendy `gcloud beta quotas` zwróci błąd. 

Aby zlikwidować to tarcie operacyjne, w folderze `scratch/` Twojego projektu stworzyliśmy dedykowany skrypt deweloperski [request_quota.py](file:///c:/Aplikacje%20MVP/Holistic%20Jason/scratch/request_quota.py). Skrypt ten łączy się bezpośrednio z oficjalnym interfejsem API Cloud Quotas w Google Cloud, omijając gcloud CLI i automatycznie składając wnioski dla wszystkich modeli i stref.

#### 🔧 Konfiguracja uwierzytelnienia (Dla konta ziomus83@gmail.com)
Przed pierwszym uruchomieniem skryptu na nowym laptopie lub komputerze stacjonarnym, wykonaj poniższe polecenia konfiguracyjne w PowerShell:

```powershell
# 1. Zaloguj się na swoje konto deweloperskie
gcloud auth login ziomus83@gmail.com

# 2. Ustaw domyślny projekt jako aktywny deweloperski
gcloud config set project project-d4dcda6d-71f8-44d8-922

# 3. Zaloguj się dla Application Default Credentials (ADC)
gcloud auth application-default login

# 4. Krytyczne: Ustaw projekt rozliczeniowy (quota project) dla ADC
gcloud auth application-default set-quota-project project-d4dcda6d-71f8-44d8-922
```

#### 🚀 Jak uruchomić programowe składanie wniosków?
Wszystkie komendy wykonuj z katalogu głównego swojego projektu (`C:\Aplikacje MVP\Holistic Jason`):

```powershell
# Opcja A: Dry-Run (Sprawdzenie i wygenerowanie ładunków zapytań bez wysyłania)
python scratch/request_quota.py --dry-run

# Opcja B: Oficjalne wysłanie wniosków (Zwiększenie RPM do 120 dla us-central1 i europe-west3)
python scratch/request_quota.py --project project-d4dcda6d-71f8-44d8-922 --rpm 120

# Opcja C: Szybkie wylistowanie statusów i wniosków na ekranie
python scratch/request_quota.py --list
```

#### 📋 Wyniki programowego wnioskowania o limity
Poniższa tabela przedstawia statusy złożonych preferencji dla projektu `project-d4dcda6d-71f8-44d8-922`:

| Model (base_model ID) | Region | Status | Wyjaśnienie |
|---|---|---|---|
| `gemini-2.0-flash-001` | us-central1 | Oczekuje | Weryfikacja automatyczna (trwa do kilku minut / maks 2 dni) |
| `gemini-2.0-flash-001` | europe-west3 | Oczekuje | Weryfikacja automatyczna |
| `gemini-2.0-flash-lite-001` | us-central1 | Oczekuje | Weryfikacja automatyczna |
| `gemini-2.0-flash-lite-001` | europe-west3 | Oczekuje | Weryfikacja automatyczna |
| `gemini-2.5-flash-preview-04-17` | us-central1 | Oczekuje | Weryfikacja automatyczna |
| `gemini-2.5-flash-preview-04-17` | europe-west3 | Oczekuje | Weryfikacja automatyczna |
| `gemini-2.5-pro-preview-06-05` | us-central1 | Oczekuje | Weryfikacja automatyczna |
| `gemini-2.5-pro-preview-06-05` | europe-west3 | Oczekuje | Weryfikacja automatyczna |

> [!NOTE]
> **Co oznacza status "Oczekuje" (Reconciling)?** Wniosek został prawidłowo zapisany w chmurze i czeka na zatwierdzenie. Google automatycznie przydziela większość limitów dla pełnopłatnych kont organizacji w kilka minut. Status możesz monitorować na żywo za pomocą polecenia: `python scratch/request_quota.py --list`.

> [!WARNING]
> **Błąd NotFoundException / Limit nieistniejący w API:** 
> Jeśli skrypt zwróci błąd `NotFoundException` (twierdząc, że dany limit nie istnieje lub jest niewidoczny w `aiplatform.googleapis.com`), oznacza to, że Google Cloud jeszcze nie zsynchronizował Twojego nowego konta billingowego z rejestrem limitów API. 
> 
> **Rozwiązanie (Formularz ręczny w 1 minutę):**
> 1. Wejdź bezpośrednio do sekcji limitów w przeglądarce: [Konsola GCP Quotas](https://console.cloud.google.com/iam-admin/quotas?project=project-d4dcda6d-71f8-44d8-922)
> 2. Przefiltruj listę wpisując w polu filtracji: `generate_content_requests_per_minute_per_project_per_base_model`
> 3. Zaznacz pola wyboru (checkboxy) przy modelach w interesujących Cię regionach (np. `gemini-2.5-flash` i `gemini-2.5-pro` w `us-central1`).
> 4. Kliknij **„Edytuj limity” (Edit Quotas)** na górze tabeli.
> 5. Wpisz wartość **`120`** (lub wyższą) i wklej jedno z powyższych uzasadnień biznesowych.
> 6. Kliknij **Wyślij** (Submit). Wniosek zostanie przetworzony w tle.

### 6. Automatyczne dostosowywanie limitów (Quota Adjuster) oraz Alerty
Google Cloud oferuje w zakładce **Konfiguracja** funkcję **Dostosowywanie limitu (Quota Adjuster)** oraz system powiadomień o zmianach.

#### 🤖 Jak działa Quota Adjuster i dlaczego nie wystarczy dla Gemini?
* **Włączenie suwaka (Dostosowywanie limitu -> Włączone):** Kiedy ta opcja jest aktywna, Google automatycznie wnioskuje o zwiększenie limitów w tle (o ok. 10-20%), gdy zbliżasz się do ich wyczerpania.
* **Stan dla modeli AI:** Zgodnie z konfiguracją w Twojej konsoli, automatyczne dostosowywanie **jest aktywne (status Włączono)** również dla modeli językowych Gemini oraz modeli graficznych Imagen (pozycja `Generate content requests per minute per project per base model...`).
* **Krytyczne ograniczenie (Dlaczego to nie wystarczy?):** Quota Adjuster działa **proaktywnie i stopniowo**, analizując historyczne zużycie w cyklach dobowych. Jeśli Twój początkowy limit wynosi **5 zapytań na minutę (RPM)**, a Twój system agentowy (np. Hermes / Antigravity) nagle uruchomi 20 równoległych zapytań, chmura natychmiast odrzuci je z błędem **HTTP 429**. Automat nie podniesie limitu natychmiast w ułamku sekundy, lecz zarejestruje to jako spike i ewentualnie zawnioskuje o niewielki wzrost (np. do 10-15 RPM) w ciągu dnia.
* **Wniosek:** Automatyczne dostosowywanie to świetny system bezpieczeństwa na przyszłość, ale **nadal musisz jednorazowo, ręcznie podnieść bazowy limit (Baseline) do wartości 120 RPM (zgodnie z Kroku 2)**. Zapewni to agentom wysoki "próg startowy", a Quota Adjuster będzie go potem samoczynnie skalował w górę, jeśli Twoja aplikacja urośnie.

#### 🔔 Konfiguracja alertów i kanałów powiadomień
Aby otrzymywać powiadomienia o zmianach limitów lub awariach automatycznego dopasowania bezpośrednio na telefon lub maila:
1. Kliknij przycisk **Utwórz alert** w sekcji konfiguracji limitów.
2. Zaznacz interesujące Cię szablony:
   * *All adjustments by quota adjuster* (zmiany limitów przez automat).
   * *Quota adjuster errors and failures* (błędy/odrzucenia limitów).
3. Włącz opcję **Użyj kanału powiadomień** (Use notification channels).
4. Jeśli nie masz jeszcze skonfigurowanego kanału:
   * Kliknij w pole wyboru i wybierz **Zarządzaj kanałami powiadomień** lub przejdź do okna konfiguracji kanałów.
   * Zlokalizuj pozycję **Email** i kliknij **Add New**, a następnie wpisz swój adres e-mail (np. `ziomus83@gmail.com`).
   * Zlokalizuj pozycję **SMS** lub **Google Cloud Console App** (jeśli chcesz otrzymywać powiadomienia push w aplikacji mobilnej Google Cloud na telefonie).
5. Po dodaniu kanału wybierz go z listy rozwijanej w konfiguratorze alertu i kliknij **Utwórz** (Create).

#### ⚠️ Dlaczego błąd HTTP 429 NIE jest zależny od pory dnia?
Błąd `HTTP 429 Resource Exhausted` oznacza osiągnięcie twardego limitu zapytań (RPM) przypisanego do Twojego projektu w danej strefie chmury Google. 
* Nie ma on żadnego związku z obciążeniem sieci Google globalnie, porą dnia ani liczbą użytkowników w internecie.
* Nowe, świeże projekty GCP mają domyślnie ustawiony limit **od 1 do 5 zapytań na minutę (RPM)**, co przy pracy z autonomicznymi agentami (którzy wykonują wiele równoległych zapytań w pętli) zostaje wyczerpane w ułamku sekundy. Podniesienie limitu do 120+ RPM to jedyny sposób na bezbłędne działanie systemów agentowych.

---

## 📉 ETAP 9: Audyt Kosztów — Usuwanie zbędnych i osieroconych zasobów

Aby Twoje darmowe środki starczyły na jak najdłużej, musisz regularnie czyścić chmurę z nieużywanych zasobów, które generują stałe, ukryte koszty za przechowywanie danych (Storage & Compute):

### 1. Wirtualne Maszyny i Dyski (Compute Engine -> Disks)
Nawet jeśli wyłączysz maszynę wirtualną, Google nadal nalicza opłaty za zarezerwowaną przestrzeń jej dysku twardego!
*   Regularnie sprawdzaj zakładkę **Disks (Dyski)** w menu Compute Engine.

#### 🔧 Etap X: Włączenie usług Discovery Engine i Dialogflow (Agent Platform)

Aby w pełni wykorzystać **Vertex AI Agent Platform** (Agent Builder, Hermes, itp.), włącz następujące API w projekcie **gtrm‑project**:

```powershell
# Włącz usługi w projekcie gtrm‑project
gcloud services enable discoveryengine.googleapis.com dialogflow.googleapis.com --project=project-d4dcda6d-71f8-44d8-922
```

> **Dlaczego to ważne?**
> - **Discovery Engine** – zapewnia RAG i indeksowanie treści potrzebne do kontekstowych botów.
> - **Dialogflow** – obsługa konwersacji, webhooki i integracje z kanałami.

**Wewnętrzna notatka:** po włączeniu API w konsoli przejdź do **IAM & Admin → Quotas**, filtruj `Generate content requests per minute per project per base model` i zweryfikuj, że pozycje Gemini 2.5‑Flash, Gemini 2.5‑Pro oraz Imagen 3.0‑generate mają status **Enabled**. W razie potrzeby przygotuj zrzuty ekranu do wewnętrznej dokumentacji, zasłaniając wrażliwe dane (e‑mail, ID projektu, kwoty kredytów).

⚠️ **Uwaga** – w organizacji może obowiązywać polityka wyłączająca klucze API. To nie blokuje działania usług, ale uniemożliwia tworzenie prostych kluczy. Używaj **ADC** (Application Default Credentials) lub konta serwisowego z odpowiednimi rolami (`roles/aiplatform.admin`, `roles/dialogflow.admin`).

Po włączeniu usług możesz od razu korzystać z **Agent Builder** i **GenAI App Builder** w projekcie `project-d4dcda6d-71f8-44d8-922`.
*   Zidentyfikuj i usuń tzw. **dyski osierocone (unattached disks)** — czyli te, które w kolumnie *"Używany przez"* nie mają przypisanej żadnej aktywnej maszyny wirtualnej.

#### Komenda PowerShell do bezpiecznego usunięcia nieużywanego dysku:
```powershell
gcloud compute disks delete NAZWA_DYSKU --zone=NAZWA_STREFY_ZONE --quiet
```

[Komentarz dla składu: Zrzut ekranu przedstawiający konsolę GCP -> Compute Engine -> Disks, pokazujący kolumnę "In-use by" z pustymi polami oznaczającymi dyski osierocone (unattached).]

### 2. Zasobniki danych (Cloud Storage -> Buckets)
*   Usuwaj zasobniki utworzone automatycznie podczas dawnych testów, migracji baz danych czy jednorazowych importów plików CSV/FAQ.
*   Pamiętaj, że przechowywanie danych w regionach typu *"Multi-region"* (np. całe terytorium USA lub Europy) jest droższe niż w pojedynczych regionach lokalnych (np. `europe-west1` w Belgii).

#### Komenda PowerShell do usuwania zbędnego zasobnika wraz z zawartością:
```powershell
gcloud storage rm --recursive gs://nazwa-twojego-zasobnika
```

---

## 🌐 ETAP 10: Konfiguracja Cloudflare DNS i Wdrażanie Certyfikatów SSL

Gdy mapujesz własną subdomenę (np. `app.twojadomena.pl`) do usług Cloud Run w Google Cloud, możesz napotkać błąd **"Waiting for certificate provisioning"** lub **"Resource readiness deadline exceeded"**.

### Dlaczego tak się dzieje?
Domyślnie Cloudflare maskuje ruch i serwery docelowe, kierując go przez własne serwery proxy (status **Proxied / Pomarańczowa chmurka**). Podczas generowania darmowego certyfikatu SSL Let's Encrypt, roboty weryfikacyjne Google próbują połączyć się bezpośrednio z Twoją domeną. Ponieważ trafiają na proxy Cloudflare, weryfikacja własności domeny kończy się niepowodzeniem.

### Jak to naprawić bez stresu (Krok po Kroku):

1.  Zaloguj się do swojego panelu kontrolnego **Cloudflare**.
2.  Przejdź do domeny, na której konfigurujesz subdomenę -> sekcja **DNS -> Records**.
3.  Zlokalizuj rekord typu **A** (lub rekord **CNAME**) odpowiadający Twojej subdonienie i kierujący na adres IP/alias Google.
4.  Kliknij **Edit** przy tym rekordzie.
5.  Kliknij na pomarańczową ikonę chmurki, aby zmienić status z **Proxied (Pomarańczowa chmurka)** na **DNS Only (Szara chmurka)**.
6.  Kliknij **Save**.
7.  Wejdź do konsoli Google Cloud (Cloud Run -> Custom Domains). Google pomyślnie zweryfikuje domenę i w ciągu maksymalnie kilku godzin certyfikat SSL zostanie wystawiony i aktywowany!
8.  *(Opcjonalnie):* Po pełnej aktywacji certyfikatu możesz z powrotem włączyć pomarańczową chmurkę (Proxy) w Cloudflare, aby chronić swoją aplikację przed atakami sieciowymi.

[Komentarz dla składu: Wstaw zrzut ekranu z panelu zarządzania DNS w Cloudflare, przedstawiający rekord subdomeny typu A lub CNAME skierowany na Google Cloud Run z ikoną chmurki o kolorze szarym (DNS Only).]

---

## 🤖 ETAP 11: Nowoczesne Modele AI w Praktyce (Nomenklatura i Modele)

Budując nowoczesną infrastrukturę AI, zrezygnuj ze starszych wersji modeli. Korzystaj wyłącznie z najnowszych osiągnięć technologicznych Google Cloud Vertex AI oraz Google AI Studio:

1.  **Gemini 3.5 Flash:** Najszybszy model multimodalny. Doskonały do analizy dokumentów, wideo i obrazów, masowego przetwarzania danych i natychmiastowych odpowiedzi. Posiada gigantyczne okno kontekstowe.
2.  **Gemini 3.1 Pro:** Król zaawansowanej logiki, wieloetapowego planowania, kodowania i pisania skomplikowanych tekstów perswazyjnych (NLP). Rozumie głęboki kontekst biznesowy.
3.  **Imagen 3:** Najwyższa jakość generowania fotorealistycznych obrazów, logotypów i grafik marketingowych, cechująca się doskonałym renderowaniem napisów i detali.
4.  **Veo:** Przełomowy model do generowania wideo i dynamicznych animacji o wysokiej rozdzielczości z opisów tekstowych.

## 🤖 ETAP 12: Wdrażanie Semantycznej Bazy Wiedzy (Vertex AI Search / RAG)

Mając aktywne darmowe środki GenAI ($1000 USD), możesz w 5 minut wyposażyć swojego agenta AI w bezbłędną pamięć i wiedzę o Twoich dokumentach bez pisania ani jednej linijki kodu RAG (Retrieval-Augmented Generation).

### KROK 12.1: Przygotowanie zasobnika (Cloud Storage)
1. Przejdź do **Cloud Storage** -> **Buckets** i utwórz nowy zasobnik (np. `baza-wiedzy-jaison-project`).
2. Prześlij tam swoje pliki PDF, dokumentacje techniczne, cenniki czy oferty.

### KROK 12.2: Konfiguracja Vertex AI Search
1. Wyszukaj w konsoli GCP **„Agent Builder”** (lub **„GenAI App Builder”**).
2. Kliknij **„Create App”** i wybierz typ aplikacji **„Search”** (Wyszukiwarka).
3. Wybierz opcję **„Generic Content”** oraz typ danych **„Cloud Storage”**.
4. Wskaż swój wcześniej utworzony bucket z plikami PDF i wybierz opcję indeksowania dokumentów.

### KROK 12.3: Spięcie z Antigravity Agentic OS
1. Po zakończeniu indeksowania, przejdź do zakładki **Data Stores** w Agent Builderze.
2. Zlokalizuj i skopiuj unikalny **Data Store ID**.
3. Wklej ten identyfikator w ustawieniach bazy wiedzy (RAG) swojego agenta w edytorze. Twój agent będzie teraz automatycznie przeszukiwał chmurę przy każdym pytaniu użytkownika, całkowicie eliminując halucynacje!

> [!TIP]
> **Low-Cost Best Practice:** Trzymanie dokumentacji w Cloud Storage kosztuje zaledwie ułamki centów miesięcznie, a darmowy pakiet $1000 USD GenAI w pełni pokryje tysiące semantycznych zapytań RAG Twoich agentów w ciągu roku.

---

> **Twój sukces jest blisko:** Masz teraz przed sobą kompletną mapę chmury Google Cloud. Połączenie darmowych środków, nowoczesnych modeli AI oraz stabilnej automatyzacji da Ci niesamowitą dźwignię biznesową i operacyjną. Czas zacząć budować!
