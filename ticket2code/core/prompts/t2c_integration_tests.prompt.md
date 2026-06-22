---
agent: t2c-integration-tests-orchestrator
description: Generate professional integration test cases from JIRA ticket requirements via orchestrator agent and jira-pbi-analysis skill.
---

# /t2c_integration_tests

Type: Slash-command entry point
Input: `/t2c_integration_tests TICKET-ID` (example: `/t2c_integration_tests PROJ-1234`)

## What this command does

Generates professional integration test cases from a JIRA ticket:
1. Fetches the ticket from JIRA
2. Parses requirements and acceptance criteria
3. Analyzes affected components and dependencies
4. Generates structured integration test cases with:
   - Test categories by functional areas (UI, business logic, data persistence, API, and more)
   - Environment setup (pre-conditions, server config, test data)
   - Test sequences with explicit triggers
   - Expected results with clear success criteria
5. Produces a comprehensive test plan in markdown
6. Validates coverage against all acceptance criteria

## Setup required

Ensure these variables are set in `.env.local` at the repo root:
```
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your JIRA base URL>
```
See `ticket2code/SETUP.md` for full setup instructions.

## Behavior rules

- Orchestrator agent: `.github/agents/t2c-integration-tests.agent.md`
- Stage-by-stage behavior: `ticket2code/integration-tests/integration-tests-agent.md`
- Output templates and report schema: `ticket2code/integration-tests/integration-tests-processor.prompt.md`
- Requirement analysis skill: `.github/skills/jira-pbi-analysis/SKILL.md`
- Mandatory first step: ask DEV to select output language.
- Mandatory second step: ask DEV to select execution phase (`Pre-Dev` or `Post-Dev`).
- Do not continue until language and phase are both explicitly selected.
- Use selected language and phase consistently in all gates and report sections.
- Generate tests according to repository testing standards.
- Classify tests into clear, non-overlapping categories.

### Two-phase model rules

- `Pre-Dev`: requirement-first planning mode; include assumptions and re-validation checklist.
- `Pre-Dev`: do not claim implementation-verified behavior.
- `Post-Dev`: implementation-aware mode with evidence-based traceability.
- `Post-Dev`: apply full coverage sign-off gates.

## Output

Integration test cases are saved to:
```
docs/test/integration/<TICKET-ID>_integration_tests_<predev|postdev>_<YYYYMMDDHHmm>.md
```

## Compatibility

- Slash command remains unchanged: `/t2c_integration_tests TICKET-ID`
- Existing report location and naming remain unchanged.
