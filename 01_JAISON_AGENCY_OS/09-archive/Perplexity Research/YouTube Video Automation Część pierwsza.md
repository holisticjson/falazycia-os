<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Dobra, teraz zrób głęboki research dotyczący albo w pierwszej kolejności takich open source, które można przez MCP albo po API się połączyć z moim stackiem technologicznym. Chodzi mi o narzędzie agentowe, gdzie  Jest zrobiony research albo przez YouTube API najbardziej takich lukratywnych nisz do YouTube jeśli chodzi o tworzenie kanału contentu na YouTube taki który da się przełoży się po prostu są najpopularniejsze nisze z bada hooki thumbnail  opisy co najlepiej działa na bazie tego na przykład tworzę swój kopiuje kanał YouTube o podobnej tematyce tak aby zdobywać na jak najwięcej wyświetleń a potrzebne był do tego pewnie pipeline tworzenia od A do Z zmontowania filmu opisu thumbnail i jakieś takie no jeszcze linków afiliacyjnych  przy okazji do polecenia produktów no i plus wyświetlenia zarabianie na rosnącym kanale YouTube na wyświetleniach i na afiliacji

Najbardziej sensowny rdzeń dla Ciebie to: **open‑source YouTube Automation Agent + open‑source MCP serwer YouTube Data API + VidPipe jako agentowy edytor wideo**, spięte przez **Hermes OS / MCP / n8n**, a jako „dopalenie” danych nisz – **NexLev Niche Finder przez MCP**.[^1][^2][^3][^4][^5]

Poniżej masz twardy research + konkretne propozycje architektury „od A do Z”.

***

## 1. Co dokładnie chcemy zautomatyzować

Celem jest **autonomiczny system YouTube** który:

- **Szuka nisz / outlierów** na YouTube (wysokie RPM, faceless, rosnące kanały).
- **Reverse‑engineeruje kanały**: hooki, tytuły, długość filmów, miniatury, opisy, strukturę playlist.
- **Buduje pipeline od idei do publikacji**:
    - risercz → pomysł → skrypt → nagranie / generatywne wideo → montaż → miniatura → opis + SEO → publikacja → afiliacja.
- Jest **sterowalny z telefonu** (Hermes OS + komunikator), działa **asynchronicznie** i w modelu **low‑cost first**.

***

## 2. Kluczowe open‑source narzędzia agentowe „od A do Z”

### 2.1 YouTube Automation Agent (MIT, multi‑agent, MCP)

**YouTube Automation Agent** to open‑source, MIT‑licensed system, który **automatyzuje cały kanał YouTube end‑to‑end**.[^2][^4][^6][^7]

Co robi z pudełka:

- **Multi‑agentowy system**: osobne agenty jako:
    - **Content strategist** – risercz trendów w Twojej niszy.
    - **Script writer** – pełne skrypty pod retencję.
    - **Thumbnail designer** – generowanie pomysłów i grafiki miniatur.
    - **SEO optimiser** – tytuły, opisy, tagi pod algorytm.
    - **Publisher** – publikacja, harmonogram, rotacja contentu.[^2]
- **Integracja z Gemini / OpenAI** – repo działa zarówno na darmowym Gemini API, jak i komercyjnych LLM, co pozwala Ci podpiąć Twój istniejący stack LLM.[^8][^9][^2]
- **MCP integration** – projekt ma warstwę MCP do łączenia z YouTube Data API, Gemini, OpenAI i innymi narzędziami, co dobrze gra z Twoją wizją Hermes Agentic OS.[^2]
- **Dashboard + scheduler** – wbudowany panel do monitorowania agentów, override decyzji i harmonogramu publikacji; scheduler pozwala ustawić częstotliwość uploadów, time‑sloty, rotację tematów.[^2]
- **Database** – trackowanie każdego filmu, metryk (wyświetlenia, CTR, retention) i uczenia się na bazie historii uploadów.[^2]

Dlaczego to pasuje do J(AI)SON:

