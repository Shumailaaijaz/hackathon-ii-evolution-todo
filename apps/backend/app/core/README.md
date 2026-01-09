# Core Configuration Module

This module contains the core configuration and settings for the FastAPI backend application.

## Files

### `config.py`

Pydantic-based settings management with environment variable validation.

**Features:**
- ✅ Type-safe configuration with Pydantic
- ✅ Environment variable loading from `.env` file
- ✅ Validation on startup (fail-fast approach)
- ✅ Secure secret length validation (min 32 chars)
- ✅ Database URL format validation
- ✅ CORS origins parsing (comma-separated)
- ✅ Environment detection helpers
- ✅ Logging configuration
- ✅ Safe string representation (hides sensitive data)

**Usage:**

```python
from app.core.config import settings

# Access settings
print(settings.DATABASE_URL)
print(settings.CORS_ORIGINS)

# Environment checks
if settings.is_production:
    # Production-specific logic
    pass

if settings.is_development:
    # Development-specific logic
    pass

# CORS origins as list
allowed_origins = settings.cors_origins_list

# Database host extraction
print(f"Connecting to: {settings.database_host}")
```

### `database.py`

Database connection and session management with SQLModel and SQLAlchemy.

**Features:**
- ✅ Connection pooling optimized for Neon PostgreSQL
- ✅ SSL/TLS encryption (required by Neon)
- ✅ Connection pre-ping for serverless resilience
- ✅ Automatic connection recycling
- ✅ Health checks
- ✅ FastAPI dependency injection
- ✅ Context managers for non-FastAPI usage

**Usage:**

```python
from app.core.database import get_session, check_database_health
from fastapi import Depends
from sqlmodel import Session

# In FastAPI routes
@app.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
    tasks = session.query(Task).all()
    return tasks

# In CLI scripts or background tasks
from app.core.database import get_session_context

with get_session_context() as session:
    task = Task(title="New task")
    session.add(task)
    session.commit()

# Health checks
if check_database_health():
    print("Database is healthy")
```

## Environment Variables

All configuration is loaded from environment variables. See `../../.env.example` for the complete list of available settings.

### Required Variables

```bash
DATABASE_URL=postgresql://user:pass@host.neon.tech/db?sslmode=require
BETTER_AUTH_SECRET=your-32-char-minimum-secret-key
```

### Optional Variables (with defaults)

```bash
JWT_ALGORITHM=HS256
JWT_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
```

## Configuration Validation

The application validates all configuration on startup:

1. **DATABASE_URL**: Must start with `postgresql://`
2. **BETTER_AUTH_SECRET**: Must be at least 32 characters
3. **CORS_ORIGINS**: Parsed and validated as comma-separated URLs

If validation fails, the application will **not start** and will display a clear error message.

## Logging

Logging is configured based on the environment:

- **Development**: Detailed logs with file names and line numbers
- **Production**: Standard logs without debug information
- **Log Level**: Controlled by `LOG_LEVEL` environment variable

```python
# Get logging configuration
logging_config = settings.get_logging_config()
logging.config.dictConfig(logging_config)
```

## Security Best Practices

1. **Never commit `.env` to version control** - It's in `.gitignore`
2. **Use strong secrets** - Minimum 32 characters, randomly generated
3. **Rotate secrets regularly** - Especially in production
4. **Use environment-specific configs** - Different secrets for dev/staging/prod
5. **Validate at startup** - Fail fast if configuration is invalid

## Generating Secrets

```bash
# Generate a secure secret
openssl rand -base64 32

# Example output:
# 87232f7daccc57a954ad0aae536a7902986ec437bed64a40a8ad11c7f87d07ce
```

## CORS Configuration

CORS origins can be configured as:

**Single origin:**
```bash
CORS_ORIGINS=http://localhost:3000
```

**Multiple origins (comma-separated):**
```bash
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app,https://staging.your-app.com
```

The configuration will automatically parse and validate all origins.

## Neon PostgreSQL Optimization

The database configuration is optimized for Neon's serverless PostgreSQL:

- **Connection pooling**: Adjusted based on pooler usage
- **Pre-ping enabled**: Tests connections before use
- **Connection recycling**: Prevents stale connections
- **SSL required**: Enforced for all connections
- **Timeouts configured**: Statement and connection timeouts

## Troubleshooting

### Configuration Validation Errors

If you see validation errors on startup:

```
ValueError: BETTER_AUTH_SECRET must be at least 32 characters
```

**Solution**: Generate a new secret with `openssl rand -base64 32`

### Database Connection Errors

```
ValueError: DATABASE_URL must start with 'postgresql://'
```

**Solution**: Check your database URL format in `.env`

### CORS Errors in Browser

```
CORS policy: No 'Access-Control-Allow-Origin' header
```

**Solution**: Add your frontend URL to `CORS_ORIGINS` in `.env`

## Development vs Production

The configuration automatically detects the environment:

```python
# Development mode (default)
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG

# Production mode
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING
```

Use environment helpers:

```python
if settings.is_development:
    # Enable debug features
    app.add_middleware(DebugMiddleware)

if settings.is_production:
    # Enable production optimizations
    app.add_middleware(GZipMiddleware)
```

## See Also

- FastAPI Settings Documentation: https://fastapi.tiangolo.com/advanced/settings/
- Pydantic Settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- Neon PostgreSQL: https://neon.tech/docs
- Better Auth: https://better-auth.com
