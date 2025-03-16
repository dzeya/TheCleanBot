# Cursor Guidelines

This document provides best practices for using Cursor IDE with our Git workflow, especially when using "YOLO" mode.

## What is "YOLO" Mode?

Cursor's "YOLO" mode allows quick AI-generated changes to be implemented without manual review of every line. While powerful, it requires caution to maintain code quality and repository integrity.

## Best Practices

### Branch Management

1. **Always check your current branch**
   - Before using YOLO mode, verify you're on the correct branch
   - In Cursor's status bar, confirm the branch name is visible and correct
   - Use `git status` in the terminal to double-check

2. **Never use YOLO directly on main**
   - Always work on feature branches or develop
   - Create a new branch if you're not already on one

3. **Set up branch protection rules**
   - Configure GitHub to prevent direct pushes to main
   - Require pull requests for all changes to protected branches

### Code Organization

1. **Keep YOLO changes focused**
   - Limit YOLO commands to a single feature or fix
   - Break complex changes into multiple smaller ones
   - Commit frequently to make changes easier to review or revert

2. **Include tests in your prompts**
   - When asking Cursor to implement features, request tests too
   - Run tests locally before pushing changes

### Commit and Push Strategy

1. **Review before pushing**
   - Use `git diff` to review changes before committing
   - Check Cursor's "Changes" panel to see what will be committed

2. **Use descriptive commit messages**
   - Follow the Conventional Commits format
   - Mention if changes were AI-assisted

3. **Push to feature branches first**
   - Always push to your feature branch, not directly to develop
   - Create a PR to merge the changes after review

## Recovery Options

1. **If YOLO makes unwanted changes:**
   - Use `git reset --hard HEAD` to discard all uncommitted changes
   - Or use `git checkout -- <file>` to discard changes in specific files

2. **If unwanted changes were committed:**
   - Use `git revert <commit>` to create a new commit that undoes changes
   - Avoid using `git reset --hard` on already pushed commits

3. **If unwanted changes were pushed:**
   - Create a new PR to fix the issues
   - Communicate with the team about the situation 