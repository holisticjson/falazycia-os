## 2026-06-24T07:04:00Z
You are the Worker for Milestone 1 (Skill Consolidation & Sync Script).

Your task:
1. Consolidate the 11 director skills from 'C:\Users\tomas_yq1b9su\.gemini\config\plugins\holistic-virtual-board\skills\' and the 5 general skills from '.agents/skills/' (excluding top-level *.md files) into the main workspace folder 'skills/' (located at 'c:\Aplikacje MVP\Holistic Jason\skills\').
2. Verify that there are exactly 22 skill folders in 'skills/' and each contains a 'SKILL.md'.
3. Modify 'scratch/sync_to_gcp.py' to create '/home/holisticjson/.hermes/skills' and '/home/holisticjson/.hermes/profiles' directories and to link/copy the consolidated skills as detailed in the strategy:
   - Symlink all 22 skills from the workspace 'skills/' into '/home/holisticjson/.hermes/skills/'.
   - Symlink the 11 director skills into '/home/holisticjson/.hermes/profiles/'.
4. Document the exact changes made and the local verification results in '.agents/worker_m1/handoff.md'.
