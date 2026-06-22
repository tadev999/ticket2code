---
name: dead-code-cleanup
description: "Identify, verify, and remove dead code, orphaned functions, variables, events, listeners, and references, generating before/after search evidence and compiler/linter checks."
argument-hint: "Target directory, file paths to analyze, and search/grep keywords"
user-invocable: true
disable-model-invocation: false
---

# Dead Code & Orphaned Reference Cleanup

## What This Skill Produces
- Systematic removal of obsolete functions, events, listeners, variables, and comments.
- **Before/After Search Evidence:** Concrete search logs verifying that references to removed symbols have dropped to zero.
- **Compilation/Validation status:** Report showing that compiler, type-checker, and linter run with 0 errors after cleanup.

## When To Use
Use this skill:
- During the final stage of code generation (`/t2c_code` Stage 9.5) to clean up old references.
- During code refactoring tasks to eliminate technical debt.
- To clean up unused imports, orphaned methods, and outdated test mocks.

---

## Procedure

### 1. Scope & Keyword Definition
Identify all symbols (functions, variables, constants, event names, subscription keys) that are part of the obsolete code block or feature being removed.

### 2. Search & Analyze (Before Cleanup)
- Run workspace-wide search (e.g., via `grep` or file search tools) for each identified symbol.
- Record the files and line numbers where the symbol is referenced.
- Distinguish between definition sites and invocation sites.
- **Required search scope:**
  - Production code
  - Test files
  - Mock/Stub/Fake definitions
  - Router, Dependency Injection, and Assembler configs

### 3. Systematic Removal
Remove the symbols in the following order:
- **Events & Listeners:** Remove emit/trigger call sites first, then listeners/subscriptions, and finally the event definitions.
- **Functions & Methods:** Verify if a function has zero callers outside itself. If yes, remove it.
- **Variables & Parameters:** Remove variables that are only passed into removed function calls.
- **Imports & Dependencies:** Remove now-unused imports or package requirements.

### 4. Search & Verify (After Cleanup)
- Re-run the workspace-wide search for all removed symbols.
- Confirm that the count of references is now **0** (or only contains the changelog/documentation references if applicable).

### 5. Build and Lint Verification
- Run the compiler or type-checker for the target language (e.g., `tsc`, `swiftc`, `go build`). Confirm **0 errors**.
- Run the repository's linter. Confirm **no new violations** are introduced.

---

## Output Template

```markdown
### Dead-Code and Orphaned Reference Cleanup Report

#### 1. Removed Symbols List
| Symbol Name | Symbol Type | Origin File | Scope of Impact |
|---|---|---|---|
| `PaymentGatewayV1` | Class | `src/payment/gateway.py` | Removed old gateway engine |
| `on_payment_deprecated` | Event | `src/events/signals.py` | Unused listener hook |
| `old_test_mock` | Function | `tests/mocks/payment.py` | Unused mock helper |

#### 2. Search Evidence (Before vs. After)
*   **Keyword:** `PaymentGatewayV1`
    *   *Before:* 4 occurrences in 3 files (`gateway.py`, `router.py`, `test_payment.py`)
    *   *After:* 0 occurrences (excluding this report)
*   **Keyword:** `on_payment_deprecated`
    *   *Before:* 2 occurrences in 2 files (`signals.py`, `app.py`)
    *   *After:* 0 occurrences

#### 3. Build & Linter Verification Status
- **Compiler/Type-checker:** `PASS` (0 errors)
- **Linter/Stylecheck:** `PASS` (0 violations)
- **Status:** Cleanup Complete. No orphaned references remain in codebase, tests, or configurations.
```
