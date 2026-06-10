# Project Ticket Processing Agent

Purpose: execute a workflow from JIRA ticket analysis to code generation with explicit DEV confirmation.

Trigger command:
- Handle ticket TICKET-XXXXX
- Xử lý ticket TICKET-XXXXX
- /ticket TICKET-XXXXX

## Workflow
1. Fetch ticket data from the JIRA REST API.
2. Parse title, description, labels, attachments, acceptance criteria.
3. Analyze the codebase to find related modules/files/APIs.
4. Print a TICKET ANALYSIS REPORT for DEV confirmation, including mandatory Impact Flows.
5. Generate code only after explicit DEV confirmation.
6. Validate against coding style, test, logging, and review pattern rules.
7. Output a summary and a suggested commit message.

## Stage 3 report requirements
- The report language must follow the user's language.
- The `TICKET`, `TITLE`, `STATUS` header block must always be wrapped by `----------` lines.
- Required header shape:

----------
TICKET: <ID>
TITLE: <summary>
STATUS: <status>
----------

- Always include a "Code Fix Approach" section after "Files to Modify/Create" and before "Impact Flows".
- Always include an "Impact Flows" section, with at least 2 flows when the ticket is not trivial.
- Each flow must explicitly include: Trigger, Function Path (entrypoint/screen/action -> business function -> dependencies), Impact, and Risk.

## Required env
- JIRA_TOKEN
- JIRA_EMAIL
- JIRA_URL

## Required project rules
- Coding style / naming convention document
- Code review guideline document
- Logging and error handling policy document
- Test rule / coverage guideline document
- Development or delivery policy document if present
- Bug pattern / release bug / review pattern knowledge base if present

## Rule discovery order
1. Repository `docs/` directory for the required rule categories above.
2. Repository-level AI instruction file only if it adds constraints not already covered by `docs/`.
3. Documents linked from that instruction file when additional clarification is needed.

## Confirmation rule
- Do not generate code unless there is clear, explicit confirmation from DEV.
