# Section 2 — AC Evaluation Matrix

## Purpose

Systematically assess whether code changes implement each acceptance criterion.

## Required fields per AC item

- **AC number and text** (original AC)
- **Decomposed atomic items**
- **Status** (Met | Partially Met | Not Met | Unclear)
- **Code references** (file:line numbers from diff and/or codebase)
- **Evidence source** (Diff | Codebase)
- **Evidence** (brief explanation of how code addresses AC)

## Template

```markdown
## Acceptance Criteria Evaluation

### AC 1: {original AC text}

**Decomposed atomic items:**
1. Trigger: {trigger}  
   Condition: {condition}  
   Expected: {output}

2. Trigger: {trigger}  
   Condition: {condition}  
   Expected: {output}

**Assessment:**

| Atomic Item | Status | Code Reference | Source | Evidence |
|-------------|--------|-----------------|--------|----------|
| Item 1 | Met | `FileName.[ext]:42-50` | Diff | Logic implements trigger/condition/output |
| Item 2 | Met | `ExistingFlow.[ext]:118-140` | Codebase | Behavior already implemented outside current diff |
| Item 3 | Not Met | N/A | N/A | No implementation found in diff or codebase |

**Summary:** {brief explanation of overall AC coverage}

### AC 2: {original AC text}

...
```

## Assessment logic

- **Met:** Code fully and correctly implements the atomic item (in diff or existing codebase).
- **Partially Met:** Implementation exists but has limitations (e.g., missing error handling, one branch).
- **Not Met:** No implementation found after checking both diff and codebase.
- **Unclear:** Cannot assess even after checking diff and codebase because external/runtime context is required.

## Code references format

Use format: `FileName.[ext]:42-50` (file name, then line range).  
Multiple references: `FileA.[ext]:10-15, FileB.[ext]:88-92`

Always indicate source per reference: `Diff` or `Codebase`.

## Evidence checklist

For each assessment, verify:
- ☐ Diff was checked first for direct implementation evidence
- ☐ If diff evidence is missing, relevant codebase areas were searched
- ☐ Line references point to actual code (diff and/or codebase)
- ☐ Logic explanation connects code to the trigger/condition/expected output
- ☐ If "Partially Met", explain what is missing
- ☐ If "Not Met" or "Unclear", explain why
