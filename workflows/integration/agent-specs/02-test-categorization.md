# Test Categorization Rules

## Purpose
Classify integration test cases into clear, non-overlapping categories for organized test planning and execution.

## Standard Test Categories

### 1. UI/UX (User Interface & Experience)
Tests for user-facing behavior and interactions.

**Scope:**
- Visual elements display correctly
- User interactions (taps, gestures, text input) work as expected
- Navigation between screens flows correctly
- UI states respond to user actions
- Error messages display appropriately
- Screen layout and formatting is correct

**Example Test Cases:**
- TC-UI-001: User can navigate to payment screen
- TC-UI-002: Payment amount input accepts numeric values
- TC-UI-003: Error message displays when amount is invalid
- TC-UI-004: Loading indicator shows during processing

---

### 2. Business Logic (Core Functionality)
Tests for business rules and functional behavior.

**Scope:**
- Business rules are enforced (e.g., payment limits, user permissions)
- Conditional logic works correctly
- State transitions happen as expected
- Calculations and transformations are correct
- Decision trees are evaluated properly

**Example Test Cases:**
- TC-BL-001: System enforces minimum payment amount
- TC-BL-002: Daily transaction limit is enforced
- TC-BL-003: User role determines available features
- TC-BL-004: Discount is calculated correctly

---

### 3. Data Persistence (Storage & Retrieval)
Tests for data integrity and persistence.

**Scope:**
- Data is stored correctly in database/cache
- Data can be retrieved accurately
- Data relationships are maintained
- Old data is not lost when new data is added
- Data is consistent across retrievals
- Database transactions are atomic

**Example Test Cases:**
- TC-DP-001: Payment record is saved to database
- TC-DP-002: Transaction history is retrieved correctly
- TC-DP-003: Database rollback works on failure
- TC-DP-004: Concurrent writes don't corrupt data

---

### 4. API Integration (External Services)
Tests for communication with external APIs and services.

**Scope:**
- Requests to external APIs are formatted correctly
- API responses are parsed correctly
- Authentication with external services works
- Timeouts and retries are handled
- Error responses from APIs are handled gracefully
- Data transformation between app and API is correct

**Example Test Cases:**
- TC-API-001: Payment API is called with correct parameters
- TC-API-002: API success response is processed correctly
- TC-API-003: API timeout triggers retry logic
- TC-API-004: Invalid API response shows error to user

---

### 5. Error Handling & Recovery
Tests for exception handling and recovery scenarios.

**Scope:**
- Invalid inputs are caught and handled
- Network errors trigger appropriate responses
- Server errors are reported to user
- System recovers from partial failures
- User can retry failed operations
- Error states are logged appropriately

**Example Test Cases:**
- TC-EH-001: Invalid email input shows validation error
- TC-EH-002: Network timeout shows retry prompt
- TC-EH-003: Server error response displays user-friendly message
- TC-EH-004: Failed payment can be retried

---

### 6. Security & Authentication
Tests for security mechanisms and access control.

**Scope:**
- Authentication is verified before sensitive operations
- Unauthorized users cannot access restricted features
- Sensitive data is not exposed
- Session management works correctly
- Credentials are handled securely
- CSRF/XSRF protection is in place

**Example Test Cases:**
- TC-SEC-001: Unauthenticated user cannot access dashboard
- TC-SEC-002: Session expires after timeout
- TC-SEC-003: Password is not logged or exposed
- TC-SEC-004: User cannot access other users' data

---

### 7. Performance & Load
Tests for system performance under various conditions.

**Scope:**
- Operations complete within acceptable time
- System handles moderate concurrent users
- Memory usage is reasonable
- Large data sets are processed efficiently
- Caching works as expected
- UI remains responsive during long operations

**Example Test Cases:**
- TC-PERF-001: Payment processing completes within 3 seconds
- TC-PERF-002: System handles 100 concurrent users
- TC-PERF-003: Large transaction history loads in < 1 second
- TC-PERF-004: UI remains responsive during background sync

---

### 8. Integration & Dependencies
Tests for interactions between components.

**Scope:**
- Multiple modules work together correctly
- Component dependencies are resolved
- State is shared appropriately between components
- Circular dependencies don't occur
- Component boundaries are maintained
- Integration with framework lifecycle is correct

**Example Test Cases:**
- TC-INT-001: Payment module works with user module
- TC-INT-002: Notification system triggers from payment module
- TC-INT-003: Database changes trigger UI updates
- TC-INT-004: Component lifecycle methods are called in order

---

### 9. Edge Cases & Boundary Conditions
Tests for unusual or extreme inputs.

**Scope:**
- Minimum and maximum values are handled
- Empty/null inputs are handled
- Very long strings are handled
- Special characters in input are handled
- Rapid successive operations work
- System recovers from extreme states

**Example Test Cases:**
- TC-EDGE-001: Zero amount is rejected
- TC-EDGE-002: Maximum amount is accepted
- TC-EDGE-003: Very long user name is truncated
- TC-EDGE-004: Rapid taps on button don't cause duplicates

---

### 10. Regression Prevention
Tests for known bugs or previous incidents.

**Scope:**
- Previously fixed bugs don't reappear
- Related features remain functional after changes
- Known edge cases continue to work
- Performance doesn't degrade

**Example Test Cases:**
- TC-REG-001: Previously fixed amount-validation bug remains resolved
- TC-REG-002: Concurrent submission scenario remains stable
- TC-REG-003: Embedded webview flow still behaves correctly

---

## Categorization Rules (Mandatory)

### Rule 1: Mutually Exclusive
Each test case belongs to **exactly one primary category**.

If a test touches multiple areas, assign to the **primary** category:
- Primary = the main focus or system under test
- Secondary categories can be noted but not assigned

### Rule 2: Exhaustive Coverage
Every test case must fit into one of the standard categories.

If a test doesn't fit, either:
- Broaden the category description, or
- Create a new justified category with clear scope

### Rule 3: Clear Naming
Test case names must indicate category and scenario:

Format: `TC-[CATEGORY]-[SEQUENCE]: [Scenario description]`

Examples:
- `TC-UI-001: User taps pay button and navigation succeeds`
- `TC-BL-003: System enforces daily transaction limit`
- `TC-API-002: Payment API timeout triggers 3 retries`

---

## Context-Specific Customization

For specific domains, add custom categories:

### Mobile App Testing
- **UI/UX**: Add subtypes (Views, Navigation, Gestures)
- **Performance**: Add device-specific metrics (CPU, Memory, Battery)
- **Integration**: Add local storage, Cache, Network layer

### API Service Testing
- Remove: UI/UX, Performance (except endpoint latency)
- Add: Schema validation, Rate limiting, API versioning

### E-commerce/Payment System
- Add: Payment gateway integration, Tax calculation
- Expand: Security & Authentication, Error Handling

---

## Validation Checklist

Before finalizing test categories:
- [ ] Each category has clear, non-overlapping scope
- [ ] Every test case assigned to exactly one category
- [ ] No test cases left unassigned
- [ ] Category distribution is reasonable (no >60% in one category)
- [ ] All AC are covered by at least one category
- [ ] Category names match project terminology
