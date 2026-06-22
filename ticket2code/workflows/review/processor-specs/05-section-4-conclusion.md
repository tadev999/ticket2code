# Section 4 — Conclusion and Recommendations

## Purpose

Provide overall verdict on code review and actionable next steps.

## Overall compliance status

Exactly one of:
- **✓ PASS** — All AC are Met and no critical/high issues.
- **⚠ CONDITIONAL PASS** — AC coverage is good but some warnings/improvements recommended.
- **✗ FAIL** — AC coverage is incomplete or critical issues found; must revise before merge.

## Template

```markdown
## Review Conclusion

### Overall Status: {PASS | CONDITIONAL PASS | FAIL}

**AC Coverage Summary:**
- Met: {n} items
- Partially Met: {n} items
- Not Met: {n} items
- Unclear: {n} items

**Code Quality Summary:**
- Critical issues: {n}
- High issues: {n}
- Medium issues: {n}
- Warnings: {n}

### Verdict

{1-2 sentence summary of review outcome}

## Recommendations

### Must address before merge
1. {specific issue and remediation}
2. {specific issue and remediation}

### Strongly recommended
1. {improvement suggestion}
2. {improvement suggestion}

### Optional (nice to have)
1. {enhancement suggestion}
2. {enhancement suggestion}

## Next steps

- [ ] Address critical and high-severity issues
- [ ] Add missing unit tests
- [ ] Update documentation if needed
- [ ] Re-request review after changes
```

## Verdict logic

- **PASS:** All AC status ≥ "Partially Met", zero critical/high issues.
- **CONDITIONAL PASS:** Most AC implemented, low-medium severity issues, no blockers.
- **FAIL:** AC coverage incomplete (≥1 "Not Met"), or critical/high issues present.

## Recommendations format

- **Must address:** Issues blocking merge.
- **Strongly recommended:** Best-practice improvements.
- **Optional:** Enhancement opportunities for future PRs.

Each recommendation should be actionable and specific (include file names and line numbers where applicable).
