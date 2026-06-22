# Agent Stages — Screen Transition Test Cases Generation

## Stages

### Stage 0 — Select communication language (mandatory)
- Ask DEV to select the language for this run before any other stage.
- Recommended options: Vietnamese, English, Japanese, or explicit custom language input.
- Record selection as `Selected communication language` and reuse it for AI-DEV interactions and test report narrative.
- This selection does not control implementation language, framework, or code syntax.

Gate rule:
- If language is not explicitly selected, stop and ask again.

### Stage 0.5 — Select execution phase (mandatory)
- Ask DEV to select the execution phase for this run: `Pre-Dev` or `Post-Dev`.
- Record selection as `Selected execution phase` and reuse it for all gates and output labels.

Phase definitions:
- `Pre-Dev`: Requirement-first planning mode for tickets without implementation yet.
- `Post-Dev`: Implementation-aware validation mode for tickets with available code.

Gate rule:
- If execution phase is not explicitly selected, stop and ask again.

### Stage 1 — Fetch ticket
- Load .env.local to resolve JIRA_TOKEN, JIRA_EMAIL, JIRA_URL.
- Fetch ticket data from JIRA REST API.
- Verify ticket access and data availability.

### Stage 2 — Parse ticket content
Extract and structure:
- Summary, description, type, priority, status
- Acceptance criteria (all conditions, including conditional branches)
- Labels, components, linked tickets
- Affected modules and services
- Attachment evidence and limitations relevant to UI flows and transitions

Completeness requirements (mandatory before Stage 3):
- Parse all acceptance criteria and requirements.
- Identify all affected components, services, and data models.
- Extract business logic and expected behaviors.
- Normalize conditional AC into explicit branches.
- Record any ambiguous or unclear requirements as gaps.
- Review supported static image attachments after local download and inspection when they affect UI/transition requirements.
- Record unsupported video attachments and unreadable attachments as explicit limitations.

Failure handling:
- If completeness cannot be guaranteed, stop and request DEV clarification.

### Stage 3 — Analyze test requirements
- Map each AC to testable conditions.
- Identify all involved screens and navigation entry points.
- Build transition edges in the form: `From Screen -> Action -> To Screen`.
- Identify required environment setup (services, data, configs).
- Determine test dependencies and execution order.
- Consult the repository's testing standards and guidance documents.

### Stage 4 — Generate analysis report
Build Stage 3 analysis with:
- Ticket header and summary
- Selected execution phase (`Pre-Dev` or `Post-Dev`)
- Affected screens, components, and services
- Requirements analysis
- Transition map draft (main flow + alternate/error branches)
- Test scope and dependencies
- Proposed transition categories and environment setup
- Confirmation options for DEV review

Phase-specific output rules:
- `Pre-Dev`: Mark report mode as draft planning artifact and include assumptions, unknowns, and re-validation checklist.
- `Post-Dev`: Mark report mode as implementation-aware validation artifact and include evidence references when available.

Save to: docs/test/screen-transition/<TICKET-ID>_screen_transition_tests_<predev|postdev>_<YYYYMMDDHHmm>.md

Attachment limitation rule:
- If any relevant attachment could not be downloaded, parsed, or inspected, the analysis report must include an `Attachment Limitations` subsection with file, reason, and confidence impact.

### Stage 4.5 — Request DEV confirmation (mandatory)
- Present Stage 4 analysis report and ask DEV to choose exactly one option:
	- Confirm and generate test cases
	- Revise analysis
	- Cancel

Attachment fallback gate:
- If the report contains `Attachment Limitations`, do not proceed silently.
- Present the limitation and require explicit DEV choice to continue despite limitation, revise with manual attachment summary, or cancel.

Gate rule:
- Only `Confirm and generate test cases` can proceed to Stage 5.
- `Revise analysis` must return to Stage 4 and re-present report.
- `Cancel` must terminate the run.
- If DEV does not explicitly choose an option, stop and ask again.

### Stage 5 — Categorize transition scenarios
- Define non-overlapping test categories.
- Common categories: Critical Path, Alternate Path, Error Recovery Path, Back Navigation Path, Entry/Deep-link Path.
- Map each AC to one or more transition scenarios.
- Ensure exhaustive coverage (all transition scenarios belong to a category).

### Stage 6 — Design environment setup
- Determine all preconditions needed for tests.
- Define server configuration (if applicable).
- Specify test data requirements and initialization.
- Document external service mocks or stubs needed.
- Include database state setup.
- Define teardown/cleanup procedures.

Environment setup must include:
- **Pre-conditions**: Current state before test starts
- **Configuration**: System settings, environment variables
- **Test Data**: Initial data state and data generation
- **Dependencies**: External services, mock servers
- **Teardown**: Cleanup after test completion

### Stage 7 — Generate test sequences
For each test case:
- Assign to single category
- Define test name following naming convention
- List pre-conditions
- Create step-by-step sequence (numbered steps)
- Define screen transition for each step (`From Screen`, `Action`, `To Screen`)
- Document expected result for each step
- Include post-conditions and cleanup

Each step must include:
- Clear action/trigger
- Expected destination screen and state change
- Verification method

### Stage 8 — Define expected results
For every test sequence:
- Specify measurable outcomes
- Define success criteria
- List verifiable assertions
- Include error/edge case handling
- Document recovery procedures

Expected results must be:
- **Measurable**: Specific values, states, or behaviors
- **Verifiable**: Can be checked programmatically or manually
- **Complete**: Cover all aspects of the test scenario

### Stage 9 — Validate coverage
- Map every atomic AC to test cases.
- Map every atomic AC to concrete verifying step numbers.
- Verify each AC is tested by at least one case.
- Identify gaps in coverage.
- Ensure environment setup supports all tests.
- Generate coverage matrix.

Coverage validation must confirm:
- 100% of atomic AC are covered
- No orphaned test cases
- All categories are represented
- Test sequences are executable
- AC-to-step traceability is explicit

Phase-specific validation rule:
- `Pre-Dev`: Coverage is requirement-level planning coverage and must include explicit re-validation-required notes.
- `Post-Dev`: Coverage is implementation-aware validation coverage and should include evidence references where available.
