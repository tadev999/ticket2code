---
title: Integration Test Cases Processor — Output Templates
---

# Integration Test Cases Processor — Output Templates

This is the entrypoint for report schema and templates used by /t2c_integration_tests.

## Required Load Order (mandatory)
Read files in this order before composing report sections:
1. ticket2code/integration-tests/processor-specs/01-language-and-convention.md
2. ticket2code/integration-tests/processor-specs/02-section-1-overview.md
3. ticket2code/integration-tests/processor-specs/03-section-2-categories.md
4. ticket2code/shared/processor-specs/04-section-3-environment.md
5. ticket2code/integration-tests/processor-specs/05-section-4-test-cases.md
6. ticket2code/integration-tests/processor-specs/06-section-5-coverage.md
7. ticket2code/shared/processor-specs/07-decision-gates.md

## Non-negotiable report requirements
- Use one report file per ticket at docs/test/integration/<TICKET-ID>_integration_tests_<predev|postdev>_<YYYYMMDDHHmm>.md.
- Always include Section 1 (Overview) with test plan summary.
- Always include Section 2 (Test Categories) with clear classification.
- Always include Section 3 (Environment Setup) with reproducible procedures.
- Always include Section 4 (Test Cases) with complete sequences and expected results.
- Always include Section 5 (Coverage Analysis) validating all AC are covered.
- Always include explicit report mode fields: `Selected execution phase`, `Report mode`, and `Confidence level`.
- Use consistent terminology and formatting across all sections.

## Workflow invariants
- One ticket maps to exactly one test plan report per run.
- Each test case must belong to exactly one category.
- Every atomic AC must be referenced in coverage analysis.
- Environment setup procedures must be complete and testable.
- Test sequences must be numbered and clearly separated.
- `Pre-Dev` mode must include assumptions, unknowns, and re-validation-required checklist.
- `Post-Dev` mode must include implementation-aware traceability references where available.

## Delegation map
- Section 1 template: processor-specs/02-section-1-overview.md
- Section 2 template: processor-specs/03-section-2-categories.md
- Section 3 template: ticket2code/shared/processor-specs/04-section-3-environment.md
- Section 4 template: processor-specs/05-section-4-test-cases.md
- Section 5 template: processor-specs/06-section-5-coverage.md
- Decision gates: ticket2code/shared/processor-specs/07-decision-gates.md
