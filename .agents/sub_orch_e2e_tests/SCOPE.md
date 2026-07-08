# Scope: E2E Testing Track

## Architecture
- Streamlit application (`app.py`) for UI.
- FastAPI webhook API (`webhook_api.py`) for lead recording.
- Core knowledge module (`01_src/knowledge.py`) for GCS and Obsidian searching.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|---|---|---|---|
| 1 | Create Test Infrastructure Document | Write TEST_INFRA.md at the project root outlining Category-Partition, BVA, Pairwise, and Workload Testing. | None | PLANNED |
| 2 | Write Pytest Test Suite | Write pytest files in `tests/` covering all 38 test cases (F1, F2, F3) with proper mocks. | M1 | PLANNED |
| 3 | Execute & Verify Tests | Run `pytest tests/` using a worker, ensuring all 38 tests pass. | M2 | PLANNED |
| 4 | Publish TEST_READY.md | Create `TEST_READY.md` at the project root with the test command and coverage summary. | M3 | PLANNED |

## Interface Contracts
- **Streamlit page routing**: depends on `st.session_state.current_page` and sidebar actions.
- **FastAPI lead API**: POST `/api/lead` takes `LeadPayload` and writes to sheets / systeme.io.
- **Dual RAG Routing**: `query_dual_knowledge_base(query: str, data_store_id: str) -> dict`.
