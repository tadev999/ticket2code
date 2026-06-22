# Section 3 — Code Quality Assessment

## Purpose

Evaluate code against repository-specific standards and best practices, separate from AC implementation.

## Required checks

1. **Coding style** (reference: repository coding standards)
   - Naming conventions (variables, functions, classes)
   - Indentation and spacing
   - Code structure and complexity

2. **Logging and error handling** (reference: repository logging/error policy)
   - Required logging at appropriate levels (DEBUG, INFO, WARN, ERROR)
   - No sensitive data in logs
   - Error cases handled correctly

3. **Test coverage** (reference: repository test strategy)
   - Unit tests added for new/modified logic
   - Test naming follows conventions
   - Tests cover positive and negative cases

4. **Review patterns** (reference: repository review-pattern knowledge base)
   - Known pitfalls from past incidents
   - Safety against race conditions, memory leaks, etc.

## Template

```markdown
## Code Quality Assessment

### 1. Coding Style

| Check | Status | Details |
|-------|--------|---------|
| Naming conventions | ✓ Pass | Variables and functions follow snake_case/camelCase |
| Indentation | ⚠ Warning | Inconsistent spacing in {file}:{lines} |
| Complexity | ✓ Pass | No excessive nesting or long functions |

### 2. Logging and Error Handling

| Check | Status | Details |
|-------|--------|---------|
| Logging coverage | ✓ Pass | Error cases logged at WARN/ERROR level |
| Sensitive data | ✗ Fail | Password found in log at {file}:{line} |
| Error handling | ✓ Pass | All error paths have recovery logic |

### 3. Test Coverage

| Check | Status | Details |
|-------|--------|---------|
| Unit tests added | ✓ Pass | {number} tests added for new functions |
| Test quality | ⚠ Warning | Negative cases missing in {test_file} |
| Coverage metrics | - N/A | No coverage tool configured |

### 4. Review Patterns

| Pattern | Status | Details |
|---------|--------|---------|
| Race conditions | ✓ Pass | No concurrent access without synchronization |
| Memory leaks | ✓ Pass | All resources properly released |
| UI update deadlocks | - N/A | No UI changes in this commit |
```

## Status symbols

- **✓ Pass** — No issues found; code meets standard.
- **⚠ Warning** — Minor issues; recommend addressing but not blocking.
- **✗ Fail** — Critical issue; must be fixed before merge.
- **- N/A** — Check not applicable to this code.

## Severity levels

- **Critical:** Security, data loss, or runtime crash risk.
- **High:** Logic error or significant deviation from repository-specific engineering standards.
- **Medium:** Code style or minor best-practice violation.
- **Low:** Documentation or minor improvement opportunity.
