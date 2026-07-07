---
description: Generate professional screen transition test cases from JIRA ticket requirements.
---

# /t2c_screen_transition_tests

**Type:** Slash-command entry point  
**Input:** `/t2c_screen_transition_tests TICKET-ID` (e.g., `/t2c_screen_transition_tests PROJ-1234`)

## What this command does

Generates screen transition focused test cases from a JIRA ticket:
1. Fetch ticket and parse all AC
2. Identify screen entries, exits, and branch points
3. Build explicit transition paths by scenario
4. Generate test cases with detailed execution steps:
   - **From Screen -> To Screen** per step
   - **Action/Trigger** that causes the transition
   - **Expected UI/System state** at destination screen
   - **Pre-condition and test data** for reproducibility
5. Build AC traceability:
   - Which test case covers which AC
   - Which steps verify that AC
6. Output report in markdown

## Setup required

Ensure these variables are set in `.env.local` at the repo root:
```
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your JIRA base URL>
```
See `ticket2code/SETUP.md` for step-by-step instructions.

## Execution Rules

1. **First step:** Ask DEV to select communication language and stop until explicit selection.
2. **Second step:** Ask DEV to select execution phase (`Pre-Dev` or `Post-Dev`) and stop until explicit selection.
3. Use `jira-pbi-analysis` workflow for requirement extraction from ticket and attachments.
4. If spreadsheet attachments are approved, convert them to markdown via `excel-to-markdown` before transition analysis.
5. Generate and present analysis report first, then stop at confirmation gate.
6. Offer a supplementary-input step after the report and before confirmation (Gate Supplement): ask DEV whether to add extra context via Excel/CSV, image, `.md`/`.txt` file, or typed text; if provided, convert Excel via `excel-to-markdown`, inspect image, read text files/notes, merge findings into an updated report, and re-present it.
7. Decompose Acceptance Criteria into atomic items using the `ac-decomposition` skill.
8. Build transition paths and generate step-wise test cases with explicit screen hops, designing the test environment using the `test-environment-designer` skill.
9. Produce AC -> TC -> Step traceability and coverage notes.

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

### Gate Supplement - Supplementary input (after analysis report, before Gate C)

After the analysis report is produced and saved, ask DEV whether to add extra context before generating test cases:
- Ask DEV: "Do you want to supplement additional information (Excel, image, .md/.txt file, or typed text) before generating test cases?"
- Options: `Provide Excel/CSV` / `Provide image` / `Provide text file (.md/.txt)` / `Type text directly` / `Provide multiple` / `No, proceed`

Handling:
- `Provide Excel/CSV`: convert with `excel-to-markdown`, store under `docs/attachments/<TICKET-ID>/excel/`, extract supplementary requirements/test data with `filename + sheet + row/column` references.
- `Provide image`: inspect with model vision or `design-image-ocr-analysis`; extract supplementary UI/transition details with filename references.
- `Provide text file (.md/.txt)`: read content directly, store a copy under `docs/attachments/<TICKET-ID>/notes/`, extract supplementary requirements/constraints with `filename + line/section` references.
- `Type text directly`: capture verbatim as a `DEV note` and extract supplementary requirements/constraints.
- `Provide multiple`: handle each provided source with the rules above.
- `No, proceed`: continue to Gate C with the current report unchanged.

Gate behavior:
- This gate is mandatory to ASK: always present the supplementary-input question after the report is saved and before Gate C. Never auto-skip; only DEV may decline via `No, proceed`.
- If any supplement is provided, merge findings into the report (Supplementary information subsection and affected screens/transitions/requirements/environment/AC), re-save the report file, and re-present it before Gate C.
- This gate never generates test cases; it only enriches the report.
- If DEV did not explicitly choose an option, stop and ask again.

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
- Supported spreadsheet attachments (`xlsx`, `xls`, `csv`) require explicit DEV confirmation, local download, and markdown conversion before requirement use.
- If a relevant attachment cannot be parsed or inspected, the analysis report must include `Attachment Limitations` and the workflow must stop for explicit DEV confirmation before detailed test-case generation.
- Spreadsheet-backed transition constraints must cite at least `filename + sheet + row/column`.
- Every test case must contain explicit `From Screen`, `Action`, `To Screen`.
- Never generate detailed test cases before Gate C explicit approval (`Confirm and generate test cases`).
- Do not infer or auto-default DEV decisions at any gate.
- Do not claim implementation-verified transition behavior in `Pre-Dev` mode.
- Keep output reproducible and evidence-based.

## References

- **Stage-by-stage behavior** → `ticket2code/screen-transition-tests/screen-transition-tests-agent.md`
- **Output templates and report schema** → `ticket2code/screen-transition-tests/screen-transition-tests-processor.prompt.md`
- **Requirement analysis skill** → `.github/skills/jira-pbi-analysis/SKILL.md`
- **AC Decomposition skill** → `.github/skills/ac-decomposition/SKILL.md`
- **Test Environment Designer skill** → `.github/skills/test-environment-designer/SKILL.md`
- **Excel conversion skill** → `core/skills/excel-to-markdown/SKILL.md`

### Two-phase model rules

- `Pre-Dev`: Use requirement-first planning mode when code for this ticket is not implemented yet.
- `Pre-Dev`: Mark report as draft planning artifact and include assumptions, unknowns, and re-validation checklist.
- `Pre-Dev`: Do not claim implementation-verified transition behavior.
- `Post-Dev`: Use implementation-aware mode when code is available and ready to validate.
- `Post-Dev`: Add evidence-based traceability (AC -> TC -> Step -> transition evidence).
- `Post-Dev`: Use full coverage sign-off gates.

## Output

Screen transition test cases are saved to:
```
docs/test/screen-transition/<TICKET-ID>_screen_transition_tests_<predev|postdev>_<YYYYMMDDHHmm>.md
```

The document includes:
- Screen transition map (entry points and branches)
- Detailed test procedures (screen-by-screen)
- AC coverage matrix (AC -> TC -> Step)
- Coverage gaps and risk notes

## Compatibility

- Slash command remains unchanged: `/t2c_screen_transition_tests TICKET-ID`
- Existing report location and naming remain unchanged.
