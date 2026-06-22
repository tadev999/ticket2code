# Agent Stages

## Stages

### Stage 0 — Select communication language (mandatory)
- Ask DEV to select the language for this run before any other stage.
- Recommended options: Vietnamese, English, Japanese, or explicit custom language input.
- Record selection as `Selected communication language` and reuse it for AI-DEV interactions and report narrative.
- This selection does not control implementation language, framework, or code syntax.

Gate rule:
- If language is not explicitly selected, stop and ask again.

### Stage 1 — Fetch ticket
- Load .env.local to resolve JIRA_TOKEN, JIRA_EMAIL, JIRA_URL.
- Fetch ticket data from JIRA REST API (see 05-jira-policy.md).

### Stage 2 — Parse ticket content
Extract and structure:
- Summary, description, type, priority, status
- Acceptance criteria (all conditions, including conditional branches)
- Labels, components, linked tickets, attachments

Completeness requirements (mandatory before Stage 3):
- Parse all available requirement sources from the fetched ticket payload, including:
	- Description/body content
	- Acceptance criteria text blocks
	- Labels/components
	- Linked issues metadata
	- Attachment metadata
	- Supported static image attachment content, after local download and inspection
	- Comments/changelog/custom fields when present in fetched payload
- Normalize conditional behavior into explicit branches; do not merge distinct outcomes.
- Record unresolved or ambiguous fields as explicit gaps.
- Record unsupported video attachments and unreadable attachments as explicit limitations.

Failure handling:
- If completeness cannot be guaranteed, stop and request additional fetch or DEV clarification.
- Never proceed to Stage 3 while Stage 2 completeness gate is open.

### Stage 3 — Explore codebase
- Identify affected modules, files, APIs, and services.
- Cross-reference with project rule documents (see 04-project-rules.md).
- Identify relevant review patterns and known prior incidents.

### Stage 4 — Generate analysis report
Build Stage 3 analysis report using templates in ../processor-specs.
Must include: ticket header, affected modules, APIs, files to modify/create, code fix approach, impact flows, related patterns, and confirmation options.

### Stage 5 — Save analysis report
- Create file: docs/report/<TICKET-ID>_reports_<YYYYMMDDHHmm>.md
- Write Section 1 (pre-generate analysis) to the file.

Attachment limitation rule:
- If any relevant attachment could not be downloaded, parsed, or inspected, Section 1 must include an `Attachment Limitations` subsection with file, reason, and confidence impact.

### Stage 6 — Request DEV confirmation
For VSCode use vscode_askQuestions.

Required options (exact intent):
- Confirm and implement
- Revise analysis
- Adjust file scope
- Cancel

Attachment fallback gate:
- If the report contains `Attachment Limitations`, do not proceed silently.
- Present the limitation and require explicit DEV choice to continue despite limitation, revise with manual attachment summary, or cancel.

Handler:
- Confirm and implement -> proceed to Stage 7
- Revise analysis -> revise and re-present; do not proceed
- Adjust file scope -> revise and re-present; do not proceed
- Cancel -> stop
- No explicit choice -> do not assume

Gate rule:
- Never generate code before explicit DEV confirmation.
- Never run write/edit tools before explicit `Confirm and implement`.

Execution rule:
- Never run test/build commands before Stage 10.5.

### Stage 7 — Generate code
- Implement according to confirmed analysis.
- Apply repository-specific engineering standards: coding style, logging policy, test rules, review patterns.
- Minimize diff.

### Stage 8 — Decompose acceptance conditions
- Decompose all ACs into atomic items via 02-ac-decomposition.md.
- Each atomic AC must contain: one trigger + one condition value + one expected output.

### Stage 9 — Evaluate code against AC matrix
- For every atomic AC item, assess: Met / Partially Met / Not Met / Unclear.
- Use templates in ../processor-specs/03-section-2-evaluation.md.

### Stage 9.5 — Post-generate code cleanup
- Follow checklist in ../processor-specs/05-cleanup-checklist.md.

Execution boundary:
- Stage 9.5 is for cleanup/search/type-check/lint evidence only.
- Do not run test/build commands here.

Completion gate (mandatory):
1. Removed symbols list
2. Search evidence before/after cleanup (keyword + remaining count)
3. Compiler/type-check and linter result status

Required search scope:
- Production code
- Test code
- Mocks/stubs/fakes
- Assembler/router wiring

### Stage 10 — Append evaluation to report
Append to report:
- Section 2.1 Detailed per-AC mapping
- Section 2.2 Coverage summary
- Section 2.3 Abnormal-case matrix (when needed)
- Section 2.4 Dead-code cleanup evidence
- Section 3 Final conclusions

### Stage 10.5 — Test execution decision gate
- For VSCode use vscode_askQuestions.
- Required options: `Yes, run now` or `No, defer`.
- If Yes, run now: run tests/build and report result.
- If No, defer: record deferred by DEV.
- If no explicit choice: do not assume.

Gate exclusivity:
- This is the only stage allowed to run test/build commands.

### Stage 11 — Validate
Verify all changes against:
- Coding style and naming conventions
- Logging and error handling policy
- Test rules and coverage requirements
- Review pattern checklist
- No sensitive data in logs
- Cleanup complete (dead code/orphan refs removed)
- Test decision gate completed

### Stage 12 — Commit summary decision gate
- For VSCode use vscode_askQuestions.
- If Yes: append Section 4 commit summary.
- If No: record deferred.
- If no explicit choice: do not assume.
