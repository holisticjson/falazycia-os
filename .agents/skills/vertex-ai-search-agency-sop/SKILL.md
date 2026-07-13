---
name: vertex-ai-search-agency-sop
description: Master SOP agencji Jaison (jaison.pl) do wdrażania niskokosztowych, hybrydowych chatbotów Vertex AI Search dla klientów B2B w ramach darmowych środków chmurowych GCP ($300 + $1000 GenAI).
---

# 🤖 Master SOP: Niskokosztowy Bot Vertex AI Search (Blended Search)
Niniejsza instrukcja stanowi kanoniczny standard wdrożeniowy agencji **Jaison** (`jaison.pl`). Pozwala na uruchomienie zaawansowanego bota hybrydowego dla klienta B2B, wykorzystując darmowe pakiety kredytów startowych Google Cloud Platform (GCP) w taki sposób, aby chatbot działał **całkowicie bezpłatnie przez okres do 12 miesięcy**.

---

## 🎯 Trzy Filary Niskich Kosztów (Low-Cost First)
1.  **Darmowe Kredyty GCP ($300)**: Pokrywają infrastrukturę pomocniczą (transfer danych, Cloud Storage, operacje API) na start.
2.  **Kredyt GenAI App Builder ($1000)**: Przyznawany automatycznie po aktywacji pierwszej aplikacji Vertex AI Search w organizacji Google Cloud. Pokrywa koszty zapytań wyszukiwarki i indeksowania witryn.
3.  **Zakaz Drogich Funkcji**:
    *   `Obraz w odpowiedziach` musi być ustawiony na **`Brak źródła`** (Generowanie obrazów AI przez Imagen jest rozliczane oddzielnie i może błyskawicznie drenować budżet).
    *   `Advanced Generative Answers` (zaawansowany chatbot Dialogflow CX) musi pozostać wyłączony – standardowy asystent Q&A wbudowany w wyszukiwarkę jest całkowicie wystarczający i tańszy.

---

## 📋 Schemat Krok po Kroku (Do Powielania dla Klientów)

### Krok 1: Założenie Projektu i Aktywacja API
1.  Zaloguj się na konto Google Cloud przydzielone dla klienta.
2.  Utwórz nowy projekt GCP (np. `nazwa-klienta-project`).
3.  Włącz rozliczenia (Paid Billing Account / Free Trial) – bez podpiętej karty kredytowej Google nie zezwoli na korzystanie z usług AI.
4.  Otwórz Cloud Shell / Terminal lokalny i aktywuj niezbędne API (jedna linia PowerShell):
    ```powershell
    gcloud services enable storage.googleapis.com discoveryengine.googleapis.com --project="ID_PROJEKTU_KLIENTA"
    ```

### Krok 2: Utworzenie Magazynu Plików Wiedzy (Cloud Storage)
W celu zasilenia bota poufnymi informacjami (instrukcje techniczne, wewnętrzne cenniki hurtowe, procedury SOP), utwórz bezpieczny kontener w GCS:
1.  Utwórz bucket (rekomendowany region to Warszawa `europe-central2` ze względu na RODO/GDPR i opóźnienia):
    ```powershell
    gcloud storage buckets create gs://nazwa-klienta-knowledge --location=europe-central2 --project="ID_PROJEKTU_KLIENTA"
    ```
2.  **Bezwzględnie włącz jednolity dostęp na poziomie bucketu** (Uniform Bucket-Level Access), aby zablokować możliwość przypadkowego publicznego udostępnienia dokumentów:
    ```powershell
    gcloud storage buckets update gs://nazwa-klienta-knowledge --uniform-bucket-level-access --project="ID_PROJEKTU_KLIENTA"
    ```
