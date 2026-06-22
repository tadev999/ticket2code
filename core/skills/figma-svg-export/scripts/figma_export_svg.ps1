param(
    [string]$FigmaUrl,
    [string]$FileKey,
    [string]$NodeId,
    [string]$Output
)

$ErrorActionPreference = 'Stop'

function Show-Usage {
    @'
Usage:
  ./figma_export_svg.cmd -FigmaUrl <url> [-Output <path>]
  ./figma_export_svg.cmd -FileKey <key> -NodeId <id> [-Output <path>]

Requirements:
  - FIGMA_TOKEN must be set in the environment.

Notes:
  - node-id from Figma URLs usually appears like 12-345 and will be normalized to 12:345.
  - This script exports one concrete node to SVG using the Figma Images API.
'@ | Write-Host
}

function Get-UrlField {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Url,
        [Parameter(Mandatory = $true)]
        [ValidateSet('file_key', 'node_id')]
        [string]$Field
    )

    $uri = [System.Uri]$Url
    if ($Field -eq 'file_key') {
        $segments = $uri.AbsolutePath.Trim('/') -split '/'
        for ($index = 0; $index -lt $segments.Length; $index++) {
            if ($segments[$index] -in @('file', 'design', 'proto')) {
                if ($index + 1 -lt $segments.Length) {
                    return $segments[$index + 1]
                }
            }
        }
        return ''
    }

    $queryParts = @{}
    if ($uri.Query.Length -gt 1) {
        foreach ($pair in $uri.Query.TrimStart('?').Split('&', [System.StringSplitOptions]::RemoveEmptyEntries)) {
            $key, $value = $pair.Split('=', 2)
            $queryParts[$key] = [System.Uri]::UnescapeDataString($value)
        }
    }
    return ($queryParts['node-id'] ?? '')
}

function Normalize-NodeId {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RawNodeId
    )

    $decoded = [System.Uri]::UnescapeDataString($RawNodeId)
    if ($decoded.Contains(':')) {
        return $decoded
    }
    return $decoded.Replace('-', ':')
}

if ($PSBoundParameters.ContainsKey('Help')) {
    Show-Usage
    exit 0
}

if (-not $env:FIGMA_TOKEN) {
    throw 'FIGMA_TOKEN is not set.'
}

if ($FigmaUrl) {
    if (-not $FileKey) {
        $FileKey = Get-UrlField -Url $FigmaUrl -Field 'file_key'
    }
    if (-not $NodeId) {
        $NodeId = Get-UrlField -Url $FigmaUrl -Field 'node_id'
    }
}

if (-not $FileKey) {
    throw 'Missing file key. Provide -FileKey or -FigmaUrl.'
}

if (-not $NodeId) {
    throw 'Missing node id. Provide -NodeId or a Figma URL with node-id=...'
}

$NodeId = Normalize-NodeId -RawNodeId $NodeId
$encodedNodeId = [System.Uri]::EscapeDataString($NodeId)

if (-not $Output) {
    $safeNodeId = $NodeId.Replace(':', '-')
    $Output = "figma-$FileKey-$safeNodeId.svg"
}

$outputDirectory = Split-Path -Parent $Output
if ($outputDirectory) {
    $null = New-Item -ItemType Directory -Force -Path $outputDirectory
}

$apiUrl = "https://api.figma.com/v1/images/$FileKey?ids=$encodedNodeId&format=svg"
$response = Invoke-RestMethod -Headers @{ 'X-Figma-Token' = $env:FIGMA_TOKEN } -Uri $apiUrl -Method Get
$exportUrl = $response.images.$NodeId

if (-not $exportUrl) {
    throw "Figma did not return an export URL for file_key=$FileKey node_id=$NodeId."
}

Invoke-WebRequest -Uri $exportUrl -OutFile $Output | Out-Null

Write-Host 'Exported SVG'
Write-Host "  file_key: $FileKey"
Write-Host "  node_id:  $NodeId"
Write-Host "  output:   $Output"
