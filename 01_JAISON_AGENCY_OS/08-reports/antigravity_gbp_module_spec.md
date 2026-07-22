
# AntiGravity — moduł Google Business Profile / Local SEO dla Lead Radar

Dokument definiuje architekturę modułu GBP dla dashboardu Streamlit w ekosystemie J(AI)SON. Cel: lokalny scanner wizytówek Google, siatka rankingowa, menedżer opinii, generator zadań optymalizacyjnych i workflow publikacji, w podejściu low-friction, low-cost i zgodnym z oficjalnymi narzędziami Google. [web:105][web:106][web:108][web:109][web:115][web:119]

## 1. Cel biznesowy

Moduł ma pomóc firmie lokalnej lub agencji szybko zrozumieć: gdzie spada widoczność w Map Pack, jakie działania podjąć w GBP, jak odpowiedzieć na opinie i jak monitorować konkurencję bez ręcznego klejenia danych. [web:115][web:119][web:116]

Dla J(AI)SON to ma być element szerszego Lead Radar, a nie osobny ciężki produkt SaaS. Ma działać jako lekki panel w Streamlit, podpięty do n8n, Vertex AI i ewentualnie Composio. [cite:5][cite:19][web:85][web:90][web:95][web:96]

## 2. Co jest oficjalne

Google Business Profile APIs pozwalają zarządzać lokalizacjami, postami i danymi recenzji, a dokumentacja Google opisuje również pracę z danymi recenzji i odczyt stanu odpowiedzi. [web:105][web:106][web:108]

Google Business Profile Help potwierdza, że można odpowiadać na recenzje z poziomu profilu, ale odpowiedzi są moderowane i profil musi być poprawnie zweryfikowany. [web:109][web:105][web:116]

## 3. Czego nie obiecywać

Nie należy projektować funkcji „blokowania negatywnych opinii” jako automatycznego usuwania dowolnych recenzji. W praktyce system może: wykryć naruszenie, zasugerować zgłoszenie, przygotować odpowiedź lub eskalację do człowieka. [web:109][web:105][web:112][web:116]

AI ma działać jako asystent odpowiedzi i triage, a nie jako autoryzacja do publikowania wszystkiego bez kontroli. [web:109][web:116]

## 4. Architektura wysokiego poziomu

Moduł powinien składać się z sześciu warstw:

1. **GBP Connector** — pobieranie lokalizacji, recenzji, postów i statusów odpowiedzi.
2. **Geo Grid Engine** — obliczanie pozycji w siatce 3x3 lub 5x5.
3. **Review Intelligence** — klasyfikacja opinii i generowanie draftów odpowiedzi.
4. **Optimization Tasks Engine** — lista działań GBP z priorytetem i wpływem.
5. **Competitor Scanner** — analiza konkurencji i porównanie pozycji.
6. **Orchestration / Storage** — n8n + baza danych + Streamlit UI. [web:105][web:106][web:108][web:115][web:119][cite:5][cite:19]

## 5. Proponowany stack

### Core
- **Streamlit** jako dashboard.
- **Python** jako backend.
- **SQLite** na MVP, potem **Postgres**.
- **n8n** jako orkiestrator automatyzacji.
- **Gemini 2.5 Flash / Pro** jako model do rekomendacji i podsumowań.

### Integracje
- **Google Business Profile API** jako źródło danych własnej wizytówki.
- **Composio** do akcji na zewnętrznych SaaS i przyszłych integracji agentowych.
- **Vertex AI** do klasyfikacji i generowania treści.

### Opcjonalnie
- **Open-source rank tracker** lub własny grid engine jako komponent pomocniczy.
- **Playwright** tylko jeśli trzeba pobierać publiczne dane pomocnicze z dynamicznych stron. [cite:5][cite:19][web:85][web:90][web:95][web:96][web:115][web:119][web:122][web:130]

## 6. Model danych

