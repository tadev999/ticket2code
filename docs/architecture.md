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
- `ticket2code.config.yaml` for project-specific paths, rules, and commands.
- output folder placeholders and env example.

4. Operations layer (`installers/`)
- install, upgrade, doctor, uninstall scripts.

## Target project installation model

1. Install copies `core/*` into target `.github/*`.
2. Install initializes `ticket2code.config.yaml` if missing.
3. Team configures policy paths and build/test commands in target config.
4. Runtime execution uses target project context and policies.

## Design principles

- Keep runtime discoverable in target project `.github/`.
- Keep workflow definitions reusable and repository-agnostic.
- Keep project-specific values in one adapter config file.
- Keep upgrade path simple and deterministic.
