# Ticket2Code

A reusable ticket-to-code automation framework designed for seamless multi-project integration. Streamline your development workflow by automatically converting JIRA tickets into actionable code scaffolding and documentation.

## Overview

Ticket2Code bridges the gap between project management and development by providing a structured framework that:
- Automatically generates code structure from JIRA tickets
- Maintains consistent project standards across multiple repositories
- Reduces manual setup time and human error
- Supports macOS, Windows, and Linux via a single npm CLI (`t2c`)

## Directory Structure

```
ticket2code/
├── bin/                   # npm CLI (t2c) entrypoint
├── core/                  # Runtime assets (prompts, skills, hooks)
├── workflows/            # Workflow definitions and processors
├── templates/            # Project bootstrap templates
├── docs/                 # Documentation and guides
└── package.json          # npm package manifest (bin: t2c)
```

---

## Quick Start

### Installation

Install the `t2c` CLI once, then initialize it inside any target project.

```bash
# 1. Install the CLI globally (once per machine)
npm i -g ticket2code

# 2. Initialize inside a target project
cd /path/to/target-repo
t2c init
t2c doctor
```

Prefer not to install globally? Use `npx`:
```bash
npx ticket2code init
npx ticket2code doctor
```

Requirements:
- Node.js >= 16.7 (CLI uses `fs.cpSync`).
- Python 3 available in PATH for skill runtime (OCR, Figma, hooks).

---

## Built-in Prompts

Ticket2Code provides specialized slash commands in VS Code to streamline your workflow. All prompts require JIRA configuration in `.env.local`.

### Required Configuration (.env.local)

Create `.env.local` in your project root with JIRA connection details:

```bash
# JIRA Connection (Required for all prompts)
JIRA_TOKEN=<your Atlassian API token>
JIRA_EMAIL=<your Atlassian account email>
JIRA_URL=<your JIRA base URL>
```

Generate JIRA API token: https://id.atlassian.com/manage-profile/security/api-tokens

### Available Prompts

#### `/t2c_code TICKET-ID` — Full Ticket-to-Code Workflow

Comprehensive workflow: requirement analysis → code generation → dead code cleanup → AC evaluation.

**Input:** `/t2c_code PROJ-1234`

