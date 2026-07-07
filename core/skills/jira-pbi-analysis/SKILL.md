---
name: jira-pbi-analysis
description: "Read and analyze Jira PBI tickets end-to-end, including image and spreadsheet attachments, then produce a professional requirement analysis with scope, risks, gaps, and testable acceptance criteria. Use for grooming, estimation, and handoff to implementation/testing."
argument-hint: "Jira key(s), analysis depth, and expected output format"
user-invocable: true
disable-model-invocation: false
---

# Jira PBI Analysis

## What This Skill Produces
- A structured requirement analysis for one or more Jira PBI issues.
- Explicit extraction of requirements from ticket fields, comments, links, and attachments (including images).
- Explicit extraction of supplemental Excel/CSV evidence after conversion to markdown.
- A decision-ready output for grooming and implementation planning:
  - confirmed scope
  - assumptions
  - unresolved questions
  - risks and dependencies
  - testable acceptance criteria

## When To Use
Use this skill when you need to:
- read a PBI thoroughly before coding
- include attachment files and screenshots in requirement understanding
- include supplemental spreadsheet files (xlsx/xls/csv) in requirement understanding
- resolve Figma design links into local SVG artifacts when MCP is unavailable
- detect missing or ambiguous requirements early
- produce a high-quality analysis for engineering, QA, and PM alignment

Typical triggers:
- "analyze Jira ticket"
- "read this PBI with attachments"
- "summarize requirement gaps"
- "prepare grooming-ready analysis"

## Required Inputs
- Jira key (for example: `PROJ-123456`)
- Jira access available in local environment (for example via `.env.local`)
- Optional context:
  - target platform ([web / mobile / backend / etc.])
  - expected output depth (quick / standard / deep)
  - whether to include implementation proposal

## Workspace Fetch Notes
- **Network preflight (run before any curl/network call):** load `.env.local` so proxy/CA settings apply automatically.
  ```bash
  [ -f .env.local ] && set -a && . ./.env.local && set +a
  ```
  - If `.env.local` defines `HTTPS_PROXY`/`HTTP_PROXY` (corporate user/pass proxy), `curl` will use them automatically after sourcing — no extra flags needed.
  - Respect `NO_PROXY` for internal Jira/mock hosts.
- Prefer curl-based Jira fetch.
- Use `-k` for self-signed certificate environments.
- Prefer this pattern:
  - `curl -s -u "$JIRA_EMAIL:$JIRA_TOKEN" -k -H "Accept: application/json" "$JIRA_URL/rest/api/2/issue/<TICKET-ID>"`
- Avoid relying on Python `urllib` for Jira API calls here because proxy tunnel auth errors can occur.

## Attachment Support Policy
- Supported in-session:
  - ticket fields, comments, linked issues, and attachment metadata
  - static image attachments (`png`, `jpg`, `jpeg`, `webp`, `gif`) **after explicit DEV confirmation and local download**
  - spreadsheet attachments (`xlsx`, `xls`, `csv`) **after explicit DEV confirmation, local download, and conversion to markdown**
- Not supported in-session:
  - video attachments (`mp4`, `mov`, `avi`, `mkv`, `webm`)
  - arbitrary binary attachments without a deterministic parser available in-session
- If an attachment is unsupported or cannot be parsed, treat that as an explicit analysis limitation rather than silently ignoring it.
- **User Confirmation Required:** Never auto-download or auto-inspect images. Always ask DEV first and document model vision capability constraints.
- **User Confirmation Required:** Never auto-download or auto-convert spreadsheet attachments. Always ask DEV first.

## Procedure
1. Collect Core Jira Data
- Fetch ticket fields: summary, description, issue type, status, priority, labels, components, assignee/reporter.
- Fetch acceptance criteria and definition-of-done details (if present).
- Fetch linked issues: parent/epic, blocks/is blocked by, related bugs/tasks.
- Fetch comments and change history when clarification depends on timeline.
- If ticket text or comments contain Figma links that are relevant to requirements, detect all such URLs explicitly.
- Normalize the detected Figma URLs by preserving first-seen order and removing exact duplicates.

1a. **MCP Capability Check (for Figma API access)**
- Check if current runtime environment supports MCP (Model Context Protocol) for Figma API calls
- If MCP is **NOT supported**:
  - Skip direct Figma API analysis (do not attempt to run `figma_analyze.py` with API calls)
  - Document: "MCP not available in current environment"
  - Jump to Step 1b (User confirmation with external tools priority)
- If MCP **IS supported** and `FIGMA_TOKEN` is available:
  - Proceed with normal Figma API flow (Steps 1b onwards)
- If MCP is supported but `FIGMA_TOKEN` is missing:
  - Suggest external tools option as primary alternative

