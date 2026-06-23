# Ticket2Code

A reusable ticket-to-code automation framework designed for seamless multi-project integration. Streamline your development workflow by automatically converting JIRA tickets into actionable code scaffolding and documentation.

## Overview

Ticket2Code bridges the gap between project management and development by providing a structured framework that:
- Automatically generates code structure from JIRA tickets
- Maintains consistent project standards across multiple repositories
- Reduces manual setup time and human error
- Supports both macOS/Linux and Windows environments

## Directory Structure

```
ticket2code/
├── core/                  # Runtime assets (prompts, skills, hooks)
├── workflows/            # Workflow definitions and processors
├── templates/            # Project bootstrap templates
├── installers/           # Installation, upgrade, and diagnostic scripts
├── docs/                 # Documentation and guides
└── CHANGELOG.md          # Version history
```

---

## Quick Start

### Installation (Recommended Method)

The safest approach uses a temporary directory and automatically cleans up after installation.

**macOS / Linux:**
```bash
TMP_DIR="$(mktemp -d)" && \
git clone --depth 1 https://github.com/tadev999/ticket2code.git "$TMP_DIR" && \
"$TMP_DIR"/installers/install.sh . && \
rm -rf "$TMP_DIR"
```

**Windows (PowerShell):**
```powershell
$tmp = Join-Path $env:TEMP ("ticket2code-" + [guid]::NewGuid().ToString()); `
git clone --depth 1 https://github.com/tadev999/ticket2code.git $tmp; `
& (Join-Path $tmp 'installers/install.ps1') -TargetDir (Get-Location).Path; `
Remove-Item -Recurse -Force $tmp
```

---

## Built-in Prompts

Ticket2Code provides specialized slash commands in VS Code to streamline your workflow. All prompts require JIRA configuration in `.env.local`.

### Setup Configuration

Before using any prompt, ensure `.env.local` contains:
```bash
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your JIRA base URL>
```

### Available Prompts

#### `/t2c_code TICKET-ID` — Full Ticket-to-Code Workflow

Comprehensive workflow: requirement analysis → code generation → dead code cleanup → AC evaluation.

**Input:** `/t2c_code PROJ-1234`

**How it works:**
1. Analyzes JIRA ticket with requirement breakdown and attachment inspection
2. Presents analysis report and waits for your confirmation
3. Generates code implementation across necessary files
4. Automatically cleans up dead code and orphaned references (with before/after evidence)
5. Asks whether to run tests/builds now or defer
6. Evaluates generated code against all acceptance criteria
7. Produces final report saved to `docs/report/<TICKET-ID>_reports_<YYYYMMDDHHmm>.md`

**Output:**
- Implementation-ready code changes
- Comprehensive analysis + evaluation report
- Dead code cleanup evidence
- AC coverage checklist

**Confirmation gates:**
- Language selection (controls report narrative)
- Analysis confirmation before code changes
- Test/build execution decision

---

#### `/t2c_review TICKET-ID` — Code Review Against Acceptance Criteria

Automated review of your code changes against ticket requirements and project standards.

**Input:** `/t2c_review PROJ-1234`

**How it works:**
1. Looks for existing ticket report (from `/t2c_code`) or fetches ticket from JIRA
2. Asks you to provide commit hash (the baseline for comparison)
3. Retrieves git diff between your commit and HEAD
4. Analyzes changes against:
   - Decomposed acceptance criteria
   - Coding style guide compliance
   - Potential regressions and edge cases
5. Generates evidence-based review findings

**Output:**
- Professional review report with line-by-line evidence
- Risk/impact assessment
- Separated facts from assumptions
- Actionable feedback

**Confirmation gates:**
- Language selection
- Commit hash validation (long or short format accepted)

---

#### `/t2c_integration_tests TICKET-ID` — Integration Test Case Generation

Generates comprehensive integration test cases covering component interactions and data flow.

**Input:** `/t2c_integration_tests PROJ-1234`

**How it works:**
1. Parses ticket requirements and acceptance criteria
2. Analyzes affected components and dependencies
3. Presents analysis report and waits for your confirmation
4. Generates categorized test cases:
   - Organized by functional areas (UI, business logic, data persistence, API, etc.)
   - With environment setup (pre-conditions, server config, test data)
   - With step-by-step execution sequences
   - With explicit success criteria
5. Produces AC-to-test-case traceability matrix
6. Validates test coverage against all acceptance criteria

**Output:**
- Comprehensive test plan in markdown
- Test categories by functional areas
- Environment setup requirements
- AC coverage matrix

**Confirmation gates:**
- Language selection
- Execution phase: `Pre-Dev` (planning phase) or `Post-Dev` (implementation verification)
- Analysis confirmation before test case generation

---

#### `/t2c_screen_transition_tests TICKET-ID` — UI Screen Flow Test Cases

Specialized test cases focused on screen navigation, transitions, and UI state verification.

**Input:** `/t2c_screen_transition_tests PROJ-1234`

**How it works:**
1. Extracts ticket requirements and acceptance criteria
2. Identifies screen entry/exit points and branch conditions
3. Presents analysis report and waits for your confirmation
4. Builds transition paths and generates test cases showing:
   - **From Screen → To Screen** for each navigation step
   - **Action/Trigger** that causes transition
   - **Expected UI/System state** at destination
   - **Pre-conditions and test data** for reproducibility
5. Creates AC-to-TC-to-Step traceability
6. Validates coverage of all screen transitions

**Output:**
- Screen transition test plan
- Detailed step-by-step flow verification
- Pre-condition and test data documentation
- AC coverage traceability

