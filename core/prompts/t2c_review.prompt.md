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
3. Decompose Acceptance Criteria into atomic items using the `ac-decomposition` skill.
4. Require explicit commit hash from DEV before diff analysis.
5. Retrieve and analyze commit..HEAD changes using the `git-diff-analysis` skill.
6. Review those changes against decomposed AC, quality standards, and potential regressions.
7. Generate findings-first review report with traceable evidence.

## Mandatory Interaction Gates

### Gate A - Communication language selection

Ask DEV to explicitly select communication language before any other step.

Gate behavior:
- If language is not explicitly selected, stop and ask again.

### Gate B - Commit hash confirmation (before diff)

Ask DEV to provide commit hash with explicit intent:
- `Provide commit hash`
- `Cancel`

Gate behavior:
- Only `Provide commit hash` with a valid resolvable hash can proceed to diff analysis.
- `Cancel` must terminate the run.
- If hash is missing/invalid/unresolvable, stop and ask again.

## Constraints

- Communication language controls AI-DEV conversation and report narrative only; it does not control programming language, framework, or code syntax.
- Never assume commit identity.
- Never run `git diff <commit>..HEAD` before Gate B explicit valid hash input.
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
