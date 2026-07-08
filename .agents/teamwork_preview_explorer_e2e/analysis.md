# E2E Test Suite Design & Codebase Analysis Report

This report provides a detailed analysis of the main application subsystems (F1, F2, F3) for the **Holistic AIDHD OS** and proposes a comprehensive 38-case test suite across 4 tiers.

---

## 1. Architectural Analysis of Subsystems

### F1: Streamlit Sidebar Navigation and Page Rendering
*   **Location**: `app.py`
*   **State Management**: Navigation is fully controlled via `st.session_state.current_page` (defaulting to `"🎯 Mission Control"`). 
*   **Navigation Mechanism**: The sidebar renders buttons dynamically using the `nav_button(label, page_name)` helper. Clicking a button updates `st.session_state.current_page` and executes `st.rerun()` to force page re-rendering.
*   **Tryb "One Thing" (Zen Mode)**: 
    *   Linked to `st.session_state.one_thing` and input box `thing = st.text_input(...)`.
    *   If set, it renders a custom styled HTML card: `🔥 Twój aktualny priorytet: [thing]` and displays a Pomodoro button.
    *   *Limitation*: Currently, "One Thing" mode displays a banner, but does *not* actually hide or filter out other UI elements (the "reducing cognitive load" is purely visual/mental rather than layout-enforced).
*   **Routing Logic**: A big `if/elif` block at the bottom of `app.py` routes the active `st.session_state.current_page` to render specific screens (e.g., `🎯 Mission Control`, `Baza Wiedzy (Vertex AI)`, individual agent consoles like `Claude` or `Antigravity`, and business modules).

### F2: Lead Webhook API
*   **Location**: `webhook_api.py`
*   **Framework**: FastAPI server running on port `8000`.
*   **Payload Schema**: `LeadPayload` Pydantic model requires:
    *   `project` ("broker" or "jason")
    *   `name`, `contact`
    *   Optional fields: `budget`, `investment_type`, `industry`, `problem`, `source` (defaults to `"Website Form"`).
*   **Sheet Routing Logic**:
    *   If `project.lower() == "broker"`, appends to `"Leady_Broker!A:G"` using columns: `[timestamp, name, contact, budget, investment_type, "NOWY", source]`.
    *   Otherwise (defaulting to Jason B2B), appends to `"Leady_Jason_B2B!A:G"` using columns: `[timestamp, name, contact, industry, problem, "NOWY", source]`.
*   **Missing Integration Alert**: Currently, `webhook_api.py` has **no code** for forwarding leads to **Systeme.io**. It only appends to Google Sheets. The Systeme.io integration needs to be added (e.g., using `SYSTEME_IO_API_KEY` to forward via HTTP requests, or mocked in the test suite).

### F3: Dual RAG Querying
*   **Location**: `01_src/knowledge.py`
*   **Vertex AI Search**: `query_vertex_ai_search` obtains Google credentials, uses a session-level SSL bypass to avoid local CA certificate verification issues, sends a POST request to Vertex Discovery Engine, and parses answer texts and snippets.
*   **Interface Contract**: The contract in `PROJECT.md` specifies `query_dual_knowledge_base(query: str, data_store_id: str) -> dict` returning `{"source": "gcs" | "brain_dump", "answer": str}`.
*   **Missing Implementation**: This router is not yet implemented in `01_src/knowledge.py`. It requires:
    1.  A classification rule (keywords or LLM-based) to decide if a query is factual (GCS) or creative/inspiration (Obsidian Brain Dump).
    2.  A local file search implementation to search `.md` files in the Obsidian Vault when routed to `brain_dump`.

---

## 2. Critical Findings & Inconsistencies
During the codebase investigation, we identified a **path inconsistency** for the Obsidian/Brain Dump directories across the three files:
1.  `app.py` defines `OBSIDIAN_DIR = os.path.join(BASE_DIR, "obsidian_vault")` where `BASE_DIR = ~/Agentic_OS`.
2.  `01_src/knowledge.py` defines `OBSIDIAN_DIR = os.path.join(os.getcwd(), "Obsidian_Vault")`.
3.  `brain_dump_api.py` defines `INBOX_DIR = r"C:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Inbox"`.

**Recommendation**: We must unify these paths in a shared configuration file or import them from a central system environment variable (e.g., `OBSIDIAN_VAULT_PATH`) to prevent component isolation.

---

## 3. Comprehensive E2E Test Suite (38 Cases)

The suite is designed following the 4-tier testing approach ($11 * 3 + \max(5, 3/2) = 38$ cases).

