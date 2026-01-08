#!/usr/bin/env python3
"""Database initialization script.

This script provides CLI commands for database management including:
- Creating all tables from SQLModel definitions
- Verifying database connection health
- Dropping tables with safety confirmations
- Seeding sample data for development

Usage:
    # Create all tables
    python scripts/init_db.py create

    # Verify database connection
    python scripts/init_db.py verify

    # Drop all tables (requires confirmation)
    python scripts/init_db.py drop

    # Drop tables without confirmation (dangerous!)
    python scripts/init_db.py drop --force

    # Create tables and seed sample data
    python scripts/init_db.py create --seed

    # Show database information
    python scripts/init_db.py info

Safety Features:
- Production environment protection (cannot drop in production)
- Interactive confirmation for destructive operations
- Connection health verification before operations
- Detailed logging of all operations

Schema Reference: specs/phase-2-todo-web/database/schema.md
Database Architect: .claude/agents/database-architect.md
"""

import sys
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
import logging
from typing import Optional

from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError
from sqlmodel import select

from app.core.config import settings
from app.core.database import (
    check_database_health,
    create_db_and_tables,
    drop_all_tables,
    engine,
    get_pool_status,
    get_session_context,
)
from app.models.task import Task, TaskStatus
from app.models.user import User

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ============================================================================
# Database Operations
# ============================================================================

def verify_connection() -> bool:
    """Verify database connection is healthy.

    Returns:
        bool: True if connection successful, False otherwise
    """
    logger.info("Verifying database connection...")

    try:
        # Check if DATABASE_URL is configured
        if not settings.DATABASE_URL:
            logger.error("❌ DATABASE_URL environment variable is not set")
            logger.info("Please set DATABASE_URL in your .env file")
            return False

        # Attempt connection health check
        if check_database_health():
            logger.info("✅ Database connection successful")
            logger.info(f"   Database: {_get_database_name()}")
            logger.info(f"   Host: {_get_database_host()}")
            return True
        else:
            logger.error("❌ Database health check failed")
            return False

    except OperationalError as e:
        logger.error(f"❌ Database connection failed: {e}")
        logger.info("Please check your DATABASE_URL and ensure the database is running")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error during connection verification: {e}")
        return False


