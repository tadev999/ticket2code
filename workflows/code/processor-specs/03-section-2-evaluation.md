# Section 2 — Post-generate Code Evaluation (Stage 10)

## 2.1 Detailed per-AC mapping

Template per AC item:

### 2.1 Detailed mapping per acceptance condition

#### <AC-ID>: <short title>

| Field                 | Content |
|-----------------------|---------|
| Source requirement    | <quoted text from ticket> |
| Normalized expectation| <one trigger + one condition value + one expected output> |
| Status                | Met / Partially Met / Not Met / Unclear |
| Code evidence         | <file> — <function/method> — <key branch or logic> |
| Test evidence         | <test case name> or None |
| Impact                | <UI / navigation / state / data / logging> |
| Gap / Risk            | <regression risk or behavior mismatch> |
| Recommendation        | <patch needed / test to add / question for PO-BA> |

## 2.2 Coverage summary

| Status        | Count |
|---------------|-------|
| Met           | x     |
| Partially Met | x     |
| Not Met       | x     |
| Unclear       | x     |
| Total         | y     |

Blocking items:
- <AC-ID>: <reason>

## 2.3 Abnormal-case matrix

Use when ticket defines conditional behavior by discrete values.

| Case ID | Input condition | Expected behavior | Current implementation | Status | Code / test evidence | Gap |
|---------|------------------|------------------|------------------------|--------|----------------------|-----|
| <ID>    | <condition>      | <expected>       | <current>              | Met/Partially Met/Not Met/Unclear | <evidence> | <gap> |

Rules:
- One row per discrete value. Never merge values.
- Lifecycle behaviors are separate rows.
- Do not mark Met for post-dismiss behavior without explicit navigation/callback evidence.

## 2.4 Dead-code cleanup evidence (required)

Template:

### 2.4 Dead-code cleanup evidence

Removed symbols:
- <symbol/type> — <file> — <reason>

Search evidence (before -> after):
- Query: <keyword or symbol>
  Scope: <prod/test/mock>
  Before: <count>
  After: <count>

- Query: <keyword or symbol>
  Scope: <prod/test/mock>
  Before: <count>
  After: <count>

Build/lint evidence:
- Type-check: Pass/Fail
- Lint: Pass/Fail
- Notes: <if skipped, explicit reason>

Rules:
- Include at least 2 search queries relevant to removed logic.
- Include test/mock scope when presenter/interactor/router logic is removed.
- If residual matches remain, explain intentional keep.
