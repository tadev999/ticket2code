# Decision Labels Dictionary

Purpose:
- Provide a single source of truth for DEV-facing option labels used in decision gates.
- Prevent wording drift across Stage 6, Stage 10.5, and Stage 12.

Usage rules:
- Keep keys stable once published.
- Reuse labels by key in processor-specs/06-decision-gates.md.
- If a label text changes, update this file first, then update consuming gates.

Dictionary:
{
  "stage6": {
    "yes_generate_code": "Yes, generate code",
    "adjust_analysis": "Adjust analysis",
    "add_files": "Add files",
    "cancel": "Cancel"
  },
  "stage10_5": {
    "yes_run_tests": "Yes, run tests now",
    "no_defer_ci": "No, defer to CI build"
  },
  "stage12": {
    "yes_generate_commit_summary": "Yes, generate commit summary",
    "no_finalize_without_summary": "No, finalize workflow without summary"
  }
}