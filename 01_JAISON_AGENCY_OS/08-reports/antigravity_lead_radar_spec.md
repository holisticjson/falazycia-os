
# AntiGravity — specyfikacja techniczna Lead Radar dla J(AI)SON

Ten dokument opisuje docelową architekturę modułu **Lead Radar** dla dashboardu Streamlit, wraz z logiką źródeł, pipeline’em danych, trybami pozyskiwania leadów, scoringiem, integracjami i kolejnością wdrożenia. Dokument jest napisany tak, aby agent kodujący AntiGravity mógł przejść z poziomu koncepcji do implementacji bez zgadywania założeń. [cite:5][cite:19][cite:7]

## Cel systemu

Lead Radar ma wykrywać polskie źródła popytu na usługi: strony internetowe, automatyzacje, n8n, chatboty, integracje API oraz wdrożenia AI, a następnie normalizować je do jednego rekordu w dashboardzie Streamlit. [cite:7][cite:16][cite:19]

Docelowo system ma działać asynchronicznie i wspierać dwa tryby: **inbound lead discovery** z portali i przetargów oraz **outbound signal discovery** z katalogów firm, wyszukiwarek i profili firmowych. [cite:5][cite:8][cite:19]

## Założenia architektoniczne

System powinien być zbudowany jako warstwowy pipeline:

1. **Source registry** — lista źródeł i metadanych.
2. **Fetch layer** — pobieranie HTML, JSON lub danych z integratora.
3. **Parse layer** — ekstrakcja tytułu, opisu, linku, daty, organizacji i sygnałów popytu.
4. **Normalize layer** — mapowanie do wspólnego schematu Lead Radar.
5. **AI classify layer** — klasyfikacja typu leada przez Gemini 2.5 Flash na Vertex AI.
6. **Scoring layer** — wycena priorytetu i jakości leada.
7. **Storage layer** — zapis do SQLite/Postgres/CSV i render w Streamlit.
8. **Action layer** — oznaczanie, filtrowanie, eksport, follow-up, webhook do n8n. [cite:5][cite:19][cite:16]

## Model danych

Każdy rekord w Lead Radar powinien mieć minimalnie takie pola:

| Pole | Typ | Opis |
|---|---|---|
| `lead_id` | string | Stabilny hash źródła + URL + tytułu |
| `source_name` | string | Nazwa źródła |
| `source_type` | enum | `freelance`, `tender`, `directory`, `social`, `search`, `job_board`, `manual` |
| `access_mode` | enum | `public`, `login`, `integrator`, `manual` |
| `fetch_mode` | enum | `httpx`, `scrapy`, `playwright`, `composio`, `serpapi`, `custom_search` |
| `url` | string | URL ogłoszenia lub wpisu |
| `title` | string | Tytuł wpisu / ogłoszenia |
| `body_raw` | text | Surowy tekst |
| `body_clean` | text | Tekst oczyszczony |
| `published_at` | datetime | Data publikacji, jeśli dostępna |
| `organization` | string | Firma / instytucja / autor |
| `city` | string | Miasto / region |
| `lead_type` | enum | `website`, `automation`, `chatbot`, `ai_implementation`, `api_integration`, `consulting`, `mixed` |
| `intent_score` | int | Sygnał realnej intencji zakupu 0–100 |
| `fit_score` | int | Dopasowanie do oferty J(AI)SON 0–100 |
| `freshness_score` | int | Świeżość ogłoszenia 0–100 |
| `priority_score` | int | Łączny wynik 0–100 |
| `needs_company` | bool | Czy najpewniej wymagana firma / formalny wykonawca |
| `needs_login` | bool | Czy źródło wymaga logowania |
| `risk_flag` | enum | `low`, `medium`, `high` |
| `outreach_mode` | enum | `apply_platform`, `email`, `form`, `manual`, `n8n_webhook` |
| `notes` | text | Uwagi operacyjne |

## Rejestr źródeł

Każde źródło w systemie powinno mieć własny rekord konfiguracyjny, niezależny od pojedynczych leadów. Ten rejestr powinien być przechowywany w YAML albo JSON. [cite:31][cite:25][cite:27][cite:45]

Przykładowy schemat źródła:

```yaml
source_name: "Zleca.pl"
source_type: "freelance"
access_mode: "public"
fetch_mode: "httpx"
needs_login: false
requires_company: false
robots_risk: "medium"
selector_hints:
  listing: ".job-item, article, .announcement"
  title: "h2, h3, a"
  link: "a[href]"
  body: ".description, .content"
  date: "time, .date"
cadence: "6h"
keyword_pack: ["strona internetowa", "chatbot", "automatyzacja", "n8n", "AI"]
```

