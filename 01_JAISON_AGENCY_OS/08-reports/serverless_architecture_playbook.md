# 🌌 Jaison OS — Serverless Architecture, Marketing & Execution Playbook

Ten dokument to Twój strategiczny **oręż biznesowy** oraz podręcznik operacyjny. Łączy on głęboką architekturę techniczną i routing modeli LLM z gotowymi narzędziami do zamykania klientów B2B na wdrożenia High-Ticket (**10 000 PLN+**), analizą produktów cyfrowych, demaskowaniem haczyków tradycyjnego hostingu oraz precyzyjnymi promptami dla Twojej floty wirtualnych agentów.

---

## 🔑 1. Bezawaryjny Routing LLM & Ochrona Przed Limitami (NVIDIA NIM vs. Google AI Studio)

Darmowy tier w Google AI Studio (Free Tier) posiada pewne ograniczenia zapytań na minutę (RPM) oraz na dzień (TPM). Aby skanowanie rynku (Lead Radar) oraz głębokie analizy w tle przez agentów nigdy nie napotykały blokad (błędu `429 Rate Limit`), wdrożyliśmy inteligentny **Smart Routing**.

> [!IMPORTANT]
> **JAK DZIAŁA SMART ROUTING W JAISON OS:**
> 1.  **Primary Model:** System wysyła zapytanie do Gemini 2.5 Flash / Pro przez oficjalne Google AI Studio za pomocą Twojego `GEMINI_API_KEY`.
> 2.  **Smartwatch Fallback (NVIDIA NIM):** W przypadku wyczerpania limitów (lub awarii), system automatycznie i bezszumnie przekierowuje zapytanie do **NVIDIA NIM (build.nvidia.com)**, odpytując model `meta/llama-3.1-70b-instruct` lub `meta/llama-3.3-70b-instruct`.
> 3.  **Korzyść:** NVIDIA NIM daje **1000 darmowych zapytań deweloperskich miesięcznie bez karty** – idealna rezerwa na ciężkie skanowanie w pętli.

### 🧠 Zaawansowany Reasoning (Wnioskowanie): Kimi K3 & GLM-5
W przypadku bardzo złożonych zadań (analiza nisz YouTube, opracowywanie ofert High-Ticket), agenci w tle mogą zostać przekierowani do chińskich modeli o wysokim poziomie logicznego wnioskowania (Reasoning) jak **Kimi K3** oraz **GLM-5** (dostępnych tanio na Together AI i Fireworks AI). Modele te, przed wygenerowaniem tekstu, przechodzą przez wewnętrzny proces myślowy (Chain-of-Thought), co gwarantuje bezkonkurencyjną głębię analiz marketingowych bez lock-inu w ekosystemie OpenAI/Anthropic.

### ⚙️ Konfiguracja .env (W głównym katalogu `01_JAISON_AGENCY_OS`):
Dla pełnej bezawaryjności uzupełnij w `.env` poniższe zmienne:
```env
GEMINI_API_KEY="twój_klucz_z_google_ai_studio"
NVIDIA_API_KEY="twój_darmowy_klucz_z_build.nvidia.com"
TELEGRAM_BOT_TOKEN="token_bota"
TELEGRAM_CHAT_ID="id_czatu"
N8N_WEBHOOK_URL="url_twojej_instancji_n8n"
```

---

## ⚔️ 2. Hostinger & InterServer VPS vs Jaison Serverless (GCP Cloud Run)

Kiedy klienci B2B mówią Ci: *"Ale po co nam Google Cloud Run? Przecież Hostinger ma tani VPS za 20 PLN, darmową domenę na rok i 30 dni gwarancji zwrotu pieniędzy, a InterServer reklamuje się za 6 USD za plaster!"* — użyj poniższego, bezlitosnego zestawienia haczyków u konkurencji, aby natychmiast uzasadnić cenę wdrożenia premium:

### ⚠️ Ukryte Haczyki Tradycyjnych VPS i Hostingów:

#### 1. Hostinger — Sztuczki cenowe i "Darmowa Domena":
*   **Pułapka Ceny Odnowienia (Renewal Price):** Reklamowana cena (np. 5.99 USD/mc) obowiązuje **wyłącznie przy płatności z góry za 48 miesięcy** (4 lata!). Przy płatności rocznej cena wzrasta, a przy odnowieniu umowy po tym okresie gwałtownie rośnie o 200-300%.
*   **Haczyk Darmowej Domeny:** Jeśli klient zrezygnuje z usług w ramach "30-dniowej gwarancji zwrotu pieniędzy", Hostinger potrąci z jego zwrotu pełną, standardową (często znacznie zawyżoną) cenę rejestracji domeny (ok. 15-25 USD). Dodatkowo, ceny odnowienia domen w kolejnych latach są u nich drastycznie wyższe niż u hurtowników (np. Cloudflare Registrar).
*   **Blokady i Throttling:** Na hostingu współdzielonym, jeśli strona wygeneruje nagły ruch (np. mailing lub wiral), system natychmiast nakłada ograniczenia procesora (throttling) lub całkowicie wyłącza witrynę z błędem *Resource Limit Exceeded*.

