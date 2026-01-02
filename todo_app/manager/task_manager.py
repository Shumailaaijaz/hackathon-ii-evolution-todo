"""TaskManager business logic layer for the Todo application.

This module implements the TaskManager class which handles all CRUD operations
for tasks, including creation, retrieval, updates, deletion, and completion.
"""

from todo_app.models.task import Task


class TaskManager:
    """Manages todo tasks with CRUD operations and in-memory storage.

    TaskManager encapsulates all business logic for task management, including
    ID generation, validation, and storage operations. It uses a dictionary
    for O(1) task lookup performance and maintains an auto-incrementing ID
    counter.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task instances (private).
        _next_id: Counter for generating unique task IDs, starts at 1 (private).

    Example:
        >>> manager = TaskManager()
        >>> task = manager.add_task("Buy groceries")
        >>> task.id
        1
        >>> task.title
        'Buy groceries'
    """

    def __init__(self) -> None:
        """Initialize TaskManager with empty storage and ID counter at 1."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_and_trim_title(self, title: str) -> str:
        """Validate and trim a task title.

        Removes leading/trailing whitespace and validates that the resulting
        title is not empty. This centralized validation ensures consistent
        behavior across add_task and update_task operations.

        Args:
            title: The title string to validate and trim.

        Returns:
            str: The trimmed title with whitespace removed.

        Raises:
            ValueError: If the title is empty or contains only whitespace
                after trimming.
        """
        trimmed_title = title.strip()
        if not trimmed_title:
            raise ValueError("Task title cannot be empty")
        return trimmed_title

    def add_task(self, title: str) -> Task:
        """Create and store a new task with auto-generated ID.

        Validates the title (cannot be empty after trimming whitespace),
        generates a unique sequential ID, creates a Task instance, stores
        it in the internal dictionary, and returns the created task.

        Args:
            title: Description of the task to be created. Leading and trailing
                whitespace will be trimmed. Cannot be empty or whitespace-only.

        Returns:
            Task: The newly created Task instance with auto-generated ID and
                completed=False.

        Raises:
            ValueError: If title is empty or contains only whitespace after
                trimming.

        Example:
            >>> manager = TaskManager()
            >>> task = manager.add_task("  Buy milk  ")
            >>> task.id
            1
            >>> task.title
            'Buy milk'
            >>> task.completed
            False
        """
        # Validate and trim the title
        trimmed_title = self._validate_and_trim_title(title)

        # Create task with current ID and trimmed title
        task = Task(id=self._next_id, title=trimmed_title, completed=False)

        # Store task in dictionary
        self._tasks[task.id] = task

        # Increment ID counter for next task
        self._next_id += 1

        # Return the created task
        return task

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks sorted by ID (creation order).

        Returns all tasks from storage as a list, sorted by their ID in
        ascending order. This preserves the creation order since IDs are
        auto-incremented sequentially.

        Returns:
            list[Task]: List of all Task instances sorted by ID. Returns
                empty list if no tasks exist.

        Example:
            >>> manager = TaskManager()
            >>> manager.add_task("First")
            >>> manager.add_task("Second")
            >>> tasks = manager.get_all_tasks()
            >>> len(tasks)
            2
            >>> tasks[0].id
            1
            >>> tasks[1].id
            2
        """
        # Return tasks sorted by ID (creation order)
        return sorted(self._tasks.values(), key=lambda task: task.id)

    def get_task_by_id(self, task_id: int) -> Task:
        """Retrieve a specific task by its ID.

        Looks up and returns the task with the specified ID from storage.

        Args:
            task_id: The unique identifier of the task to retrieve.

        Returns:
            Task: The Task instance with the matching ID.

        Raises:
            KeyError: If no task exists with the given ID.

        Example:
            >>> manager = TaskManager()
            >>> task = manager.add_task("Buy milk")
            >>> retrieved = manager.get_task_by_id(1)
            >>> retrieved.title
            'Buy milk'
        """
        # Return task from dictionary (raises KeyError if not found)
        return self._tasks[task_id]

    def mark_complete(self, task_id: int) -> None:
        """Mark a task as completed.

        Sets the task's completed status to True. Raises an error if the
        task is already completed (to prevent redundant operations).

        Args:
            task_id: The unique identifier of the task to mark complete.

        Raises:
            KeyError: If no task exists with the given ID.
            RuntimeError: If the task is already marked as completed.

        Example:
            >>> manager = TaskManager()
            >>> task = manager.add_task("Buy milk")
            >>> manager.mark_complete(task.id)
            >>> task.completed
            True
        """
        # Get task (raises KeyError if not found)
        task = self._tasks[task_id]

        # Check if already completed
        if task.completed:
            raise RuntimeError(f"Task {task_id} is already complete")

        # Mark task as completed
        task.completed = True

    def delete_task(self, task_id: int) -> None:
        """Permanently delete a task from storage.

        Removes the task with the given ID from storage. The task ID is
        never reused, even after deletion (maintained by _next_id counter).

        Args:
            task_id: The unique identifier of the task to delete.

        Raises:
            KeyError: If no task exists with the given ID.

        Example:
            >>> manager = TaskManager()
            >>> task = manager.add_task("Temporary task")
            >>> manager.delete_task(task.id)
            >>> len(manager.get_all_tasks())
            0
        """
        # Delete task from dictionary (raises KeyError if not found)
        del self._tasks[task_id]

    def update_task(self, task_id: int, new_title: str) -> Task:
        """Update the title of an existing task.

        Changes the task's title to the new value after trimming whitespace.
        The task ID and completed status remain unchanged.

        Args:
            task_id: The unique identifier of the task to update.
            new_title: The new title for the task. Leading and trailing
                whitespace will be trimmed. Cannot be empty or whitespace-only.

        Returns:
            Task: The updated Task instance.

        Raises:
            KeyError: If no task exists with the given ID.
            ValueError: If new_title is empty or whitespace-only after trimming.

        Example:
            >>> manager = TaskManager()
            >>> task = manager.add_task("Old title")
            >>> updated = manager.update_task(task.id, "New title")
            >>> updated.title
            'New title'
        """
        # Get task (raises KeyError if not found)
        task = self._tasks[task_id]

        # Validate and trim the new title
        trimmed_title = self._validate_and_trim_title(new_title)

        # Update task title
        task.title = trimmed_title

        # Return updated task
        return task
