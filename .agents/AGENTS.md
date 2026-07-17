# Jaison — Złote Zasady (Projektowa Biblia)

Te zasady są nienaruszalne dla każdego agenta pracującego w tym obszarze roboczym. Wynikają one z wcześniejszych błędów i halucynacji. Trzymaj się ich bezwzględnie:

1. **Jaison to priorytet:** Projekt `Holistic Broker` jest odłożony na później. Cały wysiłek architektoniczny idzie na konto `hello@jaison.pl` i agencję AI Jaison (jaison.pl).

2. **Infrastruktura Google:** Używamy Vertex AI (Free Trial $300), Google Cloud Storage, Cloud Build. Agenci (Dyrektorzy AI: CEO, CMO, CFO) mają być docelowo osadzeni w **Vertex AI Agent Builder** i wyposażeni w prawdziwe narzędzia do dowożenia kampanii od A do Z.
3. **Lejki i Email Marketing = SYSTEME.IO:** BEZWZGLĘDNY ZAKAZ proponowania budowy własnego systemu mailingowego i lejków od zera! Użytkownik wyraźnie nakazał **używać darmowego planu Systeme.io (do 2000 kontaktów)**, ponieważ rozwiązuje to problem dostarczalności (spam, bany domen). Agenci mają z nim współpracować, a nie go zastępować.
4. **Zero wymyślania koła od nowa:** Tam, gdzie istnieją darmowe narzędzia i MCP (np. Systeme.io do mailingu, gotowe open-source), używamy ich! Własny kod piszemy tylko tam, gdzie to konieczne.
5. **Polityka 'Low Cost First':** Wdrażamy absolutny zakaz włączania płatnych API (takich jak ElevenLabs) na wczesnym etapie. Należy zawsze szukać i wdrażać darmowe alternatywy open-source (np. Coqui TTS / XTTSv2 do klonowania głosu), testować MVP jak najniższym kosztem, a o płatne usługi pytać Tomasza o ostateczną zgodę.
6. **Zasada Proaktywnej Weryfikacji (Zero Zagadek):** Agenci mają NAKAZ sprawdzania obecności kluczy, certyfikatów SSL i poprawności autoryzacji (np. GCS Application Default Credentials) przed wywołaniem błędu. Jeśli wystąpi błąd (np. brak uwierzytelnienia), kategorycznie zabrania się wypluwania surowego, enigmatycznego błędu w Pythonie (np. `SSLError`). Agent ma wyświetlić łopatologiczny, maszynowo sprawny komunikat w UI, dokładnie instruujący użytkownika co musi pobrać lub kliknąć, by rozwiązać problem.
7. **Kompatybilność z Windows PowerShell (Standardy CLI):** Wszystkie komendy konsolowe udostępniane użytkownikowi pracującemu na systemie Windows MUSZĄ być sformatowane jako jedna, ciągła linia (One-Liners), całkowicie wolna od linuxowych znaków kontynuacji linii (ukośniki `\`). Ukośniki `\` powodują krytyczne błędy parsera PowerShell (np. "Missing expression after unary operator").
8. **Bezwzględna weryfikacja zasobów chmurowych przed ich użyciem:** Przed zaproponowaniem poleceń CLI (GCP `gcloud`, Firebase itp.) modyfikujących lub odczytujących infrastrukturę, agent ma bezwzględny obowiązek zweryfikować stan faktyczny zasobów w chmurze (np. sprawdzić, czy rzeczywista nazwa dysku rozruchowego różni się od namiaru maszyny VM), zamiast polegać na założeniach lub zewnętrznych briefach, co mogłoby prowadzić do awarii lub utraty danych.
9. **Dystrybucja produktów cyfrowych (Folder 11_digital_product):** Wszelkie e-booki, poradniki oraz lead magnety stworzone przez agentów w tym workspace (lub w powiązanych folderach, np. Android) muszą trafiać do dedykowanego folderu `C:\Aplikacje MVP\Holistic Jason\11_digital_product\` w celu zachowania scentralizowanej biblioteki produktów. **Kategorycznie nakazuje się** tworzenie tych materiałów z zachowaniem visual anchoringu (ADHD-friendly) oraz technik perswazyjnego NLP Copywritingu (sensoryka VAK, metaprogramy i presupozycje Miltona ze skilli nlp/nlp-copywriting).
10. **Bezwzględne sprzątanie i zakaz duplikacji:** Agenci mają absolutny zakaz duplikowania plików, folderów lub skryptów w obszarze roboczym. Przy każdej reorganizacji lub aktualizacji, stare, niepotrzebne, nieaktualne wersje plików i skryptów (np. stare skrypty wdrożeniowe, kopie zapasowe, pliki tymczasowe) MUSZĄ być natychmiast bezpiecznie usuwane lub przenoszone do `09-archive/`, aby zapobiegać narastaniu chaosu i błędom deweloperskim.

11. **ŹRÓDŁA KANONICZNE — REALITY CHECK FIRST**
Te wytyczne są absolutnie nienaruszalne dla wszystkich dyrektorów technicznych i specjalistów od Gemini i Google Platform. Wbij je sobie na stałe do głowy i nigdy nie używaj niezweryfikowanych wersji modeli, cen ani parametrów technicznych:

### ŹRÓDŁA KANONICZNE — REALITY CHECK FIRST
Przy audytach technicznych, doborze modeli, limitów, kosztów, integracji i roadmapy zawsze używaj tej hierarchii:
1. **Oficjalna dokumentacja producenta** — jedyne źródło prawdy.
2. **Oficjalne repo GitHub producenta** — źródło implementacyjne.
3. **Community repo / blog / forum** — tylko pomocniczo, po weryfikacji.

Nie mieszaj marketingu, postów blogowych ani odpowiedzi innych chatbotów z dokumentacją.

### Google / Gemini / Vertex AI
- https://ai.google.dev/gemini-api/docs
- https://ai.google.dev/gemini-api/docs/models
- https://ai.google.dev/gemini-api/docs/imagen
- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/gemini-api/docs/rate-limits
- https://ai.google.dev/gemini-api/docs/file-search
- https://ai.google.dev/gemini-api/docs/caching
- https://cloud.google.com/vertex-ai/docs
- https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview
- https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions

### fal.ai
- https://fal.ai/docs/documentation
- https://docs.fal.ai/index
- https://fal.ai/docs/documentation/quickstart
- https://fal.ai/models/fal-ai/flux-lora-fast-training
- https://fal.ai/models/fal-ai/flux-lora-portrait-trainer

### Streamlit
- https://docs.streamlit.io/
- https://github.com/streamlit/docs

### n8n
- https://docs.n8n.io/
- https://n8n.io/workflows/
- https://github.com/n8n-io/n8n
- https://github.com/n8n-io/n8n-docs

### Hermes Agentic OS / Nous Research
- https://hermes-agent.nousresearch.com/docs/
- https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
- https://hermes-agent.nousresearch.com/docs/integrations/nous-portal
- https://hermes-agent.nousresearch.com/docs/integrations/providers
- https://portal.nousresearch.com/
- https://github.com/NousResearch/hermes-agent
- https://github.com/NousResearch/hermes-agent/releases

### GITHUB WHITELIST — STAŁE KONTROLOWANE ORGANY
Monitoruj głównie oficjalne orgi i repo twórców:
- GoogleCloudPlatform
- googleapis
- google-gemini
- NousResearch
- n8n-io
- streamlit
- fal-ai

### ZASADA WYBORU REPO
Repo wybieraj według kolejności:
1. oficjalne repo producenta,
2. repo z aktywnymi release’ami,
3. repo z dobrą dokumentacją,
4. repo zgodne ze stackiem J(AI)SON,
5. dopiero potem liczba gwiazdek.
Liczba gwiazdek nie oznacza zgodności technicznej ani aktualności.

### ZASADA AUDYTU TECHNICZNEGO
Jeśli pojawia się claim o modelu, wersji, limicie, koszcie, referencjach, multimodalności lub integracji:
- sprawdź oficjalne docs,
- sprawdź oficjalne repo,
- jeśli brak potwierdzenia, oznacz to jako **niezweryfikowane** albo **potencjalna halucynacja**.

### MAPA STACKU J(AI)SON
Do audytów i rekomendacji priorytetowo traktuj:
- Google Cloud / Vertex AI / Gemini / Imagen
- fal.ai
- Streamlit
- n8n
- Hermes Agentic OS / Nous Portal
- oficjalne repo i docs związane z powyższymi technologiami

12. **LIMITY BUDŻETOWE GCP & LIMITA MODELI (REALITY CHECK)**
Przed planowaniem jakichkolwiek wdrożeń i rekomendacją modeli, każdy agent ma obowiązek zapoznać się ze strukturą środków i kredytów chmurowych, aby zapobiegać błędom autoryzacji oraz błędom 429 (Rate Limits).

### Tabela SKU & Środków (Stan na Lipiec 2026)

| Usługa / obszar | Który credit może pokryć | Co realnie możesz finansować | Czego **nie zakładać** | Link źródłowy |
|---|---|---|---|---|
| Google Cloud ogólnie | **$300 Free Trial** | Kwalifikowane usługi GCP w okresie trial, np. część compute, storage, data, AI zgodnie z programem Free Trial. | Że każda usługa i każdy SKU jest objęty trialem bez wyjątków. | [Free cloud features](https://cloud.google.com/free/docs/free-cloud-features) |
| Cloud Run | **$300 Free Trial**, plus część usage może wpadać w Free Tier. | Hosting lekkich usług, webhooków, API wrapperów, mini backendów pod n8n / Streamlit. | Że skalowanie i quota zwiększysz na koncie trial bez paid billing. | [Google Cloud Free](https://cloud.google.com/free) |
| Cloud Storage (GCS) | **$300 Free Trial**, część usage też może wpadać w Free Tier zależnie od limitów. | Przechowywanie assetów, PDF, plików RAG, backupów, outputów agentów. | Że wszystko będzie darmowe poza trialem — limity Free Tier są zmienne per usługa. | [Free Trial docs](https://cloud.google.com/free/docs/free-cloud-features) |
| BigQuery | **$300 Free Trial**, część usage może mieć free usage. | Logi, analityka, dane leadów, monitoring procesów i wyników agentów. | Że dłuższe trzymanie i skanowanie danych będzie zawsze „za darmo”. | [Free products](https://cloud.google.com/free) |
| Cloud Build | **$300 Free Trial** i ewentualne free usage wg programu. | Buildy, deploymenty, CI/CD dla narzędzi agencyjnych. | Że w trialu podniesiesz dowolnie quota buildów. | [Free cloud features](https://cloud.google.com/free/docs/free-cloud-features) |
| Vertex AI / Gemini na GCP | Zależy od konkretnej ścieżki produktu i billing modelu; część usage może być finansowana z **$300 Free Trial**, ale trzeba patrzeć na konkretną usługę. | Testy modeli, inference, część workloadów na płatnym Vertex billing. | Że **Gemini API w AI Studio** automatycznie bierze środki z trial credits. | [Vertex quotas](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/quotas) |
| Gemini API / AI Studio | **Nie zakładaj**, że pokryje to $1000 App Builder credit. | Osobna ścieżka z własnym billingiem i rate limits. | Że „mam $1300 łącznie, więc wszystko z Gemini API się odliczy”. | [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) |
| Vertex AI Agent Builder / GenAI App Builder / AI Applications | **$1000 GenAI App Builder credit**. | Search apps, chat apps, grounded generation, agent/search style use cases w Agent Builder. | Że to kredyt „na wszystkie modele Google wszędzie”. | [Agent Builder docs](https://docs.cloud.google.com/agent-builder) |
| n8n na GCP | Pośrednio przez **$300 Free Trial**, jeśli hostujesz n8n na Cloud Run / VM / storage / networking. | VPS-like workload w GCP, webhooki, storage, ruch sieciowy, backup. | Że Google finansuje „n8n jako produkt” — finansuje tylko zasoby chmurowe. | [Free Trial docs](https://cloud.google.com/free/docs/free-cloud-features) |

### Limity Modeli i Rate Limits
- **Gemini API**: Limity są restrykcyjnie określane per model (RPM, TPM, RPD). Dla flagowych modeli (np. Gemini 3.5 Flash) limity w planie darmowym mogą wywoływać błędy `429 Resource Exhausted`. Zawsze projektuj odporne systemy obsługujące ponawianie z wykładniczym czasem oczekiwania (Exponential Backoff).
- **Vertex AI / Gemini Enterprise Agent Platform**: Posiada oddzielne limity (quotas) i ograniczenia systemowe na poziomie projektu GCP, niezależne od standardowego API AI Studio.

### Strategiczne Rekomendacje dla J(AI)SON
- **Środki trialowe ($300 GCP)**: Przeznacz wyłącznie na infrastrukturę wspierającą (Cloud Run, GCS, webhooki n8n, bazy danych).
- **Kredyt GenAI App Builder ($1000)**: Rezerwuj wyłącznie na zaawansowane aplikacje RAG, inteligentne wyszukiwanie (Enterprise Search) oraz asystentów z uziemieniem danych (Grounded Chat/Agents).
- **Gemini API (AI Studio)**: Traktuj jako samodzielną ścieżkę operacyjną z osobnym systemem płatności i limitami.
- **Zwiększanie limitów**: Pamiętaj, że na koncie darmowym (Free Trial) Google nie zezwala na podnoszenie limitów (quota increase). W celu skalowania i podnoszenia limitów dla klientów agencji, wymagane jest przejście na płatne konto bilingowe (Paid Billing Account) i złożenie wniosku przez konsolę GCP (Quotas and System Limits).

13. **BEZWZGLĘDNA HUMANIZACJA TEKSTU I ZAKAZ WYCIEKU MARKDOWNU (BEZ GWIAZDEK W HTML)**
Te wytyczne mają na celu eliminację wszelkich śladów ("footprints") generowania treści przez sztuczną inteligencję w serwisach i aplikacjach klienckich:
- **Kategoryczny zakaz używania składni Markdown w plikach HTML**: Żaden agent nie ma prawa wstawiać literalnych gwiazdek podwójnych (`**tekst**`) lub pojedynczych (`*tekst*`), krzyżyków nagłówków (`###`) ani innych znaczników markdown do plików z rozszerzeniem `.html`. Wszystkie wyróżnienia mają być pisane za pomocą standardowych i poprawnych semantycznie tagów HTML, np. `<strong>tekst</strong>`, `<em>tekst</em>`, `<h4>tekst</h4>`.
- **Procedura automatycznego czyszczenia**: Przed zatwierdzeniem zmian w jakimkolwiek pliku HTML, agent ma bezwzględny obowiązek przeskanować plik pod kątem występowania znaków `**` i niezwłocznie zastąpić je znacznikami `<strong>` i `</strong>`.
- **Humanizacja i naturalność języka (NLP)**: Teksty pisane na strony internetowe nie mogą brzmieć szablonowo (AI-ish). Unikamy powtarzalnych zwrotów (np. "W dzisiejszym dynamicznym świecie", "Warto pamiętać", "Kluczowym aspektem"). Stosujemy naturalne, ludzkie przejścia tonalne, zróżnicowaną długość zdań oraz perswazyjne NLP (sensoryka VAK, presupozycje, visual anchoring dla ułatwienia skanowania wzrokiem).

14. **STAŁE KONFIGURACJE E-MAILI I STRATEGIA DOMENOWA JAISON OS**
Wszyscy agenci pracujący w systemie mają obowiązek trzymać się tych stałych namiarów:
- **E-maile systemowe:**
  - **Administracja, RODO, Newslettery:** `info@jaison.pl`
  - **Komunikacja bezpośrednia / Biznesowa / Kontakt:** `hello@jaison.pl`
- **Strategia Domenowa i Landing Page:**
  - **Główna domena `jaison.pl`** jest zarezerwowana na luksusowy, interaktywny frontend (np. Streamlit, chatbot, widgety, integracja z `cal.com`).
  - **Systeme.io (Funnele i Landingi):** Wszystkie strony lądowania, podstrony pobierania lead magnetów, oraz e-booki w Systeme.io mają działać pod dedykowaną subdomeną, np. **`go.jaison.pl`** lub **`leads.jaison.pl`**. Kategorycznie zabrania się podpinania głównej domeny pod Systeme.io, aby nie blokować interaktywnego frontendu i zachować czysty podział na "premium biuro" (`jaison.pl`) i "maszynę generującą ruch" (`go.jaison.pl`).
- **Skille Ads i Ruchu (Media Buyer):**
  - Wszystkie taktyki, SOP-y i checklisty dla kampanii reklamowych Meta Ads, Google Ads i TikTok Ads mają być centralizowane wyłącznie w jednym skillu: **`.agents/skills/media-buyer-ads`**. Agenci mają unikać tworzenia zduplikowanych, rozproszonych plików o reklamach.


15. **INTEGRACJA COMPOSIO.DEV ORAZ STANDARD MODEL CONTEXT PROTOCOL (MCP)**
Wszyscy agenci (w tym Hermes, Antigravity i inni) pracujący nad integracjami społecznościowymi, kalendarzami, pocztą i zewnętrznymi narzędziami SaaS, mają bezwzględny obowiązek stosowania poniższych standardów architektonicznych:
- **Centralny Hub Integracyjny - Composio.dev:** Wszelkie połączenia z platformami społecznościowymi (LinkedIn, Twitter/X, Meta, Instagram), narzędziami komunikacji (Gmail, Google Calendar, Slack) oraz CRM, mają być realizowane wyłącznie za pośrednictwem platformy **Composio.dev** (Composio) jako zaufanego i bezpiecznego mostu OAuth. Zabrania się pisania niestandardowych, rozproszonych integracji API bezpośrednio w kodzie, aby chronić konta przed blokadami (bany anty-spamowe) i centralizować zarządzanie sesjami autoryzacyjnymi.
- **Dostęp przez Model Context Protocol (MCP):** Docelowym standardem dostępu agentów do narzędzi Composio jest protokół **MCP**. Agenty serwerowe (np. Hermes OS działający na GCP VM) mają ładować i dynamicznie odpytywać narzędzia jako natywne serwery MCP, co upraszcza wywoływanie akcji bezpośrednio z pętli LLM i pozwala na pełne, autonomiczne działanie bez niepotrzebnych systemów pośredniczących (middleware).
- **Złoty Podział (n8n vs Hermes MCP):**
  - **n8n** obsługuje eventy zewnętrzne, webhooki i powtarzalne, liniowe potoki automatyzacji (np. automatyczny onboarding po formularzu).
  - **Hermes (via Composio MCP)** obsługuje dynamiczne, decyzyjne pętle aktywne, moderację treści i autonomiczne publikacje social media na żądanie użytkownika.


16. **STANDARD STACKU LOW-FRICTION / LOW-COST, MEMORY LOOP ORAZ WYTYCZNE CASE STUDY NA KONIEC PROJEKTU**

Dla każdego nowo zakładanego projektu (klienckiego lub własnego agencji) obowiązują następujące twarde wytyczne realizacyjne:

### A. Architektura Low-Friction & Low-Cost (Złoty Stack J(AI)SON)
*   **Fundament Chmurowy (Google Cloud Platform):** Maksymalnie wykorzystujemy darmowy program $300 Free Trial oraz $1000 GenAI App Builder credit. Wszystkie asynchroniczne i bazodanowe systemy (webhooki, Cloud Run, GCS, BigQuery) mają dążyć do zerowych kosztów stałych u klienta.
*   **Marketing & Funnele (Systeme.io):** Zawsze wdrażamy darmowy plan Systeme.io pod subdomenami (np. `go.jaison.pl`, `leads.jaison.pl`) do obsługi newsletterów i lead magnetów, nie blokując i nie obciążając głównego frontu aplikacji.
*   **Orkiestracja & Integracje (n8n & Composio):** Korzystamy z n8n (darmowy hosting lub darmowy plan) do liniowych automatyzacji oraz platformy Composio (via MCP) jako centralnego, bezpiecznego huba do autoryzacji społecznościowych i systemów workspace (Slack, Gmail, Calendar).
*   **Premium Frontend:** Budujemy czyste, szybkie, nowoczesne interfejsy w oparciu o Vanilla HTML/CSS/JS (z estetycznym dark-mode, neonowymi gradientami i glassmorphismem) lub Streamlit. Unikamy zbędnych, drogich platform subskrypcyjnych.

### B. Obowiązkowy Memory Loop (Project State File)
Przed rozpoczęciem prac nad jakimkolwiek projektem, agent prowadzący ma **bezwzględny nakaz** utworzenia pliku stanu w katalogu roboczym: `.agents/WORKSPACE_MEMORY.md` lub `WORKSPACE_MEMORY.md`. 
*   Plik ten służy jako żywy dziennik projektu (Zettelkasten), rejestrujący kluczowe kamienie milowe, strukturę techniczną, zmienne środowiskowe (bez wpisywania sekretów wprost!) oraz aktualne TODO.
*   Na starcie każdej kolejnej sesji, agent musi najpierw odczytać ten plik stanu, aby kontynuować pracę z pełnym kontekstem i wykluczyć utratę informacji po restartach środowiska.

### C. Obowiązkowe Case Study na Koniec Projektu (Niszowe i Unikalne)
Każdy projekt realizowany przez J(AI)SON dotyczy innej branży, innej niszy rynkowej oraz opiera się na specyficznych dla klienta wytycznych, integracjach i wzorcach. Dlatego kategorycznie zabrania się stosowania gotowych, generycznych opisów bez głębokiego wgryzienia się w specyfikę projektu.

**Procedura dwuetapowa na koniec prac:**
1.  **Etap 1: Wywiad Diagnostyczny (Niszowe Pytania):** Agent odpowiedzialny za projekt przed przygotowaniem opisu ma obowiązek sformułować zestaw **5 do 8 precyzyjnych, niszowych pytań diagnostycznych** dedykowanych dla danej branży. Pytania te muszą dotyczyć głębi technologicznej, specyficznych rozwiązań (np. asystent nawyków mentalnych, degustacje, unikalne automatyzacje) oraz twardego, mierzalnego ROI.
2.  **Etap 2: Adaptacja Szablonu:** Dopiero po uzyskaniu odpowiedzi (z logów wdrożenia lub bezpośredniego wywiadu z Tomaszem), agent tworzy unikalny opis wdrożenia, trzymając się poniższej struktury:

#### Struktura Case Study J(AI)SON (Framework Perswazyjny):
1.  **Nagłówek Hero (One-sentence hook):** Krótki, magnetyczny hak dostosowany do unikalnego rezultatu (np. *"Jak odzyskaliśmy 20 godzin..."*).
2.  **Demaskowanie Kartelu (Architecture of Trust):** Bezlitosne obnażenie specyficznych patologii, naciągań lub nieskutecznych praktyk tradycyjnej konkurencji w danej branży klienta.
3.  **Problem:** Fizyczne, techniczne i czasowe punkty tarcia specyficzne dla danej niszy rynkowej przed wdrożeniem automatyzacji.
4.  **Sposób (Nasza Technologia):** Łopatologiczne, obrazowe wyjaśnienie zastosowanego stacku (np. suwerenny agent, asystent nawyków itp.).
5.  **Rozwiązanie & Mierzalne ROI:** Twarde dane biznesowe, zaoszczędzony czas, wzrost zaangażowania zespołu oraz koszty utrzymania bliskie zeru.
6.  **Głos Marki (Ghost v2):** Tekst napisany w 100% bezpośrednio ("Ty"), surowym, zaangażowanym tonem z **bezwzględnym nakazem stosowania tagów `<strong>` i `</strong>` do pogrubień** (całkowity zakaz używania składni `**` w plikach HTML).





