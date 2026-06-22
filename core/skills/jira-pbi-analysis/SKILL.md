---
name: jira-pbi-analysis
description: "Read and analyze Jira PBI tickets end-to-end, including attachment files and image attachments, then produce a professional requirement analysis with scope, risks, gaps, and testable acceptance criteria. Use for grooming, estimation, and handoff to implementation/testing."
argument-hint: "Jira key(s), analysis depth, and expected output format"
user-invocable: true
disable-model-invocation: false
---

# Jira PBI Analysis

## What This Skill Produces
- A structured requirement analysis for one or more Jira PBI issues.
- Explicit extraction of requirements from ticket fields, comments, links, and attachments (including images).
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
- Prefer curl-based Jira fetch.
- Use `-k` for self-signed certificate environments.
- Prefer this pattern:
  - `curl -s -u "$JIRA_EMAIL:$JIRA_TOKEN" -k -H "Accept: application/json" "$JIRA_URL/rest/api/2/issue/<TICKET-ID>"`
- Avoid relying on Python `urllib` for Jira API calls here because proxy tunnel auth errors can occur.

## Attachment Support Policy
- Supported in-session:
  - ticket fields, comments, linked issues, and attachment metadata
  - static image attachments (`png`, `jpg`, `jpeg`, `webp`, `gif`) after downloading the file locally for inspection
- Not supported in-session:
  - video attachments (`mp4`, `mov`, `avi`, `mkv`, `webm`)
  - arbitrary binary attachments without a deterministic parser available in-session
- If an attachment is unsupported or cannot be parsed, treat that as an explicit analysis limitation rather than silently ignoring it.

## Procedure
1. Collect Core Jira Data
- Fetch ticket fields: summary, description, issue type, status, priority, labels, components, assignee/reporter.
- Fetch acceptance criteria and definition-of-done details (if present).
- Fetch linked issues: parent/epic, blocks/is blocked by, related bugs/tasks.
- Fetch comments and change history when clarification depends on timeline.
- If ticket text or comments contain Figma links that are relevant to requirements, detect all such URLs explicitly.
- Normalize the detected Figma URLs by preserving first-seen order and removing exact duplicates.
- For each relevant Figma URL, use `.github/skills/figma-svg-export/SKILL.md` to export the referenced node to a local SVG artifact before continuing analysis.
- When one or more Figma URLs are detected, suggest an exact ready-to-run export command list for the current shell environment, one command per link.
- Command generation rules:
  - preserve the same order as links appear in the ticket/comments
  - generate deterministic output filenames such as `docs/assets/figma-link-01.svg`, `docs/assets/figma-link-02.svg`
  - bash/zsh example format:
    - `FIGMA_TOKEN=... ./.github/skills/figma-svg-export/scripts/figma_export_svg --figma-url "<FIGMA-URL>" --output docs/assets/figma-link-01.svg`
  - PowerShell example format:
    - `$env:FIGMA_TOKEN="..."; ./.github/skills/figma-svg-export/scripts/figma_export_svg.cmd -FigmaUrl "<FIGMA-URL>" -Output "docs/assets/figma-link-01.svg"`
- If the Figma URL is missing `node-id`, stop and ask DEV for a specific node before claiming the design was exported.

2. Collect and Inspect Attachments
- Enumerate all attachments from the ticket.
- Classify each attachment by type:
  - document/spec (pdf, docx, xlsx, txt)
  - data/sample payload (json, csv)
  - media (png, jpg, webp, gif)
  - video (mp4, mov, avi, mkv, webm)
  - archive/binary (zip, tar.gz, etc.)
- For supported static image attachments:
  - download each image attachment locally first
  - inspect the downloaded image visually in-session
  - extract:
  - UI elements and copy
  - states and transitions
  - error/empty/loading behavior
  - numeric/business values shown in screenshots
- For video attachments:
  - do not claim video playback or frame-by-frame inspection support
  - record video as unsupported in-session
  - capture only metadata and filename/context unless DEV provides a manual summary
- If an attachment cannot be parsed in-session, record it as a limitation and keep analysis transparent.
- If any relevant attachment cannot be parsed or inspected, add an `Attachment Limitations` section to the analysis output with:
  - filename
  - attachment type
  - reason it could not be parsed/inspected
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
