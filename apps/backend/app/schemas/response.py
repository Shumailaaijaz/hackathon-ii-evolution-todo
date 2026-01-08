"""Generic API response schemas.

This module provides standardized response wrappers for all API endpoints.
All responses follow a consistent structure with success/error fields.
"""

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

# Generic type variable for response data
T = TypeVar("T")


class ErrorDetail(BaseModel):
    """Error details for failed requests.

    Attributes:
        code: Error code (e.g., "VALIDATION_ERROR", "NOT_FOUND")
        message: Human-readable error message
    """

    code: str = Field(
        ...,
        description="Error code",
        examples=["VALIDATION_ERROR", "UNAUTHORIZED", "NOT_FOUND"]
    )

    message: str = Field(
        ...,
        description="Human-readable error message",
        examples=[
            "Title is required and must be 1-200 characters",
            "Invalid or expired authentication token",
            "Task not found"
        ]
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "VALIDATION_ERROR",
                    "message": "Title is required and must be 1-200 characters"
                }
            ]
        }
    }


class ApiResponse(BaseModel, Generic[T]):
    """Generic API response wrapper.

    All API endpoints return responses in this format for consistency.
    Successful responses have success=True and populated data field.
    Failed responses have success=False and populated error field.

    Attributes:
        success: Whether the request succeeded
        data: Response data (only present on success)
        error: Error details (only present on failure)

    Example Success Response:
        {
            "success": true,
            "data": {"id": 1, "title": "Buy groceries", ...},
            "error": null
        }

    Example Error Response:
        {
            "success": false,
            "data": null,
            "error": {"code": "NOT_FOUND", "message": "Task not found"}
        }
    """

    success: bool = Field(
        ...,
        description="Whether the request succeeded"
    )

    data: Optional[T] = Field(
        None,
        description="Response data (present on success)"
    )

    error: Optional[ErrorDetail] = Field(
        None,
        description="Error details (present on failure)"
    )

    @classmethod
    def success_response(cls, data: T) -> "ApiResponse[T]":
        """Create a successful API response.

        Args:
            data: The response data

        Returns:
            ApiResponse with success=True and populated data

        Example:
            >>> task = Task(id=1, title="Buy groceries", ...)
            >>> return ApiResponse.success_response(task)
        """
        return cls(success=True, data=data, error=None)

    @classmethod
    def error_response(cls, code: str, message: str) -> "ApiResponse[None]":
        """Create an error API response.

        Args:
            code: Error code (e.g., "NOT_FOUND", "VALIDATION_ERROR")
            message: Human-readable error message

        Returns:
            ApiResponse with success=False and populated error

        Example:
            >>> return ApiResponse.error_response(
            ...     code="NOT_FOUND",
            ...     message="Task not found"
            ... )
        """
        return cls(
            success=False,
            data=None,
            error=ErrorDetail(code=code, message=message)
        )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "data": {"id": 1, "title": "Buy groceries"},
                    "error": None
                },
                {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": "Task not found"
                    }
                }
            ]
        }
    }


# Convenience type aliases for common response types
TaskListResponse = ApiResponse[list]
TaskSingleResponse = ApiResponse[dict]
MessageResponse = ApiResponse[dict]


# Export response types
__all__ = [
    "ErrorDetail",
    "ApiResponse",
    "TaskListResponse",
    "TaskSingleResponse",
    "MessageResponse",
]