3.  Załóż w buckecie strukturę logicznych folderów, wgrywając puste pliki `.keep` (zapobiega to usuwaniu pustych folderów przez Google):
    *   📁 `01_public-site/` (statyczne kopie stron klienta)
    *   📁 `02_lead-magnets/` (artykuły, PDF-y z perswazyjnym copywritingiem NLP)
    *   📁 `03_service-sop/` (wewnętrzne instrukcje techniczne)
    *   📁 `04_sales-playbooks/` (skrypty rozmów handlowych)
4.  **[KRYTYCZNE] Nadanie ról IAM dla GCS:** Gdy aktywowano UBLA (Uniform Bucket-Level Access), uprawnienia domyślne dla twórcy bucketu i systemowego konta Vertex AI zostają zablokowane. Agent musi automatycznie odpalić następujące komendy by wymusić twarde przypisanie ról IAM. Zastąp najpierw `NUMER_PROJEKTU_KLIENTA` poprawnym identyfikatorem liczbowym, a `MAIL_KLIENTA` głównym administratorem.
    ```powershell
    # Pobierz numer projektu (Project Number), skopiuj go:
    gcloud projects describe "ID_PROJEKTU_KLIENTA" --format="value(projectNumber)"
    
    # Nadaj uprawnienia administracyjne dla klienta:
    gcloud storage buckets add-iam-policy-binding gs://nazwa-klienta-knowledge --member="user:MAIL_KLIENTA" --role="roles/storage.admin"
    
    # Nadaj niezbędne uprawnienia do podglądu (Object Viewer) dla systemowego konta Discovery Engine w Vertex AI:
    gcloud storage buckets add-iam-policy-binding gs://nazwa-klienta-knowledge --member="serviceAccount:service-NUMER_PROJEKTU_KLIENTA@gcp-sa-discoveryengine.iam.gserviceaccount.com" --role="roles/storage.objectViewer"
    ```

### Krok 3: Konfiguracja Magazynu Danych GCS (Data Store)
1.  W konsoli GCP przejdź do **Vertex AI Agent Builder** -> **Data Stores**.
2.  Kliknij **Create Data Store** -> wybierz **Cloud Storage**.
3.  Wklej ścieżkę do bucketu: `gs://nazwa-klienta-knowledge/`.
4.  **Kluczowy Wybór**: Zaznacz **Dokumenty / Dane nieuporządkowane (Unstructured documents)**.
5.  Ustaw częstotliwość synchronizacji na **Codziennie (Daily)**, aby bot automatycznie uczył się z nowych plików wgrywanych przez techników.
6.  Nazwij go `nazwa-klienta-gcs-store`.

### Krok 4: Konfiguracja Magazynu Witryny (Data Store)
1.  Kliknij ponownie **Create Data Store** -> wybierz **Website**.
2.  Zaznacz **Zaawansowane indeksowanie witryn (Advanced Website Indexing)** (wymagane do poprawnego renderowania dynamicznego).
3.  W polu *Witryny do uwzględnienia* wpisz domenę klienta: `domena-klienta.pl/*` oraz `www.domena-klienta.pl/*`.
4.  W polu *Witryny do wykluczenia* wpisz panele logowania, koszyki zakupowe i panele administratora (jeśli klient ma WordPressa, wyklucz `/wp-admin/*`, `/koszyk/*` itd.). Jeśli strona to czysty, statyczny HTML – **pozostaw to pole całkowicie puste**.
5.  Nazwij go `nazwa-klienta-website-store`.

### Krok 5: Utworzenie i Spięcie Aplikacji (Blended Search)
1.  W menu po lewej przejdź do **Apps** -> **Create App**.
2.  Wybierz zakładkę **Wyszukiwarka i asystent** -> karta **Twoja wyszukiwarka (ogólna)**.
3.  Zaznacz opcję *Funkcje wersji Enterprise* oraz *Odpowiedzi generatywne*.
4.  Nazwij aplikację (np. `Nazwa Klienta Serwis Bot`) i wpisz nazwę firmy.
5.  W sekcji lokalizacji wybierz **`eu (wiele regionów w Unii Europejskiej)`**.
6.  W kroku wyboru danych **zaznacz oba utworzone magazyny**:
    *   `nazwa-klienta-gcs-store`
    *   `nazwa-klienta-website-store`
