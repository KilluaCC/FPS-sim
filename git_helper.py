#!/usr/bin/env python3
"""
Git Helper Script - Makes Git operations easier
"""

import os
import sys
import subprocess
import json
from datetime import datetime

class GitHelper:
    def __init__(self):
        self.repo_path = os.getcwd()
        
    def run_command(self, command):
        """Run a git command and return the result"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self.repo_path)
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def get_status(self):
        """Get current git status"""
        success, output, error = self.run_command("git status --porcelain")
        if success:
            return output.strip().split('\n') if output.strip() else []
        return []
    
    def get_branch(self):
        """Get current branch name"""
        success, output, error = self.run_command("git branch --show-current")
        if success:
            return output.strip()
        return "unknown"
    
    def get_last_commit(self):
        """Get last commit message"""
        success, output, error = self.run_command("git log -1 --pretty=format:%s")
        if success:
            return output.strip()
        return "No commits found"
    
    def show_menu(self):
        """Show the main menu"""
        print("\n🚀 Git Helper - Easy Git Operations")
        print("=" * 40)
        print("1. 📊 Show current status")
        print("2. 💾 Quick commit (all changes)")
        print("3. 📝 Smart commit (with prompts)")
        print("4. 📤 Push to remote")
        print("5. 🔄 Pull from remote")
        print("6. 🌿 Show branch info")
        print("7. 📋 Show recent commits")
        print("8. 🚪 Exit")
        print("=" * 40)
        
        choice = input("Choose an option (1-8): ").strip()
        return choice
    
    def quick_commit(self):
        """Quick commit all changes"""
        print("\n💾 Quick Commit Mode")
        print("-" * 20)
        
        # Show what will be committed
        changes = self.get_status()
        if not changes:
            print("✅ No changes to commit!")
            return
        
        print("📋 Changes to be committed:")
        for change in changes:
            if change:
                print(f"   {change}")
        
        # Get commit message
        commit_msg = input("\n📝 Enter commit message: ").strip()
        if not commit_msg:
            print("❌ Commit message cannot be empty!")
            return
        
        # Add all changes
        print("\n📦 Adding all changes...")
        success, output, error = self.run_command("git add .")
        if not success:
            print(f"❌ Error adding files: {error}")
            return
        
        # Commit
        print("💾 Committing...")
        success, output, error = self.run_command(f'git commit -m "{commit_msg}"')
        if not success:
            print(f"❌ Error committing: {error}")
            return
        
        print("✅ Commit successful!")
        
        # Ask if user wants to push
        push_choice = input("\n📤 Push to remote? (y/n): ").strip().lower()
        if push_choice in ['y', 'yes']:
            self.push_to_remote()
    
    def smart_commit(self):
        """Smart commit with guided prompts"""
        print("\n🧠 Smart Commit Mode")
        print("-" * 20)
        
        # Show current status
        changes = self.get_status()
        if not changes:
            print("✅ No changes to commit!")
            return
        
        print("📋 Changes detected:")
        for i, change in enumerate(changes, 1):
            if change:
                print(f"   {i}. {change}")
        
        # Categorize changes
        print("\n📝 What type of change is this?")
        print("1. 🐛 Bug fix")
        print("2. ✨ New feature")
        print("3. 🔧 Improvement/Refactor")
        print("4. 📚 Documentation")
        print("5. 🧪 Test")
        print("6. 🚀 Performance")
        print("7. 🎨 UI/UX")
        print("8. 🔒 Security")
        print("9. 📦 Dependencies")
        print("10. 🧹 Cleanup")
        
        change_type = input("Choose type (1-10): ").strip()
        
        # Get description
        description = input("\n📝 Describe what you changed: ").strip()
        
        # Build commit message
        type_emojis = {
            "1": "🐛", "2": "✨", "3": "🔧", "4": "📚", "5": "🧪",
            "6": "🚀", "7": "🎨", "8": "🔒", "9": "📦", "10": "🧹"
        }
        
        emoji = type_emojis.get(change_type, "📝")
        commit_msg = f"{emoji} {description}"
        
        print(f"\n📝 Commit message will be: {commit_msg}")
        confirm = input("Proceed? (y/n): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            # Add all changes
            print("\n📦 Adding all changes...")
            success, output, error = self.run_command("git add .")
            if not success:
                print(f"❌ Error adding files: {error}")
                return
            
            # Commit
            print("💾 Committing...")
            success, output, error = self.run_command(f'git commit -m "{commit_msg}"')
            if not success:
                print(f"❌ Error committing: {error}")
                return
            
            print("✅ Commit successful!")
            
            # Ask if user wants to push
            push_choice = input("\n📤 Push to remote? (y/n): ").strip().lower()
            if push_choice in ['y', 'yes']:
                self.push_to_remote()
    
    def push_to_remote(self):
        """Push to remote repository"""
        print("\n📤 Pushing to remote...")
        success, output, error = self.run_command("git push")
        if success:
            print("✅ Push successful!")
        else:
            print(f"❌ Push failed: {error}")
    
    def pull_from_remote(self):
        """Pull from remote repository"""
        print("\n🔄 Pulling from remote...")
        success, output, error = self.run_command("git pull")
        if success:
            print("✅ Pull successful!")
        else:
            print(f"❌ Pull failed: {error}")
    
    def show_branch_info(self):
        """Show current branch information"""
        print("\n🌿 Branch Information")
        print("-" * 20)
        
        current_branch = self.get_branch()
        print(f"Current branch: {current_branch}")
        
        # Show remote branches
        success, output, error = self.run_command("git branch -r")
        if success:
            print("\nRemote branches:")
            for branch in output.strip().split('\n'):
                if branch:
                    print(f"   {branch}")
    
    def show_recent_commits(self):
        """Show recent commits"""
        print("\n📋 Recent Commits")
        print("-" * 20)
        
        success, output, error = self.run_command("git log --oneline -10")
        if success:
            for line in output.strip().split('\n'):
                if line:
                    print(f"   {line}")
        else:
            print(f"❌ Error getting commits: {error}")
    
    def run(self):
        """Main loop"""
        while True:
            choice = self.show_menu()
            
            if choice == "1":
                changes = self.get_status()
                if changes:
                    print("\n📊 Current Status:")
                    for change in changes:
                        if change:
                            print(f"   {change}")
                else:
                    print("\n✅ Working directory is clean!")
                    
            elif choice == "2":
                self.quick_commit()
                
            elif choice == "3":
                self.smart_commit()
                
            elif choice == "4":
                self.push_to_remote()
                
            elif choice == "5":
                self.pull_from_remote()
                
            elif choice == "6":
                self.show_branch_info()
                
            elif choice == "7":
                self.show_recent_commits()
                
            elif choice == "8":
                print("\n👋 Goodbye!")
                break
                
            else:
                print("\n❌ Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    helper = GitHelper()
    helper.run()
