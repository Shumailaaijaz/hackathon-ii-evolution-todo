"""Application configuration using Pydantic Settings.

This module handles environment variable loading and validation.
All configuration values are typed and validated on application startup.
"""

from typing import List

from pydantic import field_validator
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
        CORS_ORIGINS: List of allowed frontend origins for CORS
        ENVIRONMENT: Application environment (development, staging, production)
        DEBUG: Enable debug mode (verbose logging, auto-reload)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Database
    DATABASE_URL: str

    # Authentication
    BETTER_AUTH_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

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


# Global settings instance
# This is imported and used throughout the application
settings = Settings()
