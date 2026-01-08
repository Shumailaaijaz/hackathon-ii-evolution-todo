"""Database connection and session management.

This module provides SQLModel engine configuration with connection pooling
optimized for Neon PostgreSQL serverless database.

Features:
- Connection pooling with Neon-optimized settings
- SSL/TLS encryption (required by Neon)
- Connection pre-ping for serverless resilience
- Automatic connection recycling
- Database health checks
- Session dependency for FastAPI

Schema Reference: specs/phase-2-todo-web/database/schema.md Section 1
Database Architect: .claude/agents/database-architect.md
"""

import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import event, text
from sqlalchemy.exc import OperationalError
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# Database Engine Configuration
# ============================================================================

def create_database_engine():
    """Create SQLModel engine with Neon PostgreSQL optimizations.

    Configuration follows specs/phase-2-todo-web/database/schema.md Section 1:
    - Connection Pool Size: 5-20 connections
    - Connection Timeout: 30 seconds
    - Statement Timeout: 30 seconds
    - SSL Mode: Required (Neon mandate)
    - Pool Pre-Ping: Enabled (serverless resilience)

    Neon-Specific Optimizations:
    - Reduced pool size (Neon handles connection pooling)
    - Connection pre-ping enabled (serverless environment)
    - Connection recycling after 1 hour
    - SSL required for all connections
    - Connection timeout for fast failure

    Returns:
        Engine: Configured SQLModel/SQLAlchemy engine

    Raises:
        ValueError: If DATABASE_URL is not configured
        OperationalError: If connection to database fails
    """
    if not settings.DATABASE_URL:
        raise ValueError(
            "DATABASE_URL environment variable is not set. "
            "Please configure database connection string."
        )

    # Parse database URL to check for Neon pooler
    db_url = settings.DATABASE_URL
    using_pooler = ".pooler." in db_url or "-pooler." in db_url

    # Adjust pool settings based on Neon pooler usage
    if using_pooler:
        # Neon pooler handles connection pooling, use smaller local pool
        pool_size = 5
        max_overflow = 5
        logger.info("Using Neon connection pooler (reduced local pool size)")
    else:
        # Direct connection, use larger pool
        pool_size = 10
        max_overflow = 10
        logger.info("Direct Neon connection (standard pool size)")

    engine = create_engine(
        db_url,
        # Logging
        echo=settings.DEBUG,  # Log SQL queries in debug mode

        # Connection Pool Settings
        pool_size=pool_size,  # Base connections maintained in pool
        max_overflow=max_overflow,  # Additional connections when pool exhausted
        pool_timeout=30,  # Seconds to wait for connection from pool
        pool_recycle=3600,  # Recycle connections after 1 hour (prevent stale connections)
        pool_pre_ping=True,  # Test connections before use (critical for serverless)

        # Connection Arguments (passed to psycopg2/asyncpg)
        connect_args={
            "sslmode": "require",  # Force SSL/TLS encryption (Neon requirement)
            "connect_timeout": 10,  # Connection timeout in seconds
            "application_name": "evolution-todo-api",  # Identify app in pg_stat_activity
            # Statement timeout (30 seconds) - set via session, not connect_args
        },

        # Performance
        pool_use_lifo=True,  # Use LIFO for better connection reuse
    )

    # Set statement timeout at session level
    @event.listens_for(engine, "connect")
    def set_session_parameters(dbapi_conn, connection_record):
        """Set PostgreSQL session parameters on new connections.

        Sets:
        - statement_timeout: 30 seconds (prevent long-running queries)
        - timezone: UTC (ensure consistent timestamp handling)
        """
        cursor = dbapi_conn.cursor()
        cursor.execute("SET statement_timeout = '30s'")
        cursor.execute("SET timezone = 'UTC'")
        cursor.close()

    logger.info(
        f"Database engine created: pool_size={pool_size}, "
        f"max_overflow={max_overflow}, pre_ping=True"
    )

    return engine


# Create global engine instance
engine = create_database_engine()


# ============================================================================
# Database Operations
# ============================================================================

def create_db_and_tables() -> None:
    """Create all database tables based on SQLModel models.

    This function uses SQLModel metadata to create all tables defined
    in the models/ directory. It's idempotent - running multiple times
    won't cause errors if tables already exist.

    Note:
        In production, use Alembic migrations instead of this function.
        This is primarily for development and testing.

        For production deployment:
        1. Generate migration: `alembic revision --autogenerate`
        2. Review migration file
        3. Apply migration: `alembic upgrade head`

    Example:
        >>> from app.core.database import create_db_and_tables
        >>> create_db_and_tables()  # Creates users and tasks tables
    """
    logger.info("Creating database tables from SQLModel metadata...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")


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

    logger.warning("Dropping all database tables...")
    SQLModel.metadata.drop_all(engine)
    logger.warning("All database tables dropped")


def check_database_health() -> bool:
    """Check database connection health.

    Performs a simple query to verify database connectivity.
    Useful for health check endpoints and startup validation.

    Returns:
        bool: True if database is healthy, False otherwise

    Example:
        >>> from app.core.database import check_database_health
        >>> if check_database_health():
        ...     print("Database is healthy")
    """
    try:
        with Session(engine) as session:
            # Execute simple query to test connection
            result = session.exec(text("SELECT 1")).first()
            if result == (1,):
                logger.debug("Database health check: OK")
                return True
            logger.error("Database health check: Unexpected result")
            return False
    except OperationalError as e:
        logger.error(f"Database health check failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Database health check error: {e}")
        return False


# ============================================================================
# Session Management
# ============================================================================

def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency to provide database session.

    This function is used as a FastAPI dependency to inject database
    sessions into route handlers. The session is automatically closed
    after the request completes (even if an exception occurs).

    Session Lifecycle:
    1. Session created from engine pool
    2. Yielded to route handler
    3. Handler executes queries
    4. Session committed (if no exception)
    5. Session closed (returns connection to pool)

    Error Handling:
    - If exception occurs in handler, session is rolled back
    - Session is always closed, even on exception
    - Connection returned to pool for reuse

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
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


@contextmanager
def get_session_context():
    """Context manager for manual session management.

    Use this when you need a database session outside of FastAPI
    route handlers (e.g., in background tasks, CLI scripts, tests).

    Yields:
        Session: SQLModel database session

    Example:
        >>> from app.core.database import get_session_context
        >>>
        >>> with get_session_context() as session:
        ...     task = Task(title="New task")
        ...     session.add(task)
        ...     session.commit()
    """
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


# ============================================================================
# Connection Pool Monitoring (Development/Debug)
# ============================================================================

def get_pool_status() -> dict:
    """Get current connection pool status.

    Returns detailed information about the connection pool state.
    Useful for monitoring and debugging connection issues.

    Returns:
        dict: Pool status with keys:
            - size: Current pool size
            - checked_in: Connections available in pool
            - checked_out: Connections currently in use
            - overflow: Overflow connections created
            - max_overflow: Maximum overflow allowed

    Example:
        >>> from app.core.database import get_pool_status
        >>> status = get_pool_status()
        >>> print(f"Pool size: {status['size']}, In use: {status['checked_out']}")
    """
    pool = engine.pool
    return {
        "size": pool.size(),
        "checked_in": pool.checkedinconns(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "max_overflow": pool._max_overflow,
    }


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    "engine",
    "create_db_and_tables",
    "drop_all_tables",
    "check_database_health",
    "get_session",
    "get_session_context",
    "get_pool_status",
]
