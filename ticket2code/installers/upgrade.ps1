param(
    [string]$TargetDir = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'

$SourceDir = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

if (-not (Test-Path -LiteralPath $TargetDir -PathType Container)) {
    throw "Target directory does not exist: $TargetDir"
}

Write-Host "Upgrading ticket2code runtime assets in: $TargetDir"

$null = New-Item -ItemType Directory -Force -Path (Join-Path $TargetDir '.github')
Copy-Item -Recurse -Force (Join-Path $SourceDir 'core/prompts') (Join-Path $TargetDir '.github/')
Copy-Item -Recurse -Force (Join-Path $SourceDir 'core/agents') (Join-Path $TargetDir '.github/')
Copy-Item -Recurse -Force (Join-Path $SourceDir 'core/skills') (Join-Path $TargetDir '.github/')
Copy-Item -Recurse -Force (Join-Path $SourceDir 'core/hooks') (Join-Path $TargetDir '.github/')

Write-Host 'Upgrade completed'
