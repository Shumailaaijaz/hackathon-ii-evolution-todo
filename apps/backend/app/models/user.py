"""User data model.

This model is primarily managed by Better Auth library for authentication.
It defines the structure for the users table with authentication fields.
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

    Attributes:
        id: Unique user identifier (UUID v4)
        email: User's email address (unique, RFC 5322 compliant)
        name: User's display name
        password_hash: Bcrypt-hashed password (managed by Better Auth)
        created_at: Timestamp when user was created
        updated_at: Timestamp of last update (auto-updated by trigger)
        tasks: Relationship to user's tasks (one-to-many)
    """

    __tablename__ = "users"  # type: ignore

    # Primary key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique user identifier (UUID v4)"
    )

    # User information
    email: str = Field(
        unique=True,
        index=True,
        max_length=254,  # RFC 5321 max email length
        description="User's email address (unique, indexed)"
    )

    name: str = Field(
        min_length=1,
        max_length=100,
        description="User's display name"
    )

    # Authentication (managed by Better Auth)
    password_hash: str = Field(
        max_length=255,  # Bcrypt produces 60-char hashes, extra buffer for safety
        description="Bcrypt-hashed password"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when user was created (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of last update (UTC, auto-updated by DB trigger)"
    )

    # Soft delete flag (optional, for future use)
    is_active: bool = Field(
        default=True,
        description="Whether the user account is active"
    )

    # Relationships
    tasks: list["Task"] = Relationship(
        back_populates="user",
        cascade_delete=True,  # Delete all tasks when user is deleted
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "john.doe@example.com",
                "name": "John Doe",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z",
                "is_active": True
            }
        }

    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, email={self.email})>"
