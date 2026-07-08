## 2026-06-19T14:57:43Z

Your role is teamwork_preview_worker. Your working directory is: c:\Aplikacje MVP\Holistic Jason\.agents\worker_streamlit_repair_1\

Please:
1. Initialize briefing.md and progress.md in your working directory.
2. Add missing dependencies to requirements.txt:
   - google-cloud-storage
   - python-dotenv
   - python-docx
3. Install these packages in the virtual environment using uv or pip:
   - Run: .venv\Scripts\python.exe -m pip install google-cloud-storage python-dotenv python-docx
4. Update c:\Aplikacje MVP\Holistic Jason\01_src\tools\github_client.py:
   - Import urllib.parse.
   - Update `search_repositories` to match signature: `def search_repositories(query, language=None, sort="stars", order="desc", per_page=15)` and correctly format language and query.
5. Populate the following 0-byte placeholder files under c:\Aplikacje MVP\Holistic Jason\01_src\tools\:
   - `social_media.py`: Must export post_to_linkedin, post_to_facebook, post_to_instagram, post_to_twitter, post_to_tiktok, get_env_var. These functions must read the required access tokens/keys from .env. If keys exist, perform simulated/actual calls. If keys do not exist, return a descriptive error dictionary like {"success": False, "error": "Missing client key in .env"}. Ensure get_env_var is implemented robustly.
   - `search_client.py`: Must export search_tavily, search_serper, search_google_cse, get_env_var. tavily and serper should run real HTTP requests if their keys are present in .env, otherwise fail gracefully with a key error dictionary.
   - `reddit_client.py`: Must export search_reddit(query, subreddit, limit). If client id/secret are in .env, use them (or return simulation/error if they are empty).
   - `hunter_client.py`: Must export hunter_domain_search, hunter_verify_email. Make real HTTP calls to Hunter.io API if HUNTER_API_KEY exists in .env, otherwise return failure dictionary.
   - `web_scraper.py`: Must export extract_contact_info(url). Implement scraping or fallback gracefully if scraping fails.
6. Edit app.py:
   - Remove the local redefinition of `call_notebooklm_mcp` at line 2600.
   - Modify the global `run_command_tool(cmd)` at line 664 to support Windows when running on Windows (os.name == 'nt'), falling back to Linux commands when on Linux.
7. Run python compiler checks to verify app.py and all updated tools compile successfully (exit code 0):
   - .venv\Scripts\python.exe -m py_compile app.py 01_src/tools/github_client.py 01_src/tools/social_media.py 01_src/tools/search_client.py 01_src/tools/reddit_client.py 01_src/tools/hunter_client.py 01_src/tools/web_scraper.py
8. Write your handoff report to: c:\Aplikacje MVP\Holistic Jason\.agents\worker_streamlit_repair_1\handoff.md with the results of your checks and changes.
9. Notify me when done.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
