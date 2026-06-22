# Section 1 — Commit Metadata and Diff Summary

## Purpose

Establish context: which commit is being reviewed, when, and what changed.

## Required fields

**Before commit (base) hash (long):** 40-character SHA-1 (the commit provided by DEV)  
**Before commit (base) hash (short):** 7-12 character short form  
**Before commit author & date:** From git log  
**After commit (HEAD) hash (long):** 40-character SHA-1 (resolved from current `HEAD`)  
**After commit (HEAD) hash (short):** 7-12 character short form  
**After commit author & date:** From git log  
**Comparison range:** `<before_commit>..HEAD` used for `git diff`  
**Diff statistics:**
- Files changed
- Insertions
- Deletions

## Template

```markdown
# Review for TICKET-ID: {ticket_summary}

## Commit Information

- **Before commit (base) - Hash (long):** {40-char before hash}
- **Before commit (base) - Hash (short):** {7-12 char before hash}
- **Before commit (base) - Author:** {before author name}
- **Before commit (base) - Date:** {before commit date}
- **After commit (HEAD) - Hash (long):** {40-char after hash}
- **After commit (HEAD) - Hash (short):** {7-12 char after hash}
- **After commit (HEAD) - Author:** {after author name}
- **After commit (HEAD) - Date:** {after commit date}
- **Review date:** {today's date}

### Before/After Commit Details

| Stage | Hash (long) | Hash (short) | Author | Email | Date | Subject |
|------|-------------|--------------|--------|-------|------|---------|
| Before code changes (base) | {before hash} | {before short} | {before author} | {before email} | {before date} | {before subject} |
| After code changes (HEAD) | {after hash} | {after short} | {after author} | {after email} | {after date} | {after subject} |

- **Comparison range used for this review:** `{before hash}..{after hash}` (`git diff <before>..HEAD`)

## Diff Summary

| Metric | Count |
|--------|-------|
| Files changed | {count} |
| Insertions (+) | {count} |
| Deletions (-) | {count} |
| Net change | {count} |

### Files affected

| File | Type | Changes |
|------|------|---------|
| {path} | {added/modified/deleted} | +{n} -{n} |
| ... | ... | ... |

### Change classification

- **Features:** {list file names}
- **Tests:** {list file names}
- **Refactor:** {list file names}
- **Cleanup:** {list file names}
- **Docs:** {list file names}
```

## Notes

- If a file is deleted, mark as "deleted" and show only line count.
- If a file is newly added, mark as "added".
- Group files by change type for clarity.
- Do not output only one commit in `Commit Information`; always output both before/base and after/HEAD.
