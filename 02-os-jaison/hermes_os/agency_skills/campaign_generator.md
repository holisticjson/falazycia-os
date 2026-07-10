---
name: Campaign Generator (Media & Marketing Pipeline)
description: Automates the creation of marketing campaigns, including copywriting for social media posts, ad scripts, and generating prompts for DALL-E / Runway AI tools.
---

# Campaign Generator Skill

## Purpose
This skill orchestrates the "Agency Pipeline" in Holistic OS. It takes a raw idea or brief from the user and expands it into a fully-fledged marketing campaign with text, image prompts, and video scripts.

## Triggers
- When the user asks to "przygotuj kampanię", "napisz posty o", or "stwórz grafiki do".
- When triggered by the "Agency Pipeline" view in Holistic OS.

## Requirements
- Access to external LLM providers (e.g., via OpenRouter/Nous Portal) for creative writing.
- Access to image generation tools/APIs (e.g., DALL-E) if configured.

## Execution Steps

### 1. Brief Analysis
Read the user's brief. Identify the target audience, tone of voice, and platform (e.g., Facebook, Instagram, LinkedIn, TikTok).

### 2. Copywriting Generation
Generate the required textual content:
- **Social Media Posts**: 3-5 variants with emojis and call-to-actions (CTAs).
- **Ad Scripts**: Short scripts for TikTok / Reels.

### 3. Media Prompt Engineering
For each post or script, generate highly detailed prompts for external AI media generators:
- **Image Prompt (DALL-E/Midjourney)**: Specify style, lighting, subject, and mood (e.g., "Photorealistic, cinematic lighting, modern dental clinic, happy patient smiling, bright colors").
- **Video Prompt (Runway/Sora)**: Specify camera movement, action, and duration.

### 4. Output & Presentation
Return the generated content to the UI so it can be displayed in the "Generator Kampanii" and "Galeria Mediów" sections.

## Example Command
`hermes run campaign_generator --brief "Promocja wybielania zębów na lato, platforma: Instagram"`