**Confirmation gates:**
- Language selection
- Execution phase: `Pre-Dev` or `Post-Dev`
- Analysis confirmation before test case generation

---

### Quick Usage Tips

- **Run `/t2c_code` first** to generate implementation, then `/t2c_review` to validate your work
- **Use `/t2c_integration_tests`** in Pre-Dev phase for test planning, Post-Dev to verify implementation
- **Use `/t2c_screen_transition_tests`** for UI-heavy features to ensure navigation correctness
- **Language selection is contextual**: Controls report language and narrative, not code syntax
- **All reports are saved** to project directories for record-keeping and reference

---

## Manual Installation

If you prefer manual setup or encounter issues with automated installation:

### Step-by-Step Setup

1. **Run installer**
   ```bash
   # macOS / Linux:
   ./installers/install.sh /absolute/path/to/target-repo
   
   # Windows (PowerShell):
   ./installers/install.ps1 -TargetDir <target-repo-path>
   ```

2. **Configure the project**
   - Edit `ticket2code.config.yaml` in your target repository
   - Create `.env.local` from `.env.local.example`
   - Add required JIRA credentials

3. **Validate setup**
   ```bash
   # macOS / Linux:
   ./installers/doctor.sh /absolute/path/to/target-repo
   
   # Windows (PowerShell):
   ./installers/doctor.ps1 -TargetDir <target-repo-path>
   ```

### Upgrade

To update Ticket2Code to the latest version:

```bash
# macOS / Linux:
./installers/upgrade.sh /absolute/path/to/target-repo

# Windows (PowerShell):
./installers/upgrade.ps1 -TargetDir <target-repo-path>
```

### Uninstall

To remove Ticket2Code from your repository:

```bash
# Using one-liner (recommended):
TMP_DIR="$(mktemp -d)" && \
git clone --depth 1 https://github.com/tadev999/ticket2code.git "$TMP_DIR" && \
"$TMP_DIR"/installers/uninstall.sh . && \
rm -rf "$TMP_DIR"

# Or manually:
./installers/uninstall.sh /absolute/path/to/target-repo
```

---

## Documentation

Comprehensive guides are available in the `docs/` directory:

- **[Installation Guide](docs/install.md)** — Detailed setup instructions and troubleshooting
- **[Architecture](docs/architecture.md)** — System design and component overview
- **[Upgrade Guide](docs/upgrade.md)** — Version upgrade procedures
- **[Migration Guide](docs/migration.md)** — Data migration between versions
- **[Compatibility Matrix](docs/compatibility-matrix.md)** — Supported platforms and versions

---

## Version Information

- **Current Version:** See `VERSION` file
- **Release History:** See `CHANGELOG.md`
- **Compatibility:** See `docs/compatibility-matrix.md`

---

## Support & Troubleshooting

### Common Issues

**Installation fails on Windows:**
- Ensure PowerShell execution policy allows scripts: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Doctor check reports warnings:**
- Run `doctor` again to see detailed diagnostic output
- Check `.env.local` configuration is complete
- Verify JIRA credentials are correct

**Configuration not being recognized:**
- Ensure `ticket2code.config.yaml` is in the repository root
- Check file formatting and YAML syntax

### Need Help?

Refer to the documentation files in the `docs/` directory or check the installation logs for detailed error information.

---

## Environment Variables

### Required Configuration (.env.local)

Create `.env.local` in your project root with JIRA connection details:

```bash
# JIRA Connection (Required for all prompts)
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your JIRA base URL>
```

Generate JIRA API token: https://id.atlassian.com/manage-profile/security/api-tokens

For detailed setup, see `ticket2code/SETUP.md`.

---

## Recommended Workflow

### Implementation Workflow
Best practice for developing a feature or bug fix:

1. **Start with `/t2c_code TICKET-ID`**
   - Full analysis and code generation in one command
   - Creates comprehensive report with acceptance criteria evaluation
   - Output: Implementation ready, report saved to `docs/report/`

2. **Implement additional requirements** (if needed)
   - Review the generated code scaffold
   - Add business logic and complete implementation
   - Reference the report for detailed requirements

3. **Validate with `/t2c_review TICKET-ID`**
   - Provide your commit hash for analysis
   - Get evidence-based feedback on your changes
   - Verify AC coverage and identify potential issues

4. **Commit to repository**
   - Include ticket ID in commit message
   - Reference report location for team visibility

### Testing Workflow (Pre-Dev Planning)

Generate test cases before implementation:

1. **Create test plan with `/t2c_integration_tests TICKET-ID` (Pre-Dev phase)**
   - Identify all test scenarios and dependencies
   - Plan environment setup and test data
   - Create test documentation

2. **For UI-heavy features, also run `/t2c_screen_transition_tests TICKET-ID` (Pre-Dev phase)**
   - Map out all screen transitions
   - Identify edge cases in navigation flow

3. **Proceed with implementation using `/t2c_code`**

### Testing Workflow (Post-Dev Verification)

Generate test cases to verify implementation:

1. **After implementation, run `/t2c_integration_tests TICKET-ID` (Post-Dev phase)**
   - Stricter validation for complete coverage
   - Verification that implementation meets all scenarios

2. **Validate screen flows with `/t2c_screen_transition_tests TICKET-ID` (Post-Dev phase)**
   - Ensure UI transitions work as designed
   - Verify all edge cases handled

3. **Final review with `/t2c_review TICKET-ID`**
   - Comprehensive code quality check
   - Confirmation all ACs implemented

---

## License

See LICENSE file for details.
