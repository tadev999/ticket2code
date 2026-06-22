# Coverage Validation Rules

## Purpose
Ensure all acceptance criteria are covered by integration tests and that test coverage is complete and traceable.

## Coverage Matrix Structure

Create an explicit mapping showing which test cases verify which atomic AC:

```
## Coverage Analysis Matrix

| AC ID | AC Description | Test Cases | Coverage Status |
|-------|---|---|---|
| AC-1.1 | User can enter valid payment amount | TC-UI-001, TC-BL-001 | ✓ Covered |
| AC-1.2 | Amount is stored in correct field | TC-DP-001 | ✓ Covered |
| AC-1.3 | Amount exceeding limit is rejected | TC-BL-002, TC-EH-001 | ✓ Covered |
| AC-2.1 | Verification code is sent on request | TC-API-001 | ✓ Covered |
| AC-2.2 | User can enter verification code | TC-UI-002 | ✓ Covered |
| AC-2.3 | Correct code is validated | TC-BL-003 | ✓ Covered |
| AC-2.4 | Incorrect code is rejected | TC-EH-002, TC-EDGE-001 | ✓ Covered |
```

---

## Coverage Validation Rules

### Rule 1: 100% AC Coverage (Mandatory)
Every atomic AC must be tested by at least one test case.

**Validation:**
- Generate mapping of all atomic ACs
- For each AC, list at least one test case
- If any AC has zero test cases, either:
  - Create new test case to cover it, or
  - Document why it's not testable (with justification)
- Mark all non-covered ACs as gaps in report

**Example Gap Documentation:**
```
## Coverage Gaps

AC-3.1: "User receives push notification on successful payment"
- **Status:** Not covered (1 gap)
- **Reason:** Push notification testing requires a physical device or simulator/emulator; 
  outside scope of automated integration tests
- **Alternative:** Manual testing procedure documented in TC-MANUAL-001
- **Recommendation:** Add automated device farm testing in Phase 2
```

---

### Rule 2: Traceability
Each test case must reference which AC it covers.

**Format in test case:**
```
## Related AC
- AC-1.1: User can enter valid amount → Verified by Step 1, Step 2
- AC-1.2: Amount is stored correctly → Verified by Step 3
```

**Format in coverage matrix:**
```
AC-1.1 | User can enter valid amount | TC-UI-001, TC-BL-001 | ✓ Covered
```

### Rule 3: No Orphaned Test Cases
Every test case should verify at least one AC.

**Validation:**
- For each test case, list related AC
- If a test case has zero related AC:
  - Either link it to an AC, or
  - Remove it as unnecessary, or
  - Document it as exploratory/regression test

**Example:**
```
Test Case: TC-REG-001: Previously fixed amount-validation bug remains resolved
- **Related AC:** None (regression prevention test)
- **Justification:** Protects a known production incident fix that is not derived directly from the current ticket AC
- **Status:** Included as regression prevention measure
```

### Rule 4: Clear AC-to-Test Relationship
Each relationship should be specific, not vague.

**Bad relationship:**
```
AC-1.1 → TC-01 (too vague, which steps in TC-01?)
```

**Good relationship:**
```
AC-1.1: User can enter valid amount 
  → TC-UI-001: User taps amount field and enters [AMOUNT] (Steps 1-2)
```

---

## Coverage Calculation

### Overall Coverage Percentage
```
Coverage % = (Number of covered AC / Total number of AC) × 100
```

**Example:**
- Total atomic AC: 10
- Covered AC: 10
- Uncovered AC: 0
- **Coverage: 100%** ✓ (Pass)

---

### Coverage by Category
```
| Category | Total AC | Covered AC | Coverage % |
|----------|----------|-----------|-----------|
| AC-BL (Business Logic) | 4 | 4 | 100% |
| AC-UI (User Interface) | 3 | 3 | 100% |
| AC-API (API Integration) | 2 | 2 | 100% |
| AC-SEC (Security) | 1 | 1 | 100% |
| **TOTAL** | **10** | **10** | **100%** |
```

---

## Coverage Types

### Type 1: Direct Coverage
Test directly verifies AC behavior.

**Example:**
```
AC-1.1: User can enter valid amount within daily limit
→ TC-BL-001: User enters [AMOUNT] and system accepts it
   (daily limit is [LIMIT_AMOUNT], so test passes ✓)
```

### Type 2: Indirect Coverage
Test verifies related behavior that implies AC is working.

