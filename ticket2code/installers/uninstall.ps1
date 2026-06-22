param(
    [string]$TargetDir = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'

Write-Host "Removing ticket2code runtime assets from: $TargetDir"

$paths = @(
    'ticket2code',
    '.github/prompts/t2c_code.prompt.md',
    '.github/prompts/t2c_integration_tests.prompt.md',
    '.github/prompts/t2c_screen_transition_tests.prompt.md',
    '.github/prompts/t2c_review.prompt.md',
    '.github/agents/t2c-code.agent.md',
    '.github/agents/t2c-integration-tests.agent.md',
    '.github/agents/t2c-review.agent.md',
    '.github/agents/t2c-screen-transition-tests.agent.md',
    '.github/skills/jira-pbi-analysis',
    '.github/hooks/safety-guard.json',
    '.github/hooks/scripts/pre_tool_guard.py'
)

foreach ($path in $paths) {
    $fullPath = Join-Path $TargetDir $path
    if (Test-Path -LiteralPath $fullPath) {
        Remove-Item -Recurse -Force $fullPath
    }
}

# Clean up only empty directories left behind after removing t2c assets.
$cleanupDirs = @(
    '.github/hooks/scripts',
    '.github/prompts',
    '.github/agents',
    '.github/skills',
    '.github/hooks',
    '.github'
)

foreach ($path in $cleanupDirs) {
    $fullPath = Join-Path $TargetDir $path
    if (Test-Path -LiteralPath $fullPath -PathType Container) {
        $isEmpty = (Get-ChildItem -LiteralPath $fullPath -Force | Measure-Object).Count -eq 0
        if ($isEmpty) {
            Remove-Item -LiteralPath $fullPath -Force
        }
    }
}

Write-Host 'Removed runtime assets. Project files remain unchanged.'
