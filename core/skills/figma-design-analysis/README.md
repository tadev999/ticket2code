# Figma Design Analysis Skill

This directory contains the Figma design analysis skill for the Ticket2Code framework.

## Contents

- `SKILL.md` — Detailed skill documentation and API integration guide
- `scripts/` — Python implementation
  - `figma_analyze.py` — Python 3 implementation (macOS, Windows, Linux)

## Quick Start

### 1. Set up FIGMA_TOKEN

Ensure Python 3.8+ is available and add the token to `.env.local` at repository root:
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

The direct API script parses actual Figma file/node JSON instead of emitting placeholder component data. The report includes selected root nodes, layer hierarchy, colors, text styles, auto-layout spacing, borders/radius, effects, published styles, component properties, visible text content, layout constraints, asset export candidates, and touch-target heuristics. Visual QA still requires screenshots or exported frame images because Figma API metadata alone cannot prove final rendering, prototype animation, or all inherited opacity/contrast details.

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

### Python (stdlib only):
```bash
python3 ./.github/skills/figma-design-analysis/scripts/figma_analyze.py \
  --figma-url "https://www.figma.com/design/FILE_KEY/Title?node-id=12-345" \
  --output docs/design/output.md
```

Using file key and node ID directly:
```bash
python3 ./.github/skills/figma-design-analysis/scripts/figma_analyze.py \
  --file-key FILE_KEY \
  --node-id 12:345 \
  --output docs/design/output.md
```

Exporting a node to SVG:
```bash
python3 ./.github/skills/figma-design-analysis/scripts/figma_analyze.py \
  --figma-url "https://www.figma.com/design/FILE_KEY/Title?node-id=12-345" \
  --export-svg \
  --asset-output docs/assets/figma-link-01.svg
```

## References

- [Figma REST API Documentation](https://www.figma.com/developers/api)
- [Skill Definition](SKILL.md)
- [/t2c_code Prompt](.../../prompts/t2c_code.prompt.md)
- [Ticket2Code Architecture](.../../code/code-agent.md)
