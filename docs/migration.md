# Migration Guide

## From repository-local ticket2code to ticket2code-core

1. Keep existing business documents and policy docs in target repository.
2. Install thin project metadata into target `.t2c/`.
3. Use user-level runtime/assets storage with version pinning from `.t2c/lock.json`.
4. Move project-specific path rules into `.t2c/config.yaml`.
5. Keep command outputs in target repository `docs/` directories.

## From older t2c naming

If your repository uses older folder names, map to current commands:

- `createIntegrationTestCases` -> `t2c_integration_tests`
- `createScreenTransitionTestCases` -> `t2c_screen_transition_tests`

## Checklist

- Slash commands visible in chat
- Agents discoverable
- `.t2c/config.yaml` present and valid
- `.t2c/lock.json` present and valid
- Jira env configured in target repository