#### 2. InterServer VPS — "Zasada Plastrów" i Opóźnienia:
*   **Pułapka Plastrów (Slices):** Oferta $6/mc za "slice" (plaster) brzmi dobrze, ale 1 slice to tylko 1 vCPU i 2GB RAM. To zbyt mało, by stabilnie utrzymać n8n, bazę PostgreSQL i skaner AI. Klient musi dokupić co najmniej 3-4 plastry, co podnosi realną cenę do $18-$24/mc.
*   **Przekleństwo Opóźnienia (High Latency):** Ich centra danych znajdują się w USA (New Jersey, Los Angeles). Brak lokalizacji w Europie Środkowej powoduje, że zapytania bazy danych, RAG oraz interfejsy ładują się polskiemu użytkownikowi z zauważalnym opóźnieniem (nawet 150-200ms na żądanie).
*   **Brak Wsparcia (Unmanaged):** Niskobudżetowe VPS-y są całkowicie niezarządzane (Unmanaged). Klient dostaje pusty terminal Linuxa. Bez opłacania administratora SysOps, klient sam musi konfigurować firewalle, certyfikaty SSL, Docker, i ręcznie podnosić bazę po każdym zawieszeniu.

---

### 🏆 Tabela Porównawcza: VPS vs. Jaison Serverless (GCP Cloud Run)

| Cecha / Funkcjonalność | Tani VPS (Hostinger / InterServer) | Jaison Serverless (GCP Cloud Run) |
| :--- | :--- | :--- |
| **Koszty w spoczynku (brak ruchu)** | **Płatny stale**. Rachunek rośnie niezależnie od tego, czy ktokolwiek wchodzi na stronę. | **Dokładnie 0 USD (Scale to Zero)**. Płacisz tylko za milisekundy rzeczywistej pracy. |
| **Opłaty za utrzymanie (Ops)** | **Wysokie**. Konieczność zatrudnienia SysOpsa do aktualizacji systemowych i łatania podatności. | **Dokładnie 0 PLN (Zero Ops)**. Google w pełni zarządza infrastrukturą, certyfikatami SSL i bezpieczeństwem. |
| **Wydajność pod piki ruchu** | **Słaba**. Serwer zawiesza się (błąd 502/504 lub OOM) przy nagłym napływie użytkowników. | **Doskonała**. Chmura w ułamku sekundy skaluje się do setek instancji i bezszumnie obsługuje ruch. |
| **Bezpieczeństwo kontenerowe** | **Niskie**. Zhakowanie jednej wtyczki na serwerze daje dostęp do całego systemu plików. | **Maksymalne**. Każdy request obsługuje odizolowany, jednorazowy i niszczony kontener (Sandbox). |
| **Opóźnienie (Latency) w Polsce** | **Wysokie** (USA / słabe trasy routingowe tanich dostawców). | **Minimalne** (Centrum danych GCP Belgia/Niemcy, bezpośrednie wpięcie w sieć Google Edge). |

---

## 🎬 3. Darmowa Automatyzacja & Obróbka Wideo w Chmurze

Analizując najnowsze trendy rynkowe (m.in. materiały od Hasana), zaimplementowaliśmy niskokosztowe mechanizmy automatycznego montażu i obróbki wideo bez obciążania Twojego lokalnego procesora:

1.  **Cloudinary (Natywny darmowy procesor wideo):**
    *   *Jak to działa:* Cloudinary oferuje potężny plan darmowy (25 kredytów miesięcznie, co przekłada się na tysiące operacji na plikach). Pozwala na bezkodowe nakładanie znaków wodnych, automatyczną zmianę proporcji wideo pod Reels/Shorts (smart cropping oparty na śledzeniu twarzy AI), wypalanie napisów oraz łączenie ujęć bezpośrednio przez proste żądanie URL!
2.  **Shotstack API (Cloud Automation):**
    *   *Jak to działa:* Platforma do programistycznego renderowania wideo w chmurze (Shotstack daje 100 minut renderowania wideo miesięcznie w darmowym planie). Idealna do automatycznego montażu: łączenie skryptu audio z darmowymi przebitkami B-roll (Pexels API) na podstawie plików JSON wysyłanych z n8n.
