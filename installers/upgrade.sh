#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DST_DIR="${1:-$(pwd)}"

if [[ ! -d "$DST_DIR" ]]; then
	echo "ERROR: target directory does not exist: $DST_DIR"
	exit 1
fi

echo "Upgrading ticket2code runtime assets in: $DST_DIR"
mkdir -p "$DST_DIR/.github"
mkdir -p "$DST_DIR/ticket2code"
cp -Rf "$SRC_DIR/core/prompts" "$DST_DIR/.github/"
cp -Rf "$SRC_DIR/core/skills" "$DST_DIR/.github/"
cp -Rf "$SRC_DIR/core/hooks" "$DST_DIR/.github/"

rm -rf "$DST_DIR/ticket2code/code" \
	"$DST_DIR/ticket2code/review" \
	"$DST_DIR/ticket2code/integration-tests" \
	"$DST_DIR/ticket2code/screen-transition-tests"
cp -Rf "$SRC_DIR/workflows/code" "$DST_DIR/ticket2code/"
cp -Rf "$SRC_DIR/workflows/review" "$DST_DIR/ticket2code/"
cp -Rf "$SRC_DIR/workflows/integration" "$DST_DIR/ticket2code/integration-tests"
cp -Rf "$SRC_DIR/workflows/screen-transition" "$DST_DIR/ticket2code/screen-transition-tests"
cp -f "$SRC_DIR/templates/project/SETUP.md" "$DST_DIR/ticket2code/SETUP.md"

echo "Upgrade completed"
