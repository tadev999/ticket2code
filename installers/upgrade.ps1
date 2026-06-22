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
$null = New-Item -ItemType Directory -Force -Path (Join-Path $TargetDir 'ticket2code')
Copy-Item -Recurse -Force (Join-Path $SourceDir 'core/prompts') (Join-Path $TargetDir '.github/')
Copy-Item -Recurse -Force (Join-Path $SourceDir 'core/skills') (Join-Path $TargetDir '.github/')
Copy-Item -Recurse -Force (Join-Path $SourceDir 'core/hooks') (Join-Path $TargetDir '.github/')

$workflowPaths = @(
    (Join-Path $TargetDir 'ticket2code/code'),
    (Join-Path $TargetDir 'ticket2code/review'),
    (Join-Path $TargetDir 'ticket2code/integration-tests'),
    (Join-Path $TargetDir 'ticket2code/screen-transition-tests')
)
foreach ($path in $workflowPaths) {
    if (Test-Path -LiteralPath $path) {
        Remove-Item -Recurse -Force $path
    }
}

Copy-Item -Recurse -Force (Join-Path $SourceDir 'workflows/code') (Join-Path $TargetDir 'ticket2code/')
Copy-Item -Recurse -Force (Join-Path $SourceDir 'workflows/review') (Join-Path $TargetDir 'ticket2code/')
Copy-Item -Recurse -Force (Join-Path $SourceDir 'workflows/integration') (Join-Path $TargetDir 'ticket2code/integration-tests')
Copy-Item -Recurse -Force (Join-Path $SourceDir 'workflows/screen-transition') (Join-Path $TargetDir 'ticket2code/screen-transition-tests')
Copy-Item -Force (Join-Path $SourceDir 'templates/project/SETUP.md') (Join-Path $TargetDir 'ticket2code/SETUP.md')

Write-Host 'Upgrade completed'
