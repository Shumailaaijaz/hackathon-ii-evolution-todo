"""Task data model following schema.md specification.

This model represents todo tasks with user ownership and status tracking.
All tasks are scoped to a specific user (user isolation enforced).

Schema Reference: specs/phase-2-todo-web/database/schema.md Section 3
"""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


class TaskStatus(str, Enum):
    """Task status enumeration matching database VARCHAR enum."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(SQLModel, table=True):
    """Task model for todo items.

    Each task belongs to a single user and has title, description, and status.
    User isolation is enforced via foreign key constraint and database indexes.

    Schema Compliance:
    - Matches actual database schema (UUID id, status VARCHAR enum)
    - UUID primary key with gen_random_uuid()
    - Status as VARCHAR(11) storing enum values
    - Title validation (1-200 characters, non-empty after trim)
    - Description optional (max 2000 characters)
    - Timestamps in UTC with automatic updated_at via trigger
    - Foreign key CASCADE delete and update to users table
    - Composite indexes for common query patterns

    Attributes:
        id: Unique task identifier (UUID v4)
        user_id: Foreign key to owning user (UUID, indexed)
        title: Task title (1-200 characters, required, non-empty)
        description: Optional task description (max 2000 characters)
        status: Task status (pending | in_progress | completed)
        created_at: Task creation timestamp (UTC, indexed for sorting)
        updated_at: Last modification timestamp (UTC, auto-updated by trigger)
        user: Relationship to owning user (many-to-one)
    """

    __tablename__ = "tasks"  # type: ignore

    # Primary key
    id: Optional[UUID] = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique task identifier (UUID v4)",
        sa_column_kwargs={"server_default": text("gen_random_uuid()")}
    )

    # Foreign key to user
    user_id: UUID = Field(
        foreign_key="users.id",
        index=True,
        description="Task owner (references users.id, indexed for performance)",
        sa_column_kwargs={"nullable": False}
    )

    # Task content
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters, required, non-empty after trim)",
        sa_column_kwargs={"nullable": False}
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional task description (max 2000 characters)",
        sa_column_kwargs={"nullable": True}
    )

    # Status field - stored as VARCHAR in database
    status: str = Field(
        default=TaskStatus.PENDING.value,
        description="Task status (pending | in_progress | completed)",
        sa_column_kwargs={"nullable": False}
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Task creation timestamp (UTC, indexed for sorting)",
        sa_column_kwargs={
            "nullable": False,
            "server_default": func.now()
        }
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last modification timestamp (UTC, auto-updated by DB trigger)",
        sa_column_kwargs={
            "nullable": False,
            "server_default": func.now()
        }
    )

    # Relationships
    user: Optional["User"] = Relationship(
        back_populates="tasks",
        sa_relationship_kwargs={"lazy": "joined"}
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "id": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Complete project proposal",
                "description": "Write and submit Q1 project proposal",
                "status": "in_progress",
                "created_at": "2026-01-05T09:00:00Z",
                "updated_at": "2026-01-08T14:30:00Z"
            }
        }

    def __repr__(self) -> str:
        """String representation of Task."""
        status_icons = {
            TaskStatus.PENDING.value: "○",
            TaskStatus.IN_PROGRESS.value: "◐",
            TaskStatus.COMPLETED.value: "●"
        }
        icon = status_icons.get(self.status, "?")
        return f"<Task(id={self.id}, {icon} {self.title!r}, status={self.status}, user_id={self.user_id})>"

    def toggle_completion(self) -> None:
        """Toggle task between completed and pending.

        The updated_at field will be auto-updated by the database trigger.
        """
        if self.status == TaskStatus.COMPLETED.value:
            self.status = TaskStatus.PENDING.value
        else:
            self.status = TaskStatus.COMPLETED.value

    def start(self) -> None:
        """Mark task as in progress.

        Convenience method for common action.
        """
        self.status = TaskStatus.IN_PROGRESS.value

    def complete(self) -> None:
        """Mark task as completed.

        Convenience method for common action.
        """
        self.status = TaskStatus.COMPLETED.value

    def reopen(self) -> None:
        """Reopen a completed task.

        Convenience method for common action.
        """
        self.status = TaskStatus.PENDING.value

    @property
    def is_pending(self) -> bool:
        """Check if task is pending."""
        return self.status == TaskStatus.PENDING.value

    @property
    def is_in_progress(self) -> bool:
        """Check if task is in progress."""
        return self.status == TaskStatus.IN_PROGRESS.value

    @property
    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.status == TaskStatus.COMPLETED.value
