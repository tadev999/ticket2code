# Compatibility Matrix

## Runtime assumptions

- Copilot customizations are loaded from target repository `.github/`.
- A single installer CLI is used: `bin/t2c.js` (npm package `ticket2code`, command `t2c`).
- Installer commands are executed with Node.js on macOS, Windows, and Linux.
- Hook script uses Python 3.

## Minimum environment

- OS: macOS, Windows, or Linux
- Node.js: 16.7+
- Python: 3.8+ (skill runtime and hooks)
- Git: 2.30+

## Project requirements

- Target repository must allow `.github/` customizations.
- Target repository must provide Jira credentials in `.env.local`.
- Target repository should include policy docs referenced by `.t2c/config.yaml`.

## Non-goals

- No direct dependency on one specific app framework.
- No hardcoded paths to a single repository.
