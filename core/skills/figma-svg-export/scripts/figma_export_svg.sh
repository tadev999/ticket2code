#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  figma_export_svg --figma-url <url> [--output <path>]
  figma_export_svg --file-key <key> --node-id <id> [--output <path>]

Requirements:
  - FIGMA_TOKEN must be set in the environment.

Notes:
  - node-id from Figma URLs usually appears like 12-345 and will be normalized to 12:345.
  - This script exports one concrete node to SVG using the Figma Images API.
EOF
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "ERROR: required command not found: $1" >&2
    exit 1
  fi
}

decode_url_component() {
  python3 - <<'PY' "$1"
import sys
from urllib.parse import unquote
print(unquote(sys.argv[1]))
PY
}

parse_url_field() {
  local url="$1"
  local field="$2"
  python3 - <<'PY' "$url" "$field"
import sys
from urllib.parse import urlparse, parse_qs

url = sys.argv[1]
field = sys.argv[2]
parts = urlparse(url)
if field == "file_key":
    segments = [segment for segment in parts.path.split('/') if segment]
    file_key = ""
    for index, segment in enumerate(segments):
        if segment in {"file", "design", "proto"} and index + 1 < len(segments):
            file_key = segments[index + 1]
            break
    print(file_key)
elif field == "node_id":
    query = parse_qs(parts.query)
    node_id = query.get("node-id", [""])[0]
    print(node_id)
PY
}

normalize_node_id() {
  local raw="$1"
  local decoded
  decoded="$(decode_url_component "$raw")"
  if [[ "$decoded" == *":"* ]]; then
    printf '%s\n' "$decoded"
  else
    printf '%s\n' "${decoded//-/:}"
  fi
}

file_key=""
node_id=""
figma_url=""
output_path=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --figma-url)
      figma_url="${2:-}"
      shift 2
      ;;
    --file-key)
      file_key="${2:-}"
      shift 2
      ;;
    --node-id)
      node_id="${2:-}"
      shift 2
      ;;
    --output)
      output_path="${2:-}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

require_command curl
require_command python3

if [[ -z "${FIGMA_TOKEN:-}" ]]; then
  echo "ERROR: FIGMA_TOKEN is not set." >&2
  exit 1
fi

if [[ -n "$figma_url" ]]; then
  if [[ -z "$file_key" ]]; then
    file_key="$(parse_url_field "$figma_url" file_key)"
  fi
  if [[ -z "$node_id" ]]; then
    node_id="$(parse_url_field "$figma_url" node_id)"
  fi
fi

if [[ -z "$file_key" ]]; then
  echo "ERROR: missing file key. Provide --file-key or --figma-url." >&2
  exit 1
fi

if [[ -z "$node_id" ]]; then
  echo "ERROR: missing node id. Provide --node-id or a Figma URL with node-id=..." >&2
  exit 1
fi

node_id="$(normalize_node_id "$node_id")"
encoded_node_id="$(python3 - <<'PY' "$node_id"
import sys
from urllib.parse import quote
print(quote(sys.argv[1], safe=''))
PY
)"

if [[ -z "$output_path" ]]; then
  safe_node_id="${node_id//:/-}"
  output_path="figma-${file_key}-${safe_node_id}.svg"
fi

mkdir -p "$(dirname "$output_path")"

api_url="https://api.figma.com/v1/images/${file_key}?ids=${encoded_node_id}&format=svg"
response_json="$(curl -fsSL -H "X-Figma-Token: ${FIGMA_TOKEN}" "$api_url")"

export_url="$(python3 - <<'PY' "$response_json" "$node_id"
import json
import sys

payload = json.loads(sys.argv[1])
node_id = sys.argv[2]
images = payload.get("images") or {}
print(images.get(node_id, ""))
PY
)"

if [[ -z "$export_url" || "$export_url" == "null" ]]; then
  echo "ERROR: Figma did not return an export URL for file_key=${file_key} node_id=${node_id}." >&2
  exit 1
fi

curl -fsSL "$export_url" -o "$output_path"

echo "Exported SVG"
echo "  file_key: $file_key"
echo "  node_id:  $node_id"
echo "  output:   $output_path"
