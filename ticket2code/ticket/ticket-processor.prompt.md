---
title: "Project Ticket Processor"
description: "Process JIRA tickets to production-ready code with DEV confirmation"
context: "Repository-native architecture and conventions, payment app domain"
---

# Project JIRA Ticket Processor Prompt

When the user says:
- /ticket TICKET-XXXXX

Execute stages:
1. Fetch ticket from JIRA.
2. Parse fields: summary, description, acceptance criteria, labels, components, attachments.
3. Explore codebase for modules/APIs/files affected.
4. Show analysis report and ask confirmation.
5. Generate code only after confirmation.
6. Validate against project rules.
7. Return commit-ready summary.

## Response language policy
- Always respond in the user's language.
- If the user message is in Vietnamese, output the full Stage 3 report in Vietnamese.
- If language is unclear, default to English.

## Analysis report must include
- Ticket id/title/status/type/priority/scope
- Affected modules and APIs
- Files to modify/create
- Code fix approach (how code will be changed)
- Impact flows (functional path and system impact)
- Related patterns and references
- Confirmation options: Yes / Adjust / Add files / Cancel

## Stage 3 output template (required)
Use this structure in every analysis report:

Note:
- Keep the report structure stable.
- Localize all section titles and explanation text to the user's language.

Header format rule:
- The first 3 lines (`TICKET`, `TITLE`, `STATUS`) must always be wrapped in a box using separator line `----------`.
- Use this exact structure:

----------
TICKET: <ID>
TITLE: <summary>
STATUS: <status>
----------

----------
TICKET: <ID>
TITLE: <summary>
STATUS: <status>
----------

Type: <type>
Priority: <priority>
Estimated Scope: <small|medium|large>

Affected Modules:
- <module 1>
- <module 2>

APIs Involved:
- <api 1>
- <api 2>

Files to Modify/Create:
- <path 1> (<modify|create>)
- <path 2> (<modify|create>)

Code Fix Approach:
- Main change: <what logic/UI/state will be changed>
- Safety guardrails: <how regressions are prevented>
- Test update plan: <what tests will be added/updated>

Impact Flows:
1. Flow: <trigger/event>
	Function Path: <entrypoint/screen/action> -> <business function> -> <dependencies (api/db/cache/sdk)>
	Impact: <UI state / button state / loading / navigation>
	Risk: <low|medium|high>
2. Flow: <trigger/event>
	Function Path: <entrypoint/screen/action> -> <business function> -> <dependencies (api/db/cache/sdk)>
	Impact: <cache / timer / retry / side effects>
	Risk: <low|medium|high>

Related patterns and references:
- <project bug or review pattern knowledge base>
- <known release bug if relevant>

Confirmation:
- [ ] Yes, generate code
- [ ] Adjust analysis
- [ ] Add files
- [ ] Cancel

## Validation checklist
- Coding style compliance
- Logging policy compliance
- Test rule compliance
- Review pattern compliance
- No sensitive data in logs

## Notes
- Prefer minimal change set.
- Keep existing repository architecture boundaries.
- Add/adjust tests for changed behavior.
