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

