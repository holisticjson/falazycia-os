## 2026-06-24T10:19:00Z
You are the Explorer subagent for Milestone 3 (Error Handling & Keys Validation).
Your working directory is: c:\Aplikacje MVP\Holistic Jason\.agents\explorer_m3\
Your mission:
1. Explore `app.py` and other modules to identify all external API keys and credentials used (e.g. `OPENROUTER_API_KEY`, GCP/Vertex AI credentials/project/data store IDs, `TAVILY_API_KEY`, `SERPER_API_KEY`, `REDDIT_CLIENT_ID`/`REDDIT_CLIENT_SECRET`, Fakturownia tokens, etc.).
2. Analyze how missing or invalid credentials are currently handled. Identify any places where raw tracebacks, exceptions, or cryptic errors are displayed to the user.
3. Propose a clear, actionable implementation plan to intercept these missing or invalid credentials at startup or runtime. Design and show mockups/layout of beautiful, user-friendly Streamlit amber warning cards (Złota Zasada 6 - Zero Zagadek) with step-by-step setup instructions for the user.
4. Document your findings and proposed code changes in `c:\Aplikacje MVP\Holistic Jason\.agents\explorer_m3\handoff.md` and send a message back with the path to the report when done. Do not modify any source code files.
