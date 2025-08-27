# Git Operations Makefile
# Usage: make <command>

.PHONY: help status commit push pull sync branch

help:
	@echo "🚀 Git Operations Makefile"
	@echo "=========================="
	@echo "make status    - Show git status"
	@echo "make commit    - Add all changes and commit"
	@echo "make push      - Push to remote"
	@echo "make pull      - Pull from remote"
	@echo "make sync      - Fetch and pull from remote"
	@echo "make branch    - Show current branch"
	@echo "make recent    - Show recent commits"
	@echo "make quick     - Quick commit and push"
	@echo "make undo      - Undo last commit (keep changes)"

status:
	@echo "📊 Git Status:"
	@git status --short

commit:
	@echo "💾 Committing changes..."
	@git add .
	@git commit -m "Update $(shell date +%Y-%m-%d_%H:%M:%S)"
	@echo "✅ Commit successful!"

push:
	@echo "📤 Pushing to remote..."
	@git push
	@echo "✅ Push successful!"

pull:
	@echo "🔄 Pulling from remote..."
	@git pull
	@echo "✅ Pull successful!"

sync:
	@echo "🔄 Syncing with remote..."
	@git fetch
	@git pull
	@echo "✅ Sync successful!"

branch:
	@echo "🌿 Current branch: $(shell git branch --show-current)"

recent:
	@echo "📋 Recent commits:"
	@git log --oneline -10

quick:
	@echo "⚡ Quick commit and push..."
	@make commit
	@make push

undo:
	@echo "↩️  Undoing last commit (keeping changes)..."
	@git reset --soft HEAD~1
	@echo "✅ Last commit undone. Changes are staged and ready to commit again."