- **Low‑cost first** – można go odpalić na darmowym Gemini API, więc inference ≈ 0 zł, płacisz tylko za ewentualne generatywne wideo / assety.[^2]
- **Agentowa architektura** – każdy etap (research, skrypt, thumbnail, SEO, publikacja) to osobny agent, który możesz spiąć z Hermes OS przez MCP.
- **Zero‑coding dla końcowego użytkownika** – po setupie kanał może lecieć w dużej części autopilotem, Ty sterujesz tylko z „wieży kontrolnej”.[^2]

***

### 2.2 VidPipe – agentowy edytor wideo (CLI + pipeline)

**VidPipe** to open‑source agentowy edytor wideo, zbudowany na GitHub Copilot SDK, który **zamienia jedno nagranie w cały pakiet contentu**.[^10][^11][^5][^12]

Kluczowe cechy:

- **CLI‑pipeline 15 kroków** – z jednego pliku wideo dostajesz:
    - pocięte highlighty / shorts,
    - wypalone napisy,
    - social‑posty dla różnych platform,
    - draft blog‑posta.[^5][^12]
- **Automatyczna ekstrakcja transkryptów i metadanych** – po nagraniu plik jest przechwytywany, transkrypt generowany, a agenci decydują gdzie ciąć wideo, co da się świetnie podpiąć pod hooki z Twojego researchu.[^10][^5]
- **Agentic flow + „swipe interface”** – autor pokazał interfejs rodem z Tindera: możesz „swipe right” na propozycje postów / shortów, system resztę robi sam.[^10]

Rola w Twoim systemie:

- **Warstwa montażu** – zamiast pisać własny edytor, dajesz Hermesowi prosty prompt: „przepuść nagranie przez VidPipe i wystaw shortlistę do akceptacji na WhatsApp”.
- **Faceless / reuse** – możesz nagrać jedną sesję materiału i wypuścić kilka shortów + social cross‑posting bez ręcznego montażu.

***

### 2.3 YouTube Autopilot (end‑to‑end, trend detection)

Repo **youtube-autopilot** to kolejny open‑source projekt typu „end‑to‑end YouTube automation”:

- **Trend detection + multi‑agent editorial** – z opisu wynika, że system wykrywa trendy, ma system agencyjny do planowania treści, generuje wideo przy użyciu modeli takich jak Veo i publikuje wg harmonogramu.[^13]
- **Zero external dependencies** – autor podkreśla, że całość jest zamknięta w jednym stacku (ważne dla low‑cost, ale trzeba sprawdzić dokładnie jak rozwiązali hosting i API).[^13]

Może być alternatywą / inspiracją, ale w praktyce bazą dla Ciebie lepiej jest **YouTube Automation Agent + VidPipe**, bo są lepiej opisane pod multi‑agentowy usage i MCP.

***

## 3. Warstwa research \& MCP (niche intelligence)

### 3.1 Open‑source MCP serwer YouTube Data API (Yash Kashte)

Na LinkedIn pojawił się **open‑source Model Context Protocol server** dla YouTube Data API v3, stworzony specjalnie pod **AI agentów, automatyzację i research**.[^3]

Co daje:

- **16 wyspecjalizowanych narzędzi** MCP:
    - channel analytics (suby, views, pattern uploadów),
    - video intelligence (metadata, transkrypt, engagement),
    - SEO optimisation (tagi, miniatury, scoring),
    - audience insights (analiza komentarzy, słowa kluczowe).[^3]
- **Brak scrapingu, czyste oficjalne API** – korzysta z YouTube Data API v3, ale opakowuje to w MCP, więc dla Ciebie to po prostu zestaw narzędzi dostępnych z Hermesa / Claude / ChatGPT.[^3]
- **Zaprojektowany pod agentowe orkiestracje** – dokładnie to, czego potrzebujesz do:
    - szukania outlierów w niszach,
    - reverse‑engineeringu tytułów / długości,
    - budowy rankingów nisz pod RPM / konkurencję.[^3]

To jest bardzo mocny klocek do Twojej architektury:

- **Hermes OS** może traktować ten MCP serwer jako „YouTube Brain” – agent zadaje pytania typu „znajdź mi faceless kanały w niszy X z rosnącymi views 90 dni”, a serwer zwraca twarde dane.

***

### 3.2 Niche‑Finder (open‑source clustering nisz)

