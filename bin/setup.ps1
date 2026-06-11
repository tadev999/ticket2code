# Get the directory of the script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# Root of the ticket2code project (one level up from bin/)
$RootDir = Split-Path -Parent $ScriptDir

# Target directory defaults to current directory
$TargetDir = $args[0]
if ([string]::IsNullOrEmpty($TargetDir)) {
    $TargetDir = Get-Location
} else {
    if (!(Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
    }
    $TargetDir = (Resolve-Path $TargetDir).Path
}

Write-Host "[*] Starting ticket2code automated setup..."
Write-Host "[*] Source root: $RootDir"
Write-Host "[*] Target directory: $TargetDir"

# 1. Verify source directory contains required assets
$Ticket2CodeDir = Join-Path $RootDir "ticket2code"
$PromptFile = Join-Path $RootDir "ticket2code\ticket\ticket.prompt.md"

if (!(Test-Path $Ticket2CodeDir) -or !(Test-Path $PromptFile)) {
    Write-Host "[-] Error: Required template files not found in $RootDir." -ForegroundColor Red
    Exit 1
}

# 2. Create target directories if they don't exist
Write-Host "[*] Creating directories in target project..."
$TargetPromptDir = Join-Path $TargetDir ".github\prompts"
if (!(Test-Path $TargetPromptDir)) {
    New-Item -ItemType Directory -Force -Path $TargetPromptDir | Out-Null
}

# 3. Copy ticket.prompt.md to target project
Write-Host "[*] Copying ticket.prompt.md to .github/prompts/..."
Copy-Item $PromptFile -Destination $TargetPromptDir -Force

# 4. Copy ticket2code folder to target project
Write-Host "[*] Copying ticket2code folder..."
$TargetTicket2CodeDir = Join-Path $TargetDir "ticket2code"
if (!(Test-Path $TargetTicket2CodeDir)) {
    New-Item -ItemType Directory -Force -Path $TargetTicket2CodeDir | Out-Null
}
Copy-Item -Path (Join-Path $Ticket2CodeDir "*") -Destination $TargetTicket2CodeDir -Recurse -Force

# 5. Handle .env.local
$EnvFile = Join-Path $TargetDir ".env.local"
$ExampleEnv = Join-Path $RootDir "ticket2code\ticket\env.local.example"

if (Test-Path $EnvFile) {
    Write-Host "[!] .env.local already exists in target directory." -ForegroundColor Yellow
    Write-Host "[->] Please verify that JIRA_TOKEN, JIRA_EMAIL, and JIRA_URL are defined in your .env.local."
} else {
    if (Test-Path $ExampleEnv) {
        Write-Host "[*] Creating .env.local from example..."
        Copy-Item $ExampleEnv -Destination $EnvFile -Force
        Write-Host "[+] Created .env.local successfully. Please fill in your JIRA credentials."
    } else {
        Write-Host "[*] Creating skeleton .env.local..."
        $content = @"
JIRA_TOKEN=your_token_here
JIRA_EMAIL=your_atlassian_email@company.com
JIRA_URL=your_jira_base_url
"@
        Set-Content -Path $EnvFile -Value $content
        Write-Host "[+] Created .env.local successfully. Please fill in your JIRA credentials."
    }
}

# 6. Verify and warn about missing rule files in target docs/ directory
$TargetDocsDir = Join-Path $TargetDir "docs"
if (!(Test-Path $TargetDocsDir)) {
    Write-Host "[!] Warning: Thu muc 'docs/' chua ton tai trong du an dich cua ban." -ForegroundColor Yellow
    Write-Host "[->] De agent hoat dong chinh xac nhat, ban nen tao thu muc 'docs/'