3.  **VidPipe & YouTube Automation Agents (Open Source):**
    *   Nasza architektura wspiera bezszumne, darmowe pipeline'y, które potrafią pobrać jedno surowe nagranie wideo, wygenerować transkrypcję, pociąć je na najciekawsze fragmenty (Highlights) za pomocą AI i automatycznie wypalić napisy w chmurze.

---

## 💎 4. Strategia Lead Magnetów (`11_digital_product`) & Kampanii Marketingowej

W Twoim katalogu `11_digital_product` znajdują się nieskończone, ale niesamowicie wartościowe zasoby. Przekształcimy je w potężne magnesy na leady (Lead Magnets), aby budować zaufanie u klientów B2B:

### 📑 Kluczowe produkty do wdrożenia:
1.  **E-book: „7 kroków do automatyzacji małej firmy”** (`produkt_7_kroków_do_automatyzacji_małej_firmy_.md`)
    *   *Zastosowanie:* Główny lead magnet na stronie agencji. Krótka, ADHD-friendly checklista do pobrania w zamian za e-mail (zapoczątkowuje automatyczny lejek w Systeme.io).
2.  **Case Study: Coolfon** (`case_study_coolfon_jaison.md`)
    *   *Zastosowanie:* Społeczny dowód słuszności (Social Proof) udowadniający, jak automatyzacja n8n i systemy RAG oszczędzają lokalnej firmie GSM dziesiątki godzin pracy tygodniowo. Publikacja na LinkedIn i jako sekcja na landing page'u.
3.  **GCP Cloud Billing Report** (`cfo_billing_optimization_report.md`)
    *   *Zastosowanie:* Magnes dla większych klientów ("High-Ticket" i korporacji), pokazujący jak optymalizować rachunki chmurowe GCP i redukować koszty operacyjne do minimum.

### 🎯 Strategia mikro-reklam (Meta & Google Ads):
*   **Budżet:** Zaledwie **10–20 PLN dziennie** na Meta Ads / Google Ads.
*   **Cel:** Targetowanie lokalnych przedsiębiorców, właścicieli e-commerce i firm usługowych (np. GSM, salony piękności, warsztaty).
*   **Kreacja:** Reklama promująca darmową checklistę: *"Jak odzyskać 15 godzin w tygodniu dzięki darmowym automatyzacjom n8n? Pobierz bezpłatny przewodnik 7 kroków!"*. 
*   **Lejek:** Pobranie checklisty -> Automatyczny e-mail z podziękowaniem -> Zaproszenie na darmową, asynchroniczną kwalifikację i demonstrację systemu Jaison OS.

---

## 👥 5. Profesjonalny Wizerunek LinkedIn dla Tomasza

Wizerunek osobisty (Thought Leadership) to fundament sprzedaży usług High-Ticket. Oto gotowe, precyzyjne prompty dla modeli generatywnych (Midjourney, Flux, Gemini) do stworzenia luksusowych materiałów graficznych:

### 📸 Prompt na Profesjonalny Awatar Biznesowy (Midjourney / Flux):
```text
A premium corporate headshot of a dynamic 30-year-old male entrepreneur with a clean-cut beard, professional modern haircut, subtle, smart, high-ticket styling (dark charcoal tailored blazer over a crisp dark grey t-shirt). High-end editorial studio lighting, soft cinematic rim light, dark moody minimalist background with a subtle blue and green warm neon glow reflecting AI and cloud technology. Real photography, shot on 85mm lens, f/1.8, highly detailed skin texture, professional, trustworthy, and visionary look. --ar 1:1 --stylize 250
```

### 🖼️ Prompt na Zdjęcie w Tle LinkedIn (Meta-Automatyzacja):
```text
Minimalist corporate abstract background banner for a tech company specializing in AI integrations and automation. Clean bento-grid layout with subtle glowing green and blue node-connections representing workflows, APIs, and cloud databases. Elegant, modern glassmorphic card on the left side with thin glowing borders, and extremely crisp, readable, high-contrast, premium sans-serif typography displaying the exact text: "Automatyzuj to, co powtarzalne, twórz to, co unikalne". Visionary, state-of-the-art, premium aesthetic, dark mode, high resolution. --ar 4:1 --style raw
```

---

## 🌳 6. Podręcznik Deweloperski: Git Worktrees

Aby uniknąć blokowania plików w systemie Windows, rozdzieliliśmy Twoją pracę na dwa dedykowane, fizyczne obszary robocze (Worktrees):

