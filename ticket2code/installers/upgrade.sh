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
cp -Rf "$SRC_DIR/core/prompts" "$DST_DIR/.github/"
cp -Rf "$SRC_DIR/core/agents" "$DST_DIR/.github/"
cp -Rf "$SRC_DIR/core/skills" "$DST_DIR/.github/"
cp -Rf "$SRC_DIR/core/hooks" "$DST_DIR/.github/"

echo "Upgrade completed"
