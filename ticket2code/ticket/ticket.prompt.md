---
agent: agent
description: Process a JIRA ticket into implementation-ready changes
---

# /ticket - Process a JIRA ticket

This prompt is a thin slash-command entry point.

## Usage

- Run `/ticket TICKET-XXXXX` for a specific ticket.

## Required setup

- Ensure `JIRA_TOKEN`, `JIRA_EMAIL`, and `JIRA_URL` are available in `.env.local` (see `ticket2code/ticket/SETUP.md`).

## Primary reference

- Follow `ticket2code/ticket/ticket-processor.prompt.md` for full workflow and output format.
- Follow `ticket2code/ticket/ticket-agent.md` for stage-by-stage behavior.

## Execution reminder

- Parse the ticket id from the command input.
- Respond in the same language as the user (Vietnamese user input => Vietnamese report output).
- Fetch from JIRA, analyze impacted modules/files, and present analysis first.
- Wait for explicit DEV confirmation before generating code.