**How it works:**
```text
Stage 0    → Chọn ngôn ngữ giao tiếp                          [GATE bắt buộc]
Stage 1    → Fetch ticket từ JIRA API
Stage 1.5  → Thu thập nguồn design (Figma) — optional         [GATE nếu có Figma]
Stage 2    → Parse & bóc tách nội dung ticket
             (mô tả, AC, label, attachment, ảnh, Excel...)    [completeness gate]
Stage 2.5  → Phân tích design (Figma/OCR) — optional
Stage 3    → Explore codebase (module, file, API ảnh hưởng)
Stage 4    → Sinh báo cáo phân tích (Section 1)
Stage 5    → Lưu báo cáo: docs/report/<TICKET>_reports_<time>.md
─────────────────────────────────────────────────────────────
Stage 5.5  → HỎI BỔ SUNG (Excel/CSV, ảnh, .md/.txt, gõ text)  [GATE bắt buộc HỎI]
             → nếu có: merge vào báo cáo, lưu lại, trình bày lại
             → chỉ làm giàu báo cáo, KHÔNG sinh code
Stage 6    → XÁC NHẬN thực hiện                               [GATE bắt buộc]
             Options: Confirm and implement / Revise / Adjust scope / Cancel
─────────────────────────────────────────────────────────────
Stage 7    → Sinh code (chỉ khi đã Confirm)
Stage 8    → Phân rã AC thành các item nguyên tử
Stage 9    → Đánh giá code theo ma trận AC (Met/Partially/Not/Unclear)
Stage 9.5  → Dọn dead-code (removed symbols + search evidence + lint/type-check)
Stage 10   → Ghi kết quả đánh giá vào báo cáo (Section 2 & 3)
Stage 10.5 → HỎI chạy test/build?                            [GATE bắt buộc]
             Options: Yes, run now / No, defer
             (đây là stage DUY NHẤT được chạy test/build)
Stage 11   → Validate (coding style, logging, test rule, cleanup...)
Stage 12   → HỎI ghi commit summary?                         [GATE bắt buộc]
             Options: Yes → Section 4 / No → defer
```

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
```text
Stage 0    → Chọn ngôn ngữ giao tiếp                          [GATE bắt buộc]
Stage 1    → Resolve báo cáo ticket
             (dùng docs/report/<TICKET>_reports_*.md nếu có; nếu không → fetch JIRA)
Stage 1.5  → HỎI BỔ SUNG (Excel/CSV, ảnh, .md/.txt, gõ text)  [GATE bắt buộc HỎI]
             → làm giàu ngữ cảnh yêu cầu, dùng cho phân tích & đánh giá AC
             → chỉ làm giàu ngữ cảnh, KHÔNG đánh giá code / ghi report
Stage 2    → HỎI BASE commit hash (commit TRƯỚC khi sửa code) [GATE bắt buộc]
             Options: Provide commit hash / Cancel
Stage 3    → Lấy diff: git diff <base-commit>..HEAD
             (parse file thay đổi, insertions/deletions, ngôn ngữ)
Stage 4    → Phân tích code changes (map vào module/API, đối chiếu chuẩn repo)
Stage 5    → Đánh giá theo AC (Met / Partially / Not / Unclear)
             thứ tự kiểm tra: 1) diff → 2) codebase ngoài diff
Stage 6    → Sinh báo cáo review + lưu:
             docs/report/<TICKET>_reviews_<time>.md
             (Section 1: metadata/diff · 2: AC matrix · 3: chất lượng · 4: kết luận)
```

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
```text
Stage 0    → Chọn ngôn ngữ giao tiếp                          [GATE bắt buộc]
Stage 0.5  → Chọn execution phase: Pre-Dev / Post-Dev         [GATE bắt buộc]
Stage 1    → Fetch ticket từ JIRA API
Stage 2    → Parse & bóc tách nội dung ticket
             (AC, module, service, ảnh, Excel...)             [completeness gate]
Stage 3    → Phân tích yêu cầu test (map AC → điều kiện test)
Stage 4    → Sinh báo cáo phân tích + lưu:
             docs/test/integration/<TICKET>_integration_tests_<predev|postdev>_<time>.md
─────────────────────────────────────────────────────────────
Stage 4.2  → HỎI BỔ SUNG (Excel/CSV, ảnh, .md/.txt, gõ text)  [GATE bắt buộc HỎI]
             → nếu có: merge vào báo cáo, lưu lại, trình bày lại
             → chỉ làm giàu báo cáo, KHÔNG sinh test case
Stage 4.5  → XÁC NHẬN                                         [GATE bắt buộc]
             Options: Confirm and generate test cases / Revise / Cancel
─────────────────────────────────────────────────────────────
Stage 5    → Phân loại test cases (UI, Business Logic, API, Error...)
Stage 6    → Thiết kế environment setup (pre-conditions, data, mock, teardown)
Stage 7    → Sinh test sequences (từng bước: action → expected result)
Stage 8    → Định nghĩa expected results (measurable, verifiable, complete)
Stage 9    → Validate coverage (100% AC được cover, không orphan case)
```

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
```text
Stage 0    → Chọn ngôn ngữ giao tiếp                          [GATE bắt buộc]
Stage 0.5  → Chọn execution phase: Pre-Dev / Post-Dev         [GATE bắt buộc]
Stage 1    → Fetch ticket từ JIRA API
Stage 2    → Parse & bóc tách nội dung ticket
             (AC, màn hình, luồng UI, ảnh, Excel...)          [completeness gate]
Stage 3    → Phân tích yêu cầu test + dựng transition edges
             (From Screen → Action → To Screen)
Stage 4    → Sinh báo cáo phân tích + transition map + lưu:
             docs/test/screen-transition/<TICKET>_screen_transition_tests_<predev|postdev>_<time>.md
─────────────────────────────────────────────────────────────
Stage 4.2  → HỎI BỔ SUNG (Excel/CSV, ảnh, .md/.txt, gõ text)  [GATE bắt buộc HỎI]
             → nếu có: merge vào báo cáo, lưu lại, trình bày lại
             → chỉ làm giàu báo cáo, KHÔNG sinh test case
Stage 4.5  → XÁC NHẬN                                         [GATE bắt buộc]
             Options: Confirm and generate test cases / Revise / Cancel
─────────────────────────────────────────────────────────────
Stage 5    → Phân loại transition scenarios
             (Critical / Alternate / Error Recovery / Back / Entry-Deeplink)
Stage 6    → Thiết kế environment setup (pre-conditions, data, mock, teardown)
Stage 7    → Sinh test sequences (mỗi bước: From Screen → Action → To Screen)
Stage 8    → Định nghĩa expected results (measurable, verifiable, complete)
Stage 9    → Validate coverage (100% AC → step traceability, không orphan case)
```

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
- **Attachment evidence is traceable**: when images/spreadsheets are used, reports cite those sources explicitly