| Test ID | Tier | Feature | Input Data / Action | Expected Output / Verification Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Tier 1 | F1 | Click `Baza Wiedzy (Vertex AI)` sidebar button | `st.session_state.current_page` sets to `"Baza Wiedzy (Vertex AI)"`; UI renders search input. |
| **TC-02** | Tier 1 | F1 | Switch profile selectbox to `"Holistic Broker (Nieruchomości)"` | `st.session_state.active_profile` updates; CRM layout adapts to Broker sheets. |
| **TC-03** | Tier 1 | F1 | Input `"Napisz ofertę handlową"` into "One Thing" box | `st.session_state.one_thing` updates; "Twój aktualny priorytet" card is visible. |
| **TC-04** | Tier 1 | F1 | Load Mission Control dashboard home page | 6 status boxes (Claude, OpenClaw, Hermes, etc.) render with valid online/offline labels. |
| **TC-05** | Tier 1 | F1 | Click `Otwórz konsolę Claude` button on grid card | `st.session_state.current_page` updates to `"Claude"`; loads Chat and Control tabs. |
| **TC-06** | Tier 2 | F1 | Access app with uninitialized session state | Default state variables (`current_page`, `one_thing`, `pomodoro_active`) initialize without traceback. |
| **TC-07** | Tier 2 | F1 | Submit empty string to "One Thing" input box | Prioritization card and Pomodoro starter button are hidden from view. |
| **TC-08** | Tier 2 | F1 | Modify session state manually to an invalid page name | App defaults page rendering safely back to `"🎯 Mission Control"` instead of breaking. |
| **TC-09** | Tier 2 | F1 | Select a bucket with no files in Workspace tab | Displays clean "Skarbiec jest pusty" or fallback mock file listings. |
| **TC-10** | Tier 2 | F1 | Trigger file editor write error (read-only path) | st.error renders in the UI with a descriptive permission error message. |
| **TC-11** | Tier 1 | F2 | POST to `/api/lead` with `project="broker"`, valid details | Inserts row into `"Leady_Broker!A:G"`; returns HTTP 200 with success status. |
| **TC-12** | Tier 1 | F2 | POST to `/api/lead` with `project="jason"`, valid details | Inserts row into `"Leady_Jason_B2B!A:G"`; returns HTTP 200 with success status. |
| **TC-13** | Tier 1 | F2 | POST to `/api/lead` missing required `contact` field | FastAPI returns HTTP 422 Unprocessable Entity with validation details. |
| **TC-14** | Tier 1 | F2 | POST valid lead payload | API returns JSON: `{"status": "success", "message": "Lead zapisany poprawnie", "updatedCells": X}`. |
| **TC-15** | Tier 1 | F2 | POST lead payload omitting the optional `source` field | Database appends lead with the default source `"Website Form"`. |
| **TC-16** | Tier 2 | F2 | POST lead when `token_brokerholistic.pickle` is missing | API returns HTTP 500 with user-friendly instructions on running Google authentication. |
| **TC-17** | Tier 2 | F2 | POST lead with expired credentials | Token auto-refresh is invoked via refresh token; lead write succeeds. |
| **TC-18** | Tier 2 | F2 | POST lead when `GOOGLE_SHEET_ID_CRM` env is empty | API returns HTTP 500 indicating configuration parameter error. |
| **TC-19** | Tier 2 | F2 | POST lead containing Polish characters (`Zaźółć`) and emojis | Data appends to sheet correctly maintaining UTF-8 character encoding. |
| **TC-20** | Tier 2 | F2 | POST lead with unsupported project code (`project="other"`) | Webhook defaults to `"jason"`/Jason B2B sheet as a safe fallback. |
| **TC-21** | Tier 1 | F3 | Execute `query_vertex_ai_search("procedura wdrożenia")` | Performs OAuth request, queries Discovery Engine, returns parsed answer string. |
| **TC-22** | Tier 1 | F3 | Run `save_idea_to_obsidian_and_gcs("T: Test", "C")` | Writes local markdown file in `Obsidian_Vault` and executes GCS upload. |
| **TC-23** | Tier 1 | F3 | Execute `query_dual_knowledge_base` with a factual query | Routes to `gcs` source; returns answer from Vertex AI. |
| **TC-24** | Tier 1 | F3 | Execute `query_dual_knowledge_base` with an idea query | Routes to `brain_dump` source; searches local vault notes and returns snippets. |
| **TC-25** | Tier 1 | F3 | Save idea with non-ASCII title (e.g. `"Żółć pomysł"`) | Normalizes title (`Zolc_pomysl.md`), uploads to GCS with `text/plain` content type. |
| **TC-26** | Tier 2 | F3 | Query Vertex AI RAG with missing ADC credentials | Catches `DefaultCredentialsError` and returns step-by-step PowerShell authentication commands. |
| **TC-27** | Tier 2 | F3 | Query Vertex AI search causing local SSL verification failure | Triggers urllib3 SSL warning suppression, requests verify=False bypass, and completes call. |
| **TC-28** | Tier 2 | F3 | Query dual RAG with empty or whitespace string | Aborts routing early and returns "Wpisz zapytanie..." helper string. |
| **TC-29** | Tier 2 | F3 | Query dual RAG targeting missing `Obsidian_Vault` directory | Brain dump route executes safely returning "Baza notatek Obsidian jest pusta". |
| **TC-30** | Tier 2 | F3 | Query Vertex AI Search when Discovery Engine is down | API timeout/exception is caught; returns friendly service unavailable error. |
| **TC-31** | Tier 3 | F1+F2 | Submit lead via Streamlit CRM UI form | UI captures inputs, sends POST to webhook API, writes to sheet, and reports success in UI. |
| **TC-32** | Tier 3 | F2+F3 | Lead webhook receives new client info | Webhook writes to sheet, and automatically saves a markdown lead card in GCS/RAG inbox. |
| **TC-33** | Tier 3 | F1+F3 | Ask question in Streamlit Baza Wiedzy UI | Invokes dual query router; UI shows source tag `[GCS]` or `[Brain Dump]` with the answer. |
| **TC-34** | Tier 4 | Scenario | High-Ticket Lead flow simulation | Client posts lead to API -> sheets update -> Streamlit CRM tab refreshes with the new row. |
| **TC-35** | Tier 4 | Scenario | Voice Note ingestion & query flow | bot posts to `/api/dump` -> saved as md -> dual router retrieves the node contents. |
| **TC-36** | Tier 4 | Scenario | ADHD Focus Session workflow | Set "One Thing" -> Start Pomodoro -> Navigate pages -> Focus banner remains visible across tabs. |
| **TC-37** | Tier 4 | Scenario | Network/Credentials outage recovery | Network is disconnected -> GCS search fails -> App falls back to local Obsidian search + displays fix instructions. |
| **TC-38** | Tier 4 | Scenario | Multi-Tenant Profile Context Switch | Switch to "Broker" -> webhook routing targets Broker sheets; RAG query targets Broker data store. |

