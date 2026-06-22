# Ticket2Code Setup

This document is installed to `ticket2code/SETUP.md` in your target repository.

## 1) Create `.env.local`

At repository root, create `.env.local` with:

```env
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your Jira base URL>
```

Notes:
- `JIRA_URL` example: `https://your-company.atlassian.net`
- Use an Atlassian API token with permission to read your project issues.

## 2) Configure project settings

Open `ticket2code.config.yaml` and update values for your repository and workflow conventions.

## 3) Run doctor check

From this framework repository:

```bash
./installers/doctor.sh /absolute/path/to/target-repo
```

PowerShell:

```powershell
./installers/doctor.ps1 -TargetDir <target-repo-path>
```

## 4) Use slash commands

Examples:
- `/t2c_code PROJ-1234`
- `/t2c_review PROJ-1234`
- `/t2c_integration_tests PROJ-1234`
- `/t2c_screen_transition_tests PROJ-1234`

## Troubleshooting

If a command reports missing files under `ticket2code/...`, rerun install or upgrade to refresh runtime assets.
