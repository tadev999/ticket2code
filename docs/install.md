# Install Guide

## Prerequisites

- Python 3 available in PATH.
- Target repository path available locally.
- GitHub Copilot chat enabled in target repository.

## Install

Run from this repository root:

```bash
python3 ./installers/t2c_installer.py install --target-dir /absolute/path/to/target-repo
```

## One-line install from any machine

Recommended (safe temp directory):

macOS / Linux (bash):

```bash
TMP_DIR="$(mktemp -d)" && \
git clone --depth 1 https://github.com/tadev999/ticket2code.git "$TMP_DIR" && \
python3 "$TMP_DIR"/installers/t2c_installer.py install --target-dir . && \
rm -rf "$TMP_DIR"
```

Windows (PowerShell):

```powershell
$tmp = Join-Path $env:TEMP ("ticket2code-" + [guid]::NewGuid().ToString()); `
git clone --depth 1 https://github.com/tadev999/ticket2code.git $tmp; `
python (Join-Path $tmp 'installers/t2c_installer.py') install --target-dir (Get-Location).Path; `
Remove-Item -Recurse -Force $tmp
```

## What gets installed

- `.github/prompts/` — Entry point prompts for slash commands
- `.github/skills/` — Shared skill implementations (jira-pbi-analysis, figma-design-analysis, ac-decomposition, dead-code-cleanup, git-diff-analysis, test-environment-designer, design-image-ocr-analysis)
- `.github/hooks/` — Pre-tool safety guards
- `ticket2code/code/` — Ticket-to-code workflow specifications
- `ticket2code/review/` — Code review workflow specifications
- `ticket2code/integration-tests/` — Integration test workflow specifications
- `ticket2code/screen-transition-tests/` — Screen transition test workflow specifications
- `ticket2code/SETUP.md` — Setup guide for project configuration
- `ticket2code.config.yaml` (if missing) — Project configuration template
- `.env.local.example` (if `.env.local` missing) — Environment variables template
- output folders: `docs/report/`, `docs/test/integration/`, `docs/test/screen-transition/`

## Post-install

1. Edit `ticket2code.config.yaml` in target repository.
2. Create `.env.local` in target repository.
3. Run doctor check:

```bash
python3 ./installers/t2c_installer.py doctor --target-dir /absolute/path/to/target-repo
```

## Notes

- Install is additive and may overwrite runtime assets in target `.github/`.
- Keep project-specific settings in target `ticket2code.config.yaml`.
- If `python3` is unavailable on Windows, use `python`.
