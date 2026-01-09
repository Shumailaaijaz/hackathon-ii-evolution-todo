"""Application configuration using Pydantic Settings.

This module handles environment variable loading and validation.
All configuration values are typed and validated on application startup.

Configuration follows FastAPI best practices:
- Environment-based settings
- Type validation with Pydantic
- Fail-fast validation on startup
- Secure defaults

Usage:
    from app.core.config import settings

    print(settings.DATABASE_URL)
    if settings.is_production:
        # Production-only logic
"""

from typing import List, Optional

from pydantic import field_validator, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All settings are validated on startup. Missing or invalid values
    will cause the application to fail fast with clear error messages.

    Attributes:
        DATABASE_URL: PostgreSQL connection string (Neon serverless)
        BETTER_AUTH_SECRET: Shared secret for JWT token validation (min 32 chars)
        JWT_ALGORITHM: Algorithm for JWT signature (HS256 recommended)
        JWT_EXPIRE_DAYS: Token expiration in days (default 7)
        CORS_ORIGINS: Comma-separated list of allowed frontend origins
        ENVIRONMENT: Application environment (development, staging, production)
        DEBUG: Enable debug mode (verbose logging, auto-reload)
        API_PREFIX: API route prefix (default: /api)
        PROJECT_NAME: Application name for OpenAPI docs
        VERSION: API version
        LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR)
        SENTRY_DSN: Optional Sentry error tracking URL
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        validate_default=True
    )

    # ============================================================================
    # Database Configuration
    # ============================================================================
    DATABASE_URL: str

    # ============================================================================
    # Authentication & Security
    # ============================================================================
    BETTER_AUTH_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_DAYS: int = 7

    # ============================================================================
    # CORS Configuration
    # ============================================================================
    CORS_ORIGINS: str = "http://localhost:3000"

    # ============================================================================
    # Application Configuration
    # ============================================================================
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Todo API"
    VERSION: str = "2.0.0"

    # ============================================================================
    # Logging & Monitoring
    # ============================================================================
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: Optional[str] = None

    @field_validator("BETTER_AUTH_SECRET")
    @classmethod
    def validate_secret_length(cls, v: str) -> str:
        """Validate that BETTER_AUTH_SECRET is at least 32 characters.

        Args:
            v: The secret value from environment

        Returns:
            The validated secret

        Raises:
            ValueError: If secret is less than 32 characters
        """
        if len(v) < 32:
            raise ValueError(
                "BETTER_AUTH_SECRET must be at least 32 characters for security. "
                f"Got {len(v)} characters. "
                "Generate with: openssl rand -base64 32"
            )
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate DATABASE_URL format.

        Args:
            v: The database URL from environment

        Returns:
            The validated URL

        Raises:
            ValueError: If URL doesn't start with postgresql://
        """
        if not v.startswith("postgresql://"):
            raise ValueError(
                "DATABASE_URL must start with 'postgresql://'. "
                f"Got: {v[:20]}..."
            )
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into list.

        Supports both single origin and comma-separated multiple origins.

        Returns:
            List of origin URLs
        """
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        """Check if running in production environment.

        Returns:
            True if ENVIRONMENT is 'production'
        """
        return self.ENVIRONMENT.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment.

        Returns:
            True if ENVIRONMENT is 'development'
        """
        return self.ENVIRONMENT.lower() == "development"

    @property
    def is_staging(self) -> bool:
        """Check if running in staging environment.

        Returns:
            True if ENVIRONMENT is 'staging'
        """
        return self.ENVIRONMENT.lower() == "staging"

    @property
    def database_host(self) -> str:
        """Extract database host from DATABASE_URL.

        Returns:
            Database hostname
        """
        # Extract host from postgresql://user:pass@host:port/db
        if "@" in self.DATABASE_URL:
            host_part = self.DATABASE_URL.split("@")[1]
            return host_part.split("/")[0].split(":")[0]
        return "unknown"

    def get_logging_config(self) -> dict:
        """Get logging configuration based on environment.

        Returns:
            Logging configuration dictionary
        """
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
                "detailed": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "detailed" if self.DEBUG else "default",
                    "level": self.LOG_LEVEL,
                },
            },
            "root": {
                "level": self.LOG_LEVEL,
                "handlers": ["console"],
            },
        }

    def __repr__(self) -> str:
        """String representation of settings (hides sensitive data).

        Returns:
            Safe string representation
        """
        return (
            f"Settings("
            f"env={self.ENVIRONMENT}, "
            f"debug={self.DEBUG}, "
            f"db_host={self.database_host}, "
            f"cors_origins={len(self.cors_origins_list)} origins"
            f")"
        )


# Global settings instance
# This is imported and used throughout the application
# Validates all settings on import - will raise exceptions if invalid
settings = Settings()


# Log configuration on startup (development only)
if settings.is_development:
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Configuration loaded: {settings}")
    logger.info(f"CORS Origins: {settings.cors_origins_list}")
    logger.info(f"Database: {settings.database_host}")
