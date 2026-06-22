---
agent: t2c-code-orchestrator
description: Process a JIRA ticket into implementation-ready changes via the t2c code orchestrator and jira-pbi-analysis skill.
---

# /t2c_code

**Type:** Slash-command entry point  
**Input:** `/t2c_code TICKET-ID` (e.g., `/t2c_code PROJ-1234`)

## What this command does

Kicks off a full ticket-to-code workflow:
1. Fetches the ticket from JIRA
2. Produces an analysis report and waits for DEV confirmation
3. Generates code after confirmation
4. **Cleans up dead code and orphaned references** with mandatory before/after search evidence
5. Asks DEV whether to run build/tests now or defer (because execution may take long)
6. Evaluates the generated code against all acceptance conditions
7. Appends the evaluation to the same report file

## Setup required

Ensure these variables are set in `.env.local` at the repo root:
```
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your JIRA base URL>
```
See `ticket2code/SETUP.md` for step-by-step instructions.

## Behavior rules

- **Orchestrator agent** → `.github/agents/t2c-code.agent.md`
- **Stage-by-stage behavior** → `ticket2code/code/code-agent.md`
- **Output templates and report schema** → `ticket2code/code/code-processor.prompt.md`
- **Requirement analysis skill** → `.github/skills/jira-pbi-analysis/SKILL.md`
- Mandatory first step: ask DEV which language to use for this run (for example: Vietnamese, English, Japanese).
- Do not continue workflow stages until DEV explicitly selects a language.
- Use the selected language for all follow-up conversation and for the generated report content in this run.
- Never generate code before explicit DEV confirmation.

## Compatibility

- Slash command remains unchanged: `/t2c_code TICKET-ID`
- Existing report location and naming remain unchanged.