# Test Sequence Rules

## Purpose
Define how to write clear, reproducible test procedures centered on screen transitions.

## Mandatory Per-Step Format
Each step must include:
- `From Screen`
- `Action / Trigger`
- `To Screen`
- `Expected Destination State`
- `Verification`

## Test Case Template

```
# Test Case: TC-[CAT]-[NNN]: [From Screen] -> [To Screen]

## Objective
[What transition behavior is validated]

## Category
[CP/ALT/ERR/BACK/ENTRY/REG]

## Pre-conditions
- User state
- Data state
- App/device state

## Transition Steps

### Step 1
From Screen: [Screen A]
Action: [User/system action]
To Screen: [Screen B]
Expected Destination State: [UI/data state on Screen B]
Verification: [How to verify]

### Step 2
From Screen: [Screen B]
Action: [User/system action]
To Screen: [Screen C]
Expected Destination State: [UI/data state on Screen C]
Verification: [How to verify]

## Expected Result
- Final screen is correct
- Mandatory UI element state is correct
- Side effects are correct (API/log/data)

## Assertions
- [ ] Correct destination screen appears at each step
- [ ] Transition trigger causes expected navigation
- [ ] No unexpected intermediate screen appears

## Related AC
- AC-1.1: [Description] -> Verified by Step 1
- AC-1.2: [Description] -> Verified by Step 2

## Post-conditions
- Cleanup actions
- Final app state
```

## Rules

### Rule 1: No Ambiguous Screen Names
Use stable names such as page title, route key, or VC/Scene identifier.

### Rule 2: Transition Assertions Are Mandatory
A step is incomplete without destination-screen verification.

### Rule 3: Include Branch Scenarios
For each critical path, include alternate and error paths when AC describes them.

### Rule 4: AC Mapping Must Be Step-Level
Do not map AC only at test-case level; always include step references.

## Validation Checklist

- [ ] Every step includes From/Action/To
- [ ] Every step has destination-screen verification
- [ ] Each test case has explicit Related AC
- [ ] Critical, alternate, and error paths are represented
- [ ] Naming is consistent across all screens