### Tabela `gbp_locations`
| Pole | Typ | Opis |
|---|---|---|
| `id` | string | ID lokalizacji |
| `business_name` | string | Nazwa firmy |
| `place_id` | string | ID miejsca Google |
| `address` | string | Adres |
| `city` | string | Miasto |
| `category` | string | Kategoria GBP |
| `website` | string | Strona www |
| `phone` | string | Telefon |
| `active` | bool | Czy aktywna |

### Tabela `gbp_reviews`
| Pole | Typ | Opis |
|---|---|---|
| `review_id` | string | ID opinii |
| `location_id` | string | Powiązanie z lokalizacją |
| `author_name` | string | Autor |
| `rating` | int | 1–5 |
| `review_text` | text | Treść opinii |
| `created_at` | datetime | Data publikacji |
| `reply_state` | string | `none`, `draft`, `pending`, `published`, `rejected` |
| `policy_flag` | string | `none`, `possible_violation`, `escalate` |

### Tabela `grid_snapshots`
| Pole | Typ | Opis |
|---|---|---|
| `snapshot_id` | string | ID pomiaru |
| `location_id` | string | Lokalizacja |
| `keyword` | string | Fraza, np. `stomatolog sopot` |
| `grid_type` | string | `3x3` / `5x5` |
| `cell_key` | string | Komórka siatki |
| `rank_position` | int | Pozycja |
| `lat` | float | Szerokość |
| `lng` | float | Długość |
| `captured_at` | datetime | Czas pomiaru |

### Tabela `optimization_tasks`
| Pole | Typ | Opis |
|---|---|---|
| `task_id` | string | ID zadania |
| `location_id` | string | Lokalizacja |
| `title` | string | Np. „Dodaj post pod frazę X” |
| `description` | text | Instrukcja |
| `impact_score` | int | Wpływ na widoczność |
| `difficulty_score` | int | Trudność |
| `status` | string | `todo`, `doing`, `done`, `blocked` |

### Tabela `reply_drafts`
| Pole | Typ | Opis |
|---|---|---|
| `draft_id` | string | ID draftu |
| `review_id` | string | Powiązanie z opinią |
| `model_name` | string | Gemini / DeepSeek-R1 |
| `draft_text` | text | Propozycja odpowiedzi |
| `tone` | string | empatyczny / profesjonalny / neutralny |
| `approved` | bool | Czy zaakceptowano |

## 7. GBP Connector

Connector powinien mieć warstwę adaptera, która najpierw korzysta z oficjalnego Google Business Profile API, a dopiero potem z alternatyw lub danych pomocniczych. [web:105][web:106][web:108]

Minimalne funkcje:
- `list_locations()`
- `get_reviews(location_id)`
- `get_review_reply_state(review_id)`
- `create_post(location_id, content)`
- `reply_to_review(review_id, text)`
- `sync_location_metrics(location_id)` [web:105][web:106][web:108][web:109]

## 8. Geo Grid Engine

Silnik siatki powinien generować punkty wokół lokalizacji w schemacie 3x3 lub 5x5, przypisywać im współrzędne oraz wykonywać pomiar pozycji dla jednej lub wielu fraz. [web:115][web:119]

Dla MVP wystarczy:
- prosty generator punktów wokół centrum miasta,
- adapter do rank trackera,
- zapis wyniku do `grid_snapshots`,
- render kolorowej mapy w Streamlit. [web:115][web:119][web:122][web:130]

## 9. Review Intelligence

Proces opinii powinien wyglądać tak:
1. Pobierz nową opinię.
2. Klasyfikuj sentyment i potencjalne naruszenia.
3. Wygeneruj draft odpowiedzi.
4. Pokaż w dashboardzie status: `draft`, `pending`, `approved`.
5. Po akceptacji opublikuj przez API. [web:109][web:105][web:112][web:116]

To jest bezpieczniejsze niż pełna automatyzacja bez akceptacji, bo Google moderuje odpowiedzi i ma własne zasady dla treści. [web:105][web:109][web:116]

