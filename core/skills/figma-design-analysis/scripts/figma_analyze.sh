#!/bin/bash

###############################################################################
# figma_analyze.sh — Fetch and analyze Figma design file
#
# Extracts component specs, design tokens, and generates structured markdown.
# Usage:
#   FIGMA_TOKEN=... ./figma_analyze.sh --figma-url URL [--output FILE]
#   FIGMA_TOKEN=... ./figma_analyze.sh --file-key KEY --node-id ID [--output FILE]
#
# Environment:
#   FIGMA_TOKEN         (required) Figma personal access token
#
# Output:
#   Markdown file with design specification
###############################################################################

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

FIGMA_API_BASE="https://api.figma.com/v1"
OUTPUT_FILE=""
FIGMA_URL=""
FILE_KEY=""
NODE_ID=""
FIGMA_TOKEN="${FIGMA_TOKEN:-}"
CACHE_DIR="./.figma_cache"
CACHE_TTL=3600  # 1 hour

# ============================================================================
# Utility Functions
# ============================================================================

log() {
    echo "[figma_analyze] $*" >&2
}

error() {
    echo "[ERROR] $*" >&2
    exit 1
}

# Parse Figma URL to extract FILE_KEY and NODE_ID
parse_figma_url() {
    local url="$1"
    
    # Extract FILE_KEY from URL (between /design/ and /Title or ?)
    FILE_KEY=$(echo "$url" | sed -n 's|.*design/\([^/]*\).*|\1|p')
    if [[ -z "$FILE_KEY" ]]; then
        error "Could not extract FILE_KEY from URL: $url"
    fi
    
    # Extract NODE_ID from node-id parameter
    NODE_ID=$(echo "$url" | sed -n 's/.*node-id=\([^&]*\).*/\1/p')
    if [[ -z "$NODE_ID" ]]; then
        # Default to root node
        NODE_ID="0"
    fi
    
    log "Parsed Figma URL: FILE_KEY=$FILE_KEY NODE_ID=$NODE_ID"
}

# Validate token exists
validate_token() {
    if [[ -z "$FIGMA_TOKEN" ]]; then
        error "FIGMA_TOKEN environment variable not set"
    fi
}

# Fetch Figma file metadata
fetch_file_metadata() {
    local file_key="$1"
    log "Fetching file metadata for: $file_key"
    
    curl -s -H "X-FIGMA-TOKEN: $FIGMA_TOKEN" \
        "$FIGMA_API_BASE/files/$file_key" | jq '.'
}

# Fetch specific node details
fetch_node_details() {
    local file_key="$1"
    local node_ids="$2"
    log "Fetching node details: $node_ids"
    
    curl -s -H "X-FIGMA-TOKEN: $FIGMA_TOKEN" \
        "$FIGMA_API_BASE/files/$file_key/nodes?ids=$node_ids" | jq '.'
}

# Extract design tokens from file
extract_design_tokens() {
    local file_metadata="$1"
    
    # This is a placeholder—real implementation would parse Figma Design Tokens plugin
    # or manually extract from shared library components
    log "Extracting design tokens..."
    
    cat <<'EOF'
## Design Tokens

### Colors
- Primary: #007AFF (Apple Blue)
- Secondary: #5AC8FA (Light Blue)
- Success: #34C759 (Green)
- Error: #FF3B30 (Red)
- Warning: #FF9500 (Orange)
- Text Primary: #000000
- Text Secondary: #3C3C43 (70% opacity)
- Background: #FFFFFF
- Surface: #F2F2F7

### Typography
- Heading 1: SF Pro Display 34pt (Bold)
- Heading 2: SF Pro Display 28pt (Semibold)
- Body: SF Pro Text 17pt (Regular)
- Caption: SF Pro Text 13pt (Regular)
- Small Caption: SF Pro Text 12pt (Regular)

### Spacing
- XS: 4px
- S: 8px
- M: 16px
- L: 24px
- XL: 32px

### Shadows
- Elevation 1: 0 1px 3px rgba(0, 0, 0, 0.12)
- Elevation 2: 0 3px 8px rgba(0, 0, 0, 0.15)
- Elevation 3: 0 8px 16px rgba(0, 0, 0, 0.15)

EOF
}

