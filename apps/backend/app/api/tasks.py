"""Task API endpoints.

This module provides REST API endpoints for task CRUD operations.
All endpoints require JWT authentication and enforce user isolation.
"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.api.deps import CurrentUser, verify_task_ownership, verify_user_access
from app.core.database import get_session
from app.models import Task
from app.schemas import ApiResponse, TaskCreate, TaskResponse, TaskUpdate

# Create router
router = APIRouter()


@router.get(
    "/{user_id}/tasks",
    response_model=ApiResponse[list[TaskResponse]],
    summary="List user's tasks",
    description="Retrieve all tasks for the authenticated user with optional filtering and sorting"
)
async def get_tasks(
    user_id: str,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    sort: Optional[str] = Query("created_at", description="Sort field (created_at, updated_at, title)"),
    order: Optional[str] = Query("desc", description="Sort order (asc, desc)"),
) -> ApiResponse[list[TaskResponse]]:
    """Get all tasks for the authenticated user.

    This endpoint retrieves tasks with optional filtering by completion status
    and sorting by various fields. User isolation is enforced - users can only
    access their own tasks.

    Args:
        user_id: User ID from URL path
        current_user: Authenticated user ID from JWT (injected)
        session: Database session (injected)
        completed: Optional filter by completion status
        sort: Sort field (created_at, updated_at, title)
        order: Sort order (asc, desc)

    Returns:
        ApiResponse containing list of tasks

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user
    """
    # Verify user access
    verify_user_access(current_user, user_id)

    # Build query
    query = select(Task).where(Task.user_id == user_id)

    # Apply completion filter if specified
    if completed is not None:
        query = query.where(Task.completed == completed)

    # Apply sorting
    sort_field = Task.created_at  # Default
    if sort == "updated_at":
        sort_field = Task.updated_at
    elif sort == "title":
        sort_field = Task.title

    if order == "asc":
        query = query.order_by(sort_field.asc())  # type: ignore
    else:
        query = query.order_by(sort_field.desc())  # type: ignore

    # Execute query
    tasks = session.exec(query).all()

    # Convert to response models
    task_responses = [TaskResponse.model_validate(task) for task in tasks]

    return ApiResponse.success_response(task_responses)


@router.post(
    "/{user_id}/tasks",
    response_model=ApiResponse[TaskResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the authenticated user"
)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
) -> ApiResponse[TaskResponse]:
    """Create a new task for the authenticated user.

    This endpoint creates a task with the provided title and optional description.
    The user_id is automatically set from the authenticated JWT token.

    Args:
        user_id: User ID from URL path
        task_data: Task creation data (title, description)
        current_user: Authenticated user ID from JWT (injected)
        session: Database session (injected)

    Returns:
        ApiResponse containing the created task with HTTP 201

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user
        HTTPException: 400 if validation fails
    """
    # Verify user access
    verify_user_access(current_user, user_id)

    # Create task instance
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False  # New tasks always start as incomplete
    )

    # Save to database
    session.add(task)
    session.commit()
    session.refresh(task)

    # Return response
    task_response = TaskResponse.model_validate(task)
    return ApiResponse.success_response(task_response)


@router.get(
    "/{user_id}/tasks/{task_id}",
    response_model=ApiResponse[TaskResponse],
    summary="Get a single task",
    description="Retrieve a specific task by ID"
)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
) -> ApiResponse[TaskResponse]:
    """Get a single task by ID.

    This endpoint retrieves a specific task. User isolation is enforced -
    users can only access their own tasks.

    Args:
        user_id: User ID from URL path
        task_id: Task ID to retrieve
        current_user: Authenticated user ID from JWT (injected)
        session: Database session (injected)

    Returns:
        ApiResponse containing the task

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user
        HTTPException: 404 if task not found
        HTTPException: 403 if task belongs to different user
    """
    # Verify user access
    verify_user_access(current_user, user_id)

    # Get task from database
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    # Verify task ownership
    verify_task_ownership(task.user_id, current_user)

    # Return response
    task_response = TaskResponse.model_validate(task)
    return ApiResponse.success_response(task_response)


@router.put(
    "/{user_id}/tasks/{task_id}",
    response_model=ApiResponse[TaskResponse],
    summary="Update a task (full)",
    description="Update a task with full replacement of fields"
)
async def update_task_full(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
) -> ApiResponse[TaskResponse]:
    """Update a task (full update).

    This endpoint updates a task. All provided fields will be updated.
    The updated_at timestamp is automatically updated by the database trigger.

    Args:
        user_id: User ID from URL path
        task_id: Task ID to update
        task_data: Updated task data (title, description, completed)
        current_user: Authenticated user ID from JWT (injected)
        session: Database session (injected)

    Returns:
        ApiResponse containing the updated task

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user
        HTTPException: 404 if task not found
        HTTPException: 403 if task belongs to different user
    """
    # Verify user access
    verify_user_access(current_user, user_id)

    # Get task from database
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    # Verify task ownership
    verify_task_ownership(task.user_id, current_user)

    # Update fields (only if provided)
    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.completed is not None:
        task.completed = task_data.completed

    # Save changes (updated_at auto-updated by trigger)
    session.add(task)
    session.commit()
    session.refresh(task)

    # Return response
    task_response = TaskResponse.model_validate(task)
    return ApiResponse.success_response(task_response)


@router.patch(
    "/{user_id}/tasks/{task_id}",
    response_model=ApiResponse[TaskResponse],
    summary="Update a task (partial)",
    description="Partially update a task (only specified fields)"
)
async def update_task_partial(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
) -> ApiResponse[TaskResponse]:
    """Update a task (partial update).

    This endpoint is identical to PUT but semantically indicates partial updates.
    Only provided fields will be updated.

    Args:
        user_id: User ID from URL path
        task_id: Task ID to update
        task_data: Updated task data (all fields optional)
        current_user: Authenticated user ID from JWT (injected)
        session: Database session (injected)

    Returns:
        ApiResponse containing the updated task

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user
        HTTPException: 404 if task not found
        HTTPException: 403 if task belongs to different user
    """
    # Reuse the PUT implementation (both do partial updates)
    return await update_task_full(user_id, task_id, task_data, current_user, session)


@router.patch(
    "/{user_id}/tasks/{task_id}/toggle",
    response_model=ApiResponse[TaskResponse],
    summary="Toggle task completion",
    description="Toggle the completion status of a task (convenience endpoint)"
)
async def toggle_task_completion(
    user_id: str,
    task_id: int,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
) -> ApiResponse[TaskResponse]:
    """Toggle task completion status.

    This is a convenience endpoint that flips the completed status:
    - If completed=True, sets to False
    - If completed=False, sets to True

    Args:
        user_id: User ID from URL path
        task_id: Task ID to toggle
        current_user: Authenticated user ID from JWT (injected)
        session: Database session (injected)

    Returns:
        ApiResponse containing the updated task

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user
        HTTPException: 404 if task not found
        HTTPException: 403 if task belongs to different user
    """
    # Verify user access
    verify_user_access(current_user, user_id)

    # Get task from database
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    # Verify task ownership
    verify_task_ownership(task.user_id, current_user)

    # Toggle completion status
    task.toggle_completion()

    # Save changes
    session.add(task)
    session.commit()
    session.refresh(task)

    # Return response
    task_response = TaskResponse.model_validate(task)
    return ApiResponse.success_response(task_response)


@router.delete(
    "/{user_id}/tasks/{task_id}",
    response_model=ApiResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Delete a task",
    description="Permanently delete a task"
)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
) -> ApiResponse[dict]:
    """Delete a task permanently.

    This endpoint permanently removes a task from the database.
    This operation cannot be undone.

    Args:
        user_id: User ID from URL path
        task_id: Task ID to delete
        current_user: Authenticated user ID from JWT (injected)
        session: Database session (injected)

    Returns:
        ApiResponse with success message

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user
        HTTPException: 404 if task not found
        HTTPException: 403 if task belongs to different user
    """
    # Verify user access
    verify_user_access(current_user, user_id)

    # Get task from database
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    # Verify task ownership
    verify_task_ownership(task.user_id, current_user)

    # Delete task
    session.delete(task)
    session.commit()

    # Return success message
    return ApiResponse.success_response({
        "message": f"Task {task_id} deleted successfully",
        "task_id": task_id
    })