Repo **Niche-Finder** to open‑source projekt analizujący **Top Trending YouTube Videos Dataset**.[^14]

- Stack: **Python + Flask + Pandas + NumPy** do przetwarzania danych, **K‑Means** + **FP‑Growth** do klastrowania nisz i częstych tagów.[^14]
- Wynik: **interaktywne wizualizacje D3.js** pokazujące grupy filmów, trendy oraz powiązania tagów.[^14]

Minus:

- bazuje na **statycznym datasetcie trendingów**, nie na YouTube API v3, więc nie masz realtime research.[^14]

Rola dla Ciebie:

- **Inspiracja dla własnych algorytmów** – możesz użyć pomysłów (clusterowanie nisz, FP‑Growth na tagach) razem z YT MCP, żeby mieć własny moduł scoringu nisz, ale jako produkt końcowy lepiej oprzeć się na live danych.

***

### 3.3 YouTube‑API‑Analyzer (przykład niszowego audytu IT)

Repo **Youtube-API-Analyzer** pokazuje, jak ktoś użył YouTube API, by przeanalizować **kanały z branży IT** i wyciągnąć wnioski dla nowego twórcy.[^15]

- To prostszy przykład niż Niche‑Finder, ale dobrze pokazuje pattern:
    - zbierz kanały w określonej niszy,
    - policz metryki (views, suby, tempo wzrostu),
    - zbuduj rekomendacje typu „co działa, czego brakuje”.[^15]

Dobre jako „minimalny przykład” integracji YouTube API pod Twój własny moduł researchu.

***

## 4. SaaS narzędzia niszowe z MCP / API (opcjonalne dopalenie)

Tu już nie jest open‑source, ale **dają przewagę danych** i dobrze sklejają się z MCP / n8n.

### 4.1 NexLev – Niche Finder + MCP + n8n

**NexLev Niche Finder** to rozbudowane narzędzie do szukania **lukratywnych nisz i faceless kanałów**, które:

- **Skanuje YouTube 24/7** i monitoruje kanały long‑ i short‑form, wyciąga **breakout niches** i outlier channels.[^1]
- Ma **21 filtrów**: format, kategoria, jakość, przewidywany revenue, co pozwala wybrać nisze wg Twoich kryteriów (faceless, RPM, rosnąca uwaga).[^1]
- Daje:
    - Channel Tracker (views 48h, real‑time),
    - Channel Analytics,
    - listę viral videos z małych kanałów (90/60/30 dni),
    - wskazanie „Future Competition” w niszy.[^1]

Najważniejsze dla Ciebie:

- **NexLev MCP** – wystawia pełną analitykę jako MCP server:
    - 60+ MCP AI tools,
    - realtime data dla ponad 110M kanałów,[^1]
    - niche \& channel research z poziomu czata (Claude, ChatGPT, Cursor).
- W pakiecie Pro masz też **n8n automations for YouTube** + docelowo cały stack dla faceless creators.[^1]

To jest gotowy **„data backend”** dla Hermesa:

- zamiast pisać pełny YT research sam, możesz podpiąć **NexLev MCP** jako zewnętrzny serwer i mieć „YouTube intelligence as a service”, sterowane z Twojego OS.[^1]

***

### 4.2 TubeLab, TubeAI, vidIQ, Autonolab, Impactube

Nie są stricte open‑source, ale warto o nich wiedzieć jako referencje / backup:

- **TubeLab Niche Analyzer / Niche Finder** – żywe dane o **market size, saturation, monetization potential**, outlier channels i viral patterns; wprost pozycjonowane jako „market research tool” dla YouTube.[^16][^17]
- **TubeAI Niche Finder \& Database** – baza **10M+ przeanalizowanych filmów**, outlier score, statystyki optymalnej długości tytułu, power wordów, długości video, similarity search miniatur.[^18]
- **vidIQ Niche Finder** – darmowe narzędzie do **sprawdzania demand, competition, RPM range, viability score** dla nisz; wskazuje sub‑nisze typu „resistance band workouts for seniors” zamiast ogólnego „fitness”.[^19]
- **Autonolab Free AI YouTube Niche Finder** – fokus na **supply vs demand, market gaps, outlier‑backed niches**, bez logowania.[^20]
- **Impactube** – „Opportunity radar”: outlier videos, niche finder, AI thumbnails i workspace Impact Studio.[^21]

