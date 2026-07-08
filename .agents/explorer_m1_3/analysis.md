# Analysis & Recommendations: Skill Consolidation and GCP Deployment

This report details the findings and implementation recommendations for consolidating director and agent skills from various local directories into a single unified `skills/` directory in the workspace root, and configuring `scratch/sync_to_gcp.py` to deploy and link them on the GCP VM.

---

## 🎯 Executive Summary
- **Goal**: Centralize all agent and director skills in `skills/` at the root of the workspace, and update the GCP sync process to deploy them to `/home/holisticjson/.hermes/skills/` and link the director skills as active profiles in `/home/holisticjson/.hermes/profiles/`.
- **Status**: Investigation completed. Ready for implementation.

---

## 1. 📂 Current Skill Architecture
We identified three separate directories where skills/SOPs currently reside:

### A. Director Skills (Plugin Directory)
- **Path**: `C:\Users\tomas_yq1b9su\.gemini\config\plugins\holistic-virtual-board\skills\`
- **Count**: 11 skills (each folder contains a `SKILL.md` defining standard operating procedures):
  1. `cco` (Content Director)
  2. `ceo` (General Director)
  3. `cfo` (Financial Director)
  4. `cmo` (Marketing Director)
  5. `coo` (Operations Director)
  6. `cso` (Sales Director)
  7. `cto` (Technology Director)
  8. `generate-video-reel` (Video pipeline)
  9. `ghost` (Tomasz's personal assistant/ghostwriter)
  10. `hermes-cloud-architect-sop` (Hermes & GCP management)
  11. `holistic` (ADHD-optimal personal advisor)

### B. Agent/General Skills (.agents directory)
- **Path**: `c:\Aplikacje MVP\Holistic Jason\.agents\skills\`
- **Count**: 5 skills (subdirectories with a `SKILL.md`):
  1. `karpathy-guidelines` (coding/LLM guidelines)
  2. `n8n-automation-blueprints` (n8n workflows)
  3. `nlp-copywriting` (NLP marketing copy methods)
  4. `react-bits-integration` (React bits animation catalog)
  5. `systeme-io-integration` (Systeme.io standards and blueprints)
- *Note*: Loose markdown files in `.agents/skills/` (like `skill_creator.md`, `auditor_research_logic.md`, `brain_dump_processing.md`) are general instructions and should **not** be consolidated into the main `skills/` folder, as they are not structured as standalone skill subdirectories.

### C. Existing Workspace Skills
- **Path**: `c:\Aplikacje MVP\Holistic Jason\skills\`
- **Count**: 6 existing skills:
  1. `analyze_legal_doc`
  2. `build_systeme_io_funnel`
  3. `create_marketing_campaign`
  4. `hermes_deployment_specialist`
  5. `holistic_broker_real_estate`
  6. `manage_emails`

---

## 2. 🔄 Consolidation Plan (Local Workspace)
To consolidate all skills into the workspace root `skills/` folder, we recommend executing the following PowerShell commands in the local workspace terminal:

```powershell
# 1. Copy the 11 director skills from the plugin directory to skills/
Copy-Item -Path "C:\Users\tomas_yq1b9su\.gemini\config\plugins\holistic-virtual-board\skills\*" -Destination "c:\Aplikacje MVP\Holistic Jason\skills\" -Recurse -Force