**Example:**
```
AC-1.3: User receives confirmation after successful payment
→ TC-DP-001: TransactionRecord is created in database with correct data
   (Confirmation is generated from this record, so if record exists ✓)
```

### Type 3: Partial Coverage
Test verifies one aspect but not all aspects of AC.

**Example:**
```
AC-1.4: System prevents duplicate payments within 60 seconds
→ TC-EH-003: User taps Pay button twice and system rejects second payment
   (Tests 2 seconds, but AC covers 60 seconds; partial coverage)
   Status: PARTIALLY COVERED - needs another test with 60-second timeout
```

### Type 4: Conditional Coverage
Test verifies one branch of conditional AC.

**Example:**
```
AC-2.2: Admin can delete any file; non-admin can only delete their own
→ TC-SEC-001: Admin deletes another user's file (verifies admin branch)
→ TC-SEC-002: Non-admin cannot delete another's file (verifies non-admin branch)
   (Both branches covered ✓)
```

---

## Gaps and Deviations

### Gap Documentation Template

```
## Coverage Gap: [AC ID]

**AC:** [AC description]

**Reason for Gap:**
- [ ] AC is not testable in integration tests
- [ ] Requires manual testing
- [ ] Requires specific hardware/environment
- [ ] Scheduled for later phase
- [ ] Out of scope for this ticket
- [ ] Other: [specify]

**Alternative Coverage:**
- Manual test: [Reference to manual test]
- Unit test: [Reference to unit test]
- E2E test: [Reference to E2E test]
- Future phase: [Phase number and description]

**Impact:** [What is not verified due to this gap]

**Risk Level:** [ ] Low [ ] Medium [ ] High

**Mitigation:** [How will this be verified later]
```

### Deviation Documentation Template

```
## Coverage Deviation: [TC ID]

**Test Case:** [TC description]

**Reason for Deviation:**
- [ ] Tests behavior beyond AC (exploratory)
- [ ] Regression prevention (known bug)
- [ ] Performance test (beyond AC scope)
- [ ] Security hardening (defense in depth)
- [ ] Framework requirement
- [ ] Other: [specify]

**Justification:** [Why this test is valuable despite not directly testing AC]

**Scope:** [What additional risk/behavior is covered]
```

---

## Coverage Validation Checklist

Before finalizing coverage:
- [ ] All atomic AC are decomposed (see 02-ac-decomposition.md)
- [ ] Coverage matrix includes all atomic AC
- [ ] Every AC has at least one test case (or documented gap)
- [ ] Every test case references related AC (or documented deviation)
- [ ] Coverage relationships are specific and traceable
- [ ] Coverage percentage is calculated and displayed
- [ ] Coverage by category is documented
- [ ] All gaps are justified and documented
- [ ] All deviations are justified and documented
- [ ] No "orphaned" test cases without AC linkage
- [ ] Coverage matrix is easy to update as tests change
- [ ] Documentation is clear for audit/review purposes

---

## Coverage Report Template

```
# Coverage Analysis Report

## Summary
- **Total Atomic AC:** 15
- **Covered AC:** 15
- **Uncovered AC:** 0
- **Coverage %:** 100%
- **Gap Count:** 0
- **Deviation Count:** 2 (both justified)

## Coverage by Category
| Category | Total | Covered | % |
|---|---|---|---|
| Business Logic | 5 | 5 | 100% |
| UI/UX | 4 | 4 | 100% |
| API Integration | 3 | 3 | 100% |
| Data Persistence | 2 | 2 | 100% |
| Security | 1 | 1 | 100% |
| **TOTAL** | **15** | **15** | **100%** |

## Coverage Matrix
[Detailed matrix showing AC, test cases, and status]

## Justified Gaps
[Any gaps with documentation]

## Justified Deviations
[Any deviations with documentation]

## Conclusion
[Summary assessment of coverage quality]
```

---

## Coverage Quality Assessment

In addition to coverage percentage, assess coverage **quality**:

### Aspect 1: Depth
Does coverage include:
- [ ] Happy path scenarios
- [ ] Error/exception scenarios
- [ ] Edge cases and boundary conditions
- [ ] Performance characteristics
- [ ] Integration between components

### Aspect 2: Realism
Does coverage test:
- [ ] Real-world user scenarios
- [ ] Actual system configurations
- [ ] Representative data volumes
- [ ] Expected failure modes

### Aspect 3: Completeness
Does coverage verify:
- [ ] All observable behaviors
- [ ] All state changes
- [ ] All side effects (logs, notifications, etc.)
- [ ] All timing constraints
