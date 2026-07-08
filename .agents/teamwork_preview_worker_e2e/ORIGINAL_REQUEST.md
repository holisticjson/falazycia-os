## 2026-06-19T16:54:36Z

<USER_REQUEST>
You are the Worker agent for the E2E Testing Track.
Your working directory is: c:\Aplikacje MVP\Holistic Jason\.agents\teamwork_preview_worker_e2e\

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your tasks:
1. Initialize briefing.md and progress.md in your working directory.
2. Unify the Obsidian Vault path inconsistency across app.py, 01_src/knowledge.py, and brain_dump_api.py. Make them use a consistent directory (e.g. os.path.join(os.getcwd(), "Obsidian_Vault") or configured via a central environment variable).
3. Implement the missing features so that the E2E tests can run and pass:
   - F2: Add lead webhook forwarding to Systeme.io in `webhook_api.py` (when a lead comes in, forward it to Systeme.io endpoint/webhook if `SYSTEME_IO_API_KEY` or `SYSTEME_IO_WEBHOOK_URL` is set, or mock it properly. The user rule says: "BEZWZGLĘDNY ZAKAZ proponowania budowy własnego systemu mailingowego i lejków od zera! Użytkownik wyraźnie nakazał używać darmowego planu Systeme.io (do 2000 kontaktów)... Agenci mają z nim współpracować, a nie go zastępować.").
   - F3: Implement the dual-mode RAG query routing logic `query_dual_knowledge_base(query: str, data_store_id: str = None) -> dict` in `01_src/knowledge.py` using keyword-based classification (GCS vs Brain dump) and local note searching in Obsidian_Vault for Brain dump, as recommended by the explorer.
4. Create `TEST_INFRA.md` at the project root following the 4-tier approach (Category-Partition, BVA, Pairwise Combinatorial, and Real-World Workload). Ensure it maps all 38 planned test cases (TC-01 through TC-38).
5. Implement the 38 pytest test cases in a new directory `tests/` at the project root:
   - `tests/test_f1_ui.py`: Use Streamlit's `AppTest` to verify sidebar navigation, pages rendering (Mission Control, Baza Wiedzy, agent consoles), and Tryb "One Thing" (Zen Mode) text inputs and session state logic.
   - `tests/test_f2_webhook.py`: Use FastAPI's `TestClient` to verify the lead webhook API. Use unittest.mock to mock the Google Sheets API append calls and Systeme.io webhook requests so that the tests do not require real API keys or credentials and run successfully offline/locally.
   - `tests/test_f3_rag.py`: Verify GCS vs Brain dump classification and query routing. Mock `query_vertex_ai_search` using unittest.mock to make it deterministic. Test local Obsidian vault search with actual temp markdown files created/deleted during the test teardown.
   - `tests/test_scenarios.py`: Test the cross-feature and real-world scenarios (TC-31 to TC-38) with proper mocking.
6. Run the test suite using `pytest tests/` (or via a script) to verify that all 38 test cases pass successfully. Show the test execution command and output in your report.
7. Create `TEST_READY.md` at the project root outlining the test runner command and the 4-tier coverage checklist.
8. Write a detailed handoff report (handoff.md) in your working directory.

</USER_REQUEST>
