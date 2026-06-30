---
name: git-diff-analysis
description: "Retrieve, parse, classify, and analyze git diff changes between a base commit and HEAD, verifying compliance with code quality, safety, logging, naming, and styling standards."
argument-hint: "Base commit hash, HEAD commit hash (optional, defaults to HEAD), and repository engineering standards reference"
user-invocable: true
disable-model-invocation: false
---

# Git Diff Analysis

## What This Skill Produces
- A parsed and structured breakdown of changes: files added, modified, deleted, along with line-level change statistics.
- Classification of changes (Feature, Bug Fix, Refactor, Test, Doc, Cleanup).
- Safety and regression assessment: checking for side effects, API compatibility, and credential leaks.
- Quality checklist compliance report (naming, styling, logging policy, test coverage).

## When To Use
Use this skill when:
- Conducting a code review against JIRA acceptance criteria (`/t2c_review`).
- Auditing local workspace changes before committing.
- Investigating regression risks or verifying naming/logging standards.

---

## Procedure

### 1. Diff Extraction & Parsing
- Run `git diff <base-commit>..HEAD` (or target reference) to retrieve the raw diff.
- Group the changes by file path.
- Parse insertions (`+` prefix), deletions (`-` prefix), and hunks (`@@` header).
- Identify the language/type of each file (Swift, Kotlin, Python, JS, etc.) to apply language-specific checks.

### 2. Change Classification
Classify each change or hunk as:
1.  **Feature implementation:** New logic, public APIs, services, or UI components.
2.  **Bug fix:** Correction of existing logic, additional edge-case handling.
3.  **Refactor:** Structural changes, renaming, or extraction of code with no behavioral impact.
4.  **Test addition:** Unit tests, mocks, test fixtures, or UI tests.
5.  **Documentation:** Comments, markdown specs, and public API docstrings.
6.  **Cleanup:** Removal of dead code, old comments, or unused assets.

### 3. Safety & Regression Assessment
- **Scope check:** Verify if changes are isolated to the intended modules/files.
- **Side effects:** Inspect modifications to shared resources, base classes, DB schemas, or global configurations.
- **Secrets leak prevention:** Search for hardcoded API keys, tokens, passwords, or PII.

### 4. Code Quality & Standards Audit
Verify changes against repository standards:
- **Logging Policy:** Ensure correct log levels are used (DEBUG, INFO, WARN, ERROR). Verify no sensitive data is printed to console or persistent files.
- **Error Handling:** Check that caught exceptions are handled, logged, and propagated correctly instead of being silently ignored.
- **Naming & Style:** Confirm class, method, and variable names comply with language conventions (camelCase, snake_case, etc.) and file formatting guides (indentation, spacing).
- **Test Coverage:** Verify that new features or critical bug fixes are accompanied by appropriate test additions.

---

## Output Template

```markdown
### Git Diff Analysis Summary

**Base Commit:** `<base_hash>` (Author: `name`, Date: `date`)  
**Target Commit:** `HEAD` (Author: `name`, Date: `date`)

#### Changed Files Overview
| File Path | Status | Insertions | Deletions | Category |
|---|---|---|---|---|
| `src/core/payment.py` | Modified | +24 | -5 | Feature |
| `tests/test_payment.py` | Modified | +15 | -0 | Test |

#### Safety & Compliance Checklist
- [ ] **Secrets & Credentials:** No hardcoded tokens, keys, or passwords found.
- [ ] **Logging Compliance:** Correct log levels; no sensitive data printed.
- [ ] **Error Handling:** Exceptions are properly caught and handled.
- [ ] **Test Coverage:** All new code paths are covered by tests.
- [ ] **Naming & Style:** Naming conventions and style guides are met.

#### Hunk-Level Findings
- **`src/core/payment.py`**:
  - Implementation of payment gateway V2 matches AC requirements.
  - Logging statement on line 42 contains debug info without sensitive values.
```
