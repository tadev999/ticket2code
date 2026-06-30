---
name: design-image-ocr-analysis
description: "Analyze local design screenshots/images from a folder using model vision, Python+OpenCV image analysis, or manual specs. Produces implementation-oriented design specs and AC traceability with graceful degradation when vision is unavailable."
argument-hint: "Screenshot/image folder path (recommended: docs/figma_design_analysis/<TICKET-ID>_screenshots/)"
user-invocable: false
disable-model-invocation: false
---

# Design Image OCR Analysis

## Scope
This skill handles screenshot/image-folder analysis only.

For direct Figma API analysis, use:
- `.github/skills/figma-design-analysis/SKILL.md`

## What This Skill Produces
- A structured design specification document (markdown).
- **Implementation-ready layout specifications:**
  - Screen/frame specs (device, dimensions, safe areas)
  - Component layout specs (position, size, constraints)
  - Spacing/padding/margin specifications
  - Typography details (font, size, weight, color, line height)
  - Visual properties (colors, borders, shadows, opacity)
  - Responsive/adaptive rules
  - Formatted as markdown tables or JSON for direct use in coding
- OCR-extracted visible text, labels, and annotation notes.
- Inferred component hierarchy and layout relationships.
- Visual token estimates (colors/typography/spacing) with confidence notes.
- Accessibility and UX notes based on image evidence.
- AC-to-design traceability mapping with screenshot filename references.

## When To Use
Use this skill when:
- DEV provides screenshots/images instead of Figma links.
- `FIGMA_TOKEN` is missing or direct Figma API access is not desired.
- Figma API access fails/rate-limits and DEV wants to proceed from images.
- Ticket has redline/annotated screenshots under docs.

## Required Inputs
- A local folder containing images (recommended):
  - `docs/figma_design_analysis/<TICKET-ID>_screenshots/`
- Supported image formats:
  - `.png`, `.jpg`, `.jpeg`, `.webp`
- Runtime dependencies:
  - `Python 3.8+` with `opencv-python`, `numpy`, `pillow` packages
  - `scikit-image` for edge detection and contour analysis
  - Install: `pip install opencv-python numpy pillow scikit-image`
- Optional:
  - `notes.md` inside the folder for manual annotations/assumptions

## Vision Capability & Fallback Options

This skill has three operational modes depending on available capabilities:

### Mode 1: Primary - Model Vision + AI Analysis (Full-Featured)
- **Requirements:**
  - Model with vision/image reading capability enabled
  - Images in local folder (no external dependencies)
- **Process:**
  - Model reads each image using vision API
  - AI extracts and analyzes: text, layout, components, colors, typography
  - Produces: Complete implementation layout specs (markdown tables + JSON)
- **Advantages:**
  - Most accurate, semantic understanding
  - Fastest execution
  - Full spec extraction without manual input
  - Best layout detail extraction
- **Fallback trigger:**
  - If model vision fails or returns error → fallback to Mode 2

### Mode 2: Secondary - Python + OpenCV Image Analysis (Visual + Text)
- **Requirements:**
  - `Python 3.8+` with libraries: `opencv-python`, `numpy`, `pillow`, `scikit-image`
  - Python available in system `PATH`
  - Install: `pip install opencv-python numpy pillow scikit-image`
- **Process:**
  1. Run Python OpenCV analysis script on screenshot folder
  2. Extract: component boundaries (contour detection), colors (pixel sampling), text regions (OCR via pytesseract optional)
  3. Infer: layout structure from edges, hierarchy from positioning, colors from dominant palette
  4. Combine: automated analysis + optional manual refinements in `notes.md`
  5. Produce: design document with colors, spacing estimates, component layout
- **Advantages:**
  - No model vision required
  - Better than pure Tesseract: detects colors, borders, shadows, layout structure
  - Good accuracy (~70-80%) for components, colors, spacing
  - Hybrid: can combine with manual notes for refinement
  - Deterministic (Python same behavior across platforms)
- **Limitations:**
  - Estimated spacing/padding (visual inference, not pixel-perfect)
  - Semantic understanding not perfect (may misidentify components)
  - Requires Python + OpenCV installed locally
  - Manual refinement often needed for complex designs
