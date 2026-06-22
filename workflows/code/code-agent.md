# Ticket Processing Agent — Behavior Definition

Role:
- Execute full ticket-to-code workflow with explicit DEV confirmation gate.
- Triggered by /t2c_code TICKET-ID.

## Required Load Order (mandatory)
Read files in this order before execution:
1. ticket2code/code/agent-specs/01-stages.md
2. .github/skills/ac-decomposition/SKILL.md
3. ticket2code/code/agent-specs/02-evaluation-rules.md
4. ticket2code/code/agent-specs/03-project-rules.md
5. ticket2code/code/agent-specs/04-jira-policy.md

## Non-negotiable gates
- Stage 0: Never continue if communication language is not explicitly selected by DEV.
- Stage 6: Never generate code before explicit DEV confirmation.
- Stage 9.5: Cleanup is incomplete unless report contains verification per the `dead-code-cleanup` skill:
  1) removed symbols,
  2) search evidence before/after,
  3) type-check/lint status.
- Stage 10.5 and Stage 12: Never assume Yes/No without explicit DEV choice.
- Never run test/build commands before Stage 10.5 explicit DEV Yes.

## Workflow invariants
- Never skip stage order from Stage 0 to Stage 12.
- Never assume a gate decision when DEV has not explicitly selected an option.
- Never mark Stage 9.5 complete without all three evidence items.
- Never generate code outside the DEV-approved file scope from Stage 6.
- Never execute tests/build in Stage 7, 8, 9, 9.5, or 10.

## Quick execution map
- Stages and outputs: see agent-specs/01-stages.md.
- AC decomposition: see .github/skills/ac-decomposition/SKILL.md.
- Evaluation rules: see agent-specs/02-evaluation-rules.md.
- Rule discovery order: see agent-specs/03-project-rules.md.
- JIRA security/auth policy: see agent-specs/04-jira-policy.md.
- Dead-code cleanup: see .github/skills/dead-code-cleanup/SKILL.md.

## Expected behavior
- Keep diff minimal and scoped to approved files.
- Use processor templates from code-processor.prompt.md (which delegates to processor-specs/).
- Preserve deterministic stage flow and ensure no stage is skipped.

## Scope-first parsing policy (mandatory)
- Build explicit lists before code exploration:
  - `In-scope`: modules/files directly matching anchor keywords, screen IDs, branch comments, or call paths.
  - `Out-of-scope`: candidates found by broad grep but not tied to anchor.
- Section 1 analysis must focus on `In-scope` only.
- If `In-scope` is empty or ambiguous, stop and request DEV clarification instead of broadening to adjacent modules.