1b. **Figma URL Confirmation (with MCP capability awareness)**
- When Figma URLs are detected, **STOP and ask DEV for explicit confirmation**:
  - Show the detected Figma URLs
  - **If MCP NOT available:** Include note "Note: Figma API analysis is not available in this environment"
  - Ask: "How would you like to proceed?"
  - Options depend on MCP availability:
    - **If MCP available:** `Yes, analyze (API)` / `Use external tools` / `Manual input` / `No, skip` / `Cancel`
    - **If MCP NOT available:** `Use external tools` / `Manual input` / `No, skip` / `Cancel`
  - If user selects `Yes, analyze (API)`: only proceed if MCP is available; run `.github/skills/figma-design-analysis/scripts/figma_analyze.py --export-svg`
  - If user selects `Use external tools` or MCP unavailable: suggest external Figma-to-JSON converter
  - If user selects `Manual input`: ask for explicit folder path or additional input
  - If user selects `No, skip` or `Cancel`: document Figma URLs as pending/skipped in analysis limitations

2. Collect and Inspect Attachments
- Enumerate all attachments from the ticket.
- Classify each attachment by type:
  - document/spec (pdf, docx, xlsx, txt)
  - spreadsheet data (xlsx, xls, csv)
  - data/sample payload (json, csv)
  - media (png, jpg, webp, gif)
  - video (mp4, mov, avi, mkv, webm)
  - archive/binary (zip, tar.gz, etc.)
- For supported static image attachments:
  - **Mandatory confirmation gate:** When image attachments are detected, **STOP and ask DEV for explicit confirmation**:
    - List detected image files (filename, type, approx size)
    - Ask: "Do you want me to download and inspect these images?"
    - **Include capability statement:** "Note: my vision/image reading capability may be limited. If analysis is incomplete, you can provide manual descriptions."
    - Options: `Yes, download and analyze` / `No, skip` / `Provide manual descriptions` / `Use external tools` / `Cancel`
  - If user selects `Yes, download and analyze`:
    - **Network preflight (required before the download loop):** load proxy/CA from `.env.local` once so every attachment download inherits them (avoids `407` on per-file downloads):
      ```bash
      [ -f .env.local ] && set -a && . ./.env.local && set +a
      ```
    - **Download each image attachment into the canonical screenshot folder** read by the image-analysis skill (do NOT use an ad-hoc temp folder, otherwise the analyzer will not find them):
      ```bash
      DEST="docs/figma_design_analysis/<TICKET-ID>_screenshots"
      mkdir -p "$DEST"
      # $TICKET_JSON = payload from the ticket fetch above (.fields.attachment[]: content, filename, mimeType)
      echo "$TICKET_JSON" \
        | jq -r '.fields.attachment[] | select(.mimeType | startswith("image/")) | [.content, .filename] | @tsv' \
        | while IFS=$'\t' read -r url filename; do
            curl -s -L -u "$JIRA_EMAIL:$JIRA_TOKEN" -k -o "$DEST/$filename" "$url" \
              && echo "Downloaded: $filename" \
              || echo "[Attachment Limitations] failed to download: $filename"
          done
      ```
    - **Route the downloaded folder into `design-image-ocr-analysis`** (see `.github/skills/design-image-ocr-analysis/SKILL.md`):
      - Mode 1 (model vision, preferred): read the images in `$DEST` directly and produce the strict extraction JSON.
      - Mode 2 (fallback, Python + OpenCV):
        ```bash
        python3 .github/skills/design-image-ocr-analysis/scripts/image_analyze.py \
          --input-folder "docs/figma_design_analysis/<TICKET-ID>_screenshots" \
          --ticket-id "<TICKET-ID>" \
          --output "docs/design/<TICKET-ID>_image_analysis_$(date +%Y%m%d%H%M).md"
        ```
    - if vision fails or the script is unavailable, request DEV to provide manual description
    - extract: UI elements, copy, states, transitions, error/empty/loading behavior, numeric/business values
    - if any download fails, record an `Attachment Limitations` entry and continue with the successfully downloaded images
  - If user selects `No, skip`: document images as pending/skipped in limitations
  - If user selects `Provide manual descriptions`: ask DEV to describe what's in each screenshot and use that as input
  - **If user selects `Use external tools`:**
    - Suggest DEV use external image/OCR tool to extract design specs → export as JSON or markdown file
    - Provide file path → AI will parse and analyze the extracted data
    - Example: "Use external OCR tool or design tool → export to `docs/figma_design_analysis/<TICKET-ID>_image_specs.json`"
  - If user selects `Cancel`: stop and record decision
- For video attachments:
  - do not claim video playback or frame-by-frame inspection support
  - record video as unsupported in-session
  - capture only metadata and filename/context unless DEV provides a manual summary
  - ask DEV if manual summary is available
