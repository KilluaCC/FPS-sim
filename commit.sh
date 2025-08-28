#!/bin/bash

# Quick Git commit and push script
# Usage: ./commit.sh "Your commit message"

if [ -z "$1" ]; then
    echo "❌ Error: Please provide a commit message"
    echo "Usage: ./commit.sh \"Your commit message\""
    exit 1
fi

COMMIT_MSG="$1"

echo "🚀 Quick Git Commit & Push"
echo "=========================="
echo "📝 Commit message: $COMMIT_MSG"
echo ""

# Show current status
echo "📊 Current status:"
git status --short
echo ""

# Add all changes
echo "➕ Adding all changes..."
git add .
echo "✅ Added all changes"
echo ""

# Commit with message
echo "💾 Committing changes..."
git commit -m "$COMMIT_MSG"
echo "✅ Commit successful!"
echo ""

# Push to remote
echo "🚀 Pushing to remote..."
git push
echo "✅ Push successful!"
echo ""

echo "🎉 All done! Changes committed and pushed."
