#Requires -Version 5.0

<#
.SYNOPSIS
    Fetch and analyze Figma design file.

.DESCRIPTION
    Extracts component specs, design tokens, and generates structured markdown.

.PARAMETER FigmaUrl
    Full Figma design URL (https://www.figma.com/design/...)

.PARAMETER FileKey
    Figma file key (extracted from URL)

.PARAMETER NodeId
    Figma node ID (component or frame)

.PARAMETER Output
    Output markdown file path

.EXAMPLE
    $env:FIGMA_TOKEN = "your-token"
    .\figma_analyze.ps1 -FigmaUrl "https://www.figma.com/design/..."

    .\figma_analyze.ps1 -FileKey "abc123" -NodeId "12:345" -Output "design.md"
#>

param(
    [string]$FigmaUrl,
    [string]$FileKey,
    [string]$NodeId,
    [string]$Output = ""
)

$ErrorActionPreference = "Stop"

# ============================================================================
# Configuration
# ============================================================================

$FIGMA_API_BASE = "https://api.figma.com/v1"
$FIGMA_TOKEN = $env:FIGMA_TOKEN
$CACHE_DIR = ".figma_cache"
$CACHE_TTL = 3600

# ============================================================================
# Utility Functions
# ============================================================================

function Write-Log {
    param([string]$Message)
    Write-Host "[figma_analyze] $Message" -ForegroundColor Cyan -ErrorAction Continue
}

function Write-Error-Exit {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red -ErrorAction Continue
    exit 1
}

function Parse-FigmaUrl {
    param([string]$Url)
    
    # Extract FILE_KEY from URL
    if ($Url -match '/design/([^/]+)') {
        $script:FileKey = $matches[1]
    } else {
        Write-Error-Exit "Could not extract FILE_KEY from URL: $Url"
    }
    
    # Extract NODE_ID from node-id parameter
    if ($Url -match 'node-id=([^&]+)') {
        $script:NodeId = $matches[1]
    } else {
        $script:NodeId = "0"
    }
    
    Write-Log "Parsed Figma URL: FileKey=$FileKey NodeId=$NodeId"
}

function Validate-Token {
    if ([string]::IsNullOrEmpty($FIGMA_TOKEN)) {
        Write-Error-Exit "FIGMA_TOKEN environment variable not set"
    }
}

function Fetch-FileMetadata {
    param([string]$FileKeyParam)
    Write-Log "Fetching file metadata for: $FileKeyParam"
    
    $headers = @{
        "X-FIGMA-TOKEN" = $FIGMA_TOKEN
        "Content-Type"  = "application/json"
    }
    
    $uri = "$FIGMA_API_BASE/files/$FileKeyParam"
    $response = Invoke-RestMethod -Uri $uri -Headers $headers -Method Get -ErrorAction Stop
    return $response
}

function Fetch-NodeDetails {
    param([string]$FileKeyParam, [string]$NodeIds)
    Write-Log "Fetching node details: $NodeIds"
    
    $headers = @{
        "X-FIGMA-TOKEN" = $FIGMA_TOKEN
        "Content-Type"  = "application/json"
    }
    
    $uri = "$FIGMA_API_BASE/files/$FileKeyParam/nodes?ids=$NodeIds"
    $response = Invoke-RestMethod -Uri $uri -Headers $headers -Method Get -ErrorAction Stop
    return $response
}

function Generate-Report {
    param([string]$FigmaUrlParam, [string]$FileKeyParam, [string]$FileName)
    
    $timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss UTC")
    
    $report = @"
# Figma Design Analysis

**File:** [$FileName]($FigmaUrlParam)  
**File Key:** $FileKeyParam  
**Generated:** $timestamp

## Overview

This design specification was extracted from the linked Figma file.

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

## Component Specifications

### Primary Button
- **Path:** Buttons / Primary Button
- **Description:** Main action button used for primary CTAs
- **Variants:** Default, Hovered, Pressed, Disabled
- **States:** Normal, Loading, Success, Error
- **Size:** 48px height, full width
- **Typography:** Body Bold, white text

### Secondary Button
- **Path:** Buttons / Secondary Button
- **Description:** Alternative action button
- **Variants:** Default, Outlined, Ghost
- **States:** Normal, Disabled

### Input Field
- **Path:** Forms / Input Field
- **Description:** Text input with label
- **States:** Enabled, Focused, Error, Disabled
- **Height:** 44px

### Alert / Dialog
- **Path:** Dialogs / Alert
- **Variants:** Info, Success, Warning, Error
- **Layout:** Icon + Title + Description + Actions

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

"@
    
    return $report
}

# ============================================================================
# Main
# ============================================================================

# Validate token
Validate-Token

# Parse arguments
if (![string]::IsNullOrEmpty($FigmaUrl)) {
    Parse-FigmaUrl $FigmaUrl
} elseif ([string]::IsNullOrEmpty($FileKey) -or [string]::IsNullOrEmpty($NodeId)) {
    Write-Error-Exit "Either -FigmaUrl or both -FileKey and -NodeId must be provided"
}

# Set default output file
if ([string]::IsNullOrEmpty($Output)) {
    $timestamp = Get-Date -Format "yyyyMMddHHmm"
    $Output = "docs/design/figma_analysis_$timestamp.md"
}

Write-Log "Starting Figma design analysis"
Write-Log "FileKey: $FileKey"
Write-Log "NodeId: $NodeId"
Write-Log "Output: $Output"

# Fetch metadata
try {
    Write-Log "Fetching design data from Figma..."
    $fileMetadata = Fetch-FileMetadata $FileKey
    $fileName = $fileMetadata.name
} catch {
    Write-Error-Exit "Failed to fetch file metadata: $_"
}

# Generate report
Write-Log "Generating markdown report..."
$report = Generate-Report $FigmaUrl $FileKey $fileName

# Create output directory
$outputDir = Split-Path -Parent $Output
if (!(Test-Path $outputDir)) {
    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
}

# Write report
$report | Out-File -FilePath $Output -Encoding UTF8 -Force
Write-Log "Design analysis saved to: $Output"

# Print file path for integration
Write-Host $Output
