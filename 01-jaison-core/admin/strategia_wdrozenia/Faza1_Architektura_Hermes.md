# **Raport Techniczny: Architektura Techniczna i Wtyczki Hermes OS (Faza 1)**

Jako Główny Strateg Technologiczny i Architekt AI w projekcie "Holistic A(I)DHD Agentic OS", przeanalizowałem wymagania dotyczące wdrożenia frameworka Nous Research Hermes Agent na maszynie GCP, w połączeniu z interfejsem Streamlit i architekturą chmurową Google Cloud. Poniżej znajduje się szczegółowy projekt techniczny rozwiązujący problemy ze strukturą wtyczek, blokadami bazy SQLite oraz optymalizacją kosztów GCS w modelu wielodostępnym (Multi-tenancy).

---

### 1. Struktura folderów i szablon wtyczki Hermes OS

Zgodnie z oficjalną architekturą frameworka Hermes, wtyczki (Plugins) służą do rozszerzania natywnych możliwości systemu o nowe narzędzia, punkty zaczepienia cyklu życia (hooks) i komendy bez konieczności modyfikowania rdzenia systemu. Aby mechanizm wykrywania wtyczek (`PluginManager`) poprawnie zarejestrował Twoje rozszerzenie, należy umieścić je w katalogu `~/.hermes/plugins/` i zachować rygorystyczny podział na pliki.

**Dokładna struktura katalogów dla nowej wtyczki (np. `custom-agency-plugin`):**
```text
~/.hermes/plugins/custom-agency-plugin/
├── plugin.yaml       # Manifest deklarujący metadane, narzędzia i zmienne środowiskowe
├── __init__.py       # Punkt wejścia inicjalizujący rejestrację poprzez register(ctx)
├── schemas.py        # Definicje schematów JSON narzędzi widocznych dla LLM
└── tools.py          # Implementacja funkcji wykonawczych (handlers) w języku Python
```

#### Szablony kodu wtyczki

**1. Manifest `plugin.yaml`**
Plik ten jest kluczowy dla mechanizmu wykrywania i pre-flight weryfikacji. Musi bezwzględnie deklarować `requires_env` dla zmiennych zawierających klucze API, w przeciwnym razie system nie ostrzeże o braku wymaganych tokenów.
```yaml
name: custom-agency-plugin
version: "1.0.0"
description: Niestandardowa wtyczka dla Holistic Agentic OS dodająca funkcje agencyjne.
kind: standalone
provides_tools:
  - holistic_tool
provides_hooks:
  - post_tool_call
requires_env:
  - AGENCY_API_KEY
```

**2. Definicja schematów `schemas.py`**
Schemat pozwala LLM zrozumieć, jak i kiedy użyć narzędzia. Opis musi być bardzo precyzyjny.
```python
HOLISTIC_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "holistic_tool",
        "description": "Wykonuje wyspecjalizowane zadanie dla Holistic Agentic OS.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_name": {
                    "type": "string",
                    "description": "Nazwa zadania do wykonania."
                }
            },
            "required": ["task_name"]
        }
    }
}
```

**3. Funkcje wykonawcze `tools.py`**
Zgodnie ze specyfikacją Hermes, tzw. handlers **muszą zawsze zwracać ciąg znaków JSON**, przechwytywać wszelkie wyjątki i akceptować parametr `**kwargs` dla przyszłej kompatybilności.
```python
import json

def handle_holistic_tool(args: dict, **kwargs) -> str:
    try:
        task_name = args.get("task_name", "unknown")
        # Miejsce na logikę narzędzia
        result = {"status": "success", "executed_task": task_name}
        return json.dumps(result)
    except Exception as e:
        # Nigdy nie zgłaszaj wyjątków (raise) - zwracaj błędy jako JSON
        return json.dumps({"error": str(e)})
```

**4. Inicjalizacja `__init__.py`**
Plik ten łączy schematy z logiką wykonawczą i rejestruje je w systemie agenta przy użyciu metody `ctx.register_tool()`.
```python
from .schemas import HOLISTIC_TOOL_SCHEMA
from .tools import handle_holistic_tool

def log_tool_call(event_name: str, payload: dict, **kwargs):
    print(f"[Holistic OS] Hook uruchomiony: {event_name}")

def register(ctx):
    # Rejestracja narzędzia w systemie
    ctx.register_tool(
        name="holistic_tool",
        toolset="agency_tools",
        schema=HOLISTIC_TOOL_SCHEMA,
        handler=handle_holistic_tool
    )
    # Rejestracja punktu zaczepienia (hook)
    ctx.register_hook("post_tool_call", log_tool_call)
```

---

### 2. Konfiguracja SQLite (tryb WAL) dla wielowątkowości w Streamlit

Praca w architekturze agentowej w środowisku Streamlit generuje ryzyko konfliktów wyścigów (race conditions) oraz błędów `database is locked`, gdy wielu sub-agentów (np. CEO, CMO, CTO) próbuje asynchronicznie odczytywać i zapisywać stan w lokalnej bazie. We frameworku Hermes, szczególnie przy szybkim, równoległym tworzeniu zadań (np. w Kanban DB), tego typu zderzenia mogą prowadzić do błędów blokowania lub nawet uszkodzenia danych.

Rozwiązaniem jest zastosowanie w bazie danych SQLite mechanizmu Write-Ahead Logging (WAL), co pozwala na nieblokujące współbieżne czytanie przez wielu agentów oraz precyzyjny ustawienie pragm chroniących przed przerwaniem transakcji (torn-write).

