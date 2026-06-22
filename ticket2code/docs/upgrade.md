# Upgrade Guide

## Upgrade runtime assets in a target project

```bash
./installers/upgrade.sh /absolute/path/to/target-repo
```

## Upgrade behavior

- Replaces target `.github/prompts/*`
- Replaces target `.github/agents/*`
- Replaces target `.github/skills/*`
- Replaces target `.github/hooks/*`
- Does not replace target `ticket2code.config.yaml`

## Recommended flow

1. Backup or commit target repository before upgrade.
2. Run upgrade script.
3. Run doctor check.
4. Validate one command end-to-end in target project.

## Validation command

```bash
./installers/doctor.sh /absolute/path/to/target-repo
```
