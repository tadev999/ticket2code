# Decision Gates

## Purpose
Document decision points and gates throughout the test case generation workflow.

## Gate Locations

### Gate 0.5: Execution Phase Confirmation
**Question:** Which execution phase should be used for this run?

**Options:**
- [ ] **Pre-Dev** → Requirement-first planning mode
- [ ] **Post-Dev** → Implementation-aware validation mode
- [ ] **Cancel** → Stop workflow

**Rule:** Never proceed without explicit phase selection.

### Gate 1: After Stage 4 (Analysis Complete)
**Question:** Do you approve the test analysis and proposed test categories?

**Options:**
- [ ] **Yes, proceed** → Continue to Stage 5
- [ ] **Adjust analysis** → Revise scope and pre-conditions, re-present
- [ ] **Add/remove categories** → Modify category list, re-present
- [ ] **Cancel** → Stop workflow

**Rule:** Never proceed without explicit approval.

### Gate 2: After Stage 6 (Environment Setup Complete)
**Question:** Is the environment setup complete and correct?

**Options:**
- [ ] **Yes, correct** → Continue to Stage 7
- [ ] **Adjust setup** → Modify configuration, test data, or mocks, re-present
- [ ] **Add requirements** → Add missing services or data, re-present
- [ ] **Cancel** → Stop workflow

**Rule:** Never proceed without explicit approval.

### Gate 3: After Stage 8 (Test Sequences Complete)
**Question:** Are all test sequences clear and ready for execution?

**Options:**
- [ ] **Yes, ready** → Continue to Stage 9
- [ ] **Clarify sequence** → Revise steps or expected results, re-present
- [ ] **Add test cases** → Add missing scenarios, re-present
- [ ] **Cancel** → Stop workflow

**Rule:** Never proceed without explicit approval.

### Gate 4: Final Gate (Coverage Complete)
**Question:** Is test coverage adequate?

**Options (Post-Dev):**
- [ ] **Yes, approved** → Complete and generate report
- [ ] **Add coverage** → Create additional test cases for gaps
- [ ] **Document gap** → Record why coverage is incomplete, generate report
- [ ] **Cancel** → Stop workflow

**Options (Pre-Dev):**
- [ ] **Yes, draft approved** → Complete draft planning report
- [ ] **Adjust draft** → Revise assumptions/unknowns/re-validation checklist
- [ ] **Cancel** → Stop workflow

**Rule:** Never sign off without explicit assessment for the selected phase.

---

## Gate Documentation

When recording gate decisions, document:

```
## Gate X: [Gate Name]

**Date:** [Date and time]
**Decision:** [Yes/No/Adjust/Cancel]
**Approver:** [Name/Email]
**Rationale:** [Brief explanation of decision]

[If adjusted/clarified:]
**Changes Made:**
- [Change 1]
- [Change 2]
```

---

## Decision Escalation

If stakeholder cannot decide at a gate:

1. **Record blocker** in report
2. **List decision options** clearly
3. **Provide recommendation** from test lead
4. **Escalate to** [manager/product owner]
5. **Continue when resolved**

```
## Blocker: [Gate Name]

**Issue:** [What prevents decision]
**Options:**
1. [Option A] - Pros: [...] Cons: [...]
2. [Option B] - Pros: [...] Cons: [...]

**Recommendation:** [Which option is preferred and why]

**Escalated to:** [Name/Date]
**Resolved on:** [Date and decision]
```

---

## Quality Assurance Gates

In addition to workflow gates, enforce these quality checks:

### QA Gate 1: AC Completeness
**Check:** All acceptance criteria are decomposed into atomic AC

**Validation:**
- [ ] Every AC has trigger, condition, and expected output
- [ ] No ambiguous or vague AC remain
- [ ] All AC are traceable to original ticket

### QA Gate 2: Test Case Completeness
**Check:** Every test case has required elements

**Validation:**
- [ ] Every TC has ID, scenario, objective
- [ ] Every TC has pre-conditions and test sequence
- [ ] Every TC has expected results and assertions
- [ ] Every TC has related AC mapping

### QA Gate 3: Coverage Completeness
**Check:** All AC are covered by test cases

**Validation:**
- [ ] Every AC has at least one test case
- [ ] Every test case has at least one related AC
- [ ] Coverage matrix is complete and accurate
- [ ] No orphaned test cases or AC

---

## Gate Decision Record Template

Use this template to document all gate decisions:

