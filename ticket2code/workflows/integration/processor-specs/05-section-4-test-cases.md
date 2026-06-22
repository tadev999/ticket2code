# Section 4: Test Cases

## Purpose
Document all integration test cases with detailed sequences, expected results, and assertions.

## Template

```
# Section 4: Integration Test Cases

---

## [Category Name] Tests

### TC-[CAT]-001: [Scenario description]

**Objective:** [1-2 sentence description of test purpose]

**Category:** [Category name]

**Pre-conditions:**
- User is authenticated with role: [Role]
- [Data state requirement 1]
- [Data state requirement 2]
- [System state requirement]

**Test Sequence**

#### Step 1: [Action description]
**Action:** [What user or system does]  
**Expected State Change:** [What changes in the system]

#### Step 2: [Action description]
**Action:** [What user or system does]  
**Expected State Change:** [What changes in the system]

#### Step 3: [Action description]
**Action:** [What user or system does]  
**Expected State Change:** [What changes in the system]

**Expected Result**

**User-visible Outcome:**
- [What user sees/experiences]
- [UI elements displayed]
- [Messages or notifications]

**Data State Outcome:**
- Database record created/modified:
  - Entity: [Table]
  - Attributes: [Attribute values]
- Cache updated: [Cache details]

**System State Outcome:**
- External API calls made: [API endpoint, parameters, response]
- Logs generated: [Log level, message content]
- Notifications sent: [Type, content]

**Timing:**
- Total test duration: [Expected time]
- Step-by-step timing: [Optional]

**Assertions**
- [ ] Payment form displays with all required fields
- [ ] Amount field accepts numeric input
- [ ] User can tap Pay button
- [ ] Payment API is called with correct amount
- [ ] Transaction record exists in database with correct amount
- [ ] User receives confirmation message
- [ ] Confirmation shows transaction ID
- [ ] Balance is updated immediately

**Post-conditions**
- Payment record exists in database
- User's balance is reduced by payment amount
- Transaction history is updated
- Session remains active

**Related AC**
- AC-1.1: User enters valid amount → Verified by Steps 1-2
- AC-1.3: System processes payment → Verified by Steps 3-4

**Notes:**
[Any additional context, known issues, or edge cases]

---

### TC-[CAT]-002: [Scenario description]

[Repeat structure above]

---

### TC-[CAT]-003: [Error case scenario]

**Objective:** [Test error handling]

**Category:** [Category name]

**Pre-conditions:**
- [Setup for error condition]

**Test Sequence**

#### Step 1: [Setup for error]
**Action:** [What triggers the error]
**Expected State Change:** [System enters error state]

#### Step 2: [Trigger action]
**Action:** [User attempts operation]
**Expected State Change:** [Error is detected and handled]

#### Step 3: [Error response]
**Action:** [System shows error to user]
**Expected State Change:** [User sees error message]

**Expected Result**

**User-visible Outcome:**
- Error message displays
- Message text is clear and actionable
- Retry option is available

**Data State Outcome:**
- No transaction record is created
- No balance change occurs

**System State Outcome:**
- Error logged with details
- Error reported to monitoring system
- Retry counter is incremented

**Assertions**
- [ ] Error message is displayed
- [ ] Error message is user-friendly (not technical)
- [ ] No transaction is created
- [ ] Retry button is available
- [ ] Error is logged

**Post-conditions**
- User can retry operation
- System is in stable state
- No orphaned resources

**Related AC**
- AC-2.4: Incorrect code is rejected → Verified by Steps 1-3

---

## Test Case Summary Table

| TC ID | Category | Scenario | Pre-req | Status |
|-------|----------|----------|---------|--------|
| TC-UI-001 | UI/UX | User enters valid amount | Authenticated | ✓ |
| TC-BL-001 | Business Logic | Amount within limit | Authenticated | ✓ |
| TC-BL-002 | Business Logic | Amount exceeds limit | Authenticated | ✓ |
| TC-API-001 | API Integration | Payment gateway call | Authenticated | ✓ |
| TC-DP-001 | Data Persistence | Transaction stored | Authenticated | ✓ |
| TC-EH-001 | Error Handling | Timeout handling | Authenticated | ✓ |

---

## Variant Test Cases

### Variant A: Edge Cases

#### TC-EDGE-001: Zero amount
**Scenario:** User enters zero as payment amount
**Expected Result:** System validates and rejects zero amount
**Assertions:**
- [ ] Zero amount is rejected
- [ ] Error message: "Amount must be greater than 0"

#### TC-EDGE-002: Maximum amount
**Scenario:** User enters maximum allowed amount
**Expected Result:** System accepts and processes maximum amount
**Assertions:**
- [ ] Maximum amount is accepted
- [ ] Payment is processed successfully

### Variant B: Alternate Flows

#### TC-ALT-001: User cancels payment
**Scenario:** User confirms payment form but cancels before submission
**Expected Result:** Payment is not processed
**Assertions:**
- [ ] No transaction is created
- [ ] User returns to payment form

---

## Test Execution Notes

### Execution Order
Tests can be executed in any order (independent):
1. UI tests can run in parallel with Business Logic tests
2. Data Persistence tests should run after Business Logic (depend on data)
3. Error Handling tests are independent
4. Edge case tests are independent

### Test Dependencies
```
TC-UI-001 (prerequisites for others)
  └─→ TC-BL-001, TC-BL-002
      └─→ TC-DP-001
          └─→ TC-API-001
