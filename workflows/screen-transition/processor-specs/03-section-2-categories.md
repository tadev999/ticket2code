# Section 2: Screen Transition Map

## Purpose
Document all navigation flows as explicit transition edges and group them by transition category.

## Template

```markdown
# Section 2: Screen Transition Map

## 2.1 Screen Inventory

| Screen ID | Screen Name | Entry Conditions |
|-----------|-------------|------------------|
| SCR-001 | Home | User logged in |
| SCR-002 | Mini App Top | Home shortcut tapped |
| SCR-003 | Mini App Detail | Item selected |

## 2.2 Transition Edge List

| Edge ID | Category | From Screen | Trigger/Action | To Screen | Notes |
|---------|----------|-------------|----------------|-----------|-------|
| EDGE-001 | Critical Path | Home | Tap mini app shortcut | Mini App Top | Main entry flow |
| EDGE-002 | Critical Path | Mini App Top | Tap item card | Mini App Detail | Main detail flow |
| EDGE-003 | Error Recovery | OTP Input | Submit invalid OTP | OTP Error Dialog | Error branch |

## 2.3 Path Definitions

### Path P1: Main purchase path (Critical Path)
1. Home -> Mini App Top
2. Mini App Top -> Mini App Detail
3. Mini App Detail -> Checkout
4. Checkout -> Result Success

### Path P2: Error recovery path (Error Recovery)
1. OTP Input -> OTP Error Dialog
2. OTP Error Dialog -> OTP Input (retry)

## 2.4 AC to Transition Mapping

| AC ID | AC Summary | Transition Edges |
|------|------------|------------------|
| AC-1.1 | Open mini app screen | EDGE-001 |
| AC-1.2 | Open detail screen | EDGE-002 |
| AC-2.1 | Invalid OTP shows error flow | EDGE-003 |
```

## Composition Rules

- Include all screens used by test cases.
- Every transition edge must include From Screen, Trigger, and To Screen.
- Every AC must map to at least one transition edge.
- Keep category names aligned with 03-test-categorization.md.

## Quality Checklist

- [ ] Screen names are consistent across all sections
- [ ] All transition edges are explicit and testable
- [ ] AC mapping references existing edge IDs
- [ ] Critical path and error path are both present when applicable
