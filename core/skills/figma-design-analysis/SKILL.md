---
name: figma-design-analysis
description: "Analyze a Figma design link to extract component specs, documentation, design tokens, and accessibility requirements for integration with JIRA acceptance criteria."
argument-hint: "Figma file URL or file key + node ID, optional local cache path"
user-invocable: false
disable-model-invocation: false
---

# Figma Design Analysis

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
- You need to extract visual specifications for code implementation.
- You want to correlate design components with acceptance criteria.
- You're implementing UI features that require pixel-perfect accuracy or component variants.

Typical usage flow:
1. `/t2c_code TICKET-ID` is invoked with optional `--figma-link`
2. Skill fetches and analyzes the Figma design
3. Design analysis is merged with JIRA analysis to produce unified implementation guide

## Required Inputs
- `FIGMA_TOKEN` available in `.env.local`
- One of:
  - A full Figma design URL: `https://www.figma.com/design/FILE_KEY/Title?node-id=123-456`
  - A Figma FILE_KEY + NODE_ID pair

## Support Policy
- **Supported:**
  - Frame and component hierarchy analysis
  - Design token extraction (colors, typography, spacing)
  - Variant and state documentation
  - Documentation strings attached to components
  - Layer structure and naming conventions
  - Responsive breakpoints and constraints
  - Visual hierarchy and spacing relationships
- **Not supported:**
  - Prototype/interaction flow export as code
  - Video or animation playback details
  - Developer handoff plugin-specific metadata (if not in standard Figma API)
  - Private designs without access token permission

## Design Analysis Output Structure

### Section 1: Design Overview
- File name and link
- Canvas page structure
- Top-level component hierarchy
- Design file author and last modified date

### Section 2: Component Specifications
For each primary component:
- Component name and path
- Figma node ID
- Component description (from documentation)
- Variants (if present)
- States (default, hover, active, disabled, error, etc.)
- Dimensions (width, height, aspect ratio constraints)
- Content sizing and overflow behavior

### Section 3: Design Tokens
- **Colors:** Primary, secondary, background, text, borders, with hex values and semantic names
- **Typography:** Font families, sizes, weights, line heights, letter spacing
- **Spacing:** Margins, padding, gaps (in logical units and pixels)
- **Shadows, borders, radius:** Standard patterns used across components
- **Icons:** List of icon components with sizes and use cases

### Section 4: Accessibility & UX Notes
- Contrast ratio compliance
- Touch target sizes (if specified)
- Keyboard navigation hints
- Focus state documentation
- Semantic layer naming conventions
- Content flow and reading order

### Section 5: AC-to-Design Traceability Matrix
Map each JIRA AC to specific Figma components:
```
| JIRA AC | Design Component | Figma Node ID | Implementation Notes |
|---------|------------------|---------------|----------------------|
| AC-1    | PaymentButton    | 123:456       | Primary variant      |
| AC-2    | ErrorAlert       | 234:567       | With error icon      |
```

### Section 6: Implementation Recommendations
- Suggested component structure (view hierarchy)
- Responsive breakpoint handling
- State management strategy for variants
- Suggested framework patterns (Storybook, SwiftUI, React, etc.)
- Known constraints or limitations
- Placeholder handling for dynamic content

## API Integration

### Extract File Content
```bash
curl -H "X-FIGMA-TOKEN: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/{FILE_KEY}"
```

### Parse Component Metadata
- Traverse `document.children` to build hierarchy
- Extract `components` array for main component definitions
- Parse `componentSets` for variant groups
- Read `description` fields for documentation

### Get Component Details
```bash
curl -H "X-FIGMA-TOKEN: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/{FILE_KEY}/nodes?ids={NODE_IDS}"
```

Returns:
- Full node properties (fills, strokes, typography, layout)
- Child structure
- Constraints and responsive settings
- Component properties and variants

### Extract Images (for visual review)
```bash
curl -H "X-FIGMA-TOKEN: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/images?ids={NODE_IDS}&format=png&scale=2"
```

## Procedure

### Input Validation
1. Parse Figma URL or validate FILE_KEY + NODE_ID
2. Resolve `FIGMA_TOKEN` from environment
3. Validate token has read access to file

### Fetch Design Data
1. Call `/files/{FILE_KEY}` to get document structure
2. Identify primary components and component sets
3. Parse layer hierarchy and naming conventions
4. Extract design tokens (colors, typography, spacing)

### Analyze Components
1. For each top-level component:
   - Map node hierarchy (frame → group → shape)
   - Document variants and their properties
   - Extract state information (default, hover, disabled, etc.)
   - List child components and instances
2. Record dimensions, constraints, and responsive rules
3. Parse accessibility metadata (alt text, semantic role, etc.)

### Cross-Reference with JIRA
1. Accept JIRA AC list as parameter
2. Match design components to AC requirements
3. Flag components not covered by AC (scope questions)
4. Flag AC without design components (design gaps)
5. Note assumed vs. explicitly designed behaviors

### Generate Output Report
1. Write structured markdown per output schema above
2. Include visual references (where feasible, note: exported images not embedded)
3. Add AC-to-design traceability matrix
4. Append implementation recommendations tailored to target framework
5. Save to: `docs/design/<TICKET-ID>_figma_analysis_<YYYYMMDDHHmm>.md`

## Integration with /t2c_code

When invoked as part of `/t2c_code` workflow:

1. **Stage 1.5 (new):** After fetching JIRA ticket, if Figma link is provided:
   - Extract Figma link from ticket description or comments
   - OR ask DEV to provide Figma link if not found
2. **Stage 2.5 (new):** Run this skill to analyze design
3. **Stage 3 (updated):** Codebase exploration considers both JIRA AC + design specs
4. **Stage 4 (updated):** Analysis report merges JIRA analysis + design analysis into single unified implementation guide
5. **Stage 7 (updated):** Code generation references both AC and design tokens/variants

## Environment Variables

Requires in `.env.local`:
```bash
FIGMA_TOKEN=<your Figma personal access token>
```

Generate token: https://www.figma.com/developers/api#authentication

## Error Handling

- **Invalid Figma URL:** Return structured error with expected format
- **Access Denied:** Suggest checking FIGMA_TOKEN permission
- **Design file too large:** Limit to first N components, warn about truncation
- **Missing documentation:** Proceed with layer analysis, note gap in Section 6
- **Component with no variants:** Document as single-state component

## Caching & Performance

- Cache downloaded design JSON for 1 hour to reduce API calls
- Cache extracted images locally in `docs/design/figma_assets/`
- Reuse cache if same FILE_KEY requested within same session
- Allow DEV to force refresh with `--no-cache` flag

## References

- Figma REST API: https://www.figma.com/developers/api
- Figma Tokens plugin: https://tokens.studio/
- Design-to-code best practices: See repository design guidelines
- AC decomposition: `.github/skills/ac-decomposition/SKILL.md`
- JIRA analysis: `.github/skills/jira-pbi-analysis/SKILL.md`
