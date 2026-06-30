# Compatibility Matrix

## Runtime assumptions

- Copilot customizations are loaded from target repository `.github/`.
- A single installer CLI is used: `installers/t2c_installer.py`.
- Installer commands are executed with Python 3 on both macOS and Windows.
- Hook script uses Python 3.

## Minimum environment

- OS: macOS or Windows
- Shell: any shell that can run Python commands
- Python: 3.8+
- Git: 2.30+

## Project requirements

- Target repository must allow `.github/` customizations.
- Target repository must provide Jira credentials in `.env.local`.
- Target repository should include policy docs referenced by `ticket2code.config.yaml`.

## Non-goals

- No direct dependency on one specific app framework.
- No hardcoded paths to a single repository.
