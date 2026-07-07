# Section 1 — Pre-generate Analysis Report (Stage 5)

Template:

# Full Report — <TICKET-ID>

## 1. Pre-generate analysis report

### 1.1 Ticket header
----------
TICKET: <ID>
TITLE:  <summary>
STATUS: <status>
----------
Type:            <type>

Priority:        <priority>

Estimated Scope: <small | medium | large>

### 1.2 Affected modules
- <Module name — component role>

### 1.3 APIs involved
- <API name or endpoint>

### 1.4 Files to modify / create
- <path/to/file.ext> (modify | create)

### 1.5 Code fix approach
- Main change:       <what logic/UI/state will be changed>
- Safety guardrails: <how regressions are prevented>
- Test update plan:  <what tests will be added or updated>

### 1.6 Impact flows
1. Flow: <trigger / event>
   Function path: <entry point> -> <business function> -> <dependencies>
   Impact: <UI state / navigation / data / side effects>
   Risk: <low | medium | high>

2. Flow: <trigger / event>
   Function path: <entry point> -> <business function> -> <dependencies>
   Impact: <UI state / navigation / data / side effects>
   Risk: <low | medium | high>

### 1.7 Related patterns and references
- <review pattern or known release bug>

### 1.8 Supplementary information (DEV-provided, optional)
- Source: <none | excel | image | text-file | dev-note | multiple>
- Excel/CSV supplement:
  - <filename + sheet + row/column + requirement or data derived>
- Image supplement:
  - <filename + what was extracted + relevance>
- Text file supplement (.md / .txt):
  - <filename + line/section + requirement or constraint derived>
- DEV note (typed text):
  - <verbatim note + requirement or constraint derived>
- Impact on analysis:
  - <how the supplement updates modules / APIs / files / impact flows / AC in this report>

### 1.9 Confirmation
- [ ] Yes, generate code
- [ ] Adjust analysis
- [ ] Add files
- [ ] Cancel

Rules:
- TICKET/TITLE/STATUS block must be wrapped by ---------- lines.
- Include at least 2 impact flows for non-trivial tickets.
- Every flow includes trigger, function path, impact, risk.
- Place Code fix approach between file list and impact flows.
- If image/spreadsheet attachments are used, include explicit evidence references in 1.8.
