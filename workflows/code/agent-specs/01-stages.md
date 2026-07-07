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

### Stage 1.5 — Collect design input source (optional)
- Search JIRA ticket description and comments for Figma design links (pattern: `https://www.figma.com/design/...`)
- If Figma link found, present to DEV with options:
  - `Analyze design` (run Stage 2.5)
  - `Skip design` (proceed directly to Stage 2)
- If `--figma LINK` was provided in command input, use it directly and ask DEV for confirmation
- If no Figma link is detected from ticket/command input, ask DEV:
  - `No` (continue without design analysis and proceed to Stage 2)
  - `Provide Figma links` (DEV supplies one or more Figma links to be used for Stage 2.5)
  - `Provide screenshot folder for OCR` (DEV provides a folder path under `docs/figma_design_analysis/`)
- Record selected design source (Figma links and/or screenshot folder path) for potential Stage 2.5 execution

Gate rule:
- If Figma link is found, wait for explicit DEV choice before proceeding
- If no Figma link is found, do not auto-skip; ask DEV explicitly whether to provide links, screenshot folder, or skip
- This stage is completely optional; DEV can always skip

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
  - Supported spreadsheet attachment content (`xlsx`, `xls`, `csv`) after local download and markdown conversion
	- Comments/changelog/custom fields when present in fetched payload
- Normalize conditional behavior into explicit branches; do not merge distinct outcomes.
- Record unresolved or ambiguous fields as explicit gaps.
- Record unsupported video attachments and unreadable attachments as explicit limitations.

Failure handling:
- If completeness cannot be guaranteed, stop and request additional fetch or DEV clarification.
- Never proceed to Stage 3 while Stage 2 completeness gate is open.

### Stage 2.5 — Analyze design source (optional, conditional on Stage 1.5)
Run only if:
- Figma link was detected in Stage 1.5 AND DEV chose `Analyze design`, OR
- Figma link was provided via `--figma` flag AND DEV confirmed, OR
- DEV provided one or more Figma links manually in Stage 1.5, OR
- DEV provided screenshot folder path for OCR analysis in Stage 1.5

Procedure:
- Choose analysis mode based on Stage 1.5 source:
  - Direct Figma mode: verify `FIGMA_TOKEN` and use `figma-design-analysis` (see .github/skills/figma-design-analysis/SKILL.md)
  - Screenshot/image mode (with vision): Use AI model vision analysis (automatic)
  - Screenshot/image mode (without vision): Use Python+OpenCV analysis via `design-image-ocr-analysis` (see .github/skills/design-image-ocr-analysis/SKILL.md)
- Extract:
  - Component hierarchy and specifications
  - Design tokens (colors, typography, spacing, shadows)
  - Variants and states
  - Accessibility requirements and constraints
  - Design documentation strings
- Generate AC-to-design traceability matrix mapping JIRA AC to Figma components
- Save design analysis to:
  - Direct Figma mode: `docs/design/<TICKET-ID>_figma_analysis_<YYYYMMDDHHmm>.md`
  - Screenshot/image mode: `docs/design/<TICKET-ID>_image_analysis_<YYYYMMDDHHmm>.md`

Output:
- Structured design specification document
- Design tokens and component catalog
- AC-to-design traceability matrix
- Implementation recommendations based on design intent

Failure handling:
- If `FIGMA_TOKEN` is missing in direct Figma mode, stop and ask DEV to either:
  - Provide `FIGMA_TOKEN` in `.env.local` and retry, OR
  - Switch to screenshot/OCR mode by providing screenshot folder, OR
  - Skip design analysis and proceed with JIRA AC only
- If Figma file cannot be accessed, record reason in report and proceed with JIRA AC only
- If screenshot folder is missing/invalid or contains no supported images, ask DEV to correct folder/input before skipping
- If design analysis fails, record error and proceed with JIRA AC only (design analysis never blocks workflow)
- If dependency installation is required for analysis tools (for example Python/OpenCV) and installation fails with proxy-like errors (`407`, `proxy`, `tunnel`, SSL cert issues in proxy path):
  - Stop and request DEV proxy information explicitly before retry
  - Do not retry silently more than once
  - If retry still fails, record limitation and ask DEV to choose fallback/manual path

