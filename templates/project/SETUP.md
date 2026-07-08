# Ticket2Code Setup

This document is available in user-level Ticket2Code assets for your installed version.

## 1) Create `.env.local`

At repository root, create `.env.local` with:

```env
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your Jira base URL>

# Optional: only if you are behind a corporate proxy that requires user/pass.
# URL-encode special characters in USER/PASS (@ -> %40, : -> %3A, / -> %2F).
#HTTPS_PROXY="http://USER:PASS@proxy.host:PORT"
#HTTP_PROXY="http://USER:PASS@proxy.host:PORT"
#NO_PROXY="localhost,127.0.0.1,.company.local"
```

Notes:
- `JIRA_URL` example: `https://your-company.atlassian.net`
- Use an Atlassian API token with permission to read your project issues.
- Any skill that performs network or install steps (`curl`, `pip install`, Python API fetch)
  loads `.env.local` first, so uncommenting the proxy lines is enough — no per-command flags needed.
- Network preflight (skills run this automatically before any network/install step):
  ```bash
  [ -f .env.local ] && set -a && . ./.env.local && set +a
  ```

## 2) Configure project settings

Open `.t2c/config.yaml` and update values for your repository and workflow conventions.

## 3) Run doctor check

From the target repository:

```bash
t2c doctor --target-dir /absolute/path/to/target-repo
```

## 4) Use slash commands

Examples:
- `/t2c_code PROJ-1234`
- `/t2c_review PROJ-1234`
- `/t2c_integration_tests PROJ-1234`
- `/t2c_screen_transition_tests PROJ-1234`

## Troubleshooting

If a command reports missing files under `.t2c/...` or your user-level runtime/assets path, rerun install or upgrade to refresh runtime assets.
