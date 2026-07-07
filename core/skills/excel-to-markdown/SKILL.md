---
name: excel-to-markdown
description: "Convert Excel/CSV attachments into markdown tables with sheet-level outputs and row/column references for requirement analysis and reporting workflows."
argument-hint: "Input file path (.xlsx/.xls/.csv), optional output path, and ticket ID"
user-invocable: false
disable-model-invocation: false
---

# Excel To Markdown

## What This Skill Produces
- Markdown tables converted from spreadsheet files.
- A deterministic evidence artifact for requirement analysis reports.
- Optional per-sheet markdown files for large workbooks.
- Source references in the form:
  - `attachment:<filename> > sheet:<sheet-name> > row:<n> > col:<letter>`

## When To Use
Use this skill when:
- a PBI contains supplemental Excel/CSV attachments with business rules, mappings, test data, or acceptance matrices
- a report must cite spreadsheet evidence explicitly
- spreadsheet content must be normalized before analysis by other skills

## Supported Inputs
- `.xlsx` (primary)
- `.xls` (best-effort, requires compatible engine)
- `.csv`

## CLI
Run the converter script:

```bash
python3 ./core/skills/excel-to-markdown/scripts/excel_to_markdown.py \
  --input <path/to/file.xlsx> \
  --output <path/to/output.md>
```

Optional flags:
- `--max-rows 500` limit rows per sheet in output
- `--max-cols 30` limit columns per sheet in output
- `--encoding utf-8` CSV encoding override

## Dependencies
- `.xlsx` requires `openpyxl`; legacy `.xls` requires `xlrd`. Install with `pip install openpyxl xlrd`.
- Behind a corporate proxy, run the network preflight first so `pip` inherits proxy/CA settings from `.env.local`:
  ```bash
  [ -f .env.local ] && set -a && . ./.env.local && set +a
  ```

## Procedure
1. Validate input file exists and extension is supported.
2. Load workbook/sheet data in stable order.
3. Normalize cell values:
   - trim trailing spaces
   - convert empty cells to empty string
   - stringify numeric/date values consistently
4. Render markdown tables per sheet.
5. Prepend sheet metadata:
   - original filename
   - sheet name
   - row/column count (after truncation if applicable)
6. Save markdown output to the requested path.
7. Return a short summary for downstream report sections.

## Output Principles
- Preserve worksheet order as in source file.
- Keep headers from row 1 when available.
- If no clear header is present, generate fallback headers: `Column A`, `Column B`, ...
- Do not silently skip unreadable sheets; surface them in limitations.

## Error Handling
- If input is unsupported or unreadable:
  - return explicit failure reason
  - mark as `Attachment Limitations` in the parent report
- If output truncation is applied:
  - report applied limits (`max-rows`, `max-cols`)
  - include truncation note in the markdown output

## Report Integration Contract
When this skill is used by requirement/report workflows:
- Report must include:
  - converted markdown artifact path
  - list of sheets parsed
  - key findings traced to sheet + row references
