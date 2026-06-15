# AC Decomposition Rules (5 Passes)

Goal:
- Reach the smallest independently testable unit per AC.

Apply passes in order and stop when no further split is possible.

## Pass 1 — Structural split
Split by connectors that produce different outcomes: if / else / when / and / or.
- Rule: one different outcome = one AC item.
- Example: If A -> X, otherwise -> Y => AC-xx-a (X), AC-xx-b (Y)

## Pass 2 — Condition-value split
When same behavior is tested across multiple discrete values, make one AC per value.
- Applies to: error codes, HTTP status codes, enum values, feature flags, roles, OS versions, payment methods.
- Example: dialog for ERR001, ERR002, ERR003 => AC-xx-ERR001, AC-xx-ERR002, AC-xx-ERR003

## Pass 3 — Lifecycle/timing split
Split by lifecycle points.
- Lifecycle points: on-open, on-success, on-error, on-dismiss, on-retry, on-timeout, on-foreground, on-reconnect.
- Example: show dialog on error; return on close => AC-xx-a, AC-xx-b

## Pass 4 — Side-effect split
Each observable side effect is an AC item.
- Side effects: UI change, navigation, API call triggered/blocked, local write, analytics event, cache invalidation, notification, timer reset, logging.

## Pass 5 — Negative/boundary split
Negative conditions and boundaries are standalone ACs.
- Example: do not call API-B if API-A fails is separate from call API-B if API-A succeeds.

## Labeling
- Use AC-<group>-<sub> (example: AC-03-a, AC-03-b).
- If no explicit AC exists, derive from requirement text and tag as (derived).
