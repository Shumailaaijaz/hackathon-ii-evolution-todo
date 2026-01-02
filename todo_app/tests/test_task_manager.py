"""Tests for the TaskManager business logic layer.

This module contains comprehensive tests for TaskManager CRUD operations,
including task creation, retrieval, updates, deletion, and completion.
"""

import pytest
from todo_app.manager.task_manager import TaskManager
from todo_app.models.task import Task


@pytest.fixture
def manager() -> TaskManager:
    """Provide a fresh TaskManager instance for each test.

    Returns:
        TaskManager: A new TaskManager instance with empty task storage.
    """
    return TaskManager()


class TestTaskManagerAddTask:
    """Tests for TaskManager.add_task method."""

    def test_add_first_task_generates_id_one(self, manager: TaskManager) -> None:
        """Test that the first task added gets ID 1."""
        # Given: A new TaskManager instance
        # When: Adding the first task
        task = manager.add_task("First task")

        # Then: Task should have ID 1
        assert task.id == 1

    def test_add_second_task_generates_id_two(self, manager: TaskManager) -> None:
        """Test that IDs increment sequentially (1, 2, 3,...)."""
        # Given: A TaskManager with one task already added
        first_task = manager.add_task("First task")

        # When: Adding a second task
        second_task = manager.add_task("Second task")

        # Then: IDs should be sequential
        assert first_task.id == 1
        assert second_task.id == 2

    def test_add_multiple_tasks_increments_ids(self, manager: TaskManager) -> None:
        """Test that adding multiple tasks increments IDs correctly."""
        # Given: A new TaskManager
        # When: Adding three tasks
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        task3 = manager.add_task("Task 3")

        # Then: IDs should be 1, 2, 3
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_trims_whitespace(self, manager: TaskManager) -> None:
        """Test that add_task trims leading/trailing whitespace from title."""
        # Given: A title with whitespace
        title_with_whitespace = "  Test Task  "

        # When: Adding task with whitespace
        task = manager.add_task(title_with_whitespace)

        # Then: Title should be trimmed
        assert task.title == "Test Task"

    def test_add_task_raises_error_for_empty_title(
        self, manager: TaskManager
    ) -> None:
        """Test that add_task raises ValueError for empty title."""
        # Given: An empty string title
        # When: Attempting to add task with empty title
        # Then: ValueError should be raised
        with pytest.raises(ValueError, match=r"cannot be empty"):
            manager.add_task("")

    def test_add_task_raises_error_for_whitespace_only_title(
        self, manager: TaskManager
    ) -> None:
        """Test that add_task raises ValueError for whitespace-only title."""
        # Given: A whitespace-only title
        # When: Attempting to add task with whitespace title
        # Then: ValueError should be raised
        with pytest.raises(ValueError, match=r"cannot be empty"):
            manager.add_task("   ")

    def test_add_task_returns_task_with_completed_false(
        self, manager: TaskManager
    ) -> None:
        """Test that newly added tasks have completed=False."""
        # Given: A new task being added
        # When: Adding the task
        task = manager.add_task("New task")

        # Then: Task should not be completed
        assert task.completed is False

    def test_add_task_returns_task_instance(self, manager: TaskManager) -> None:
        """Test that add_task returns a Task instance."""
        # Given: A title for a new task
        # When: Adding the task
        task = manager.add_task("Test task")

        # Then: Returned value should be a Task instance
        assert isinstance(task, Task)

    def test_add_task_with_title_preserves_content(
        self, manager: TaskManager
    ) -> None:
        """Test that task title content is preserved correctly."""
        # Given: A specific title
        title = "Buy groceries and cook dinner"

        # When: Adding task with that title
        task = manager.add_task(title)

        # Then: Title should match exactly
        assert task.title == title


class TestTaskManagerGetAllTasks:
    """Tests for TaskManager.get_all_tasks method."""

    def test_get_all_tasks_returns_empty_list_initially(
        self, manager: TaskManager
    ) -> None:
        """Test that get_all_tasks returns empty list for new manager."""
        # Given: A new TaskManager with no tasks
        # When: Getting all tasks
        tasks = manager.get_all_tasks()

        # Then: Should return empty list
        assert tasks == []
        assert len(tasks) == 0

    def test_get_all_tasks_returns_single_task(self, manager: TaskManager) -> None:
        """Test that get_all_tasks returns list with one task after adding."""
        # Given: A TaskManager with one task added
        added_task = manager.add_task("Single task")

        # When: Getting all tasks
        tasks = manager.get_all_tasks()

        # Then: Should return list with that task
        assert len(tasks) == 1
        assert tasks[0] == added_task

    def test_get_all_tasks_returns_tasks_in_id_order(
        self, manager: TaskManager
    ) -> None:
        """Test that tasks are returned sorted by ID (creation order)."""
        # Given: Multiple tasks added
        task1 = manager.add_task("First task")
        task2 = manager.add_task("Second task")
        task3 = manager.add_task("Third task")

        # When: Getting all tasks
        tasks = manager.get_all_tasks()

        # Then: Tasks should be in ID order (1, 2, 3)
        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3
        assert tasks[0] == task1
        assert tasks[1] == task2
        assert tasks[2] == task3

    def test_get_all_tasks_returns_list_not_dict(
        self, manager: TaskManager
    ) -> None:
        """Test that get_all_tasks returns a list, not a dict."""
        # Given: A TaskManager with tasks
        manager.add_task("Task 1")
        manager.add_task("Task 2")

        # When: Getting all tasks
        tasks = manager.get_all_tasks()

        # Then: Result should be a list
        assert isinstance(tasks, list)
        assert not isinstance(tasks, dict)


