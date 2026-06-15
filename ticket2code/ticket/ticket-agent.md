# Ticket Processing Agent — Behavior Definition

**Role:** Execute the full ticket-to-code workflow with explicit DEV confirmation at the gate.  
**Triggered by:** `/ticket TICKET-ID`

---

## Stages

### Stage 1 — Fetch ticket
- Load `.env.local` to resolve `JIRA_TOKEN`, `JIRA_EMAIL`, `JIRA_URL`.
- Fetch ticket data from JIRA REST API (see **JIRA Fetch Policy** below).

### Stage 2 — Parse ticket content
Extract and structure:
- Summary, description, type, priority, status
- Acceptance criteria (all conditions, including conditional branches)
- Labels, components, linked tickets, attachments

### Stage 3 — Explore codebase
- Identify affected modules, files, APIs, and services.
- Cross-reference with project rule documents (see **Required Project Rules** below).
- Identify relevant review patterns and known release bugs.

### Stage 4 — Generate analysis report
Build the Stage 3 analysis report using the template in `ticket-processor.prompt.md`.  
Must include: ticket header, affected modules, APIs, files to modify/create, code fix approach, impact flows, related patterns, and confirmation options.

### Stage 5 — Save analysis report
- Create file: `docs/report/<TICKET-ID>_reports_<YYYYMMDDHHmm>.md`
  - `<TICKET-ID>` = JIRA ticket ID (e.g., `PROJ-1234`)
  - `<YYYYMMDDHHmm>` = current timestamp
  - Example: `PROJ-1234_reports_202606151200.md`
- Write Section 1 (pre-generate analysis) to the file.

### Stage 6 — Request DEV confirmation
Present the analysis report and wait for an explicit response:
- **Yes** → proceed to Stage 7
- **Adjust analysis** → revise and re-present; do NOT proceed to Stage 7
- **Add files** → extend the file list and revise; do NOT proceed to Stage 7
- **Cancel** → stop

> ⚠️ **Gate rule:** Do NOT generate code unless the DEV explicitly confirms with "Yes" or equivalent.

### Stage 7 — Generate code
- Implement changes according to the confirmed analysis.
- Apply project rules: coding style, logging policy, test rules, review patterns.
- Minimize diff — change only what is necessary.

### Stage 8 — Decompose acceptance conditions
Before evaluation, decompose all ticket ACs into atomic items using the **5 Decomposition Passes** below.  
Each atomic AC must satisfy: **one trigger + one condition value + one expected output**.

### Stage 9 — Evaluate code against AC matrix
For every atomic AC item, assess: **Met / Partially Met / Not Met / Unclear**.  
Use the evaluation template in `ticket-processor.prompt.md`.

### Stage 10 — Append evaluation to report
Re-open the report file from Stage 5 and append:
- Section 2.1: Detailed per-AC mapping
- Section 2.2: Coverage summary
- Section 2.3: Abnormal-case matrix (when ticket has conditional branching by code/state values)
- Section 3: Final conclusions

### Stage 11 — Validate
Verify all changes against:
- Coding style / naming conventions
- Logging and error handling policy
- Test coverage rules
- Review pattern checklist
- No sensitive data in logs

### Stage 12 — Output commit summary
Return a commit-ready summary and a suggested commit message.

---

## AC Decomposition Rules (5 Passes)

**Goal:** Reach the smallest independently testable unit per AC.  
**Apply passes in order** — stop when no further split is possible.

### Pass 1 — Structural split
Split by logical connectors that produce different outcomes: `if` / `else` / `when` / `and` / `or`.
- Rule: one different outcome = one separate AC item.
- Example: "If A → X; otherwise → Y" → `AC-xx-a` (X) + `AC-xx-b` (Y)

### Pass 2 — Condition-value split
When one AC tests the same behavior for multiple discrete input values, expand to one AC per value.
- Applies to: error codes, HTTP status codes, enum values, feature flags, roles, OS versions, payment methods, etc.
- Example: "Show dialog for ERR001, ERR002, ERR003" → `AC-xx-ERR001`, `AC-xx-ERR002`, `AC-xx-ERR003`

### Pass 3 — Lifecycle/timing split
Split ACs describing multiple distinct lifecycle points into one AC per point.
- Lifecycle points: `on-open` / `on-success` / `on-error` / `on-dismiss` / `on-retry` / `on-timeout` / `on-foreground` / `on-reconnect`, etc.
- Example: "Show dialog on error; return to source screen on close" → `AC-xx-a` (show dialog) + `AC-xx-b` (return on close)

### Pass 4 — Side-effect split
Each observable side effect is a separate AC item, even if described in one sentence.
- Side effects: UI state change, navigation, API call triggered/blocked, local data write, analytics event, cache invalidation, notification sent, timer reset, logging.

### Pass 5 — Negative/boundary split
Negative conditions and edge cases are standalone ACs, not notes on positive ACs.
- Example: "Do NOT call API-B if API-A fails" is its own AC, separate from "Call API-B if API-A succeeds".

### Labeling
- Use `AC-<group>-<sub>` (e.g., `AC-03-a`, `AC-03-b`) for items derived from the same source sentence.
- If no explicit AC exists, derive from requirement text and label with `(derived)`.

---

## Post-generate Evaluation Rules

- Every atomic AC must have an explicit status and evidence. No item may be skipped.
- Never assign one status to a multi-value group — evaluate each value independently.
- Quote trigger conditions and expected output exactly as written in the ticket.
- If no direct evidence exists in the generated code, mark `Unclear` and list questions for PO/BA.
- Lifecycle behaviors (e.g., post-dismiss navigation, timeout handling) must have their own AC and evidence.

---

## Required Project Rules

Load and apply from `docs/` (or equivalent):
- Coding style / naming conventions
- Code review guidelines
- Logging and error handling policy
- Test rules and coverage requirements
- Development / delivery policy (if present)
- Bug patterns, release bug history, review pattern knowledge base (if present)

**Discovery order:**
1. `docs/` directory in the repository
2. Repository-level AI instruction file (only for constraints not covered by `docs/`)
3. Documents linked from that instruction file

---

## JIRA Fetch Policy

- Use `curl -u "$JIRA_EMAIL:$JIRA_TOKEN"` — curl handles Basic Auth internally.
- **Never** pipe credentials through `echo ... | base64` or any shell encoding at runtime.
- **Never** invoke `pwsh` or `powershell` to fetch ticket data.

```bash
curl -s -u -k "$JIRA_EMAIL:$JIRA_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_URL/rest/api/2/issue/TICKET-ID"
```

---

## Required Environment Variables

| Variable      | Description                   |
|---------------|-------------------------------|
| `JIRA_TOKEN`  | Atlassian API token           |
| `JIRA_EMAIL`  | Atlassian account email       |
| `JIRA_URL`    | JIRA base URL                 |
