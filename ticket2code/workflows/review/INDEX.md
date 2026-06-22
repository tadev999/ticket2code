# Architecture Reference — /t2c_review workflow

This index is the canonical navigation file for the modularized /t2c_review code review system.

## Start here
- Entry command: ticket2code/review/t2c_review.prompt.md
- Agent entrypoint: ticket2code/review/review-agent.md
- Processor entrypoint: ticket2code/review/review-processor.prompt.md
- Setup: ticket2code/SETUP.md

## Current workflow map (Stage 0 -> Stage 6)
- Source of truth: ticket2code/review/agent-specs/01-stages.md
- Gate points:
  - Stage 1: Report resolution (cache or fetch)
  - Stage 2: Commit hash input validation
  - Stage 3: Diff retrieval and parsing
  - Stage 5: AC evaluation systematic assessment
  - Stage 6: Report generation and file save
- Important rule: if a required input or decision is not explicit, workflow must stop and must not assume.

## Agent workflow definitions
1. ticket2code/review/agent-specs/01-stages.md
2. .github/skills/ac-decomposition/SKILL.md
3. ticket2code/review/agent-specs/02-evaluation-rules.md
4. .github/skills/git-diff-analysis/SKILL.md

## Processor workflow definitions
1. ticket2code/review/processor-specs/01-language-and-convention.md
2. ticket2code/review/processor-specs/02-section-1-commit-metadata.md
3. ticket2code/review/processor-specs/03-section-2-ac-evaluation.md
4. ticket2code/review/processor-specs/04-section-3-code-quality.md
5. ticket2code/review/processor-specs/05-section-4-conclusion.md

## Shared skills (installed to .github/skills/)
- AC decomposition: .github/skills/ac-decomposition/SKILL.md
- Git diff analysis: .github/skills/git-diff-analysis/SKILL.md

## Design principles
- Review reports are separate from implementation reports (produced by /t2c_code).
- Each review is a point-in-time assessment of a specific commit against known AC.
- Review workflow is shorter and more focused than full ticket-to-code workflow.
- Code quality checks apply repository-specific engineering standards consistently across all reviews.

## Relationship to /t2c_code workflow
- Both workflows use the shared `ac-decomposition` skill (.github/skills/ac-decomposition/SKILL.md).
- Both workflows apply the same repository-specific engineering standards and guidance.
- /t2c_review focuses on existing code assessment; /t2c_code focuses on code generation and implementation.
