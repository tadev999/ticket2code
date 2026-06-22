# Test Sequence Rules

## Purpose
Define how to write clear, reproducible, and verifiable test sequences with explicit expected results.

## Test Sequence Structure

Each test case must have this structure:

```
# Test Case: [TC-CATEGORY-NNN]: [One-line scenario description]

## Objective
[1-2 sentence description of what behavior is being tested]

## Category
[Primary test category from categorization rules]

## Pre-conditions
- [Precondition 1]
- [Precondition 2]
- [System state required before test starts]

## Test Sequence

### Step 1: [Action description]
**Action:** [What the user/system does]
**Expected State Change:** [What changes as a result]

### Step 2: [Action description]
**Action:** [What the user/system does]
**Expected State Change:** [What changes as a result]

[More steps as needed]

## Expected Result
[Overall outcome after all steps]

## Assertions
- [ ] [Verifiable assertion 1]
- [ ] [Verifiable assertion 2]
- [ ] [Verifiable assertion 3]

## Post-conditions
- [System state after test completes]
- [Cleanup actions needed]

## Related AC
- [AC-X.X]: [Description of AC this test verifies]

## Notes
[Any additional context or edge cases]
```

---

## Step Definition Rules

### Rule 1: Clear Actions
Each action must be specific and observable.

**Bad:** "User interacts with payment form"  
**Good:** "User enters amount '[AMOUNT]' in the payment amount field"

**Bad:** "System processes payment"  
**Good:** "System sends payment request to PaymentGateway API with amount [AMOUNT] and card token"

### Rule 2: Expected State Changes
Describe what changes in the system after each action.

**Template:** After [Action], [Component] [State Change]

**Examples:**
- After user taps "Pay", PaymentButton state changes to "disabled" and LoadingIndicator becomes visible
- After API returns success, TransactionRecord is created in database with status "completed"
- After user enters invalid email, ValidationError message displays below email field

### Rule 3: Sequential Clarity
Order steps logically so each builds on previous.

**Bad:** Random order that's hard to follow  
**Good:**
1. Open payment form (prerequisite)
2. Enter required fields (setup)
3. Trigger payment action (main action)
4. Verify results (assertion)

### Rule 4: Isolation
Tests should be independent and runnable in any order.

**Bad:** Test 2 depends on data created by Test 1  
**Good:** Each test sets up its own data

---

## Expected Results Format

### Structure
Every test sequence must end with explicit expected results covering:

1. **User-visible outcomes** (what user sees/experiences)
2. **Data state outcomes** (what was created/modified in database)
3. **System state outcomes** (API calls made, logs generated, etc.)
4. **Timing outcomes** (operation completed within expected time)

### Examples

**Example 1: Payment Success Flow**
```
## Expected Result
1. User-visible: Payment success page displayed showing transaction ID and confirmation details
2. Data: TransactionRecord created in database with:
   - status = 'completed'
   - amount = [AMOUNT]
   - userId = authenticated user
   - timestamp = current time
3. System: Email confirmation sent to user's registered email
4. Timing: Entire flow completes within 3 seconds
```

**Example 2: Validation Error**
```
## Expected Result
1. User-visible: Error message displayed "Please enter a valid amount"
   Error message text is shown in red below amount field
   Pay button remains enabled for retry
2. Data: No transaction record created in database
3. System: Validation error logged with user ID and invalid input
4. Timing: Validation completes within 100ms
```

**Example 3: Network Timeout**
```
## Expected Result
1. User-visible: After 10 seconds, loading indicator disappears
   Error message shown: "Connection timeout. Please try again."
   Retry button becomes available
2. Data: No transaction created (payment not processed)
3. System: Timeout error logged with timestamp and API endpoint
4. Timing: System responds to timeout within 11 seconds total
```

---

## Assertions Format

Assertions must be:
- **Specific**: Test a single behavior
- **Verifiable**: Can be checked programmatically or manually
- **Measurable**: Can be evaluated as pass/fail

### Examples

