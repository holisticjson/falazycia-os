---
name: Landing Page Builder (Anti-Gravity IDE Interface)
description: Analyzes user briefs and delegates coding tasks to the Anti-Gravity IDE sub-agent to generate full, responsive HTML/CSS/JS websites.
---

# Landing Page Builder Skill

## Purpose
This skill acts as a bridge between the Hermes orchestrator and the Anti-Gravity IDE sub-agent. It translates business requirements into technical steps and triggers the coding process.

## Triggers
- When the user asks to "zbuduj stronę dla", "stwórz landing page", or "wygeneruj kod strony".
- When triggered by the "Anti-Gravity IDE" view in Holistic OS.

## Requirements
- Access to the `subagent` invocation tool (to spawn the Anti-Gravity coder).
- Access to the file system (to create directories under `04_clients/`).

## Execution Steps

### 1. Requirements Gathering
Analyze the user's prompt (e.g., "Zbuduj stronę dla dentysty").
Identify:
- Niche/Industry
- Color palette preferences (default: modern, glassmorphic, clean)
- Key sections (Hero, Features, Contact Form, Footer)

### 2. Task Delegation (Nano-Steps)
Break down the project into nano-steps and place them on the Kanban board (via Kanban plugin).
Example:
- Task 1: Setup HTML skeleton & CSS variables.
- Task 2: Build Hero section with abstract background.
- Task 3: Build interactive Appointment form.

### 3. Sub-Agent Invocation
Invoke the Anti-Gravity IDE sub-agent with the specific nano-steps.
Pass the context of the project path (e.g., `04_clients/dentist_landing/`).

### 4. Verification & Feedback
Once Anti-Gravity completes the file writes, Hermes should verify the existence of the files.
Report back to the user: "Strona została wygenerowana przez Anti-Gravity. Pliki znajdują się w folderze projektu."

## Example Command
`hermes run landing_page_builder --client "Dentysta" --theme "Blue/White, Glassmorphism"`
