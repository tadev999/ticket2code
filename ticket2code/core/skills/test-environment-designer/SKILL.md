---
name: test-environment-designer
description: "Design and generate a comprehensive environment setup documentation (Section 3) including database configs, API endpoints, mock services, test data initialization scripts, and validation checklists."
argument-hint: "Target system architecture, database type, mock services list, and test case requirements"
user-invocable: true
disable-model-invocation: false
---

# Test Environment Designer

## What This Skill Produces
A detailed, standardized environment setup specification (Section 3 of the test plan report) that contains:
- **Environment Overview:** Configuration parameters for database, external APIs, and frameworks.
- **Pre-conditions:** Initial system states, user accounts, and credentials.
- **Service Mocks:** Detailed definitions of mocked services, endpoints, and latency scenarios.
- **Test Data Fixtures:** JSON/SQL structure representing test datasets (users, accounts, limits).
- **Procedures:** Step-by-step setup, teardown, and cleanup scripts.
- **Validation Checklist:** Checks to verify the environment is correctly initialized.

## When To Use
Use this skill when:
- Designing integration test plans (`/t2c_integration_tests`).
- Creating screen transition test cases (`/t2c_screen_transition_tests`).
- Documenting deployment configurations and developer setup instructions.

---

## Procedure

### 1. Identify Environment Constraints
Define the database engine (PostgreSQL, SQLite, MySQL, In-Memory), environment variables, API endpoints, and mock servers needed to run the test cases.

### 2. Specify Pre-conditions
- **Users/Roles:** List all required mock user profiles, active/inactive statuses, and associated permissions.
- **Data States:** State what transactions, historical records, and states must exist prior to test execution.
- **System Configs:** Specify feature flags, threshold limits, locales, and timezones.

### 3. Detail API & Service Mocks
- Document the URL endpoints, request payloads, and expected response payloads (success, decline, timeout, error).
- Define latency/delay settings to test async behavior and retry limits.

### 4. Construct Data Fixtures
Generate clear, reproducible JSON, CSV, or SQL fixtures for database initialization. Ensure all data fields are explicitly declared.

### 5. Document Setup & Teardown Procedures
Write step-by-step execution scripts for:
- **One-time setup:** Database migration, service launch, connectivity checks.
- **Per-test setup:** Transaction boundaries, state resets, database seed reloading.
- **Per-test teardown:** Transaction rollbacks, connections closure.
- **One-time teardown:** Killing mock services, deleting temporary files, archiving logs.

---

## Output Template

Use the following Markdown structure for Section 3 of the test report:

```markdown
# Section 3: Environment Setup

## Environment Overview
| Aspect | Configuration |
|---|---|
| Test Database | [Type e.g., SQLite in-memory] |
| External Services | [List of mocked/real endpoints] |
| Test Framework | [e.g., XCTest, PyTest, Jest] |

## Pre-conditions (Initial System State)
### User Accounts
- **Test User 1 (`user_standard`):** Role: standard user, Status: active, Balance: [AMOUNT] [CURRENCY]
- **Test User 2 (`user_privileged`):** Role: privileged, Status: active, Balance: [AMOUNT] [CURRENCY]

### System Configurations
- **Feature Flags:** `FEATURE_PAYMENT_V2=true`
- **Locale/Timezone:** Locale: `[locale]`, Timezone: `[timezone]`

## Configuration Details
### API Endpoints
```
Base URL: https://api-staging.example.com
Payment API: /v1/payments
```

### Service Mocks
- **Payment Mock Gateway:** URL: `http://localhost:8081`
  - *Success Case:* `{ status: 'approved', transactionId: 'TXN-123' }`
  - *Decline Case:* `{ status: 'declined', reason: 'insufficient_funds' }`

## Setup Procedures
### Procedure 1: One-time Setup
1. Run migrations: `./scripts/migrate_test_db.sh`
2. Start mock services: `./bin/mock_services &`

### Procedure 2: Per-Test Setup Example
```swift
// Per-test setup hook
setup() {
    resetTestDatabase()
    loadTestFixtures()
}
```

## Environment Validation Checklist
- [ ] Database is created and accessible.
- [ ] Mock services are running and healthy.
- [ ] Fixtures load successfully with correct data counts.
```
