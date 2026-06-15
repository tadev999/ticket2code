---
title: "Ticket Processor — Output Templates"
description: "Schema and templates for all report sections produced by the /ticket workflow"
---

# Ticket Processor — Output Templates

This file defines the required output format and report schema for every stage of the `/ticket` workflow.  
For stage-by-stage execution behavior, see `ticket-agent.md`.

---

## Language policy

- Output all report content in the same language as the user's message.
- If language is unclear, default to English.
- Keep section heading names consistent with the language used.

---

## Report file convention

- **Path:** `docs/report/<TICKET-ID>_reports_<YYYYMMDDHHmm>.md`
- **`<TICKET-ID>`** = JIRA ticket ID (e.g., `PROJ-1234`)
- **`<YYYYMMDDHHmm>`** = timestamp when Stage 5 creates the file
- **One file per ticket** — contains analysis → code → evaluation in sequence

---

## Section 1 — Pre-generate analysis report (Stage 5)

Saved to the report file after DEV confirmation and before code generation.

```markdown
# Full Report — <TICKET-ID>

## 1. Pre-generate analysis report

### 1.1 Ticket header
----------
TICKET: <ID>
TITLE:  <summary>
STATUS: <status>
----------
Type:            <type>
Priority:        <priority>
Estimated Scope: <small | medium | large>

### 1.2 Affected modules
- <Module name — component role>

### 1.3 APIs involved
- <API name or endpoint>

### 1.4 Files to modify / create
- <path/to/file.ext> (modify | create)

### 1.5 Code fix approach
- Main change:       <what logic/UI/state will be changed>
- Safety guardrails: <how regressions are prevented>
- Test update plan:  <what tests will be added or updated>

### 1.6 Impact flows
1. Flow: <trigger / event>
   Function path: <entry point> → <business function> → <dependencies>
   Impact: <UI state / navigation / data / side effects>
   Risk: <low | medium | high>

2. Flow: <trigger / event>
   Function path: <entry point> → <business function> → <dependencies>
   Impact: <UI state / navigation / data / side effects>
   Risk: <low | medium | high>

### 1.7 Related patterns and references
- <review pattern or known release bug>

### 1.8 Confirmation
- [ ] Yes, generate code
- [ ] Adjust analysis
- [ ] Add files
- [ ] Cancel
```

**Rules for Section 1:**
- The `TICKET / TITLE / STATUS` block must always be wrapped with `----------` lines.
- Include at least 2 impact flows for non-trivial tickets.
- Each flow must include: trigger, function path, impact, and risk level.
- `Code fix approach` must appear between `Files to modify/create` and `Impact flows`.

---

## Section 2 — Post-generate code evaluation (Stage 10)

Appended to the same report file after code generation completes.

### 2.1 Detailed per-AC mapping

One entry per AC item. Use this template for each:

```markdown
### 2.1 Detailed mapping per acceptance condition

#### <AC-ID>: <short title>

| Field                 | Content |
|-----------------------|---------|
| Source requirement    | <quoted text from ticket> |
| Normalized expectation| <one trigger + one condition value + one expected output> |
| Status                | Met / Partially Met / Not Met / Unclear |
| Code evidence         | `<file>` — `<function/method>` — `<key branch or logic>` |
| Test evidence         | `<test case name>` or None |
| Impact                | <UI / navigation / state / data / logging> |
| Gap / Risk            | <regression risk or behavior mismatch> |
| Recommendation        | <patch needed / test to add / question for PO-BA> |
```

### 2.2 Coverage summary

```markdown
### 2.2 Acceptance condition coverage summary

| Status        | Count |
|---------------|-------|
| Met           | x     |
| Partially Met | x     |
| Not Met       | x     |
| Unclear       | x     |
| **Total**     | y     |

Blocking items (prevent ticket completion):
- <AC-ID>: <reason>
```

### 2.3 Abnormal-case matrix (conditional branching)

**Include this section when the ticket defines conditional behavior by discrete values** (error codes, result codes, HTTP statuses, enum values, feature flags, roles, etc.).

