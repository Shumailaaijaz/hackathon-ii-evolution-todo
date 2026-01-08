"""Database connection and session management.

This module provides SQLModel engine configuration with connection pooling
optimized for Neon PostgreSQL serverless database.
"""

from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

# Create database engine with connection pooling
# Configuration optimized for Neon PostgreSQL serverless platform
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_size=5,  # Maintain 5 connections in the pool
    max_overflow=10,  # Allow up to 10 additional connections
    pool_pre_ping=True,  # Verify connections before using (important for serverless)
    pool_recycle=3600,  # Recycle connections after 1 hour
    connect_args={
        "sslmode": "require",  # Force SSL for security (required by Neon)
        "connect_timeout": 10,  # Connection timeout in seconds
    }
)


def create_db_and_tables() -> None:
    """Create all database tables based on SQLModel models.

    This function uses SQLModel metadata to create all tables defined
    in the models/ directory. It's idempotent - running multiple times
    won't cause errors if tables already exist.

    Note:
        In production, use Alembic migrations instead of this function.
        This is primarily for development and testing.

    Example:
        >>> from app.core.database import create_db_and_tables
        >>> create_db_and_tables()  # Creates users and tasks tables
    """
    SQLModel.metadata.create_all(engine)


def drop_all_tables() -> None:
    """Drop all database tables.

    WARNING: This is a destructive operation that deletes all data!
    Only use in development or testing environments.

    Raises:
        RuntimeError: If called in production environment

    Example:
        >>> from app.core.database import drop_all_tables
        >>> drop_all_tables()  # Removes all tables and data
    """
    if settings.is_production:
        raise RuntimeError(
            "Cannot drop tables in production environment! "
            "This operation is only allowed in development/testing."
        )

    SQLModel.metadata.drop_all(engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency to provide database session.

    This function is used as a FastAPI dependency to inject database
    sessions into route handlers. The session is automatically closed
    after the request completes (even if an exception occurs).

    Yields:
        Session: SQLModel database session

    Example:
        >>> from fastapi import Depends
        >>> from app.core.database import get_session
        >>>
        >>> @app.get("/tasks")
        >>> def get_tasks(session: Session = Depends(get_session)):
        ...     tasks = session.exec(select(Task)).all()
        ...     return tasks
    """
    with Session(engine) as session:
        yield session


# Export commonly used items
__all__ = [
    "engine",
    "create_db_and_tables",
    "drop_all_tables",
    "get_session",
]
