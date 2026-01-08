"""FastAPI dependencies for authentication and authorization.

This module provides dependency injection functions for protecting API endpoints
and verifying user access to resources.
"""

from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status

from app.core.security import get_user_id_from_token


async def get_current_user(authorization: Annotated[str | None, Header()] = None) -> str:
    """FastAPI dependency to extract and validate JWT from Authorization header.

    This dependency is used to protect API endpoints that require authentication.
    It extracts the JWT token from the Authorization header, validates it,
    and returns the authenticated user's ID.

    Args:
        authorization: The Authorization header value (injected by FastAPI)

    Returns:
        The authenticated user's ID (UUID as string)

    Raises:
        HTTPException: 401 if Authorization header is missing or token is invalid

    Example:
        >>> @app.get("/api/tasks")
        >>> async def get_tasks(user_id: str = Depends(get_current_user)):
        ...     # user_id is guaranteed to be a valid authenticated user
        ...     return get_user_tasks(user_id)
    """
    # Check if Authorization header exists
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if header uses Bearer scheme
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected 'Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract token (remove "Bearer " prefix)
    token = authorization.split(" ", 1)[1] if " " in authorization else ""

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify token and extract user ID
    user_id = get_user_id_from_token(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


def verify_user_access(authenticated_user_id: str, requested_user_id: str) -> None:
    """Verify that authenticated user matches the requested user ID.

    This function enforces user isolation by ensuring users can only
    access their own resources. It raises 403 Forbidden if there's a mismatch.

    Args:
        authenticated_user_id: User ID from JWT token
        requested_user_id: User ID from request path/body

    Raises:
        HTTPException: 403 if user IDs don't match

    Example:
        >>> @app.get("/api/{user_id}/tasks")
        >>> async def get_tasks(
        ...     user_id: str,
        ...     current_user: str = Depends(get_current_user)
        ... ):
        ...     verify_user_access(current_user, user_id)
        ...     return get_tasks_for_user(user_id)
    """
    if authenticated_user_id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only access your own resources.",
        )


def verify_task_ownership(
    task_user_id: UUID | str,
    authenticated_user_id: str
) -> None:
    """Verify that a task belongs to the authenticated user.

    This is similar to verify_user_access but specifically for task resources.
    It prevents users from accessing or modifying other users' tasks.

    Args:
        task_user_id: The user_id field from the task record
        authenticated_user_id: User ID from JWT token

    Raises:
        HTTPException: 403 if task doesn't belong to authenticated user

    Example:
        >>> @app.put("/api/tasks/{task_id}")
        >>> async def update_task(
        ...     task_id: int,
        ...     current_user: str = Depends(get_current_user),
        ...     session: Session = Depends(get_session)
        ... ):
        ...     task = session.get(Task, task_id)
        ...     if not task:
        ...         raise HTTPException(404, "Task not found")
        ...     verify_task_ownership(task.user_id, current_user)
        ...     # Now safe to update task
    """
    # Convert UUID to string for comparison
    task_user_id_str = str(task_user_id) if isinstance(task_user_id, UUID) else task_user_id

    if task_user_id_str != authenticated_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This task belongs to a different user.",
        )


# Type alias for cleaner dependency injection
CurrentUser = Annotated[str, Depends(get_current_user)]


# Export commonly used dependencies
__all__ = [
    "get_current_user",
    "verify_user_access",
    "verify_task_ownership",
    "CurrentUser",
]