## Warstwy pobierania

### 1. HTTPX + BeautifulSoup

Używać dla źródeł publicznych, prostych i lekkich: Zleca.pl, WorkConnect, część agregatorów przetargów, część BIP-ów, lokalne katalogi i proste job boardy. [cite:25][cite:27][cite:46][cite:52]

### 2. Scrapy

Używać dla dużego wolumenu źródeł, katalogów firm, wielu stron paginowanych oraz agregatorów, gdzie liczy się kolejka, deduplikacja i harmonogram crawlu. To dotyczy szczególnie katalogów typu Panorama Firm / pkt.pl, TED Europa oraz większych zbiorów stron regionalnych. [cite:52][cite:61][cite:66]

### 3. Playwright

Używać dla źródeł z ciężkim JS, dynamicznymi filtrami, paginacją klikaną lub częściowo zamkniętym UI: platformazakupowa.pl, oneplace.marketplanet.pl, eB2B, część job boardów, Oferteo, Fixly, OLX, Pracuj.pl. [cite:31][cite:41][cite:45][cite:52][cite:57]

### 4. Integratory i query-based discovery

Używać tam, gdzie klasyczny scraping jest słabszy, ryzykowny albo niepotrzebnie ciężki: LinkedIn, część sociali, wyniki Google i wyszukiwanie profili/firm po frazach. [cite:85][cite:90][cite:95][cite:97][cite:99]

## LinkedIn i wyszukiwanie po zapytaniach

Dla LinkedIn nie należy budować agresywnego scrappera jako pierwszego wyboru. Rozsądniejsza architektura to dwa równoległe tryby: **Composio LinkedIn toolkit** do akcji i integracji oraz **Google Search / Google Custom Search / SerpApi** do discovery opartego o zapytania. [cite:85][cite:90][cite:95][cite:96][cite:97][cite:99]

Przykładowe zapytania query-based discovery:

- `site:linkedin.com/in "founder" "Łódź" "software"`
- `site:linkedin.com/in "marketing manager" "e-commerce" "Polska"`
- `site:linkedin.com/company "automation" "Poland"`
- `site:linkedin.com/posts "szukam automatyzacji"`
- `site:linkedin.com/posts "wdrożenie AI"`
- `site:linkedin.com/posts "szukam wykonawcy strony"`

Ten sam wzorzec można stosować do Google dla stron firmowych i zapytań:

- `"szukam wykonawcy strony" OR "zlecę stronę"`
- `"wdrożenie chatbota" Polska`
- `"automatyzacja procesów" "zapytanie ofertowe"`
- `"n8n" OR "Make" "szukam"`
- `"AI dla firmy" "oferta" OR "zapytanie"`

## Alternatywa: Composio + broker integracyjny

Jeżeli źródło ma sensowną integrację przez Composio, należy dodać do rejestru źródeł dodatkowe pole `integrator_mode = composio`. Dla LinkedIn Composio publikuje toolkit i CLI/MCP pod agentowe akcje, więc warto potraktować to jako warstwę do automatyzacji działań na koncie, a nie jako pełny zamiennik discovery w całym rynku. [cite:85][cite:90][cite:95][cite:96]

Dla wyszukiwania można rozważyć dwa tryby:

- **SerpApi / podobny broker przez Composio** do strukturalnych wyników Google. [cite:97]
- **Google Custom Search / query URL templates** do budowy tańszego discovery dla wybranych nisz. [cite:98][cite:99]

## Mapa źródeł v3

