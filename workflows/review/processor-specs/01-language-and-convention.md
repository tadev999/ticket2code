# Language and Convention — Review Reports

## Report language

- Language must come from explicit Stage 0 selection (`Selected communication language`).
- Do not infer review language from ticket content or the latest user message.
- Use the same `Selected communication language` for AI-DEV conversation and review report narrative.
- Communication language selection does not control implementation language, framework, or code syntax.
- Use professional, neutral tone.
- Avoid casual language; maintain formality suitable for code review.

## File naming

Review reports are saved as:
```
docs/report/<TICKET-ID>_reviews_<YYYYMMDDHHmm>.md
```

Format:
- TICKET-ID: exact ticket identifier (e.g., `PROJ-1234`)
- YYYYMMDDHHmm: current date-time when report is created (e.g., `202606181430`)

Example: `docs/report/PROJ-1234_reviews_202606181430.md`

## Document structure

All review reports must follow this section order:
1. Section 1 — Commit metadata and diff summary
2. Section 2 — AC evaluation matrix
3. Section 3 — Code quality assessment
4. Section 4 — Conclusion and recommendations

## Frontmatter

All reports start with YAML frontmatter:
```yaml
---
ticket: PROJ-1234
commit_hash: 9f6d309fdf40c50f0439aee9984e03b6563056ed
commit_short: 9f6d309f
diff_date: 2026-06-18T14:30:00Z
review_date: 2026-06-18T14:35:00Z
---
```

## Markdown conventions

- Use `#` for section headers (never use underlines).
- Use `**bold**` for emphasis, `_italic_` for code references.
- Use `` ` `` for inline code, ` ```lang ``` ` for code blocks.
- Use `|` for tables with proper alignment.
- Use `- ` for bullet lists, `1. ` for numbered lists.

## Terminology

- **AC** = Acceptance Criteria (from ticket)
- **Atomic AC** = Decomposed, testable unit of AC
- **Diff** = Output of `git diff <commit>..HEAD`
- **Hunk** = Group of related changes in diff
- **Status** = Met | Partially Met | Not Met | Unclear
