---
agent: agent
description: Conduct a code review
---

# /review — Conduct a code review

This prompt is a thin entry point for review execution in this repository.

## Primary references

- Follow `docs/review/review_target_rule.md` to determine the exact diff to review.
- Follow `docs/codeReviewGuideline.md` for review criteria and report-file rules.
- Consult `docs/release_bugs/` for past incident facts and recurrence notes.
- Consult `docs/review_patterns/` for generalized review checklists extracted from past incidents.

## Output reminder

- Findings must be reported first, ordered by severity, with file and line references when available.
- If the review process requires a report file, generate it under `docs/report/` using the timestamp rule from `docs/codeReviewGuideline.md`.

