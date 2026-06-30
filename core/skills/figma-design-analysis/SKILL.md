---
name: figma-design-analysis
description: "Analyze a Figma design link via Figma REST API to extract component specs, design tokens, variants, and accessibility requirements for integration with JIRA acceptance criteria."
argument-hint: "Figma URL/file key + node ID"
user-invocable: false
disable-model-invocation: false
---

# Figma Design Analysis

## Scope
This skill handles only direct Figma API analysis.

For screenshot/image-folder OCR analysis, use:
- `.github/skills/design-image-ocr-analysis/SKILL.md`

## What This Skill Produces
- A structured design specification document (markdown).
- Component hierarchy, variants, and state documentation.
- Design tokens (colors, typography, spacing, shadows).
- Accessibility constraints and UX requirements.
- Traceability mapping between design elements and JIRA AC items.
- Implementation recommendations based on design intent.

## When To Use
Use this skill when:
- A JIRA ticket includes a Figma design link in description or comments.
- You have Figma URL or `FILE_KEY + NODE_ID` and valid API access.
- You need to extract visual specifications for code implementation.
- You want to correlate design components with acceptance criteria.

Do not use this skill for screenshot/image-only inputs.

## Required Inputs
- One of:
  - A full Figma design URL: `https://www.figma.com/design/FILE_KEY/Title?node-id=123-456`
  - A Figma `FILE_KEY + NODE_ID` pair
- Node.js available on the machine
- `FIGMA_TOKEN` available in `.env.local`

## Support Policy
- Supported:
  - Frame and component hierarchy analysis
  - Design token extraction (colors, typography, spacing, borders/effects)
  - Variant and state documentation from node properties
  - Layer structure and naming conventions
  - Responsive constraints from Figma node metadata
- Not supported:
  - Screenshot/image OCR extraction
  - Prototype/interaction flow export as code
  - Video or animation playback details
  - Private designs without token permission

## Preferred Script
```bash
node ./.github/skills/figma-design-analysis/scripts/figma_analyze.js \
  --figma-url "https://www.figma.com/design/FILE_KEY/Title?node-id=123-456" \
  --output docs/design/output.md
```

Using file key and node id directly:
```bash
node ./.github/skills/figma-design-analysis/scripts/figma_analyze.js \
  --file-key FILE_KEY \
  --node-id 123:456 \
  --output docs/design/output.md
```

Exporting SVG with the same script:
```bash
node ./.github/skills/figma-design-analysis/scripts/figma_analyze.js \
  --figma-url "https://www.figma.com/design/FILE_KEY/Title?node-id=123-456" \
  --export-svg \
  --asset-output docs/assets/figma-link-01.svg
```

## Procedure

### Input Validation
1. Parse and validate Figma URL or `FILE_KEY + NODE_ID`.
2. Resolve `FIGMA_TOKEN` from environment.
3. Validate token has read access to file.

### Fetch Design Data
1. Call `/files/{FILE_KEY}` to get document structure.
2. Call `/files/{FILE_KEY}/nodes?ids={NODE_IDS}` to get selected node details.
3. Parse hierarchy, naming, tokens, constraints, and properties.

### Analyze Components
1. For each top-level component:
   - map hierarchy (frame -> group -> layer)
   - document variants/state-related properties
   - list child components and instances
2. Record dimensions, constraints, and responsive rules.
3. Capture accessibility-relevant signals (touch-size heuristics, reading order clues).

### Cross-Reference with JIRA
1. Accept JIRA AC list as parameter.
2. Match design components to AC requirements.
3. Flag components not covered by AC and AC without design mapping.

### Generate Output Report
1. Write structured markdown report.
2. Add AC-to-design traceability matrix.
3. Append implementation recommendations.
4. Save to: `docs/design/<TICKET-ID>_figma_analysis_<YYYYMMDDHHmm>.md`

## Integration with /t2c_code
- If design input is Figma link: use this skill.
- If design input is screenshot folder: use `.github/skills/design-image-ocr-analysis/SKILL.md`.

## Environment Variables
Requires in `.env.local`:
```bash
FIGMA_TOKEN=<your Figma personal access token>
```

## Error Handling
- Invalid Figma URL: return structured error with expected format.
- Access denied: suggest checking `FIGMA_TOKEN` permission.
- Missing `FIGMA_TOKEN`: ask DEV to provide token or switch to OCR skill.
- Rate limited (`429`): retry with backoff; if unresolved, suggest OCR skill.
- Design file too large: limit extraction scope and warn.

## References
- Figma REST API: https://www.figma.com/developers/api
- OCR skill: `.github/skills/design-image-ocr-analysis/SKILL.md`
- AC decomposition: `.github/skills/ac-decomposition/SKILL.md`
- JIRA analysis: `.github/skills/jira-pbi-analysis/SKILL.md`