```
# Gate Decision Record: [TICKET-ID]_gates_[TIMESTAMP]

## Gate 0.5: Execution Phase
**Status:** [ ] Pending [ ] Pre-Dev [ ] Post-Dev
**Approver:** [Name]
**Decision Date:** [Date]
**Notes:** [Any notes or conditions]

## Gate 1: Analysis Approval
**Status:** [ ] Pending [ ] Approved [ ] Adjusted
**Approver:** [Name]
**Decision Date:** [Date]
**Notes:** [Any notes or conditions]

## Gate 2: Environment Setup Approval
**Status:** [ ] Pending [ ] Approved [ ] Adjusted
**Approver:** [Name]
**Decision Date:** [Date]
**Notes:** [Any notes or conditions]

## Gate 3: Test Sequence Approval
**Status:** [ ] Pending [ ] Approved [ ] Adjusted
**Approver:** [Name]
**Decision Date:** [Date]
**Notes:** [Any notes or conditions]

## Gate 4: Coverage Approval
**Status:** [ ] Pending [ ] Approved [ ] Approved with Gaps
**Approver:** [Name]
**Decision Date:** [Date]
**Coverage %:** [Percentage]
**Gaps:** [If any, documented]
**Notes:** [Any notes or conditions]

## Overall Status
**Final Decision:** [ ] Approved [ ] Approved with Gaps [ ] Rejected
**Overall Coverage:** [Percentage]
**Ready for Execution:** [ ] Yes [ ] No
```

---

## Workflow State Machine

```
┌─────────────────┐
│  Start Workflow │
└────────┬────────┘
         │
         v
  ┌────────────────┐
  │ Stage 1-3:     │
  │ Analyze & Plan │
  └────────┬───────┘
         │
         v
  ┌────────────────────────┐
  │ Gate 1: Approved?      │
  └────────┬───────────────┘
         │
    ┌────┴────┐
    │          │
   Yes        No/Adjust
    │          │
    v          v
  ┌──┐    ┌─────────────┐
  │  │    │ Adjust      │
  │  │    │ & Re-review │
  │  │    └────────┬────┘
  │  │             │
  │  │             └──────┐
  │  │                    │
  │  v                    v
  │┌────────────────────────────┐
  ││ Stage 4-6: Setup & Design  │
  │└────────────┬───────────────┘
  │             │
  │             v
  │    ┌────────────────────────┐
  │    │ Gate 2: Approved?      │
  │    └────────┬───────────────┘
  │           │
  │      ┌────┴────┐
  │      │          │
  │     Yes        No/Adjust
  │      │          │
  │      v          v
  │    ┌──┐    ┌──────────┐
  │    │  │    │ Revise   │
  │    │  │    └────┬─────┘
  │    │  │         │
  │    │  │         └──┐
  │    │  │            │
  │    v  v            v
  │  ┌──────────────────────────┐
  │  │ Stage 7-8: Test Cases    │
  │  └────────────┬─────────────┘
  │               │
  │               v
  │      ┌────────────────────────┐
  │      │ Gate 3: Approved?      │
  │      └────────┬───────────────┘
  │            │
  │       ┌────┴────┐
  │       │          │
  │      Yes        No/Adjust
  │       │          │
  │       v          v
  │     ┌──┐    ┌──────────┐
  │     │  │    │ Refine   │
  │     │  │    └────┬─────┘
  │     │  │         │
  │     │  │         └──┐
  │     │  │            │
  │     v  v            v
  │   ┌───────────────────────────┐
  └─> │ Stage 9: Coverage Analysis│
      └────────────┬──────────────┘
                   │
                   v
           ┌───────────────────────┐
           │ Gate 4: Coverage OK?  │
           └────────┬──────────────┘
                  │
              ┌───┴────┐
              │         │
             Yes       No/Gaps
              │         │
              v         v
            ┌──┐   ┌──────────────┐
            │  │   │ Document Gap │
            │  │   │ or Add Tests │
            │  │   └────┬─────────┘
            │  │        │
            │  │        └──────┐
            │  │               │
            v  v               v
         ┌──────────────────────────┐
         │ Generate Final Report    │
         └─────────┬────────────────┘
                   │
                   v
         ┌──────────────────────────┐
         │  Complete & Save Report  │
         └──────────────────────────┘
```

---

## Approval Delegation

If primary approver is unavailable:

| Role | Primary Approver | Delegate |
|------|---|---|
| Analysis | QA Lead | Dev Lead |
| Environment Setup | Test Infrastructure | QA Lead |
| Test Sequence | QA Lead | Senior QA |
| Coverage | QA Lead + Dev Lead | Product Owner |

---

## Gate Escalation Criteria

Escalate a gate decision if:
- Gate decision blocks progress >1 business day
- Stakeholders cannot agree on decision
- Decision has significant resource impact
- Decision affects other tickets or projects

**Escalation Process:**
1. Document decision blocker
2. List all options and impact analysis
3. Provide team recommendation
4. Escalate to [Manager/Director] with context
5. Record final decision
6. Continue workflow with decision