Gate rule:
- Design analysis is completely optional and never blocks code generation
- If design analysis fails or is skipped, proceed to Stage 3 with JIRA AC only

### Stage 3 — Explore codebase
- Identify affected modules, files, APIs, and services.
- Cross-reference with project rule documents (see 04-project-rules.md).
- Identify relevant review patterns and known prior incidents.
- If Figma design analysis was completed in Stage 2.5, correlate design components with codebase structures
- Reference design tokens and component specs when identifying files to modify

### Stage 4 — Generate analysis report
Build Stage 3 analysis report using templates in ../processor-specs.
Must include: 
- Ticket header
- Affected modules, APIs, files to modify/create
- Code fix approach and impact flows
- Related patterns and known incidents
- Source evidence summary for image and spreadsheet attachments (when present)
- (If Figma analysis completed) Design specifications section with:
  - Component hierarchy and specs
  - Design tokens and accessibility requirements
  - AC-to-design traceability matrix
- Confirmation options

### Stage 5 — Save analysis report
- Create file: docs/report/<TICKET-ID>_reports_<YYYYMMDDHHmm>.md
- Write Section 1 (pre-generate analysis) to the file.

Attachment limitation rule:
- If any relevant attachment could not be downloaded, parsed, or inspected, Section 1 must include an `Attachment Limitations` subsection with file, reason, and confidence impact.

Evidence traceability rule:
- If image and/or spreadsheet attachments were used, Section 1 must include explicit references to those sources.
- Spreadsheet references must include at least `filename + sheet name + row/column` for each critical claim.

### Stage 5.5 — Supplementary input gate (optional, before confirmation)
Purpose:
- After the PBI-based report exists, allow DEV to add extra context before coding.
- Supported supplement sources: Excel/CSV, image, text file (`.md`, `.txt`), and direct text input typed by DEV.
- This stage only enriches the report; it never generates code.

Procedure:
- Ask DEV: "Do you want to supplement additional information (Excel, image, .md/.txt file, or typed text) before coding?"
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
	- extract supplementary requirements/UI details with filename references
- If text file (`.md`, `.txt`) provided:
	- read the file content directly
	- store a copy under docs/attachments/<TICKET-ID>/notes/
	- extract supplementary requirements/constraints with `filename + line/section` references
- If DEV types text directly:
	- capture the text verbatim as a DEV-provided note
	- extract supplementary requirements/constraints and label the source as `DEV note`
- If multiple sources are provided, process each source with the rules above.
- Merge supplementary findings into the existing report:
	- update Section 1.8 Supplementary information
	- update affected modules, APIs, files, impact flows, and AC as needed
	- re-save the report file at the same path
- Re-present the updated report to DEV.

Gate rule:
- This gate is mandatory to ASK: always present the supplementary-input question after Stage 5 and before Stage 6. "Optional" refers to DEV's freedom to decline, not the agent's freedom to skip.
- Never auto-skip this stage even when the report looks complete; only DEV may skip it by selecting `No, proceed`.
- If DEV selects `No, proceed`, continue to Stage 6 with the current report unchanged.
- If supplement is provided, always regenerate and re-present the updated report before Stage 6.
- Never start coding from this stage.
- If DEV does not explicitly choose an option, stop and ask again.

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

Cross-stage installation/proxy rule:
- Before any network or dependency-installation step (for example `curl`, `pip install`, Python API fetch), run the network preflight to load proxy/CA settings from `.env.local`:
  ```bash
  [ -f .env.local ] && set -a && . ./.env.local && set +a
  ```
- Whenever any stage requires tool/dependency installation and command output indicates proxy restriction (`407`, `proxy connect`, `tunnel connection failed`, `CERTIFICATE_VERIFY_FAILED` under corporate proxy), the agent must:
  1. Stop current automation
  2. Ask DEV for proxy settings (`HTTP_PROXY`/`HTTPS_PROXY`, auth requirement, `NO_PROXY`, custom CA) and confirm they are set in `.env.local`
  3. Retry once after DEV confirmation (re-run the preflight first)
  4. If still failing, document limitation and ask whether to continue with fallback/manual alternative

### Stage 12 — Commit summary decision gate
- For VSCode use vscode_askQuestions.
- If Yes: append Section 4 commit summary.
- If No: record deferred.
- If no explicit choice: do not assume.