| Źródło | Tryb główny | Biblioteka / integrator | Needs login | Robots risk | Cadence | Lead score start | Uwagi |
|---|---|---|---:|---|---|---:|---|
| Useme | public + konto | httpx + bs4 | Tak | medium | 6h | 70 | Publiczne listy + konto do rozliczeń [cite:34][cite:69] |
| Zleca.pl | public crawl | httpx + bs4 | Nie | medium | 6h | 78 | Dobry kandydat na szybki inbound crawl [cite:27][cite:67] |
| WorkConnect | public crawl | httpx + bs4 | Nie | low | 6h | 82 | Ma sekcje AI i automatyzacja [cite:25] |
| Oferteo | dynamic | playwright + bs4 | Tak | medium | 12h | 74 | Dobre pod usługi lokalne i strony |
| Fixly | dynamic | playwright + bs4 | Tak | medium | 12h | 62 | Filtry i UI oparte o JS |
| Baza Konkurencyjności | public crawl | httpx + bs4 | Nie | low | 12h | 80 | Wysoka wartość przy zapytaniach IT |
| eZamówienia | dynamic | playwright + bs4 | Nie / warunkowo | medium | 24h | 76 | Formalne postępowania, selekcja po słowach kluczowych |
| platformazakupowa.pl | dynamic | playwright + bs4 | Tak | medium | 12h | 84 | Bardzo dobre źródło chatbotów i wdrożeń [cite:31] |
| oneplace.marketplanet.pl | dynamic | playwright + bs4 | Tak | medium | 12h | 79 | IT i procurement [cite:45] |
| eB2B | dynamic | playwright + bs4 | Tak | medium | 12h | 78 | Źródło postępowań IT [cite:41] |
| Przetargi.eGospodarka | public crawl | httpx + bs4 | Nie | low | 6h | 81 | Dobry agregator przetargów chatbot/AI [cite:46] |
| PrzetargHub | public crawl | httpx + bs4 | Nie | low | 6h | 80 | Warto monitorować po frazach chatbot/LLM [cite:24] |
| i-przetargi | public crawl | httpx + bs4 | Nie | low | 6h | 79 | Publiczne ogłoszenia [cite:20] |
| Pressinfo | public crawl | httpx + bs4 | Nie | low | 12h | 72 | Dodatkowy agregator |
| LinkedIn Jobs | query discovery | composio linkedin + google search | Tak | high | 24h | 68 | Lepiej query-based niż pełny scraping [cite:85][cite:90] |
| LinkedIn Posts | query discovery | google search + composio | Tak | high | 12h | 75 | Dobre do wykrywania intencji i postów “szukam” [cite:85][cite:96][cite:99] |
| LinkedIn Profiles | query discovery | custom search / serpapi | Nie w discovery | medium | 24h | 66 | `site:linkedin.com/in` + role + branże [cite:97][cite:98] |
| Google SERP | search broker | serpapi / custom search | Nie | low | 12h | 77 | Odkrywanie stron, artykułów, ogłoszeń i profili [cite:97][cite:99] |
| No Fluff Jobs | public crawl | httpx + bs4 | Nie | low | 12h | 52 | Niższy priorytet; sygnały kontraktowe |
| Just Join IT | public crawl | httpx + bs4 | Nie | low | 12h | 50 | Bardziej sygnał rynku niż lead core |
| Pracuj.pl | dynamic | playwright + bs4 | Nie / warunkowo | high | 24h | 45 | Rynek pracy, nie główny kanał zleceń |
| Panorama Firm / pkt.pl | directory crawl | scrapy + bs4 | Nie | medium | weekly | 64 | Outbound i lookup firm do segmentacji |
| BIP uczelni i instytucji | public crawl | httpx + bs4 | Nie | medium | 24h | 73 | Często pojawiają się chatboty, portale i wdrożenia [cite:24][cite:32] |
| Strony firm z formularzem | manual + assist | playwright + manual | Nie | high | weekly | 55 | Discovery tak, kontakt ostrożnie, bez harvestu danych |

## Pola konfiguracyjne źródeł

AntiGravity powinien generować dla każdego źródła pełny rekord konfiguracyjny z takimi kolumnami:

| Kolumna | Znaczenie |
|---|---|
| `source_name` | Nazwa źródła |
| `category` | `freelance`, `tender`, `directory`, `social`, `search` |
| `needs_login` | Czy trzeba logować się do źródła |
| `requires_company` | Czy źródło zwykle zakłada działanie jako firma / wykonawca |
| `preferred_stack` | `httpx`, `scrapy`, `playwright`, `composio`, `serpapi`, `custom_search` |
| `selector_hint` | Wstępne selektory listingu i tytułu |
| `cadence` | Jak często odpytywać źródło |
| `query_templates` | Lista gotowych zapytań |
| `robots_risk` | Ocena ryzyka technicznego i regulaminowego |
| `dedupe_key` | Jak deduplikować rekordy |
| `outreach_mode` | `platform_apply`, `email`, `form`, `manual`, `crm_push` |
| `enabled` | Flaga włączenia w panelu |

## Scoring

Proponowany scoring początkowy:

