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
1.  **Wybór Modelu**: Zmień model językowy na najnowszy stabilny z rodziny Flash (np. **`Gemini 2.5 Flash`** lub **`Gemini 2.0 Flash 1`**). Są najszybsze i najtańsze.
2.  **System Prompt (Instrukcje)**: Wklej spersonalizowany prompt nadający tożsamość asystentowi. Upewnij się, że zawiera:
    *   Zakaz używania formatowania Markdown (gwiazdek) w odpowiedziach na stronie.
    *   Instrukcję uziemienia (nie wymyślamy faktów poza bazą wiedzy).
    *   Perswazyjne wezwania do akcji (CTA) kierujące na kontakt telefoniczny.
3.  **Filtr Halucynacji**: Włącz suwak **`Ignoruj podsumowanie przy braku odpowiedzi na zapytanie`** (zmień na True), aby bot milczał i kierował do kontaktu w przypadku pytań niezwiązanych z ofertą.
4.  **Generowanie obrazów**: Pozostaw suwak *Obraz w odpowiedziach* w pozycji **`Brak źródła`** (oszczędność budżetu!).
5.  Kliknij **Zapisz i opublikuj (Save and publish)**.

---

## 🛠️ Jak Uruchomić to na Stronie Klienta?
Gdy indeksowanie dobiegnie końca (około 20-30 minut), przejdź do zakładki **Integracja (Integration)** w lewym menu. Masz do wyboru dwie metody integracji bota na stronie:

1.  **Gotowy Widget (Najprostsza — Low-Code)**:
    *   Google wygeneruje dla Ciebie gotowy kod JavaScript (zwykle ok. 10 linii kodu), który po prostu wklejasz w sekcji `<body>` w kodzie HTML strony klienta.
    *   Widget wyświetli w prawym dolnym rogu strony elegancką, pływającą ikonkę czatu, po kliknięciu której otwiera się nowoczesne okno rozmowy.
2.  **Integracja przez API (Dla Programistów — Custom UI)**:
    *   Jeśli klient życzy sobie unikalnego wyglądu czatu stworzonego od zera we własnym CSS/React, możesz odpytywać Vertex AI Search za pomocą zapytań REST API lub oficjalnego SDK Google Cloud, pobierając wygenerowane podsumowania i prezentując je we własnym szablonie.
