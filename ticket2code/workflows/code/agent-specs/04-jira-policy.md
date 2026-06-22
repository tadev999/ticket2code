# JIRA Fetch Policy

- Use curl -u "$JIRA_EMAIL:$JIRA_TOKEN".
- Never pipe credentials through runtime base64 encoding.
- Never invoke pwsh or powershell to fetch ticket data.
- Fetch must prioritize completeness for Stage 1/2 gates before Stage 3 exploration.

Command template:

curl -s -u -k "$JIRA_EMAIL:$JIRA_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_URL/rest/api/2/issue/TICKET-ID"

Required environment variables:
- JIRA_TOKEN
- JIRA_EMAIL
- JIRA_URL
