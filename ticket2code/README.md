# ticket2code-core

Reusable ticket-to-code framework for multi-project setup.

## Structure
- `core/`: runtime assets (prompts, agents, skills, hooks)
- `workflows/`: workflow definitions and processor workflow definitions
- `templates/`: project bootstrap templates
- `installers/`: install/upgrade/doctor scripts

## Version
- Current version: see `VERSION`
- Change history: see `CHANGELOG.md`

## Quick Start
1. Install into a target repository:
	- `./installers/install.sh /absolute/path/to/target-repo`
	- `./installers/install.ps1 -TargetDir <target-repo-path>`
2. Edit `ticket2code.config.yaml` in target repository.
3. Create `.env.local` in target repository from `.env.local.example`.
4. Run doctor check:
	- `./installers/doctor.sh /absolute/path/to/target-repo`
	- `./installers/doctor.ps1 -TargetDir <target-repo-path>`

## One-line Install (Any Machine)

Recommended (safe temp directory):

```bash
TMP_DIR="$(mktemp -d)" && \
git clone --depth 1 https://github.com/tadev999/ticket2code.git "$TMP_DIR" && \
"$TMP_DIR"/installers/install.sh . && \
rm -rf "$TMP_DIR"
```

Fixed `/tmp` variant:

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

## Upgrade
- `./installers/upgrade.sh /absolute/path/to/target-repo`

## Uninstall
- `./installers/uninstall.sh /absolute/path/to/target-repo`

## Documentation
- `docs/architecture.md`
- `docs/install.md`
- `docs/upgrade.md`
- `docs/migration.md`
- `docs/compatibility-matrix.md`