```

### Parallel Execution
The following test cases can run in parallel:
- TC-UI-001, TC-UI-002, TC-UI-003 (independent users)
- TC-EH-001, TC-EH-002, TC-EH-003 (independent error scenarios)

The following tests must run sequentially:
- TC-BL-002 → TC-BL-003 (depend on transaction count)

---

## Test Case Quality Checklist

For each test case, verify:
- [ ] Objective is clear and specific
- [ ] Pre-conditions are complete and reproducible
- [ ] Test sequence has numbered steps
- [ ] Each step has clear action and expected state change
- [ ] Expected results cover all outcome types (user, data, system, timing)
- [ ] All assertions are specific and verifiable
- [ ] Related AC are explicitly mapped to steps
- [ ] Post-conditions are documented
- [ ] Test is independent and can run in isolation
- [ ] Test is repeatable with same setup
- [ ] Test has clear pass/fail criteria
```

---

## Section 4 Composition Rules

### Required Elements for Each Test Case
- [ ] TC ID following format TC-[CAT]-[NNN]
- [ ] Scenario title (what is being tested)
- [ ] Objective (why test matters)
- [ ] Category (primary test category)
- [ ] Pre-conditions (setup requirements)
- [ ] Test sequence (numbered steps with actions and state changes)
- [ ] Expected result (comprehensive outcomes)
  - [ ] User-visible outcomes
  - [ ] Data state outcomes
  - [ ] System state outcomes
  - [ ] Timing outcomes
- [ ] Assertions (specific, verifiable checks)
- [ ] Post-conditions (final state and cleanup)
- [ ] Related AC mapping

### Optional Elements
- [ ] Variant test cases
- [ ] Notes on known issues or edge cases
- [ ] Reference to previous incidents
- [ ] Performance expectations
- [ ] Dependencies on other tests

### Do Not Include
- Implementation details (how to code the test)
- Framework-specific code
- Test results or execution history
- Detailed assertion library syntax

---

## Quality Checklist for Section 4

- [ ] All test cases have unique IDs
- [ ] All test cases have clear objectives
- [ ] All pre-conditions are complete
- [ ] All test sequences are numbered and ordered logically
- [ ] All expected results are comprehensive
- [ ] All assertions are specific and measurable
- [ ] All AC references are accurate
- [ ] All post-conditions are documented
- [ ] All test cases are independent (can run in any order)
- [ ] No ambiguous or vague language
- [ ] No implementation details in test descriptions
- [ ] Variant tests are clearly marked
- [ ] Test execution dependencies are documented
- [ ] Parallel execution possibilities are noted
