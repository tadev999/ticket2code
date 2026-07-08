# Install Guide

## Prerequisites

- Node.js >= 16.7 in PATH (for the `t2c` CLI).
- Python 3 in PATH (for skill runtime: OCR, Figma, hooks).
- Target repository path available locally.
- GitHub Copilot chat enabled in target repository.

## Install

Install the CLI once, then run it inside the target repository:

```bash
npm i -g ticket2code
cd /absolute/path/to/target-repo
t2c init
```

Prefer not to install globally? Use `npx`:

```bash
npx ticket2code init
```

## What gets installed

Ticket2Code uses a hybrid install model with 2 layers.

In target project repository (minimal):

- `.github/prompts/t2c_*.prompt.md` — Lightweight Copilot slash-command entrypoints
- `.t2c/config.yaml` — Project-level t2c configuration
- `.t2c/lock.json` — Pinned runtime/assets version metadata
- `.t2c/state/` — Small local state and metadata cache
- `.env.local.example` (if `.env.local` missing) — Environment variables template

Outside target project (user-level runtime):

- macOS runtime by version: `~/Library/Application Support/ticket2code/runtime/<version>/`
- macOS prompts/skills/core assets by version: `~/Library/Application Support/ticket2code/assets/<version>/`
- macOS download cache: `~/Library/Caches/ticket2code/`
- macOS logs: `~/Library/Logs/ticket2code/`
- Windows runtime by version: `%LOCALAPPDATA%\ticket2code\runtime\<version>\`
- Windows prompts/skills/core assets by version: `%LOCALAPPDATA%\ticket2code\assets\<version>\`
- Windows download cache: `%LOCALAPPDATA%\ticket2code\cache\`
- Windows logs: `%LOCALAPPDATA%\ticket2code\logs\`

## Post-install

1. Edit `.t2c/config.yaml` in target repository.
2. Create `.env.local` in target repository.
3. Run doctor check:

```bash
t2c doctor --target-dir /absolute/path/to/target-repo
```

## Notes

- Install writes lightweight `.github/prompts/t2c_*.prompt.md` entrypoints and a small project-local `.t2c/` directory.
- Runtime assets remain in user-level directories.
- Keep project-specific settings in target `.t2c/config.yaml`.
- Python 3 is required at skill runtime even though the CLI is Node-based.
