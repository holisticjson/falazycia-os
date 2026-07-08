<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# PROFIL PROJEKTU:

Projekt dotyczy "Jaison" (jaison.pl) - agencji wdrożeniowej systemów AI i automatyzacji biznesowych (B2B). Właścicielem jest Tomasz Duda (Holistic Jason), przedsiębiorca z ADHD. Wszelkie materiały, instrukcje, dashboardy i e-booki muszą być projektowane w duchu "ADHD-friendly" (brak ścian tekstu, silne kotwice wizualne, tabele, punktory, emotikony na start sekcji) oraz perswazyjnego NLP Copywritingu (sensoryka VAK - Visual/Auditory/Kinesthetic/Auditory Digital, presupozycje Miltona, metaprogramy decyzyjne).

INFRASTRUKTURA \& STACK TECHNOLOGICZNY:

1. Środowisko lokalne (PC + Laptop): AntiGravity Agentic (silnik wykonawczy w tle), AntiGravity IDE, CLI, SDK.
2. Warstwa chmurowa: Google Cloud Platform (GCP). Korzystamy z Vertex AI, Google Cloud Storage (GCS) jako bazy danych/RAG, Cloud Build oraz darmowych kredytów chmurowych (\$300 trial + \$1000 GenAI App Builder).
3. Routing LLM: LiteLLM Router (self-hosted proxy kompatybilne z API OpenAI), kierujące zapytania do Vertex AI (modele Gemini 2.0 / 2.5 Flash i Pro).
4. Automatyzacja n8n: Samodzielnie hostowany kontener n8n na serwerze VPS (Debian, reverse proxy Nginx, szyfrowanie SSL Full Strict przez Cloudflare, baza PostgreSQL).
5. Marketing i CRM: Systeme.io (darmowy plan do 2000 kontaktów: 1 tag główny 'holistic-contact', 1 reguła automatyzacji, 1 lejek). Zintegrowany przez API i webhooki z n8n.
6. Integracje z zewnętrznym oprogramowaniem: Composio.dev (jako broker narzędziowy dla agentów).
7. Wirtualny Zarząd (Flota Agentów): Flota 8 wirtualnych dyrektorów (CEO, GHOST, CMO, CCO, CSO, COO, CFO, CTO) w Vertex AI Agent Builder.

POLITYKA 'LOW-COST FIRST':
Nacisk na darmowe rozwiązania open-source, wolne API z darmowymi pakietami startowymi lub lokalnie uruchamiane modele. Unikamy drogich, płatnych subskrypcji bez uprzedniego przetestowania bezkosztowych alternatyw.

Działasz jako światowej klasy Analityk Systemów Agentowych AI i Architekt chmurowy. Na podstawie dostarczonego kontekstu technologiczno-biznesowego projektu Jaison (jaison.pl), przeprowadź dogłębne badanie (Deep Research) w celu znalezienia najlepszych, darmowych i otwartoźródłowych (open-source) zasobów w następujących kategoriach.

WYNIKI MUSZĄ ZAWIERAĆ BEZPOŚREDNIE LINKI DO GITHUB / DOKUMENTACJI.

KATEGORIA 1: Serwery MCP (Model Context Protocol) i Narzędzia
Wyszukaj stabilne i gotowe do wdrożenia serwery MCP (kompatybilne z protokołem MCP od Anthropic/Gemini), które możemy wstrzyknąć do AntiGravity lokalnie:

1. Serwery MCP dla Google Cloud Platform (GCP): Zarządzanie zasobami chmurowymi, Vertex AI, GCS.
2. Serwery MCP dla Github / Git / dokumentacji technicznej: Do indeksowania kodu i automatycznych commitów/pull requestów.
3. Serwery MCP dla n8n / Systeme.io / Google Workspace: Ułatwiające zarządzanie webhookami, mailami i plikami.
4. Specjalistyczny serwer mcp-server-gemini (lub gemini-api-docs-mcp) i zasoby na apidoxmcp.dev.

KATEGORIA 2: Pakiety Skilli (Prompty \& Checklisty) World-Class Copywritingu i Sprzedaży B2B
Znajdź publicznie dostępne repozytoria i pliki ze szczegółowymi promptami systemowymi, checklistami i strukturami opartymi na strategiach autorytetów biznesowych:

