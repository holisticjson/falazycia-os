## 2026-06-24T07:09:22Z

You are the Worker for Milestone 2 (Akademia.pl UI Tab & Hosting Docs).

Your task:
1. Copy the prompts and checklists from 'C:\Aplikacje MVP\02_knowledge_base\raw\Mirek_Burnejko_AI_Biznes_Lab\' into a new folder 'c:\Aplikacje MVP\Holistic Jason\scratch\burnejko\'.
2. Implement the new tab '🎯 Akademia.pl Mentoring' in 'app.py':
   - Add the navigation button in the sidebar under 'I. WORKSPACE'.
   - Load and parse the consolidated markdown checklists and prompts from 'scratch/burnejko/'.
   - Allow the user to select a prompt or checklist.
   - Render interactive input fields (e.g. Profil firmy, Target group, Cel marketingowy) and a text area for any additional context.
   - Integrate calling the Gemini API using the existing `call_gemini_api` function defined in 'app.py'.
   - Render the generated results in Markdown, with a button to copy the output to the clipboard.
3. Integrate the other materials into the UI:
   - In the 'Domena & Hosting' page, add a section/card to view and copy the browser automation prompt from 'tasks/comed_browser_prompt.md'.
   - In the 'Domena & Hosting' page (or as a separate expander), display the alternative architecture text from 'docs/alternative_architecture.md' (styled in ADHD format, clean paragraphs, key points, bold headers).
4. Resolve the critical issues identified in 'scratch/sync_to_gcp.py':
   - Remove the hardcoded conversation ID (`8870d516-bbf7-4a9b-b540-34938cc9c42f`) and dynamically resolve it by searching the newest directory under 'C:\Users\tomas_yq1b9su\.gemini\antigravity\brain\'.
   - Fix the copy-to-self/credential overwrite issue on line 119 by backing up the existing remote '.env' file before extraction and restoring it afterwards.
   - Implement Option B profile isolation on the VM: create proper profile folders under '~/.hermes/profiles/$name/' and link/copy 'config.yaml' and symlink the skill under '~/.hermes/profiles/$name/skills/' to prevent runtime logs from leaking back to the git-tracked workspace.
5. Document all changes made and verify locally by running 'pytest' and checking the Streamlit UI. Report results in '.agents/worker_m2/handoff.md'.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
