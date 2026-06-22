param(
    [string]$TargetDir = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'
$missing = $false

function Check-Path {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RelativePath
    )

    $fullPath = Join-Path $TargetDir $RelativePath
    if (Test-Path -LiteralPath $fullPath) {
        Write-Host "OK   $RelativePath"
    }
    else {
        Write-Host "MISS $RelativePath"
        $script:missing = $true
    }
}

Check-Path '.github/prompts/t2c_code.prompt.md'
Check-Path '.github/skills/jira-pbi-analysis/SKILL.md'
Check-Path '.github/skills/figma-svg-export/SKILL.md'
Check-Path '.github/hooks/safety-guard.json'
Check-Path 'ticket2code/code/code-agent.md'
Check-Path 'ticket2code/code/code-processor.prompt.md'
Check-Path 'ticket2code/review/review-agent.md'
Check-Path 'ticket2code/integration-tests/integration-tests-agent.md'
Check-Path 'ticket2code/screen-transition-tests/screen-transition-tests-agent.md'
Check-Path 'ticket2code/SETUP.md'
Check-Path 'ticket2code.config.yaml'
Check-Path '.env.local'

if ($missing) {
    throw 'Doctor check failed. Missing required files.'
}

Write-Host 'Doctor check passed.'