- +30 gdy występuje słowo: `chatbot`, `voicebot`, `AI`, `LLM`, `automatyzacja`, `n8n`.
- +20 gdy jest budżet, zakres lub termin realizacji.
- +15 gdy wpis jest z ostatnich 7 dni.
- +15 gdy źródło ma wysoki fit do oferty J(AI)SON.
- +10 gdy istnieje łatwa ścieżka odpowiedzi: formularz, kontakt, platforma.
- -20 gdy to wyłącznie etat bez komponentu B2B/usługowego.
- -25 gdy ogłoszenie jest bardzo ogólne i bez zakresu. [cite:7][cite:16][cite:25][cite:27]

## Moduły w Streamlit

W Lead Radar w Streamlit powinny znaleźć się przynajmniej takie moduły:

1. **Sources** — włączanie i wyłączanie źródeł.
2. **Crawl queue** — status zadań fetch/parse.
3. **Lead inbox** — nowe rekordy z filtrem po `lead_type` i `priority_score`.
4. **Search builder** — generator zapytań Google / LinkedIn / branż.
5. **AI triage** — Gemini klasyfikuje i streszcza lead.
6. **Outreach actions** — eksport do CSV, webhook do n8n, oznaczanie statusów.
7. **Analytics** — skuteczność źródeł, top frazy, top branże, top miasta. [cite:5][cite:19]

## Proponowane klasy Python

```python
class SourceConfig:
    source_name: str
    category: str
    needs_login: bool
    requires_company: bool
    preferred_stack: str
    cadence: str
    query_templates: list[str]
    robots_risk: str
    selector_hint: dict

class RawLead:
    source_name: str
    url: str
    title: str
    body_raw: str
    published_at: str | None
    metadata: dict

class NormalizedLead:
    lead_id: str
    source_name: str
    source_type: str
    lead_type: str
    title: str
    body_clean: str
    organization: str | None
    city: str | None
    intent_score: int
    fit_score: int
    freshness_score: int
    priority_score: int
    outreach_mode: str

class SourceAdapter:
    def fetch(self, source_config):
        ...
    def parse(self, html_or_payload):
        ...
    def normalize(self, parsed_items):
        ...
```

## Kolejność wdrożenia

Najrozsądniejszy rollout dla AntiGravity to trzy fale:

### Faza 1 — szybkie źródła

- Zleca.pl
- WorkConnect
- Przetargi.eGospodarka
- PrzetargHub
- i-przetargi
- Baza Konkurencyjności
- Google SERP query builder [cite:25][cite:27][cite:20][cite:24][cite:46]

Cel: szybko wykryć pierwsze leady przy niskim koszcie technicznym.

### Faza 2 — źródła dynamiczne

- platformazakupowa.pl
- oneplace.marketplanet.pl
- eB2B
- Oferteo
- Fixly
- wybrane BIP-y uczelni [cite:31][cite:41][cite:45][cite:24]

Cel: wejść w droższe, ale lepsze jakościowo źródła.

### Faza 3 — discovery hybrydowe

- LinkedIn Jobs
- LinkedIn Posts
- LinkedIn Profiles query search
- katalogi firm i strony firmowe
- Panorama Firm / pkt.pl
- Clutch / GoodFirms [cite:85][cite:90][cite:96][cite:97][cite:99]

Cel: zbudować warstwę outbound signal discovery, partnerstwa i targetowane prospecting listy.

## Zasady bezpieczeństwa i higieny wdrożenia

Agent powinien preferować źródła publiczne, lekkie i przewidywalne zamiast budowania od razu skomplikowanych obejść. To zmniejsza chaos operacyjny i koszt utrzymania. [cite:5][cite:8][cite:16]

W praktyce należy:

- logować błędy per źródło,
- stosować cache i deduplikację,
- rozdzielać tryb `manual`, `public`, `integrator`, `login`,
- ograniczyć częstotliwość zapytań,
- nie harvestować wrażliwych danych kontaktowych z miejsc, gdzie nie ma do tego jasnego uzasadnienia procesowego,
- dać Tomaszowi prosty panel do zatrzymywania źródeł jednym kliknięciem. [cite:5][cite:8][cite:19]

## Decyzje operacyjne

Na dziś najbardziej opłacalny rdzeń systemu to: **HTTPX + BS4 + Scrapy + Playwright + query-based discovery + Gemini 2.5 Flash**. [cite:5][cite:19][cite:52][cite:61][cite:97]

Największy quick win leży nie w „scrapowaniu wszystkiego”, tylko w połączeniu czterech warstw: publiczne portale zleceń, agregatory przetargów, query builder Google/LinkedIn oraz katalogi firm do outboundu. [cite:16][cite:25][cite:27][cite:24][cite:46][cite:97]
