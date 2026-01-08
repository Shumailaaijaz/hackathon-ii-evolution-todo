"""Pydantic schemas for Task API request/response validation.

These schemas define the structure for creating, updating, and returning tasks.
They provide validation and documentation for the API.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    """Schema for creating a new task.

    This schema validates task creation requests. The user_id is not included
    here as it's extracted from the JWT token for security.

    Attributes:
        title: Task title (1-200 characters, required)
        description: Optional task description (max 1000 characters)
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title (required, 1-200 characters)",
        examples=["Buy groceries", "Complete project documentation"]
    )

    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Optional task description (max 1000 characters)",
        examples=["Milk, eggs, bread", "Write API documentation and examples"]
    )

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate that title is not empty after trimming whitespace."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip()

    @field_validator("description")
    @classmethod
    def description_cleaned(cls, v: Optional[str]) -> Optional[str]:
        """Clean description (trim whitespace, return None if empty)."""
        if v is None:
            return None
        cleaned = v.strip()
        return cleaned if cleaned else None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread"
                },
                {
                    "title": "Complete project documentation",
                    "description": None
                }
            ]
        }
    }


class TaskUpdate(BaseModel):
    """Schema for updating an existing task.

    All fields are optional to support partial updates.
    Only provided fields will be updated.

    Attributes:
        title: Optional new title (1-200 characters)
        description: Optional new description (max 1000 characters, use "" to clear)
        completed: Optional completion status
    """

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="New task title (optional)",
        examples=["Updated task title"]
    )

    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="New description (optional, empty string to clear)",
        examples=["Updated description", ""]
    )

    completed: Optional[bool] = Field(
        None,
        description="Task completion status (optional)",
        examples=[True, False]
    )

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate that title is not empty if provided."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip() if v else None

    @field_validator("description")
    @classmethod
    def description_cleaned(cls, v: Optional[str]) -> Optional[str]:
        """Clean description (empty string becomes None)."""
        if v == "":
            return None  # Allow clearing description
        return v.strip() if v else None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"title": "Updated title"},
                {"description": "New description"},
                {"completed": True},
                {"title": "New title", "completed": True}
            ]
        }
    }


class TaskResponse(BaseModel):
    """Schema for task responses.

    This is the standard format for returning task data from the API.

    Attributes:
        id: Task identifier
        user_id: Owner's user ID
        title: Task title
        description: Task description (optional)
        completed: Completion status
        created_at: Creation timestamp (UTC)
        updated_at: Last update timestamp (UTC)
    """

    id: int = Field(..., description="Task identifier", examples=[1, 42, 100])

    user_id: UUID = Field(
        ...,
        description="Owner's user ID",
        examples=["550e8400-e29b-41d4-a716-446655440000"]
    )

    title: str = Field(
        ...,
        description="Task title",
        examples=["Buy groceries"]
    )

    description: Optional[str] = Field(
        None,
        description="Task description",
        examples=["Milk, eggs, bread"]
    )

    completed: bool = Field(
        ...,
        description="Completion status",
        examples=[False, True]
    )

    created_at: datetime = Field(
        ...,
        description="Creation timestamp (UTC)",
        examples=["2024-01-15T10:30:00Z"]
    )

    updated_at: datetime = Field(
        ...,
        description="Last update timestamp (UTC)",
        examples=["2024-01-15T14:25:00Z"]
    )

    model_config = {
        "from_attributes": True,  # Allow creation from ORM models
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread",
                    "completed": False,
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-01-15T10:30:00Z"
                }
            ]
        }
    }


# Export schemas
__all__ = [
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
]
