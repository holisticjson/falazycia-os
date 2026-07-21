# 🎯 MASTER GOALS — Holistic Jason AI Agency OS
*Dokument zyjacy. Aktualizuj po kazdej znaczacej decyzji architektonicznej.*
Ostatnia aktualizacja: 2026-06-20 | Wlasciciel: Tomasz (holisticjson@gmail.com)

---

## WIZJA (North Star)

Zbudowac pelnoprawna agencje marketingowa AI dzialajaca na 90% autonomicznie — z Tomaszem jako dyrektorem zarzadzajacym, a nie operatorem. Klientami sa firmy B2B i lokalny biznes (Polska). Projekt Holistic Broker jest projektem rownoleglym — NIE priorytetem dopoki Agencja nie generuje cashflow.

---

## CELE KWARTALNE (Q3 2026)

| # | Cel | Wskaznik Sukcesu | Status |
|---|-----|-----------------|--------|
| 1 | Pierwszy placy klient Agencji | Kontrakt >= 2000 PLN/mies. | Nie started |
| 2 | Hermes dziala 24/7 na Telegramie | Bot odpowiada < 30s, 0 awarii/tydzien | Czesciowo |
| 3 | Lejek B2B live na Systeme.io | 100+ leadow w bazie | Nie started |
| 4 | RAG Baza Wiedzy dziala | Agent cytuje zrodla, 0 halucynacji | Czesciowo |
| 5 | Social Media na autopilocie | 3 posty/tydzien publikowane przez agenta | Nie started |

---

## AGENCI W SIDEBARZE — Stan Faktyczny

AKTYWNE (4 agentów):
- Hermes - Główny orkiestrator. Telegram, Swarm, automatyzacje, Systeme.io
- Antigravity - Systemowy architekt. Kod, debugging, konfiguracja GCP, wdrożenia
- Gemini - Super-analityk. Bezpośrednie zapytania do bazy wiedzy Vertex AI RAG
- Claude - Redaktor treści. Copywriting i maile (wbudowany kontekst Ghostwritera)

USUNIĘTE (w celu redukcji szumu kognitywnego i ADHD-friendly UI):
- OpenClaw (duplikacja)
- Codex (zastąpiony przez Antigravity)
- Free Claude Code (duplikacja)
- Ghost Operator (przeniesiony jako filtr kontekstowy bezpośrednio do agenta Claude)

---

## STRATEGIA RAG (Mózg Danych Vertex AI Search)

Tworzymy jedną główną aplikację wyszukiwania (Search App) o nazwie `notebook-search-agent` i podpinamy pod nią 3 natywne magazyny danych (Data Stores) w GCP:

