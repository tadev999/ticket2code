# Architecture Reference — /t2c_integration_tests workflow

This index is the canonical navigation file for the modularized /t2c_integration_tests system.

## Command Summary

This command generates professional integration test plans from a JIRA ticket.

### What It Produces
- Categorized integration test suites mapped to ticket requirements
- Environment setup documentation including preconditions, configuration, test data, and mocks
- Detailed test sequences with explicit actions, expected results, and assertions
- Coverage analysis with AC-to-test traceability
- Two-phase output for `Pre-Dev` planning and `Post-Dev` implementation-aware validation

### Prerequisites
- Configure `.env.local` with JIRA credentials
- Prepare `docs/test/integration/` as the output directory
- Define repository-specific testing standards and reference docs as needed
- Follow shared setup guidance in `ticket2code/SETUP.md`

## Start here
- Entry command: `ticket2code/integration-tests/t2c_integration_tests.prompt.md`
- Agent entrypoint: `ticket2code/integration-tests/integration-tests-agent.md`
- Processor entrypoint: `ticket2code/integration-tests/integration-tests-processor.prompt.md`
- Setup: `ticket2code/SETUP.md`

## Workflow Map (Stage 0 -> Stage 9, with Stage 0.5 phase gate)

**Source of truth:** `ticket2code/integration-tests/agent-specs/01-stages.md`

### Stages Overview
1. **Select communication language** — Set AI-DEV communication language for this run
2. **Select execution phase** — Choose `Pre-Dev` (draft planning) or `Post-Dev` (implementation-aware validation)
3. **Fetch ticket** — Load JIRA ticket data
4. **Parse requirements** — Extract AC and business logic
5. **Analyze test requirements** — Identify test scope and dependencies
6. **Generate analysis report** — Create initial test plan overview
7. **Categorize tests** — Define non-overlapping test categories
8. **Design environment setup** — Specify preconditions, config, test data, mocks
9. **Generate test sequences** — Write detailed test cases with steps
10. **Define expected results** — Specify measurable outcomes and assertions
11. **Validate coverage** — Ensure all AC are covered by tests

### Decision Gates
- **Gate 0.5** (after Stage 0): Confirm execution phase (`Pre-Dev` or `Post-Dev`)
- **Gate 1** (after Stage 4): Approve analysis and test categories
- **Gate 2** (after Stage 6): Approve environment setup
- **Gate 3** (after Stage 8): Approve test sequences
- **Gate 4** (after Stage 9): Approve coverage/sign-off for selected phase

**Important rule:** If a gate choice is not explicit, workflow must stop and must not assume Yes/No.

## Agent workflow definitions
1. `ticket2code/integration-tests/agent-specs/01-stages.md` — Stage definitions
2. `.github/skills/ac-decomposition/SKILL.md` — Breaking AC into testable units
3. `ticket2code/integration-tests/agent-specs/02-test-categorization.md` — Test classification system
4. `.github/skills/test-environment-designer/SKILL.md` — Test environment setup rules
5. `ticket2code/integration-tests/agent-specs/03-test-sequence-rules.md` — Writing test cases
6. `ticket2code/integration-tests/agent-specs/04-coverage-rules.md` — Test coverage validation

## Processor workflow definitions
1. `ticket2code/integration-tests/processor-specs/01-language-and-convention.md` — Language style and naming conventions
2. `ticket2code/integration-tests/processor-specs/02-section-1-overview.md` — Executive summary template
3. `ticket2code/integration-tests/processor-specs/03-section-2-categories.md` — Test categories documentation
4. `ticket2code/integration-tests/processor-specs/04-section-3-environment.md` — Environment setup documentation
5. `ticket2code/integration-tests/processor-specs/05-section-4-test-cases.md` — Test case specifications
6. `ticket2code/integration-tests/processor-specs/06-section-5-coverage.md` — Coverage analysis and matrix
7. `ticket2code/integration-tests/processor-specs/07-decision-gates.md` — Decision points and sign-off

## Output Artifacts

### Report Location
```
docs/test/integration/<TICKET-ID>_integration_tests_<predev|postdev>_<YYYYMMDDHHmm>.md
```

