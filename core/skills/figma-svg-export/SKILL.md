---
name: figma-svg-export
description: "Export a Figma frame/component/node to SVG using the Figma REST API when MCP is unavailable. Use for Jira/Figma links, design handoff, and reproducible local asset extraction."
argument-hint: "Figma file URL or file key, node ID, and output path"
user-invocable: true
disable-model-invocation: false
---

# Figma SVG Export

## What This Skill Produces
- A locally downloaded SVG file exported from a specific Figma node.
- A reproducible export path that does not depend on Figma MCP.
- Clear limitations when the link cannot be resolved or the node cannot be exported.

## When To Use
Use this skill when you need to:
- export a Figma frame/component/vector as SVG
- work from a Figma link inside Jira comments or ticket description
- prepare a local artifact for visual review or downstream analysis
- compensate for missing Figma MCP integration

Typical triggers:
- "export this Figma node to svg"
- "use the Figma link in the PBI"
- "download the design as SVG"

## Required Inputs
- `FIGMA_TOKEN` available in the environment
- One of:
  - a full Figma URL that contains the file key and `node-id`
  - a `FILE_KEY` plus `NODE_ID`
- Optional:
  - output path for the SVG file

## Support Policy
- Supported:
  - static node export via Figma Images API with `format=svg`
  - file URLs that expose `file key` and `node-id`
- Not supported:
  - prototype/video playback export
  - exporting arbitrary interactive flows as SVG without a concrete node id
  - private files/nodes without access token permission

## Preferred Local Script
Use the OS-aware wrapper entrypoint when possible:

`./.github/skills/figma-svg-export/scripts/figma_export_svg`

On Windows Command Prompt / PowerShell launcher contexts:

`./.github/skills/figma-svg-export/scripts/figma_export_svg.cmd`

Underlying scripts are also available:

`./.github/skills/figma-svg-export/scripts/figma_export_svg.sh`

`./.github/skills/figma-svg-export/scripts/figma_export_svg.ps1`

### Examples

Using a Figma URL:

```bash
FIGMA_TOKEN=... ./.github/skills/figma-svg-export/scripts/figma_export_svg \
  --figma-url "https://www.figma.com/design/FILE_KEY/Title?node-id=12-345" \
  --output docs/assets/figma-node.svg
```

Using file key and node id directly:

```bash
FIGMA_TOKEN=... ./.github/skills/figma-svg-export/scripts/figma_export_svg \
  --file-key FILE_KEY \
  --node-id 12:345 \
  --output docs/assets/figma-node.svg
```

Using PowerShell with a Figma URL:

```powershell
$env:FIGMA_TOKEN="..."
./.github/skills/figma-svg-export/scripts/figma_export_svg.cmd `
  -FigmaUrl "https://www.figma.com/design/FILE_KEY/Title?node-id=12-345" `
  -Output "docs/assets/figma-node.svg"
```

Using PowerShell with file key and node id directly:

```powershell
$env:FIGMA_TOKEN="..."
./.github/skills/figma-svg-export/scripts/figma_export_svg.cmd `
  -FileKey "FILE_KEY" `
  -NodeId "12:345" `
  -Output "docs/assets/figma-node.svg"
```

## Procedure
1. Resolve file key and node id.
2. Validate that `FIGMA_TOKEN` is present.
3. Call Figma Images API with `format=svg`.
4. Download the returned signed URL to a local `.svg` file.
5. If export fails, record the cause explicitly.

## Exact Command Suggestion Rule
- If a Figma URL is already known, suggest an exact ready-to-run command, not just general guidance.
- Prefer `figma_export_svg` wrapper for bash/zsh environments.
- Prefer `figma_export_svg.cmd` wrapper for Windows Command Prompt or PowerShell launcher contexts.
- Fall back to direct `.sh` or `.ps1` scripts only when wrapper usage is not suitable.
- If output path is not specified by DEV, suggest a deterministic default such as `docs/assets/figma-<node>.svg`.

## Decision Gates
- If the Figma URL does not contain a usable node id:
  - stop and ask DEV for a specific node id
- If the API returns no export URL:
  - stop and report the node could not be exported
- If token/access is missing:
  - stop and ask DEV to provide valid Figma access outside chat

## Output Expectations
- Report the final SVG path.
- Report the resolved file key and node id.
- If export fails, separate confirmed facts from assumptions.