- **Optional user input format (in `notes.md` for refinement):**
  ```markdown
  ## Layout Refinements
  
  ### Screen: SAMPLE-001_ExampleScreen
  # Device and safe areas auto-detected; add corrections here if needed
  Device: iPhone 14 (390×844)  # Detected from image, verify
  Safe Area: top=47pt, bottom=34pt  # Add if auto-detection missed
  
  ### Component: ActionButton
  # Position/size auto-detected from contours; refine text/semantic here
  Semantic role: Primary action button
  Text content: Submit
  Font refinement: SF Pro Display Bold (if misdetected)
  ```
- **Fallback trigger:**
  - If model vision not available → offer Mode 2

### Mode 3: Fallback - DEV Manual Specifications Only
- **Requirements:**
  - User provides complete manual specification
  - Input format: JSON or markdown table
  - No Python+OpenCV or model vision available
- **Process:**
  1. Request DEV to provide full layout specifications
  2. Ask for manual descriptions of each screen/component
  3. Parse provided specs → generate design document
- **Advantages:**
  - Works in all environments
  - No dependencies required
  - Guaranteed to work
- **Limitations:**
  - Requires significant DEV effort
  - Slower (manual input)
  - Higher error risk (human transcription)
  - No visual verification available
- **User input template:**
  ```json
  {
    "ticket": "PROJ-1234",
    "screens": [
      {
        "name": "SAMPLE-001_ExampleScreen",
        "device": "iPhone 14",
        "dimensions": {"width": 390, "height": 844},
        "components": [
          {
            "name": "HeaderView",
            "position": {"top": 100, "left": 0},
            "size": {"width": 390, "height": 120},
            "backgroundColor": "#FFFFFF",
            "border": {"width": 1, "color": "#E0E0E0"}
          }
        ]
      }
    ]
  }
  ```
- **Fallback trigger:**
  - If Mode 1 (vision) fails AND Mode 2 (tesseract) unavailable

### Capability Detection & Fallback Logic
```
1. **Check Model Vision Capability**
   - Attempt to read a test image or first screenshot
   - If success → Use Mode 1 (full AI analysis)
   - If fail (error/disabled) → Continue to Step 2

2. **Check Python + OpenCV**
   - Run: `python3 --version && python3 -c "import cv2; import numpy; import PIL; import skimage"`
   - If available → Offer Mode 2 (Python + OpenCV automated analysis)
   - If not available (missing Python or libraries) → Continue to Step 3
   - If OpenCV missing: suggest `pip install opencv-python numpy pillow scikit-image`

3. **Request DEV Manual Input**
   - Offer Mode 3 (full manual specifications)
   - Provide template (JSON or markdown)
   - Ask: "Please provide complete layout specifications for this design"

4. **Graceful Degradation Message**
   - Document which modes are available:
     - "Model vision: [Available / Disabled / Not Supported]"
     - "Python + OpenCV: [Available / Not Found / Libraries Missing]"
     - "Fallback mode: Requesting manual specifications"
```

### Recommended Mode Selection by Scenario

| Scenario | Recommended Mode | Why |
|---|---|---|
| GitHub Copilot with vision enabled | Mode 1 | Fastest, most accurate (95%+) |
| Model without vision, Python + OpenCV available | Mode 2 | Good accuracy (70-80%) for colors, layout, spacing |
| Model without vision, Python not available | Mode 3 | Manual input required |
| Enterprise with vision disabled, Python available | Mode 2 | Compliance-friendly, good analysis |
| Local development, Python + OpenCV installed | Mode 2 + Mode 1 | Hybrid approach for reliability |
| All capabilities unavailable | Mode 3 | Only reliable option |

## CLI Execution

### Mode 1: Model Vision (Automatic via AI)
- No manual CLI execution needed; invoked by the AI model

### Mode 2: Python + OpenCV Analysis
Run the Python analysis script:

```bash
python3 ./.github/skills/design-image-ocr-analysis/scripts/image_analyze.py \
  --input-folder docs/figma_design_analysis/<TICKET-ID>_screenshots \
  --ticket-id <TICKET-ID>
```

Optional flags:
- `--output docs/design/<TICKET-ID>_image_analysis_<YYYYMMDDHHmm>.md`
- `--confidence-threshold 0.5` (0.0-1.0, default 0.5)
- `--extract-text` (attempt OCR on detected text regions with pytesseract if available)
- `--debug` (output intermediate images for inspection)

### Mode 3: Manual Specifications
- No CLI execution; user provides specs directly

## Output Principles
- Explicitly distinguish:
  - `extracted from annotation/text`
  - `estimated from screenshot`
- Cite source filename for each important extracted rule.
- Preserve filename order where names encode states/steps.

