#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DST_DIR="${1:-$(pwd)}"

if [[ ! -d "$DST_DIR" ]]; then
  echo "ERROR: target directory does not exist: $DST_DIR"
  exit 1
fi

echo "Installing ticket2code core into: $DST_DIR"
mkdir -p "$DST_DIR/.github" "$DST_DIR/docs/report" "$DST_DIR/docs/test/integration" "$DST_DIR/docs/test/screen-transition"
cp -Rf "$SRC_DIR/core/prompts" "$DST_DIR/.github/"
cp -Rf "$SRC_DIR/core/agents" "$DST_DIR/.github/"
cp -Rf "$SRC_DIR/core/skills" "$DST_DIR/.github/"
cp -Rf "$SRC_DIR/core/hooks" "$DST_DIR/.github/"

if [[ ! -f "$DST_DIR/ticket2code.config.yaml" ]]; then
  cp "$SRC_DIR/templates/project/ticket2code.config.yaml" "$DST_DIR/ticket2code.config.yaml"
fi
if [[ ! -f "$DST_DIR/.env.local" ]]; then
  cp "$SRC_DIR/templates/project/env.local.example" "$DST_DIR/.env.local.example"
fi

echo "Done."
echo "Next steps:"
echo "1) Edit $DST_DIR/ticket2code.config.yaml"
echo "2) Create $DST_DIR/.env.local from .env.local.example"
echo "3) Run: $(cd "$SRC_DIR" && pwd)/installers/doctor.sh $DST_DIR"
