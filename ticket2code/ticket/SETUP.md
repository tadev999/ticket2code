# Setup Guide

Get `/ticket` running in your repository in under 5 minutes.

---

## Step 1 — Add files to your repository

Copy the following into your repo:

```
.github/
└── prompts/
    └── ticket.prompt.md       ← copy from ticket2code/ticket/ticket.prompt.md

ticket2code/
└── ticket/
    ├── ticket.prompt.md
    ├── ticket-agent.md
    ├── ticket-processor.prompt.md
    ├── env.local.example
    ├── INDEX.md
    ├── SETUP.md

    # Required spec folders
    ├── agent-specs/
    │   ├── 01-stages.md
    │   ├── 02-ac-decomposition.md
    │   ├── 03-evaluation-rules.md
    │   ├── 04-project-rules.md
    │   └── 05-jira-policy.md
    └── processor-specs/
        ├── 01-language-and-convention.md
        ├── 02-section-1-analysis.md
        ├── 03-section-2-evaluation.md
        ├── 04-section-3-conclusion.md
        ├── 05-cleanup-checklist.md
        ├── 06-decision-gates.md
        ├── 07-validation-checklist.md
        └── 08-decision-labels.md
```

---

## Step 2 — Create `.env.local`

At the **repo root**, create `.env.local` (copy from `ticket2code/ticket/env.local.example`):

```dotenv
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your JIRA base URL>
```

> **Example `JIRA_URL`:** `https://yourcompany.atlassian.net`

---

## Step 3 — Get your Atlassian API token

1. Sign in to your Atlassian account at [id.atlassian.com](https://id.atlassian.com).
2. Go to **Security → API tokens**: https://id.atlassian.com/manage-profile/security/api-tokens
3. Click **Create API token**, give it a name (e.g., `ticket-command-local`), and click **Create**.
4. Copy the token immediately — it is only shown once.
5. Paste it as the value of `JIRA_TOKEN` in `.env.local`.

> If you suspect a token has been compromised, revoke it from the same page and create a new one.

---

## Step 4 — Verify directory structure

```
your-repo/
├── .env.local                        ← credentials (never commit this)
├── .github/
│   └── prompts/
│       └── ticket.prompt.md
└── ticket2code/
    └── ticket/
        ├── ticket.prompt.md
        ├── ticket-agent.md
        ├── ticket-processor.prompt.md
        ├── env.local.example
        ├── INDEX.md
        ├── SETUP.md
        ├── agent-specs/
        └── processor-specs/
```

---

## Step 5 — Add project rules (required for best results)

The agent reads rule documents from your `docs/` folder to enforce project-specific conventions.  
Create these files if they don't exist:

| File | Purpose |
|---|---|
| `docs/coding_style.md` | Naming conventions, formatting rules |
| `docs/codeReviewGuideline.md` | Code review criteria |
| `docs/logging/logging_policy.md` | Logging and error handling rules |
| `docs/test/test_code_rules.md` | Test naming, coverage requirements |
| `docs/development_policy.md` | Branching, delivery, prioritization rules |
| `docs/review_patterns/` | Generalized review checklists from past incidents |
| `docs/release_bugs/` | Known release bug history |

The more complete your `docs/` folder, the more accurate the generated code.

---

## Step 6 — Create the report output directory

```bash
mkdir -p docs/report
```

Report files are saved here as `docs/report/<TICKET-ID>_reports_<YYYYMMDDHHmm>.md`.

---

## Step 7 — Add `.env.local` to `.gitignore`

```bash
echo ".env.local" >> .gitignore
```

---

## Run

Open GitHub Copilot Chat and type:

```
/ticket PROJ-1234
```

Replace `PROJ-1234` with your actual JIRA ticket ID.

## Workflow behavior (important)

- The flow has Stage 1 -> Stage 12 (see `agent-specs/01-stages.md`).
- Stage 10.5 and Stage 12 are explicit decision gates.
- If no explicit choice is captured, the workflow must stop and must not assume Yes/No.
- Test/build commands are allowed only after Stage 10.5 explicit Yes.

## When a run is interrupted

- If you see request errors (for example HTTP 400 invalid_request_body), start a new chat and resume from the latest completed stage.
- Keep resume context concise (ticket ID, report path, completed stage, pending gate) to reduce payload risk.

---

## Security reminders

- Never commit `.env.local`.
- Never share `JIRA_TOKEN` via chat, email, or code comments.
- The agent uses `curl -u` for JIRA requests — your token is never base64-encoded at runtime in a way that triggers security alerts.
