# Decision Gates

## Canonical gate schema

Every VSCode prompt config must use this shape:
{
  "id": "<stable_gate_id>",
  "stage": "<stage_label>",
  "header": "<vscode_askQuestions_header>",
  "question": "<prompt_text>",
  "options": [
    { "label": "<choice_1>", "recommended": true },
    { "label": "<choice_2>" }
  ],
  "defaultPolicy": "no_assumption",
  "onNoExplicitChoice": "do_not_assume"
}

Schema rules:
- id must remain stable for parser compatibility.
- header maps directly to vscode_askQuestions header.
- defaultPolicy and onNoExplicitChoice are mandatory for all gates.

Label source of truth:
- Reuse labels from processor-specs/08-decision-labels.md.

## Stage 6 — DEV confirmation gate

VSCode prompt config:
{
  "id": "stage6_generate_code_decision",
  "stage": "Stage 6",
  "header": "generate_code_decision",
  "question": "Analysis is ready. What would you like to do next?",
  "options": [
    { "key": "stage6.yes_generate_code", "label": "Yes, generate code", "recommended": true },
    { "key": "stage6.adjust_analysis", "label": "Adjust analysis" },
    { "key": "stage6.add_files", "label": "Add files" },
    { "key": "stage6.cancel", "label": "Cancel" }
  ],
  "defaultPolicy": "no_assumption",
  "onNoExplicitChoice": "do_not_assume"
}

Handler:
- Yes -> proceed to Stage 7
- Adjust analysis -> revise analysis and re-present Stage 6
- Add files -> update impacted file list and re-present Stage 6
- Cancel -> stop workflow
- No explicit choice -> do not assume

## Stage 10.5 — Test execution decision gate

Policy:
- Stage 10.5 is the exclusive gate for running test/build commands.
- Before this gate, only compile/type-check/lint allowed for cleanup evidence.

VSCode prompt config:
{
  "id": "stage10_5_run_tests_decision",
  "stage": "Stage 10.5",
  "header": "run_tests_decision",
  "question": "Would you like to run the test suite now to validate the code changes?",
  "options": [
    { "key": "stage10_5.yes_run_tests", "label": "Yes, run tests now", "recommended": true },
    { "key": "stage10_5.no_defer_ci", "label": "No, defer to CI build" }
  ],
  "defaultPolicy": "no_assumption",
  "onNoExplicitChoice": "do_not_assume"
}

Handler:
- Yes -> execute tests/build and report results
- No -> record deferred in Section 3
- No explicit choice -> do not assume

## Stage 12 — Commit summary decision gate

VSCode prompt config:
{
  "id": "stage12_output_commit_summary",
  "stage": "Stage 12",
  "header": "output_commit_summary",
  "question": "Would you like me to generate and output a commit summary now?",
  "options": [
    { "key": "stage12.yes_generate_commit_summary", "label": "Yes, generate commit summary", "recommended": true },
    { "key": "stage12.no_finalize_without_summary", "label": "No, finalize workflow without summary" }
  ],
  "defaultPolicy": "no_assumption",
  "onNoExplicitChoice": "do_not_assume"
}

Handler:
- Yes -> append Section 4 commit summary
- No -> record commit summary deferred
- No explicit choice -> do not assume