1. Alex Hormozi: Modele tworzenia ofert o wysokiej wartości (\$100M Offers), modelowanie lejków sprzedażowych High-Ticket i zbijanie obiekcji (zamykanie B2B).
2. Dan Koe: Wzorce budowania marki osobistej, Thought Leadership, strukturyzowanie newsletterów i jednozdaniowych kotwic uwagi w mediach społecznościowych.
3. Biblioteki wiralnych hooków i skryptów wideo: Sprawdzone wskaźniki zatrzymania uwagi (retention rate) dla rolek, Shorts i TikToków.
4. Psychologiczne NLP w Copywritingu: Wzorce językowe Miltona, dopasowanie sensoryczne VAK i metaprogramy.
*UWAGA: Posiadamy już lokalnie checklisty Mirka Burnejko (Akademia.pl), więc NIE szukaj ich w sieci.*

KATEGORIA 3: Narzędzia do Automatyzacji Wideo i Grafiki (Wiralny Content) - Polityka Low-Cost
Wyszukaj repozytoria, narzędzia CLI lub API z darmowymi pakietami do automatycznego montażu wideo, generowania B-rolli oraz grafik:

1. Integracja Higgsfield AI: Czy istnieją serwery MCP, API lub skrypty integrujące Higgsfield do automatycznego tworzenia i obróbki wideo?
2. Narzędzia do automatycznego montażu B-rolli: Biblioteki w Pythonie (np. rozszerzenia MoviePy) lub darmowe API (np. Pexels, Pixabay) do automatycznego łączenia lektora z przebitkami wideo.
3. Generatory karuzel i postów graficznych: Skrypty/biblioteki (np. Pillow/Canvas w Node.js) generujące gotowe pliki graficzne/PDF z surowego tekstu dostarczonego przez agenta AI.
4. Najlepsze darmowe/tanie API do klonowania głosu i generowania mowy (TTS) – alternatywy dla ElevenLabs.

KATEGORIA 4: Alternatywy Low-Friction dla Dashboardów w Streamlit
Streamlit jest używany do Holistic OS CRM i Kanban. Wyszukaj alternatywne, darmowe, open-source'owe systemy budowy dashboardów (Low-Code / No-Code), które można postawić w kontenerze obok n8n, a które posiadają premium design (ADHD-friendly, nowoczesna estetyka, ciemne motywy):

1. Windmill.dev (alternatywa dla n8n i Streamlit).
2. Retool (darmowe limity) vs open-source: ToolJet, Appsmith, Budibase.
3. Czy lepiej pozostać przy Streamlit, stosując gotowe, animowane komponenty UI (np. React Bits, Tailwind)? Podaj wady i zalety w kontekście ADHD-friendly.

KATEGORIA 5: Alternatywy dla Systeme.io
Porównaj darmowy plan Systeme.io (do 2000 kontaktów, 1 tag) z innymi darmowymi systemami mailingowymi o bogatych limitach (np. Brevo, MailerLite, Mailchimp). Wskaż, które z nich oferuje najmniej tarcia (low friction) przy integracji API/Webhooków z n8n w darmowej wersji.

ZASADY FORMATOWANIA RAPORTU:
Sformatuj odpowiedź w trybie ADHD-friendly:

* Pogrubiaj kluczowe słowa (Visual Anchors).
* Stosuj krótkie micro-akapity i jednoznaczne listy wypunktowane.
* Każdy znaleziony zasób musi mieć link do repozytorium GitHub lub oficjalnej strony.
* Używaj emotikonów na początku głównych sekcji (np. 🚀, 🛠️, 💡, 🎬).

Tak — poniżej masz **praktyczny raport researchowy** pod Twój stack **Jaison / AntiGravity / GCP / n8n**, z naciskiem na **open-source**, **free tier** i **niski friction** wdrożeniowy. Uwzględniam też Twój styl pracy: **ADHD-friendly**, modularność, autonomia agentów i low-cost-first.

## 🚀 Kategoria 1 — MCP

Najmocniejszy kierunek to oparcie AntiGravity o miks: **oficjalne / półoficjalne serwery MCP Google**, serwery do **GitHub / dokumentacji**, oraz praktyczne konektory do **n8n** i **Google Workspace**. Dla Twojego przypadku najważniejsze są źródła, które dają agentowi **aktualny kontekst dokumentacji** i możliwość działania na repo/infrastrukturze bez ręcznego przepisywania instrukcji.[^1][^2][^3]

### **GCP / Gemini / Docs**

