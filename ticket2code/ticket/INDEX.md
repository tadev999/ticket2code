# Architecture Reference — /ticket workflow

This index is the canonical navigation file for the modularized /ticket system.

## Start here
- Entry command: ticket2code/ticket/ticket.prompt.md
- Agent entrypoint: ticket2code/ticket/ticket-agent.md
- Processor entrypoint: ticket2code/ticket/ticket-processor.prompt.md
- Setup: ticket2code/ticket/SETUP.md

## Agent specs
1. ticket2code/ticket/agent-specs/01-stages.md
2. ticket2code/ticket/agent-specs/02-ac-decomposition.md
3. ticket2code/ticket/agent-specs/03-evaluation-rules.md
4. ticket2code/ticket/agent-specs/04-project-rules.md
5. ticket2code/ticket/agent-specs/05-jira-policy.md

## Processor specs
1. ticket2code/ticket/processor-specs/01-language-and-convention.md
2. ticket2code/ticket/processor-specs/02-section-1-analysis.md
3. ticket2code/ticket/processor-specs/03-section-2-evaluation.md
4. ticket2code/ticket/processor-specs/04-section-3-conclusion.md
5. ticket2code/ticket/processor-specs/05-cleanup-checklist.md
6. ticket2code/ticket/processor-specs/06-decision-gates.md
7. ticket2code/ticket/processor-specs/07-validation-checklist.md
8. ticket2code/ticket/processor-specs/08-decision-labels.md

## Design principles
- Entrypoint files are concise and stable.
- Detailed logic/templates are split into focused modules.
- Load-order is explicit to avoid stage omission.
- Stage gates remain strict and testable.
