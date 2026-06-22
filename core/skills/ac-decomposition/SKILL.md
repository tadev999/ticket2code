---
name: ac-decomposition
description: "Decompose raw JIRA ticket acceptance criteria (AC) into atomic, testable, and traceable units using the 5-pass rule."
argument-hint: "List of raw acceptance criteria, ticket text, and epic/parent context"
user-invocable: true
disable-model-invocation: false
---

# Acceptance Criteria (AC) Decomposition

## What This Skill Produces
- A structured list of atomic AC items, each consisting of:
  - **Trigger:** What action or condition initiates the behavior.
  - **Condition:** What value or state must be true.
  - **Expected Output:** What observable result occurs (UI changes, navigation, API calls, DB writes, logs).
- Traceable labels mapping each atomic item back to the original AC (e.g., `AC-<group>-<sub>`).

## When To Use
Use this skill when:
- Preparing a grooming-ready requirement analysis.
- Decomposing acceptance criteria before writing code changes.
- Setting up the validation matrix for code review (`/t2c_review`).
- Structuring integration and screen transition test cases (`/t2c_integration_tests` and `/t2c_screen_transition_tests`).

---

## Procedure: The 5-Pass Rules

Apply the following passes in order to reach the smallest independently testable unit. Stop when no further splitting is possible.

### Pass 1: Structural Split
Split by logical connectors that produce different outcomes: `if`, `else`, `when`, `and`, `or`.
*   **Rule:** One distinct outcome/branch = one atomic AC item.
*   **Example:** "If User is admin, show Dashboard, otherwise show Home" 
    *   `AC-01-a`: Show Dashboard (if admin).
    *   `AC-01-b`: Show Home (if not admin).

### Pass 2: Condition-Value Split
When the same behavior is tested across multiple discrete values, make one atomic AC per value.
*   **Applies to:** Error codes, HTTP status codes, enum values, feature flags, user roles, OS versions, payment methods.
*   **Example:** "Show custom error dialog for ERR001, ERR002, and ERR003"
    *   `AC-02-ERR001`: Dialog for ERR001.
    *   `AC-02-ERR002`: Dialog for ERR002.
    *   `AC-02-ERR003`: Dialog for ERR003.

### Pass 3: Lifecycle/Timing Split
Split by lifecycle phases and action timing.
*   **Lifecycle points:** `on-open`, `on-success`, `on-error`, `on-dismiss`, `on-retry`, `on-timeout`, `on-foreground`, `on-reconnect`.
*   **Example:** "Show progress dialog on submit, then show success message on completion, or error dialog on failure"
    *   `AC-03-submit`: Show progress on submit.
    *   `AC-03-success`: Show success on complete.
    *   `AC-03-failure`: Show error dialog on failure.

### Pass 4: Side-Effect Split
Each observable side effect must be a separate atomic AC item.
*   **Side effects:** UI updates, navigation, triggering/blocking APIs, database writes, analytics event logging, cache invalidation, push notifications, timer resets.
*   **Example:** "On success, navigate to home page and save session token"
    *   `AC-04-a`: Navigate to home page.
    *   `AC-04-b`: Save session token to local storage.

### Pass 5: Negative/Boundary Split
Negative conditions and boundaries must be modeled as standalone ACs.
*   **Example:** "Do not call API-B if API-A fails" (Separate from "Call API-B if API-A succeeds").

---

## Output Template and Format

### Labeling Policy
- Use the format: `AC-<group>-<sub>` (e.g., `AC-03-a`, `AC-03-b`).
- If no explicit AC exists in the JIRA ticket but is inferred from the description, tag it as `(derived)` (e.g., `AC-04-a (derived)`).

### Template Schema
```markdown
### Decomposed Acceptance Criteria Matrix

| ID | Trigger | Condition | Expected Output | Source Reference |
|---|---|---|---|---|
| AC-01-a | User taps "Submit" | Input form is valid | Send API request to `/submit` | Ticket Description |
| AC-01-b | User taps "Submit" | Input form is invalid | Show validation error below fields | Ticket Description |
| AC-02-a | API returns 200 OK | Response body contains valid token | Navigate to Dashboard & save token | Section 2 / Comment #3 |
| AC-02-b | API returns 401 | - | Show authentication error toast | Section 2 / Comment #3 |
```

---

## Common Pitfalls to Avoid
1.  **Merging multiple atomic items:** Do not combine navigation and data persistence in one row (e.g., "User navigates to home AND saves token" -> split into two).
2.  **Omitting conditional branches:** Ensure failure flows (timeouts, invalid inputs, network down) are explicitly captured.
3.  **Vague Expected Outputs:** Avoid "process correctly" or "update UI". Specify exactly *how* (e.g., "Label color changes to red", "POST /v1/logs is triggered").