## Suggested Folder Structure
```text
docs/figma_design_analysis/<TICKET-ID>_screenshots/
├── 01_default.png
├── 02_error.png
├── 03_small_device.png
└── notes.md
```

## Procedure

### Vision Capability Check (First Step)
- Before processing images:
  1. Check: Does model support vision/image reading? (try reading test image)
  2. Check: Is Python + OpenCV available? (test imports: `opencv`, `numpy`, `PIL`, `scikit-image`)
  3. Determine operating mode:
     - If model vision available → Use Mode 1 (full AI analysis)
     - Else if Python + OpenCV available → Offer Mode 2 (automated image analysis)
     - Else → Fall back to Mode 3 (manual specifications)
- Document capability status upfront to DEV
- Never proceed silently; always inform DEV of mode and any limitations
- If Python/OpenCV missing: suggest `pip install opencv-python numpy pillow scikit-image`
- If install command fails with proxy-related error (`407`, `proxy`, `tunnel`, SSL/certificate error via proxy), stop and ask DEV for proxy info before retrying.

### Input Validation
1. Verify folder exists.
2. Enumerate supported image files.
3. If no supported files found, ask DEV to add valid images.
4. Read optional `notes.md` when present.

### OCR + Visual Extraction
- **Mode 1 (Model Vision):**
  1. For each image:
     - Use model vision to read and analyze image
     - Extract visible text and labels
     - Capture dimensions and filename
     - Detect state cues from filename/annotations
  2. Infer layout relationships:
     - grouping and hierarchy
     - spacing patterns
     - responsive differences across images
  3. Record confidence:
     - explicit annotation/text values = high confidence
     - visual estimates = medium/low confidence
- **Mode 2 (Python + OpenCV):**
  1. Load image and convert to appropriate color space
  2. Detect edges and contours to identify component boundaries
  3. Extract dominant colors from regions (color quantization)
  4. Infer text regions (edge density, aspect ratio heuristics)
  5. Measure positions and sizes from contour bounding boxes
  6. Optionally extract text from regions using pytesseract if available
  7. Combine automated analysis + optional manual notes
- **Mode 3 (Manual Specs):**
  1. Request DEV to provide complete specifications
  2. Parse provided format (JSON or markdown)

### Analyze Components
1. Build component/state catalog from multi-image comparison.
2. Document state deltas (default/error/disabled/small-device/etc.).
3. Capture constraints and truncation clues from image evidence.

### Extract Implementation Layout Specification
This step produces concrete layout specs that developers can use directly for coding.

**For each screen/frame in the images:**

1. **Screen/Frame Specifications:**
   - Device type/platform (iPhone 14, iPad, Android, etc.) - infer from image dimensions if available
   - Screen dimensions: width × height (in points or pixels)
   - Safe areas: top (status bar), bottom (home indicator), left, right
   - Notch/Dynamic Island presence and impact on layout

2. **Component Layout Mapping:**
   - For each major UI component/view:
     - Component name/identifier (inferred from context or AC reference)
     - Position on screen: top, left (absolute or relative positioning)
     - Dimensions: width, height (fixed, percentage, or flexible)
     - Z-index/stacking order (front to back)
   - Estimated from visual inspection (document confidence level)

3. **Spacing & Constraints:**
   - Padding (within component): top, bottom, left, right
   - Margin (outside component): top, bottom, left, right
   - Gaps between components/list items
   - Layout constraints:
     - Fixed size vs flexible/adaptive
     - Alignment: left, center, right, top, bottom, fill
     - Distribution: equal spacing, justified, etc.

4. **Typography Specifications:**
   - For each text element:
     - Font family name (estimated: San Francisco, Roboto, etc.)
     - Font size (in points/SP)
     - Font weight (regular, medium, bold, etc.)
     - Line height (in points or as multiplier)
     - Letter spacing (if visible)
     - Text color and opacity (hex or RGB, with alpha if semi-transparent)
     - Text alignment (left, center, right, justified)

5. **Visual Properties:**
   - Background colors/gradients: color values, transparency
   - Border: width (in points), color, style (solid, dashed, etc.)
   - Border radius (corner rounding): all corners or per-corner
   - Shadows: blur radius, offset (x, y), color, opacity
   - Opacity levels for views/components

6. **Responsive/Adaptive Rules:**
   - How layout changes across different screen sizes
   - Components that resize vs reflow vs hide
   - Orientation changes (portrait vs landscape)
   - Multi-state transitions (default, error, disabled, loading, etc.)

