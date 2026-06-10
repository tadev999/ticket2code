#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Resolve the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# Root of the ticket2code project (one level up from bin/)
ROOT_DIR="$( cd "$SCRIPT_DIR/.." >/dev/null 2>&1 && pwd )"

# Target directory defaults to the current working directory if not specified
TARGET_DIR="${1:-.}"

# Normalize backslashes to forward slashes (helps with Windows paths in Git Bash)
TARGET_DIR="${TARGET_DIR//\\//}"

# Create target directory if it does not exist
mkdir -p "$TARGET_DIR"

# Resolve target directory to absolute path
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

echo "🚀 Starting ticket2code automated setup..."
echo "📂 Source root: $ROOT_DIR"
echo "🎯 Target directory: $TARGET_DIR"

# 1. Verify source directory contains required assets
TICKET_PROMPT_SRC="$ROOT_DIR/ticket2code/ticket/ticket.prompt.md"
if [ ! -d "$ROOT_DIR/ticket2code" ] || [ ! -f "$TICKET_PROMPT_SRC" ]; then
  echo "❌ Error: Required template files not found in $ROOT_DIR."
  echo "Make sure the script is located in the bin/ directory of ticket2code."
  exit 1
fi

# 2. Create target directories if they don't exist
echo "📁 Creating directories in target project..."
mkdir -p "$TARGET_DIR/.github/prompts"

# 3. Copy ticket.prompt.md to target project
echo "📄 Copying ticket.prompt.md to .github/prompts/..."
cp "$TICKET_PROMPT_SRC" "$TARGET_DIR/.github/prompts/ticket.prompt.md"

# 4. Copy ticket2code folder to target project
echo "📦 Copying ticket2code folder..."
mkdir -p "$TARGET_DIR/ticket2code"
# Copy recursive, preserving directory structure under ticket2code/
cp -R "$ROOT_DIR/ticket2code/" "$TARGET_DIR/ticket2code/"

# 5. Handle .env.local
ENV_FILE="$TARGET_DIR/.env.local"
EXAMPLE_ENV="$ROOT_DIR/ticket2code/ticket/env.local.example"

if [ -f "$ENV_FILE" ]; then
  echo "⚠️  .env.local already exists in target directory."
  echo "👉 Please verify JIRA_TOKEN, JIRA_EMAIL, and JIRA_URL are defined in your .env.local."
else
  if [ -f "$EXAMPLE_ENV" ]; then
    echo "📝 Creating .env.local from example..."
    cp "$EXAMPLE_ENV" "$ENV_FILE"
    echo "💡 Created .env.local successfully. Please fill in your JIRA credentials."
  else
    echo "📝 Creating skeleton .env.local..."
    cat <<EOT >> "$ENV_FILE"
JIRA_TOKEN=your_token_here
JIRA_EMAIL=your_atlassian_email@company.com
JIRA_URL=your_jira_base_url
EOT
    echo "💡 Created .env.local successfully. Please fill in your JIRA credentials."
  fi
fi

# 6. Verify and warn about missing rule files in target docs/ directory
TARGET_DOCS="$TARGET_DIR/docs"
if [ ! -d "$TARGET_DOCS" ]; then
  echo "⚠️  Warning: Thư mục 'docs/' chưa tồn tại trong dự án đích của bạn."
  echo "👉 Để agent hoạt động chính xác nhất, bạn nên tạo thư mục 'docs/' ở thư mục gốc"
  echo "   và bổ sung các file quy chuẩn như: coding_style.md, logging_policy.md, test_rules.md, review_guideline.md."
else
  # Check for common rule files
  MISSING_RULES=()
  for rule_file in coding_style.md logging_policy.md test_rules.md review_guideline.md; do
    if [ ! -f "$TARGET_DOCS/$rule_file" ]; then
      MISSING_RULES+=("$rule_file")
    fi
  done
  if [ ${#MISSING_RULES[@]} -ne 0 ]; then
    echo "⚠️  Warning: Dự án của bạn thiếu một số file quy chuẩn trong thư mục 'docs/':"
    for rule in "${MISSING_RULES[@]}"; do
      echo "   - $rule"
    done
    echo "👉 Hãy bổ sung các file này để cung cấp ngữ cảnh tốt nhất cho agent khi chạy /ticket."
  fi
fi

# 7. Add .env.local to target's .gitignore if it exists and doesn't contain it
GITIGNORE="$TARGET_DIR/.gitignore"
if [ -f "$GITIGNORE" ]; then
  if ! grep -q ".env.local" "$GITIGNORE"; then
    echo "" >> "$GITIGNORE"
    echo "# ticket2code local environment variables" >> "$GITIGNORE"
    echo ".env.local" >> "$GITIGNORE"
    echo "🔒 Added .env.local to target .gitignore"
  fi
fi

echo "✅ Setup completed successfully!"
echo "🎉 You can now use the /ticket command in Copilot Chat within the target project."
echo "👉 Remember to fill in the credentials in: $TARGET_DIR/.env.local"
