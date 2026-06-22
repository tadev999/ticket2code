# Section 3: Environment Setup

## Purpose
Document all environment configuration and setup procedures required to execute the integration tests.

## Template

```
# Section 3: Environment Setup

---

## Environment Overview

| Aspect | Configuration |
|--------|---|
| Test Database | [Type and connection] |
| External Services | [Mock or real] |
| Framework | [Test framework used] |
| Environment | [Dev/Staging/Production] |
| Isolation | [How tests are isolated] |

---

## Pre-conditions (Initial System State)

### User and Authentication
- **Test User 1:** [Username/ID]
  - Role: [User role]
  - Status: [Active/Inactive]
  - Permissions: [List permissions]
  - Balance/Account State: [Current state]

- **Test User 2:** [Username/ID]
  - Role: [User role]
  - Status: [Active/Inactive]
  - Permissions: [List permissions]
  - Balance/Account State: [Current state]

### Existing Data
- **Database Records:**
  - [Entity Type]: [Count] records with characteristics [details]
  - [Entity Type]: [Count] records with characteristics [details]

- **Transaction History:**
  - User 1 today: [Transaction details]
  - User 1 this month: [Summary]
  - User 2 today: [Transaction details]

### System Configuration
- **Feature Flags:**
  - Feature X: [Enabled/Disabled]
  - Feature Y: [Enabled/Disabled]

- **Limits and Thresholds:**
  - Daily limit: [Amount]
  - Transaction limit: [Amount]
  - Max retries: [Count]

- **Locale and Timezone:**
  - Locale: [ja_JP/en_US/etc.]
  - Timezone: [JST/UTC/etc.]
  - Date Format: [Format]

---

## Configuration

### Database Configuration
**Type:** [SQLite/PostgreSQL/MySQL/In-Memory]

```
Host: [localhost or connection string]
Port: [Port number or N/A]
Database: test_database_[timestamp]
Schema: Load from migrations/v001_initial.sql
Isolation Level: [SERIALIZABLE/READ_COMMITTED/etc.]
```

### API Endpoints
**Environment:** [staging/mock]

```
Base URL: https://api-staging.example.com
Payment API: /v1/payments
Verification API: /v1/verify
User API: /v1/users
```

### Environment Variables
```
API_BASE_URL=https://api-staging.example.com
API_TIMEOUT=10000
RETRY_COUNT=3
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite://test.db
FEATURE_PAYMENT_V2=true
LOCALE=[locale]
TIMEZONE=[timezone]
```

### Service Mocks
**Payment Gateway Mock:**
- URL: http://localhost:8081
- Behavior:
  - Success: Returns { status: 'approved', transactionId: 'TXN-123' }
  - Decline: Returns { status: 'declined', reason: 'insufficient_funds' }
  - Timeout: Delays 15 seconds then times out

**Email Service Mock:**
- Captures all email sends in MockNotificationCapture
- Allows inspection of sent emails in test assertions
- Can simulate delivery delays

**Notification Service Mock:**
- Captures all notifications
- Can verify notification content and timing

---

## Test Data Initialization

### Data Setup Script
```bash
# Run database migrations
./scripts/migrate_test_db.sh

# Load test fixtures
./scripts/load_test_fixtures.sh

# Initialize mock services
./scripts/init_mock_services.sh

# Verify setup
./scripts/verify_setup.sh
```

### Test Fixtures

**File:** fixtures/test_users.json
```json
{
  "users": [
    {
      "id": "user_standard",
      "email": "user_standard@test.com",
      "name": "Standard User",
      "role": "user",
      "status": "active",
      "balance": [AMOUNT],
      "dailyTransactionCount": 0,
      "dailyTransactionTotal": 0
    },
    {
      "id": "user_privileged",
      "email": "user_privileged@test.com",
      "name": "Privileged User",
      "role": "premium",
      "status": "active",
      "balance": [AMOUNT],
      "dailyTransactionCount": 0,
      "dailyTransactionTotal": 0
    }
  ]
}
```

**File:** fixtures/test_payment_methods.json
```json
{
  "paymentMethods": [
    {
      "id": "payment_method_default",
      "userId": "user_standard",
      "type": "credit_card",
      "brand": "visa",
      "last4": "1234",
      "verified": true,
      "default": true
    }
  ]
}
```

### Transaction History Setup
- User: user_standard
  - Today: 0 transactions (ready for testing)
  - Yesterday: 2 transactions totaling [AMOUNT]
  - This month: 5 transactions totaling [AMOUNT]

---

## External Service Mocks

### Payment Gateway Mock
**Library:** MockExternalService.[ext]

**Scenarios:**
1. **Success Scenario**
   - Request: { amount: [AMOUNT], currency: '[CURRENCY_CODE]', cardToken: 'token_success' }
   - Response: { status: 'approved', transactionId: 'TXN-123', timestamp: '2024-01-15T10:30:00Z' }
   - Latency: 500ms

2. **Decline Scenario**
   - Request: { amount: [AMOUNT], currency: '[CURRENCY_CODE]', cardToken: 'token_decline' }
   - Response: { status: 'declined', reason: 'insufficient_funds' }
   - Latency: 500ms

3. **Timeout Scenario**
   - Request: Any request
   - Behavior: Delay 15 seconds, then timeout
   - Allows testing retry logic

### Email Service Mock
**Library:** MockNotificationService.[ext]

**Capabilities:**
- Captures all outgoing emails in `capturedEvents` list
- Allows assertions on email content, recipients, subject
- Can simulate delivery delays

**Usage in Test:**
```swift
let capturedEvents = MockNotificationService.capturedEvents
assertEqual(capturedEvents.count, 1)
assertTrue(capturedEvents[0].to.contains("user_standard@test.com"))
assertTrue(capturedEvents[0].subject.contains("[Action] Confirmation"))
```

---

## Setup Procedures

### Procedure 1: One-time Setup (Before All Tests)

Execute once before running all tests:

```bash
#!/bin/bash
set -e

