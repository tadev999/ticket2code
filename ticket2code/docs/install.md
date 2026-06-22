# Install Guide

## Prerequisites

- Bash shell on developer machine or CI runner.
- Target repository path available locally.
- GitHub Copilot chat enabled in target repository.

## Install

Run from this repository root:

```bash
./installers/install.sh /absolute/path/to/target-repo
```

PowerShell:

```powershell
./installers/install.ps1 -TargetDir <target-repo-path>
```

## One-line install from any machine

Recommended (safe temp directory):

```bash
TMP_DIR="$(mktemp -d)" && \
git clone --depth 1 https://github.com/tadev999/ticket2code.git "$TMP_DIR" && \
"$TMP_DIR"/installers/install.sh . && \
rm -rf "$TMP_DIR"
```

Alternative using a fixed tmp path:

```bash
git clone --depth 1 https://github.com/tadev999/ticket2code.git /tmp/ticket2code && \
/tmp/ticket2code/installers/install.sh . && \
rm -rf /tmp/ticket2code
```

Windows PowerShell one-liner:

```powershell
$tmp = Join-Path $env:TEMP ("ticket2code-" + [guid]::NewGuid().ToString()); `
git clone --depth 1 https://github.com/tadev999/ticket2code.git $tmp; `
& (Join-Path $tmp 'installers/install.ps1') -TargetDir (Get-Location).Path; `
Remove-Item -Recurse -Force $tmp
```

## What gets installed

- `.github/prompts/*`
- `.github/agents/*`
- `.github/skills/*`
- `.github/hooks/*`
- `ticket2code.config.yaml` (if missing)
- `.env.local.example` (if `.env.local` missing)
- output folders under `docs/report` and `docs/test/*`

## Post-install

1. Edit `ticket2code.config.yaml` in target repository.
2. Create `.env.local` in target repository.
3. Run doctor check:

```bash
./installers/doctor.sh /absolute/path/to/target-repo
```

PowerShell:

```powershell
./installers/doctor.ps1 -TargetDir <target-repo-path>
```

## Notes

- Install is additive and may overwrite runtime assets in target `.github/`.
- Keep project-specific settings in target `ticket2code.config.yaml`.
