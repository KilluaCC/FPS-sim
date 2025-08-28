.PHONY: help status commit push pull sync branch recent quick undo

help:
	@echo "🚀 Git Operations Makefile"
	@echo "=========================="
	@echo ""
	@echo "📊 Available commands:"
	@echo "  make status    - Show Git status"
	@echo "  make commit    - Add, commit with timestamp"
	@echo "  make push      - Push to remote"
	@echo "  make pull      - Pull from remote"
	@echo "  make sync      - Pull then push"
	@echo "  make branch    - Show current branch"
	@echo "  make recent    - Show recent commits"
	@echo "  make quick     - Quick commit and push"
	@echo "  make undo      - Undo last commit"
	@echo ""
	@echo "💡 Quick workflow: make quick"

status:
	@echo "📊 Git Status:"
	@git status --short

commit:
	@echo "💾 Committing changes..."
	@git add .
	@git commit -m "Update $(shell date +%Y-%m-%d_%H:%M:%S)"
	@echo "✅ Commit successful!"

push:
	@echo "🚀 Pushing to remote..."
	@git push
	@echo "✅ Push successful!"

pull:
	@echo "📥 Pulling from remote..."
	@git pull
	@echo "✅ Pull successful!"

sync:
	@echo "🔄 Syncing with remote..."
	@make pull
	@make push

branch:
	@echo "🌿 Current branch:"
	@git branch --show-current

recent:
	@echo "📝 Recent commits:"
	@git log --oneline -10

quick:
	@echo "⚡ Quick commit and push..."
	@make commit
	@make push

undo:
	@echo "↩️  Undoing last commit..."
	@git reset --soft HEAD~1
	@echo "✅ Last commit undone (changes still staged)"
