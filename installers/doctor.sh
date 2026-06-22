#!/usr/bin/env bash
set -euo pipefail

DST_DIR="${1:-$(pwd)}"
missing=0

check() {
  local path="$1"
  if [[ -e "$DST_DIR/$path" ]]; then
    echo "OK  $path"
  else
    echo "MISS $path"
    missing=1
  fi
}

check ".github/prompts/t2c_code.prompt.md"
check ".github/skills/jira-pbi-analysis/SKILL.md"
check ".github/skills/figma-svg-export/SKILL.md"
check ".github/hooks/safety-guard.json"
check "ticket2code/code/code-agent.md"
check "ticket2code/code/code-processor.prompt.md"
check "ticket2code/review/review-agent.md"
check "ticket2code/integration-tests/integration-tests-agent.md"
check "ticket2code/screen-transition-tests/screen-transition-tests-agent.md"
check "ticket2code/SETUP.md"
check "ticket2code.config.yaml"
check ".env.local"

if [[ "$missing" -ne 0 ]]; then
  echo "Doctor check failed. Missing required files."
  exit 1
fi

echo "Doctor check passed."
