# Handoff Report — Reviewer M2 1 (Gen 2)

## 1. Observation
- **Mentoring Tab**: `app.py` contains the `"🎯 Akademia.pl Mentoring"` tab starting on line 5939. It scans the `scratch/burnejko/` directory recursively for `.md` files, allows user selection, captures user inputs, calls `call_gemini_api` (with appropriate role instruction), and renders a copy-to-clipboard HTML/JS button.
- **Domena & Hosting Tab**: `app.py` contains `"Domena & Hosting"` on line 6044 with 4 tabs: 
  - `tab_cloud`: Mapowanie domen.
  - `tab_email`: Architektura E-mail.
  - `tab_automation`: Automatyzacja COMED (linked to `tasks/comed_browser_prompt.md`).
  - `tab_alternative`: Architektura Alternatywna (linked to `docs/alternative_architecture.md`).
- **Sync Script**: `scratch/sync_to_gcp.py` contains `get_newest_brain_dir()` (lines 25-39) which dynamically queries the latest modified directory in `C:\Users\tomas_yq1b9su\.gemini\antigravity\brain`. It also implements Option B profile isolation (lines 154-160) inside the SSH execution blocks.
- **Test execution**: Running `python -m pytest tests/` completed successfully with `43 passed, 1 skipped` (excluding the archive directory to prevent SystemExit issues).
- **API Key Misplacement**: In `app.py`, the "Zapisz klucze API" button (lines 6137-6166) is placed inside `tab_email` (under `menu == "Domena & Hosting"`). This button references `tavily_key`, `serper_key`, `hunter_key`, `reddit_id`, and `reddit_secret` which are only defined on lines 5933-5937 inside `tab_settings` (under `menu == "Prospecting Hub"`).

---

## 2. Logic Chain
- When a user navigates to `"Domena & Hosting"`, the `"Prospecting Hub"` page is not rendered. This means `tavily_key`, `serper_key`, and other settings inputs are never defined.
- Clicking the `"Zapisz klucze API"` button under `"Domena & Hosting" -> "Poczta E-mail"` immediately throws a `NameError: name 'tavily_key' is not defined` Streamlit error.
- Furthermore, under `"Prospecting Hub" -> "Settings"`, there is no button to trigger saving the keys, rendering the settings input fields useless since they cannot be committed.
- Moving the button block from `tab_email` (under `menu == "Domena & Hosting"`) to `tab_settings` (under `menu == "Prospecting Hub"`) will resolve this bug.

---

## 3. Caveats
- We did not execute the `sync_to_gcp.py` script against the live GCP VM because SSH access cannot be verified from our current environment. However, the logic was verified statically and via unit tests.
- We did not find any integrity violations or dummy/facade implementations.

---

## 4. Conclusion
Milestone 2 implementation is logically complete, correct, and robust EXCEPT for the misplaced API key saving button.
**Verdict**: **REQUEST_CHANGES**

### Major Finding: Misplaced "Zapisz klucze API" Button
- **What**: The save button for API keys is placed in the wrong tab/menu block, leading to a `NameError` crash and rendering settings unsavable.
- **Where**: `app.py` lines 6137-6166.
- **Why**: References variables defined only in `Prospecting Hub` tab settings.
- **Suggestion**: Move lines 6137-6166 to `app.py` inside the `with tab_settings:` block in `Prospecting Hub` (directly below line 5937).

---

## 5. Verification Method
1. Run:
   `python -m pytest tests/`
   Verify that all 43 tests pass.
2. Verify the `NameError` crash by navigating to "Domena & Hosting" -> "Poczta E-mail" tab and clicking "Zapisz klucze API".

---

# Quality Review Report

**Verdict**: REQUEST_CHANGES

## Findings
### [Major] Misplaced "Zapisz klucze API" Button
- **What**: Misplaced save button leading to `NameError` crash.
- **Where**: `app.py` lines 6137-6166.
- **Why**: Tries to save variables `tavily_key`, `serper_key`, etc., which are defined in a separate menu block ("Prospecting Hub") that is not executed in "Domena & Hosting" page context.
- **Suggestion**: Move the save button block to `with tab_settings:` under `menu == "Prospecting Hub"`.

## Verified Claims
- Akademia.pl Mentoring tab operates correctly and handles files dynamically -> verified via `tests/test_milestone2_adversarial.py::test_akademia_mentoring_successful_generation` -> PASS
- Dynamic brain directory resolve functions based on mtime -> verified via `tests/test_sync_script.py::test_get_newest_brain_dir_success` -> PASS
- WordPress and COMED prompt integration tabs are rendered -> verified via `tests/test_milestone2_adversarial.py::test_domena_hosting_new_tabs_rendering` -> PASS

## Coverage Gaps
- None.

## Unverified Items
- Actual execution of VM script on GCP VM -> reason: lack of actual credentials and network capability in CODE_ONLY mode.

---

# Adversarial Challenge Report

**Overall risk assessment**: MEDIUM (due to the Streamlit app crash hazard)

## Challenges
### [High] Streamlit Application Crash on Key Saving
- **Assumption challenged**: That the API key saving button would work inside any page context.
- **Attack scenario**: User goes to "Domena & Hosting" -> "Poczta E-mail" and clicks "Zapisz klucze API".
- **Blast radius**: The application throws a NameError exception and crashes that user session.
- **Mitigation**: Move the save button to the Prospecting Hub tab where the inputs are defined.
