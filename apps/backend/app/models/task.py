"""Task data model.

This model represents todo tasks with user ownership and completion tracking.
All tasks are scoped to a specific user (user isolation enforced).
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


class Task(SQLModel, table=True):
    """Task model for todo items.

    Each task belongs to a single user and has title, description, and completion status.
    User isolation is enforced via foreign key constraint and database indexes.

    Attributes:
        id: Auto-incrementing task identifier
        user_id: Foreign key to owning user (UUID)
        title: Task title (1-200 characters, required)
        description: Optional task description (max 1000 characters)
        completed: Whether task is completed (default False)
        created_at: Timestamp when task was created
        updated_at: Timestamp of last update (auto-updated by trigger)
        user: Relationship to owning user (many-to-one)
    """

    __tablename__ = "tasks"  # type: ignore

    # Primary key
    id: int = Field(
        default=None,
        primary_key=True,
        description="Auto-incrementing task identifier"
    )

    # Foreign key to user
    user_id: UUID = Field(
        foreign_key="users.id",
        index=True,
        description="Foreign key to owning user (indexed for performance)"
    )

    # Task content
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters, required)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional task description (max 1000 characters)"
    )

    # Status
    completed: bool = Field(
        default=False,
        index=True,
        description="Whether task is completed (indexed for filtering)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Timestamp when task was created (UTC, indexed for sorting)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of last update (UTC, auto-updated by DB trigger)"
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
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }

    def __repr__(self) -> str:
        """String representation of Task."""
        status = "✓" if self.completed else "○"
        return f"<Task(id={self.id}, {status} {self.title!r}, user_id={self.user_id})>"

    def toggle_completion(self) -> None:
        """Toggle task completion status.

        This method flips the completed flag from True to False or vice versa.
        The updated_at field will be auto-updated by the database trigger.
        """
        self.completed = not self.completed
