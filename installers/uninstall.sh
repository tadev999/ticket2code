#!/usr/bin/env bash
set -euo pipefail

DST_DIR="${1:-$(pwd)}"

echo "Removing ticket2code runtime assets from: $DST_DIR"

paths=(
	"$DST_DIR/ticket2code"
	"$DST_DIR/.github/prompts/t2c_code.prompt.md"
	"$DST_DIR/.github/prompts/t2c_integration_tests.prompt.md"
	"$DST_DIR/.github/prompts/t2c_screen_transition_tests.prompt.md"
	"$DST_DIR/.github/prompts/t2c_review.prompt.md"
	"$DST_DIR/.github/skills/jira-pbi-analysis"
	"$DST_DIR/.github/skills/figma-svg-export"
	"$DST_DIR/.github/skills/ac-decomposition"
	"$DST_DIR/.github/skills/dead-code-cleanup"
	"$DST_DIR/.github/skills/git-diff-analysis"
	"$DST_DIR/.github/skills/test-environment-designer"
	"$DST_DIR/.github/hooks/safety-guard.json"
	"$DST_DIR/.github/hooks/scripts/pre_tool_guard.py"
)

for path in "${paths[@]}"; do
	rm -rf "$path"
done

echo "Removed runtime assets. Project files remain unchanged."
