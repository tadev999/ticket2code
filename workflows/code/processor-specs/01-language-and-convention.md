# Language Policy and Report Convention

Language policy:
- Communication language must come from explicit Stage 0 selection (`Selected communication language`).
- Do not infer report language from ticket text or user message language.
- Keep all section headings and report body consistent with `Selected communication language`.
- Use the same `Selected communication language` for agent-DEV conversation in this run.
- Communication language selection does not control implementation language, framework, or code syntax.

Report file convention:
- Path: docs/report/<TICKET-ID>_reports_<YYYYMMDDHHmm>.md
- <TICKET-ID>: JIRA key (example: PROJ-1234)
- <YYYYMMDDHHmm>: timestamp at Stage 5
- One file per ticket: analysis -> code -> evaluation sequence
