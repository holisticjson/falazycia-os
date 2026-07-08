# Streamlit Codebase Audit Report

This report summarizes findings and recommendations from a read-only audit of the Streamlit dashboard and its submodules.

## 1. Observation
Below are direct observations of syntax, dependency, path compatibility, and signature errors in the codebase:

### 1.1 Missing Dependencies and Import Failures
* **Obsidian RAG / GCS:** In `01_src/knowledge.py:3`, the module imports `from google.cloud import storage`.
* **Swarm Orchestrator:** In `01_src/swarm/directors.py:4` and `01_src/swarm/workers.py:3`, the module imports `from dotenv import load_dotenv`.
* **Legal Engine:** In `app.py:3496`, the code imports `from docx import Document as DocxDoc`.
* **Command Output:** Running programmatic import testing in the `.venv` virtual environment resulted in:
  ```
  Testing import of 01_src.knowledge...
  FAILED: 01_src.knowledge
  Error: cannot import name 'storage' from 'google.cloud' (unknown location)

  Testing import of 01_src.swarm.directors...
  FAILED: 01_src.swarm.directors
  Error: No module named 'dotenv'
  ```
* **Venv Packages:** Running `uv pip list` shows that `google-cloud-storage`, `python-dotenv`, and `python-docx` are not installed in the virtual environment. They are also missing from `requirements.txt`.

### 1.2 Empty (0-Byte) Local Tool Placeholders
* **File size:** Running `Get-ChildItem -Path "01_src/tools"` returned a file size of `0` bytes for several tool modules.
* **Social Media Hub (`app.py:4564`):** Dynamically loads `01_src/tools/social_media.py` and tries to access:
  ```python
  post_to_linkedin = social_media.post_to_linkedin
  post_to_facebook = social_media.post_to_facebook
  post_to_instagram = social_media.post_to_instagram
  post_to_twitter = social_media.post_to_twitter
  post_to_tiktok = social_media.post_to_tiktok
  get_env_var = social_media.get_env_var
  ```
* **Prospecting Hub (`app.py:4682`):** Dynamically loads:
  * `01_src/tools/search_client.py` (accesses `search_tavily`, `search_serper`, `search_google_cse`, `get_env_var`)
  * `01_src/tools/reddit_client.py` (accesses `search_reddit`)
  * `01_src/tools/hunter_client.py` (accesses `hunter_domain_search`, `hunter_verify_email`)
  * `01_src/tools/web_scraper.py` (accesses `extract_contact_info`)
* **Result:** Because these files are completely empty, retrieving their attributes raises `AttributeError`. The screens catch this error, print a loading error message, and call `st.stop()`, rendering the screens blank.

### 1.3 Windows Path and Duplicate Function Redefinition
* **NotebookLM MCP:** Global `call_notebooklm_mcp` is defined at `app.py:719` with a platform check:
  ```python
  if os.name == 'nt':
      cmd = ["npx", "-y", "notebooklm-mcp"]
  ```
* **Local Redefinition:** At `app.py:2600`, the function `call_notebooklm_mcp` is redefined *inside* a tab block without a platform check, hardcoding Linux commands:
  ```python
  cmd = [
      "sudo", "-u", "holisticjson", "sh", "-c",
      "cd /home/holisticjson && "
      "NODE_PATH=/home/holisticjson/.npm/_npx/0d29dd9f4e472da9/node_modules "
      "/home/holisticjson/.hermes/node/bin/node "
      "/home/holisticjson/.npm/_npx/0d29dd9f4e472da9/node_modules/notebooklm-mcp/dist/index.js"
  ]
  ```
* **Global Command Exec:** `run_command_tool(cmd)` at `app.py:664` hardcodes `["sudo", "-u", "holisticjson", "sh", "-c", cmd]`.
* **Result:** On Windows, interacting with the NotebookLM panel or calling general shell commands will fail with a `FileNotFoundError` traceback or failure because the Linux binaries and users do not exist.

### 1.4 GitHub Explorer Bugs
* **Signature Mismatch:** In `01_src/tools/github_client.py:5`, `search_repositories` is defined as:
  ```python
  def search_repositories(query, limit=5):
  ```
  But in `app.py:4311`, it is called with:
  ```python
  results = search_repositories(query, language=lang_query, sort=sort_by, order=order_by, per_page=15)
  ```
* **Missing Import:** In `01_src/tools/github_client.py:7`, the function uses `urllib.parse.quote(query)` but the file only imports `import urllib.request` and does not import `urllib.parse`.
* **Result:** Pressing "Szukaj na GitHubie" raises a `TypeError` and crashes, or raises `NameError` due to missing `urllib.parse`.

