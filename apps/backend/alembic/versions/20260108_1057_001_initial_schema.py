"""Initial schema with users and tasks tables.

Revision ID: 001
Revises:
Create Date: 2026-01-08 10:57:00.000000

This migration creates:
- users table (managed by Better Auth)
- tasks table with user_id foreign key
- Indexes on user_id, completed, created_at
- PostgreSQL trigger for auto-updating updated_at timestamps
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from uuid import uuid4

# revision identifiers, used by Alembic
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema."""

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column('email', sa.String(length=254), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create index on email (case-insensitive)
    op.create_index(
        'idx_users_email',
        'users',
        [sa.text('LOWER(email)')],
        unique=True
    )

    # Create index on created_at for sorting
    op.create_index(
        'idx_users_created_at',
        'users',
        ['created_at'],
        postgresql_using='btree',
        postgresql_ops={'created_at': 'DESC'}
    )

    # Create index on is_active for filtering active users
    op.create_index(
        'idx_users_is_active',
        'users',
        ['is_active'],
        postgresql_where=sa.text('is_active = TRUE')
    )

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            name='fk_tasks_user',
            ondelete='CASCADE',
            onupdate='CASCADE'
        ),
        sa.CheckConstraint("LENGTH(TRIM(title)) > 0", name='tasks_title_not_empty'),
        sa.CheckConstraint("LENGTH(title) <= 200", name='tasks_title_max_length'),
        sa.CheckConstraint(
            "description IS NULL OR LENGTH(description) <= 1000",
            name='tasks_description_max_length'
        )
    )

    # Create indexes on tasks table
    op.create_index(
        'idx_tasks_user_id',
        'tasks',
        ['user_id']
    )

    op.create_index(
        'idx_tasks_completed',
        'tasks',
        ['completed']
    )

    op.create_index(
        'idx_tasks_created_at',
        'tasks',
        ['created_at'],
        postgresql_using='btree',
        postgresql_ops={'created_at': 'DESC'}
    )

    op.create_index(
        'idx_tasks_updated_at',
        'tasks',
        ['updated_at'],
        postgresql_using='btree',
        postgresql_ops={'updated_at': 'DESC'}
    )

    # Composite index for common query pattern (user's tasks by status)
    op.create_index(
        'idx_tasks_user_completed',
        'tasks',
        ['user_id', 'completed']
    )

    # Composite index for user's tasks ordered by creation
    op.create_index(
        'idx_tasks_user_created',
        'tasks',
        ['user_id', 'created_at'],
        postgresql_ops={'created_at': 'DESC'}
    )

    # Create trigger function for auto-updating updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create trigger on users table
    op.execute("""
        CREATE TRIGGER update_users_updated_at
        BEFORE UPDATE ON users
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)

    # Create trigger on tasks table
    op.execute("""
        CREATE TRIGGER update_tasks_updated_at
        BEFORE UPDATE ON tasks
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    """Drop all tables and triggers."""

    # Drop triggers
    op.execute('DROP TRIGGER IF EXISTS update_tasks_updated_at ON tasks;')
    op.execute('DROP TRIGGER IF EXISTS update_users_updated_at ON users;')

    # Drop trigger function
    op.execute('DROP FUNCTION IF EXISTS update_updated_at_column();')

    # Drop tables (cascade will drop foreign keys)
    op.drop_table('tasks')
    op.drop_table('users')