class TestTaskManagerGetTaskById:
    """Tests for TaskManager.get_task_by_id method."""

    def test_get_task_by_id_returns_correct_task(
        self, manager: TaskManager
    ) -> None:
        """Test that get_task_by_id returns the task with matching ID."""
        # Given: Multiple tasks added
        task1 = manager.add_task("First task")
        task2 = manager.add_task("Second task")
        task3 = manager.add_task("Third task")

        # When: Getting task by ID 2
        retrieved_task = manager.get_task_by_id(2)

        # Then: Should return the second task
        assert retrieved_task == task2
        assert retrieved_task.id == 2
        assert retrieved_task.title == "Second task"

    def test_get_task_by_id_raises_key_error_for_nonexistent_id(
        self, manager: TaskManager
    ) -> None:
        """Test that get_task_by_id raises KeyError for non-existent ID."""
        # Given: A TaskManager with one task (ID 1)
        manager.add_task("Only task")

        # When: Attempting to get task with non-existent ID
        # Then: KeyError should be raised
        with pytest.raises(KeyError):
            manager.get_task_by_id(999)

    def test_get_task_by_id_raises_key_error_for_empty_manager(
        self, manager: TaskManager
    ) -> None:
        """Test that get_task_by_id raises KeyError when no tasks exist."""
        # Given: A new TaskManager with no tasks
        # When: Attempting to get any task
        # Then: KeyError should be raised
        with pytest.raises(KeyError):
            manager.get_task_by_id(1)


class TestTaskManagerMarkComplete:
    """Tests for TaskManager.mark_complete method."""

    def test_mark_complete_sets_completed_to_true(
        self, manager: TaskManager
    ) -> None:
        """Test that mark_complete sets task's completed status to True."""
        # Given: A task that is not completed
        task = manager.add_task("Incomplete task")
        assert task.completed is False

        # When: Marking task as complete
        manager.mark_complete(task.id)

        # Then: Task should be marked as completed
        updated_task = manager.get_task_by_id(task.id)
        assert updated_task.completed is True

    def test_mark_complete_raises_error_for_already_completed_task(
        self, manager: TaskManager
    ) -> None:
        """Test that marking an already-completed task raises RuntimeError."""
        # Given: A task that is already completed
        task = manager.add_task("Task")
        manager.mark_complete(task.id)
        assert task.completed is True

        # When: Attempting to mark it complete again
        # Then: RuntimeError should be raised
        with pytest.raises(RuntimeError, match=r"already.*complete"):
            manager.mark_complete(task.id)

    def test_mark_complete_raises_key_error_for_nonexistent_task(
        self, manager: TaskManager
    ) -> None:
        """Test that mark_complete raises KeyError for non-existent task."""
        # Given: A TaskManager with no tasks
        # When: Attempting to mark non-existent task complete
        # Then: KeyError should be raised
        with pytest.raises(KeyError):
            manager.mark_complete(999)

    def test_mark_complete_does_not_affect_other_tasks(
        self, manager: TaskManager
    ) -> None:
        """Test that marking one task complete doesn't affect others."""
        # Given: Multiple tasks
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        task3 = manager.add_task("Task 3")

        # When: Marking only task2 as complete
        manager.mark_complete(task2.id)

        # Then: Only task2 should be completed
        assert manager.get_task_by_id(task1.id).completed is False
        assert manager.get_task_by_id(task2.id).completed is True
        assert manager.get_task_by_id(task3.id).completed is False