- For spreadsheet attachments (`xlsx`, `xls`, `csv`):
  - **Mandatory confirmation gate:** When spreadsheet attachments are detected, **STOP and ask DEV for explicit confirmation**:
    - List detected spreadsheet files (filename, type, approx size)
    - Ask: "Do you want me to download and convert these spreadsheets to markdown for analysis?"
    - Options: `Yes, download and convert` / `No, skip` / `Provide manual summary` / `Cancel`
  - If user selects `Yes, download and convert`:
    - download each spreadsheet locally to temp folder
    - convert using `excel-to-markdown` skill/script
    - store outputs in `docs/attachments/<TICKET-ID>/excel/`
    - extract requirement evidence with references: `file > sheet > row/column`
  - If user selects `No, skip`: document spreadsheets as pending/skipped in limitations
  - If user selects `Provide manual summary`: request structured summary and treat as user-provided evidence
  - If conversion fails for any file:
    - add conversion failure details to `Attachment Limitations`
    - request explicit DEV choice (continue with limitation, provide manual summary, or cancel)
- If an attachment cannot be parsed in-session, record it as a limitation and keep analysis transparent.
- If any relevant attachment cannot be parsed or inspected:
  - add an `Attachment Limitations` section to the analysis output with:
    - filename
    - attachment type
    - reason it could not be parsed/inspected
  - **Required decision:** ask DEV:
    - Can you provide manual description/summary for this?
    - Should we skip this attachment and continue?
    - Should we cancel the analysis?
  - likely impact on confidence/scope

3. Build Requirement Inventory
- Convert raw ticket content into normalized requirement statements:
  - functional requirements
  - non-functional requirements (performance, reliability, security, compliance)
  - constraints (OS version, API contract, rollout flags, locale, accessibility)
  - out-of-scope items
- Mark each requirement with source evidence:
  - ticket field
  - comment
  - linked issue
  - specific attachment
  - spreadsheet reference (`attachment > sheet > row/column`) when applicable

4. Identify Gaps and Ambiguities
- Detect missing details:
  - unclear trigger conditions
  - undefined edge cases
  - contradictory statements across description/comments/attachments
  - missing failure handling or recovery flow
- Convert each gap into a concrete clarification question.

5. Analyze Risks and Dependencies
- Technical risks: architectural impact, migration concerns, state consistency, backward compatibility.
- Product risks: UX mismatch, legal/compliance uncertainty, localization drift.
- Delivery risks: blocked by other teams, backend/API readiness, test environment constraints.
- List mitigations and owner candidates for each major risk.

6. Derive Testable Acceptance Criteria
- Rewrite acceptance criteria into verifiable Given/When/Then style where possible.
- Add negative and edge scenarios inferred from requirements.
- Ensure each criterion has observable expected result.

7. Produce Final Professional Analysis
- Deliver output using the report template in this skill.
- Separate facts from assumptions from recommendations.
- Include confidence level and remaining unknowns.

## Decision Gates
- If any relevant attachment cannot be parsed or inspected:
  - present `Attachment Limitations` in the analysis report
  - stop and request explicit DEV confirmation before continuing
  - acceptable next actions:
    - continue with limitation acknowledged
    - provide manual summary of attachment
    - cancel
- If ticket and attachments conflict:
  - prioritize latest explicit product decision in comments/changelog
  - otherwise mark conflict and request PO confirmation before implementation
- If acceptance criteria are missing:
  - generate proposed criteria and mark as "needs confirmation"
- If attachment references unavailable systems/contracts:
  - flag external dependency and stop short of speculative implementation detail
- If scope is too broad for one iteration:
  - split into MUST/SHOULD/COULD phases and propose decomposition

## Output Template
Use this structure in the final response:

1. Ticket Snapshot
- key, title, status, priority, owner

2. Source Coverage
- fields reviewed
- comments reviewed
- linked issues reviewed
- attachments reviewed (with type and relevance)
- converted spreadsheet artifacts and key sheet references (if any)
- attachment limitations (if any)
- Figma links detected, generated export commands, and export status (if any)

3. Confirmed Requirements
- functional
- non-functional
- constraints
- out-of-scope

4. Ambiguities and Clarification Questions
- question
- why it matters
- blocking or non-blocking

5. Risks and Dependencies
- risk
- impact
- likelihood
- mitigation
- owner

6. Proposed Acceptance Criteria (Testable)
- scenario list in Given/When/Then or equivalent verifiable format

7. Implementation Notes (Optional)
- impacted modules
- API/data considerations
- migration or rollout notes

8. Confidence and Next Actions
- confidence level (high/medium/low)
- required follow-ups

## Quality Checklist (Definition of Done for Analysis)
- Every important claim is traceable to a source (field/comment/attachment).
- Supported image attachments were explicitly downloaded, reviewed, and reflected.
- Supported spreadsheet attachments were explicitly downloaded, converted to markdown, and reflected.
- Unsupported or unreadable attachments were explicitly listed under `Attachment Limitations`.
- Facts vs assumptions are clearly separated.
- Ambiguities are converted into actionable questions.
- Acceptance criteria are testable and observable.
- Risks include mitigation and ownership suggestion.
- Output is concise but complete enough for grooming and implementation kickoff.

## Notes on Security and Professionalism
- Never expose Jira tokens, credentials, or sensitive payloads in chat output.
- Avoid overconfident conclusions when source data is incomplete.
- Prefer explicit uncertainty over hidden assumptions.
