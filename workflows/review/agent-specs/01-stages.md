# Review Stages

## Stages

### Stage 0 — Select communication language (mandatory)
- Ask DEV to select the language for this run before any other stage.
- Recommended options: Vietnamese, English, Japanese, or explicit custom language input.
- Record selection as `Selected communication language` and reuse it for AI-DEV interactions and review report narrative.
- This selection does not control implementation language, framework, or code syntax.

Gate rule:
- If language is not explicitly selected, stop and ask again.

### Stage 1 — Resolve ticket report
- Search for existing report in `docs/report/<TICKET-ID>_reports_*.md`.
- If found, load it to extract ticket summary, AC, and context.
- If not found, fetch ticket from JIRA API (same as /t2c_code Stage 1-2).
- Record which source was used (cached report or fresh fetch).

Completion gate (mandatory):
- Report file location or fetch confirmation is recorded.
- AC list is available for Stage 2.

### Stage 2 — Request commit hash
- Ask DEV for commit hash in either format: long (40-char) or short (7-12 char).
- Required options at this gate:
	- Provide commit hash
	- Cancel
- Validate hash format.
- Attempt to resolve hash in local repo.

Gate rule:
- If hash cannot be resolved, stop and ask for clarification.
- Do not assume partial hash refers to HEAD or recent commits.
- If DEV selects Cancel, terminate the run.
- Never continue to Stage 3 without explicit valid hash input.

### Stage 3 — Retrieve commit diff
- Execute `git diff <commit>..HEAD` to get all changes.
- Resolve and record metadata for both:
	- before/base commit (`<commit>` provided by DEV)
	- after commit (`HEAD`)
- Parse and structure the diff: files modified, insertions, deletions, hunks.
- Identify language/type of each file (Swift, Kotlin, Python, etc.).

Completion gate (mandatory):
- Diff is successfully retrieved and parsed.
- Both before/base and after/HEAD commit metadata are available for Section 1.
- File list with change statistics is available.

### Stage 4 — Analyze code changes
- Map each change to relevant codebase areas (modules, APIs, services).
- Cross-reference with repository-specific engineering standards (coding style, logging policy, test rules).
- Identify potentially risky changes or missing tests.
- For AC items not satisfied in diff, search the existing codebase for pre-existing implementation before concluding.

### Stage 5 — Evaluate against AC
- Decompose AC (from Stage 1 report) into atomic items.
- For each atomic AC, check implementation in this order:
	1) diff (`git diff <commit>..HEAD`), then
	2) existing codebase outside diff.
- Assess: Met / Partially Met / Not Met / Unclear.
- Document which lines address each AC and identify evidence source: Diff or Codebase.

Completion gate (mandatory):
- Every AC has an assessment status.
- Each assessment includes line references from diff and/or codebase.
- Any "Unclear" status confirms codebase verification was already performed.

### Stage 6 — Generate review report
- Write Section 1: commit metadata, diff summary.
- Write Section 2: AC evaluation matrix with line references.
- Write Section 3: code quality assessment against repository-specific engineering standards.
- Write Section 4: overall conclusion and recommendations.
- Save to `docs/report/<TICKET-ID>_reviews_<YYYYMMDDHHmm>.md`.

Output gate (mandatory):
- Report file is created at correct path.
- All four sections are present and complete.
