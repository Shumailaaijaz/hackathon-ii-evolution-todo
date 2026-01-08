# Security Checklist

## Authentication & Authorization

- [ ] JWT tokens use BETTER_AUTH_SECRET (min 32 characters)
- [ ] JWT tokens have expiration (7 days default)
- [ ] JWT signature verification works correctly
- [ ] Invalid/expired tokens return 401 Unauthorized
- [ ] Missing tokens return 401 Unauthorized
- [ ] All protected endpoints require valid JWT
- [ ] User ID extracted from JWT, not URL parameters

## User Isolation

- [ ] Users can only access their own tasks
- [ ] GET /api/{user_id}/tasks filters by authenticated user
- [ ] POST /api/{user_id}/tasks sets user_id from JWT
- [ ] PUT/PATCH/DELETE verify task ownership (403 if not owner)
- [ ] Database queries always filter by user_id
- [ ] No cross-user data leakage possible

## Password Security

- [ ] Passwords hashed with bcrypt (Better Auth handles this)
- [ ] Password hashing uses work factor ≥10
- [ ] Plaintext passwords never stored
- [ ] Passwords never logged or exposed in errors
- [ ] Password strength requirements enforced (min 8 chars)

## API Security

- [ ] CORS configured with specific origins (not *)
- [ ] HTTPS enforced in production
- [ ] SQL injection prevented (parameterized queries)
- [ ] XSS prevented (input sanitization)
- [ ] CSRF protection enabled
- [ ] Rate limiting configured
- [ ] Error messages don't leak sensitive info

## Data Protection

- [ ] .env files in .gitignore
- [ ] No secrets in code or commits
- [ ] DATABASE_URL uses SSL (sslmode=require)
- [ ] Environment variables validated on startup
- [ ] Sensitive data not logged

## Frontend Security

- [ ] JWT tokens stored in httpOnly cookies (if using cookies)
- [ ] No sensitive data in localStorage
- [ ] API calls use Authorization header
- [ ] Client-side validation + server-side validation
- [ ] User input sanitized before display
