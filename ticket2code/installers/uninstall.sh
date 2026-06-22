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
	"$DST_DIR/.github/agents/t2c-code.agent.md"
	"$DST_DIR/.github/agents/t2c-integration-tests.agent.md"
	"$DST_DIR/.github/agents/t2c-review.agent.md"
	"$DST_DIR/.github/agents/t2c-screen-transition-tests.agent.md"
	"$DST_DIR/.github/skills/jira-pbi-analysis"
	"$DST_DIR/.github/hooks/safety-guard.json"
	"$DST_DIR/.github/hooks/scripts/pre_tool_guard.py"
)

for path in "${paths[@]}"; do
	rm -rf "$path"
done

# Clean up only empty directories left behind after removing t2c assets.
rmdir "$DST_DIR/.github/hooks/scripts" 2>/dev/null || true
rmdir "$DST_DIR/.github/prompts" 2>/dev/null || true
rmdir "$DST_DIR/.github/agents" 2>/dev/null || true
rmdir "$DST_DIR/.github/skills" 2>/dev/null || true
rmdir "$DST_DIR/.github/hooks" 2>/dev/null || true
rmdir "$DST_DIR/.github" 2>/dev/null || true

echo "Removed runtime assets. Project files remain unchanged."
