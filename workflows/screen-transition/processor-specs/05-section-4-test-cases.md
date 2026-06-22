# Section 4: Test Cases

## Purpose
Document detailed, executable test cases that clearly show how transitions happen between screens.

## Template

```markdown
# Section 4: Screen Transition Test Cases

## TC-CP-001: Home -> Mini App Top

Objective: Verify main entry transition from Home to Mini App Top.
Category: Critical Path

Pre-conditions:
- User logged in
- Mini app shortcut is visible on Home

Transition Steps:

Step 1
From Screen: Home
Action: Tap mini app shortcut
To Screen: Mini App Top
Expected Destination State: Header/title and first content block are visible
Verification: Validate route ID and required UI elements

Expected Result:
- User lands on Mini App Top without intermediate error screen
- Route state is stable and interactive

Assertions:
- [ ] Transition reaches Mini App Top
- [ ] Required components are visible on destination screen
- [ ] No error dialog appears

Related AC:
- AC-1.1: Open mini app top screen -> Verified by Step 1

Post-conditions:
- Return to Home for next test

---

## Test Case Summary

| TC ID | Category | From Screen | To Screen | Covered AC |
|------|----------|-------------|-----------|------------|
| TC-CP-001 | Critical Path | Home | Mini App Top | AC-1.1 |
| TC-CP-002 | Critical Path | Mini App Top | Detail | AC-1.2 |
| TC-ERR-001 | Error Recovery | OTP Input | OTP Error Dialog | AC-2.1 |
```

## Composition Rules

- Every step must include From Screen, Action, To Screen.
- Destination-screen verification is mandatory for every step.
- Every test case must include Related AC with step references.
- Keep wording executable and deterministic.

## Quality Checklist

- [ ] Step format is complete for all test cases
- [ ] Transition assertions are measurable
- [ ] AC mapping is explicit and step-level
- [ ] Pre-conditions and post-conditions are reproducible