---

## CLI Commands

The `t2c` CLI runs against a target project directory (defaults to the current directory).

```bash
t2c init        # Install hybrid runtime into the target project (alias: install)
t2c doctor      # Validate project + user-level assets + Python runtime
t2c upgrade     # Refresh runtime/assets and version lock
t2c uninstall   # Remove project-local .t2c metadata and t2c prompt entrypoints
```

Global options:
```bash
t2c --version   # Print the installed t2c version (aliases: -v, version)
t2c --help      # Print usage and available commands (alias: -h)
```

By default `uninstall` only removes project-local files and keeps the shared
user-level runtime/assets (other projects may still use them). To also remove the
shared user-level runtime/assets/cache/logs, add `--purge`:

```bash
t2c uninstall --purge
```

> Note: `--purge` and `--version` are provided by the CLI binary itself. Running
> `t2c upgrade` only refreshes the runtime/assets — it does not update the global
> `t2c` executable. If these flags appear to have no effect, your globally
> installed CLI is outdated; reinstall it with `npm i -g ticket2code` (or
> `npm i -g .` from a local checkout) and run `hash -r`.

Use `--target-dir` to target another repository:
```bash
t2c init --target-dir /absolute/path/to/target-repo
t2c doctor --target-dir /absolute/path/to/target-repo
```

After `t2c init`:
1. Edit `.t2c/config.yaml` in the target repository.
2. Create `.env.local` from `.env.local.example` and add JIRA credentials.
3. Run `t2c doctor` to validate.

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
- **Compatibility:** See `docs/compatibility-matrix.md`

---

## Support & Troubleshooting

### Common Issues

**npm install / CLI issues:**
- Ensure Node.js >= 16.7 (`node -v`); older versions lack `fs.cpSync`.
- `command not found: t2c` after global install — the npm global bin is not on PATH. Run `npm config get prefix` and add its `bin` (macOS/Linux) or the prefix folder (Windows `%APPDATA%\npm`) to PATH.
- Permission error on global install — set a user-level prefix instead of using sudo/admin (e.g. `npm config set prefix "$HOME/.npm-global"`), then reinstall.

**Windows-specific:**
- If PowerShell blocks scripts (ExecutionPolicy), run via `cmd.exe` or use `npx ticket2code ...`, or allow user scripts: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- Global installs use `%APPDATA%\npm` and normally do not require admin.

**Doctor check reports warnings:**
- `WARN python runtime not found` — install Python 3 (required at skill runtime, not for the CLI).
- Run `doctor` again to see detailed diagnostic output
- Check `.env.local` configuration is complete
- Verify JIRA credentials are correct

**Configuration not being recognized:**
- Ensure `.t2c/config.yaml` exists in the repository root
- Check file formatting and YAML syntax

### Need Help?

Refer to the documentation files in the `docs/` directory or check the installation logs for detailed error information.

---

## Environment Variables

### Optional: Corporate Proxy (.env.local)

If your machine is behind a proxy that requires authentication, add these to `.env.local`. Any skill that performs network or install steps (`curl`, `pip install`, Figma API fetch) loads `.env.local` first, so no per-command flags are needed:

```bash
# URL-encode special characters in USER/PASS (@ -> %40, : -> %3A, / -> %2F)
HTTPS_PROXY="http://USER:PASS@proxy.host:PORT"
HTTP_PROXY="http://USER:PASS@proxy.host:PORT"
NO_PROXY="localhost,127.0.0.1,.company.local"

# Only if you hit CERTIFICATE_VERIFY_FAILED behind a TLS-intercepting proxy
#REQUESTS_CA_BUNDLE="/absolute/path/to/corp-ca.pem"
#CURL_CA_BUNDLE="/absolute/path/to/corp-ca.pem"
```

For detailed setup, see `docs/install.md`.

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
https://github.com/tadev999/ticket2code