Dla Twojej architektury:

- trzymałbym je jako **manualne narzędzia researchowe** do pierwszego wyboru niszy, a później przeniósł logikę do MCP (NexLev / własny YT MCP).

***

## 5. Proponowana architektura pod Twój stack

### 5.1 Warstwa danych / research (MCP)

1. **Primary (open‑source):**
    - self‑hostowany **MCP serwer YouTube Data API v3** (projekt Yasha) jako „YouTube Intelligence Engine”.[^3]
    - Hermesa uczysz narzędzi typu:
        - `get_top_channels_in_niche`,
        - `get_outlier_videos`,
        - `analyze_titles_thumbnails`,
        - `segment_audience_comments`.
2. **Optional (SaaS dopalenie):**
    - podpięty **NexLev MCP** jako drugi provider danych nisz:
        - agent „Niche Strategist” pyta NexLev o profitable niches, faceless outliers, RPM predictions, future competition.[^1]
3. **Logika scoringu nisz:**
    - wykorzystujesz inspiracje z Niche‑Finder (K‑Means, FP‑Growth) i TubeAI (outlier score, stats tytułów) do własnych metryk:
        - score niszy = demand + RPM + competition gap + faceless potential + trend.[^19][^18][^14]

***

### 5.2 Warstwa agentów contentowych

1. **YouTube Automation Agent jako trzon**:
    - każdy agent (strategist, script writer, thumbnail designer, SEO optimiser, publisher) staje się **Hermes tool** lub „sub‑agent” w Twojej orkiestracji.[^4][^2]
    - integrujesz go z:
        - Gemini 2.5 (free tier),
        - Twoim routerem LLM (open‑weight, NIM, Ollama) wg wcześniejszego stacku.
2. **VidPipe jako moduł montażu / repurposing**:
    - n8n / Hermes odpala CLI `vidpipe /path/to/video.mp4`,
    - VidPipe generuje shorts, captions, social posts i blog,
    - Ty z telefonu „swipe’ujesz” akceptowane propozycje (przez prostą UI / link).[^5][^10]
3. **Opcjonalnie youtube-autopilot**:
    - jako dodatkowy pipeline dla kanałów stricte generatywnych (Veo + full automation).[^13]

***

### 5.3 Warstwa orkiestracji (n8n + Hermes OS)

Prosty model:

- **Cron jobs** w n8n:
    - co 24h: „scan niche via MCP” → update scoreboard nisz,
    - co X dni: „plan next 3 videos” w YouTube Automation Agent,
    - po nagraniu pliku w folderze GCS / lokalnym: trigger VidPipe.
- **Hermes OS jako „text‑to‑action” hub**:
    - komenda z WhatsApp:
        - „/yt‑scan AI dla przedsiębiorców w PL” → agent robi research przez MCP, zwraca top 5 sub‑nisz + kanały do sklonowania, z hookami i miniaturami.
    - „/yt‑batch 3 shorty na temat X” → Hermes odpala YouTube Automation Agent + VidPipe end‑to‑end.
- **Streamlit dashboard**:
    - tylko najważniejsze KPI: views 48h, RPM estimates (jeśli z NexLev), nowe outlier videos, status kolejnych uploadów, affiliate konwersje.

***

### 5.4 Afiliacja + opisy + linki

W warstwie SEO / publikacji:

- **SEO optimiser agent** z YouTube Automation Agent dokleja:
    - sekcję „Polecane narzędzia” z Twoimi affiliate linkami,
    - CTA do lead magnetów w Systeme.io.[^2]
- W bazie (DB) trzymasz mapę:
    - *temat filmu* → *lista afiliacji* → *kody UTM* → *landing w Systeme.io*.

To można łatwo podpiąć pod n8n (webhook do Systeme.io) i mieć **tracking afiliacyjny** oraz **lead flow** spójny z lejkiem agencji.

***

## 6. Krótka tabela porównawcza kluczowych narzędzi

