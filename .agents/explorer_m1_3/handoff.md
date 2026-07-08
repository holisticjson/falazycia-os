# Handoff Report — Skill Consolidation & VM Sync Strategy

## 1. Observation
- Under `C:\Users\tomas_yq1b9su\.gemini\config\plugins\holistic-virtual-board\skills\`, we observed 11 subdirectories containing director skills (`cco`, `ceo`, `cfo`, `cmo`, `coo`, `cso`, `cto`, `generate-video-reel`, `ghost`, `hermes-cloud-architect-sop`, `holistic`), each containing a `SKILL.md` file. For example:
  - `skills/ceo/SKILL.md` contains:
    ```markdown
    ---
    name: CEO-AI-SOP
    description: "Dyrektor Generalny (CEO AI). Orkiestruje trzy filary: SaaS, Agencję i Społeczność..."
    ---
    ```
- Under `.agents/skills/`, we observed 5 subdirectories containing general skills (`karpathy-guidelines`, `n8n-automation-blueprints`, `nlp-copywriting`, `react-bits-integration`, `systeme-io-integration`), and 3 loose markdown files (`auditor_research_logic.md`, `brain_dump_processing.md`, `skill_creator.md`).
- Under the local workspace directory `skills/` (`c:\Aplikacje MVP\Holistic Jason\skills\`), we observed 6 existing skills.
- The file `scratch/sync_to_gcp.py` contains the `remote_cmds` array which deploys the workspace and unzips it to `WORKSPACE_REMOTE` on the GCP VM.
  - Line 12: `WORKSPACE_REMOTE = "/home/holisticjson/Agentic_OS/holistic-aidhd-os"`
  - `EXCLUDED_DIRS` (lines 21-24) does not include `skills`, meaning the `skills` directory in the local workspace will be packaged in the zip file and uploaded to the VM.

## 2. Logic Chain
- Since `skills/` is packaged in the ZIP, any consolidated skills in the local `skills/` folder will be uploaded to `/home/holisticjson/Agentic_OS/holistic-aidhd-os/skills/` on the VM.
- By running `Copy-Item` commands locally, we can copy the 11 director skills from the plugin path and the 5 general skills from `.agents/skills/` (excluding the loose `.md` files) to the local `skills/` folder. This results in 22 total skills (6 existing + 11 director + 5 general).
- Once uploaded, we want to expose these skills to the Hermes runtime. Since Hermes expects global skills in `/home/holisticjson/.hermes/skills/`, we can loop over all subdirectories under the workspace `skills/` directory on the VM and symlink them to `/home/holisticjson/.hermes/skills/`.
- Furthermore, the 11 director skills need to be available as active Hermes profiles in `/home/holisticjson/.hermes/profiles/`. We can loop over the list of director names and symlink their folders from `/home/holisticjson/Agentic_OS/holistic-aidhd-os/skills/<name>` to `/home/holisticjson/.hermes/profiles/<name>`.

## 3. Caveats
- We assume that the user's VM environment has standard bash tools (`ln`, `rm`, `basename`) available. Since it is a Linux VM (based on `unzip` and `nohup` commands in `sync_to_gcp.py`), this is a standard and safe assumption.
- We assume the loose `.md` files in `.agents/skills/` are not intended to be standalone skills and should be excluded from `skills/`.

## 4. Conclusion
- The director skills and agent skills can be consolidated into `skills/` in the local workspace root using PowerShell `Copy-Item` commands.
- `scratch/sync_to_gcp.py` should be updated by adding directory creation and symlinking loops in the `remote_cmds` list. A complete `.patch` file for this change has been created at `.agents/explorer_m1_3/sync_to_gcp.patch`.

## 5. Verification Method
- **Local Verification**:
  Run this PowerShell command in the workspace root to verify that exactly 22 subdirectories exist in `skills/`:
  `@(Get-ChildItem -Path "skills" -Directory).Count`
- **GCP VM Verification**:
  After running `python scratch/sync_to_gcp.py`, run these verification commands on the VM:
  1. `ls -la /home/holisticjson/.hermes/skills/` (Verify all 22 symlinks point to the workspace `skills/` folder).
  2. `ls -la /home/holisticjson/.hermes/profiles/` (Verify the 11 director profiles are symlinked to their respective workspace folders).
  3. `find /home/holisticjson/.hermes/skills/ -type l -xtype l` (Confirm zero broken symlinks).