class TestTaskManagerDeleteTask:
    """Tests for TaskManager.delete_task method."""

    def test_delete_task_removes_task_from_storage(
        self, manager: TaskManager
    ) -> None:
        """Test that delete_task removes the task from storage."""
        # Given: A task in storage
        task = manager.add_task("Task to delete")
        assert len(manager.get_all_tasks()) == 1

        # When: Deleting the task
        manager.delete_task(task.id)

        # Then: Task should be removed
        assert len(manager.get_all_tasks()) == 0
        with pytest.raises(KeyError):
            manager.get_task_by_id(task.id)

    def test_delete_task_raises_key_error_for_nonexistent_task(
        self, manager: TaskManager
    ) -> None:
        """Test that delete_task raises KeyError for non-existent task."""
        # Given: TaskManager with no tasks
        # When: Attempting to delete non-existent task
        # Then: KeyError should be raised
        with pytest.raises(KeyError):
            manager.delete_task(999)

    def test_delete_task_does_not_affect_other_tasks(
        self, manager: TaskManager
    ) -> None:
        """Test that deleting one task doesn't affect others."""
        # Given: Multiple tasks
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        task3 = manager.add_task("Task 3")

        # When: Deleting task2
        manager.delete_task(task2.id)

        # Then: task1 and task3 should remain
        all_tasks = manager.get_all_tasks()
        assert len(all_tasks) == 2
        assert task1 in all_tasks
        assert task3 in all_tasks
        assert task2 not in all_tasks

    def test_delete_task_does_not_reuse_deleted_ids(
        self, manager: TaskManager
    ) -> None:
        """Test that IDs are never reused after deletion (ADR-003).

        Critical test validating that the auto-increment counter never
        decrements, ensuring deleted task IDs are never recycled for new tasks.
        This maintains ID uniqueness and preserves creation order semantics.
        """
        # Given: Add task with ID 1, then delete it
        task1 = manager.add_task("First task")
        first_id = task1.id
        assert first_id == 1
        manager.delete_task(first_id)

        # When: Add new task after deletion
        task2 = manager.add_task("Second task")

        # Then: New task should have ID 2, not reuse ID 1
        assert task2.id == 2
        assert task2.id != first_id

        # Further validation: delete multiple and verify IDs continue incrementing
        task3 = manager.add_task("Third task")
        assert task3.id == 3
        manager.delete_task(2)  # Delete task2
        manager.delete_task(3)  # Delete task3

        task4 = manager.add_task("Fourth task")
        assert task4.id == 4  # Should be 4, not 2 or 3


class TestTaskManagerUpdateTask:
    """Tests for TaskManager.update_task method."""

    def test_update_task_changes_title(self, manager: TaskManager) -> None:
        """Test that update_task changes the task's title."""
        # Given: A task with original title
        task = manager.add_task("Original title")
        original_id = task.id

        # When: Updating the task title
        updated_task = manager.update_task(task.id, "New title")

        # Then: Title should be updated, ID unchanged
        assert updated_task.id == original_id
        assert updated_task.title == "New title"
        assert manager.get_task_by_id(task.id).title == "New title"

    def test_update_task_trims_whitespace(self, manager: TaskManager) -> None:
        """Test that update_task trims whitespace from new title."""
        # Given: A task
        task = manager.add_task("Original")

        # When: Updating with whitespace
        updated = manager.update_task(task.id, "  New Title  ")

        # Then: Whitespace should be trimmed
        assert updated.title == "New Title"

    def test_update_task_raises_error_for_empty_title(
        self, manager: TaskManager
    ) -> None:
        """Test that update_task raises ValueError for empty title."""
        # Given: A task
        task = manager.add_task("Original")

        # When: Attempting to update with empty title
        # Then: ValueError should be raised
        with pytest.raises(ValueError, match=r"cannot be empty"):
            manager.update_task(task.id, "")

    def test_update_task_raises_error_for_whitespace_only_title(
        self, manager: TaskManager
    ) -> None:
        """Test that update_task raises ValueError for whitespace-only title."""
        # Given: A task
        task = manager.add_task("Original")

        # When: Attempting to update with whitespace
        # Then: ValueError should be raised
        with pytest.raises(ValueError, match=r"cannot be empty"):
            manager.update_task(task.id, "   ")

    def test_update_task_raises_key_error_for_nonexistent_task(
        self, manager: TaskManager
    ) -> None:
        """Test that update_task raises KeyError for non-existent task."""
        # Given: TaskManager with no tasks
        # When: Attempting to update non-existent task
        # Then: KeyError should be raised
        with pytest.raises(KeyError):
            manager.update_task(999, "New title")

    def test_update_task_does_not_change_completed_status(
        self, manager: TaskManager
    ) -> None:
        """Test that updating title doesn't affect completed status."""
        # Given: A completed task
        task = manager.add_task("Task")
        manager.mark_complete(task.id)
        assert task.completed is True

        # When: Updating the title
        manager.update_task(task.id, "Updated")

        # Then: Completed status should remain True
        assert manager.get_task_by_id(task.id).completed is True
