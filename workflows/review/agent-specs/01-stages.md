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

### Stage 1.5 — Supplementary input gate (mandatory to ask, before diff evaluation)
Purpose:
- After the ticket report/AC context is resolved, allow DEV to add extra context before diff analysis and AC evaluation.
- Supported supplement sources: Excel/CSV, image, text file (`.md`, `.txt`), and direct text input typed by DEV.
- This stage only enriches requirement context; it never evaluates code or writes the review report.

Procedure:
- Ask DEV: "Do you want to supplement additional information (Excel, image, .md/.txt file, or typed text) before reviewing?"
- For VSCode use vscode_askQuestions.
- Required options (exact intent):
	- Provide Excel/CSV
	- Provide image
	- Provide text file (.md / .txt)
	- Type text directly
	- Provide multiple
	- No, proceed
- If Excel/CSV provided:
	- convert the file(s) with the `excel-to-markdown` skill
	- store outputs under docs/attachments/<TICKET-ID>/excel/
	- extract supplementary requirements/data with `filename + sheet + row/column` references
- If image provided:
	- inspect with model vision or the `design-image-ocr-analysis` skill (after confirmation)
	- extract supplementary requirement/UI details with filename references
- If text file (`.md`, `.txt`) provided:
	- read the file content directly
	- store a copy under docs/attachments/<TICKET-ID>/notes/
	- extract supplementary requirements/constraints with `filename + line/section` references
- If DEV types text directly:
	- capture the text verbatim as a DEV-provided note
	- extract supplementary requirements/constraints and label the source as `DEV note`
- If multiple sources are provided, process each source with the rules above.
- Carry supplementary findings into Stage 4 analysis and Stage 5 AC evaluation, and cite them in the Stage 6 report.

Gate rule:
- This gate is mandatory to ASK: always present the supplementary-input question after Stage 1 and before Stage 2. "Optional" refers to DEV's freedom to decline, not the agent's freedom to skip.
- Never auto-skip this stage; only DEV may skip it by selecting `No, proceed`.
- If DEV selects `No, proceed`, continue to Stage 2 with the current context unchanged.
- Never evaluate code or write the review report from this stage.
- If DEV does not explicitly choose an option, stop and ask again.

### Stage 2 — Request commit hash (BASE commit before code changes)
- **Context reminder:** Your current code (HEAD) is the latest version with fixes applied. We need the BASE commit (commit BEFORE the changes) to compare against.
- Ask DEV for the BASE commit hash in either format: long (40-char) or short (7-12 char).
  - Example: If you are working on TICKET-123 fixes, provide the commit hash from BEFORE you started making changes.
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
- **Clarification:** The command will run `git diff <BASE-commit>..HEAD` to show all changes from BASE to your current code.

### Stage 3 — Retrieve commit diff
- Execute `git diff <base-commit>..HEAD` to get all changes.
  - `<base-commit>` = commit provided by DEV in Stage 2 (the "before" state)
  - `HEAD` = current code with fixes (the "after" state)
- Resolve and record metadata for both:
	- BASE commit (`<base-commit>` provided by DEV): starting point before changes
	- HEAD commit (`HEAD`): current code with all fixes applied
- Parse and structure the diff: files modified, insertions, deletions, hunks.
- Identify language/type of each file (Swift, Kotlin, Python, etc.).

Completion gate (mandatory):
- Diff is successfully retrieved and parsed.
- Both BASE and HEAD commit metadata are available for Section 1.
- File list with change statistics is available.

### Stage 4 — Analyze code changes
- Map each change to relevant codebase areas (modules, APIs, services).
- Cross-reference with repository-specific engineering standards (coding style, logging policy, test rules).
- Identify potentially risky changes or missing tests.
- For AC items not satisfied in diff, search the existing codebase for pre-existing implementation before concluding.

### Stage 5 — Evaluate against AC
- Decompose AC (from Stage 1 report) into atomic items.
- For each atomic AC, check implementation in this order:
	1) diff (`git diff <base-commit>..HEAD`), then
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
