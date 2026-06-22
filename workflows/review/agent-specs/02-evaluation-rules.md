# Code Review Evaluation Rules

## Assessment categories

For each atomic AC item, code review must produce one of four statuses:

1. **Met** — Atomic AC is fully implemented and behavior is complete/correct, either in diff or already in existing codebase.
2. **Partially Met** — Implementation exists (in diff or codebase) but has limitations or incomplete branch coverage.
3. **Not Met** — No implementation found after checking both diff and existing codebase.
4. **Unclear** — Insufficient technical context remains after checking both diff and codebase (e.g., depends on external system behavior that is not observable in repo).

## Evidence requirements

Each assessment must include:
- **Code references:** Exact file names and line numbers from diff and/or codebase that implement (or fail to implement) the AC.
- **Evidence source:** Explicitly label `Diff` or `Codebase` for each reference.
- **Logic explanation:** How the code addresses the trigger, condition, and expected output.
- **Compliance check:** Does code follow repository-specific engineering standards (style, logging, test coverage)?

## Cross-reference to repository guidance

Apply checks from the repository's guidance documents, for example:
- coding style or naming convention guidelines
- logging and error handling policy
- test strategy or test code rules
- review-pattern or incident knowledge base

## Conditional coverage

If an AC has branches (e.g., "success" and "error" paths):
- Assess code for each branch separately.
- Note if one branch is missing implementation.
- Mark as "Partially Met" if only some branches are covered.

## Unclear status

Use "Unclear" when:
- AC depends on server behavior that cannot be verified from repository code.
- AC requires runtime/database/external system interaction that cannot be validated statically.
- Context is genuinely ambiguous and requires DEV clarification.

Do **not** use "Unclear" just because implementation is not present in the current diff.  
If implementation is already present elsewhere in the codebase, assess as "Met" or "Partially Met" with `Codebase` evidence.

In these cases, note explicitly what additional information is needed.