7.  Potwierdź i utwórz aplikację.

### Krok 6: Dostrajanie i System Prompt (Konfiguracja Premium)
Przejdź do sekcji **Konfiguracja** (Configuration) -> zakładka **UI / Dostrajanie**:
1.  **Wybór Modelu**: Zmień model językowy na **`Gemini 2.5 Flash`** (aktualnie optymalny model pod kątem relacji jakość/koszt w zastosowaniach hybrydowych RAG). Nie wybieraj przestarzałych wersji (gemini-pro).
2.  **System Prompt (Instrukcje)**: Zastąp domyślny komunikat tym spersonalizowanym szablonem "Ghost v2":
    
    ```text
    Jesteś wirtualnym doradcą i asystentem AI reprezentującym markę Jaison (jaison.pl), agencję wdrażającą infrastrukturę opartą o sztuczną inteligencję. Twoim celem jest merytoryczna pomoc i kwalifikacja leadów biznesowych.
    Kierujesz się zasadami Ghost v2 oraz architekturą 'Low-Friction'. Pisz zwięźle, bez korpo-żargonu, jak specjalista B2B.
    Masz BEZWZGLĘDNY ZAKAZ używania formatowania Markdown (żadnych pogrubień **, kursyw *, nagłówków ###). Pisz czystym tekstem.
    
    TWOJE ZADANIE - AUDYT (21 PYTAŃ):
    Gdy rozpoznasz, że klient jest zainteresowany współpracą lub szuka rozwiązania, zaproponuj bezpłatny audyt potrzeb (składający się łącznie z 21 pytań ewaluacyjnych z Twojej bazy wiedzy, opartych m.in. o Umiejętności Jutra).
    Zadawaj pytania naturalnie, maksymalnie 1-2 na raz, wchodząc w dialog. Kategoryzuj odpowiedzi.
    Jeśli klient nie zna odpowiedzi na jakieś pytanie, nie dotyczy go ono, lub jawnie wyrazi chęć bezpośredniej rozmowy z człowiekiem, NATYCHMIAST przerwij audyt i zaproponuj bezpośredni kontakt.
    
    ŚCIEŻKI KONTAKTU (Zawsze podawaj te konkretne linki, aby system wygenerował klikalne adresy URL):
    Gdy klient chce się skontaktować lub umówić, przedstaw mu 3 opcje wyboru podając te dokładne linki w swoim tekście:
    1. Umówienie spotkania wideo: https://cal.com/jaison
    2. Szybka wiadomość na WhatsApp (bezpośrednio do Tomasza): https://wa.me/48791636644
    3. Wiadomość e-mail (wywołuje program pocztowy): mailto:hello@jaison.pl
    
    Zawsze odpowiadaj z dużą empatią, dopasowując się do problemu rozmówcy. Jeśli czegoś nie wiesz, nie zmyślaj - od razu kieruj do człowieka używając powyższych ścieżek kontaktu.
    ```
3.  **Filtr Halucynacji**: Włącz suwak **`Ignoruj podsumowanie przy braku odpowiedzi na zapytanie`** (zmień na True), aby bot milczał i kierował do kontaktu w przypadku pytań niezwiązanych z ofertą.
4.  **Generowanie obrazów**: Pozostaw suwak *Obraz w odpowiedziach* w pozycji **`Brak źródła`** (oszczędność budżetu!).
5.  Kliknij **Zapisz i opublikuj (Save and publish)**.

---

## 🛠️ Jak Uruchomić to na Stronie Klienta?

