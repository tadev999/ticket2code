# Compatibility Matrix

## Runtime assumptions

- Copilot customizations are loaded from target repository `.github/`.
- Shell installer scripts use bash.
- PowerShell installer scripts support Windows native setup.
- Hook script uses Python 3.

## Minimum environment

- OS: macOS or Linux
- Shell: bash
- Windows: PowerShell 5.1+ or PowerShell 7+
- Python: 3.8+
- Git: 2.30+

## Project requirements

- Target repository must allow `.github/` customizations.
- Target repository must provide Jira credentials in `.env.local`.
- Target repository should include policy docs referenced by `ticket2code.config.yaml`.

## Non-goals

- No direct dependency on one specific app framework.
- No hardcoded paths to a single repository.
