# TheCleanBot

A cleaning service management application with user and admin interfaces.

## Branch Structure
- `main` - Production branch with stable, tested code
- `develop` - Primary development branch
- Feature branches follow the pattern: `feat/feature-name`

## Environments
- **Staging**: Deployed from the `develop` branch
- **Production**: Deployed from the `main` branch

## Development Workflow
1. Create feature branches from `develop`
2. Submit PRs to merge completed features into `develop`
3. Test thoroughly in staging environment
4. Periodically merge `develop` into `main` for production releases

## Development Notes

- Force redeployment: 2025-03-17 