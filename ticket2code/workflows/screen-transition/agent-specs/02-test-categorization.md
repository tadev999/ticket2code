# Test Categorization Rules

## Purpose
Classify screen transition test cases into clear, non-overlapping groups so each navigation scenario is easy to review and execute.

## Standard Transition Categories

### 1. Critical Path Transition (CP)
Main user flow that must always work.

Examples:
- TC-CP-001: Home -> Tap Mini App -> Mini App Top
- TC-CP-002: Product List -> Tap Item -> Product Detail

### 2. Alternate Path Transition (ALT)
Valid alternate routes from the same start point.

Examples:
- TC-ALT-001: Home -> Tap Notification Banner -> Campaign Detail
- TC-ALT-002: Product Detail -> Tap Related Item -> Product Detail (another item)

### 3. Error Recovery Transition (ERR)
Transitions when input/network/service failure occurs.

Examples:
- TC-ERR-001: OTP Screen -> Invalid OTP Submit -> OTP Error Dialog
- TC-ERR-002: Checkout -> Network Timeout -> Retry Bottom Sheet

### 4. Back Navigation Transition (BACK)
Transitions using back button, close button, or cancel flow.

Examples:
- TC-BACK-001: Product Detail -> Tap Back -> Product List
- TC-BACK-002: Payment Confirm -> Tap Cancel -> Payment Form

### 5. Entry Point Transition (ENTRY)
Transitions started from deep link, push notification, or external trigger.

Examples:
- TC-ENTRY-001: Deep Link -> Mini App Landing
- TC-ENTRY-002: Push Notification -> Transaction Detail

### 6. Regression Transition (REG)
Transitions derived from known release incidents and must not regress.

Examples:
- TC-REG-001: Embedded webview header route remains correct
- TC-REG-002: Concurrent token refresh route remains stable

## Categorization Rules (Mandatory)

### Rule 1: One Primary Category
Each test case belongs to exactly one primary category.

### Rule 2: Explicit Transition Edge
Each test case must include at least one explicit transition edge:
`From Screen -> Action -> To Screen`

### Rule 3: Naming Convention
Use format `TC-[CATEGORY]-[NNN]: [From] -> [To]`

Examples:
- `TC-CP-001: Home -> Mini App Top`
- `TC-ERR-002: Checkout -> Retry Bottom Sheet`

## Validation Checklist

- [ ] Each test case has one primary category
- [ ] Each test case declares From Screen and To Screen
- [ ] All AC are covered by at least one category
- [ ] Critical Path category exists
- [ ] Error Recovery category exists when AC has failure branches
