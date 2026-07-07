---
description: Review code changes against ticket acceptance criteria with evidence-based findings.
---

# /t2c_review

**Type:** Slash-command entry point  
**Input:** `/t2c_review TICKET-ID` (e.g., `/t2c_review PROJ-1234`)

## What this command does

Performs automated code review against ticket acceptance criteria:
1. Searches for existing ticket report in `docs/report/TICKET-ID_reports_*.md`
2. If not found, fetches ticket and AC from JIRA (same as `/t2c_code`)
3. Requests commit hash (long or short format) from DEV
4. Retrieves diff between the commit and HEAD
5. Analyzes code changes against AC
6. Generates professional review report

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
2. Resolve ticket context from existing implementation report; if missing, run Jira requirement analysis using the `jira-pbi-analysis` workflow.
3. Offer a supplementary-input step after ticket context is resolved and before requesting the commit hash (Gate Supplement): ask DEV whether to add extra context via Excel/CSV, image, `.md`/`.txt` file, or typed text; if provided, convert Excel via `excel-to-markdown`, inspect image, read text files/notes, and carry findings into diff analysis, AC evaluation, and the review report.
4. Decompose Acceptance Criteria into atomic items using the `ac-decomposition` skill.
5. **Remind DEV:** Current code (HEAD) = latest with fixes. Request explicit **BASE commit hash** (commit before changes) for comparison.
6. Retrieve and analyze `<base-commit>..HEAD` changes using the `git-diff-analysis` skill.
7. Review those changes against decomposed AC, quality standards, and potential regressions.
8. Generate findings-first review report with traceable evidence.

## Mandatory Interaction Gates

### Gate A - Communication language selection

Ask DEV to explicitly select communication language before any other step.

Gate behavior:
- If language is not explicitly selected, stop and ask again.

### Gate Supplement - Supplementary input (after ticket context, before Gate B)

After ticket report/AC context is resolved, ask DEV whether to add extra context before diff analysis and AC evaluation:
- Ask DEV: "Do you want to supplement additional information (Excel, image, .md/.txt file, or typed text) before reviewing?"
- Options: `Provide Excel/CSV` / `Provide image` / `Provide text file (.md/.txt)` / `Type text directly` / `Provide multiple` / `No, proceed`

Handling:
- `Provide Excel/CSV`: convert with `excel-to-markdown`, store under `docs/attachments/<TICKET-ID>/excel/`, extract supplementary requirements/data with `filename + sheet + row/column` references.
- `Provide image`: inspect with model vision or `design-image-ocr-analysis`; extract supplementary details with filename references.
- `Provide text file (.md/.txt)`: read content directly, store a copy under `docs/attachments/<TICKET-ID>/notes/`, extract supplementary requirements/constraints with `filename + line/section` references.
- `Type text directly`: capture verbatim as a `DEV note` and extract supplementary requirements/constraints.
- `Provide multiple`: handle each provided source with the rules above.
- `No, proceed`: continue to Gate B with the current context unchanged.

Gate behavior:
- This gate is mandatory to ASK: always present the supplementary-input question after ticket context is resolved and before Gate B. Never auto-skip; only DEV may decline via `No, proceed`.
- Carry supplementary findings into diff analysis, AC evaluation, and the final review report.
- This gate never evaluates code or writes the review report.
- If DEV did not explicitly choose an option, stop and ask again.

### Gate B - Base commit hash confirmation (before diff analysis)

**Context reminder to DEV:**
> Your current code (HEAD) is the **latest version with fixes**. We need the **BASE commit** (commit BEFORE you started making changes) to analyze what changed.
>
> Example: If you started working on this ticket at commit `abc123`, provide `abc123` as the base commit.

Ask DEV to provide the **base commit hash** (format: long or short):
- `Provide commit hash`
- `Cancel`

Gate behavior:
- Only `Provide commit hash` with a valid resolvable base hash can proceed to diff analysis.
- The command will execute: `git diff <base-commit>..HEAD` to show all your changes.
- `Cancel` must terminate the run.
- If hash is missing/invalid/unresolvable, stop and ask again.
- **Never assume** which commit should be used — always require explicit input from DEV.

## Constraints

- Communication language controls AI-DEV conversation and report narrative only; it does not control programming language, framework, or code syntax.
- **Base vs HEAD clarification:**
  - BASE commit = commit BEFORE code changes were made (starting point)
  - HEAD = current code with fixes applied (ending point)
  - Always require DEV to explicitly specify BASE commit hash
- Never assume commit identity.
- Never run `git diff <base-commit>..HEAD` before Gate B explicit valid hash input.
- Do not infer or auto-default DEV decisions at any gate.
- Keep findings evidence-based and prioritize risk/impact.
- Separate confirmed facts from assumptions.

## References

- **Stage-by-stage behavior** → `ticket2code/review/review-agent.md`
- **Review report templates** → `ticket2code/review/review-processor.prompt.md`
- **Requirement analysis skill** → `.github/skills/jira-pbi-analysis/SKILL.md`
- **AC Decomposition skill** → `.github/skills/ac-decomposition/SKILL.md`
- **Git Diff Analysis skill** → `.github/skills/git-diff-analysis/SKILL.md`

## Compatibility

- Slash command remains unchanged: `/t2c_review TICKET-ID`
- Existing report location and naming remain unchanged.
