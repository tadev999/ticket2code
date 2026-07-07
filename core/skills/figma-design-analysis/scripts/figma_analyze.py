#!/usr/bin/env python3
"""Figma design analysis via the Figma REST API.

Python port of the previous Node.js analyzer. Produces a markdown design
report (or exports an SVG asset) from a Figma file/node.

Environment:
  FIGMA_TOKEN is required for direct Figma API analysis.
  .env.local is loaded automatically when present.
  HTTP(S)_PROXY / NO_PROXY are honored automatically (urllib proxy handling,
  including CONNECT tunneling and Basic proxy auth from the proxy URL).
  REQUESTS_CA_BUNDLE / CURL_CA_BUNDLE / PIP_CERT are used as the CA bundle
  when set (helps with corporate TLS interception).
"""

import base64
import hashlib
import json
import os
import random
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from urllib.parse import unquote, urlparse

FIGMA_API_BASE = "https://api.figma.com/v1"
CACHE_DIR = ".figma_cache"
CACHE_TTL_SECONDS = 3600
MAX_RETRIES = 6
BASE_DELAY_SECONDS = 1
INTER_REQUEST_DELAY_MS = 200
MAX_RETRY_AFTER_SECONDS = 30


def log(message):
    sys.stderr.write(f"[figma_analyze] {message}\n")


def screenshot_input_hint():
    sys.stderr.write(
        "\n".join(
            [
                "[figma_analyze] Alternative input option:",
                "[figma_analyze] - Capture screenshots/images from Figma and place them under:",
                "[figma_analyze]   docs/figma_design_analysis/<TICKET-ID>_screenshots/",
                "[figma_analyze] - Supported formats: .png, .jpg, .jpeg, .webp",
                "[figma_analyze] - Then run the design analysis workflow in screenshot/image mode.",
                "",
            ]
        )
        + "\n"
    )


def fail(message):
    sys.stderr.write(f"[ERROR] {message}\n")
    sys.exit(1)


def show_usage():
    sys.stdout.write(
        "Usage:\n"
        "  python3 figma_analyze.py --figma-url <url> [--output <file>] [--no-cache]\n"
        "  python3 figma_analyze.py --file-key <key> --node-id <id> [--output <file>] [--no-cache]\n"
        "  python3 figma_analyze.py --figma-url <url> --export-svg --asset-output <file.svg>\n"
        "  python3 figma_analyze.py --file-key <key> --node-id <id> --export-svg --asset-output <file.svg>\n"
        "\n"
        "Environment:\n"
        "  FIGMA_TOKEN is required for direct Figma API analysis.\n"
        "  .env.local is loaded automatically when present.\n"
        "  HTTP(S)_PROXY / NO_PROXY are honored automatically.\n"
    )


def load_dotenv_local():
    env_path = os.path.join(os.getcwd(), ".env.local")
    if not os.path.isfile(env_path):
        return
    with open(env_path, "r", encoding="utf-8") as handle:
        for raw_line in handle.read().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            if not key or not (key[0].isalpha() or key[0] == "_"):
                continue
            value = value.strip()
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            os.environ.setdefault(key, value)


def parse_args(argv):
    options = {
        "figmaUrl": "",
        "fileKey": "",
        "nodeId": "",
        "output": "",
        "assetOutput": "",
        "exportSvg": False,
        "exportSvgNodeId": "",
        "noCache": False,
    }

    aliases = {
        "--figma-url": "figmaUrl",
        "-FigmaUrl": "figmaUrl",
        "--file-key": "fileKey",
        "-FileKey": "fileKey",
        "--node-id": "nodeId",
        "-NodeId": "nodeId",
        "--output": "output",
        "-Output": "output",
        "--asset-output": "assetOutput",
        "-AssetOutput": "assetOutput",
        "--export-svg-node-id": "exportSvgNodeId",
        "-ExportSvgNodeId": "exportSvgNodeId",
    }

    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in ("--help", "-h", "/?"):
            show_usage()
            sys.exit(0)
        if arg in ("--no-cache", "-NoCache"):
            options["noCache"] = True
            index += 1
            continue
        if arg in ("--export-svg", "-ExportSvg"):
            options["exportSvg"] = True
            index += 1
            continue

        key = aliases.get(arg)
        if not key:
            fail(f"Unknown option: {arg}")
        value = argv[index + 1] if index + 1 < len(argv) else None
        if not value or value.startswith("--"):
            fail(f"Missing value for {arg}")
        options[key] = value
        index += 2

    return options