---

## 2. Logic Chain
1. We verified syntactical correctness of all `.py` files using `py_compile`. Both `app.py` and all submodules compiled without syntax errors.
2. We then ran import checks inside the `.venv` python environment. We observed that modules `01_src.knowledge` and all `01_src.swarm` files threw `ImportError`/`ModuleNotFoundError` due to missing packages `google-cloud-storage` and `python-dotenv`.
3. Analyzing `uv pip list` and `requirements.txt` confirmed that these packages, along with `python-docx` (imported in `app.py`), are entirely missing from the environment configuration.
4. Programmatic scan of `01_src/tools` revealed that five core client tools (social_media, search_client, reddit_client, hunter_client, web_scraper) are 0 bytes.
5. In `app.py`, these files are imported dynamically, and specific functions are extracted. When the user visits `Social Media Hub` or `Prospecting Hub`, these attributes are accessed. Since the files are empty, `AttributeError` is thrown, halting rendering via `st.stop()`.
6. Reading `app.py` line-by-line revealed that `call_notebooklm_mcp` is redefined locally at line 2600. This redefinition lacks the `os.name == 'nt'` check from line 719 and hardcodes Linux-specific environment and user variables (`sudo -u holisticjson`). This will fail on the Windows environment.
7. Examining `01_src/tools/github_client.py` showed that `urllib.parse` is not imported, and `search_repositories` has a signature mismatch (2 positional parameters vs 5 keyword parameters passed in `app.py`). This guarantees a crash upon clicking search.

---

## 3. Caveats
* The audit was performed under a read-only constraint. No file changes were made to the source codebase.
* The local GCP configurations and actual credential files (`holistic-dashboard-dev-dea2c872139e.json`) were not verified for actual API authentication success, only for existence and code validation.
* External API responses (Tavily, Pexels, Google Places, OpenRouter) are assumed to work if the API keys are correctly set up in the `.env` file.

---

## 4. Conclusion & Proposed Fix Strategies

### 4.1 Missing Dependencies Fix
* Add `google-cloud-storage`, `python-dotenv`, and `python-docx` to `requirements.txt`.
* Install the missing packages in the environment:
  ```powershell
  uv pip install google-cloud-storage python-dotenv python-docx
  ```

### 4.2 Empty Tool Implementations Fix
* Populating the 0-byte files in `01_src/tools/` with mock interfaces or functional code is necessary to prevent `st.stop()` from rendering the pages empty.
* At minimum, define empty dummy functions that return polite mock info or helpful instructions rather than leaving the files at 0 bytes. For example, in `social_media.py`:
  ```python
  def post_to_linkedin(text, title=None, link=None):
      return {"status": "mock", "message": "Post to LinkedIn simulated successfully."}
  def post_to_facebook(text, link=None): ...
  ```

### 4.3 Windows Path & Duplicate Function Fix
* Remove the local redefinition of `call_notebooklm_mcp` at `app.py:2600`. The global function at `app.py:719` is sufficient and correctly handles both Windows (`nt`) and Linux/UNIX platforms.
* Modify `run_command_tool` at `app.py:664` to support Windows execution (e.g., executing the cmd directly without `sudo` and `sh` when `os.name == 'nt'`).

### 4.4 GitHub Explorer Fix
* Update `01_src/tools/github_client.py` imports:
  ```python
  import urllib.request
  import urllib.parse
  import json
  ```
* Update `search_repositories` in `github_client.py` to match the expected signature:
  ```python
  def search_repositories(query, language=None, sort="stars", order="desc", per_page=5, limit=None):
      # Ensure limit is handled correctly (per_page could be used instead)
      # Build query with optional language parameter
  ```

---

## 5. Verification Method
To verify that all modules load and run correctly after applying fixes:

1. **Import Verification:** Run the import test script:
   ```powershell
   .venv\Scripts\python.exe .agents\explorer_streamlit_1\test_imports.py
   ```
   *Expected result:* All modules should print `SUCCESS`.

2. **Syntax/Compile Verification:** Compile the modified files:
   ```powershell
   .venv\Scripts\python.exe -m py_compile app.py 01_src/tools/github_client.py
   ```
   *Expected result:* Exit code 0, no output.

3. **Streamlit App Check:** Start the streamlit app:
   ```powershell
   .venv\Scripts\streamlit.exe run app.py
   ```
   *Expected result:* View each sidebar page (Social Media Hub, Prospecting Hub, GitHub Explorer, NotebookLM panel) and ensure no error popups or blank page stops are executed.
