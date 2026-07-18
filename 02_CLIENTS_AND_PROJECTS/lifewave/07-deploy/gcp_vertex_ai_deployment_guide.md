# 🌐 Instrukcja Konfiguracji Vertex AI Search i Wdrożenia Portalu Jaison X2O

Gratulacje! Wszystkie kluczowe pliki bazy wiedzy, instrukcje i patenty naukowe zostały **automatycznie i pomyślnie przesłane** do Twoich kontenerów w chmurze **Google Cloud Storage (GCS)** za pomocą bezpiecznego klucza konta usługi `x2o-service@jaison-x2o-portal.iam.gserviceaccount.com`.

Poniższy podręcznik opisuje krok po kroku, jak skonfigurować zaawansowaną, **mieszaną architekturę wyszukiwania (Dual Data-Store)**, która łączy statyczne dokumenty z chmury (GCS) z dynamicznym indeksowaniem Twojego portalu (**Web Store**) oraz oficjalnych źródeł naukowych.

---

## 📦 1. Status Zasobów w Google Cloud Storage

Pliki naukowe i biznesowe zostały poprawnie wgrane i są gotowe do zindeksowania. Oto struktura Twoich bucketów:

### 📢 A. Bucket Marketingowo-Biznesowy: `gs://x2o-marketing-knowledge-jaison-x2o-portal/`
*Ten bucket zasila bota sprzedażowego na stronie głównej (`index.html`).*

| Lp. | Nazwa Pliku | Rozmiar | Opis i Rola w Datastore |
| :--- | :--- | :--- | :--- |
| 1 | `lifewave-science-kb.md` | ~5.8 KB | ADHD-friendly baza wiedzy naukowej (komórki macierzyste, EZ Water). |
| 2 | `lifewave-patch-patent.pdf` | ~53 KB | Oficjalny patent technologii plastrów fototerapeutycznych (US10716953B1). |
| 3 | `lifewave-patch-yage-glutathione-patent.pdf` | ~637 KB | Oficjalny patent na podnoszenie poziomu glutationu za pomocą światła własnego ciała. |
| 4 | `Czas-na-Lifewave (1).pdf` | ~5.4 MB | Oficjalna prezentacja biznesowa modelu MLM "LifeWave for Life" i zarobków. |

### 🔧 B. Bucket Techniczno-Eksploatacyjny: `gs://x2o-tech-knowledge-jaison-x2o-portal/`
*Ten bucket zasila asystenta serwisowego na podstronie instrukcji (`x2o-guide-pl.html`).*

| Lp. | Nazwa Pliku | Rozmiar | Opis i Rola w Datastore |
| :--- | :--- | :--- | :--- |
| 1 | `Instrukcja Users Guide X2O LifeWave.pdf` | ~4.6 MB | Oryginalny, techniczny podręcznik obsługi, czyszczenia i kodów błędów stacji X2O™. |
| 2 | `x2o-guide-pl.html` | ~98 KB | Zlokalizowany, prosty polski przewodnik użytkownika z sekcją FAQ. |

---

## 🧠 2. Mieszana Architektura Wyszukiwania (Dual Data-Store)

Zgodnie z Twoją dyspozycją, dla chatbota marketingowego na stronie głównej wdrażamy **model hybrydowy**. Łączy on dokumenty nieustrukturyzowane (patenty, prezentacje) z pełnym indeksowaniem witryny internetowej w czasie rzeczywistym (**Web Store / Website Search**). Dzięki temu, gdy tylko zaktualizujesz portal lub dodasz nowe treści na `x2o.jaison.pl`, wyszukiwarka Google automatycznie je przeanalizuje bez konieczności ponownego wgrywania plików!

