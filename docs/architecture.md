# Architecture

This repository is a reusable ticket2code core package for multi-project rollout.

## Layers

1. Runtime layer (`core/`)
- `prompts/`: slash entrypoints exposed in Copilot chat.
- `skills/`: reusable domain workflows.
- `hooks/`: deterministic guardrails.

2. Workflow definition layer (`workflows/`)
- Workflow-specific stages, rules, and processor templates.
- Intended as source content for orchestrators and skills.

3. Project adapter layer (`templates/project/`)
- `.t2c/config.yaml` for project-specific paths, rules, and commands.
- output folder placeholders and env example.

4. Operations layer (`bin/`)
- `t2c` npm CLI: init, upgrade, doctor, uninstall.

## Target project installation model

1. Install writes lightweight prompt entrypoints into target `.github/prompts/`.
2. Install writes minimal project-local metadata under `.t2c/`.
3. Install initializes `.t2c/config.yaml` and `.t2c/lock.json` if missing.
4. Runtime and assets are stored at user level and resolved by pinned version.
4. Runtime execution uses target project context and policies.

User-level runtime storage:

- macOS: `~/Library/Application Support/ticket2code/runtime/<version>/`
- macOS assets: `~/Library/Application Support/ticket2code/assets/<version>/`
- Windows: `%LOCALAPPDATA%\\ticket2code\\runtime\\<version>\\`
- Windows assets: `%LOCALAPPDATA%\\ticket2code\\assets\\<version>\\`

## Design principles

- Keep target repository clean with a thin `.t2c/` project footprint.
- Keep only lightweight Copilot prompt entrypoints in target `.github/prompts/`.
- Keep heavy runtime and assets outside the target repository.
- Keep workflow definitions reusable and repository-agnostic.
- Keep project-specific values in one adapter config file.
- Keep upgrade path simple and deterministic.
