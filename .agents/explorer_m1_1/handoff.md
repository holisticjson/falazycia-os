# Handoff Report: Consolidate Director Skills and Update GCP Deployment

This report summarizes the findings of the read-only investigation on consolidating director skills and updating the GCP VM deployment script.

---

## 1. Observation
- **Local Director Skills in .gemini**: The folder `C:\Users\tomas_yq1b9su\.gemini\config\plugins\holistic-virtual-board\skills\` contains exactly 11 subdirectories: `cco`, `ceo`, `cfo`, `cmo`, `coo`, `cso`, `cto`, `generate-video-reel`, `ghost`, `hermes-cloud-architect-sop`, `holistic`. Each contains a single `SKILL.md` file.
- **Local Agent Skills in Workspace**: The folder `.agents/skills/` contains:
  - Folders: `karpathy-guidelines`, `n8n-automation-blueprints`, `nlp-copywriting`, `react-bits-integration`, `systeme-io-integration` (each with a `SKILL.md` file; `nlp-copywriting` also contains a `references/` subdirectory).
  - Standalone files: `skill_creator.md`, `auditor_research_logic.md`, `brain_dump_processing.md`.
- **Main Workspace Skills**: The folder `c:\Aplikacje MVP\Holistic Jason\skills\` exists and contains 6 directory-based skills: `analyze_legal_doc`, `build_systeme_io_funnel`, `create_marketing_campaign`, `hermes_deployment_specialist`, `holistic_broker_real_estate`, `manage_emails`.
- **Deploy Script**: In `scratch/sync_to_gcp.py`, the `create_workspace_zip()` function packages everything under the workspace path (except items in `EXCLUDED_DIRS`). The `remote_cmds` execution block in `main()` runs command strings joined by `" && "`, but currently has no steps for copying/symlinking skills to the Hermes config directory (`/home/holisticjson/.hermes/`).

---

## 2. Logic Chain
- **Step 1**: Moving all folders and files from the two source locations into `skills/` at the workspace root will group them into one central place.
- **Step 2**: Individual files like `skill_creator.md`, `auditor_research_logic.md`, and `brain_dump_processing.md` should be converted into directories (e.g. `skills/skill-creator/SKILL.md`) to comply with the Hermes layout standard for skills.
- **Step 3**: Since `sync_to_gcp.py` zips the workspace, the consolidated `skills/` folder will be uploaded and extracted to `{WORKSPACE_REMOTE}/skills/` on the VM.
- **Step 4**: To make the skills and profiles accessible to Hermes, we can add a shell command loop to the `remote_cmds` block of `sync_to_gcp.py`. This loop will dynamically create symlinks for all directories in `{WORKSPACE_REMOTE}/skills/` inside `/home/holisticjson/.hermes/skills/` and `/home/holisticjson/.hermes/profiles/`.
- **Step 5**: Symlinking is chosen over copying because it ensures that subsequent syncs immediately reflect updates on the VM without requiring manual cleanup or file copying.

---

## 3. Caveats
- The investigation was conducted in `CODE_ONLY` network mode, meaning direct connection to the GCP VM (using SSH) was not executed. The remote commands are formulated based on local code analysis and standard bash scripting.
- It is assumed that the remote directories `/home/holisticjson/.hermes/skills` and `/home/holisticjson/.hermes/profiles` are writable by the `holisticjson` SSH user.

---

## 4. Conclusion
We recommend:
1. Copying/moving all skills from both folders into `skills/` in the main workspace root.
2. Converting the standalone `.md` files in `.agents/skills/` into standard directories with `SKILL.md` inside `skills/`.
3. Updating `scratch/sync_to_gcp.py`'s `remote_cmds` list to run the following bash command block on the VM:
   ```bash
   mkdir -p /home/holisticjson/.hermes/skills
   mkdir -p /home/holisticjson/.hermes/profiles
   for d in {WORKSPACE_REMOTE}/skills/*; do
       if [ -d "$d" ]; then
           name=$(basename "$d")
           rm -rf "/home/holisticjson/.hermes/skills/$name"
           ln -sf "$d" "/home/holisticjson/.hermes/skills/$name"
           rm -rf "/home/holisticjson/.hermes/profiles/$name"
           ln -sf "$d" "/home/holisticjson/.hermes/profiles/$name"
       fi
   done
   ```
   *A complete proposed script has been written to `.agents/explorer_m1_1/proposed_sync_to_gcp.py`.*

---

## 5. Verification Method
1. **Local Consolidation Check**: Execute `Get-ChildItem -Path .\skills -Directory` in PowerShell and check that all consolidated folders exist.
2. **VM Symlink Check**: SSH to the VM and run:
   ```bash
   ls -la /home/holisticjson/.hermes/skills/
   ls -la /home/holisticjson/.hermes/profiles/
   ```
   Verify that symlinks correctly point to the matching directories under `/home/holisticjson/Agentic_OS/holistic-aidhd-os/skills/`.
3. **Regression Check**: Run `pytest` locally to confirm all tests pass.

---

## 6. Remaining Work
- Implementer to perform the local folder copy and file-to-directory conversions.
- Implementer to apply the changes to `scratch/sync_to_gcp.py` (using `proposed_sync_to_gcp.py` as reference).
- Run the deploy script `python scratch/sync_to_gcp.py` and verify the links on GCP VM.
