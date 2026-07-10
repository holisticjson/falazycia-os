# E2E Test Infra: Holistic AIDHD OS

## Test Philosophy
The testing strategy for Holistic AIDHD OS is structured around a rigorous 4-Tier verification methodology to ensure the reliability of the system under different operational states, edge cases, and user workflows. We emphasize zero-hardcoding and verify real logic and states:

1. **Tier 1: Category-Partition** - Verifies functional partitioning of inputs, pages, and configurations.
2. **Tier 2: Boundary Value Analysis (BVA)** - Tests edge cases, empty/null inputs, long bounds, and missing credentials.
3. **Tier 3: Pairwise Combinatorial** - Checks combinations of inputs, configurations (Systeme.io credentials), and state persistence.
4. **Tier 4: Real-World Workload** - Tests user workflows, multi-step scenarios, and failure recoveries.

---

## Feature Inventory

| Feature ID & Name | Description | Target Code File | Test Cases (Tier 1 - Tier 3) |
| :--- | :--- | :--- | :--- |
| **F1: Streamlit UI & Zen Mode** | Sidebar navigation, rendering of Mission Control, Baza Wiedzy, Agent Consoles, and tryb "One Thing" (Zen Mode). | `app.py` | TC-01, TC-02, TC-03, TC-04 (Tier 1)<br>TC-05, TC-06 (Tier 2)<br>TC-07, TC-08 (Tier 3) |
| **F2: Lead Webhook API** | FastAPI webhook for submitting leads, writing to Google Sheets, forwarding to Systeme.io webhook and API. | `webhook_api.py` | TC-11, TC-12 (Tier 1)<br>TC-13, TC-14 (Tier 2)<br>TC-15, TC-16, TC-17, TC-18 (Tier 3) |
| **F3: Dual-Mode RAG Routing** | Routing queries containing keyword patterns to local Obsidian search, and standard queries to cloud GCS / Vertex AI Search. | `01_src/knowledge.py` | TC-21, TC-22, TC-23 (Tier 1)<br>TC-24, TC-25, TC-26 (Tier 2)<br>TC-27, TC-28 (Tier 3) |

---

## Test Architecture
The test infrastructure uses the following testing frameworks and practices to ensure high-fidelity testing:
- **Pytest Suite**: The core test runner.
- **Streamlit AppTest**: Simulates the Streamlit application execution and state transitions. Allows setting session state variables and checking rendering outputs.
- **FastAPI TestClient**: Tests FastAPI routes for webhooks (`webhook_api.py` and `brain_dump_api.py`).
- **Unittest Mocks**: Used extensively to isolate external dependencies (Google Sheets API, Google Cloud Storage, Vertex AI Search, and Systeme.io API).
- **Environment Isolation**: Patched environment variables and temporary folders are created for note saving (Obsidian Vault and Inbox folder) to prevent test contamination.

---

## Real-World Application Scenarios (Tier 4)

| Scenario ID & Name | Description | Target Test Function | Target File |
| :--- | :--- | :--- | :--- |
| **TC-09**: Multi-page navigation workflow | Multi-page transition flow: Mission Control -> Baza Wiedzy -> Agent Consoles -> Mission Control | `test_tc09_multi_page_navigation` | `tests/test_f1_ui.py` |
| **TC-10**: Pomodoro / Zen Mode workflow | Enter a "One Thing" task, update it, toggle Zen mode, and verify the display updates correctly | `test_tc10_one_thing_flow` | `tests/test_f1_ui.py` |
| **TC-19**: Webhook sheets flow | Webhook executes Google Sheets append call and finishes successfully under normal mock conditions | `test_tc19_webhook_success_flow` | `tests/test_f2_webhook.py` |
| **TC-20**: Webhook sheets error resilience | Webhook handles Google Sheets API errors gracefully by returning a 500 error but keeping logs clean | `test_tc20_sheets_api_failure_graceful` | `tests/test_f2_webhook.py` |
| **TC-29**: Cloud search snippets parsing | Mock GCS / Vertex AI search returns structured answers and formatted search result snippets | `test_tc29_vertex_ai_search_snippets` | `tests/test_f3_rag.py` |
| **TC-30**: Cloud search auth error resilience | GCS / Vertex AI search handles authentication/credentials error by displaying gcloud instruction message | `test_tc30_vertex_ai_auth_error` | `tests/test_f3_rag.py` |
| **TC-31**: E2E Webhook integration | Lead received -> saved to Google Sheets -> forwarded to Systeme.io webhook successfully | `test_tc31_e2e_lead_webhook_flow` | `tests/test_scenarios.py` |
| **TC-32**: E2E Knowledge Sync | Save a note via Streamlit knowledge flow -> verify it is written to the local vault -> execute a RAG query containing "notatki" to retrieve it | `test_tc32_e2e_knowledge_sync_flow` | `tests/test_scenarios.py` |
| **TC-33**: GCS Sync failure resilience | Save note -> mock GCS upload failure -> verify note is still saved locally and function returns success with warning | `test_tc33_gcs_sync_resilience` | `tests/test_scenarios.py` |
| **TC-34**: Webhook validation resilience | Malformed webhook request fails immediately before contacting Sheets or Systeme.io | `test_tc34_malformed_webhook_fails_early` | `tests/test_scenarios.py` |
| **TC-35**: Brain Dump REST API flow | POST `/api/dump` -> note created in Inbox -> query with "inbox" keyword retrieves the note | `test_tc35_brain_dump_api_to_rag` | `tests/test_scenarios.py` |
| **TC-36**: RAG Cloud SSL failure resilience | RAG search directed to GCS with mock SSL error is caught and converted to a user-friendly error message | `test_tc36_cloud_ssl_error_fallback` | `tests/test_scenarios.py` |
| **TC-37**: Zen Mode UI state isolation | Tryb "One Thing" UI state change doesn't interfere with or delete other session state keys | `test_tc37_one_thing_state_isolation` | `tests/test_scenarios.py` |
| **TC-38**: Comprehensive E2E system flow | User enters "One Thing" task, submits a lead, dumps a thought via Brain Dump API, and uses RAG search to verify | `test_tc38_comprehensive_e2e_scenario` | `tests/test_scenarios.py` |

---

## Coverage Thresholds
To ensure the highest reliability and standard of code quality, the following rules apply:
- **Core Coverage**: All 38 required test cases (TC-01 through TC-38) must be implemented and verified.
- **Pass Rate**: 100% pass rate for all executed tests.
- **Failures**: 0 allowed failures in the main test run.
- **Resilience Verification**: System failures (API exceptions, network/SSL issues, directory missing) must be gracefully handled and checked by dedicated test cases.
