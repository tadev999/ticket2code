# Language and Convention — Screen Transition Test Report

## Document Language and Style

### Language
- Language must come from explicit Stage 0 selection (`Selected communication language`).
- Do not infer report language from ticket/AC language or user message language.
- Use `Selected communication language` consistently for AI-DEV conversation and report narrative.
- Communication language selection does not control implementation language, framework, or code syntax.
- Maintain consistency throughout the document

### Execution Phase Labeling
- Execution phase must come from explicit Stage 0.5 selection (`Selected execution phase`).
- Allowed values: `Pre-Dev`, `Post-Dev`.
- Report must include all of the following in Section 1 header:
  - `Selected execution phase`
  - `Report mode` (`Draft Planning` for Pre-Dev, `Implementation-aware Validation` for Post-Dev)
  - `Confidence level` (`Requirement-derived` for Pre-Dev, `Implementation-aware` for Post-Dev)
- `Pre-Dev` report must include disclaimer: implementation may differ and re-run is required after code is ready.
- `Post-Dev` report should include transition evidence references when available.

### Tone and Voice
- **Professional and precise**: Clear, specific language
- **Action-oriented**: Active voice preferred
- **Testable focus**: All descriptions must be verifiable
- **Non-ambiguous**: Avoid vague terms like "might", "could", "maybe"

**Example Good:** "User enters [AMOUNT] and system accepts the amount"  
**Example Bad:** "User might enter an amount and the system could process it"

---

## Markdown Formatting Standards

### Headings
```
# Main Section (Heading 1)
## Subsection (Heading 2)
### Sub-subsection (Heading 3)
#### Details (Heading 4)
```

### Lists
Use markdown lists for clarity:

**Unordered list:**
```
- Item 1
- Item 2
  - Sub-item 2a
  - Sub-item 2b
```

**Ordered list:**
```
1. Step 1
2. Step 2
3. Step 3
```

**Checkbox list:**
```
- [ ] Assertion 1
- [ ] Assertion 2
```

### Code Blocks
Use backticks for file references, variable names, and code:

```
`user_email`, `payment_amount`, `TransactionRecord`
```

For multi-line examples:
```python
response = api.payment.create(
    amount=[AMOUNT],
    currency='[CURRENCY_CODE]'
)
```

### Tables
Use markdown tables for matrices and comparisons:

```
| AC ID | Description | Test Case | Status |
|-------|---|---|---|
| AC-1.1 | User enters amount | TC-UI-001 | ✓ |
```

### Links and References
Link to related documents:
```
See [repository testing standards](<link-to-your-test-standards>)
```

### Emphasis
```
**Bold** for important terms
*Italic* for emphasis
`Code` for technical terms
```

---

## Naming Conventions

### Test Case Names
Format: `TC-[CATEGORY]-[NNN]: [From Screen] -> [To Screen]`

Examples:
- `TC-CP-001: Home -> Mini App Top`
- `TC-ERR-002: Checkout -> Retry Bottom Sheet`
- `TC-BACK-001: Detail -> List`

### Acceptance Criteria IDs
Format: `AC-[SEQUENCE].[SUB]`

Examples:
- `AC-1.1`, `AC-1.2`, `AC-1.3`
- `AC-2.1`, `AC-2.2`

### Categories
Use transition category names (from 03-test-categorization.md):
- `Critical Path`
- `Alternate Path`
- `Error Recovery`
- `Back Navigation`
- `Entry Point`
- `Regression Transition`

### Step IDs
Format: `Step [N]` or `Step [N.1], Step [N.2]` for sub-steps

---

## Standard Abbreviations

Use these abbreviations for consistency:

| Term | Abbreviation |
|------|---|
| Acceptance Criteria | AC |
| Test Case | TC |
| Test Sequence | TS |
| Pre-condition | Pre-req |
| Post-condition | Post-req |
| Expected | Exp. |
| Verification | Verif. |
| Maximum | Max |
| Minimum | Min |

---

## Terminology Standards

### User/System Actions
- **User actions:** "User enters", "User taps", "User clicks", "User swipes"
- **System actions:** "System creates", "System validates", "System sends", "System stores"
- **Verification:** "Verify that", "Assert that", "Confirm that"

### State Descriptions
- **Component states:** "Component becomes visible", "Component is disabled", "Component displays error"
- **Data states:** "Record is created", "Record is updated", "Record is deleted"
- **System states:** "Service is available", "Connection is established", "Cache is populated"

### Time References
- Use explicit time units: "5 seconds", "100ms", "within 3 minutes"
- Avoid vague: "quickly", "soon", "immediately" (unless specifications define)

---

## Consistency Checklist

- [ ] All test case names follow TC-[CAT]-[NNN] format
- [ ] All AC references use AC-[SEQ].[SUB] format
- [ ] All categories use standard names
- [ ] All action descriptions use active voice
- [ ] All assertions are specific and measurable
- [ ] All time references have explicit units
- [ ] All component names are consistent (used same name throughout)
- [ ] All abbreviations are from standard list
- [ ] Document language is consistent throughout
- [ ] Markdown formatting is consistent