```mermaid
graph TD
    subgraph Wyszukiwarka Marketingowa (x2o-marketing-search)
        A1[gs://x2o-marketing-knowledge-jaison-x2o-portal/*] -->|Indeksowanie GCS| DS1[(Data Store 1: x2o-marketing-gcs-engine)]
        A2[Witryna x2o.jaison.pl/* + Whitelista Linków Naukowych] -->|Crawl / Web Store| DS2[(Data Store 2: x2o-marketing-web-engine)]
        
        DS1 --> APP1[App: x2o-marketing-search]
        DS2 --> APP1
    end
    
    subgraph Wyszukiwarka Techniczna (x2o-technical-search)
        B1[gs://x2o-tech-knowledge-jaison-x2o-portal/*] -->|Indeksowanie GCS| DS3[(Data Store: x2o-technical-engine)]
        DS3 --> APP2[App: x2o-technical-search]
    end
```

---

## 🛠️ 3. Konfiguracja Baz Danych (Data Stores) w Google Cloud

Zaloguj się do [GCP Console](https://console.cloud.google.com/) w projekcie `jaison-x2o-portal` i przejdź do sekcji **Vertex AI Agent Builder** (wyszukaj w górnym pasku wyszukiwania).

### 🔹 KROK A: Baza Plików GCS (`x2o-marketing-gcs-engine`)
1. W menu po lewej stronie kliknij **"Data Stores"**, a następnie **"Create Data Store"**.
2. Jako źródło danych wybierz **"Cloud Storage"**.
3. W polu ścieżki wpisz: `gs://x2o-marketing-knowledge-jaison-x2o-portal/*` (lub kliknij *Browse*).
4. Wybierz opcję **"Unstructured documents"** (Dokumenty nieustrukturyzowane).
5. Kliknij **"Continue"**.
6. Nazwij bazę dokładnie: `x2o-marketing-gcs-engine`.
7. Kliknij **"Create"**.

### 🔹 KROK B: Baza Witryny & Linków Naukowych (`x2o-marketing-web-engine`)
1. Kliknij **"Create Data Store"** ponownie.
2. Jako źródło danych wybierz **"Website"** (Web Store / Website Search).
3. Kliknij **"Continue"**.
4. W sekcji **Sites to crawl** dodaj adres swojej głównej domeny oraz wszystkie dozwolone linki naukowe:
   *   `https://x2o.jaison.pl/*` *(Twoja domena po deployu – roboty Google automatycznie zindeksują całą witrynę!)*
   *   `https://lifewave.com/*`
   *   `https://patents.google.com/patent/US10716953B1/en`
   *   `https://networkmagazyn.pl/lifewave-corporate-swiety-graal-w-dziedzinie-zdrowia-i-biznesu-spolecznosciowego/`
   *   `https://researchopenworld.com/double-blind-testing-of-the-lifewave-x39-patch-to-determine-ghk-cu-production-levels/`
   *   `https://clinmedjournals.org/articles/ijsem/international-journal-of-sports-and-exercise-medicine-ijsem-9-250.php`
5. Wybierz opcję **"Advanced crawl settings"** (możesz pozostawić domyślne parametry głębokości indeksowania).
6. Kliknij **"Continue"**.
7. Nazwij bazę dokładnie: `x2o-marketing-web-engine`.
8. Kliknij **"Create"**.

### 🔹 KROK C: Baza Serwisowa/Techniczna (`x2o-technical-engine`)
1. Kliknij **"Create Data Store"** po raz trzeci.
2. Wybierz **"Cloud Storage"**.
3. Wskaż ścieżkę: `gs://x2o-tech-knowledge-jaison-x2o-portal/*`.
4. Wybierz **"Unstructured documents"**.
5. Kliknij **"Continue"**.
6. Nazwij bazę dokładnie: `x2o-technical-engine`.
7. Kliknij **"Create"**.

---

## 🤖 4. Tworzenie i Publikowanie Aplikacji (Apps)

Teraz połączymy bazy danych w dwie zunifikowane aplikacje wyszukiwania, z którymi będzie komunikować się nasz kod PHP na serwerze:

### 📱 1. Aplikacja Marketingowa (`x2o-marketing-search`)
1. W menu Vertex AI Agent Builder przejdź do zakładki **"Apps"** i kliknij **"Create App"**.
2. Wybierz typ aplikacji: **"Search"** (Wyszukiwanie).
3. Jako platformę docelową wybierz **"Generic"** (ogólna aplikacja API).
4. Nazwij aplikację: `x2o-marketing-search`.
5. W kroku wyboru baz danych **zaznacz pola wyboru obok dwóch baz**:
   *   `x2o-marketing-gcs-engine`
   *   `x2o-marketing-web-engine`
   *(Dzięki temu Twój chatbot na stronie głównej zyska potężną, mieszaną inteligencję łączącą patenty GCS z zawartością portalu i linkami zewnętrznymi!)*
6. Kliknij **"Create"**.

### 📱 2. Aplikacja Techniczna (`x2o-technical-search`)
1. Kliknij **"Create App"** ponownie, wybierz typ **"Search"** i platformę **"Generic"**.
2. Nazwij ją: `x2o-technical-search`.
3. W kroku wyboru baz danych zaznacz wyłącznie bazę serwisową:
   *   `x2o-technical-engine`
4. Kliknij **"Create"**.

---

## 🚀 5. Finalne Wdrożenie Portalu (FTP / Hosting)

Gdy tylko ukończysz konfigurację w konsoli GCP, możecie z Moniką przystąpić do wdrożenia kodu na serwer hostingowy (np. darmowy lub współdzielony podpięty pod domenę `x2o.jaison.pl`).

### 📋 Lista plików do umieszczenia w głównym katalogu serwera (public_html / www):
1.  **`index.html`** — Strona główna z marketingowym chatbotem i animacją cząsteczek 3D.
2.  **`x2o-guide-pl.html`** — Przewodnik serwisowy z technicznym chatbotem.
3.  **`php/chat.php`** — Skrypt proxy łączący się z API Vertex AI (obsługuje obie aplikacje wyszukiwania w zależności od parametru `engine`).
4.  **`php/key.json`** — Pobrany przez Ciebie klucz dostępu do konta usługi GCP (musi znajdować się w tym samym folderze co `chat.php`).
5.  **`images/`** — Folder z grafikami, luksusowym nowym logotypem Jaison X2O oraz tłem wody.

---

## 👥 6. Uruchomienie Podgrup WhatsApp i n8n

Zgodnie z zatwierdzonym planem automatyzacji WhatsApp [whatsapp_broadcast_automation_plan.md](file:///C:/Users/user/.gemini/antigravity/brain/fabf24a5-2645-426d-839b-ec6e33c3a29a/whatsapp_broadcast_automation_plan.md):

1.  **Załóż podgrupy:** Tomasz, Monika i Ania powinni utworzyć 3 dedykowane grupy dyskusyjne na WhatsApp (Klub X2O, Fototerapia X39, Biznes MLM).
2.  **Ustaw okładki:** Użyj luksusowych grafik, które wygenerowaliśmy dla Ciebie w katalogu artefaktów (są one w pełni zoptymalizowane pod standardy premium):
    *   Grafika dla wody X2O: [whatsapp_group_x2o_water_1784196649379.png](file:///C:/Users/user/.gemini/antigravity/brain/fabf24a5-2645-426d-839b-ec6e33c3a29a/whatsapp_group_x2o_water_1784196649379.png)
    *   Grafika dla plastrów X39: [whatsapp_group_x39_light_1784196690604.png](file:///C:/Users/user/.gemini/antigravity/brain/fabf24a5-2645-426d-839b-ec6e33c3a29a/whatsapp_group_x39_light_1784196690604.png)
3.  **Uruchom n8n:** Zaimportuj węzły dystrybucyjne n8n i połącz je z wybraną bramką API (np. darmowym Evolution API lub Z-API za ok. 39 zł/msc).

---

> [!TIP]
> **Bezpieczeństwo i Elastyczność:** Skrypt proxy `php/chat.php` posiada wbudowany, inteligentny mechanizm „mock-fallback”. Oznacza to, że dopóki nie utworzysz i nie aktywujesz datastores w konsoli GCP, chatboty na stronie nie zepsują się – będą odpowiadać eleganckimi, luksusowymi odpowiedziami lokalnymi o wodzie EZ i plastrach X39. Gdy tylko skończysz klikać w GCP, system automatycznie przełączy się na sztuczną inteligencję Vertex AI!
