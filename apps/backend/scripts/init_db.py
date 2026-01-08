"""Database initialization script.

This script provides utilities for initializing and managing the database.
It can create tables, verify connections, and reset the database (dev only).

Usage:
    python scripts/init_db.py              # Initialize database
    python scripts/init_db.py --reset      # Reset database (DEV ONLY!)
    python scripts/init_db.py --verify     # Verify connection only
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from sqlmodel import Session, select

from app.core.config import settings
from app.core.database import create_db_and_tables, drop_all_tables, engine
from app.models import Task, User


def verify_connection() -> bool:
    """Verify database connection.

    Returns:
        True if connection successful, False otherwise
    """
    print("🔍 Verifying database connection...")
    print(f"   Database: {settings.DATABASE_URL.split('@')[1].split('/')[0]}")

    try:
        with Session(engine) as session:
            # Simple query to test connection
            result = session.exec(text("SELECT 1")).first()
            if result == (1,):
                print("✅ Database connection successful!")
                return True
            else:
                print("❌ Database query returned unexpected result")
                return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def check_tables_exist() -> bool:
    """Check if required tables exist.

    Returns:
        True if all tables exist, False otherwise
    """
    print("\n🔍 Checking for existing tables...")

    try:
        with Session(engine) as session:
            # Query information_schema to check for tables
            result = session.exec(
                text("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name IN ('users', 'tasks')
                    ORDER BY table_name
                """)
            ).all()

            existing_tables = [row[0] for row in result]

            if 'users' in existing_tables:
                print("   ✓ users table exists")
            else:
                print("   ✗ users table missing")

            if 'tasks' in existing_tables:
                print("   ✓ tasks table exists")
            else:
                print("   ✗ tasks table missing")

            return len(existing_tables) == 2

    except Exception as e:
        print(f"   ❌ Error checking tables: {e}")
        return False


def initialize_database() -> None:
    """Initialize database by creating all tables."""
    print("\n🚀 Initializing database...")

    # Check if tables already exist
    if check_tables_exist():
        print("\n⚠️  Tables already exist. Skipping creation.")
        print("   Use --reset to drop and recreate (DEV ONLY!)")
        return

    print("\n📦 Creating tables...")
    try:
        create_db_and_tables()
        print("✅ Tables created successfully!")

        # Verify tables were created
        if check_tables_exist():
            print("\n✅ Database initialization complete!")
        else:
            print("\n❌ Tables creation reported success but verification failed")

    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        sys.exit(1)


def reset_database() -> None:
    """Reset database by dropping and recreating all tables.

    WARNING: This is a destructive operation!
    """
    if settings.is_production:
        print("❌ Cannot reset database in production environment!")
        print("   This operation is only allowed in development/testing.")
        sys.exit(1)

    print("\n⚠️  WARNING: This will delete ALL data!")
    print("   Environment:", settings.ENVIRONMENT)

    # Require explicit confirmation
    confirmation = input("\n   Type 'DELETE ALL DATA' to confirm: ")

    if confirmation != "DELETE ALL DATA":
        print("\n✗ Reset cancelled.")
        return

    print("\n🗑️  Dropping all tables...")
    try:
        drop_all_tables()
        print("✅ Tables dropped successfully!")
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        sys.exit(1)

    print("\n📦 Creating fresh tables...")
    try:
        create_db_and_tables()
        print("✅ Tables created successfully!")

        if check_tables_exist():
            print("\n✅ Database reset complete!")
        else:
            print("\n❌ Reset completed but verification failed")

    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)


def display_stats() -> None:
    """Display database statistics."""
    print("\n📊 Database Statistics:")

    try:
        with Session(engine) as session:
            # Count users
            user_count = session.exec(
                select(User).where(User.is_active == True)  # noqa: E712
            ).all()
            print(f"   Active Users: {len(user_count)}")

            # Count tasks
            task_count = session.exec(select(Task)).all()
            completed_count = len([t for t in task_count if t.completed])
            print(f"   Total Tasks: {len(task_count)}")
            print(f"   Completed Tasks: {completed_count}")
            print(f"   Active Tasks: {len(task_count) - completed_count}")

    except Exception as e:
        print(f"   ❌ Error fetching statistics: {e}")


def main() -> None:
    """Main entry point for database initialization script."""
    parser = argparse.ArgumentParser(
        description="Initialize and manage the Todo application database"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset database (drop and recreate tables) - DEV ONLY!"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify database connection only"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Display database statistics"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("   Todo Application - Database Initialization")
    print("=" * 60)

    # Always verify connection first
    if not verify_connection():
        print("\n❌ Exiting due to connection failure")
        sys.exit(1)

    # Handle different modes
    if args.verify:
        print("\n✅ Connection verification complete!")

    elif args.reset:
        reset_database()
        if args.stats:
            display_stats()

    elif args.stats:
        check_tables_exist()
        display_stats()

    else:
        initialize_database()

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
