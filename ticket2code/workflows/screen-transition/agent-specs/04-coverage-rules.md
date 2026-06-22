# Coverage Validation Rules

## Purpose
Ensure all AC are covered with explicit traceability to transition test case steps.

## Required Coverage Matrix

```markdown
| AC ID | AC Summary | Test Case | Step | Transition | Status |
|------|------------|-----------|------|------------|--------|
| AC-1.1 | Open mini app screen | TC-CP-001 | Step 1 | Home -> Mini App Top | Covered |
| AC-1.2 | Open detail screen | TC-CP-002 | Step 1 | Mini App Top -> Detail | Covered |
| AC-2.1 | Invalid OTP error flow | TC-ERR-001 | Step 2 | OTP Input -> OTP Error Dialog | Covered |
```

## Mandatory Rules

1. 100% Atomic AC Coverage
- Every atomic AC must have at least one mapped test case and step.

2. Step-Level Traceability
- AC mapping must include step number, not only TC ID.

3. No Orphaned Test Cases
- Every test case must map to at least one AC.

4. Branch Completeness
- If AC has success/error branches, both must be represented or explicitly documented as gap.

## Gap Documentation

If any AC is not covered, include:
- AC ID
- Reason
- Impact
- Mitigation plan

## Checklist

- [ ] Coverage matrix contains all atomic AC
- [ ] Every row includes TC and Step
- [ ] All branch AC are covered or documented as gap
- [ ] No orphaned test case exists