- **Gemini Cloud Assist MCP** — repo: [GoogleCloudPlatform/gemini-cloud-assist-mcp](https://github.com/GoogleCloudPlatform/gemini-cloud-assist-mcp); serwer łączy klientów MCP z Gemini Cloud Assist APIs i pozwala rozumieć, zarządzać oraz troubleshootować środowisko Google Cloud z poziomu lokalnego CLI, ale API są oznaczone jako **Private Preview**.[^1]
- **Gemini API Docs MCP** — repo: [philschmid/gemini-api-docs-mcp](https://github.com/philschmid/gemini-api-docs-mcp); serwer wystawia MCP pod endpointem `/mcp`, działa lokalnie, w Dockerze i na Cloud Run, więc świetnie nadaje się jako **live docs backend** dla AntiGravity.[^2]
- **Gemini MCP Server** — repo: [philschmid/gemini-mcp-server](https://github.com/philschmid/gemini-mcp-server); daje dostęp do Gemini API przez MCP i ma gotowe instrukcje deployu na Cloud Run, co dobrze pasuje do Twojego GCP-first stacku.[^4]
- **Gmail MCP Reference** — docs: [developers.google.com/workspace/gmail/api/reference/mcp](https://developers.google.com/workspace/gmail/api/reference/mcp?hl=pl); to ważny sygnał, że Google publikuje już własne referencje MCP dla Workspace, więc warto budować na ich standardzie zamiast wyłącznie na community hackach.[^3]


### **n8n / Git / Workspace**

- **mcp-n8n** — repo: [gomakers-ai/mcp-n8n](https://github.com/gomakers-ai/mcp-n8n); integruje API n8n z klientami MCP i wspiera konfigurację przez `npx`, co jest wygodne dla lokalnego AntiGravity bez ciężkiego setupu.[^5]
- **Google Workspace MCP** — katalog: [mcpservers.org – Google Services MCP Server](https://mcpservers.org/servers/matheusbuniotto/go-google-mcp); serwer obejmuje Drive, Gmail, Calendar, Sheets, Docs, Tasks i People, więc może być jednym z najbardziej użytecznych „hubów narzędziowych” dla Twoich agentów operacyjnych.[^6]
- **Google Calendar MCP** — repo: [nspady/google-calendar-mcp](https://github.com/nspady/google-calendar-mcp); prostszy, węższy serwer do kalendarza, dobry jeśli chcesz ograniczyć zakres uprawnień i chaos konfiguracyjny.[^7]
- **Awesome MCP Servers** — katalog: [mcpservers.org](https://mcpservers.org); dobry punkt startowy do dalszego filtrowania stabilnych serwerów MCP według kategorii i aktywności ekosystemu.[^8]


### **Werdykt wdrożeniowy**

Dla **Jaison** zacząłbym od takiego minimum:

- **`gemini-api-docs-mcp`** jako live docs dla Gemini / Agent Platform[^2]
- **`gemini-mcp-server`** jako warstwa dostępu do Gemini API[^4]
- **`mcp-n8n`** do automatyzacji workflow[^5]
- **`go-google-mcp`** albo osobne MCP dla Gmail/Calendar/Drive, jeśli chcesz mniejsze ryzyko uprawnień[^6][^7]

To da Ci zestaw: **dokumentacja + LLM + workflow + workspace** bez przeskakiwania od razu do zbyt ciężkiej orkiestracji.

## 🛠️ Kategoria 2 — skille copy/sales

Tutaj trzeba rozróżnić dwie rzeczy: **legalnie dostępne repo z promptami/checklistami** oraz **nieautoryzowane „zrzuty system promptów”**, których nie warto robić fundamentem firmowego stacku. Najbezpieczniej bazować na publicznych bibliotekach promptów, własnych skillach AntiGravity i repozytoriach uczących struktury promptów zamiast kopiować cudze zamknięte playbooki.[^9][^10][^11]

### **Najbardziej użyteczne źródła bazowe**

- **Google Antigravity Skills Codelab** — [Authoring Google Antigravity Skills](https://codelabs.developers.google.com/getting-started-with-antigravity-skills); pokazuje, jak konstruować skillsy jako modularne instrukcje z jasnym celem i zakresem użycia.[^9]
- **Google / DEV write-up o AntiGravity Skills** — [My First Experience Creating Antigravity Skills](https://dev.to/googleai/my-first-experience-creating-antigravity-skills-524b); przydatne jako materiał praktyczny do struktury skilli i ich użyteczności w workflow.[^12]
- **Anthropic: Effective context engineering for AI agents** — [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents); bardzo mocna baza do budowy promptów systemowych i skilli z sekcjami typu `<background_information>`, instrukcjami narzędzi i formatem wyjścia.[^11]
- **AWS prompt engineering guide** — [aws.amazon.com](https://aws.amazon.com/blogs/machine-learning/prompt-engineering-techniques-and-best-practices-learn-by-doing-with-anthropics-cl...); użyteczne przez nacisk na **XML tags**, przykłady i wymuszenie formatu odpowiedzi.[^13]


### **Jak to przełożyć na Twoje kategorie**

Zamiast szukać „gotowych repo Alex Hormozi / Dan Koe official prompts”, lepiej zbudować lokalne skille oparte na ich **publicznie znanych frameworkach**, bo to stabilniejsze i bezpieczniejsze prawnie. Dla Jaison polecam utworzyć osobne skille:

- **`b2b-offer-hormozi`** — value equation, offer stack, risk reversal, objection handling.
- **`thought-leadership-dan-koe`** — one-sentence anchor, newsletter arc, authority ladder.
- **`viral-hooks-library`** — hook types, retention beats, scene changes, CTA bridges.
- **`nlp-copy-vak-milton`** — sensory layers, embedded commands, metaprogram framing.


### **Źródła pomocnicze do konstrukcji**

- **LearnWithCheer – AntiGravity skills**: [learnwithcheer.com/blog/agents-skills-in-antigravity](https://learnwithcheer.com/blog/agents-skills-in-antigravity); opisuje, że skille zastępują powtarzanie złożonych instrukcji i kapsułkują workflow oraz preferencje.[^10]
- **Claude XML tags reference**: [aipromptlibrary.app](https://www.aipromptlibrary.app/blog/claude-xml-tags-prompt-engineering); pomocne do budowy czytelnych sekcji promptu i łatwej walidacji.[^14]

W Twoim przypadku warto połączyć to z zasadą **ADHD-friendly copy system**: krótkie bloki, tabele, listy, mocne kotwice wizualne i sensoryczne ramy VAK, bo to jest spójne z Twoją grupą docelową i Twoim własnym sposobem pracy.

## 🎬 Kategoria 3 — wideo, grafika, TTS

Dla polityki **low-cost first** najlepszy setup to **Python + stock APIs + open-source TTS** zamiast zamykania się w drogich SaaS-ach od pierwszego dnia. Kluczowe są tu narzędzia, które zepniesz przez n8n albo CLI i odpalisz lokalnie lub na VPS.[^15]

### **Montaż wideo / B-roll**

- **MoviePy** — repo: [zulko/moviepy](https://github.com/zulko/moviepy); do cięć, konkatenacji, napisów, kompozycji i prostego automatycznego montażu video w Pythonie.[^15]
- **Pexels workflow for AI videos** — [n8n workflow example](https://n8n.io/workflows/10502-create-ai-videos-from-prompts-with-openai-script-tts-and-pexels-b-roll-assembly/); pokazuje praktyczny wzorzec: prompt → skrypt → TTS → B-roll z Pexels → składanie materiału.[^16]
- **Pixabay / Pexels APIs** są sensowną warstwą stockową do przebitek, bo mają darmowe wejście i nadają się do automatycznego pobierania mediów pod temat filmu.[^16]


### **Higgsfield**

W wynikach nie znalazłem wiarygodnego, mocnego open-source repo MCP lub oficjalnego serwera MCP dla **Higgsfield**, więc na dziś traktowałbym tę integrację jako **eksperymentalną** i budował przez zwykłe API/webhook wrappery, jeśli Higgsfield daje oficjalne endpointy. Tu nie ma jeszcze tak mocnego, zaufanego ekosystemu jak przy Gemini docs MCP czy mcp-n8n.[^17][^8]

### **Grafiki / karuzele**

Najpraktyczniejszy kierunek to generatory oparte o:

- **Python + Pillow** do statycznych karuzel i cytatów,
- **Node Canvas** do szablonów social,
- **PDF render** dla e-booków / checklist.
To są raczej wzorce architektoniczne niż jeden kanoniczny repo, ale przewaga jest taka, że idealnie wspierają Twój wymóg **ADHD-friendly**: duże nagłówki, boxy, ikony, krótkie slajdy.


### **TTS / voice cloning**

- **OmniVoice-Studio** — repo: [debpalash/OmniVoice-Studio](https://github.com/debpalash/OmniVoice-Studio); projekt pozycjonuje się jako open-source alternatywa dla ElevenLabs, z voice cloningiem, dubbingiem i desktopowym workflow.[^18]
- **Coqui TTS / Mozilla TTS / Festival / eSpeak / MaryTTS** — jako rodzina narzędzi open-source do TTS są wskazane w przeglądzie ElevenLabs jako popularne open-source opcje integracyjne.[^19]
- **Kokoro TTS** pojawia się jako mocny open-weight kandydat w materiałach społecznościowych, ale w tych wynikach mam tylko źródło pośrednie, więc traktowałbym je jako opcję do testów, nie jako jedyne źródło prawdy.[^20]

Jeśli chcesz **najmniejszy friction**, to na start wybrałbym:

- **MoviePy + Pexels API**
- **OmniVoice-Studio** albo **Coqui TTS**
- prosty generator karuzel Python/Node
To da się spiąć z n8n i Twoją flotą agentów bez szybkiego wpadania w wysokie koszty.[^18][^15][^16]


## 💡 Kategoria 4–5 — dashboardy i mailing

Dla dashboardów obok n8n najczęściej wygrywa rozwiązanie, które ma **ładny interfejs bez dużego narzutu poznawczego**, a dla mailingu wygrywa platforma z **najprostszym API/webhookami** i sensownym free planem. U Ciebie trzeba oceniać nie tylko funkcje, ale też **energię decyzyjną**, bo to realnie wpływa na wdrożenie i utrzymanie.

### **Dashboardy: alternatywy dla Streamlit**

| Narzędzie | Link | Co warto wiedzieć |
| :-- | :-- | :-- |
| **Windmill** | [windmill.dev](https://www.windmill.dev) | Często wskazywany jako alternatywa dla n8n i lekkich dashboardów; dobry, jeśli chcesz bardziej „ops/agentic” feeling niż klasyczny BI [^21]. |
| **ToolJet** | [github.com/ToolJet/ToolJet](https://github.com/ToolJet/ToolJet) | Popularny low-code builder, ale warto uważać na różnice między open-source a pełnym produktem komercyjnym [^22]. |
| **Appsmith** | [github.com/appsmithorg/appsmith](https://github.com/appsmithorg/appsmith) / [pricing](https://www.appsmith.com/pricing) | Dojrzały, ma free plan i self-host, ale znowu trzeba sprawdzać granice funkcji między wersją free a płatną [^23]. |
| **Budibase** | [github.com/Budibase/budibase](https://github.com/Budibase/budibase) | Przyjazny do prostych wewnętrznych aplikacji CRUD i paneli, dobry gdy chcesz szybkie MVP [^22]. |
| **Streamlit** | [streamlit.io](https://streamlit.io) | Nadal sensowny, jeśli dołożysz własny design system i komponenty, ale natywnie bywa mniej „premium” i może wymagać dopieszczania ADHD-friendly UX [^24]. |

### **Czy zostać przy Streamlit?**

**Zostać**, jeśli:

- chcesz **najszybciej** budować prototypy,
- logika jest ważniejsza niż polish UI,
- masz już gotowy CRM/Kanban i zależy Ci na czasie.

**Wyjść w ToolJet/Appsmith/Windmill**, jeśli:

- chcesz mocniej **produktowy wygląd**,
- potrzebujesz mniej kodu frontowego,
- zależy Ci na bardziej „aplikacyjnym” feelingu i lepszej pracy z formularzami / tabelami.[^22][^23]

W kontekście **ADHD-friendly** Streamlit ma plus za prostotę i minus za to, że łatwo kończy się ekranem pełnym bloków bez dobrej hierarchii. Low-code panele często dają lepszy **visual rhythm**, ale mogą dodać więcej złożoności konfiguracyjnej.

### **Alternatywy dla Systeme.io**

- **Systeme.io** — ma darmowy plan do 2000 kontaktów i jest dla Ciebie punktem odniesienia z niskim kosztem wejścia, ale ograniczenia tagów/automatyzacji są wyraźne już na starcie według Twojego opisu [user query].
- **Brevo** — mocny kandydat przy free tier i automatyzacjach; bywa często polecany jako elastyczny wybór do małych firm i integracji.[^21][^25]
- **MailerLite** — zwykle prosty UX i sensowny startowy plan, ale trzeba porównać limity automatyzacji oraz webhooków z aktualnym cennikiem.[^21]
- **Mailchimp** — znany, ale zwykle większy friction i więcej ograniczeń/upsell pressure niż bardziej „lean” alternatywy we free tier.[^21]
- **listmonk** — [listmonk.app](https://listmonk.app); self-hosted, open-source newsletter manager, bardzo mocny jeśli chcesz pełną kontrolę i brak vendor lock-in, ale wymaga własnej obsługi technicznej.[^26]


### **Najmniej tarcia z n8n**

Dla Twojego modelu wygrałbym to tak:

1. **Brevo** — najlepszy balans między gotowym SaaS a integracyjnością.[^25][^21]
2. **Systeme.io** — prosty na start, ale szybciej ograniczy bardziej złożony CRM i segmentację [user query].
3. **listmonk** — najlepszy low-cost/self-host, jeśli chcesz niezależność i możesz utrzymać własny stack.[^26]

Dla **Jaison** praktyczna ścieżka wygląda tak:

- **krótki termin**: Systeme.io albo Brevo,
- **średni termin**: Brevo,
- **docelowa niezależność**: listmonk + n8n + własne formularze/landingi.[^27][^26]

Chcesz, żebym w następnym kroku zrobił z tego **ranking Top 3 per kategoria** z oceną: **koszt / łatwość wdrożenia / zgodność z AntiGravity / ADHD-friendly / ryzyko vendor lock-in**?
<span style="display:none">[^28][^29][^30][^31][^32][^33][^34][^35][^36][^37][^38]</span>

<div align="center">⁂</div>

[^1]: https://github.com/GoogleCloudPlatform/gemini-cloud-assist-mcp

[^2]: https://github.com/philschmid/gemini-api-docs-mcp

[^3]: https://developers.google.com/workspace/gmail/api/reference/mcp?hl=pl

[^4]: https://github.com/philschmid/gemini-mcp-server

[^5]: https://github.com/gomakers-ai/mcp-n8n

[^6]: https://mcpservers.org/servers/matheusbuniotto/go-google-mcp

[^7]: https://github.com/nspady/google-calendar-mcp

[^8]: https://mcpservers.org

[^9]: https://codelabs.developers.google.com/getting-started-with-antigravity-skills

[^10]: https://learnwithcheer.com/blog/agents-skills-in-antigravity

[^11]: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

[^12]: https://dev.to/googleai/my-first-experience-creating-antigravity-skills-524b

[^13]: https://aws.amazon.com/blogs/machine-learning/prompt-engineering-techniques-and-best-practices-learn-by-doing-with-anthropics-claude-3-on-amazon-bedrock/

[^14]: https://www.aipromptlibrary.app/blog/claude-xml-tags-prompt-engineering

[^15]: https://github.com/zulko/moviepy

[^16]: https://n8n.io/workflows/10502-create-ai-videos-from-prompts-with-openai-script-tts-and-pexels-b-roll-assembly/

[^17]: https://uibakery.io/blog/best-mcp-servers

[^18]: https://github.com/debpalash/OmniVoice-Studio

[^19]: https://elevenlabs.io/blog/exploring-open-source-tools-for-integrating-text-to-speech-in-conversational-ai

[^20]: https://www.youtube.com/watch?v=Yk4PLI72sks

[^21]: https://www.sequenzy.com/blog/best-email-tools-with-free-tier

[^22]: https://www.reddit.com/r/selfhosted/comments/1f4mb9b/genuinely_opensource_selfhostable_lowcode/

[^23]: https://www.appsmith.com/pricing

[^24]: https://www.perplexity.ai/search/5fbf613f-5f99-4983-8a97-9e54e7cdb446

[^25]: https://www.brevo.com/blog/best-email-marketing-services/

[^26]: https://listmonk.app

[^27]: https://www.perplexity.ai/search/11396d19-67a0-4ec6-a316-3800794a9dad

[^28]: https://modelcontextprotocol.io/development/roadmap

[^29]: https://www.merge.dev/blog/model-context-protocol-alternatives

[^30]: https://community.n8n.io/t/are-mcp-servers-alternative-to-n8n/138615

[^31]: https://www.mailerlite.com/pl/blog/email-marketing-mcp

[^32]: https://www.youtube.com/watch?v=A2HY8KwU6QQ

[^33]: https://www.youtube.com/watch?v=dN27lRvaSK0

[^34]: https://blog.tooljet.com/appsmith-review/

[^35]: https://github.com/pricing

[^36]: https://www.mcpserverfinder.com/servers/aaronsb/google-workspace-mcp

[^37]: https://gist.github.com/keypressingmonkey/e8d33133752105ad54987c083d71b84a

[^38]: https://www.truefoundry.com/docs/ai-gateway/mcp/google-workspace-mcp-server