def normalize_node_id(raw):
    return unquote(str(raw)).replace("-", ":")


def parse_figma_url(url):
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("missing scheme/host")
    except ValueError:
        fail(f"Invalid Figma URL: {url}")

    segments = [segment for segment in parsed.path.split("/") if segment]
    file_marker_index = -1
    for position, segment in enumerate(segments):
        if segment in ("design", "file", "proto"):
            file_marker_index = position
            break
    if file_marker_index < 0 or file_marker_index + 1 >= len(segments):
        fail(f"Could not extract FILE_KEY from URL: {url}")

    node_id = "0"
    for pair in parsed.query.split("&"):
        if pair.startswith("node-id="):
            node_id = normalize_node_id(pair[len("node-id="):])
            break

    return {"fileKey": segments[file_marker_index + 1], "nodeId": node_id}


def cache_key(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def cache_path(key):
    return os.path.join(CACHE_DIR, f"{key}.json")


def cache_get(key, no_cache):
    target_path = cache_path(key)
    if no_cache or not os.path.isfile(target_path):
        return None
    age_seconds = time.time() - os.path.getmtime(target_path)
    if age_seconds > CACHE_TTL_SECONDS:
        return None
    log(f"Cache hit: {key}")
    with open(target_path, "r", encoding="utf-8") as handle:
        return handle.read()


def cache_put(key, content):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(cache_path(key), "w", encoding="utf-8") as handle:
        handle.write(content)


def build_opener():
    handlers = []
    proxies = urllib.request.getproxies()
    if proxies:
        handlers.append(urllib.request.ProxyHandler(proxies))
    ca_bundle = (
        os.environ.get("REQUESTS_CA_BUNDLE")
        or os.environ.get("CURL_CA_BUNDLE")
        or os.environ.get("PIP_CERT")
    )
    context = ssl.create_default_context(cafile=ca_bundle) if ca_bundle else ssl.create_default_context()
    handlers.append(urllib.request.HTTPSHandler(context=context))
    return urllib.request.build_opener(*handlers)


def request_text(opener, url, token):
    headers = {"Accept": "application/json"}
    if token:
        headers["X-FIGMA-TOKEN"] = token
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with opener.open(request, timeout=60) as response:
            return {
                "status": getattr(response, "status", response.getcode()),
                "headers": response.headers,
                "body": response.read().decode("utf-8"),
            }
    except urllib.error.HTTPError as error:
        return {
            "status": error.code,
            "headers": error.headers,
            "body": error.read().decode("utf-8", "replace"),
        }


def request_buffer(opener, url):
    request = urllib.request.Request(url, method="GET")
    try:
        with opener.open(request, timeout=120) as response:
            return {
                "status": getattr(response, "status", response.getcode()),
                "body": response.read(),
            }
    except urllib.error.HTTPError as error:
        return {"status": error.code, "body": error.read()}


def api_get_json(opener, url, key, token, no_cache):
    cached = cache_get(key, no_cache)
    if cached:
        return json.loads(cached)

    for attempt in range(1, MAX_RETRIES + 1):
        response = request_text(opener, url, token)
        status = response["status"]
        if 200 <= status < 300:
            cache_put(key, response["body"])
            time.sleep(INTER_REQUEST_DELAY_MS / 1000)
            return json.loads(response["body"])

        if status == 429:
            retry_after_raw = response["headers"].get("Retry-After") if response["headers"] else None
            try:
                retry_after = float(retry_after_raw)
            except (TypeError, ValueError):
                retry_after = None
            exponential_delay = min(BASE_DELAY_SECONDS * (2 ** (attempt - 1)), MAX_RETRY_AFTER_SECONDS)
            if retry_after is not None and retry_after <= MAX_RETRY_AFTER_SECONDS:
                delay_seconds = retry_after
            else:
                delay_seconds = exponential_delay + random.random() * 0.5
            log(
                f"Rate limited (429). Backoff {delay_seconds:.2f}s "
                f"(attempt {attempt}/{MAX_RETRIES})"
            )
            time.sleep(delay_seconds)
            continue

        fail(f"Figma API request failed (HTTP {status}): {response['body']}")

    screenshot_input_hint()
    fail("Figma API exhausted retries after 429 responses.")


def fetch_file_metadata(opener, file_key, token, no_cache):
    log(f"Fetching file metadata for: {file_key}")
    return api_get_json(
        opener,
        f"{FIGMA_API_BASE}/files/{urllib.parse.quote(file_key, safe='')}",
        cache_key(f"file:{file_key}"),
        token,
        no_cache,
    )


def fetch_node_details(opener, file_key, node_ids, token, no_cache):
    normalized = ",".join(normalize_node_id(node_id.strip()) for node_id in node_ids.split(","))
    encoded = ",".join(urllib.parse.quote(node_id, safe="") for node_id in normalized.split(","))
    log(f"Fetching node details: {normalized}")
    return api_get_json(
        opener,
        f"{FIGMA_API_BASE}/files/{urllib.parse.quote(file_key, safe='')}/nodes?ids={encoded}",
        cache_key(f"nodes:{file_key}:{normalized}"),
        token,
        no_cache,
    )


def fetch_image_export(opener, file_key, node_id, image_format, token, no_cache):
    normalized = normalize_node_id(node_id)
    encoded = urllib.parse.quote(normalized, safe="")
    log(f"Requesting {image_format.upper()} export URL for node: {normalized}")
    return api_get_json(
        opener,
        f"{FIGMA_API_BASE}/images/{urllib.parse.quote(file_key, safe='')}?ids={encoded}&format={image_format}",
        cache_key(f"images:{file_key}:{normalized}:{image_format}"),
        token,
        no_cache,
    )


def export_svg_node(opener, file_key, node_id, asset_output, token, no_cache):
    normalized_node_id = normalize_node_id(node_id)
    export_response = fetch_image_export(opener, file_key, normalized_node_id, "svg", token, no_cache)
    export_url = (export_response.get("images") or {}).get(normalized_node_id, "")
    if not export_url:
        fail(
            f"Figma did not return an SVG export URL for file_key={file_key} "
            f"node_id={normalized_node_id}."
        )

    output = asset_output or f"figma-{file_key}-{normalized_node_id.replace(':', '-')}.svg"
    svg_response = request_buffer(opener, export_url)
    if not (200 <= svg_response["status"] < 300):
        fail(f"Failed to download SVG export (HTTP {svg_response['status']}).")

    output_directory = os.path.dirname(output)
    if output_directory and output_directory != ".":
        os.makedirs(output_directory, exist_ok=True)
    with open(output, "wb") as handle:
        handle.write(svg_response["body"])
    log(f"SVG export saved to: {output}")
    sys.stdout.write(f"{output}\n")


def coalesce(*values, default=None):
    for value in values:
        if value is not None:
            return value
    return default


def js_str(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return repr(value)
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return str(value)


def markdown(value):
    text = js_str(value)
    text = text.replace("|", "\\|")
    return " ".join(text.split("\n"))


def node_size(node):
    box = node.get("absoluteBoundingBox") or node.get("size") or {}
    width = coalesce(box.get("width"), box.get("x"), default="?")
    height = coalesce(box.get("height"), box.get("y"), default="?")
    return f"{js_str(width)} x {js_str(height)}"


def selected_documents(node_details):
    documents = []
    for entry in (node_details.get("nodes") or {}).values():
        document = entry.get("document") if isinstance(entry, dict) else None
        if document:
            documents.append(document)
    return documents


def flatten_nodes(root):
    if not isinstance(root, dict):
        return []
    nodes = [root]
    for child in root.get("children") or []:
        nodes.extend(flatten_nodes(child))
    return nodes


def all_selected_nodes(node_details):
    nodes = []
    for document in selected_documents(node_details):
        nodes.extend(flatten_nodes(document))
    return nodes


def to_byte(value):
    return max(0, min(255, int((value or 0) * 255 + 0.5)))


def color_hex(color):
    if not color:
        return "n/a"
    hex_value = "#" + "".join(
        f"{to_byte(color.get(part)):02X}" for part in ("r", "g", "b")
    )
    alpha = coalesce(color.get("a"), default=1)
    return f"{hex_value} @ {js_str(alpha)}" if alpha < 1 else hex_value


def paint_name(paint):
    if paint and paint.get("type") == "SOLID" and paint.get("color"):
        return color_hex(paint.get("color"))
    return (paint.get("type") if paint else None) or "Unknown paint"


def unique_sorted(values):
    seen = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return sorted(seen)


def limit(values, count):
    return list(values)[:count]


def section(title, lines):
    return "\n".join([f"## {title}", "", *lines])


def visible_paints(node, keys):
    paints = []
    for key in keys:
        for paint in node.get(key) or []:
            if paint.get("visible") is not False:
                paints.append(paint)
    return paints


def extract_overview(file_metadata, node_details):
    documents = selected_documents(node_details)
    pages = ", ".join(
        page.get("name", "") for page in (file_metadata.get("document") or {}).get("children") or []
    )
    if not documents:
        root_rows = ["| Not found | - | - | - | - |"]
    else:
        root_rows = [
            f"| {markdown(document.get('name') or 'Unnamed')} "
            f"| {markdown(document.get('type') or 'Unknown')} "
            f"| {markdown(document.get('id') or '-')} "
            f"| {node_size(document)} "
            f"| {len(document.get('children') or [])} |"
            for document in documents
        ]

    return section(
        "Overview",
        [
            "- **Input source:** Direct Figma API",
            f"- **File name:** {markdown(file_metadata.get('name') or 'Unknown')}",
            f"- **Last modified:** {markdown(file_metadata.get('lastModified') or 'Unknown')}",
            f"- **Version:** {markdown(file_metadata.get('version') or 'Unknown')}",
            f"- **Selected node count:** {len(documents)}",
            f"- **Top-level pages in file:** {markdown(pages)}",
            "",
            "### Selected Root Nodes",
            "",
            "| Node | Type | Figma Node ID | Size | Children |",
            "|------|------|---------------|------|----------|",
            *root_rows,
        ],
    )


def extract_design_tokens(file_metadata, node_details):
    log("Extracting design tokens from Figma JSON...")
    nodes = all_selected_nodes(node_details)

    colors = unique_sorted(
        [paint_name(paint) for node in nodes for paint in visible_paints(node, ("fills", "strokes"))]
    )

    typography = []
    for node in nodes:
        if node.get("type") == "TEXT" and node.get("style"):
            style = node["style"]
            typography.append(
                " | ".join(
                    [
                        style.get("fontFamily") or "Unknown",
                        style.get("fontPostScriptName") or "",
                        f"{js_str(coalesce(style.get('fontSize'), default='?'))}px",
                        f"weight {js_str(coalesce(style.get('fontWeight'), default='?'))}",
                        "lineHeight "
                        + js_str(
                            coalesce(
                                style.get("lineHeightPx"),
                                style.get("lineHeightPercentFontSize"),
                                default="?",
                            )
                        ),
                        f"letterSpacing {js_str(coalesce(style.get('letterSpacing'), default='?'))}",
                    ]
                )
            )
    typography = unique_sorted(typography)

    spacing = limit(
        unique_sorted(
            [
                f"- **{markdown(node.get('name') or 'Unnamed')}** (id={node.get('id') or '-'}): "
                f"layout={node.get('layoutMode')}, gap={js_str(coalesce(node.get('itemSpacing'), default='n/a'))}, "
                f"padding={js_str(coalesce(node.get('paddingTop'), default=0))}/"
                f"{js_str(coalesce(node.get('paddingRight'), default=0))}/"
                f"{js_str(coalesce(node.get('paddingBottom'), default=0))}/"
                f"{js_str(coalesce(node.get('paddingLeft'), default=0))}, "
                f"sizing={js_str(coalesce(node.get('layoutSizingHorizontal'), default='n/a'))}/"
                f"{js_str(coalesce(node.get('layoutSizingVertical'), default='n/a'))}"
                for node in nodes
                if node.get("layoutMode") and node.get("layoutMode") != "NONE"
            ]
        ),
        40,
    )

    radii = limit(
        unique_sorted(
            [
                f"- **{markdown(node.get('name') or 'Unnamed')}** (id={node.get('id') or '-'}): "
                f"radius={js_str(coalesce(node.get('cornerRadius'), node.get('rectangleCornerRadii'), default='n/a'))}, "
                f"strokeWeight={js_str(coalesce(node.get('strokeWeight'), default='n/a'))}"
                for node in nodes
                if node.get("cornerRadius") is not None
                or node.get("rectangleCornerRadii") is not None
                or node.get("strokeWeight") is not None
            ]
        ),
        40,
    )

    effects = limit(
        unique_sorted(
            [
                f"- {effect.get('type') or 'Unknown'}: radius={js_str(coalesce(effect.get('radius'), default='n/a'))}, "
                f"offset={js_str(coalesce((effect.get('offset') or {}).get('x'), default=0))},"
                f"{js_str(coalesce((effect.get('offset') or {}).get('y'), default=0))}, "
                f"spread={js_str(coalesce(effect.get('spread'), default='n/a'))}, color={color_hex(effect.get('color'))}"
                for node in nodes
                for effect in node.get("effects") or []
                if effect.get("visible") is not False
            ]
        ),
        40,
    )

    styles = limit(
        [
            f"- **{markdown(style.get('name') or style_id)}**: type={style.get('styleType') or 'unknown'}, id={style_id}"
            for style_id, style in (file_metadata.get("styles") or {}).items()
        ],
        60,
    )

    return section(
        "Design Tokens",
        [
            "### Colors",
            "",
            *(["- " + color for color in colors] if colors else ["- Not found in selected node JSON."]),
            "",
            "### Typography",
            "",
            *(["- " + item for item in typography] if typography else ["- Not found in selected node JSON."]),
            "",
            "### Spacing & Auto Layout",
            "",
            *(spacing if spacing else ["- No auto-layout spacing found in selected node JSON."]),
            "",
            "### Borders & Radius",
            "",
            *(radii if radii else ["- No border/radius values found in selected node JSON."]),
            "",
            "### Effects",
            "",
            *(effects if effects else ["- No effects found in selected node JSON."]),
            "",
            "### Published Styles",
            "",
            *(styles if styles else ["- No published styles returned by Figma API."]),
        ],
    )


def tree_lines(node, depth=0):
    if not node or depth > 5:
        return []
    indent = "  " * depth
    lines = [
        f"{indent}- {markdown(node.get('name') or 'Unnamed')} "
        f"(type={node.get('type') or 'Unknown'}, id={node.get('id') or '-'}, size={node_size(node)})"
    ]
    for child in node.get("children") or []:
        lines.extend(tree_lines(child, depth + 1))
    return lines


def property_lines(nodes):
    lines = []
    for node in nodes:
        source = node.get("componentProperties") or node.get("componentPropertyDefinitions")
        if not source:
            continue
        properties = [
            f"{markdown(key)}="
            f"{js_str(coalesce(value.get('value'), value.get('defaultValue'), value.get('type'), default=''))}"
            for key, value in source.items()
        ]
        lines.append(
            f"- **{markdown(node.get('name') or 'Unnamed')}** (id={node.get('id') or '-'}): {', '.join(properties)}"
        )
    return limit(unique_sorted(lines), 80)


def extract_components(node_details):
    log("Extracting component hierarchy from Figma JSON...")
    documents = selected_documents(node_details)
    nodes = all_selected_nodes(node_details)

    root_lines = (
        [
            f"- **{markdown(document.get('name') or 'Unnamed')}** (id={document.get('id') or '-'}, "
            f"type={document.get('type') or 'Unknown'}): size={node_size(document)}, "
            f"visible={js_str(coalesce(document.get('visible'), default=True))}, "
            f"clips={js_str(coalesce(document.get('clipsContent'), default=False))}"
            for document in documents
        ]
        if documents
        else ["- Selected node was not returned by Figma API."]
    )

    hierarchy = limit([line for document in documents for line in tree_lines(document)], 160)
    properties = property_lines(nodes)

    text = limit(
        [
            f"- **{markdown(node.get('name') or 'Text')}** (id={node.get('id') or '-'}): "
            f"{markdown(node.get('characters') or '')}"
            for node in nodes
            if node.get("type") == "TEXT"
        ],
        80,
    )

    constraints = limit(
        unique_sorted(
            [
                f"- **{markdown(node.get('name') or 'Unnamed')}** (id={node.get('id') or '-'}): "
                f"horizontal={js_str(coalesce((node.get('constraints') or {}).get('horizontal'), default='n/a'))}, "
                f"vertical={js_str(coalesce((node.get('constraints') or {}).get('vertical'), default='n/a'))}, "
                f"layoutAlign={js_str(coalesce(node.get('layoutAlign'), default='n/a'))}, "
                f"grow={js_str(coalesce(node.get('layoutGrow'), default='n/a'))}"
                for node in nodes
                if node.get("constraints")
            ]
        ),
        80,
    )

    asset_types = {"VECTOR", "BOOLEAN_OPERATION", "STAR", "LINE", "ELLIPSE", "POLYGON"}
    assets = limit(
        unique_sorted(
            [
                f"- **{markdown(node.get('name') or 'Asset')}** (id={node.get('id') or '-'}, "
                f"type={node.get('type') or 'Unknown'}): export candidate for image/icon asset."
                for node in nodes
                if node.get("type") in asset_types
                or any(fill.get("type") == "IMAGE" for fill in node.get("fills") or [])
            ]
        ),
        80,
    )

    return section(
        "Component Specifications",
        [
            *root_lines,
            "",
            "### Layer Hierarchy",
            "",
            *(hierarchy if hierarchy else ["- No layer hierarchy returned."]),
            "",
            "### Variants, Component Properties & States",
            "",
            *(properties if properties else ["- No explicit component properties or variants found in selected node JSON."]),
            "",
            "### Text Content",
            "",
            *(text if text else ["- No text layers found."]),
            "",
            "### Layout Constraints",
            "",
            *(constraints if constraints else ["- No explicit constraints found."]),
            "",
            "### Asset Candidates",
            "",
            *(assets if assets else ["- No vector/image asset candidates found in selected node JSON."]),
        ],
    )


def extract_accessibility(node_details):
    small_targets = []
    for node in all_selected_nodes(node_details):
        box = node.get("absoluteBoundingBox")
        if not box:
            continue
        name = node.get("name") or ""
        width = box.get("width")
        height = box.get("height")
        if width is None or height is None:
            continue
        keyword_hit = any(
            keyword in name.lower()
            for keyword in ("button", "btn", "icon", "close", "back", "next", "tap", "link")
        )
        if (width < 44 or height < 44) and (keyword_hit or node.get("type") == "INSTANCE"):
            small_targets.append(
                f"- **{markdown(name or 'Unnamed')}** (id={node.get('id') or '-'}): "
                f"{js_str(width)} x {js_str(height)}"
            )
    small_targets = limit(small_targets, 60)

    return section(
        "Accessibility & UX Notes",
        [
            "- Verify contrast in implementation because Figma API colors can be nested in overlays, effects, and opacity inheritance.",
            "- Preserve reading order according to the layer hierarchy unless product requirements specify a different order.",
            "- Validate touch targets for all tappable layers; flag any controls below 44 x 44 pt during implementation review.",
            "- Map disabled/error/loading states from component properties when present; otherwise confirm missing states with design/product.",
            "",
            "### Small Touch Target Candidates",
            "",
            *(
                small_targets
                if small_targets
                else ["- No obvious small touch-target candidates detected by name/type heuristic."]
            ),
        ],
    )


def extract_implementation(file_key, node_id):
    return section(
        "Implementation Recommendations",
        [
            f"- Treat this report as the implementation source of truth only for nodes returned by the selected Figma node ID: {node_id}.",
            "- Map extracted colors, typography, spacing, radius, and effects to existing project design constants before adding new constants.",
            "- Implement Figma component properties as explicit UI states where applicable: default, selected, disabled, loading, error, expanded/collapsed.",
            "- Export each asset candidate through this Python analyzer before coding the final screen.",
            "- Keep raw Figma node IDs in implementation notes or test fixtures when useful for design QA traceability.",
            "",
            "### Useful Follow-up Commands",
            "",
            f"python3 ./.github/skills/figma-design-analysis/scripts/figma_analyze.py --file-key {file_key} --node-id {node_id}",
            f"python3 ./.github/skills/figma-design-analysis/scripts/figma_analyze.py --file-key {file_key} --node-id <NODE_ID> --export-svg --asset-output docs/assets/figma-<NODE_ID>.svg",
            "",
            "## AC-to-Design Traceability",
            "",
            "| JIRA AC | Design Component | Figma Node | Notes |",
            "|---------|------------------|-----------|-------|",
            "| (Merge with JIRA analysis) | | | |",
            "",
            "---",
            "",
            "**Next Steps:**",
            "1. Cross-reference design components with JIRA acceptance criteria.",
            "2. Confirm missing states and ambiguous interactions with design/product.",
            "3. Export required image/vector assets.",
            "4. Implement UI using project components and design constants.",
            "5. Validate against screenshots or exported frame images on target devices.",
        ],
    )


def generate_report(figma_url, file_key, node_id, file_metadata, node_details):
    file_name = file_metadata.get("name") or "Figma Design"
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    href = figma_url or f"https://www.figma.com/file/{file_key}"
    return "\n".join(
        [
            "# Figma Design Analysis",
            "",
            f"**File:** [{markdown(file_name)}]({href})  ",
            f"**File Key:** {file_key}  ",
            f"**Node ID:** {node_id}  ",
            f"**Generated:** {generated_at}",
            "",
            extract_overview(file_metadata, node_details),
            "",
            extract_design_tokens(file_metadata, node_details),
            "",
            extract_components(node_details),
            "",
            extract_accessibility(node_details),
            "",
            extract_implementation(file_key, node_id),
            "",
        ]
    )


def default_output_path():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M")
    return os.path.join("docs", "design", f"figma_analysis_{timestamp}.md")


def main():
    load_dotenv_local()
    options = parse_args(sys.argv[1:])

    if options["figmaUrl"]:
        parsed = parse_figma_url(options["figmaUrl"])
        options["fileKey"] = options["fileKey"] or parsed["fileKey"]
        options["nodeId"] = options["nodeId"] or parsed["nodeId"]
        log(f"Parsed Figma URL: FILE_KEY={options['fileKey']} NODE_ID={options['nodeId']}")

    if not options["fileKey"] or not options["nodeId"]:
        fail("Either --figma-url or both --file-key and --node-id must be provided.")

    options["nodeId"] = normalize_node_id(options["nodeId"])
    if options["exportSvgNodeId"]:
        options["exportSvgNodeId"] = normalize_node_id(options["exportSvgNodeId"])

    token = os.environ.get("FIGMA_TOKEN")
    if not token:
        screenshot_input_hint()
        fail("FIGMA_TOKEN environment variable is not set. Direct Figma API analysis requires a token.")

    opener = build_opener()
    output = options["output"] or default_output_path()
    log("Starting Figma design analysis")
    log(f"FILE_KEY: {options['fileKey']}")
    log(f"NODE_ID: {options['nodeId']}")
    log(
        "OUTPUT: "
        + (options["assetOutput"] or "(default SVG output)" if options["exportSvg"] else output)
    )

    if options["exportSvg"]:
        export_svg_node(
            opener,
            options["fileKey"],
            options["exportSvgNodeId"] or options["nodeId"],
            options["assetOutput"],
            token,
            options["noCache"],
        )
        return

    file_metadata = fetch_file_metadata(opener, options["fileKey"], token, options["noCache"])
    node_details = fetch_node_details(opener, options["fileKey"], options["nodeId"], token, options["noCache"])
    report = generate_report(
        options["figmaUrl"],
        options["fileKey"],
        options["nodeId"],
        file_metadata,
        node_details,
    )

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w", encoding="utf-8") as handle:
        handle.write(report)
    log(f"Design analysis saved to: {output}")
    sys.stdout.write(f"{output}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # noqa: BLE001 - top-level guard mirrors the Node version
        fail(str(error))