*   **Środowisko Główne (Dashboard):** `C:\Aplikacje MVP\01_JAISON_AGENCY_OS`
*   **Środowisko Marketingowe:** `C:\Aplikacje MVP_streamlit` (gałąź `feature/streamlit-dashboard`)
*   **Środowisko Automatyzacji i Chatbotów:** `C:\Aplikacje MVP_chatbots` (gałąź `feature/chatbots-n8n`)

---

## 🤖 7. Gotowe Prompty dla Agentów (Uwzględniające Triggery Kuby)

Zgodnie z mądrością biznesową od Kuby, ludzie kupują wyłącznie 3 rzeczy: **1. Rozwiązania (Solutions), 2. Wygodę (Convenience), 3. Doświadczenia (Experiences)**. Nasze produkty i content must być projektowane wyłącznie w oparciu o te 3 filary!

Uruchom swoich agentów w odpowiednich Worktree, podając im poniższe, chirurgicznie precyzyjne prompty:

### 📢 A. Prompt dla Agenta Marketingowego (Uruchom w `C:\Aplikacje MVP_streamlit`)
```text
Jesteś Dyrektorem ds. Marketingu (CMO AI) w agencji Jaison.pl. Działasz w katalogu roboczym: `C:\Aplikacje MVP_streamlit` (gałąź marketingowa).
Twój cel to przygotowanie kompletnego organicznego lejka sprzedażowego B2B oraz strategii dystrybucji treści na LinkedIn w oparciu o 3 triggery zakupowe Kuby:
1. Rozwiązania (Solutions) — np. Gotowy system n8n ratujący czas.
2. Wygoda (Convenience) — np. Bezobsługowa infrastruktura Serverless (Cloud Run).
3. Doświadczenia (Experiences) — np. Przemiana biznesowa po wdrożeniu Jaison OS.

Zadania do wykonania:
1. Wejdź do katalogu `11_digital_product` i przeanalizuj nieskończony plik: `produkt_7_kroków_do_automatyzacji_małej_firmy_.md`.
2. Zredaguj ten materiał jako luksusowy, gotowy do dystrybucji plik PDF/Markdown (Lead Magnet) o wysokiej wartości merytorycznej.
3. Przeanalizuj plik case study Coolfon (`case_study_coolfon_jaison.md`). Na jego bazie stwórz perswazyjny wpis na LinkedIn pokazujący twarde liczby i oszczędności (Social Proof).
4. Zaproponuj precyzyjną strategię oraz strukturę na mikro-kampanię reklamową za 10-20 PLN dziennie na Meta Ads promującą ten lead magnet.
5. Przygotuj kompletny pakiet dystrybucyjny w pliku markdown zawierający:
   - Przeredagowaną treść Lead Magnetu (7 kroków do automatyzacji)
   - 2 wiralne posty na LinkedIn (jeden oparty na Case Study Coolfon, drugi na "3 triggerach zakupu")
   - Skrypt na wideo rolkę (Reels/Shorts) z mocnym haczykiem (Hook).
```

### ⚡ B. Prompt dla Agenta Automatyzacji & Sprzedaży (Uruchom w `C:\Aplikacje MVP_chatbots`)
```text
Jesteś Dyrektorem Operacyjnym (COO AI) i Architektem n8n w Jaison.pl. Działasz w katalogu roboczym: `C:\Aplikacje MVP_chatbots` (gałąź chatbots).
Twój cel to dopracowanie i przetestowanie pełnego pipeline'u synchronizacji danych (Git Sync) oraz automatyzacji procesów sprzedażowych w oparciu o triggery zakupowe.

Zadania do wykonania:
1. Przeanalizuj pliki konfiguracyjne i webhooki w folderze `integrations/` oraz skrypt `git_sync.log`.
2. Zaimplementuj mechanizm automatycznego przesyłania nowych leadów z Lead Radaru za pomocą webhooka bezpośrednio do systemu n8n.
3. Zaimplementuj i przetestuj automatyczny, odporny na blokady plików Windows skrypt synchronizacyjny Git (git pull --rebase, git push) działający w tle. Skrypt musi zapewniać płynne scalanie zmian deweloperskich między komputerem stacjonarnym a laptopem Tomasza.
4. Wykorzystaj darmowy darmowy tier NVIDIA NIM (`build.nvidia.com` i model Llama 3.1 70B) jako stabilny fallback w komunikacji API, aby omijać limity rate-limitów Google AI Studio podczas masowego researchu.
5. Po zakończeniu testów, przygotuj plik README_INTEGRATION.md z listą aktywnych webhooków oraz instrukcją uruchomienia skryptu Git Sync.
```