| Narzędzie | Open‑source | Fokus | MCP / API | Rola w Twoim systemie |
| :-- | :-- | :-- | :-- | :-- |
| YouTube Automation Agent | Tak (MIT)[^2][^4] | End‑to‑end kanał: research, skrypt, thumbnail, SEO, publikacja | MCP + Gemini/OpenAI + YouTube Data API[^2] | Główny „YouTube Agent” – generacja contentu i publikacja |
| VidPipe | Tak[^5][^10] | Agentowy edytor wideo, shorts, captions, social posts, blog | CLI + GitHub Copilot SDK[^5][^10] | Montaż i repurposing jednego nagrania na multi‑content |
| YT MCP Server (Yash) | Tak[^3] | Channel/video analytics, SEO, audience insights | MCP + YouTube Data API v3[^3] | Warstwa „YouTube Intelligence” dla Hermes OS |
| NexLev Niche Finder + MCP | Nie (SaaS)[^1] | Niche finder, RPM predictor, faceless outliers, channel tracker | Własny MCP + 110M+ kanałów, 60+ narzędzi[^1] | Opcjonalny data backend nisz i faceless kanałów |
| Niche-Finder | Tak[^14] | Klasterowanie nisz na podstawie datasetu trendingów | Dataset + Flask, brak live API[^14] | Inspiracja algorytmiczna pod Twój scoring nisz |


***

Jeżeli chcesz, w następnym kroku mogę Ci rozpisać **konkretny plan wdrożenia**:

- które repo ściągamy jako pierwsze,
- jak je spiąć z Hermes OS / MCP,
- jak ustawić przykładowe **scenariusze n8n** (cron research nisz, automatyczne generowanie paczki: skrypt + thumbnail + opis + afiliacja).
<span style="display:none">[^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^32][^33]</span>

<div align="center">⁂</div>

[^1]: https://www.nexlev.io/niche-finder

[^2]: https://www.linkedin.com/posts/himanshu-sanwal-7a5b04197_youtubeautomation-ai-genai-activity-7463340234567622656-PsJB

[^3]: https://www.linkedin.com/posts/yash-kashte_ai-machinelearning-youtube-activity-7429784011851501570-dwK7

[^4]: https://github.com/darkzOGx/youtube-automation-agent

[^5]: https://htekdev.github.io/vidpipe/

[^6]: https://trendshift.io/repositories/29499

[^7]: https://ai-heartland.com/automation/youtube-automation-agent/

[^8]: https://github.com/darkzOGx/youtube-automation-agent/blob/master/package.json

[^9]: https://github.leishennb.icu/darkzOGx

[^10]: https://www.youtube.com/watch?v=ESzej015TaE

[^11]: https://htek.dev/articles/vidpipe-copilot-cli-challenge

[^12]: https://dev.to/htekdev/introducing-vidpipe-my-ai-video-editor-that-does-everything-435b

[^13]: https://github.com/khaoss85/youtube-autopilot

[^14]: https://github.com/johanfortus/Niche-Finder

[^15]: https://github.com/EspositoLucas/Youtube-API-Analyzer

[^16]: https://tubelab.net/niche-analyzer

[^17]: https://tubelab.net/youtube-niche-finder

[^18]: https://tubeai.app/youtube-niche-finder

[^19]: https://vidiq.com/youtube-niche-finder/

[^20]: https://autonolab.com/free-ai-youtube-niche-finder

[^21]: https://impactube.com/en/

[^22]: service-packages.md

[^23]: Ghost v2 - Głos Marki Tomasz.md

[^24]: moj-profil-i-srodowisko.md

[^25]: PROFIL PROJEKTU__Projekt dotyczy _Jaison_ (jaison..md

[^26]: https://jaison.pl/

[^27]: https://www.nexlev.io/

[^28]: https://github.leishennb.icu/darkzOGx/youtube-automation-agent

[^29]: https://github.com/darkzOGx/youtube-automation-agent/issues

[^30]: https://github.com/darkzOGx

[^31]: https://github.leishennb.icu/darkzOGx/youtube-automation-agent/pulls

[^32]: https://github.leishennb.icu/darkzOGx/youtube-automation-agent/pull/6

[^33]: https://github.leishennb.icu/darkzOGx/youtube-automation-agent/actions

