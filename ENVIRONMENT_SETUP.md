# Environment Setup Guide

## Vercel Projects

### Staging Environment
1. Create a new project on Vercel
2. Connect it to the repository
3. Configure deployment to use the `develop` branch
4. Add relevant environment variables for staging
5. Set the project name with a `-staging` suffix

### Production Environment
1. Create a new project on Vercel 
2. Connect it to the repository
3. Configure deployment to use the `main` branch
4. Add production environment variables
5. Set the project name without any suffix

## Supabase Projects

### Staging Database
1. Create a separate Supabase project for staging
2. Name the project with a `-staging` suffix
3. Configure database schema and tables
4. Set up appropriate access policies for testing
5. Connect the staging Vercel project to this database

### Production Database
1. Create a Supabase project for production
2. Configure database with the same schema as staging
3. Set up stricter access policies for production
4. Connect the production Vercel project to this database

## Environment Variables
Ensure each Vercel project has the appropriate environment variables:

### Staging
```
NEXT_PUBLIC_SUPABASE_URL=<staging-supabase-url>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<staging-supabase-anon-key>
ENVIRONMENT=staging
```

### Production
```
NEXT_PUBLIC_SUPABASE_URL=<production-supabase-url>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<production-supabase-anon-key>
ENVIRONMENT=production
```

## Deployment Workflow
1. Changes pushed to feature branches are not automatically deployed
2. Changes merged to `develop` automatically deploy to staging
3. Changes merged to `main` automatically deploy to production 