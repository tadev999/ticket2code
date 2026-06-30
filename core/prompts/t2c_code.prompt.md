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

### 1. Configure output settings
Edit `ticket2code.config.yaml` at the repo root (non-sensitive configuration only):
```yaml
# Output language for reports (e.g. "Vietnamese", "English", "Japanese")
default_output_language: "Vietnamese"
```

### 2. Set up authentication tokens and server details
Create `.env.local` at the repo root (this file is gitignored for security):
```
# JIRA configuration (required)
JIRA_TOKEN=<your Atlassian API token>
JIRA_URL=https://your-jira-instance.com
JIRA_EMAIL=your-email@company.com

# Figma (optional, only if analyzing Figma designs directly via API)
FIGMA_TOKEN=<your Figma personal access token>
```

**Setup Requirements:**
- `JIRA_TOKEN` (required): Generate from [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- `JIRA_URL` (required): Your JIRA instance URL (e.g., `https://jira.company.com`)
- `JIRA_EMAIL` (required): Your JIRA account email address
- `FIGMA_TOKEN` (optional): Only needed if analyzing Figma designs directly via API

For screenshot/image analysis mode:
- Model vision: No additional setup required (uses AI analysis)
- Python+OpenCV: Install `pip install opencv-python numpy pillow scikit-image`

Proxy note for setup/install:
- If any install command fails with proxy-related errors (for example: `407 Proxy Authentication Required`, `proxy connect`, `tunnel connection failed`, `CERTIFICATE_VERIFY_FAILED` behind corporate proxy), stop and ask DEV to provide proxy info before retrying.

**File locations:**
- `ticket2code.config.yaml` - Non-sensitive config (version-controlled)
- `.env.local` - Secrets and server details (gitignored)

See `ticket2code/SETUP.md` for step-by-step instructions.

## Execution Rules

1. **First step:** Ask DEV to select communication language for this run and stop until explicit selection.
2. Check for design input source (with MCP capability check):
   - **First: Check MCP capability** - Does the current environment support MCP (Model Context Protocol)?
     - If MCP **NOT available**: Mark as limitation; skip direct Figma API mode; prioritize external tools
     - If MCP **IS available**: Proceed with Figma API mode as option (if FIGMA_TOKEN exists)
   - If DEV provided `--figma FIGMA-LINK`, show it and ask confirmation (considering MCP availability)
   - Else, search JIRA ticket description/comments for Figma links
   - If Figma link(s) found:
     - If MCP available: ask DEV: "Analyze this Figma design? (API mode)" → proceed only if user confirms
     - If MCP NOT available: inform DEV "Figma API analysis not available (MCP limitation)" → offer external tools option
   - Separately, check for image attachments (screenshots) in ticket
   - If image attachments found, ask DEV for confirmation before download/inspection (required gate, include vision capability note)
   - If no Figma link and no images found, ask DEV to choose one design input option:
     - `No` (continue without design analysis)
     - `Provide Figma links` (DEV provides links, then confirmation gate applies with MCP awareness)
     - `Provide screenshot folder for OCR` (accept folder path under `docs/figma_design_analysis/`)
   - For Figma links: if user confirms AND MCP available, use the `figma-design-analysis` skill; otherwise suggest external tools
   - For screenshots: if user confirms, use the `design-image-ocr-analysis` skill
   - If user declines or MCP unavailable: document as limitation, offer external tools or manual description, continue without design data
3. Use the `jira-pbi-analysis` skill workflow to analyze ticket fields, comments, linked issues, and attachments (with confirmation gates).
4. If Figma/design analysis was run (after user confirmation), merge design specifications with JIRA analysis into unified implementation guide
5. Decompose Acceptance Criteria into atomic items using the `ac-decomposition` skill.
6. Produce analysis report first, save to `docs/report/<TICKET-ID>_reports_<YYYYMMDDHHmm>.md`, then stop at confirmation gate.
7. After code changes, perform dead-code and orphan-reference cleanup using the `dead-code-cleanup` skill.
8. Ask DEV whether to run tests/build now or defer.
9. Append evaluation against AC to the same report artifact.

## Mandatory Interaction Gates

### Gate Design - Design analysis confirmation (before Figma/image analysis)

When design input is detected (Figma URLs or image attachments):

**For Figma URLs:**
- **If MCP is NOT available:** Show message "Note: Figma API analysis is not available in this environment (MCP limitation)"
- List detected Figma URLs
- Ask DEV: "How would you like to proceed?"
- Options (depending on MCP availability):
  - **If MCP available:** `Yes, analyze (API)` / `Use external tools` / `Manual input` / `No, skip` / `Cancel`
  - **If MCP NOT available:** `Use external tools` / `Manual input` / `No, skip` / `Cancel`
- Only `Yes, analyze (API)` (when MCP available) allows execution of figma_analyze.js scripts
- `Use external tools` suggests DEV use external Figma-to-JSON converter (e.g., `figma-export-json` CLI) → export design to JSON → provide filename for parsing
- `Manual input` requests additional Figma links or folder paths
- `No, skip` or `Cancel` branches accordingly
- Never attempt Figma API calls without MCP capability

**For Image Attachments:**
- List detected image files (filename, size, type)
- Include capability statement: "Note: my vision/image reading capability may be limited. If analysis is incomplete, you can provide manual descriptions."
- Ask DEV: "Do you want me to download and inspect these images?"
- Options: `Yes, download and analyze` / `No, skip` / `Provide manual descriptions` / `Use external tools` / `Cancel`
- Only `Yes, download and analyze` proceeds to local download and inspection
- `Provide manual descriptions` requests DEV to describe images manually
- `Use external tools` suggests DEV use external OCR/image tools to extract specs → export to JSON/markdown → provide filename for parsing
- `No, skip` or `Cancel` branches accordingly

Gate rule:
- **Never auto-download, auto-analyze, or auto-execute design-related operations**
- Always wait for explicit user input before any design processing
- Check MCP capability before offering Figma API option
- If analysis fails (vision not supported, API error, MCP missing, etc.), offer fallback: external tools, manual description, or skip

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
- **MCP capability awareness:**
  - Always check if current runtime environment supports MCP (Model Context Protocol)
  - If MCP is NOT supported: skip direct Figma API analysis, document as limitation
  - If MCP IS supported but `FIGMA_TOKEN` missing: skip Figma API, suggest external tools
  - Never attempt Figma API calls without MCP capability
  - Always inform DEV of MCP/token limitations upfront
- **Design analysis user confirmation required:**
  - Never auto-download images, auto-run Figma scripts, or auto-parse design attachments
  - When design input is detected (Figma URLs, image attachments), **always ask DEV explicitly** before proceeding
  - Document model vision capability constraints when requesting image inspection
  - Document MCP availability when offering Figma API option
  - Provide graceful fallbacks in priority order:
    1. Direct analysis (Figma API if MCP+token available, vision reading)
    2. Manual descriptions from DEV
    3. **External tools option:** DEV uses external tools (Figma-to-JSON converter, image OCR tools, etc.) to extract specs → export to JSON/markdown → provide filename for AI to parse
- **FIGMA_TOKEN requirement:** Required only for direct Figma API mode. Screenshot/OCR mode must remain available without `FIGMA_TOKEN`.
- Supported attachments for in-session inspection are static images only (`png`, `jpg`, `jpeg`, `webp`, `gif`) **after explicit DEV confirmation and local download**; video attachments are not supported for in-session inspection.
- If a relevant attachment cannot be parsed or inspected:
  - The analysis report must include `Attachment Limitations` section
  - Ask DEV for decision: provide manual description, skip, or cancel
  - Do not proceed to code generation without explicit DEV confirmation
- Never modify code or run write/edit tools before Gate A explicit approval (`Confirm and implement`).
- Never run test/build commands before Gate B explicit approval (`Yes, run now`).
- Do not infer or auto-default DEV decisions at any gate.
- Do not skip evidence for cleanup and AC validation.
- Keep output structured, professional, and traceable.
- **Proxy-failure handling for installation (mandatory):**
  - Applies to any dependency/tool installation step in this workflow (for example `pip install`, package manager setup, installer scripts).
  - If command output indicates proxy/network-gateway restriction (`407`, `proxy`, `tunnel`, `CERTIFICATE_VERIFY_FAILED` in corporate proxy path), do not keep retrying silently.
  - Stop and ask DEV to provide proxy configuration to continue.
  - Request these fields explicitly:
    1. Proxy URL (scheme + host + port)
    2. Whether auth is required (username only in chat; password/token must be entered by DEV directly in terminal)
    3. `NO_PROXY` domains/IP ranges (if any)
    4. Whether custom CA certificate is required
  - After DEV confirms, apply proxy settings and retry once; if it still fails, report limitation and ask whether to continue with fallback/manual path.

## References

- **Stage-by-stage behavior** → `ticket2code/code/code-agent.md`
- **Output templates and report schema** → `ticket2code/code/code-processor.prompt.md`
- **Requirement analysis skill** → `.github/skills/jira-pbi-analysis/SKILL.md`
- **Design analysis skill (Figma)** → `.github/skills/figma-design-analysis/SKILL.md`
- **Design analysis skill (Image OCR)** → `.github/skills/design-image-ocr-analysis/SKILL.md`
- **AC Decomposition skill** → `.github/skills/ac-decomposition/SKILL.md`
- **Dead Code Cleanup skill** → `.github/skills/dead-code-cleanup/SKILL.md`

## Compatibility

- Slash command remains unchanged: `/t2c_code TICKET-ID`
- Existing report location and naming remain unchanged.