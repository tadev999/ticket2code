# Upgrade Guide

## Upgrade runtime assets in a target project

```bash
t2c upgrade --target-dir /absolute/path/to/target-repo
```

## Upgrade behavior

- Keeps target project footprint in `.t2c/`.
- Refreshes lightweight entrypoint prompts in target `.github/prompts/`.
- Refreshes pinned runtime/assets version referenced by `.t2c/lock.json`.
- Preserves project-specific settings in `.t2c/config.yaml`.
- Updates user-level runtime/assets directories per OS.

## Recommended flow

1. Backup or commit target repository before upgrade.
2. Run upgrade script.
3. Run doctor check.
4. Validate one command end-to-end in target project.

## Validation command

```bash
t2c doctor --target-dir /absolute/path/to/target-repo
```
