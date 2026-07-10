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

- **VoxCPM2** — oficjalna strona: [voxcpm2.org](https://voxcpm2.org/) (kod: OpenBMB); rewolucyjny, open-source model bazowy TTS (2B parametrów) bez tokenizera (tokenizer-free), oferujący studyjną jakość 48kHz audio i natychmiastowe klonowanie głosu (zero-shot voice cloning) z obsługą 30 języków (w tym polskiego). Licencja Apache 2.0 pozwala na pełne uruchomienie lokalnie na GPU bez ponoszenia kosztów subskrypcji.
- **OmniVoice-Studio** — repo: [debpalash/OmniVoice-Studio](https://github.com/debpalash/OmniVoice-Studio); projekt pozycjonuje się jako open-source alternatywa dla ElevenLabs, z voice cloningiem, dubbingiem i desktopowym workflow.[^18]
- **Coqui TTS / Mozilla TTS / Festival / eSpeak / MaryTTS** — jako rodzina narzędzi open-source do TTS są wskazane w przeglądzie ElevenLabs jako popularne open-source opcje integracyjne.[^19]
- **Kokoro TTS** pojawia się jako mocny open-weight kandydat w materiałach społecznościowych, ale w tych wynikach mam tylko źródło pośrednie, więc traktowałbym je jako opcję do testów, nie jako jedyne źródło prawdy.[^20]

Jeśli chcesz **najmniejszy friction** i najwyższą jakość, to na start wybrałbym:

- **MoviePy + Pexels API**
- **VoxCPM2** (do bezkosztowego klonowania głosu o studyjnej jakości) lub **Coqui TTS** (lokalnie)
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


# **Raport Gemini Deep Research

# **Architektura Systemowa i Dokumentacja Wdrożeniowa: Jaison Agentic OS**

Zaprojektowanie autonomicznego, wieloagentowego systemu operacyjnego dla jednoosobowej agencji marketingowej (model Ghost Agency / Digital Maker Studio) wymaga radykalnego odejścia od tradycyjnych architektur oprogramowania. System Jaison Agentic OS, działający w ramach szerszego ekosystemu Holistic AiDHD OS, opiera się na wysoce zoptymalizowanej infrastrukturze chmurowej Google Cloud Platform (GCP) oraz frameworku Nous Research Hermes Agent. Konstrukcja ta realizuje wizję środowiska typu Low-Friction, gdzie złożone procesy poznawcze i operacyjne są delegowane do Wirtualnego Zarządu AI (C-Level Specialist Board). Niniejszy raport stanowi dogłębną analizę architektoniczną, dostarczając precyzyjnych rozwiązań dla problemów współbieżności, separacji danych wielu najemców (multi-tenancy) oraz niskokosztowej automatyzacji potoków multimedialnych.

## **Architektura Nous Hermes Agent i Zamknięta Pętla Umiejętności (Skills Pipeline)**

Framework Hermes Agentic OS różni się od standardowych nakładek na modele językowe (chatbots) wbudowaną, zamkniętą pętlą uczenia (closed learning loop). System ten nie tylko wykorzystuje dostarczone narzędzia, ale samodzielnie tworzy, udoskonala i archiwizuje procedury, znane jako Umiejętności (Skills), na podstawie doświadczeń zebranych w trakcie sesji1. Zrozumienie mechaniki wtyczek (Plugins) i pamięci stanu jest krytyczne dla zachowania ciągłości biznesowej.

### **Oficjalne Wytyczne Tworzenia Wtyczek (Plugins) w Języku Python**

Zgodnie z oficjalną specyfikacją Nous Research, rozszerzanie rdzenia systemu Hermes o niestandardowe narzędzia dla agencji wymaga stworzenia dedykowanych wtyczek w katalogu \~/.hermes/plugins/3. Każda wtyczka jest izolowanym modułem, który rejestruje swoje schematy i funkcje wykonawcze za pomocą obiektu kontekstu (PluginContext), co eliminuje konieczność modyfikacji rdzennego kodu frameworka3.  
Struktura katalogów i plików dla nowej wtyczki zintegrowanej z logiką agencyjną musi ściśle przestrzegać poniższego schematu3:  
\~/.hermes/plugins/agency-core/ ├── plugin.yaml \# Manifest: definiuje metadane, narzędzia, haki (hooks) oraz wymagania środowiskowe ├── **init**.py \# Punkt wejścia: implementuje funkcję register(ctx) ├── schemas.py \# Słowniki JSON Schema definiujące parametry wejściowe dla modelu LLM └── tools.py \# Logika biznesowa w języku Python obsługująca wywołania narzędzi  
Manifest plugin.yaml jest niezbędny, ponieważ procesy wykrywania wtyczek w systemie Hermes używają go do kategoryzacji i bezpiecznego ładowania środowiska5. Wymusza on politykę "fail-closed", blokując inicjalizację, jeśli w środowisku brakuje niezbędnych kluczy API. Z perspektywy dewelopera (AntiGravity), plik ten powinien wyglądać następująco:

YAML  
name: agency-core  
version: 1.0.0  
description: "Zestaw narzędzi orkiestracji dla Jaison Agentic OS."  
kind: general  
author: Tomasz  
provides\_tools:  
  \- generate\_client\_strategy  
provides\_hooks:  
  \- post\_tool\_call  
requires\_env:  
  \- name: SYSTEME\_IO\_API\_KEY  
    description: "Klucz API do integracji z platformą Systeme.io"

Rejestracja narzędzi odbywa się w pliku \_\_init\_\_.py. Funkcja register(ctx) przyjmuje obiekt kontekstu i wiąże słownik schematu z funkcją wykonawczą, definiując jednocześnie przynależność narzędzia do określonego zestawu (toolset)3.

Python  
import json  
from .schemas import STRATEGY\_SCHEMA  
from .tools import handle\_generate\_strategy

def register(ctx):  
    \# Rejestracja natywnego narzędzia dla agentów C-Level  
    ctx.register\_tool(  
        name="generate\_client\_strategy",  
        toolset="agency\_planning",  
        schema=STRATEGY\_SCHEMA,  
        handler=handle\_generate\_strategy,  
        description="Tworzy i zapisuje ustrukturyzowaną strategię klienta."  
    )  
      
    \# Rejestracja haka (hook) nasłuchującego na zdarzenia  
    def on\_tool\_call(tool\_name, params, result):  
        if tool\_name \== "generate\_client\_strategy":  
            print(f"\[AgencyCore\] Zakończono generowanie strategii. Status: {result.get('success')}")  
              
    ctx.register\_hook("post\_tool\_call", on\_tool\_call)

Ładowanie samych Umiejętności (Skills) z katalogu \~/.hermes/skills/ opiera się na wydajnym tokenowo schemacie stopniowego ujawniania (progressive disclosure)8. Na poziomie zerowym agent ładuje jedynie nazwy i opisy umiejętności. Pełny kod pliku SKILL.md (zgodny ze standardem agentskills.io) jest wstrzykiwany do kontekstu dopiero wtedy, gdy model zadecyduje o jego użyciu9. Dzięki temu system unika przeciążenia okna kontekstowego, co jest kluczowe na instancjach o ograniczonych zasobach (GCP e2-micro).

### **Zarządzanie Stanem i Pamięć Wektorowa: Mnemosyne i SQLite WAL**

W architekturze, w której wirtualny zarząd (Streamlit) operuje współbieżnie — na przykład podczas gdy CEO AI aktualizuje strategię, CTO AI pisze kod — tradycyjne zarządzanie pamięcią za pomocą pojedynczych plików MEMORY.md prowadzi do nieodwracalnych konfliktów nadpisywania (race conditions)10. Zintegrowanie wtyczki mnemosyne-plugin radykalnie rozwiązuje ten problem, przenosząc ciężar operacji na lokalną bazę SQLite z zaawansowaną wektoryzacją.  
System Mnemosyne opiera się na architekturze Bilevel Episodic-Associative Memory (BEAM), która całkowicie uniezależnia środowisko od drogich, zewnętrznych baz wektorowych12. Najistotniejszą przewagą tej wtyczki jest kompresja wektorów przy użyciu binarnej przestrzeni (MIB), co pozwala na redukcję 384-wymiarowych osadzeń typu float32 do zaledwie 48 bajtów13. Dzięki temu odległość Hamminga kalkulowana jest bezpośrednio wewnątrz SQLite z sub-milisekundowym czasem reakcji.  
Dla zapewnienia absolutnego bezpieczeństwa współbieżnego zapisu przez wielu agentów bez wywoływania blokad (locks), baza SQLite w Mnemosyne musi zostać przełączona w tryb Write-Ahead Logging (WAL)15. Tryb ten zezwala na równoległy odczyt bazy przez dowolną liczbę instancji asystentów, podczas gdy proces konsolidacji lub agent zapisujący bezpiecznie aktualizuje log transakcyjny. Z technicznego punktu widzenia, wymusza to następującą konfigurację w systemie:

| Warstwa Pamięci Mnemosyne | Charakterystyka Techniczna i Cykl Życia | Cel Operacyjny w Zarządzie AI |
| :---- | :---- | :---- |
| **Working Memory** | Gorąca pamięć podręczna (Hot Context). Zapisywana asynchronicznie z określonym TTL (domyślnie 24h). Odczytywana przy każdym pre\_llm\_call. | Przechowywanie bieżących wniosków z analizy sesji, widocznych natychmiast dla wszystkich agentów. |
| **Episodic Memory** | Długoterminowa baza z wyszukiwaniem hybrydowym FTS5 \+ Wektory. Przenoszenie z Working Memory następuje podczas procesu sleep\_consolidation. | Archiwizacja głębokiej wiedzy o klientach, preferencjach marki i historii zakończonych kampanii. |
| **TripleStore** | Temporalny graf wiedzy oparty o logiczne trójki (podmiot, orzeczenie, obiekt) z kryptograficznymi identyfikatorami SHA-25617. | Eliminacja duplikacji faktów biznesowych i jednoznaczne mapowanie zależności (np. "Tomasz \-\> preferuje \-\> Low-Cost"). |

Aby silnik w pełni przejął kontrolę nad stanem, w głównym pliku config.yaml systemu Hermes należy dokonać aktywacji dostawcy przy jednoczesnym wyłączeniu przestarzałych plików tekstowych, co zapobiega dublowaniu wstrzyknięć do promptu18. Ustawienie parametru auto\_sleep: true gwarantuje, że po każdej zakończonej sesji agenta automatycznie uruchomi się proces konsolidacji wektorowej19.

YAML  
memory:  
  provider: mnemosyne  
  memory\_enabled: false  
  user\_profile\_enabled: false  
  mnemosyne:  
    auto\_sleep: true  
    sleep\_threshold: 20  
    ignore\_patterns:  
      \- "^Traceback \\\\(most recent call last\\\\)"  
      \- "^pip install"

Dzięki temu agenci mogą asynchronicznie komunikować się ze sobą, zapisując ustalenia przy użyciu natywnych wywołań narzędziowych (np. mnemosyne\_remember), a rygorystyczne blokady transakcyjne na poziomie systemu operacyjnego zapobiegają jakimkolwiek wyciekom czy utracie danych17.

## **Przepływ i Podział Danych dla RAG (Multi-Tenancy)**

Działanie środowiska Jaison Agentic OS dla wielu profili klientów w chmurze implikuje konieczność wdrożenia bezpiecznej izolacji najemców (multi-tenancy)20. Biorąc pod uwagę ograniczone zasoby sprzętowe lokalnej instancji wirtualnej oraz dostępność darmowych kredytów w Google Cloud Console, implementacja Retrieval-Augmented Generation (RAG) z wykorzystaniem Vertex AI Search staje się centralnym mechanizmem analitycznym.

### **Strategia Wywołań dla Vertex AI Search**

Decyzja architektoniczna dotycząca tego, czy ładować dane kontekstowe z Google Cloud Storage (GCS) bezpośrednio do promptu systemowego, czy też odpytywać je poprzez narzędzie (Tool Call), musi opierać się na zarządzaniu zużyciem tokenów i zapobieganiu zjawisku "zgubienia w środku" (lost in the middle) charakterystycznemu dla długich okien kontekstowych.  
Najwyższą efektywność osiąga się poprzez **podejście hybrydowe**: Fundamentalne zasady biznesowe (np. żelazne reguły tworzenia ofert "Grand Slam", czy instrukcje stylizacji) powinny być ładowane na sztywno przy starcie sesji, jako część pliku SOUL.md lub AGENTS.md w kontekście systemowym21. Natomiast obszerne archiwa plików z Obsidiana, surowe transkrypcje wywiadów z klientami czy dokumentacja techniczna, muszą być indeksowane przez platformę Google GenAI App Builder. W tym scenariuszu, agent korzysta z wyszukiwarki Vertex AI w sposób celowy, jako narzędzia (Tool Call) wywoływanego w razie braku pewności22.  
Implementacja potoku w Pythonie (integracja z frameworkiem LangChain lub natywnym klientem Discovery Engine) wykorzystuje specjalizowany rodzaj zapytań (Extractive Segments/Answers), który zmusza Google Cloud do zwrócenia zwięzłych, najbardziej trafnych fragmentów, a nie całych dokumentów, co optymalizuje czas odpowiedzi agenta:

Python  
from google.cloud import discoveryengine\_v1 as discoveryengine

def perform\_tenant\_search(query: str, data\_store\_id: str, location: str \= "global") \-\> str:  
    """Narzędzie RAG: przeszukuje indeksy Vertex AI dedykowane konkretnemu profilowi."""  
    client \= discoveryengine.SearchServiceClient()  
    serving\_config \= client.serving\_config\_path(  
        project="holistic-dashboard-dev",  
        location=location,  
        data\_store=data\_store\_id,  
        serving\_config="default\_config"  
    )  
      
    request \= discoveryengine.SearchRequest(  
        serving\_config=serving\_config,  
        query=query,  
        page\_size=5,  
        content\_search\_spec=discoveryengine.SearchRequest.ContentSearchSpec(  
            extractive\_content\_spec=discoveryengine.SearchRequest.ContentSearchSpec.ExtractiveContentSpec(  
                max\_extractive\_answer\_count=3  
            )  
        )  
    )  
    response \= client.search(request)  
    return "\\n\\n".join(\[result.document.derived\_struct\_data.get("extractive\_answers", \[{}\])\[0\].get("content", "") for result in response.results\])

### **Logiczna Organizacja Podziału Zasobów (Data Partitioning)**

W chmurze GCP proces separacji wiedzy dla różnych ról dyrektorskich i klientów realizowany jest za pomocą strukturyzacji samych magazynów danych (Data Stores)20. Płaska konfiguracja prowadzi do halucynacji; dlatego też zasoby na GCS dzielone są na odseparowane silosy, które fizycznie mapują się na odrębne przestrzenie wektorowe.

| Silos GCS / Data Store | Odbiorca C-Level | Typ Danych | Cel Operacyjny |
| :---- | :---- | :---- | :---- |
| gs://holistic\_kubelek/silos-ceo/ | CEO AI, CFO AI | Książki Hormoziego, arkusze kalkulacji CAC/LTV, zasady modeli subskrypcyjnych. | Strategia, inżynieria wartości (Grand Slam), modele wycen (High-Ticket). |
| gs://holistic\_kubelek/silos-cmo/ | CMO AI, CCO AI | Publikacje na temat marketingu dla neuroatypowych, badania nisz, NLP, psychologia zachowań (np. Cialdini). | Analiza lejków sprzedażowych i tworzenie perswazyjnych kampanii. |
| gs://holistic\_kubelek/silos-cto/ | CTO AI (AntiGravity) | Dokumentacje Hermes Agentic OS, API Systeme.io, skrypty integracyjne n8n. | Orkiestracja infrastruktury i kodowanie architektoniczne komponentów. |

Aby zapobiec wyciekowi danych (data bleeding) pomiędzy klientami (np. Agencja Jason vs Nieruchomości), Streamlit zarządza dynamicznym wskaźnikiem kontekstu na poziomie sesji. Kiedy użytkownik dokonuje zmiany profilu, aplikacja Streamlit aktualizuje słownik st.session\_state.active\_profile. Ten stan natychmiast rekonfiguruje zmienne środowiskowe, takie jak HERMES\_HOME, nakazując demonowi Hermes przełączenie przestrzeni roboczej katalogu plugins/mnemosyne/data/ oraz nadpisując wtyczkę wyszukiwania, by wskazywała na prawidłowy data\_store\_id profilu w środowisku chmurowym. Taka izolacja wymusza twarde, kryptograficzne ramy bezpieczeństwa, w których agent dla jednego profilu fizycznie nie posiada tokenów uwierzytelniających by odczytać buckety innej firmy.

## **Kreator Profili Klienta (Onboarding Wizard)**

Zbudowanie oferty o wysokiej marży (High-Ticket) wymaga precyzyjnego mapowania potrzeb klienta na strukturę inżynierii ofert. Onboarding Wizard, zastępując tradycyjne, manualne tworzenie plików konfiguracyjnych, wykorzystuje formularz diagnostyczny, którego odpowiedzi ulegają syntezie przez model językowy20.

### **Schemat Techniczny client\_context.json**

Podstawą algorytmicznego działania agentów CMO i CEO jest ustrukturyzowany plik JSON generowany po zakończeniu sesji diagnostycznej. Aby spełnić założenia metodyki "Grand Slam Offer" Alexa Hormoziego, plik ten musi implementować tzw. równanie wartości (Value Equation): ![][image1]. Dodatkowo musi ewaluować leada pod kątem paradygmatów kwalifikacji sprzedażowej (BANT lub wariacja S-C-A-R).  
Wymagana struktura wyjściowa, zoptymalizowana do parsowania przez Hermes OS, prezentuje się następująco:

JSON  
{  
  "client\_metadata": {  
    "tenant\_id": "profile\_b2b\_tech",  
    "industry": "Oprogramowanie B2B",  
    "qualification\_score": {  
      "budget\_tier": "High-Ticket (\>20,000 PLN)",  
      "authority": "CEO / Właściciel",  
      "pain\_point\_severity": "Krytyczna",  
      "timing": "Natychmiastowa gotowość"  
    }  
  },  
  "hormozi\_value\_equation": {  
    "dream\_outcome": "Wyeliminowanie 80% pracy manualnej przy jednoczesnym podwojeniu retencji klientów.",  
    "perceived\_likelihood": "Implementacja w pełni audytowalnych logów i asynchronicznych agentów AI.",  
    "time\_delay\_reduction": "Wdrożenie operacyjnego MVP w ciągu 14 dni roboczych.",  
    "effort\_and\_sacrifice\_minimization": "Brak konieczności uczenia się kodowania przez zespół klienta (Done-For-You)."  
  },  
  "grand\_slam\_mechanics": {  
    "guarantee\_structure": "Model warunkowy (Performance-based) \- płatność za dostarczony zysk operacyjny.",  
    "bonus\_stack": \[  
      "Standardy operacyjne (SOP) dla zespołu",  
      "Gotowe skrypty automatyzacji n8n"  
    \],  
    "scarcity": "Wdrożenie ograniczone do 2 klientów miesięcznie"  
  },  
  "brand\_voice": "Zwięzły, ADHD-friendly, pozbawiony korporacyjnego żargonu, stawiający na mierzalne ROI."  
}

### **Dynamiczna Przebudowa Instrukcji w Streamlit**

Zapisanie wyżej wymienionego dokumentu JSON uruchamia potok aktualizacyjny w interfejsie Streamlit. Kluczowym wyzwaniem UX jest to, aby po załadowaniu profilu dyrektorzy (modele językowe) natychmiast przyjęli nową tożsamość bez widocznych opóźnień lub restartów w tle. Implementacja opiera się na modyfikacji zasobu st.session\_state przy użyciu wbudowanych mechanizmów zdarzeń (on\_change).

Python  
import streamlit as st  
import json  
import os

def build\_system\_prompt(role: str, context: dict) \-\> str:  
    """Konstruuje dynamiczny prompt systemowy na bazie struktury Hormoziego."""  
    outcome \= context\['hormozi\_value\_equation'\]\['dream\_outcome'\]  
    brand\_voice \= context\['brand\_voice'\]  
      
    base\_prompt \= f"Pełnisz rolę {role} w wirtualnym zarządzie Jaison OS. "  
    base\_prompt \+= f"Twój aktualny cel to zaoferowanie klientowi wartości: '{outcome}'. "  
    base\_prompt \+= f"Styl komunikacji musi być ściśle: {brand\_voice}. "  
      
    if role \== "CEO AI":  
        base\_prompt \+= f"Skup się na mechanice gwarancji: {context\['grand\_slam\_mechanics'\]\['guarantee\_structure'\]} "  
        base\_prompt \+= "Zaprojektuj nieodpartą ofertę redukującą tarcia percepcyjne."  
          
    return base\_prompt

def handle\_profile\_change():  
    """Callback wywoływany przez selektor profilu; aktualizuje instrukcje bez przerywania sesji."""  
    selected\_profile \= st.session\_state.profile\_dropdown  
    file\_path \= f"/opt/data/profiles/{selected\_profile}\_context.json"  
      
    if os.path.exists(file\_path):  
        with open(file\_path, "r", encoding="utf-8") as f:  
            client\_context \= json.load(f)  
              
        st.session\_state.client\_context \= client\_context  
        \# Dynamiczna aktualizacja instrukcji dla C-Level  
        st.session\_state.ceo\_prompt \= build\_system\_prompt("CEO AI", client\_context)  
        st.session\_state.cmo\_prompt \= build\_system\_prompt("CMO AI", client\_context)  
          
        \# Wywołanie interfejsu API Hermesa do rekonfiguracji pamięci roboczej w tle  
        \# np. wymuszenie przeładowania pliku SOUL.md dla instancji

Takie podejście umożliwia błyskawiczne przejście od diagnostyki do pracy kreatywnej — w ułamku sekundy CMO AI otrzymuje precyzyjny kontekst i może rozpocząć proces generowania wysoce konwertującego tekstu (copywritingu) na stronę lądowania (landing page).

## **Automatyzacja Multimediów i Tworzenia Treści (Polityka Low-Cost)**

Prowadzenie agencji zautomatyzowanej (Faceless Channels) wymaga potężnego, lecz skrajnie oszczędnego strumienia roboczego (pipeline) dla multimediów20. Obniżenie kosztów osiąga się przez całkowite wyeliminowanie rozwiązań chmurowych płatnych za minutę renderowania na rzecz narzędzi programistycznych i integracji API.

### **Integracja Higgsfield AI via Webhooks**

Platforma Higgsfield AI stanowi potężne narzędzie do generowania wysokiej jakości ujęć kinematograficznych i animowania obrazów26. Asynchroniczny charakter generowania wideo wymaga podejścia bazującego na zdarzeniach (event-driven). Oczekiwanie na renderowanie w pętli zablokowałoby wątek wykonawczy agenta Hermesa.  
Zastosowanie serwera MCP (Model Context Protocol) łączy wirtualny zarząd z Higgsfield. Użytkownik przekazuje do API Higgsfield parametry wideo (np. task: text-to-video) oraz specjalny nagłówek wywołania zwrotnego X-Webhook-URL, ustawiając tryb działania na terminalny (X-Webhook-Mode: terminal), który gwarantuje dostarczenie pojedynczego żądania HTTP POST z powiadomieniem po ostatecznym zakończeniu procesu renderowania28. Gdy proces się zakończy, lekki serwer Nginx/FastAPI postawiony na instancji GCP odbiera webhook, ściąga wygenerowany zasobnik MP4 do lokalnego systemu plików i wyzwala asynchroniczne powiadomienie do CTO AI o pomyślnym wykonaniu zadania, całkowicie uwalniając zasoby procesora na czas trwania renderowania.

### **Oszczędnościowy Potok dla Wideo Pionowego (Shorts/Reels)**

Dla masowej produkcji wideo typu Shorts, dedykowany potok integruje pobieranie darmowych przebitek wideo, generowanie głosu na lokalnych zasobach sprzętowych oraz programowy montaż.

1. **Darmowe B-Roll z Pexels API:** Wykorzystanie darmowego API Pexels do wyszukiwania materiałów stockowych drastycznie redukuje koszty29. Skrypt w języku Python filtruje wyniki pod kątem orientacji pionowej, idealnej do social mediów:  
   Python  
   import requests

   def fetch\_pexels\_broll(query: str, api\_key: str) \-\> str:  
       url \= f"https://api.pexels.com/videos/search?query={query}\&orientation=portrait\&size=medium\&per\_page=1"  
       headers \= {"Authorization": api\_key}  
       response \= requests.get(url, headers=headers)  
       \# Zwraca najwyższej jakości link MP4 z wyników  
       video\_files \= response.json()\['videos'\]\[0\]\['video\_files'\]  
       hd\_link \= next((f\['link'\] for f in video\_files if f\['quality'\] \== 'hd'), video\_files\[0\]\['link'\])  
       return hd\_link

2. **Lokalny Syntezator Mowy (Coqui XTTSv2):** Aby ominąć wysokie stawki API (np. ElevenLabs), zastosowano wielojęzyczny, udostępniony na otwartej licencji model XTTSv2, operujący bezpośrednio z instancji lokalnej lub dedykowanego środowiska. Model potrafi sklonować unikalny głos (np. Tomasza) na podstawie pojedynczej próbki referencyjnej trwającej od 6 do 20 sekund31. Dla zapewnienia błyskawicznego przetwarzania konieczna jest optymalizacja polegająca na jednorazowym zakodowaniu warunków referencyjnych (speaker embeddings), oszczędzając około 1,2 sekundy czasu operacyjnego na każdej fazie renderowania32:  
   Python  
   from TTS.api import TTS  
   import torch

   device \= "cuda" if torch.cuda.is\_available() else "cpu"  
   tts \= TTS("tts\_models/multilingual/multi-dataset/xtts\_v2").to(device)

   \# Prekalkulacja parametrów gpt\_cond i speaker\_emb dla szybkości  
   gpt\_cond, speaker\_emb \= tts.synthesizer.tts\_model.get\_conditioning\_latents(audio\_path=\["tomasz\_reference.wav"\])

   def generate\_voiceover(text: str, output\_path: str):  
       \# Generowanie dźwięku bez wymogu ponownego ładowania wzorca głosu  
       chunks \= tts.synthesizer.tts\_model.inference\_stream(  
           text, "pl", gpt\_cond, speaker\_emb, stream\_chunk\_size=20  
       )  
       \# (Zapis strumienia chunks do pliku .wav)

3. **Automatyczny Montaż z MoviePy:** Biblioteka MoviePy realizuje bezstratne łączenie warstwy audio z obrazem. Poważnym wyzwaniem jest obsługa orientacji wideo — nawet materiały oznaczone jako pionowe mogą posiadać niewłaściwy współczynnik kształtu dla formatu Instagram Reels (1080x1920). Narzędzie dynamicznie sprawdza proporcje; jeśli obraz nie pasuje, najpierw skaluje wysokość na sztywno do 1920 pikseli, a następnie wycina precyzyjnie 1080 pikseli od środka obwiedni obrazu (crop), gwarantując brak zniekształceń i czarnych pasów na brzegach33.  
   Python  
   from moviepy.editor import VideoFileClip, AudioFileClip

   def assemble\_vertical\_reel(video\_path: str, audio\_path: str, output\_path: str):  
       clip \= VideoFileClip(video\_path)  
       audio \= AudioFileClip(audio\_path)

       \# Formatowanie stricte wertykalne (9:16) \- Crop ze środka  
       clip\_resized \= clip.resize(height=1920)  
       clip\_cropped \= clip\_resized.crop(  
           x\_center=clip\_resized.w/2,   
           y\_center=clip\_resized.h/2,   
           width=1080,   
           height=1920  
       )

       final\_video \= clip\_cropped.set\_audio(audio).set\_duration(audio.duration)  
       \# Użycie wydajnych kodeków do webu  
       final\_video.write\_videofile(output\_path, fps=30, codec="libx264", audio\_codec="aac", preset="medium")

### **Zautomatyzowane Generowanie Karuzel z Pillow**

Tworzenie angażujących karuzel edukacyjnych na LinkedIn lub Instagram realizowane jest poprzez parsowanie wniosków z dokumentów PDF do plików obrazów. Pythonowa biblioteka Pillow wymaga stworzenia autorskiej funkcji zawijania tekstu, ponieważ jej metody natywnie nie rozwiązują problemu łamania wyrazów w obrębie danego pola35. Istotnym elementem jest odejście od metody getsize() (wycofanej z racji błędów wyliczania marginesów) na rzecz aktywnego wykorzystania textlength() lub wyznaczania wysokości poprzez pętlę sprawdzającą36.

Python  
from PIL import Image, ImageDraw, ImageFont

def create\_carousel\_slide(text\_content: str, output\_path: str):  
    bg\_color \= (15, 23, 42) \# Ciemny, elegancki granat  
    img \= Image.new('RGB', (1080, 1080), color=bg\_color)  
    draw \= ImageDraw.Draw(img)  
      
    try:  
        font \= ImageFont.truetype("Montserrat-Bold.ttf", size=55)  
    except IOError:  
        font \= ImageFont.load\_default()  
          
    max\_width \= 880  
    x\_offset, y\_offset \= 100, 200  
      
    words \= text\_content.split()  
    current\_line \= \[\]  
      
    \# Implementacja logicznego zawijania wierszy  
    for word in words:  
        test\_line \= ' '.join(current\_line \+ \[word\])  
        \# textlength pozwala na poprawne obliczenie szerokości tekstu  
        if draw.textlength(test\_line, font=font) \<= max\_width:  
            current\_line.append(word)  
        else:  
            \# Wypisz obecną linię i przesuń oś Y w dół  
            draw.text((x\_offset, y\_offset), ' '.join(current\_line), font=font, fill=(255, 255, 255))  
            y\_offset \+= 85 \# Interlinia  
            current\_line \= \[word\]  
              
    \# Narysowanie ostatniego wiersza bufora  
    if current\_line:  
        draw.text((x\_offset, y\_offset), ' '.join(current\_line), font=font, fill=(255, 255, 255))  
          
    img.save(output\_path)

Tak opracowany kod działa asynchronicznie, generując dziesiątki slajdów graficznych z przetworzonych przez LLM bloków tekstowych w ciągu kilku sekund i wystawiając je jako załączniki lub przekazując do zewnętrznych systemów publikujących (np. n8n).

## **Ghostwriter i Rygorystyczny Filtr Stylu (GHOST V2)**

Moduł filtrujący (Ghost Operator) odgrywa krytyczną rolę w konwersji surowych struktur analitycznych generowanych przez CMO na autentyczny i dynamiczny język człowieka, co bezpośrednio determinuje skuteczność lejków sprzedażowych. Niestety, niemal wszystkie komercyjne modele językowe cierpią na zjawisko wtórnej sztuczności (używanie tzw. "AI-isms"), które momentalnie osłabiają konwersję i zmniejszają zaufanie20.  
Aby zminimalizować paraliż percepcyjny oraz zaspokoić potrzeby odbiorców z neuroatypowością (ADHD), przekaz musi unikać skomplikowanej składni, blokowych akapitów oraz generycznych podsumowań.  
**Wymagany szablon precyzyjnego promptu systemowego dla GHOST V2:**  
Jesteś elitarnym filtrem komunikacyjnym (GHOST V2), cyfrowym ghostwriterem dla Tomasza – praktyka biznesu, eksperta od automatyzacji B2B i High-Ticket.  
TWOJA MISJA: Przekształć każdy dostarczony surowy tekst w dynamiczną, niezwykle precyzyjną, mówioną treść, pozbawioną jakiegokolwiek cienia sztuczności. Tekst ma być zorientowany na neuroatypowych odbiorców (ADHD-friendly): bezlitośnie przykuwający uwagę, krótki, z silną bodźcowością.  
ŻELAZNE ZASADY, KTÓRYCH ZŁAMANIE OZNACZA PORAŻKĘ:

1. ABSOLUTNY ZAKAZ AI-ISMS (Słowa zakazane): Nigdy nie używaj zwrotów takich jak: "kluczowy", "warto pamiętać", "podsumowując", "rewolucyjny", "w dzisiejszym dynamicznym środowisku", "niezwykle ważne", "zanurzmy się w", "zrozumienie tego jest istotne", "zagłębmy się", "zaczynamy". Słowa te natychmiastowo niszczą wiarygodność.  
2. OPTYMALIZACJA DOPAMINOWA (ADHD-Friendly):  
   * Konstruuj krótkie, asertywne zdania (maksymalnie kilkanaście słów).  
   * Akapity mogą składać się najwyżej z dwóch lub trzech krótkich zdań. Przejrzyste światło między tekstem jest konieczne.  
   * Jeśli to konieczne, stosuj pogrubienia na najważniejszych uderzeniach punktowych (ROI, liczby, stawki LTV/CAC), ale unikaj nadużywania list wypunktowanych, jeśli mogą zostać opowiedziane jednym mocnym zdaniem.  
3. PERSPEKTYWA I TON:  
   * Jesteś brutalnie praktycznym inżynierem biznesu, nie akademikiem. Nie obiecujesz złotych gór — dowodzisz wartości faktami.  
   * Pisz w pierwszej osobie z nutą luzu, asertywności, oraz bezwzględnego skupienia na wynikach.  
4. MECHANIKA KOŃCÓWKI:  
   * Zero dydaktycznych, ciepłych konkluzji na końcu. Koniec tekstu musi uciąć dyskusję stanowczym wezwaniem do akcji (Call to Action), wciągnąć w pętlę logiczną lub pozostawić odbiorcę z mocną myślą (np. "Wybór należy do Ciebie.").

WEJŚCIOWY MATERIAŁ DO PRZETWORZENIA: \[Wklej tekst tutaj\]  
Wyposażony w taki mechanizm i odpalony na modelach o wyjątkowych zdolnościach rozumienia instrukcji (np. Claude 3.5 Sonnet / DeepSeek V4 poprzez OpenRouter), agent staje się niemal niemożliwy do odróżnienia od zawodowego copywritera.

## **Wytyczne Bezpieczeństwa dla Dewelopera (AntiGravity)**

Lokalny system agentowego programowania, AntiGravity, jest autonomicznym środowiskiem wykonującym potężne modyfikacje w architekturze20. Aby uchronić jednosobową agencję przed ryzykiem wprowadzenia drogich i skomplikowanych bibliotek do struktury, które ubiją maszynę e2-micro GCP, agent ten musi operować w ciasno zarysowanych ramach ("Guardrails").  
Ramy te są ładowane przy każdej sesji poprzez utworzenie dedykowanego pliku markdown, np. /.agents/rules/antigravity\_guardrails.md, dzięki czemu AntiGravity samoczynnie absorbuje tę politykę jako fundament własnych decyzji inżynieryjnych20.  
**Specyfikacja reguł konfiguracyjnych dla AntiGravity:**

# **ZASADY FUNDAMENTALNE OPERACJI (Guardrails dla AntiGravity)**

Jesteś elitarnym Architektem i DevOps Systemów Jaison Agentic OS. Przed przystąpieniem do pisania jakiegokolwiek kodu, musisz zaabsorbować i stosować się do poniższych, niewzruszalnych praw operacyjnych.

1. **POLITYKA LOW-COST FIRST I OCHRONA ZASOBÓW:**  
   * Ograniczenia środowiska: Nasz węzeł operacyjny w Google Cloud to e2-micro (1 GB RAM \+ 2 GB Swap). Uruchamiasz się w systemie w trybie absolutnego oszczędzania pamięci.  
   * Bezwzględny zakaz proponowania lub instalacji komercyjnych/chmurowych baz wektorowych typu Pinecone, Qdrant czy ChromaDB. Jako wektorową pamięć i system RAG stosujesz wyłącznie wtyczki oparte na SQLite (np. Mnemosyne) lub korzystasz z API Vertex AI.  
   * Eliminuj nadmierne biblioteki (bloatware) w potokach Python i preferuj rozwiązania natywne.  
2. **ZARZĄDZANIE KONFIGURACJAMI HERMES OS:**  
   * Wszelkie tworzone wtyczki (Plugins) dla środowiska Hermes muszą rygorystycznie utrzymywać strukturę plików (plugin.yaml, schemas.py) i wykorzystywać rejestrację ctx.register\_tool().  
   * Zanim stworzysz lub zmodyfikujesz zasób wiedzy, jesteś zobowiązany użyć narzędzia systemu plików (mcp-filesystem) do odczytania struktury indeksowej umieszczonej pod adresem /opt/holistic\_os/knowledge\_base/000\_MASTER\_INDEX.md. Nigdy nie zgaduj ścieżek.  
3. **DIAGNOSTYKA LOKALNA I ZERO ZAPĘTLEŃ (Błędy 502/404):**  
   * Nigdy nie modyfikuj binarnych czy systemowych plików źródłowych innych środowisk, by na siłę "zapatchować" błędy w swoim kodzie.  
   * W przypadku wystąpienia błędów z bramkami lub portami w sieci Windows/WSL, zanim napiszesz poprawkę, MUSISZ przeanalizować surowe logi oraz przetestować połączenia (np. curl, polecenia sieciowe) aby wykluczyć pomyłkę konfiguracyjną (np. zajęty port 4000).  
4. **SEPARACJA ŚRODOWISK (Zero Hardcoding):**  
   * Rygorystyczny zakaz twardego kodowania (hardcoding) kluczy API, ścieżek, certyfikatów uwierzytelniających i sekretów w plikach z logiką .py czy manifestach.  
   * Dostęp do zmiennych konfiguracyjnych odbywa się wyłącznie poprzez moduł środowiskowy w pliku .env (odczyt za pomocą os.environ.get()). W manifestach stosuj requires\_env.

Wdrożenie powyższych wytycznych skutecznie blokuje "nadgorliwość" asystenta kodu, powstrzymując próby nieodwracalnego uszkodzenia środowiska operacyjnego i zachowując smukłość oprogramowania zgodną z polityką niskiego zużycia zasobów. Implementacja opisanych mechanizmów — od wtyczek Mnemosyne po skrypty MoviePy i Pillow — transformuje teoretyczny zamysł jednoosobowej Ghost Agencji w potężną, rentowną rzeczywistość działającą autonomicznie bez ciągłego manualnego nadzoru, co było pierwotnym zamysłem systemu Jaison Agentic OS.

#### **Cytowane prace**

1. Hermes Agent: Self-Hosted AI That Never Forgets You (2026) \- AI Builder Club, [https://www.aibuilderclub.com/blog/hermes-nous-research-self-improving-agent](https://www.aibuilderclub.com/blog/hermes-nous-research-self-improving-agent)  
2. Hermes Agent \- Hermes Agent, [https://nousresearch-hermes-agent.mintlify.app/introduction](https://nousresearch-hermes-agent.mintlify.app/introduction)  
3. Plugins | Hermes Agent \- nous research, [https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)  
4. OpenCode integration plugin for Hermes Agent — dispatch coding tasks to OMO's multi-agent harness \- GitHub, [https://github.com/zaycruz/hermes-opencode-plugin](https://github.com/zaycruz/hermes-opencode-plugin)  
5. Build a Hermes Plugin, [https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin](https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin)  
6. Model Provider Plugins \- Hermes Agent, [https://hermes-agent.nousresearch.com/docs/developer-guide/model-provider-plugin](https://hermes-agent.nousresearch.com/docs/developer-guide/model-provider-plugin)  
7. hermes-agent/hermes\_cli/plugins.py at main \- GitHub, [https://github.com/NousResearch/hermes-agent/blob/main/hermes\_cli/plugins.py](https://github.com/NousResearch/hermes-agent/blob/main/hermes_cli/plugins.py)  
8. Hermes Agent: Self-Improving AI | Build This Now \- BuildThisNow, [https://www.buildthisnow.com/blog/guide/agents/hermes-agent](https://www.buildthisnow.com/blog/guide/agents/hermes-agent)  
9. Hermes Agent — Open-Source AI Agent with Persistent Memory, [https://hermes-agent.org/](https://hermes-agent.org/)  
10. The Hermes Agent Memory Guidebook, [https://hermesatlas.com/guide/memory/](https://hermesatlas.com/guide/memory/)  
11. Persistent Memory | Hermes Agent \- nous research, [https://hermes-agent.nousresearch.com/docs/user-guide/features/memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)  
12. Proposal: Add Mnemosyne to official memory provider documentation · Issue \#34271 · NousResearch/hermes-agent \- GitHub, [https://github.com/NousResearch/hermes-agent/issues/34271](https://github.com/NousResearch/hermes-agent/issues/34271)  
13. mnemosyne-memory \- PyPI, [https://pypi.org/project/mnemosyne-memory/](https://pypi.org/project/mnemosyne-memory/)  
14. GitHub \- mnemosyne-oss/mnemosyne: The Zero-Dependency, Sub-Millisecond AI Memory System for Hermes Agents and Everyone Else\!, [https://github.com/mnemosyne-oss/mnemosyne](https://github.com/mnemosyne-oss/mnemosyne)  
15. \[IMPROVEMENT\] Mnemosyne SQLite DB may not be in WAL mode under concurrent access · Issue \#20351 · NousResearch/hermes-agent \- GitHub, [https://github.com/NousResearch/hermes-agent/issues/20351](https://github.com/NousResearch/hermes-agent/issues/20351)  
16. github.com/aj-nt/mnemosyne v0.1.0 on Go \- Libraries.io \- security, [https://libraries.io/go/github.com%2Faj-nt%2Fmnemosyne](https://libraries.io/go/github.com%2Faj-nt%2Fmnemosyne)  
17. Memory Providers: I tested them all : r/hermesagent \- Reddit, [https://www.reddit.com/r/hermesagent/comments/1tms3g6/memory\_providers\_i\_tested\_them\_all/](https://www.reddit.com/r/hermesagent/comments/1tms3g6/memory_providers_i_tested_them_all/)  
18. mnemosyne/docs/hermes-integration.md at main \- GitHub, [https://github.com/mnemosyne-oss/mnemosyne/blob/main/docs/hermes-integration.md](https://github.com/mnemosyne-oss/mnemosyne/blob/main/docs/hermes-integration.md)  
19. mnemosyne/docs/configuration.md at main \- GitHub, [https://github.com/AxDSan/mnemosyne/blob/main/docs/configuration.md](https://github.com/AxDSan/mnemosyne/blob/main/docs/configuration.md)  
20. Holistic A(I)DHD Architect System, uploaded:Holistic A(I)DHD Architect System  
21. Tips & Best Practices | Hermes Agent, [https://hermes-agent.nousresearch.com/docs/guides/tips](https://hermes-agent.nousresearch.com/docs/guides/tips)  
22. Get search results | Agent Search \- Google Cloud Documentation, [https://docs.cloud.google.com/generative-ai-app-builder/docs/preview-search-results](https://docs.cloud.google.com/generative-ai-app-builder/docs/preview-search-results)  
23. Google Vertex AI search integration \- Docs by LangChain, [https://docs.langchain.com/oss/python/integrations/retrievers/google\_vertex\_ai\_search](https://docs.langchain.com/oss/python/integrations/retrievers/google_vertex_ai_search)  
24. How To Build A 5-Agent Team With Hermes Agentic OS In 30 Days : r/AISEOInsider \- Reddit, [https://www.reddit.com/r/AISEOInsider/comments/1u8zxt4/how\_to\_build\_a\_5agent\_team\_with\_hermes\_agentic\_os/](https://www.reddit.com/r/AISEOInsider/comments/1u8zxt4/how_to_build_a_5agent_team_with_hermes_agentic_os/)  
25. How to Use AI for Short-Form Video Creation: A Full Workflow from Script to MP4, [https://www.mindstudio.ai/blog/ai-short-form-video-creation-workflow-script-to-mp4](https://www.mindstudio.ai/blog/ai-short-form-video-creation-workflow-script-to-mp4)  
26. How to Use Higgsfield API \- Apidog, [https://apidog.com/blog/higgsfield-api/](https://apidog.com/blog/higgsfield-api/)  
27. Higgsfield | Provider | Eachlabs, [https://www.eachlabs.ai/higgsfield](https://www.eachlabs.ai/higgsfield)  
28. Higgsfield API \- AI Video Generation API: Pricing, Documentation \- Pixazo, [https://www.pixazo.ai/models/higgsfield](https://www.pixazo.ai/models/higgsfield)  
29. How To Create a Pexels API Python Pipeline with PyAirbyte, [https://airbyte.com/pyairbyte/pexels-api-python](https://airbyte.com/pyairbyte/pexels-api-python)  
30. pexels-api-with-video-searches \- PyPI, [https://pypi.org/project/pexels-api-with-video-searches/](https://pypi.org/project/pexels-api-with-video-searches/)  
31. Coqui TTS Python Guide: pip install \+ XTTS API Examples | Local AI Master, [https://localaimaster.com/blog/coqui-tts-python-guide](https://localaimaster.com/blog/coqui-tts-python-guide)  
32. Build a Voice Agent with Coqui TTS XTTS-v2 (Voice Cloning, Local) | CallSphere Blog, [https://callsphere.ai/blog/vw4h-build-voice-agent-coqui-tts-xtts-v2](https://callsphere.ai/blog/vw4h-build-voice-agent-coqui-tts-xtts-v2)  
33. Write\_videofile results in 1930x1080 even when I force clip.resize(width=1920,height=1080) before write\_videofile · Issue \#547 · Zulko/moviepy \- GitHub, [https://github.com/Zulko/moviepy/issues/547](https://github.com/Zulko/moviepy/issues/547)  
34. MoviePy: How to convert horizontal 1920x1080 video to vertical 1080x1920 video?, [https://stackoverflow.com/questions/73197950/moviepy-how-to-convert-horizontal-1920x1080-video-to-vertical-1080x1920-video](https://stackoverflow.com/questions/73197950/moviepy-how-to-convert-horizontal-1920x1080-video-to-vertical-1080x1920-video)  
35. SSD1306 OLED headless system monitor \- Raspberry Pi Forums, [https://forums.raspberrypi.com/viewtopic.php?t=150342](https://forums.raspberrypi.com/viewtopic.php?t=150342)  
36. Wrap and Render Multiline Text on Images Using Python's Pillow Library \- DEV Community, [https://dev.to/emiloju/wrap-and-render-multiline-text-on-images-using-pythons-pillow-library-2ppp](https://dev.to/emiloju/wrap-and-render-multiline-text-on-images-using-pythons-pillow-library-2ppp)  
37. Automatic text wrapping/text box filling · Issue \#6201 · python-pillow/Pillow \- GitHub, [https://github.com/python-pillow/Pillow/issues/6201](https://github.com/python-pillow/Pillow/issues/6201)

[image1]: <data:image/png;base64,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>