echo "=== One-time Test Environment Setup ==="

# Step 1: Verify dependencies
echo "1. Verifying test dependencies..."
command -v sqlite3 >/dev/null || { echo "sqlite3 is required"; exit 1; }

# Step 2: Create test database
echo "2. Creating test database..."
rm -f test.db
sqlite3 test.db < schema.sql

# Step 3: Load test fixtures
echo "3. Loading test fixtures..."
sqlite3 test.db < fixtures/users.sql
sqlite3 test.db < fixtures/payment_methods.sql

# Step 4: Start mock services
echo "4. Starting mock services..."
./bin/mock_payment_gateway &
MOCK_PID=$!
sleep 2

# Step 5: Verify setup
echo "5. Verifying setup..."
curl -s http://localhost:8081/health || { echo "Mock service not available"; exit 1; }

echo "=== Setup Complete ==="
```

### Procedure 2: Per-Test Setup (Before Each Test)

Execute before each test case:

```swift
// Per-test setup hook
setup() {
    // Reset database state
    resetTestDatabase()
    
    // Clear mock service state
    MockExternalService.reset()
    MockNotificationService.capturedEvents.removeAll()
    
    // Reload test data
    loadTestFixtures()
    
    // Start fresh transaction
    beginTransaction()
}
```

### Procedure 3: Per-Test Teardown (After Each Test)

Execute after each test case:

```swift
// Per-test teardown hook
tearDown() {
    // Rollback transaction
    rollbackTransaction()
    
    // Verify no leaked resources
    assertEqual(MockExternalService.activeConnections(), 0)
    
    // Log test result
    print("Test completed: \(name)")
}
```

### Procedure 4: One-time Teardown (After All Tests)

Execute once after all tests:

```bash
#!/bin/bash

echo "=== One-time Cleanup ==="

# Kill mock services
pkill -f mock_payment_gateway || true

# Clean up database
rm -f test.db
rm -rf temp_test_files/

# Archive logs
mkdir -p logs_archive
tar -czf logs_archive/test_logs_$(date +%s).tar.gz logs/

echo "=== Cleanup Complete ==="
```

---

## Dependency Management

### Required Dependencies
- SQLite3: For test database
- [Test Framework]: For test execution
- Mock Libraries: For service mocking

### Optional Dependencies
- Docker: For containerized external services
- Test Data Generators: For large data sets

### Dependency Versions
| Dependency | Version | Purpose |
|---|---|---|
| [Test Framework] | [Framework version] | Test framework |
| SQLite3 | 3.40+ | Test database |

---

## Environment Validation Checklist

- [ ] Database is created and accessible
- [ ] Test fixtures are loaded correctly
- [ ] All users exist with correct attributes
- [ ] All payment methods are configured
- [ ] Transaction history is set up correctly
- [ ] Mock services are running
- [ ] API endpoints are reachable
- [ ] Environment variables are set
- [ ] Configuration is correct
- [ ] All setup procedures are documented
- [ ] All teardown procedures are documented
- [ ] Setup can be automated via scripts
- [ ] Setup is reproducible on any machine
- [ ] Documentation is clear and complete

---

## Troubleshooting Setup Issues

### Issue: Database connection fails
- Verify SQLite3 is installed: `sqlite3 --version`
- Check database file exists: `ls -la test.db`
- Check permissions: `chmod 666 test.db`

### Issue: Mock service not responding
- Verify service is running: `curl http://localhost:8081/health`
- Check firewall: `lsof -i :8081`
- Restart service: `pkill -f mock; sleep 1; ./bin/mock_payment_gateway &`

### Issue: Test fixtures not loaded
- Verify schema exists: `sqlite3 test.db '.schema'`
- Check fixture SQL syntax: `sqlite3 test.db < fixtures/users.sql`
- Verify file permissions

```

---

## Section 3 Composition Rules

### Required Elements
- [ ] Environment overview table
- [ ] Pre-conditions documentation
  - [ ] User/authentication setup
  - [ ] Existing data requirements
  - [ ] System configuration
- [ ] Configuration details
  - [ ] Database configuration
  - [ ] API endpoints
  - [ ] Environment variables
  - [ ] Service mocks
- [ ] Test data fixtures
  - [ ] Users and accounts
  - [ ] Payment methods
  - [ ] Transaction history
- [ ] External service mocks
  - [ ] Mock descriptions
  - [ ] Scenario definitions
  - [ ] Response examples
- [ ] Setup procedures (one-time, per-test, teardown)
- [ ] Validation checklist
- [ ] Troubleshooting guide (optional)

### Do Not Include
- Detailed test sequences (save for Section 4)
- Test assertions (save for Section 4)
- Coverage analysis (save for Section 5)

---

## Quality Checklist

- [ ] All environment requirements are explicitly stated
- [ ] Pre-conditions are complete and reproducible
- [ ] Configuration is documented with values
- [ ] Test data fixtures are clear and correct
- [ ] Mock services are well-defined
- [ ] Setup procedures are step-by-step
- [ ] Teardown procedures are complete
- [ ] Validation checklist is comprehensive
- [ ] Documentation is clear enough for another developer to reproduce
- [ ] No manual steps that can't be automated