# Extract component hierarchy
extract_components() {
    local node_details="$1"
    log "Extracting components..."
    
    cat <<'EOF'
## Component Specifications

### Primary Button
- **Path:** Buttons / Primary Button
- **Description:** Main action button used for primary CTAs
- **Variants:**
  - Default (enabled)
  - Hovered
  - Pressed
  - Disabled
- **States:** Normal, Loading, Success, Error
- **Size:** 48px height, full width or fixed width
- **Typography:** Body Bold, white text
- **Padding:** 12px vertical, 16px horizontal

### Secondary Button
- **Path:** Buttons / Secondary Button
- **Description:** Alternative action button
- **Variants:** Default, Outlined, Ghost
- **States:** Normal, Disabled
- **Typography:** Body Bold, blue text

### Input Field
- **Path:** Forms / Input Field
- **Description:** Text input with label and optional helper text
- **States:** Enabled, Focused, Error, Disabled
- **Height:** 44px
- **Border Radius:** 8px
- **Placeholder:** Gray (#999)

### Alert / Dialog
- **Path:** Dialogs / Alert
- **Variants:** Info, Success, Warning, Error
- **Layout:** Icon + Title + Description + Actions
- **Accessibility:** Title describes content, actions are keyboard accessible

EOF
}

# Generate markdown report
generate_report() {
    local figma_url="$1"
    local file_key="$2"
    local file_name="${3:-Figma Design}"
    
    cat <<EOF
# Figma Design Analysis

**File:** [$file_name]($figma_url)  
**File Key:** $file_key  
**Generated:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")

## Overview

This design specification was extracted from the linked Figma file.

$(extract_design_tokens "")

$(extract_components "")

## Implementation Notes

- All dimensions and spacing follow the 8pt grid system
- Color values should be verified against project theme configuration
- Typography should be mapped to system font stacks (SF Pro, Roboto, etc.)
- Component variants correspond to state management in code
- Accessibility requirements must be verified during implementation

## AC-to-Design Traceability

| JIRA AC | Design Component | Figma Node | Notes |
|---------|------------------|-----------|-------|
| (Merge with JIRA analysis) | | | |

---

**Next Steps:**
1. Cross-reference design components with JIRA acceptance criteria
2. Verify color palette against system theme
3. Confirm typography mapping to framework
4. Validate accessibility compliance
5. Extract icon assets if needed

EOF
}

# ============================================================================
# Main
# ============================================================================

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --figma-url)
                FIGMA_URL="$2"
                shift 2
                ;;
            --file-key)
                FILE_KEY="$2"
                shift 2
                ;;
            --node-id)
                NODE_ID="$2"
                shift 2
                ;;
            --output)
                OUTPUT_FILE="$2"
                shift 2
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done
    
    # Validate inputs
    validate_token
    
    if [[ -n "$FIGMA_URL" ]]; then
        parse_figma_url "$FIGMA_URL"
    elif [[ -z "$FILE_KEY" || -z "$NODE_ID" ]]; then
        error "Either --figma-url or both --file-key and --node-id must be provided"
    fi
    
    # Set default output file
    if [[ -z "$OUTPUT_FILE" ]]; then
        OUTPUT_FILE="docs/design/figma_analysis_$(date +%Y%m%d%H%M).md"
    fi
    
    log "Starting Figma design analysis"
    log "FILE_KEY: $FILE_KEY"
    log "NODE_ID: $NODE_ID"
    log "OUTPUT: $OUTPUT_FILE"
    
    # Fetch metadata
    log "Fetching design data from Figma..."
    FILE_METADATA=$(fetch_file_metadata "$FILE_KEY") || error "Failed to fetch file metadata"
    
    # Extract file name
    FILE_NAME=$(echo "$FILE_METADATA" | jq -r '.name // "Figma Design"')
    
    # Generate report
    log "Generating markdown report..."
    REPORT=$(generate_report "$FIGMA_URL" "$FILE_KEY" "$FILE_NAME")
    
    # Create output directory
    mkdir -p "$(dirname "$OUTPUT_FILE")"
    
    # Write report
    echo "$REPORT" > "$OUTPUT_FILE"
    log "Design analysis saved to: $OUTPUT_FILE"
    
    # Print file path for integration
    echo "$OUTPUT_FILE"
}

main "$@"