```markdown
### 2.3 Abnormal-case matrix

| Case ID | Input condition                            | Expected behavior (per ticket) | Current implementation | Status        | Code / test evidence | Gap |
|---------|--------------------------------------------|-------------------------------|------------------------|---------------|----------------------|-----|
| <ID>    | <api: result=NG + code=ERR001>             | <expected>                    | <what code does>       | Met           | <file — function>    | —   |
| <ID>    | <api: result=NG + code=ERR002>             | <expected>                    | <what code does>       | Partially Met | <file — function>    | <gap description> |
| <ID>    | <api: resultCode=SESSION_EXPIRED>          | Auto-logout and redirect      | <what code does>       | Unclear       | None                 | Needs confirmation from PO/BA |
```

**Rules for Section 2.3:**
- One row per discrete value — never merge multiple values into one row.
- Lifecycle behaviors (post-dismiss navigation, on-retry, on-timeout) are separate rows.
- Do not mark `Met` for post-dialog / post-dismiss behavior unless there is explicit code evidence for the navigation/callback.

---

## Section 3 — Final conclusions (Stage 10)

```markdown
## 3. Final conclusions

**Overall status:** Complete | Mostly complete | Needs adjustment | Not complete

**Summary:**
<2–3 sentence summary of what was implemented and what remains open.>

**Blockers / open questions:**
- <question or clarification needed from PO/BA>

**Next steps:**
- <action item: test run, PO confirmation, patch, review>
```

---

## Post-Generation Code Cleanup (Stage 9.5)

**CRITICAL:** Before proceeding to code evaluation, perform systematic cleanup to remove dead code and orphaned references.

### Dead Code Removal Checklist
When removing logic paths (e.g., event handlers, conditional branches, routing logic):

1. **Event/Listener Cleanup** (applies to all languages with event systems)
   - [ ] Identify all signal emissions, event listeners, or subscriber registrations tied to removed logic
   - [ ] Search workspace for all sites where removed event is emitted/triggered
   - [ ] Search workspace for all sites where removed event is subscribed/listened to
   - [ ] Remove all event emit/signal call sites
   - [ ] Remove all event subscription/listener registration blocks
   - [ ] Remove unused event definition declarations
   - **Examples:**
     - Swift: `.send()` calls and `.sink()` subscriptions to removed publishers
     - JavaScript/TypeScript: `emit()` calls and `.on()` listener registrations
     - Python: direct callback invocations and listener subscriptions
     - Java: observer pattern registrations and event handler calls

2. **Dead Code Function Detection**
   - [ ] Identify functions/methods that only appear in removed code paths
   - [ ] Verify function is NOT called from any other location
   - [ ] Remove dead code functions if invocation count = 0
   - **Examples:**
     - Function only checking a condition that was removed upstream
     - Helper method only used by removed feature flag branch
     - Validator only invoked from deleted router method

3. **Orphaned Variable/Parameter Removal**
   - [ ] Identify variables/parameters passed to removed method/function calls
   - [ ] Verify variable is NOT used elsewhere in codebase
   - [ ] Remove unused event/listener definitions for variables with zero subscribers
   - [ ] Remove unused listener/subscription blocks that only handle removed logic
   - **Examples:**
     - Event variable only passed to removed router call → remove
     - Callback parameter only used in deleted feature branch → remove
     - State variable only updated in removed event handler → remove

4. **Verification**
   - [ ] Run compiler/type checker on all modified files — zero errors required
   - [ ] Run linter/style check — confirm no new violations introduced
   - [ ] Final search pass: verify no orphaned references remain in codebase

**Estimated time:** 10-15 minutes per significant refactor

---

## Test Execution Decision Gate (Stage 10.5)

Before running build/test commands, the agent must explicitly notify DEV that execution may take a long time.

Required interaction (same language as DEV):
- Notify: build/test can take significant time in this repository.
- Ask: "Do you want me to run build/tests now, or will you run them later yourself?"

Allowed choices:
- **Run now**
- **I will run later**
- **Skip for now**

Report requirement:
- If tests are not run by the agent, Section 3 must explicitly state: test execution deferred/skipped by DEV.

---

## Validation checklist (Stage 11)

Before closing the workflow, verify:
- [ ] Coding style and naming conventions followed
- [ ] Logging policy applied — no sensitive data in logs
- [ ] Test cases added or updated for changed behavior
- [ ] Test execution decision gate completed (run now / deferred / skipped)
- [ ] Review pattern checklist completed
- [ ] All blocking AC items resolved or documented
- [ ] Post-generation code cleanup completed (dead code + orphaned references removed)