### Report Structure
```
Section 1: Overview
  - Executive summary
  - Test statistics
  - Test categories overview
  - AC summary
  - Dependencies
  - Coverage goals

Section 2: Test Categories
  - Category definitions and scope
  - Category-to-AC mapping
  - Distribution analysis

Section 3: Environment Setup
  - Pre-conditions
  - Configuration (DB, API, ENV vars)
  - Test data fixtures
  - External service mocks
  - Setup procedures (one-time, per-test, teardown)

Section 4: Test Cases
  - [For each test category]
    - Test case details (objective, pre-req, sequence, expected results, assertions)
  - Summary table
  - Variant cases (edge cases, error cases)

Section 5: Coverage Analysis
  - Coverage summary (percentage, status)
  - Coverage matrix (AC to test cases)
  - Coverage by category
  - AC-to-test traceability
  - Gap analysis
  - Coverage quality assessment
```

## Design Principles

1. **Modular:** Each concern (stages, categorization, environment, test sequences, coverage) is in separate module
2. **Explicit:** All rules and templates are documented, not implied
3. **Staged:** Clear gates ensure quality at each phase
4. **Testable:** All requirements are decomposed into measurable, verifiable units
5. **Traceable:** Every AC maps to test cases; every test case maps to AC

## Load Order (Mandatory)

### For Generating Test Plans
1. Read `integration-tests-agent.md` (defines load order)
2. Load agent-specs in order (01 through 06)
3. Read `integration-tests-processor.prompt.md` (defines report templates)
4. Load processor-specs in order (01 through 07)
5. Execute stages with processor templates

### For Reading Test Plans
1. Read Section 1 (Overview) for quick summary
2. Read Section 2 (Categories) to understand test organization
3. Read Section 3 (Environment) to understand setup
4. Read Section 4 (Test Cases) for detailed test specifications
5. Read Section 5 (Coverage) to understand coverage and traceability

## Key Concepts

### Acceptance Criteria (AC)
Requirements from JIRA ticket that tests must verify.

### Atomic AC
Smallest testable unit: one trigger + one condition + one expected output.
Each atomic AC must be decomposed before test planning.

### Test Categories
Non-overlapping classifications: UI/UX, Business Logic, Data Persistence, API Integration, Error Handling, Security, Performance, Integration, Edge Cases, Regression Prevention.

### Environment Setup
Complete specification of preconditions, configuration, test data, and mocks needed to run tests.

### Test Sequence
Step-by-step procedure with explicit actions and expected state changes for each step.

### Expected Results
Measurable outcomes covering user-visible, data, system, and timing aspects.

### Coverage
Mapping of all atomic AC to test cases ensuring 100% traceability and no orphaned tests.

## Related Workflows

### /t2c_code — Code Implementation Workflow
- Generates code implementation from JIRA ticket
- Applies the same AC decomposition and repository-specific engineering standards
- See `ticket2code/code/INDEX.md` for architecture

### /t2c_review — Code Review Workflow
- Reviews code changes against AC and repository-specific engineering standards
- Applies same AC decomposition
- See `ticket2code/review/INDEX.md` for architecture

## Integration with Project Ecosystem

### Consult These Documents
- Repository test strategy or test code rules
- Repository coding style or naming conventions
- Repository logging and error handling policy
- Review-pattern knowledge base for common issues to test for
- Incident or release-bug history for regression planning

## Troubleshooting

### If workflow stops at a gate
- Confirm gate question was presented explicitly
- Confirm stakeholder gave explicit Yes/No/Adjust choice
- If no explicit choice recorded, workflow must stop

### If coverage seems incomplete
- Verify all atomic AC were decomposed (see .github/skills/ac-decomposition/SKILL.md)
- Check coverage matrix for any unmapped AC
- Document gaps explicitly with justification

### If test categories seem wrong
- Verify each test case belongs to exactly one category
- Check that categories are mutually exclusive
- Review categorization rules in 02-test-categorization.md

### If environment setup is unclear
- Verify all preconditions are documented
- Check that setup procedures are step-by-step
- Ensure teardown procedures exist for cleanup

## Quick Reference

| Need | Go To |
|------|-------|
| Understand workflow | This file (INDEX.md) |
| Understand stages | 01-stages.md |
| Decompose AC | .github/skills/ac-decomposition/SKILL.md |
| Define test categories | 02-test-categorization.md |
| Design test environment | .github/skills/test-environment-designer/SKILL.md |
| Write test sequences | 03-test-sequence-rules.md |
| Validate coverage | 04-coverage-rules.md |
| Write overview section | 02-section-1-overview.md |
| Write categories section | 03-section-2-categories.md |
| Write environment section | 04-section-3-environment.md |
| Write test cases section | 05-section-4-test-cases.md |
| Write coverage section | 06-section-5-coverage.md |
| Understand decision gates | 07-decision-gates.md |

## Version History

- **v1.0** (2024-01-15): Initial system design for integration test generation
