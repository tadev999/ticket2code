---
agent: t2c-screen-transition-tests-orchestrator
description: Generate professional screen transition test cases from JIRA ticket requirements via orchestrator agent and jira-pbi-analysis skill.
---

# /t2c_screen_transition_tests

**Type:** Slash-command entry point  
**Input:** `/t2c_screen_transition_tests TICKET-ID` (e.g., `/t2c_screen_transition_tests PROJ-1234`)

## What this command does

Generates screen transition focused test cases from a JIRA ticket:
1. Fetch ticket and parse all AC
2. Identify screen entries, exits, and branch points
3. Build explicit transition paths by scenario
4. Generate test cases with detailed execution steps:
   - **From Screen -> To Screen** per step
   - **Action/Trigger** that causes the transition
   - **Expected UI/System state** at destination screen
   - **Pre-condition and test data** for reproducibility
5. Build AC traceability:
   - Which test case covers which AC
   - Which steps verify that AC
6. Output report in markdown

## Setup required

Ensure these variables are set in `.env.local` at the repo root:
```
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your JIRA base URL>
```
See `ticket2code/SETUP.md` for step-by-step instructions.

## Behavior rules

- **Orchestrator agent** → `.github/agents/t2c-screen-transition-tests.agent.md`
- **Stage-by-stage behavior** → `ticket2code/screen-transition-tests/screen-transition-tests-agent.md`
- **Output templates and report schema** → `ticket2code/screen-transition-tests/screen-transition-tests-processor.prompt.md`
- **Requirement analysis skill** → `.github/skills/jira-pbi-analysis/SKILL.md`
- Mandatory first step: ask DEV which language to use for this run (for example: Vietnamese, English, Japanese).
- Mandatory second step: ask DEV which execution phase to use for this run (`Pre-Dev` or `Post-Dev`).
- Do not continue workflow stages until DEV explicitly selects a language.
- Do not continue workflow stages until DEV explicitly selects an execution phase.
- Use the selected language for all follow-up conversation and for the generated test report content in this run.
- Use the selected execution phase consistently for all gates, report labeling, and validation strictness.
- Generate tests following the repository's testing standards and conventions.
- Every test case must include explicit screen transitions (`From Screen`, `Action`, `To Screen`).
- Every test case must include AC mapping with step-level traceability.

### Two-phase model rules

- `Pre-Dev`: Use requirement-first planning mode when code for this ticket is not implemented yet.
- `Pre-Dev`: Mark report as draft planning artifact and include assumptions, unknowns, and re-validation checklist.
- `Pre-Dev`: Do not claim implementation-verified transition behavior.
- `Post-Dev`: Use implementation-aware mode when code is available and ready to validate.
- `Post-Dev`: Add evidence-based traceability (AC -> TC -> Step -> transition evidence).
- `Post-Dev`: Use full coverage sign-off gates.

## Output

Screen transition test cases are saved to:
```
docs/test/screen-transition/<TICKET-ID>_screen_transition_tests_<predev|postdev>_<YYYYMMDDHHmm>.md
```

The document includes:
- Screen transition map (entry points and branches)
- Detailed test procedures (screen-by-screen)
- AC coverage matrix (AC -> TC -> Step)
- Coverage gaps and risk notes

## Compatibility

- Slash command remains unchanged: `/t2c_screen_transition_tests TICKET-ID`
- Existing report location and naming remain unchanged.
