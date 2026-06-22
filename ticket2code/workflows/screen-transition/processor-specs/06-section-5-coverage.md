# Section 5: Coverage Analysis

## Purpose
Document AC coverage with explicit traceability to test case IDs and step numbers.

## Template

```markdown
# Section 5: Coverage Analysis

## Coverage Summary

| Metric | Value |
|--------|-------|
| Total Atomic AC | 10 |
| Covered AC | 10 |
| Uncovered AC | 0 |
| Coverage Percentage | 100% |

## AC -> Test -> Step Matrix

| AC ID | AC Summary | Test Case | Step | Transition | Status |
|------|------------|-----------|------|------------|--------|
| AC-1.1 | Open mini app screen | TC-CP-001 | Step 1 | Home -> Mini App Top | Covered |
| AC-1.2 | Open detail screen | TC-CP-002 | Step 1 | Mini App Top -> Detail | Covered |
| AC-2.1 | Invalid OTP error flow | TC-ERR-001 | Step 2 | OTP Input -> OTP Error Dialog | Covered |

## Coverage by Transition Category

| Category | Total AC | Covered AC | Coverage % |
|----------|----------|------------|------------|
| Critical Path | 4 | 4 | 100% |
| Alternate Path | 2 | 2 | 100% |
| Error Recovery | 2 | 2 | 100% |
| Back Navigation | 1 | 1 | 100% |
| Entry Point | 1 | 1 | 100% |

## Gaps

- None

## Risk Notes

- Identify AC with single-point coverage only.
- Recommend at least one additional scenario for high-risk AC when possible.
```

## Composition Rules

- Every AC row must include at least one test case and one step.
- Transition column must contain explicit `From -> To` data.
- Gaps must be documented with reason and mitigation.

## Quality Checklist

- [ ] Coverage percentage is accurate
- [ ] All AC are represented in matrix
- [ ] Every matrix row has TC and Step values
- [ ] Gap and risk notes are present
