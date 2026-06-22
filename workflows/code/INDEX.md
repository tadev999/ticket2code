# Architecture Reference — /t2c_code workflow

This index is the canonical navigation file for the modularized /t2c_code system.

## Start here
- Entry command: ticket2code/code/t2c_code.prompt.md
- Agent entrypoint: ticket2code/code/code-agent.md
- Processor entrypoint: ticket2code/code/code-processor.prompt.md
- Setup: ticket2code/SETUP.md

## Current workflow map (Stage 0 -> Stage 12)
- Source of truth: ticket2code/code/agent-specs/01-stages.md
- Decision gates:
	- Stage 6: explicit DEV confirmation before code generation
	- Stage 10.5: explicit test/build decision gate
	- Stage 12: explicit commit-summary decision gate
- Important rule: if a gate choice is not explicit, workflow must stop and must not assume Yes/No.

## Agent workflow definitions
1. ticket2code/code/agent-specs/01-stages.md
2. .github/skills/ac-decomposition/SKILL.md
3. ticket2code/code/agent-specs/02-evaluation-rules.md
4. ticket2code/code/agent-specs/03-project-rules.md
5. ticket2code/code/agent-specs/04-jira-policy.md

## Processor workflow definitions
1. ticket2code/code/processor-specs/01-language-and-convention.md
2. ticket2code/code/processor-specs/02-section-1-analysis.md
3. ticket2code/code/processor-specs/03-section-2-evaluation.md
4. ticket2code/code/processor-specs/04-section-3-conclusion.md
5. ticket2code/code/processor-specs/05-decision-gates.md
6. ticket2code/code/processor-specs/06-validation-checklist.md
7. ticket2code/code/processor-specs/07-decision-labels.md

## Shared skills (installed to .github/skills/)
- AC decomposition: .github/skills/ac-decomposition/SKILL.md
- Dead-code cleanup: .github/skills/dead-code-cleanup/SKILL.md

## Design principles
- Entrypoint files are concise and stable.
- Detailed logic/templates are split into focused modules.
- Load-order is explicit to avoid stage omission.
- Stage gates remain strict and testable.

## Related workflows

### /t2c_review — Code review workflow
- Separate subsystem for reviewing code changes against acceptance criteria.
- See `ticket2code/review/INDEX.md` for architecture and usage.
- Workflow: resolve ticket report → request commit hash → retrieve diff → evaluate AC → generate review report.
- Useful for code review gate before merge, post-implementation assessment, or incident investigation.

## Troubleshooting
- If execution appears to stop at Stage 10.5 or Stage 12, first confirm the DEV choice was explicitly captured by the gate question.
- A 400 invalid_request_body error indicates request payload/transport failure, not stage-count mismatch.