---

## 4. Testing Strategy Recommendations

### For F1: Streamlit AppTest vs Playwright
*   **Recommendation**: Use **Streamlit AppTest** (`streamlit.testing.v1.app_test.AppTest`) for local logic, sidebar navigation, and session state verification. Use **Playwright** for browser-side visuals (CSS, glassmorphism) and visual snapshot tests.
*   **Why AppTest?** It runs completely headless without spawning a browser, enabling lightning-fast test execution. It allows querying and interacting with widgets natively in python.
*   **Example AppTest Script**:
    ```python
    from streamlit.testing.v1 import AppTest

    def test_sidebar_navigation_and_one_thing():
        at = AppTest.from_file("app.py", default_timeout=10)
        at.run()
        
        # 1. Test session state defaults
        assert at.session_state["current_page"] == "🎯 Mission Control"
        assert at.session_state["one_thing"] == ""
        
        # 2. Test Tryb One Thing input
        # Note: at.text_input is indexed by order of appearance
        thing_input = at.text_input(key="one_thing_input") # or index
        thing_input.input("Implement E2E test suite").run()
        assert at.session_state["one_thing"] == "Implement E2E test suite"
        
        # 3. Test Navigation button click
        baza_wiedzy_btn = at.button(label="🧠 Baza Wiedzy (Vertex AI)")
        baza_wiedzy_btn.click().run()
        assert at.session_state["current_page"] == "Baza Wiedzy (Vertex AI)"
    ```

### For F2: FastAPI Webhook API Testing
*   **Recommendation**: Use `fastapi.testclient.TestClient` with `pytest`. Mock the Google Sheets service and verify the payload mappings. Include mock validation for Systeme.io.
*   **Example FastAPI Test Client with Mocks**:
    ```python
    import pytest
    from fastapi.testclient import TestClient
    from unittest.mock import MagicMock, patch
    from webhook_api import app

    client = TestClient(app)

    @patch("webhook_api.get_sheets_service")
    def test_receive_lead_broker(mock_get_sheets):
        # Mocking Google Sheets append chain
        mock_service = MagicMock()
        mock_get_sheets.return_value = mock_service
        mock_append = mock_service.spreadsheets().values().append()
        mock_append.execute.return_value = {"updates": {"updatedCells": 7}}

        payload = {
            "project": "broker",
            "name": "Jan Kowalski",
            "contact": "jan@kowalski.pl",
            "budget": "500000 PLN",
            "investment_type": "Mieszkanie",
            "source": "Landing Page"
        }
        
        response = client.post("/api/lead", json=payload)
        
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["updatedCells"] == 7
        
        # Verify right range is selected
        mock_service.spreadsheets().values().append.assert_called_with(
            spreadsheetId=pytest.any,
            range="Leady_Broker!A:G",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=pytest.any
        )
    ```