def create_tables(seed_data: bool = False) -> bool:
    """Create all database tables from SQLModel definitions.

    Args:
        seed_data: If True, populate tables with sample data

    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("Creating database tables...")

    try:
        # Verify connection first
        if not verify_connection():
            logger.error("Cannot create tables: database connection failed")
            return False

        # Create tables
        create_db_and_tables()
        logger.info("✅ Database tables created successfully")

        # Show created tables
        tables = _get_table_list()
        if tables:
            logger.info(f"   Created {len(tables)} tables: {', '.join(tables)}")
        else:
            logger.warning("   No tables found after creation")

        # Seed sample data if requested
        if seed_data:
            logger.info("Seeding sample data...")
            if seed_sample_data():
                logger.info("✅ Sample data seeded successfully")
            else:
                logger.warning("⚠️  Sample data seeding failed")

        return True

    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
        return False


def drop_tables(force: bool = False) -> bool:
    """Drop all database tables with safety confirmation.

    Args:
        force: If True, skip confirmation prompt

    Returns:
        bool: True if successful, False otherwise
    """
    # Check if running in production
    if settings.is_production:
        logger.error("❌ Cannot drop tables in production environment!")
        logger.error("   This operation is blocked for safety")
        return False

    # Get list of tables to be dropped
    tables = _get_table_list()
    if not tables:
        logger.info("No tables found to drop")
        return True

    # Show what will be dropped
    logger.warning("⚠️  WARNING: This will permanently delete all data!")
    logger.warning(f"   Tables to drop: {', '.join(tables)}")
    logger.warning(f"   Environment: {settings.ENVIRONMENT}")

    # Confirmation prompt (unless force flag is set)
    if not force:
        logger.warning("")
        response = input("Are you sure you want to drop all tables? (yes/no): ")
        if response.lower() != "yes":
            logger.info("Operation cancelled")
            return False

    # Drop tables
    try:
        logger.info("Dropping all tables...")
        drop_all_tables()
        logger.info("✅ All tables dropped successfully")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to drop tables: {e}")
        return False


def show_database_info() -> None:
    """Display comprehensive database information."""
    logger.info("Database Information")
    logger.info("=" * 60)

    # Connection info
    logger.info(f"Database: {_get_database_name()}")
    logger.info(f"Host: {_get_database_host()}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Production: {settings.is_production}")

    # Connection pool info
    try:
        pool_status = get_pool_status()
        logger.info("")
        logger.info("Connection Pool:")
        logger.info(f"  Size: {pool_status['size']}")
        logger.info(f"  Checked in: {pool_status['checked_in']}")
        logger.info(f"  Checked out: {pool_status['checked_out']}")
        logger.info(f"  Overflow: {pool_status['overflow']}/{pool_status['max_overflow']}")
    except Exception as e:
        logger.warning(f"  Could not retrieve pool status: {e}")

    # Tables info
    tables = _get_table_list()
    logger.info("")
    logger.info(f"Tables ({len(tables)}):")
    for table in tables:
        row_count = _get_table_row_count(table)
        logger.info(f"  - {table}: {row_count} rows")

    logger.info("=" * 60)


def seed_sample_data() -> bool:
    """Seed database with sample data for development.

    Creates:
    - 3 sample users
    - 10 sample tasks across different statuses

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with get_session_context() as session:
            # Check if data already exists
            existing_users = session.exec(select(User)).first()
            if existing_users:
                logger.warning("Sample data already exists, skipping seed")
                return True

            # Create sample users
            users = [
                User(
                    email="alice@example.com",
                    password_hash="$2b$12$KIXx6jH3r.tQVxFwZ9vVGeJ3YQ7Z8pL3vWn0qY5jK9mN2oP1qR2sS",
                    is_active=True,
                ),
                User(
                    email="bob@example.com",
                    password_hash="$2b$12$L9wE5jI4s.uRWyGxA0wWFuK4ZR8aQm4oXwO1rZ6lN0pO2qS3rT4uU",
                    is_active=True,
                ),
                User(
                    email="charlie@example.com",
                    password_hash="$2b$12$M0xF6kJ5t.vSXzHyB1xXGvL5aS9bRn5pYxP2sA7mO1qP3rT4uU5vV",
                    is_active=False,
                ),
            ]

            for user in users:
                session.add(user)
            session.flush()  # Get user IDs

            # Create sample tasks for Alice
            alice_tasks = [
                Task(
                    user_id=users[0].id,
                    title="Complete project proposal",
                    description="Write and submit Q1 project proposal with budget breakdown and timeline.",
                    status=TaskStatus.IN_PROGRESS,
                ),
                Task(
                    user_id=users[0].id,
                    title="Review pull requests",
                    description=None,
                    status=TaskStatus.PENDING,
                ),
                Task(
                    user_id=users[0].id,
                    title="Update documentation",
                    description="Add API examples and troubleshooting guide to README",
                    status=TaskStatus.COMPLETED,
                ),
                Task(
                    user_id=users[0].id,
                    title="Fix bug in authentication flow",
                    description="Users are getting logged out unexpectedly",
                    status=TaskStatus.IN_PROGRESS,
                ),
                Task(
                    user_id=users[0].id,
                    title="Prepare presentation slides",
                    description="Create slides for weekly team meeting",
                    status=TaskStatus.PENDING,
                ),
            ]

            # Create sample tasks for Bob
            bob_tasks = [
                Task(
                    user_id=users[1].id,
                    title="Buy groceries",
                    description="Milk, eggs, bread, vegetables, coffee",
                    status=TaskStatus.COMPLETED,
                ),
                Task(
                    user_id=users[1].id,
                    title="Schedule dentist appointment",
                    description="Call Dr. Smith office for regular checkup",
                    status=TaskStatus.PENDING,
                ),
                Task(
                    user_id=users[1].id,
                    title="Renew car insurance",
                    description="Insurance expires on Jan 31. Compare quotes from 3 providers.",
                    status=TaskStatus.IN_PROGRESS,
                ),
            ]

            # Create sample tasks for Charlie (inactive user)
            charlie_tasks = [
                Task(
                    user_id=users[2].id,
                    title="Update resume",
                    description="Add recent project experience and new certifications",
                    status=TaskStatus.PENDING,
                ),
                Task(
                    user_id=users[2].id,
                    title="Read book: Clean Code",
                    description=None,
                    status=TaskStatus.COMPLETED,
                ),
            ]

            # Add all tasks
            for task in alice_tasks + bob_tasks + charlie_tasks:
                session.add(task)

            session.commit()

            logger.info(f"   Created {len(users)} users")
            logger.info(f"   Created {len(alice_tasks + bob_tasks + charlie_tasks)} tasks")

        return True

    except Exception as e:
        logger.error(f"Failed to seed sample data: {e}")
        return False


