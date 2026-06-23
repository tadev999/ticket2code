---
description: Process a JIRA ticket into implementation-ready changes with requirement analysis, staged implementation, and AC evaluation.
---

# /t2c_code

**Type:** Slash-command entry point  
**Input:** `/t2c_code TICKET-ID [--figma FIGMA-LINK]` (e.g., `/t2c_code PROJ-1234` or `/t2c_code PROJ-1234 --figma https://www.figma.com/design/...`)

## What this command does

Kicks off a full ticket-to-code workflow:
1. Fetches the ticket from JIRA
2. (Optional) Analyzes Figma design if link is provided or found in ticket
3. Produces a unified analysis report (JIRA AC + design specs) and waits for DEV confirmation
4. Generates code after confirmation
5. **Cleans up dead code and orphaned references** with mandatory before/after search evidence
6. Asks DEV whether to run build/tests now or defer (because execution may take long)
7. Evaluates the generated code against all acceptance conditions
8. Appends the evaluation to the same report file

## Setup required

Ensure these variables are set in `.env.local` at the repo root:
```
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your JIRA base URL>
FIGMA_TOKEN=<your Figma personal access token> (optional, required only if using Figma links)
```

**FIGMA_TOKEN is optional** — only needed if:
- Figma link is provided via `--figma` flag, OR
- Figma link is found in the JIRA ticket description/comments

See `ticket2code/SETUP.md` for step-by-step instructions.

## Execution Rules

1. **First step:** Ask DEV to select communication language for this run and stop until explicit selection.
2. Check for Figma link:
   - If DEV provided `--figma FIGMA-LINK`, use it directly
   - Else, search JIRA ticket description/comments for Figma links
   - If Figma link found, ask DEV for confirmation to analyze design (optional, can skip)
   - If no Figma link is found, ask DEV whether to add related Figma links:
     - `No` (continue without Figma)
     - `Provide Figma links` (accept one or more Figma links from DEV)
   - If DEV confirms or provides link, use the `figma-design-analysis` skill to analyze design
3. Use the `jira-pbi-analysis` skill workflow to analyze ticket fields, comments, linked issues, and attachments before code generation.
4. If Figma analysis was run, merge design specifications with JIRA analysis into unified implementation guide
5. Decompose Acceptance Criteria into atomic items using the `ac-decomposition` skill.
6. Produce analysis report first, save to `docs/report/<TICKET-ID>_reports_<YYYYMMDDHHmm>.md`, then stop at confirmation gate.
7. After code changes, perform dead-code and orphan-reference cleanup using the `dead-code-cleanup` skill.
8. Ask DEV whether to run tests/build now or defer.
9. Append evaluation against AC to the same report artifact.

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
- **Figma integration:** Figma analysis is optional and triggered only by explicit `--figma` flag or when Figma link exists in JIRA ticket AND DEV confirms.
- **FIGMA_TOKEN requirement:** Only required if Figma analysis is enabled; Figma analysis step can be skipped if token is missing or design is not needed.
- Supported attachments for in-session inspection are static images only (`png`, `jpg`, `jpeg`, `webp`, `gif`) after local download; video attachments are not supported for in-session inspection.
- If a relevant attachment cannot be parsed or inspected, the analysis report must include `Attachment Limitations` and the workflow must stop for explicit DEV confirmation before code generation.
- Never modify code or run write/edit tools before Gate A explicit approval (`Confirm and implement`).
- Never run test/build commands before Gate B explicit approval (`Yes, run now`).
- Do not infer or auto-default DEV decisions at any gate.
- Do not skip evidence for cleanup and AC validation.
- Keep output structured, professional, and traceable.

## References

- **Stage-by-stage behavior** → `ticket2code/code/code-agent.md`
- **Output templates and report schema** → `ticket2code/code/code-processor.prompt.md`
- **Requirement analysis skill** → `.github/skills/jira-pbi-analysis/SKILL.md`
- **Design analysis skill (Figma)** → `.github/skills/figma-design-analysis/SKILL.md`
- **AC Decomposition skill** → `.github/skills/ac-decomposition/SKILL.md`
- **Dead Code Cleanup skill** → `.github/skills/dead-code-cleanup/SKILL.md`

## Compatibility

- Slash command remains unchanged: `/t2c_code TICKET-ID`
- Existing report location and naming remain unchanged.