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
    '.github/skills/jira-pbi-analysis',
    '.github/skills/figma-svg-export',
    '.github/skills/ac-decomposition',
    '.github/skills/dead-code-cleanup',
    '.github/skills/git-diff-analysis',
    '.github/skills/test-environment-designer',
    '.github/hooks/safety-guard.json',
    '.github/hooks/scripts/pre_tool_guard.py'
)

foreach ($path in $paths) {
    $fullPath = Join-Path $TargetDir $path
    if (Test-Path -LiteralPath $fullPath) {
        Remove-Item -Recurse -Force $fullPath
    }
}

Write-Host 'Removed runtime assets. Project files remain unchanged.'
