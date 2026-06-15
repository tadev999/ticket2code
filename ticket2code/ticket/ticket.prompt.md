---
agent: agent
description: Process a JIRA ticket into implementation-ready changes
---

# /ticket

**Type:** Slash-command entry point  
**Input:** `/ticket TICKET-ID` (e.g., `/ticket PROJ-1234`)

## What this command does

Kicks off a full ticket-to-code workflow:
1. Fetches the ticket from JIRA
2. Produces an analysis report and waits for DEV confirmation
3. Generates code after confirmation
4. Evaluates the generated code against all acceptance conditions
5. Appends the evaluation to the same report file

## Setup required

Ensure these variables are set in `.env.local` at the repo root:
```
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your JIRA base URL>
```
See `ticket2code/ticket/SETUP.md` for step-by-step instructions.

## Behavior rules

- **Stage-by-stage behavior** → `ticket2code/ticket/ticket-agent.md`
- **Output templates and report schema** → `ticket2code/ticket/ticket-processor.prompt.md`
- Always respond in the same language as the user's message.
- Never generate code before explicit DEV confirmation.