# 2. Copy the 5 general skills from .agents/skills/ to skills/, excluding top-level markdown guidelines
Copy-Item -Path "c:\Aplikacje MVP\Holistic Jason\.agents\skills\*" -Destination "c:\Aplikacje MVP\Holistic Jason\skills\" -Recurse -Exclude "*.md" -Force
```

### Resulting Folder Structure (`skills/`):
After execution, `c:\Aplikacje MVP\Holistic Jason\skills\` will contain a total of **22 subdirectories** (6 existing + 11 director skills + 5 general skills), each containing its respective `SKILL.md` file.

---

## 3. 🚀 GCP VM Synchronization & Deployment Plan
The file `scratch/sync_to_gcp.py` manages zipping, uploading, and extracting the workspace on the GCP VM.

### How the skills folder is deployed:
- In `sync_to_gcp.py`, the `create_workspace_zip()` function packages the entire workspace folder except those listed in `EXCLUDED_DIRS`.
- Since `skills` is not in `EXCLUDED_DIRS`, the newly consolidated `skills/` directory is automatically zipped and uploaded to the VM inside `/home/holisticjson/Agentic_OS/holistic-aidhd-os/`.

### Updating the VM extraction block:
To link the skills to their active directories on the GCP VM, we must update the `remote_cmds` array inside `sync_to_gcp.py` to:
1. Ensure the directories `/home/holisticjson/.hermes/skills` and `/home/holisticjson/.hermes/profiles` exist.
2. Symlink all skills from the workspace `skills/` to `/home/holisticjson/.hermes/skills/`.
3. Symlink the 11 director skills to `/home/holisticjson/.hermes/profiles/` so they act as active Hermes profiles.

### Proposed Code Changes in `scratch/sync_to_gcp.py`
Add the following commands to `remote_cmds` (around line 103-126):

```python
    remote_cmds = [
        # Create directories if not exist
        f"mkdir -p {WORKSPACE_REMOTE}",
        "mkdir -p /home/holisticjson/.gemini",
        "mkdir -p /home/holisticjson/.hermes/skills",
        "mkdir -p /home/holisticjson/.hermes/profiles",
        
        # Unzip workspace (overwrite existing)
        f"unzip -o /home/holisticjson/{WORKSPACE_ZIP} -d {WORKSPACE_REMOTE} > /dev/null",
        
        # Unzip .gemini config
        f"unzip -o /home/holisticjson/{GEMINI_ZIP} -d /home/holisticjson/.gemini/ > /dev/null",
        
        # Symlink all consolidated skills to Hermes skills directory
        f'for d in {WORKSPACE_REMOTE}/skills/*/; do if [ -d "$d" ]; then name=$(basename "$d"); rm -rf "/home/holisticjson/.hermes/skills/$name"; ln -sf "$d" "/home/holisticjson/.hermes/skills/$name"; fi; done',
        
        # Symlink director skills to Hermes profiles directory
        f'for name in cco ceo cfo cmo coo cso cto generate-video-reel ghost hermes-cloud-architect-sop holistic; do if [ -d "{WORKSPACE_REMOTE}/skills/$name" ]; then rm -rf "/home/holisticjson/.hermes/profiles/$name"; ln -sf "{WORKSPACE_REMOTE}/skills/$name" "/home/holisticjson/.hermes/profiles/$name"; fi; done',

        # Clean up remote ZIP files
        f"rm -f /home/holisticjson/{WORKSPACE_ZIP}",
        f"rm -f /home/holisticjson/{GEMINI_ZIP}",
        
        # Copy .env to workspace directory on VM for API keys
        f"cp -f {WORKSPACE_REMOTE}/.env {WORKSPACE_REMOTE}/.env 2>/dev/null || true",
        
        # Restart Streamlit process
        "pkill -u holisticjson -f 'streamlit run' 2>/dev/null || true",
        "sleep 2",
        f"nohup /home/holisticjson/.local/bin/streamlit run {WORKSPACE_REMOTE}/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true > /tmp/streamlit_os.log 2>&1 & sleep 3",
        "ss -tlnp | grep 8501"
    ]
```

---

## 4. ✅ Verification & E2E Testing Plan

### A. Local Verification (Windows)
1. Verify that `skills/` contains exactly 22 directories (no loose files or missing director folders).
   - In PowerShell, run: `(Get-ChildItem -Path "skills" -Directory).Count` (Should output `22`).
2. Verify that each directory contains a `SKILL.md` file.

### B. Remote Verification (GCP VM)
1. After running `python scratch/sync_to_gcp.py`, SSH into the VM:
   - `ssh -i C:\Users\tomas_yq1b9su\.ssh\id_rsa_gcp holisticjson@34.55.82.86`
2. Run diagnostic checks:
   - Check all global skills are symlinked:
     `ls -la /home/holisticjson/.hermes/skills/` (Verify symlinks are active and point to `/home/holisticjson/Agentic_OS/holistic-aidhd-os/skills/...`).
   - Check director skills are linked as profiles:
     `ls -la /home/holisticjson/.hermes/profiles/` (Verify 11 director profiles exist and point to the respective workspace skills).
   - Verify there are no broken links:
     `find /home/holisticjson/.hermes/skills/ -type l -xtype l` (Should output nothing).
     `find /home/holisticjson/.hermes/profiles/ -type l -xtype l` (Should output nothing).
