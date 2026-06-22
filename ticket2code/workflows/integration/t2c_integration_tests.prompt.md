---
agent: t2c-integration-tests-orchestrator
description: Generate professional integration test cases from JIRA ticket requirements via orchestrator agent and jira-pbi-analysis skill.
---

# /t2c_integration_tests

**Type:** Slash-command entry point  
**Input:** `/t2c_integration_tests TICKET-ID` (e.g., `/t2c_integration_tests PROJ-1234`)

## What this command does

Generates professional integration test cases from a JIRA ticket:
1. Fetches the ticket from JIRA
2. Parses requirements and acceptance criteria
3. Analyzes affected components and dependencies
4. Generates structured integration test cases with:
   - **Test Categories**: Classification by functional areas (UI, Business Logic, Data Persistence, API, etc.)
   - **Environment Setup**: Pre-conditions, server configuration, test data initialization
   - **Test Sequences**: Step-by-step test procedures with clear triggers
   - **Expected Results**: Detailed outcomes and success criteria
5. Produces a comprehensive test plan in markdown format
6. Validates test coverage against all acceptance criteria

## Setup required

Ensure these variables are set in `.env.local` at the repo root:
```
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your JIRA base URL>
```
See `ticket2code/SETUP.md` for step-by-step instructions.

## Behavior rules

- **Orchestrator agent** → `.github/agents/t2c-integration-tests.agent.md`
- **Stage-by-stage behavior** → `ticket2code/integration-tests/integration-tests-agent.md`
- **Output templates and report schema** → `ticket2code/integration-tests/integration-tests-processor.prompt.md`
- **Requirement analysis skill** → `.github/skills/jira-pbi-analysis/SKILL.md`
- Mandatory first step: ask DEV which language to use for this run (for example: Vietnamese, English, Japanese).
- Mandatory second step: ask DEV which execution phase to use for this run (`Pre-Dev` or `Post-Dev`).
- Do not continue workflow stages until DEV explicitly selects a language.
- Do not continue workflow stages until DEV explicitly selects an execution phase.
- Use the selected language for all follow-up conversation and for the generated test report content in this run.
- Use the selected execution phase consistently for all gates, report labeling, and validation strictness.
- Generate tests following the repository's testing standards and conventions.
- Classify tests into clear, non-overlapping categories.

### Two-phase model rules

- `Pre-Dev`: Use requirement-first planning mode when code for this ticket is not implemented yet.
- `Pre-Dev`: Mark report as draft planning artifact and include assumptions, unknowns, and re-validation checklist.
- `Pre-Dev`: Do not claim implementation-verified behavior.
- `Post-Dev`: Use implementation-aware mode when code is available and ready to validate.
- `Post-Dev`: Add evidence-based traceability (AC -> TC -> Step -> implementation/artifact references).
- `Post-Dev`: Use full coverage sign-off gates.

## Output

Integration test cases are saved to:
```
docs/test/integration/<TICKET-ID>_integration_tests_<predev|postdev>_<YYYYMMDDHHmm>.md
```

The document includes:
- Test plan overview
- Environment setup procedures
- Test case matrix (organized by category)
- Test sequences with expected results
- Coverage analysis against AC

## Compatibility

- Slash command remains unchanged: `/t2c_integration_tests TICKET-ID`
- Existing report location and naming remain unchanged.