7. **Output Format - Implementation Specs Document:**
   - Generate a markdown table or structured list with all specs
   - Example markdown format:
     ```markdown
     ## SAMPLE-001_ExampleScreen - iPhone Layout Specs
     
     ### Screen Properties
     | Property | Value |
     |---|---|
     | Device | iPhone 14 |
     | Width | 390pt |
     | Height | 844pt |
     | Safe Area Top | 47pt |
     | Safe Area Bottom | 34pt |
     
     ### Component: HeaderView
     | Property | Value |
     |---|---|
     | Position | (0, 100) |
     | Size | 390×120 |
     | Background Color | #FFFFFF |
     | Padding | 12,12,12,12 |
     | Border | 1pt #E0E0E0 |
     
     ### Component: ActionButton
     | Property | Value |
     |---|---|
     | Position | (16, 700) |
     | Size | 358×56 |
     | Background Color (enabled) | #0066FF |
     | Background Color (disabled) | #CCCCCC |
     | Corner Radius | 12pt |
     | Text: Font | SF Pro Display, 16pt, Bold |
     | Text: Color | #FFFFFF |
     ```
   - Alternative: JSON format for machine-readable specs (if DEV prefers)
   - Always cite source screenshot filename for each spec

### Cross-Reference with JIRA
1. Map JIRA AC to screenshot-derived components/states.
2. Flag AC without visual evidence.
3. Flag visual behaviors not covered in AC.

### Generate Output Report
1. Write report sections equivalent to design analysis schema.
2. Include implementation layout specification section (from Extract Implementation Layout Specification step).
3. Include filename-based traceability for all specs.
4. Mark uncertain values as `estimated from screenshot` with confidence levels (high/medium/low).
5. Provide markdown tables and/or JSON snippets for direct use in implementation.
6. Save to: `docs/design/<TICKET-ID>_image_ocr_analysis_<YYYYMMDDHHmm>.md`
7. Optional: Generate companion `<TICKET-ID>_layout_specs.json` for programmatic access.

## Integration with /t2c_code
- Stage 1.5 design source choice:
  - If DEV selects screenshot folder input, use this skill.
- Stage 2.5:
  - Run this skill without requiring `FIGMA_TOKEN`.
- Output integration:
  - Implementation layout specs are ready for direct use during code generation
  - Developers can reference markdown tables or JSON output when writing layout code
  - AC-to-design mapping helps verify implementation completeness

## Error Handling
- **Model vision not available/disabled:**
  - Document: "Model vision capability unavailable in current environment"
  - Check Python + OpenCV availability automatically
  - If Python + OpenCV available: offer Mode 2 (automated image analysis)
  - If Python + OpenCV unavailable: fall back to Mode 3 (request manual specs)
- **Python + OpenCV not found:**
  - Document: "Python not in PATH" or "Required libraries missing: opencv-python, numpy, pillow, scikit-image"
  - Suggest: `pip install opencv-python numpy pillow scikit-image`
  - If install fails because of proxy restrictions (`407 Proxy Authentication Required`, `proxy connect`, `tunnel connection failed`, `CERTIFICATE_VERIFY_FAILED` in corporate network), ask DEV to provide:
    - Proxy URL (`http://host:port` or `https://host:port`)
    - Whether proxy authentication is required
    - `NO_PROXY` list
    - Custom CA certificate requirement
  - Apply provided proxy configuration and retry once only
  - If DEV refuses to install: fall back to Mode 3 (request manual specifications)
- **OpenCV analysis fails (corrupted image, unsupported format):**
  - Document: "Could not analyze image: [reason]" with filename
  - Suggest: provide different screenshot format or try manual inspection
  - Continue with other images if batch processing
- Missing folder: ask DEV to provide correct path.
- No supported images: ask DEV to add supported files.
- Unreadable image quality (Mode 1): ask for clearer exports/annotated crop.
- Unreadable image quality (Mode 2/3): request clearer descriptions or annotated crops.
- Conflicts between screenshots and ticket text: report explicitly and ask which is authoritative.
- **Vision capability check failure:**
  - Do not silently skip; document reason
  - Always offer alternative fallback modes
  - Ask DEV: "Would you like to use Mode 2 (Python + OpenCV) or Mode 3 (manual specs only)?"

## References
- Figma API skill: `.github/skills/figma-design-analysis/SKILL.md`
- JIRA analysis: `.github/skills/jira-pbi-analysis/SKILL.md`
- AC decomposition: `.github/skills/ac-decomposition/SKILL.md`
