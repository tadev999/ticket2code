---
agent: t2c-review-orchestrator
description: Review code changes against ticket acceptance criteria via the t2c review orchestrator and jira-pbi-analysis skill.
---

# /t2c_review

**Type:** Slash-command entry point  
**Input:** `/t2c_review TICKET-ID` (e.g., `/t2c_review PROJ-1234`)

## What this command does

Performs automated code review against ticket acceptance criteria:
1. Searches for existing ticket report in `docs/report/TICKET-ID_reports_*.md`
2. If not found, fetches ticket and AC from JIRA (same as `/t2c_code`)
3. Requests commit hash (long or short format) from DEV
4. Retrieves diff between the commit and HEAD
5. Analyzes code changes against AC
6. Generates professional review report

## Setup required

Ensure these variables are set in `.env.local` at the repo root:
```
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your JIRA base URL>
```
See `ticket2code/SETUP.md` for step-by-step instructions.

## Behavior rules

- **Orchestrator agent** → `.github/agents/t2c-review.agent.md`
- **Stage-by-stage behavior** → `ticket2code/review/review-agent.md`
- **Review report templates** → `ticket2code/review/review-processor.prompt.md`
- **Requirement analysis skill** → `.github/skills/jira-pbi-analysis/SKILL.md`
- Mandatory first step: ask DEV which language to use for this run (for example: Vietnamese, English, Japanese).
- Do not continue workflow stages until DEV explicitly selects a language.
- Use the selected language for all follow-up conversation and for the generated review report content in this run.
- Never make assumptions about commit; require explicit input from DEV.
- Review focuses on AC compliance and code quality against repository-specific engineering standards.

## Compatibility

- Slash command remains unchanged: `/t2c_review TICKET-ID`
- Existing report location and naming remain unchanged.
