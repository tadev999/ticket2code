---
description: Process a JIRA ticket into implementation-ready changes with requirement analysis, staged implementation, and AC evaluation.
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

## Execution Rules

1. **First step:** Ask DEV to select communication language for this run and stop until explicit selection.
2. Use the `jira-pbi-analysis` skill workflow to analyze ticket fields, comments, linked issues, and attachments before code generation.
3. Decompose Acceptance Criteria into atomic items using the `ac-decomposition` skill.
4. Produce analysis report first, save to `docs/report/<TICKET-ID>_reports_<YYYYMMDDHHmm>.md`, then stop at confirmation gate.
5. After code changes, perform dead-code and orphan-reference cleanup using the `dead-code-cleanup` skill.
6. Ask DEV whether to run tests/build now or defer.
7. Append evaluation against AC to the same report artifact.

## Mandatory Interaction Gates

### Gate A - Analysis confirmation (before any code edits)

After presenting Section 1 analysis report, ask DEV to choose exactly one option:
- `Confirm and implement`
- `Revise analysis`
- `Adjust file scope`
- `Cancel`

Gate behavior:
- Only `Confirm and implement` is allowed to proceed to code changes.
- `Revise analysis` or `Adjust file scope` must return to analysis and re-present report.
- `Cancel` must terminate the run.
- If DEV did not explicitly choose an option, stop and ask again.

### Gate B - Test/build decision (after code and cleanup)

Ask DEV explicitly whether to run test/build now:
- `Yes, run now`
- `No, defer`

Gate behavior:
- Only `Yes, run now` is allowed to execute test/build commands.
- `No, defer` records deferred status in report.
- If DEV did not explicitly choose an option, stop and ask again.

## Constraints

- Communication language controls AI-DEV conversation and report narrative only; it does not control programming language, framework, or code syntax.
- Supported attachments for in-session inspection are static images only (`png`, `jpg`, `jpeg`, `webp`, `gif`) after local download; video attachments are not supported for in-session inspection.
- If a relevant attachment cannot be parsed or inspected, the analysis report must include `Attachment Limitations` and the workflow must stop for explicit DEV confirmation before code generation.
- Never modify code or run write/edit tools before Gate A explicit approval (`Confirm and implement`).
- Never run test/build commands before Gate B explicit approval (`Yes, run now`).
- Do not infer or auto-default DEV decisions at any gate.
- Do not skip evidence for cleanup and AC validation.
- Keep output structured, professional, and traceable.

## References

For detailed behavior definitions, refer to:
- **Ticket Processing Stages** → `ticket2code/code/agent-specs/01-stages.md`
- **Evaluation Rules** → `ticket2code/code/agent-specs/02-evaluation-rules.md`
- **Project-Specific Rules** → `ticket2code/code/agent-specs/03-project-rules.md`
- **JIRA Security Policy** → `ticket2code/code/agent-specs/04-jira-policy.md`
- **Processor Output Schema** → `ticket2code/code/processor-specs/`
- **Requirement Analysis Skill** → `.github/skills/jira-pbi-analysis/SKILL.md`
- **AC Decomposition Skill** → `.github/skills/ac-decomposition/SKILL.md`
- **Dead Code Cleanup Skill** → `.github/skills/dead-code-cleanup/SKILL.md`

## Compatibility

- Slash command remains unchanged: `/t2c_code TICKET-ID`
- Existing report location and naming remain unchanged.