| Nazwa w GCP | Typ | Zawartość / Źródło |
|-------------|-----|--------------------|
| **ds-tech-docs** | Website | Dokumentacja techniczna z sitemapami: n8n, Systeme.io help, cloud.google.com/vertex-ai/docs/*, hermes-agent.nousresearch.com/docs/* |
| **ds-agency-drive** | Google Drive | Notatki Obsidian, Briefy, Cele (Udostępniony folder z konta prywatnego `tomasz.duda` do `holisticjson`) |
| **ds-static-archive** | Cloud Storage | Duże pliki PDF, raporty rynkowe, stare archiwum GCS (`gs://holistic_kubelek`) |

---

## BUDZET GCP (3600 PLN Free Trial)

PULAPKA 1: Free Trial wygasa po 90 dniach lub po wyczerpaniu. Potem platnosci z karty.
PULAPKA 2: Enterprise Edition (do Workspace connectors) ma wyszsza cene po Free Trial.
PULAPKA 3: Stitch to odrebna firma — GCP Free Trial NIE pokrywa ich subskrypcji.
STRATEGIA: Stabilizacja RAG (Vertex AI Search + GCS). NIE aktywujemy enterprise connectorow.

---

## BAZA WIEDZY — Hierarchia Zrodel

POZIOM 1 (zawsze aktywne):
- GCS holistic_kubelek — kursy, notatki
- Obsidian Vault — brain_dump Tomasza

POZIOM 2 (przez NotebookLM MCP):
- HOLISTIC_KNOWLEDGE_BASE/01_Newslettery_MD (auto via GAS)
- HOLISTIC_KNOWLEDGE_BASE/02_Kursy_Szkolenia_MD
- Dokumentacja Hermesa (https://hermes-agent.nousresearch.com/docs/)

POZIOM 3 (planowane, n8n):
- GCS -> Google Drive sync pipeline
- Dokumenty klientow -> GCS -> Vertex AI

---

## ROADMAP
 
 Sprint 1 (TERAZ): Integracja GTM/Stripe/Slack, naprawa os.holisticjson.pl i aktywacja Hermes Studio.
 Sprint 2 (Tydz. 1): Konfiguracja lejków Systeme.io oraz podpięcie 10 narzędzi do Viktor.com (zysk 10 000 kredytów).
 Sprint 3 (Tydz. 2): Złożenie wniosku o grant $2000 Google for Developers dla holistycznybroker.pl (zasilanie modeli Gemini).
 Sprint 4 (Tydz. 3): Budowa smartrade.pl (Damian Dzik WS, społeczność 100k+) — portal, blog i platforma sprzedażowa.
 Sprint 5 (Tydz. 4): Wdrożenie automatyzacji i chatbotów na stronach WordPress klientów agencji (VIPTransporter, KurczakUJasia, coolfon, swiatyniaharmonii) jako case studies.

---

## 🚀 PROJEKTY I INTEGRACJE STRATEGICZNE (Agencja AI)

### 1. Viktor.com — Scentralizowany Mostek Integracyjny
- **Budżet i korzyści:** $100 w wersji startowej + **10 000 darmowych kredytów** (1000 kredytów za każde z 10 podłączonych narzędzi).
- **Zastosowanie:** Podłączenie Meta Ads, Google Ads, Google Analytics, LinkedIn, Instagram, YouTube, Canva, Search Console, Sheets i Stripe. Służy do automatyzacji marketingu pod wspólnym kierownictwem Hermesa i Viktora.

### 2. Projekt holistycznybroker.pl (Real Estate AI Driven)
- **Cel finansowy:** Wniosek o **grant $2000** do *Google for Developers*.
- **Zastosowanie środków:** Finansowanie i zasilanie modeli Gemini z Google Agent Platform na koncie organizacji GCP (`brokerholistic@gmail.com`) dla Hermesa, Streamlita oraz lokalnych i chmurowych agentów AntiGravity. Z kolei agencja J(a)SON ADHD działa na koncie `holisticjson@gmail.com`.

### 3. Portal smartrade.pl (Edukacja Tradingowa & Infoprodukty)
- **Partner strategiczny:** Damian Dzik WS (społeczność **100k+** na Instagramie).
- **Zastosowanie:** Stworzenie edukacyjnego bloga, portalu o tradingu oraz zautomatyzowanej platformy do sprzedaży infoproduktów jako potężnego kanału edukacyjnego i agencyjnego showcase.

### 4. Pilotażowe Wdrożenia u Klientów (Case Studies Agencji)
Wszystkie poniższe strony są oparte na WordPressie. Wdrażamy na nich optymalizację SEO, n8n, chatboty i automatyzacje sprzedaży w celach pokazowych agencji:
- **VIPTransporter.pl** — automatyzacja rezerwacji i zapytań VIP.
- **KurczakUJasia.pl** — chatbot zamówień i asystent menu.
- **coolfon.pl** — asystent serwisu i automatyczna wycena.
- **swiatyniaharmonii.pl** — asystent rezerwacji sesji i harmonii.

---

## PODJĘTE DECYZJE ARCHITEKTONICZNE

1. **Uproszczenie UI:** Usunięto 3 nadmiarowe agenty. Została siatka 2x2 z głównymi 4 profilami.
2. **Ghost Operator:** Wbudowany w prompt systemowy (Claude wczytuje plik `Ghost v2 - Głos Marki Tomasz.md` ze Skarbca).
3. **NotebookLM w chmurze:** Zamiast lokalnego mostka Playwright MCP, wykorzystujemy natywną funkcję Google Drive + Website w Vertex AI Search (100% stabilności).
4. **Holistic Broker:** Pozostaje jako przełącznik kontekstu w Streamlicie. Prace nad brokeringiem odkładamy na Q4.

---

Ten dokument jest zrodlem prawdy dla wszystkich agentow. Przy kazdej decyzji architektonicznej — sprawdz tu najpierw.