# ============================================================================
# Helper Functions
# ============================================================================

def _get_database_name() -> str:
    """Extract database name from DATABASE_URL."""
    try:
        url = settings.DATABASE_URL
        # Extract database name (last part of path)
        if "/" in url:
            db_name = url.split("/")[-1].split("?")[0]
            return db_name
        return "unknown"
    except Exception:
        return "unknown"


def _get_database_host() -> str:
    """Extract database host from DATABASE_URL."""
    try:
        url = settings.DATABASE_URL
        # Extract host (after @ and before /)
        if "@" in url and "/" in url:
            host_part = url.split("@")[1].split("/")[0]
            return host_part
        return "unknown"
    except Exception:
        return "unknown"


def _get_table_list() -> list[str]:
    """Get list of all tables in the database.

    Returns:
        list[str]: List of table names
    """
    try:
        inspector = inspect(engine)
        return inspector.get_table_names()
    except Exception as e:
        logger.error(f"Failed to get table list: {e}")
        return []


def _get_table_row_count(table_name: str) -> int:
    """Get row count for a specific table.

    Args:
        table_name: Name of the table

    Returns:
        int: Number of rows, or -1 if error
    """
    try:
        with get_session_context() as session:
            result = session.exec(text(f"SELECT COUNT(*) FROM {table_name}")).first()
            return result[0] if result else 0
    except Exception:
        return -1


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Database initialization and management tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create all tables
  python scripts/init_db.py create

  # Create tables and seed sample data
  python scripts/init_db.py create --seed

  # Verify database connection
  python scripts/init_db.py verify

  # Show database information
  python scripts/init_db.py info

  # Drop all tables (with confirmation)
  python scripts/init_db.py drop

  # Drop all tables (skip confirmation - dangerous!)
  python scripts/init_db.py drop --force
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create all database tables")
    create_parser.add_argument(
        "--seed", action="store_true", help="Seed sample data after creating tables"
    )

    # Verify command
    subparsers.add_parser("verify", help="Verify database connection")

    # Drop command
    drop_parser = subparsers.add_parser(
        "drop", help="Drop all database tables (destructive!)"
    )
    drop_parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompt (dangerous!)",
    )

    # Info command
    subparsers.add_parser("info", help="Show database information")

    # Seed command
    subparsers.add_parser("seed", help="Seed sample data into database")

    args = parser.parse_args()

    # Execute command
    if args.command == "create":
        success = create_tables(seed_data=args.seed)
        sys.exit(0 if success else 1)

    elif args.command == "verify":
        success = verify_connection()
        sys.exit(0 if success else 1)

    elif args.command == "drop":
        success = drop_tables(force=args.force)
        sys.exit(0 if success else 1)

    elif args.command == "info":
        show_database_info()
        sys.exit(0)

    elif args.command == "seed":
        if seed_sample_data():
            sys.exit(0)
        else:
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
