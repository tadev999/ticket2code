---
title: Ticket Processor — Output Templates
---

# Ticket Processor — Output Templates

This is the entrypoint for report schema and templates used by /t2c_code.

## Required Load Order (mandatory)
Read files in this order before composing or appending report sections:
1. ticket2code/code/processor-specs/01-language-and-convention.md
2. ticket2code/code/processor-specs/02-section-1-analysis.md
3. ticket2code/code/processor-specs/03-section-2-evaluation.md
4. ticket2code/code/processor-specs/04-section-3-conclusion.md
5. ticket2code/code/processor-specs/05-decision-gates.md
6. ticket2code/code/processor-specs/06-validation-checklist.md
7. ticket2code/code/processor-specs/07-decision-labels.md

## Non-negotiable report requirements
- Use one report file per ticket at docs/report/<TICKET-ID>_reports_<YYYYMMDDHHmm>.md.
- Always include Section 1 before code generation.
- After code generation, append Section 2.1, 2.2, 2.3 (when applicable), 2.4, and Section 3.
- If commit summary is requested by DEV, append Section 4.
- Dead-code cleanup evidence (Section 2.4) is mandatory when removing/refactoring logic paths.

## Workflow invariants
- Section 1 must exist before any code-generation output is appended.
- Section 2.4 must include all mandatory cleanup evidence when logic paths are removed.
- Stage 10.5 and Stage 12 decisions must be explicit; no implied Yes/No states.
- One ticket maps to exactly one report file path format per run.

## Delegation map
- Section 1 template: processor-specs/02-section-1-analysis.md
- Section 2 templates: processor-specs/03-section-2-evaluation.md
- Section 3 template: processor-specs/04-section-3-conclusion.md
- Dead-code cleanup: see .github/skills/dead-code-cleanup/SKILL.md
- Decision gates: processor-specs/05-decision-gates.md
- Final validation checklist: processor-specs/06-validation-checklist.md
- Decision labels dictionary: processor-specs/07-decision-labels.md