Aby optymalnie skonfigurować bazę danych dla wielowątkowego środowiska Streamlit, użyj dekoratora `@st.cache_resource`, który gwarantuje, że pula połączeń do bazy zostanie zainicjowana tylko raz dla instancji aplikacji.

**Wzorzec połączenia z bezpieczną konfiguracją SQLite:**
```python
import sqlite3
import streamlit as st

@st.cache_resource
def get_db_connection(db_path: str):
    # Inicjalizacja współdzielonego połączenia z bazą SQLite
    conn = sqlite3.connect(db_path, check_same_thread=False)
    
    # Wyegzekwowanie trybu WAL i rygorystycznych reguł bezpieczeństwa dla współbieżności
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=FULL;")          # Ochrona b-tree przed przerwaniem zapisu (torn write)
    conn.execute("PRAGMA wal_autocheckpoint=100;")    # Częstsze zrzuty (checkpoints) zmniejszają długość WAL
    conn.execute("PRAGMA secure_delete=ON;")          # Zerowanie usuniętych stron dla bezpieczeństwa
    conn.execute("PRAGMA cell_size_check=ON;")        # Natychmiastowe wykrywanie uszkodzonych wierszy bazy
    conn.execute("PRAGMA busy_timeout=5000;")         # Czekanie 5 sekund w przypadku nałożenia się zapisów
    
    return conn

# W kodzie Streamlit użycie:
# db = get_db_connection("~/.hermes/mnemosyne/data/mnemosyne.db")
```
Dzięki parametryzacji `busy_timeout` agent poczeka do 5000 milisekund na zwolnienie blokady zapisu, co praktycznie całkowicie wyeliminuje komunikat `database is locked` w asynchronicznym środowisku.

---

### 3. Architektura Multi-tenancy i podział GCS (Low-Cost Partitioning)

Tworzenie dla każdego klienta (np. profil "Agencja Jason" vs "Nieruchomości") odrębnych zasobników (bucketów) lub zaawansowanych instancji w chmurze spowodowałoby znaczny przyrost kosztów i zapytań o przekroczenie limitów (Quotas). Framework Hermes z definicji nie posiada wbudowanych mechanizmów multi-tenancy. 

Najtańszym i najprostszym (low-cost) podejściem jest **logiczna separacja zasobów z wykorzystaniem jednego bucketu bazowego GCS podzielonego na foldery (prefiksy)**. 

Zamiast budować jeden gigantyczny RAG mieszający dane, Bucket `gs://holistic_kubelek` powinien zostać fizycznie podzielony na foldery takie jak `silos-ceo/`, `silos-cmo/`, i `silos-cto/`. W ten sposób zapobiegamy tzw. "wylewaniu się" danych i halucynacjom modeli (np. agent programistyczny z `silos-cto` ma odcięty dostęp do instrukcji dotyczących marketingu klienta nieruchomości z `silos-cmo`).

Izolacja agentów w systemie Hermes odbywa się przez parametryzację ścieżki środowiskowej `HERMES_HOME`, co uniemożliwia poszczególnym profilom wyjście poza swój katalog roboczy. W Streamlicie kluczem do mapowania jest wykorzystanie zmiennej stanowej `st.session_state.active_profile`, aby na żywo przypisywać konkretne identyfikatory Data Store i prefiksy GCS do operacji.

**Szablon konfiguracji i dynamicznego routingu GCS w Pythonie:**
```python
import streamlit as st

def get_current_tenant_config():
    """
    Mapuje aktywny profil w Streamlit na odizolowaną ścieżkę GCS i Data Store.
    """
    # Domyślny profil w przypadku braku wyboru
    active_profile = st.session_state.get("active_profile", "default_agency")
    
    # Słownik multi-tenancy mapujący profil na dedykowane, tanie silosy w jednym buckecie
    tenant_mapping = {
        "Holistic Broker": {
            "gcs_prefix": "gs://holistic_kubelek/silos-broker/",
            "data_store_id": "ds-broker-realestate",
            "hermes_home": "/opt/holistic_os/profiles/broker"
        },
        "Agencja Jason": {
            "gcs_prefix": "gs://holistic_kubelek/silos-agency/",
            "data_store_id": "ds-agency-marketing",
            "hermes_home": "/opt/holistic_os/profiles/agency"
        },
        "default_agency": {
            "gcs_prefix": "gs://holistic_kubelek/silos-default/",
            "data_store_id": "ds-default",
            "hermes_home": "/opt/holistic_os/profiles/default"
        }
    }
    
    return tenant_mapping.get(active_profile, tenant_mapping["default_agency"])

# Przykład użycia przy odpytywaniu lub zmianie kontekstu:
# tenant_config = get_current_tenant_config()
# os.environ["HERMES_HOME"] = tenant_config["hermes_home"]
# print(f"Agent połączony z bezpiecznym silosem: {tenant_config['gcs_prefix']}")
```
Takie rozwiązanie pozwala na wykorzystywanie do woli tańszych tokenów w izolowanych przestrzeniach dla dowolnej liczby profili. Koszt GCS pozostaje ten sam, a precyzyjne odpytywanie wyszukiwarki Vertex AI w locie dla konkretnego pre-fiksu minimalizuje użycie okna kontekstowego modelu i zapewnia wysoką celność wyników (Top-K). Dodatkowo podział ten doskonale komponuje się z "C-Level Board", zapobiegając informacyjnemu przestymulowaniu charakterystycznemu dla środowisk pracy niedostosowanych do osób neuroatypowych.
