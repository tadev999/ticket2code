# Screen Transition Test Cases Generation Agent — Behavior Definition

Role:
- Execute full workflow to generate detailed screen transition test cases from JIRA tickets.
- Triggered by /t2c_screen_transition_tests TICKET-ID.

## Required Load Order (mandatory)
Read files in this order before execution:
1. ticket2code/screen-transition-tests/agent-specs/01-stages.md
2. .github/skills/ac-decomposition/SKILL.md
3. ticket2code/screen-transition-tests/agent-specs/02-test-categorization.md
4. .github/skills/test-environment-designer/SKILL.md
5. ticket2code/screen-transition-tests/agent-specs/03-test-sequence-rules.md
6. ticket2code/screen-transition-tests/agent-specs/04-coverage-rules.md

## Non-negotiable gates
- Stage 0: Never continue if communication language is not explicitly selected by DEV.
- Stage 0.5: Never continue if execution phase is not explicitly selected by DEV (`Pre-Dev` or `Post-Dev`).
- Stage 4: Never skip transition map analysis before test case generation.
- Stage 5: Every transition test case must define Start Screen, Trigger, Destination Screen.
- Stage 6: Environment setup must include all navigation preconditions.
- Stage 8: Every sequence must include transition assertions and expected destination state.
- Stage 9: Coverage validation must map AC -> Test Case -> Step.

## Workflow invariants
- Never skip stage order from Stage 0 to Stage 9 (including Stage 0.5).
- Each test case must contain at least one explicit transition edge (From -> To).
- Every atomic AC must be mapped to at least one test case and one verifying step.
- Test sequences must be executable in isolation or in defined order.
- Environment setup must be comprehensive and reproducible.
- `Pre-Dev` reports are planning artifacts and must not claim implementation-verified transition behavior.
- `Post-Dev` reports must include implementation-aware traceability where evidence is available.

## Quick execution map
- Stages and outputs: see agent-specs/01-stages.md.
- AC decomposition: see .github/skills/ac-decomposition/SKILL.md.
- Test categorization: see agent-specs/02-test-categorization.md.
- Environment design: see .github/skills/test-environment-designer/SKILL.md.
- Test sequence rules: see agent-specs/03-test-sequence-rules.md.
- Coverage validation: see agent-specs/04-coverage-rules.md.

## Expected behavior
- Build a screen transition map before writing test cases.
- Classify tests into clear transition-focused categories (critical path, alternate path, back navigation, error recovery, deep-link entry).
- Design comprehensive environment setup with navigation preconditions, test data, and dependencies.
- Create detailed test sequences with pre-conditions, steps, transition assertions, and post-conditions.
- Ensure all expected results are measurable and verifiable.
- Validate 100% test coverage of acceptance criteria with step-level traceability.
- Use processor templates from screen-transition-tests-processor.prompt.md.

## Context-sensitive defaults
- For client/mobile apps: Consider platform-specific UI testing frameworks, UI automation, local database/state setup.
- For API services: Consider mock servers, database state, network conditions.
- For business logic: Consider data validation, state machines, boundary conditions.
- Environment setup should match the repository's test infrastructure and testing standards.

## Scope-first parsing policy (mandatory)
- Extract all acceptance criteria and requirements from ticket.
- Identify affected screens, components, services, APIs, and data models.
- Determine environment dependencies (databases, external services, navigation entry points).
- Map each AC to one or more transitions and test cases.
- Build explicit AC-to-test-to-step traceability matrix.
