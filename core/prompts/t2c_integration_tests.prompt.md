---
description: Generate professional integration test cases from JIRA ticket requirements.
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

## Execution Rules

1. **First step:** Ask DEV to select communication language and stop until explicit selection.
2. **Second step:** Ask DEV to select execution phase (`Pre-Dev` or `Post-Dev`) and stop until explicit selection.
3. Use `jira-pbi-analysis` workflow to build requirement inventory from ticket data and attachments.
4. Generate and present analysis report first, then stop at confirmation gate.
5. Decompose Acceptance Criteria into atomic items using the `ac-decomposition` skill.
6. Generate categorized integration test cases, designing the test environment using the `test-environment-designer` skill.
7. Detail step-by-step expected results and validate AC coverage, producing a traceability matrix.

## Mandatory Interaction Gates

### Gate A - Communication language selection

Ask DEV to explicitly select communication language.

Gate behavior:
- If language is not explicitly selected, stop and ask again.

### Gate B - Execution phase selection

Ask DEV to explicitly select execution phase:
- `Pre-Dev`
- `Post-Dev`

Gate behavior:
- If phase is not explicitly selected, stop and ask again.

### Gate C - Analysis confirmation (before generating test cases)

After presenting analysis report, ask DEV to choose exactly one option:
- `Confirm and generate test cases`
- `Revise analysis`
- `Cancel`

Gate behavior:
- Only `Confirm and generate test cases` is allowed to proceed to detailed test case generation.
- `Revise analysis` must return to analysis and re-present report.
- `Cancel` must terminate the run.
- If DEV did not explicitly choose an option, stop and ask again.

## Constraints

- Communication language controls AI-DEV conversation and report narrative only; it does not control programming language, framework, or code syntax.
- Supported attachments for in-session inspection are static images only (`png`, `jpg`, `jpeg`, `webp`, `gif`) after local download; video attachments are not supported for in-session inspection.
- If a relevant attachment cannot be parsed or inspected, the analysis report must include `Attachment Limitations` and the workflow must stop for explicit DEV confirmation before detailed test-case generation.
- Apply phase-specific rules consistently in labeling and validation strictness.
- Keep categories clear and non-overlapping.
- Never generate detailed test cases before Gate C explicit approval (`Confirm and generate test cases`).
- Do not infer or auto-default DEV decisions at any gate.
- Do not claim implementation-verified behavior in `Pre-Dev` mode.

## References

- **Stage-by-stage behavior** → `ticket2code/integration-tests/integration-tests-agent.md`
- **Output templates and report schema** → `ticket2code/integration-tests/integration-tests-processor.prompt.md`
- **Requirement analysis skill** → `.github/skills/jira-pbi-analysis/SKILL.md`
- **AC Decomposition skill** → `.github/skills/ac-decomposition/SKILL.md`
- **Test Environment Designer skill** → `.github/skills/test-environment-designer/SKILL.md`

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
