# E2E Test Suite Ready

This document outlines the test runner details, the coverage summary, and the verification checklist for the entire 49-case test suite covering all 38 core E2E and unit test cases and additional verification tests.

## Test Runner

To execute the test suite locally in the project root:

```powershell
python -m pytest tests/
```

### Verification Execution Log Snippet
When executed successfully, the test run produces the following output:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Aplikacje MVP\Holistic Jason
plugins: anyio-4.13.0, mock-3.15.1
collected 49 items

tests\test_f1_ui.py ........s...                                         [ 24%]
tests\test_f2_webhook.py ..........                                      [ 44%]
tests\test_f3_rag.py ..........                                          [ 65%]
tests\test_milestone2_adversarial.py ....                                [ 73%]
tests\test_scenarios.py ........                                         [ 89%]
tests\test_skills_consolidation.py ...                                   [ 95%]
tests\test_sync_script.py ..                                             [100%]

============================== warnings summary ===============================
.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Aplikacje MVP\Holistic Jason\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================== 48 passed, 1 skipped, 1 warning in 48.59s ==================
```

> **Note on skipped test:** `test_tc09_multi_page_navigation` is skipped automatically on Windows environments due to Streamlit `AppTest` concurrent execution limits on the OS, preventing execution timeouts.

---

## Coverage Summary

| Feature / Module | Test File | Target Code File | Mapped Core Cases | Total Test Cases | Passed | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **F1: Streamlit UI & Zen Mode** | `tests/test_f1_ui.py` | `app.py` | TC-01 to TC-10 | 12 | 11 (1 skipped) | Passed/Skipped |
| **F2: Webhook & Systeme.io** | `tests/test_f2_webhook.py` | `webhook_api.py` | TC-11 to TC-20 | 10 | 10 | Passed |
| **F3: Dual-Mode RAG Routing** | `tests/test_f3_rag.py` | `01_src/knowledge.py` | TC-21 to TC-30 | 10 | 10 | Passed |
| **F4: Real-World Scenarios** | `tests/test_scenarios.py` | Multi-module | TC-31 to TC-38 | 8 | 8 | Passed |
| **Extra: UI Adversarial** | `tests/test_milestone2_adversarial.py` | `app.py` | N/A | 4 | 4 | Passed |
| **Extra: Skills Validation** | `tests/test_skills_consolidation.py` | `skills/` | N/A | 3 | 3 | Passed |
| **Extra: GCP Sync Script** | `tests/test_sync_script.py` | `scratch/sync_to_gcp.py` | N/A | 2 | 2 | Passed |
| **Total** | | | **38 Core Cases** | **49** | **48 (1 skipped)** | **Passed** |

---

## Feature Checklist

| Case ID | Feature / Tier | Short Description | Target Test Function | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | F1 / Tier 1 | Sidebar navigation between pages | `test_tc01_sidebar_navigation` | ✅ Passed |
| **TC-02** | F1 / Tier 1 | Mission Control rendering check | `test_tc02_mission_control_rendering` | ✅ Passed |
| **TC-03** | F1 / Tier 1 | Baza Wiedzy rendering check | `test_tc03_baza_wiedzy_rendering` | ✅ Passed |
| **TC-04** | F1 / Tier 1 | Agent Consoles rendering check | `test_tc04_agent_consoles_rendering` | ✅ Passed |
| **TC-05** | F1 / Tier 2 | Zen Mode (One Thing) empty input handling | `test_tc05_one_thing_empty` | ✅ Passed |
| **TC-06** | F1 / Tier 2 | Zen Mode (One Thing) long input boundary | `test_tc06_one_thing_long` | ✅ Passed |
| **TC-07** | F1 / Tier 3 | Zen Mode state persistence | `test_tc07_one_thing_state_persistence` | ✅ Passed |
| **TC-08** | F1 / Tier 3 | Zen Mode navigation persistence | `test_tc08_one_thing_navigation_persistence` | ✅ Passed |
| **TC-09** | F1 / Tier 4 | Multi-page navigation workflow | `test_tc09_multi_page_navigation` | ⚠️ Skipped (Windows) |
| **TC-10** | F1 / Tier 4 | Pomodoro / Zen Mode workflow | `test_tc10_one_thing_flow` | ✅ Passed |
| **TC-11** | F2 / Tier 1 | Lead "broker" maps to "Leady_Broker!A:G" | `test_tc11_broker_lead_sheets_range` | ✅ Passed |
| **TC-12** | F2 / Tier 1 | Lead "jason" maps to "Leady_Jason_B2B!A:G" | `test_tc12_jason_lead_sheets_range` | ✅ Passed |
| **TC-13** | F2 / Tier 2 | Missing required fields API response (422) | `test_tc13_missing_required_fields` | ✅ Passed |
| **TC-14** | F2 / Tier 2 | Empty contact field validation | `test_tc14_empty_contact_field` | ✅ Passed |
| **TC-15** | F2 / Tier 3 | Forwarding to Systeme.io webhook when set | `test_tc15_forward_webhook_only` | ✅ Passed |
| **TC-16** | F2 / Tier 3 | Forwarding to Systeme.io API when set | `test_tc16_forward_api_only` | ✅ Passed |
| **TC-17** | F2 / Tier 3 | Forwarding to both webhook and API when set | `test_tc17_forward_both` | ✅ Passed |
| **TC-18** | F2 / Tier 3 | Forwarding when neither is set | `test_tc18_forward_neither` | ✅ Passed |
| **TC-19** | F2 / Tier 4 | Webhook success flow with Google Sheets | `test_tc19_webhook_success_flow` | ✅ Passed |
| **TC-20** | F2 / Tier 4 | Webhook Google Sheets API failure resilience | `test_tc20_sheets_api_failure_graceful` | ✅ Passed |
| **TC-21** | F3 / Tier 1 | Route query "brain dump" to local Obsidian | `test_tc21_route_brain_dump` | ✅ Passed |
| **TC-22** | F3 / Tier 1 | Route query "notatki" to local Obsidian | `test_tc22_route_notatki` | ✅ Passed |
| **TC-23** | F3 / Tier 1 | Route standard query to Vertex AI Search | `test_tc23_route_standard_gcs` | ✅ Passed |
| **TC-24** | F3 / Tier 2 | Empty query routing defaults to cloud | `test_tc24_empty_query_routing` | ✅ Passed |
| **TC-25** | F3 / Tier 2 | Mixed keywords routing correctness | `test_tc25_mixed_keywords_routing` | ✅ Passed |
| **TC-26** | F3 / Tier 2 | Empty local Obsidian directory search | `test_tc26_local_search_empty_dir` | ✅ Passed |
| **TC-27** | F3 / Tier 3 | Obsidian file search success with snippet | `test_tc27_local_search_success_verbatim` | ✅ Passed |
| **TC-28** | F3 / Tier 3 | Obsidian multi-word keywords search | `test_tc28_local_search_keywords_fallback` | ✅ Passed |
| **TC-29** | F3 / Tier 4 | Mock GCS / Vertex AI search structured answers | `test_tc29_vertex_ai_search_snippets` | ✅ Passed |
| **TC-30** | F3 / Tier 4 | GCS/Vertex AI auth error fallback handling | `test_tc30_vertex_ai_auth_error` | ✅ Passed |
| **TC-31** | F4 / Tier 4 | E2E Lead webhook to Sheets and Systeme.io | `test_tc31_e2e_lead_webhook_flow` | ✅ Passed |
| **TC-32** | F4 / Tier 4 | E2E Knowledge Sync to local vault and RAG | `test_tc32_e2e_knowledge_sync_flow` | ✅ Passed |
| **TC-33** | F4 / Tier 4 | Local saving resilience on GCS sync failure | `test_tc33_gcs_sync_resilience` | ✅ Passed |
| **TC-34** | F4 / Tier 4 | Webhook validation rejects malformed requests | `test_tc34_malformed_webhook_fails_early` | ✅ Passed |
| **TC-35** | F4 / Tier 4 | Brain Dump REST API note creation and RAG | `test_tc35_brain_dump_api_to_rag` | ✅ Passed |
| **TC-36** | F4 / Tier 4 | RAG cloud GCS SSL error fallback handling | `test_tc36_cloud_ssl_error_fallback` | ✅ Passed |
| **TC-37** | F4 / Tier 4 | Tryb "One Thing" session state isolation | `test_tc37_one_thing_state_isolation` | ✅ Passed |
| **TC-38** | F4 / Tier 4 | Comprehensive E2E system integration flow | `test_tc38_comprehensive_e2e_scenario` | ✅ Passed |
