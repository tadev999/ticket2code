# JIRA Fetch Policy

- Use curl -u "$JIRA_EMAIL:$JIRA_TOKEN".
- Never pipe credentials through runtime base64 encoding.
- Never invoke non-curl wrapper commands to fetch ticket data.
- Fetch must prioritize completeness for Stage 1/2 gates before Stage 3 exploration.
- Static image attachments (`png`, `jpg`, `jpeg`, `webp`, `gif`) are supported only after downloading the attachment locally for in-session inspection.
- Video attachments (`mp4`, `mov`, `avi`, `mkv`, `webm`) are not supported for in-session inspection; treat them as explicit limitations.

Command template:

curl -s -u -k "$JIRA_EMAIL:$JIRA_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_URL/rest/api/2/issue/TICKET-ID"

Attachment handling:
- Enumerate attachment metadata from the issue payload first (`.fields.attachment[]`: `filename`, `mimeType`, `content`).
- Run the network preflight once before the download loop so proxy/CA settings apply to every attachment (prevents `407` on per-file downloads):
  `[ -f .env.local ] && set -a && . ./.env.local && set +a`
- For supported static image attachments, download each `content` URL into the canonical screenshot folder read by the image-analysis skill (not an ad-hoc temp folder):
  ```bash
  DEST="docs/figma_design_analysis/TICKET-ID_screenshots"; mkdir -p "$DEST"
  echo "$TICKET_JSON" | jq -r '.fields.attachment[] | select(.mimeType | startswith("image/")) | [.content, .filename] | @tsv' \
    | while IFS=$'\t' read -r url filename; do
        curl -s -L -u "$JIRA_EMAIL:$JIRA_TOKEN" -k -o "$DEST/$filename" "$url" || echo "[Attachment Limitations] $filename";
      done
  ```
- Hand the downloaded folder to `design-image-ocr-analysis` (Mode 1 vision, or `image_analyze.py --input-folder <DEST> --ticket-id TICKET-ID`).
- If a supported image download fails or the file cannot be inspected in-session, record an `Attachment Limitations` entry and stop for DEV confirmation.
- Do not claim to inspect video content in-session.

Required environment variables:
- JIRA_TOKEN
- JIRA_EMAIL
- JIRA_URL
