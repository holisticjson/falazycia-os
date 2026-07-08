---
name: Web Researcher (Social Media Prospecting)
description: Analyzes social media platforms (LinkedIn, Reddit) and web pages to find potential leads, verify contact info, and aggregate business intelligence. Compatible with Hermes Web Browser control.
---

# Web Researcher Skill

## Purpose
This skill instructs Hermes Agent on how to perform deep web research to identify leads, extract sentiment, and build a mailing list.

## Triggers
- When the user asks to "skanuj leady", "przeszukaj LinkedIn", or "znajdź klientów dla...".
- When triggered by the "Prospecting" view in Holistic OS.

## Requirements
- Browser automation enabled (Playwright/Puppeteer via Hermes core).
- Access to `knowledge` (Mnemosyne plugin) to store results.

## Execution Steps

### 1. Platform Selection
Determine the target platforms based on the user's query:
- B2B (CEOs, Founders) -> LinkedIn
- Pain points, organic issues (ADHD, productivity) -> Reddit (r/ADHD, r/Entrepreneur)
- General trends -> Platform X / Web

### 2. Scraping & Extraction
Navigate to the platform using Hermes Browser Control.
- **Search Query**: Construct a highly targeted search query (e.g., `"szukam nowej strony internetowej"`, `"poleci ktoś agencję"`).
- **Data Points to Extract**:
  - Author Name / Handle
  - Content / Post text
  - Sentiment (Hot, Warm, Cold)
  - Contact method (DM, Email if available in bio)

### 3. Verification & Formatting
Ensure the extracted data is relevant to the Holistic Jason offering.
Format the output as a JSON array or a Markdown table.

### 4. Storage & Reporting
- Save the extracted leads into the `Mnemosyne` database under the tag `#prospecting_leads`.
- Report back to the user via Telegram/Dashboard: "Znalazłem X nowych leadów na platformie Y."

## Example Command
`hermes run web_researcher --target "LinkedIn" --query "CEO szuka agencji marketingowej"`
