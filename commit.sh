#!/bin/bash

# Simple Git Commit Automation Script
# Usage: ./commit.sh "your commit message"

echo "🚀 Git Commit Automation Script"
echo "================================"

# Check if commit message was provided
if [ -z "$1" ]; then
    echo "❌ Please provide a commit message!"
    echo "Usage: ./commit.sh \"your commit message\""
    exit 1
fi

COMMIT_MSG="$1"

echo "📝 Commit message: $COMMIT_MSG"
echo ""

# Check git status
echo "🔍 Checking git status..."
git status --short

echo ""
echo "📦 Adding all changes..."
git add .

echo ""
echo "💾 Committing with message: '$COMMIT_MSG'"
git commit -m "$COMMIT_MSG"

echo ""
echo "📤 Pushing to remote..."
git push

echo ""
echo "✅ Done! Your changes are now committed and pushed."
echo "🌐 Check your repository: https://github.com/KilluaCC/FPS-sim"
