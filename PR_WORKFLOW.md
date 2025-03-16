# Pull Request Workflow

This document outlines the recommended workflow for contributing code to TheCleanBot project.

## Feature Development

1. **Start from the develop branch**
   ```bash
   git checkout develop
   git pull origin develop
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```
   Use appropriate prefixes for different types of work:
   - `feat/` - for new features
   - `fix/` - for bug fixes
   - `docs/` - for documentation changes
   - `chore/` - for maintenance tasks

3. **Work on your feature**
   - Make regular commits with descriptive messages
   - Follow the [Conventional Commits](https://www.conventionalcommits.org/) format
   - Keep changes focused on a single task/feature

4. **Push your branch to remote**
   ```bash
   git push origin feat/your-feature-name
   ```

## Creating a Pull Request

1. **Create a PR from your feature branch to develop**
   - Go to GitHub and create a new Pull Request
   - Set the base branch to `develop`
   - Set the compare branch to your feature branch
   
2. **Fill out the PR template with:**
   - Description of changes
   - Related issue number(s)
   - Screenshots or videos (if UI changes)
   - Testing steps

3. **Request reviews** from at least one team member

## Review Process

1. **Automated checks**
   - Wait for CI tests to pass
   - Address any linting or test failures

2. **Code review**
   - Respond to reviewer comments
   - Make requested changes
   - Request re-review when changes are complete

3. **Approval and merge**
   - PR requires at least one approval
   - Use "Squash and merge" option when merging to develop
   - Delete the feature branch after merging

## Production Release

1. **Create a release PR**
   - When ready to release to production, create a new PR from `develop` to `main`
   - Title the PR "Release vX.Y.Z" following semantic versioning
   
2. **Review the release PR**
   - Ensure all changes have been tested in staging
   - Get approval from product owner

3. **Merge to main**
   - Use "Create a merge commit" option for the release PR
   - Vercel will automatically deploy to production

4. **Create a release tag**
   - Create and push a new version tag after the merge
   ```bash
   git checkout main
   git pull origin main
   git tag v1.0.0
   git push origin v1.0.0
   ``` 