## 10. Optimization Tasks Engine

System powinien generować zadania optymalizacyjne w stylu Localo:
- dodaj post pod konkretną frazę,
- dopisz usługę do GBP,
- uzupełnij opis i kategorie,
- odpowiedz na recenzję,
- dodaj zdjęcia,
- popraw sekcję Q&A,
- zaktualizuj dane kontaktowe.

Każde zadanie ma mieć `impact_score`, `difficulty_score`, `time_estimate` i `reason`. [web:115][web:119]

## 11. Competitor Scanner

Konkurencję trzeba skanować w warstwach:
- pozycja w gridzie,
- liczba i tempo nowych opinii,
- aktywność postów,
- kategorie i usługi,
- sygnały z publicznych stron WWW. [web:115][web:119][web:118]

Nie należy polegać tylko na jednym źródle, bo lokalne SEO to miks sygnałów z profilu, strony i mapy. [web:115][web:119]

## 12. Streamlit layout

### Zakładka 1: Skaner Wizytówek Google
- wykres grid 3x3,
- ranking pozycji,
- zmiana pozycji w czasie,
- alerty o spadkach.

### Zakładka 2: Menedżer Opinii
- lista nowych opinii,
- filtrowanie po ratingu,
- draft odpowiedzi,
- akceptacja i publikacja,
- flaga naruszeń.

### Zakładka 3: Zadania GBP
- lista kroków optymalizacyjnych,
- sortowanie po wpływie,
- status realizacji,
- instrukcje dla użytkownika.

### Zakładka 4: Konkurencja
- porównanie siatek,
- benchmark recenzji,
- różnice w aktywności,
- export raportu PDF/CSV. [web:115][web:119][cite:5]

## 13. n8n workflows

n8n powinien obsłużyć:
- cron: pobranie nowych opinii,
- cron: pomiar pozycji w gridzie,
- webhook: nowa opinia -> AI draft,
- webhook: akceptacja -> publikacja odpowiedzi,
- cron: tygodniowy raport optymalizacyjny,
- cron: alert konkurencyjny. [cite:5][cite:19]

## 14. Integracja z Composio

Composio warto włączyć jako warstwę integracji tam, gdzie agent ma działać na SaaS-ach obok GBP, np. Google Search, LinkedIn, Gmail czy inne narzędzia operacyjne. [web:85][web:90][web:95][web:96][web:97]

Dla samego GBP lepiej trzymać się oficjalnego API Google, a Composio zostawić dla komunikacji, discovery i akcji pobocznych. [web:105][web:108][web:109]

## 15. MVP roadmap

### Etap 1
- GBP connector dla własnej wizytówki,
- recenzje,
- draft odpowiedzi,
- zapis do SQLite,
- prosty widok Streamlit. [web:105][web:109][cite:5]

### Etap 2
- grid map,
- historie pozycji,
- task engine,
- eksport CSV/PDF. [web:115][web:119]

### Etap 3
- n8n automations,
- competitor scanning,
- AI recommendation layer,
- webhook approvals. [cite:5][cite:19]

### Etap 4
- Composio integrations,
- ranking comparison,
- multi-location support,
- agency mode dla klientów J(AI)SON. [web:85][web:90][web:95][web:96]

## 16. Decyzje wdrożeniowe

Najlepszy low-cost stack to:
- Google Business Profile API,
- Streamlit,
- n8n,
- Gemini 2.5 Flash,
- SQLite/Postgres,
- opcjonalnie Composio,
- opcjonalnie open-source local rank tracker jako komponent pomocniczy. [web:105][web:108][web:115][web:119][web:122][web:130][cite:5][cite:19]

Nie warto próbować odtworzyć całego Localo jako open-source clone. Lepiej zbudować wąski, szybki, zaufany moduł, który robi 80% pracy przy 20% kosztu. [web:115][web:118][web:119]
