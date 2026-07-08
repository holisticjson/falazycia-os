# Handoff Report — E2E Testing Track Explorer

**Role**: Explorer Agent (Read-only Investigation)
**Target Directory**: `c:\Aplikacje MVP\Holistic Jason\.agents\teamwork_preview_explorer_e2e\`
**Handoff Type**: Hard (Task Complete)

---

## 1. Observation

### Observation 1: Streamlit Sidebar Navigation and Page Rendering (`app.py`)
- **State Initialization** (`app.py` lines 1474-1479):
  ```python
  if "one_thing" not in st.session_state:
      st.session_state.one_thing = ""
  if "pomodoro_active" not in st.session_state:
      st.session_state.pomodoro_active = False
  if "current_page" not in st.session_state:
      st.session_state.current_page = "🎯 Mission Control"
  ```
- **Navigation Buttons** (`app.py` lines 1500-1503):
  ```python
  def nav_button(label, page_name):
      if st.button(label, use_container_width=True, type="primary" if col_menu == page_name else "secondary"):
          st.session_state.current_page = page_name
          st.rerun()
  ```
- **Tryb "One Thing" Input** (`app.py` lines 1921-1923):
  ```python
  thing = st.text_input("Moje jedyne zadanie na ten moment:", value=st.session_state.one_thing, placeholder="Np. zredagowanie oferty...")
  if thing:
      st.session_state.one_thing = thing
  ```

### Observation 2: FastAPI Lead Webhook API (`webhook_api.py`)
- **Lead Payload Schema & POST Endpoint** (`webhook_api.py` lines 30-38 & 49-50):
  ```python
  class LeadPayload(BaseModel):
      project: str # Wartość: "broker" or "jason"
      name: str
      ...
  @app.post("/api/lead")
  async def receive_lead(payload: LeadPayload):
  ```
- **Sheets Routing** (`webhook_api.py` lines 56-78):
  - If `payload.project.lower() == "broker"`, range is `"Leady_Broker!A:G"`.
  - Else, range is `"Leady_Jason_B2B!A:G"`.
- **Systeme.io Integration**: No active forwarding code exists in `webhook_api.py`.

### Observation 3: Path Inconsistencies for Obsidian / Brain Dump Vault
The workspace uses three different paths for the Obsidian Vault, which isolates the components:
1.  `app.py` line 31: `OBSIDIAN_DIR = os.path.join(BASE_DIR, "obsidian_vault")` where `BASE_DIR = ~/Agentic_OS`.
2.  `01_src/knowledge.py` line 6: `OBSIDIAN_DIR = os.path.join(os.getcwd(), "Obsidian_Vault")`.
3.  `brain_dump_api.py` line 21: `INBOX_DIR = os.getenv("OBSIDIAN_INBOX_PATH", r"C:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Inbox")`.

### Observation 4: Dual RAG Querying (`01_src/knowledge.py`)
- `query_vertex_ai_search` is fully implemented (lines 70-159) and handles GCP OAuth2 credentials with a verify=False SSL verification bypass.
- `query_dual_knowledge_base` is **not** implemented in `01_src/knowledge.py` despite being specified in `PROJECT.md` line 28:
  ```markdown
  - Function signature: `query_dual_knowledge_base(query: str, data_store_id: str) -> dict`
  - Output: `{"source": "gcs" | "brain_dump", "answer": str}`
  ```

---

## 2. Logic Chain

1.  **Sidebar & State Navigation (F1)**: Page routing is purely dependent on `st.session_state.current_page`. Therefore, E2E logic tests can be run headlessly using **Streamlit AppTest** to inspect `st.session_state` and click buttons without a browser. Visual/styling tests (glassmorphism cards) must be verified via **Playwright** because AppTest does not execute CSS layout engines.
2.  **API Data Integrity (F2)**: FastAPI TestClient will allow fast unit/integration testing. Because the sheets write depends on Google API credentials (`token_brokerholistic.pickle`), tests will fail in CI/CD without mocks. Thus, a mocked sheet service structure is required for deterministic checks. Furthermore, systeme.io webhook forwarding is missing from the source and must be mocked.
3.  **Directory Path Isolation**: If `brain_dump_api.py` writes to `Baza_Wiedzy\Inbox`, `app.py` reads/writes to `~/Agentic_OS/obsidian_vault`, and `knowledge.py` searches `Obsidian_Vault`, then RAG queries for "Brain Dump" will return empty results because they look in empty directories. Unifying directories is a logical prerequisite for E2E testing.
4.  **Dual RAG routing (F3)**: A query router classifier must evaluate the query. If a query contains creative, thought-based, or note-seeking keywords, it should search local markdown files (low cost, local). If it is a business/factual query, it should query GCS. Testing this routing mechanism is only possible by implementing the routing logic in `knowledge.py` or mocking the signature in tests. We choose to propose the actual implementation for the implementer and design mock assertions for tests to bypass live GCS auth requirements.

---

## 3. Caveats

- **External Services**: We cannot run live tests against Vertex AI Discovery Engine during automated testing because it requires valid GCP service accounts and OAuth tokens, which are not present in a local, offline sandbox or CI environment. Therefore, tests of RAG routing must mock the responses of `query_vertex_ai_search` to remain deterministic.
- **Systeme.io API**: We assume Systeme.io requires an API key (`SYSTEME_IO_API_KEY`) which is currently not present. Webhook tests will mock the forwarding post request.

---

## 4. Conclusion

The application code is functional but contains two major integration gaps:
1.  **Directory path inconsistencies** for Obsidian vault across `app.py`, `knowledge.py`, and `brain_dump_api.py`.
2.  **Missing lead forwarding to Systeme.io** in `webhook_api.py` and **missing routing implementation** `query_dual_knowledge_base` in `01_src/knowledge.py`.

We have designed a **38-case test suite** covering Feature Coverage, Boundaries, Cross-Feature Combinations, and Real-World Scenarios. We recommend using `streamlit.testing.v1.app_test` for UI logic and FastAPI's `TestClient` with mocks for Webhooks, combined with our proposed keyword-based routing implementation.

---

## 5. Verification Method

To verify the findings and design:
1.  **Check Path Inconsistencies**: Open `app.py` at line 31, `01_src/knowledge.py` at line 6, and `brain_dump_api.py` at line 21, and inspect the directories assigned to Obsidian/Inbox.
2.  **Verify Missing Implementations**: Search `01_src/knowledge.py` for the string `query_dual_knowledge_base` (it will return no results). Search `webhook_api.py` for `systeme` (it will return no results).
3.  **Test Run command**: Once the implementer implements the test files (e.g. `tests/test_ui.py`, `tests/test_webhook.py`, `tests/test_rag.py`), execute:
    ```powershell
    pytest tests/
    ```