Gdy konfiguracja jest gotowa, przejdź do zakładki **Integracja (Integration)** w lewym menu. Aby uruchomić czat na publicznej witrynie klienta bez konieczności kodowania skomplikowanego backendu (JWT), wykonaj poniższe kroki:

### Krok 1: Wybór Autoryzacji Publicznej i Whitelisting
1.  **Bezwzględnie zaznacz opcję: `Dostęp publiczny` (Public access)**. 
    *   *Uwaga:* Domyślnie zaznaczony jest "JWT lub OAuth", co wymagałoby pisania serwerowej aplikacji generującej tokeny. Dla statycznej strony HTML wybór `Dostęp publiczny` pozwala na bezpośrednie uruchomienie bota!
2.  W polu **Dodaj dozwolone domeny dla widżetu** wpisz domenę klienta bez protokołu (np. `jaison.pl`) i kliknij niebieski przycisk **Dodaj (Add)**. Zrób to dla wariantu z www i bez www (`jaison.pl` oraz `www.jaison.pl`).
3.  Zjedź niżej i kliknij przycisk **Zapisz (Save)**.
4.  Gdy to zrobisz, kod w polu niżej automatycznie się zaktualizuje i otrzyma skompilowany parametr `configId="Twój-Unikalny-Hash-Kodu"`.
5.  **Podanie ID do Agenta:** Klient / operator NIE wkleja kodu do HTML ręcznie! Jego zadaniem jest jedynie skopiowanie z panelu wygenerowanego ciągu znaków (hasha z atrybutu `configId`) i wklejenie go z powrotem na czat agentowi AntiGravity.
6.  **Agent zastępuje kod:** Agent AI w tle podmienia wartość `configId="..."` w pliku HTML za pomocą narzędzi zastępowania tekstu (np. sed / multi_replace_file_content) i puszcza nowy `deploy`.

---

### Krok 2: Dostosowanie Wyglądu i Premium Design (Vanilla CSS & HTML)

Domyślne pole wyszukiwania Google (`<input id="searchwidgetTrigger" />`) wygląda bardzo prosto i surowo. Aby nadać projektowi standard **premium** i dopasować go do identyfikacji wizualnej marki (np. niebiesko-granatowych barw Coolfon), wdrożymy **autorski pływający przycisk czatu (Launcher)**, który po kliknięciu wywoła okno asystenta z niesamowitym efektem wizualnym!

Skopiuj i wklej poniższy kompletny kod na sam dół strony internetowej klienta (tuż przed tagiem `</body>`):

