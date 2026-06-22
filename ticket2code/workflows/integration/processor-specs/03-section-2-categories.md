# Section 2: Test Categories

## Purpose
Document all test categories and explain the rationale for each category.

## Template

```
# Section 2: Test Categories

## Overview

This section defines the test categories used to organize and classify integration tests.
Each category focuses on a specific aspect of the system under test.

**Total Categories:** [N]
**Total Test Cases:** [N]

---

## Category Definitions and Rationale

### Category 1: [Category Name]

**Definition:**
[1-2 sentence description of what this category tests]

**Scope:**
- [What is included]
- [What is included]
- [What is NOT included]

**Why This Category:**
[Explanation of why this category is important for the ticket]

**Test Cases in This Category:**
- TC-[CAT]-001: [Scenario 1]
- TC-[CAT]-002: [Scenario 2]
- TC-[CAT]-003: [Scenario 3]

**Count:** 3 test cases

---

### Category 2: [Category Name]

[Repeat structure above]

---

## Category Distribution

| Category | Count | % |
|----------|-------|---|
| [Category 1] | 3 | 21% |
| [Category 2] | 4 | 29% |
| [Category 3] | 2 | 14% |
| [Category 4] | 3 | 21% |
| [Category 5] | 2 | 14% |
| **TOTAL** | **14** | **100%** |

**Distribution Notes:**
- Largest category: [Category] with [X]% of tests (reason: [explanation])
- Smallest category: [Category] with [X]% of tests (reason: [explanation])
- Distribution is balanced for [reason]

---

## Category Mapping to Acceptance Criteria

### Category 1: [Name]
Maps to AC:
- AC-1.1: [Description] → Test Cases: [TC-xxx, TC-yyy]
- AC-1.2: [Description] → Test Cases: [TC-xxx]
- AC-2.1: [Description] → Test Cases: [TC-xxx, TC-yyy, TC-zzz]

### Category 2: [Name]
Maps to AC:
[Repeat pattern]

---

## Category Interactions

**Tests spanning multiple categories:**
Some test cases may test interactions between categories:

- TC-xxx: Tests [Category 1] and [Category 2] interaction
  - Primary Category: [Category 1]
  - Secondary Aspect: [Category 2]
  - Reason: [Why both categories are tested in one case]

---

## Special Categories

### Regression Prevention Category
**Purpose:** Prevent recurrence of known bugs

**Related Issues:**
- [INCIDENT-001]: Previously fixed production defect
  - Test: TC-REG-001
  - Verification: [How test prevents regression]

### Custom Categories (if applicable)
**[Custom Category Name]:** [Description and rationale]

---

## Category Completeness Checklist

- [ ] Each category has clear definition
- [ ] Each category has explicit scope
- [ ] Each category has rationale for ticket
- [ ] All test cases assigned to exactly one primary category
- [ ] All categories represented in test plan
- [ ] No category is empty
- [ ] Category distribution is reasonable
- [ ] All AC are mapped to categories
- [ ] Distribution matches ticket complexity
```

---

## Section 2 Composition Rules

### Required Elements
- [ ] Overview with category count
- [ ] Definition for each category (1-2 sentences)
- [ ] Scope statement for each category (included/excluded)
- [ ] Rationale for each category
- [ ] List of test cases per category
- [ ] Distribution table with percentages
- [ ] AC mapping to categories
- [ ] Count of test cases per category

### Optional Elements
- [ ] Category interaction notes
- [ ] Custom category descriptions
- [ ] Regression prevention details
- [ ] Category prioritization

### Do Not Include
- Detailed test sequences (save for Section 4)
- Environment setup details (save for Section 3)
- Expected results (save for Section 4)

---

## Quality Checklist

- [ ] All categories have clear, non-overlapping definitions
- [ ] Each category is justified for this ticket
- [ ] All test cases are assigned to categories
- [ ] No test cases are unassigned
- [ ] Distribution is logical and balanced
- [ ] AC-to-category mapping is complete
- [ ] All AC are covered by at least one category
- [ ] Category names are consistent with project terminology
- [ ] Rationale for each category is clear
