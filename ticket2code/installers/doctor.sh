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
check ".github/agents/t2c-code.agent.md"
check ".github/skills/jira-pbi-analysis/SKILL.md"
check ".github/hooks/safety-guard.json"
check "ticket2code.config.yaml"
check ".env.local"

if [[ "$missing" -ne 0 ]]; then
  echo "Doctor check failed. Missing required files."
  exit 1
fi

echo "Doctor check passed."