### For F3: Dual RAG Query Routing Test Strategy
Since `query_dual_knowledge_base` is defined only in the contract, we recommend:
1.  **Implementing the routing logic** directly in `01_src/knowledge.py` using keyword-based classification (highly performant and deterministic) combined with a local search mechanism for Obsidian Vault notes.
2.  **Mocking the external Discovery Engine** (`query_vertex_ai_search`) in test runs to bypass GCS authentication requirements during testing.

#### Proposed Implementation for `01_src/knowledge.py`:
```python
def search_obsidian_notes(query: str) -> str:
    """Przeszukuje lokalne notatki w Obsidian_Vault w poszukiwaniu dopasowań słów kluczowych."""
    notes_dir = os.path.join(os.getcwd(), "Obsidian_Vault")
    if not os.path.exists(notes_dir):
        return "Baza notatek Obsidian jest pusta (brak katalogu)."
    
    results = []
    keywords = [w.lower() for w in query.split() if len(w) > 3]
    if not keywords:
        keywords = [query.lower()]
        
    for root, _, files in os.walk(notes_dir):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        content_lower = content.lower()
                        score = sum(content_lower.count(kw) for kw in keywords)
                        if score > 0:
                            title = file
                            for line in content.split("\n"):
                                if line.startswith("title:"):
                                    title = line.replace("title:", "").strip().strip('"')
                                    break
                            results.append((score, title, content))
                except Exception:
                    pass
                    
    if not results:
        return "Nie znaleziono pasujących notatek w Twoim Skarbcu (Brain Dump)."
        
    results.sort(key=lambda x: x[0], reverse=True)
    best_results = results[:3]
    answer = "Znaleziono następujące notatki w Brain Dump:\n\n"
    for score, title, content in best_results:
        clean_content = content
        if "---" in content:
            parts = content.split("---", 2)
            if len(parts) >= 3:
                clean_content = parts[2].strip()
        snippet = clean_content[:300] + "..." if len(clean_content) > 300 else clean_content
        answer += f"### 📝 {title} (dopasowanie: {score})\n{snippet}\n\n"
        
    return answer

def query_dual_knowledge_base(query: str, data_store_id: str = None) -> dict:
    """
    Kieruje zapytanie do odpowiedniego źródła wiedzy:
    - gcs: twarde dane z GCP (Vertex AI Discovery Engine).
    - brain_dump: luźne pomysły z Obsidian_Vault.
    """
    brain_dump_keywords = [
        "pomysł", "idea", "inspiracja", "zrzut", "myśl", "notatka", 
        "brain dump", "kreatywn", "szybki zrzut", "luźne", "co zapisałem",
        "wymyśliłem", "notatki", "pomysły", "ideas", "thoughts", "dump"
    ]
    
    query_lower = query.lower()
    is_brain_dump = any(kw in query_lower for kw in brain_dump_keywords)
    
    if is_brain_dump:
        answer = search_obsidian_notes(query)
        return {"source": "brain_dump", "answer": answer}
    else:
        try:
            engine_id = data_store_id if data_store_id else "holistic-search-app_1780143991783"
            answer = query_vertex_ai_search(query, engine=engine_id)
            return {"source": "gcs", "answer": answer}
        except Exception as e:
            return {"source": "gcs", "answer": f"Błąd RAG (Vertex AI): {e}"}
```

#### Router Routing Test Case Example:
```python
import pytest
from unittest.mock import patch
from knowledge import query_dual_knowledge_base

def test_query_router_classification():
    # 1. Test query routed to Brain Dump
    with patch("knowledge.search_obsidian_notes") as mock_obsidian:
        mock_obsidian.return_value = "Mocked Obsidian Answer"
        res = query_dual_knowledge_base("mój nowy pomysł na biznes")
        assert res["source"] == "brain_dump"
        assert res["answer"] == "Mocked Obsidian Answer"
        mock_obsidian.assert_called_once()
        
    # 2. Test query routed to GCS
    with patch("knowledge.query_vertex_ai_search") as mock_gcs:
        mock_gcs.return_value = "Mocked Vertex Answer"
        res = query_dual_knowledge_base("jakie są warunki umowy?")
        assert res["source"] == "gcs"
        assert res["answer"] == "Mocked Vertex Answer"
        mock_gcs.assert_called_once_with("jakie są warunki umowy?", engine=pytest.any)
```
