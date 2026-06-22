# JIRA Fetch Policy

- Use curl -u "$JIRA_EMAIL:$JIRA_TOKEN".
- Never pipe credentials through runtime base64 encoding.
- Never invoke pwsh or powershell to fetch ticket data.
- Fetch must prioritize completeness for Stage 1/2 gates before Stage 3 exploration.
- Static image attachments (`png`, `jpg`, `jpeg`, `webp`, `gif`) are supported only after downloading the attachment locally for in-session inspection.
- Video attachments (`mp4`, `mov`, `avi`, `mkv`, `webm`) are not supported for in-session inspection; treat them as explicit limitations.

Command template:

curl -s -u -k "$JIRA_EMAIL:$JIRA_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_URL/rest/api/2/issue/TICKET-ID"

Attachment handling:
- Enumerate attachment metadata from the issue payload first.
- For supported static image attachments, download the file with curl using the attachment content URL before visual inspection.
- If a supported image download fails or the file cannot be inspected in-session, record an `Attachment Limitations` entry and stop for DEV confirmation.
- Do not claim to inspect video content in-session.

Required environment variables:
- JIRA_TOKEN
- JIRA_EMAIL
- JIRA_URL
