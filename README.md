# ticket2code — `/ticket` command

> Turn a JIRA ticket into analysis report + production-ready code, with a mandatory human confirmation gate before any file is touched.

---

## Install in one command

**macOS / Linux / Git Bash**
```bash
git clone --depth 1 https://github.com/tadev999/ticket2code.git /tmp/ticket2code && /tmp/ticket2code/bin/setup.sh . && rm -rf /tmp/ticket2code
```

**Windows (PowerShell)**
```powershell
git clone --depth 1 https://github.com/tadev999/ticket2code.git $env:TEMP\ticket2code; powershell -ExecutionPolicy Bypass -File "$env:TEMP\ticket2code\bin\setup.ps1" .; Remove-Item -Recurse -Force $env:TEMP\ticket2code
```

Then configure credentials in `.env.local` — see [Step 2](#2-create-envlocal) below.

---

## Quick start (manual)

### 1. Add files to your repository

Copy `ticket.prompt.md` to `.github/prompts/` and copy the `ticket2code/` folder to your repo root.

### 2. Create `.env.local`

At the repo root, create `.env.local`:

```dotenv
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your JIRA base URL>
```

See [SETUP.md](SETUP.md) for step-by-step credential instructions.

### 3. Run

Open GitHub Copilot Chat and type:

```
/ticket PROJ-1234
```

---

## How it works

```mermaid
flowchart TD
    A[/ticket PROJ-1234] --> B[Fetch & Parse ticket]
    B --> C[Explore codebase]
    C --> D[Generate analysis report]
    D --> E[Save report to docs/report/]
    E --> F{DEV confirmation}
    F -->|Yes| G[Generate code]
    F -->|Adjust / Add files| D
    F -->|Cancel| Z[Stop]
    G --> H[Decompose ACs + Evaluate code]
    H --> I[Append evaluation to report]
    I --> J[Validate against project rules]
    J --> K[Output commit summary]
```

**The gate rule:** The agent never writes code without explicit DEV confirmation.

---

## What you get per ticket

| Artifact | When | Location |
|---|---|---|
| Pre-generate analysis report | After DEV confirms | `docs/report/<TICKET-ID>_reports_<YYYYMMDDHHmm>.md` |
| Generated code | After confirmation | Files listed in the analysis |
| Post-generate AC evaluation | After code generation | Appended to the same report file |
| Coverage summary | After evaluation | Section 2.2 of the report |
| Commit message | End of workflow | Printed in chat |

---

## File layout

```
ticket2code/ticket/
├── README.md                   ← You are here
├── INDEX.md                    ← Architecture, stages, troubleshooting
├── SETUP.md                    ← Credential setup guide
├── env.local.example           ← .env.local template
├── ticket.prompt.md            ← Slash-command entry point
├── ticket-agent.md             ← Stage-by-stage behavior + AC decomposition rules
└── ticket-processor.prompt.md  ← Report schema and output templates
```

---

## Requirements

- GitHub Copilot with agent mode enabled
- JIRA account with API token access
- Repository `docs/` folder with project rules (coding style, logging, test rules, review guidelines)
  — see [SETUP.md § Project rules](SETUP.md) for details

---

## Security

- Never commit `.env.local`. Add it to `.gitignore`.
- Never share `JIRA_TOKEN` via chat or email.
- If a token is compromised, revoke it immediately at [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens).
