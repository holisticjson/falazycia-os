# Scope: E2E Testing Track

## Architecture
- Streamlit UI tests using AppTest (`tests/test_f1_ui.py`)
- Lead Webhook API using FastAPI TestClient & mocks (`tests/test_f2_webhook.py`)
- RAG Routing tests (`tests/test_f3_rag.py`)
- Multi-step scenarios and resilience (`tests/test_scenarios.py`)

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Investigate and Verify | Verify existing tests run, identify failures | None | IN_PROGRESS (a78ca868-e573-494f-b9c1-f8394f5b6588) |
| 2 | Code & Fix Tests | Write/Fix any missing test cases in tests/ | M1 | PLANNED |
| 3 | Document and Publish | Write/Update TEST_INFRA.md and TEST_READY.md | M2 | PLANNED |