**Testable Assertions:**
- [ ] Payment success message displays with correct transaction ID
- [ ] TransactionRecord exists in database with amount [AMOUNT]
- [ ] User receives email within 5 seconds
- [ ] Payment API was called exactly once with correct parameters
- [ ] Balance is reduced by [AMOUNT] after successful payment

**Non-testable Assertions (avoid):**
- [ ] User is happy with the result ❌ (not measurable)
- [ ] System works correctly ❌ (too vague)
- [ ] Payment is processed ❌ (ambiguous, what does "processed" mean?)

---

## Related AC Mapping

Each test case must reference which atomic AC it verifies:

**Format:**
```
## Related AC
- [AC-X.X]: [AC description] → Verified by: [Step numbers that verify it]
- [AC-Y.Y]: [AC description] → Verified by: [Step numbers that verify it]
```

**Example:**
```
## Related AC
- AC-1.1: Given payment form loaded, When user enters valid amount, 
  Then amount is accepted → Verified by: Step 1, Step 2
- AC-1.3: Given validation passed, When user taps Pay, 
  Then payment is initiated → Verified by: Step 3, Step 4
```

---

## Conditional Test Sequences

For tests with multiple paths or conditions:

### Variant A: Happy Path (Success Case)
```
## Variant: Happy Path
### Step 1: [Normal flow step 1]
### Step 2: [Normal flow step 2]
## Expected Result
[Happy path outcome]
```

### Variant B: Error Case
```
## Variant: Error Case
### Step 1: [Setup that triggers error]
### Step 2: [Verification of error handling]
## Expected Result
[Error handling outcome]
```

### Variant C: Edge Case
```
## Variant: Edge Case
### Step 1: [Setup with edge case condition]
### Step 2: [Action with edge case value]
## Expected Result
[Edge case handling outcome]
```

---

## Naming Conventions

### Test Case Names
Format: `TC-[CATEGORY]-[NNN]: [Scenario]`

Examples:
- `TC-BL-001: User can pay within daily limit`
- `TC-BL-002: System blocks payment exceeding daily limit`
- `TC-EH-001: System retries on payment API timeout`

### Step Names
Format: `[Verb] [Object] [Condition]`

Examples:
- `Enter amount [AMOUNT] in payment field`
- `User taps Pay button`
- `System calls PaymentGateway API`
- `Receive success response with transaction ID`

### Expected State Names
Format: `[Component] [State] [Details]`

Examples:
- `LoadingIndicator displays with message "Processing payment..."`
- `PayButton state changes to disabled`
- `TransactionRecord created with status completed`

---

## Test Sequence Template

Use this template for consistency:

```
# Test Case: TC-[CAT]-[NNN]: [Scenario]

## Objective
[What behavior is tested - 1-2 sentences]

## Category
[Primary category]

## Pre-conditions
- User: [User state/role]
- Data: [Required data state]
- System: [System configuration needed]

## Test Sequence

### Step 1: [Action]
**Action:** [Specific action taken]
**Expected State Change:** [What changes]

### Step 2: [Action]
**Action:** [Specific action taken]
**Expected State Change:** [What changes]

[Continue steps...]

## Expected Result
**User-visible:** [What user sees]
**Data State:** [Database/storage changes]
**System State:** [Logs, API calls, internal state]
**Timing:** [When complete]

## Assertions
- [ ] [Assertion 1]
- [ ] [Assertion 2]
- [ ] [Assertion 3]

## Post-conditions
- [Cleanup needed]
- [Final system state]

## Related AC
- AC-X.X: [Description] → Steps: [Numbers]

## Variants
- [Variant A: Happy path]
- [Variant B: Error case]
- [Variant C: Edge case]
```

---

## Validation Checklist

Before finalizing test sequences:
- [ ] Every step has specific, observable action
- [ ] Every step documents expected state change
- [ ] Steps are ordered logically
- [ ] Test sequences are independent and isolated
- [ ] Expected results cover all outcome types (user, data, system, timing)
- [ ] All assertions are specific and measurable
- [ ] All assertions are verifiable
- [ ] Related AC are explicitly mapped to steps
- [ ] Pre-conditions are complete and documented
- [ ] Post-conditions and cleanup are defined
