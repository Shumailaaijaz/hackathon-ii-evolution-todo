# Environment Variables for Railway Deployment

To deploy your FastAPI backend on Railway, you'll need to configure the following environment variables:

## Required Variables

### Database Configuration
```
DATABASE_URL=postgresql://username:password@railway-postgres.internal:5432/mydb
```
This will be automatically set by Railway when you connect a PostgreSQL addon.

### Authentication & Security
```
BETTER_AUTH_SECRET=your-super-secret-key-at-least-32-characters-long
```
**Important**: Generate a secure secret with at least 32 characters. You can use:
```bash
openssl rand -base64 32
```

### Application Configuration
```
ENVIRONMENT=production
DEBUG=False
CORS_ORIGINS=https://your-frontend-url.onrender.com,https://yourdomain.com
```

## Optional Variables

### JWT Configuration
```
JWT_ALGORITHM=HS256
JWT_EXPIRE_DAYS=7
```

### Logging
```
LOG_LEVEL=INFO
```

## Railway-Specific Configuration

Railway automatically provides:
- `$PORT` - The port your application should bind to
- Database connection details when using Railway's PostgreSQL addon

## Setting Up PostgreSQL with Railway

1. In your Railway dashboard:
   - Go to your project
   - Click on "+ Add" → "PostgreSQL" (or "Database")
   - Railway will provision a PostgreSQL database
   - The `DATABASE_URL` environment variable will be automatically added to your project

2. The `DATABASE_URL` will follow this format:
   ```
   postgresql://username:password@railway-postgres.internal:5432/mydb
   ```

## Setup Instructions

1. Generate a secure `BETTER_AUTH_SECRET`:
   ```bash
   openssl rand -base64 32
   ```

2. In your Railway dashboard:
   - Go to your project
   - Navigate to "Settings" → "Environment Variables"
   - Add the variables listed above (except DATABASE_URL which will be auto-generated)

3. For CORS, include your frontend domain(s) in the `CORS_ORIGINS` variable, comma-separated.

4. Deploy your application using one of these methods:
   - Connect your GitHub repository to Railway for automatic deployments
   - Use the Railway CLI: `railway up`

5. Your application will be accessible at your Railway-provided URL or custom domain.