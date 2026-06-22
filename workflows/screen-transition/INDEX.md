# Architecture Reference — /t2c_screen_transition_tests

## Command Summary

This command generates screen transition test cases from a JIRA ticket.

### What It Produces
- Transition maps organized by scenario and branch
- Test cases with explicit `From Screen`, `Action`, and `To Screen`
- AC coverage matrix with step-level traceability (`AC -> TC -> Step`)
- Two-phase output for `Pre-Dev` draft planning and `Post-Dev` implementation-aware validation

## Start Here

- Entry command: `ticket2code/screen-transition-tests/t2c_screen_transition_tests.prompt.md`
- Agent behavior: `ticket2code/screen-transition-tests/screen-transition-tests-agent.md`
- Processor schema: `ticket2code/screen-transition-tests/screen-transition-tests-processor.prompt.md`

## Workflow Summary

1. Select communication language
2. Select execution phase (`Pre-Dev` or `Post-Dev`)
3. Fetch and parse ticket AC
4. Build screen transition map
5. Generate transition-focused test cases
6. Validate AC coverage with step-level traceability

## Core workflow definitions

- `agent-specs/01-stages.md`
- `.github/skills/ac-decomposition/SKILL.md`
- `agent-specs/02-test-categorization.md`
- `.github/skills/test-environment-designer/SKILL.md`
- `agent-specs/03-test-sequence-rules.md`
- `agent-specs/04-coverage-rules.md`

## Processor workflow definitions

- `processor-specs/02-section-1-overview.md`
- `processor-specs/03-section-2-categories.md`
- `processor-specs/04-section-3-environment.md`
- `processor-specs/05-section-4-test-cases.md`
- `processor-specs/06-section-5-coverage.md`

## Output

`docs/test/screen-transition/<TICKET-ID>_screen_transition_tests_<predev|postdev>_<YYYYMMDDHHmm>.md`
