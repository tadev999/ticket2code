# Figma Design Analysis Skill

This directory contains the Figma design analysis skill for the Ticket2Code framework.

## Contents

- `SKILL.md` — Detailed skill documentation and API integration guide
- `scripts/` — Implementation scripts for different platforms
  - `figma_analyze.sh` — macOS/Linux bash implementation
  - `figma_analyze.ps1` — Windows PowerShell implementation

## Quick Start

### 1. Set up FIGMA_TOKEN

Add to `.env.local` at repository root:
```bash
FIGMA_TOKEN=<your-figma-personal-access-token>
```

Generate token: https://www.figma.com/developers/api#authentication

### 2. Use with /t2c_code

**Option A: Provide Figma link explicitly**
```
/t2c_code PROJ-1234 --figma https://www.figma.com/design/FILE_KEY/Title?node-id=123-456
```

**Option B: Automatic detection**
```
/t2c_code PROJ-1234
```
- Workflow searches JIRA ticket for Figma links
- Asks for confirmation to analyze design
- Continues with JIRA AC only if skipped

### 3. Output

Design analysis is saved to: `docs/design/<TICKET-ID>_figma_analysis_<YYYYMMDDHHmm>.md`

Contents:
- Component hierarchy and specifications
- Design tokens (colors, typography, spacing, shadows)
- Component variants and states
- Accessibility requirements
- AC-to-design traceability matrix
- Implementation recommendations

## Integration with /t2c_code Workflow

1. **Stage 1.5:** Detect Figma link in JIRA ticket or from `--figma` flag
2. **Stage 2.5:** Run design analysis (optional)
3. **Stage 3:** Correlate design components with codebase
4. **Stage 4:** Merge design specs into analysis report
5. **Stage 7:** Code generation references design tokens and component specs

## Error Handling

- If `FIGMA_TOKEN` is missing: Ask user to provide token or skip design analysis
- If Figma file not accessible: Proceed with JIRA AC only (design analysis never blocks)
- If design analysis fails: Log error, append to report, continue workflow

Design analysis is always optional and non-blocking.

## Manual Script Usage

### macOS/Linux:
```bash
FIGMA_TOKEN=... ./.github/skills/figma-design-analysis/scripts/figma_analyze.sh \
  --figma-url "https://www.figma.com/design/FILE_KEY/Title?node-id=12-345" \
  --output docs/design/output.md
```

### Windows PowerShell:
```powershell
$env:FIGMA_TOKEN = "..."
.\.github\skills\figma-design-analysis\scripts\figma_analyze.ps1 `
  -FigmaUrl "https://www.figma.com/design/FILE_KEY/Title?node-id=12-345" `
  -Output "docs/design/output.md"
```

## References

- [Figma REST API Documentation](https://www.figma.com/developers/api)
- [Skill Definition](SKILL.md)
- [/t2c_code Prompt](.../../prompts/t2c_code.prompt.md)
- [Ticket2Code Architecture](.../../code/code-agent.md)
