"""Tests for the Task data model.

This module contains comprehensive tests for the Task dataclass,
covering creation, validation, and attribute access.
"""

import pytest
from todo_app.models.task import Task


class TestTaskCreation:
    """Tests for Task instance creation."""

    def test_task_creation_with_valid_attributes(self) -> None:
        """Test creating a Task with all valid attributes."""
        # Given: Valid task attributes
        task_id = 1
        title = "Test Task"
        completed = False

        # When: Creating a Task instance
        task = Task(id=task_id, title=title, completed=completed)

        # Then: All attributes should be set correctly
        assert task.id == task_id
        assert task.title == title
        assert task.completed == completed

    def test_task_creation_defaults_completed_to_false(self) -> None:
        """Test that Task defaults completed to False when not provided."""
        # Given: Task ID and title only
        task_id = 1
        title = "Test Task"

        # When: Creating a Task without specifying completed
        task = Task(id=task_id, title=title)

        # Then: completed should default to False
        assert task.completed is False

    def test_task_attributes_are_accessible(self) -> None:
        """Test that Task attributes can be read after creation."""
        # Given: A created task
        task = Task(id=5, title="Accessible Task", completed=True)

        # When: Accessing attributes
        task_id = task.id
        title = task.title
        completed = task.completed

        # Then: Attributes should be accessible and correct
        assert task_id == 5
        assert title == "Accessible Task"
        assert completed is True

    def test_task_repr_includes_all_fields(self) -> None:
        """Test that Task __repr__ includes id, title, and completed."""
        # Given: A task with known values
        task = Task(id=10, title="Repr Task", completed=False)

        # When: Getting string representation
        repr_str = repr(task)

        # Then: Representation should contain all field values
        assert "10" in repr_str
        assert "Repr Task" in repr_str
        assert "False" in repr_str or "completed=False" in repr_str

    def test_task_title_can_be_modified(self) -> None:
        """Test that Task title is mutable (can be updated)."""
        # Given: A created task
        task = Task(id=1, title="Original Title")

        # When: Modifying the title
        task.title = "Updated Title"

        # Then: Title should be updated
        assert task.title == "Updated Title"

    def test_task_completed_can_be_modified(self) -> None:
        """Test that Task completed status is mutable (can be changed)."""
        # Given: A created task with completed=False
        task = Task(id=1, title="Task", completed=False)

        # When: Modifying completed status
        task.completed = True

        # Then: Completed status should be updated
        assert task.completed is True


class TestTaskValidation:
    """Tests for Task input validation in __post_init__."""

    def test_task_rejects_zero_id(self) -> None:
        """Test that Task raises ValueError for ID of 0."""
        # Given: Task ID of 0 (invalid)
        # When: Attempting to create Task with ID=0
        # Then: ValueError should be raised mentioning "positive integer"
        with pytest.raises(ValueError, match=r"positive integer"):
            Task(id=0, title="Test Task")

    def test_task_rejects_negative_id(self) -> None:
        """Test that Task raises ValueError for negative ID."""
        # Given: Negative task ID (invalid)
        # When: Attempting to create Task with negative ID
        # Then: ValueError should be raised
        with pytest.raises(ValueError, match=r"positive integer"):
            Task(id=-1, title="Test Task")

    def test_task_rejects_empty_title(self) -> None:
        """Test that Task raises ValueError for empty title."""
        # Given: Empty string title (invalid)
        # When: Attempting to create Task with empty title
        # Then: ValueError should be raised mentioning "cannot be empty"
        with pytest.raises(ValueError, match=r"cannot be empty"):
            Task(id=1, title="")

    def test_task_rejects_whitespace_only_title(self) -> None:
        """Test that Task raises ValueError for whitespace-only title."""
        # Given: Whitespace-only title (invalid)
        # When: Attempting to create Task with whitespace title
        # Then: ValueError should be raised mentioning "cannot be empty"
        with pytest.raises(ValueError, match=r"cannot be empty"):
            Task(id=1, title="   ")

    def test_task_accepts_valid_data(self) -> None:
        """Test that Task accepts valid ID and title (positive control)."""
        # Given: Valid task ID and title
        # When: Creating Task with valid data
        # Then: No exception should be raised
        task = Task(id=1, title="Valid Task")
        assert task.id == 1
        assert task.title == "Valid Task"
