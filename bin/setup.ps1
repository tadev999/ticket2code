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

Write-Host "🚀 Starting ticket2code automated setup..."
Write-Host "📂 Source root: $RootDir"
Write-Host "🎯 Target directory: $TargetDir"

# 1. Verify source directory contains required assets
$Ticket2CodeDir = Join-Path $RootDir "ticket2code"
$PromptFile = Join-Path $RootDir "ticket2code\ticket\ticket.prompt.md"

if (!(Test-Path $Ticket2CodeDir) -or !(Test-Path $PromptFile)) {
    Write-Host "❌ Error: Required template files not found in $RootDir." -ForegroundColor Red
    Exit 1
}

# 2. Create target directories if they don't exist
Write-Host "📁 Creating directories in target project..."
$TargetPromptDir = Join-Path $TargetDir ".github\prompts"
if (!(Test-Path $TargetPromptDir)) {
    New-Item -ItemType Directory -Force -Path $TargetPromptDir | Out-Null
}

# 3. Copy ticket.prompt.md to target project
Write-Host "📄 Copying ticket.prompt.md to .github/prompts/..."
Copy-Item $PromptFile -Destination $TargetPromptDir -Force

# 4. Copy ticket2code folder to target project
Write-Host "📦 Copying ticket2code folder..."
$TargetTicket2CodeDir = Join-Path $TargetDir "ticket2code"
if (!(Test-Path $TargetTicket2CodeDir)) {
    New-Item -ItemType Directory -Force -Path $TargetTicket2CodeDir | Out-Null
}
Copy-Item -Path (Join-Path $Ticket2CodeDir "*") -Destination $TargetTicket2CodeDir -Recurse -Force

# 5. Handle .env.local
$EnvFile = Join-Path $TargetDir ".env.local"
$ExampleEnv = Join-Path $RootDir "ticket2code\ticket\env.local.example"

if (Test-Path $EnvFile) {
    Write-Host "⚠️  .env.local already exists in target directory." -ForegroundColor Yellow
    Write-Host "👉 Please verify that JIRA_TOKEN, JIRA_EMAIL, and JIRA_URL are defined in your .env.local."
} else {
    if (Test-Path $ExampleEnv) {
        Write-Host "📝 Creating .env.local from example..."
        Copy-Item $ExampleEnv -Destination $EnvFile -Force
        Write-Host "💡 Created .env.local successfully. Please fill in your JIRA credentials."
    } else {
        Write-Host "📝 Creating skeleton .env.local..."
        $content = @"
JIRA_TOKEN=your_token_here
JIRA_EMAIL=your_atlassian_email@company.com
JIRA_URL=your_jira_base_url
"@
        Set-Content -Path $EnvFile -Value $content
        Write-Host "💡 Created .env.local successfully. Please fill in your JIRA credentials."
    }
}

# 6. Verify and warn about missing rule files in target docs/ directory
$TargetDocsDir = Join-Path $TargetDir "docs"
if (!(Test-Path $TargetDocsDir)) {
    Write-Host "⚠️  Warning: Thư mục 'docs/' chưa tồn tại trong dự án đích của bạn." -ForegroundColor Yellow
    Write-Host "👉 Để agent hoạt động chính xác nhất, bạn nên tạo thư mục 'docs/' ở thư mục gốc"
    Write-Host "   và bổ sung các file quy chuẩn như: coding_style.md, logging_policy.md, test_rules.md, review_guideline.md."
} else {
    $CommonRules = @("coding_style.md", "logging_policy.md", "test_rules.md", "review_guideline.md")
    $MissingRules = @()
    foreach ($rule in $CommonRules) {
        $rulePath = Join-Path $TargetDocsDir $rule
        if (!(Test-Path $rulePath)) {
            $MissingRules += $rule
        }
    }
    if ($MissingRules.Count -gt 0) {
        Write-Host "⚠️  Warning: Dự án của bạn thiếu một số file quy chuẩn trong thư mục 'docs/':" -ForegroundColor Yellow
        foreach ($rule in $MissingRules) {
            Write-Host "   - $rule"
        }
        Write-Host "👉 Hãy bổ sung các file này để cung cấp ngữ cảnh tốt nhất cho agent khi chạy /ticket."
    }
}

# 7. Add .env.local to target's .gitignore if it exists and doesn't contain it
$Gitignore = Join-Path $TargetDir ".gitignore"
if (Test-Path $Gitignore) {
    $gitignoreContent = Get-Content $Gitignore
    if ($gitignoreContent -notcontains ".env.local") {
        Add-Content -Path $Gitignore -Value "`n# ticket2code local environment variables`n.env.local"
        Write-Host "🔒 Added .env.local to target .gitignore"
    }
}

Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
Write-Host "🎉 You can now use the /ticket command in Copilot Chat within the target project."
Write-Host "👉 Remember to fill in the credentials in: $EnvFile"
