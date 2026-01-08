"""User data model following schema.md specification.

This model is primarily managed by Better Auth library for authentication.
It defines the structure for the users table with authentication fields.

Schema Reference: specs/phase-2-todo-web/database/schema.md Section 2
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.task import Task


class User(SQLModel, table=True):
    """User model for authentication and task ownership.

    Better Auth manages user registration, login, and password hashing.
    This model defines the database schema for storing user information.

    Schema Compliance:
    - Follows specs/phase-2-todo-web/database/schema.md Section 2
    - UUID primary key with gen_random_uuid()
    - Email validation (RFC 5321 max 254 characters)
    - Bcrypt password hashing (min 60 characters, max 255)
    - Timestamps in UTC with automatic updated_at via trigger
    - Soft delete via is_active flag

    Attributes:
        id: Unique user identifier (UUID v4)
        email: User's email address (unique, RFC 5322 compliant, case-insensitive)
        password_hash: Bcrypt-hashed password (managed by Better Auth)
        created_at: Account creation timestamp (UTC, immutable)
        updated_at: Last modification timestamp (UTC, auto-updated by trigger)
        is_active: Account active status (False = soft deleted)
        last_login: Last successful authentication timestamp (UTC, nullable)
        tasks: Relationship to user's tasks (one-to-many with cascade delete)
    """

    __tablename__ = "users"  # type: ignore

    # Primary key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique user identifier (UUID v4)",
        sa_column_kwargs={"server_default": "gen_random_uuid()"}
    )

    # Authentication - Email
    email: str = Field(
        unique=True,
        index=True,
        max_length=254,  # RFC 5321 max email length
        description="User's email address (unique, indexed, case-insensitive)",
        sa_column_kwargs={
            "nullable": False,
        }
    )

    # Authentication - Password
    password_hash: str = Field(
        max_length=255,  # Bcrypt produces 60-char hashes, buffer for future algorithms
        min_length=60,   # Minimum bcrypt hash length
        description="Bcrypt-hashed password (work factor >= 12)",
        sa_column_kwargs={"nullable": False}
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp (UTC, immutable after insert)",
        sa_column_kwargs={
            "nullable": False,
            "server_default": "NOW()"
        }
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last modification timestamp (UTC, auto-updated by DB trigger)",
        sa_column_kwargs={
            "nullable": False,
            "server_default": "NOW()"
        }
    )

    # Account Status
    is_active: bool = Field(
        default=True,
        description="Account active status (True=active, False=soft deleted)",
        sa_column_kwargs={
            "nullable": False,
            "server_default": "TRUE"
        }
    )

    last_login: Optional[datetime] = Field(
        default=None,
        description="Last successful authentication timestamp (UTC, nullable)",
        sa_column_kwargs={"nullable": True}
    )

    # Relationships
    tasks: list["Task"] = Relationship(
        back_populates="user",
        cascade_delete=True,  # Delete all tasks when user is deleted
        sa_relationship_kwargs={
            "lazy": "selectin",
            "cascade": "all, delete-orphan"
        }
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "alice@example.com",
                "password_hash": "$2b$12$KIXx6jH3r.tQVxFwZ9vVGeJ3YQ7Z8pL3vWn0qY5jK9mN2oP1qR2sS",
                "created_at": "2026-01-01T10:00:00Z",
                "updated_at": "2026-01-08T15:30:00Z",
                "is_active": True,
                "last_login": "2026-01-08T15:30:00Z"
            }
        }

    def __repr__(self) -> str:
        """String representation of User."""
        status = "active" if self.is_active else "inactive"
        return f"<User(id={self.id}, email={self.email!r}, {status})>"
