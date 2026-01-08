# Deployment Checklist

## Environment Configuration

- [ ] Production .env files configured
- [ ] BETTER_AUTH_SECRET set (32+ chars, production value)
- [ ] DATABASE_URL points to Neon production database
- [ ] CORS_ORIGINS set to production frontend URL
- [ ] DEBUG=False in production backend
- [ ] NODE_ENV=production in frontend
- [ ] All secrets stored securely (not in code)

## Database Setup

- [ ] Neon PostgreSQL database created
- [ ] Database migrations run (alembic upgrade head)
- [ ] Database backups configured
- [ ] Database connection pooling verified
- [ ] SSL/TLS enabled for database connections

## Backend Deployment (Railway/Render)

- [ ] GitHub repository connected
- [ ] Build succeeds
- [ ] Environment variables configured
- [ ] Health check endpoint accessible
- [ ] HTTPS enforced
- [ ] Logs accessible and monitored
- [ ] Auto-deploy on git push configured

## Frontend Deployment (Vercel)

- [ ] GitHub repository connected
- [ ] Build succeeds
- [ ] Environment variables configured
- [ ] NEXT_PUBLIC_API_URL points to backend
- [ ] Custom domain configured (if applicable)
- [ ] HTTPS enforced
- [ ] Preview deployments working

## Post-Deployment Verification

- [ ] Frontend loads successfully
- [ ] Backend health check returns 200
- [ ] User can sign up
- [ ] User can sign in
- [ ] User can create task
- [ ] User can view tasks
- [ ] User can edit task
- [ ] User can delete task
- [ ] User can sign out
- [ ] All API endpoints working

## Monitoring & Alerts

- [ ] Uptime monitoring configured
- [ ] Error tracking enabled (Sentry/similar)
- [ ] Performance monitoring active
- [ ] Database performance tracked
- [ ] Alerts for downtime configured
- [ ] Logs aggregated and searchable

## Documentation

- [ ] README updated with deployment URLs
- [ ] Environment setup documented
- [ ] Deployment process documented
- [ ] Troubleshooting guide created
- [ ] API documentation accessible
- [ ] User guide available

## Security in Production

- [ ] HTTPS enforced (frontend and backend)
- [ ] Security headers configured
- [ ] CORS restricted to production domains
- [ ] Rate limiting enabled
- [ ] No debug info exposed
- [ ] Error messages sanitized
- [ ] Database credentials secure