```html
<!-- ========================================== -->
<!-- 🤖 PREMIUM VERTEX AI CHATBOT BY JAISON.PL  -->
<!-- ========================================== -->

<!-- 1. Stylizacja Premium dla Pływającego Przycisku i Chmurki (Vanilla CSS) -->
<style>
  /* Pływający Przycisk Czatu (Launcher) */
  #coolfon-chat-launcher {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1e40af 0%, #0f172a 100%); /* Granatowo-niebieski gradient Coolfon */
    box-shadow: 0 8px 30px rgba(30, 64, 175, 0.4);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999999;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 2px solid rgba(255, 255, 255, 0.1);
  }

  /* Efekt Hover na przycisku */
  #coolfon-chat-launcher:hover {
    transform: scale(1.1) translateY(-3px);
    box-shadow: 0 12px 35px rgba(30, 64, 175, 0.6);
    background: linear-gradient(135deg, #2563eb 0%, #0f172a 100%);
  }

  /* Animacja pulsującego okręgu wokół przycisku */
  #coolfon-chat-launcher::before {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: rgba(30, 64, 175, 0.4);
    animation: coolfon-chat-pulse 2s infinite;
    z-index: -1;
  }

  /* Ikona czatu (SVG) */
  #coolfon-chat-launcher svg {
    width: 28px;
    height: 28px;
    fill: none;
    stroke: #ffffff;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
    transition: transform 0.3s ease;
  }

  #coolfon-chat-launcher:hover svg {
    transform: rotate(5deg);
  }

  /* Chmurka podpowiedzi (Tooltip) */
  #coolfon-chat-tooltip {
    position: absolute;
    right: 80px; /* Po lewej stronie przycisku */
    white-space: nowrap;
    background: #0f172a; /* Ciemny granat pasujący do marki */
    color: #ffffff;
    padding: 10px 18px;
    border-radius: 20px 20px 0 20px; /* Zaokrąglony dymek w stylu dymku czatu */
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.3px;
    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.25);
    opacity: 0;
    transform: translateX(15px);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    pointer-events: none; /* Zapobiega blokowaniu kliknięć pod dymkiem */
    border: 1px solid rgba(255, 255, 255, 0.15);
  }

  /* Mały trójkąt (dzióbek) chmurki */
  #coolfon-chat-tooltip::after {
    content: '';
    position: absolute;
    right: -6px;
    bottom: -1px;
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 6px 0 6px 8px;
    border-color: transparent transparent transparent #0f172a;
  }

  /* Aktywna widoczna chmurka */
  #coolfon-chat-tooltip.visible {
    opacity: 1;
    transform: translateX(0);
  }

  /* Klasyczny hover na przycisk również wywołuje dymek */
  #coolfon-chat-launcher:hover #coolfon-chat-tooltip {
    opacity: 1;
    transform: translateX(0);
  }

  @keyframes coolfon-chat-pulse {
    0% {
      transform: scale(1);
      opacity: 0.8;
    }
    100% {
      transform: scale(1.4);
      opacity: 0;
    }
  }
</style>

<!-- 2. Autorski Launcher, Chmurka i Elementy Kontrolne bota -->
<div id="coolfon-chat-launcher" title="Porozmawiaj z asystentem AI">
  <!-- Pływająca chmurka zachęcająca (Tooltip) -->
  <div id="coolfon-chat-tooltip">Zapytaj bota Coolfon! ⚡</div>
  
  <!-- Elegancka ikona czatu w formacie SVG -->
  <svg viewBox="0 0 24 24">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
  </svg>
</div>

<!-- Ukryty element wyzwalający wymagany przez Google -->
<input type="text" id="searchwidgetTrigger" style="display: none !important;" />

<!-- 3. Skrypty Google Vertex AI Search -->
<script src="https://cloud.google.com/ai/gen-app-builder/client?hl=pl"></script>

<gen-search-widget
  configId="f0e7372e-fee0-4943-9c8d-aad4282ed181"
  location="eu"
  triggerId="searchwidgetTrigger">
</gen-search-widget>

<!-- 4. Skrypt łączący nasz ładny przycisk z ukrytym wyzwalaczem Google -->
<script>
  // Wywołanie kliknięcia w widget
  document.getElementById('coolfon-chat-launcher').addEventListener('click', function() {
    document.getElementById('searchwidgetTrigger').click();
  });

  // Inteligentny UX: Automatyczne wysunięcie chmurki po 1.5 sekundy (walka ze ślepotą banerową)
  setTimeout(function() {
    var tooltip = document.getElementById('coolfon-chat-tooltip');
    if (tooltip) {
      tooltip.classList.add('visible');
    }
  }, 1500);

  // Ukrycie chmurki po najechaniu myszką, by nie przeszkadzała w czytaniu strony
  document.getElementById('coolfon-chat-launcher').addEventListener('mouseenter', function() {
    var tooltip = document.getElementById('coolfon-chat-tooltip');
    if (tooltip) {
      tooltip.classList.remove('visible');
    }
  });
</script>
```

*   **Powyższy kod działa w 100% z czystym HTML/CSS i wtapia się w kolorystykę Coolfon.** Pływająca ikonka pulsuje w prawym dolnym rogu ekranu, a po jej kliknięciu natychmiast wysuwa się oficjalny panel asystenta AI z cytowaniami źródeł!

