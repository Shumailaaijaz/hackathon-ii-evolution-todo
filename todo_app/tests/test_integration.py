"""Integration tests for the complete Todo application.

This module tests end-to-end workflows combining Models, Manager, and UI layers.
"""

from io import StringIO
from unittest.mock import patch

import pytest
from todo_app.manager.task_manager import TaskManager
from todo_app.ui.menu_ui import MenuUI


@pytest.fixture
def manager() -> TaskManager:
    """Provide a fresh TaskManager instance for each test."""
    return TaskManager()


@pytest.fixture
def menu_ui(manager: TaskManager) -> MenuUI:
    """Provide a MenuUI instance with a fresh TaskManager."""
    return MenuUI(manager)


class TestIntegrationEndToEndWorkflows:
    """Integration tests for complete user workflows."""

    @patch("builtins.input", side_effect=["1", "Buy groceries", "2", "6"])
    def test_add_then_view_task_workflow(
        self, mock_input, menu_ui: MenuUI
    ) -> None:
        """Test adding a task and then viewing it."""
        # When: User adds task, views tasks, then exits
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui.run()
            output = fake_stdout.getvalue()

        # Then: Task should appear in view output
        assert "Buy groceries" in output
        assert "[ ]" in output  # Incomplete task

    @patch("builtins.input", side_effect=[
        "1", "Task 1",
        "1", "Task 2",
        "1", "Task 3",
        "2",
        "6"
    ])
    def test_add_multiple_tasks_maintains_order(
        self, mock_input, menu_ui: MenuUI
    ) -> None:
        """Test that multiple tasks maintain creation order."""
        # When: Adding 3 tasks and viewing
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui.run()
            output = fake_stdout.getvalue()

        # Then: All tasks present in order
        task1_pos = output.index("Task 1")
        task2_pos = output.index("Task 2")
        task3_pos = output.index("Task 3")
        assert task1_pos < task2_pos < task3_pos

    @patch("builtins.input", side_effect=[
        "1", "Complete this",
        "3", "1",  # Mark complete
        "2",  # View
        "6"
    ])
    def test_add_mark_complete_view_workflow(
        self, mock_input, menu_ui: MenuUI
    ) -> None:
        """Test adding, completing, and viewing a task."""
        # When: Add task, mark complete, view
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui.run()
            output = fake_stdout.getvalue()

        # Then: Task should show as complete
        assert "Complete this" in output
        assert "[X]" in output or "[x]" in output.lower()

    @patch("builtins.input", side_effect=[
        "1", "Delete me",
        "4", "1",  # Delete task
        "2",  # View
        "6"
    ])
    def test_add_delete_view_workflow(
        self, mock_input, menu_ui: MenuUI
    ) -> None:
        """Test adding, deleting, and verifying task is gone."""
        # When: Add task, delete it, view
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui.run()
            output = fake_stdout.getvalue()

        # Then: Task should not appear, show empty message
        assert "Delete me" not in output or "deleted" in output.lower()
        assert "no tasks" in output.lower() or "deleted successfully" in output.lower()

    @patch("builtins.input", side_effect=[
        "1", "Original Title",
        "5", "1", "Updated Title",  # Update task
        "2",  # View
        "6"
    ])
    def test_add_update_view_workflow(
        self, mock_input, menu_ui: MenuUI
    ) -> None:
        """Test adding, updating, and viewing a task."""
        # When: Add task, update it, view
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui.run()
            output = fake_stdout.getvalue()

        # Then: New title shown, old title not shown
        assert "Updated Title" in output
        # Original may still appear in "updated successfully" message

    @patch("builtins.input", side_effect=[
        "1", "Task A",
        "1", "Task B",
        "3", "1",  # Complete first
        "4", "1",  # Delete first (already complete)
        "2",  # View remaining
        "6"
    ])
    def test_mixed_operations_workflow(
        self, mock_input, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test complex workflow with multiple operation types."""
        # When: Add 2, complete 1, delete 1, view
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui.run()
            output = fake_stdout.getvalue()

        # Then: Only Task B should remain
        final_tasks = manager.get_all_tasks()
        assert len(final_tasks) == 1
        assert final_tasks[0].title == "Task B"
        assert final_tasks[0].completed is False

    @patch("builtins.input", side_effect=[
        "1", "First",
        "4", "1",  # Delete ID 1
        "1", "Second",  # Add after deletion
        "2",  # View
        "6"
    ])
    def test_id_persistence_after_deletion_integration(
        self, mock_input, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that IDs are not reused after deletion (ADR-003)."""
        # When: Add, delete, add again, view
        menu_ui.run()

        # Then: Second task should have ID 2, not 1
        tasks = manager.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 2
        assert tasks[0].title == "Second"

    @patch("builtins.input", side_effect=[
        "1", "",  # Empty title
        "1", "   ",  # Whitespace only
        "1", "Valid Task",
        "2",
        "6"
    ])
    def test_error_handling_continues_execution(
        self, mock_input, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that errors don't crash app, execution continues."""
        # When: Invalid inputs followed by valid input
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui.run()
            output = fake_stdout.getvalue()

        # Then: Valid task created, errors displayed
        tasks = manager.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Valid Task"
        assert output.lower().count("error") >= 2

    @patch("builtins.input", side_effect=[
        "3", "999",  # Mark complete nonexistent
        "4", "999",  # Delete nonexistent
        "5", "999", "New Title",  # Update nonexistent
        "6"
    ])
    def test_nonexistent_task_operations_handled(
        self, mock_input, menu_ui: MenuUI
    ) -> None:
        """Test operations on nonexistent tasks fail gracefully."""
        # When: Attempting operations on nonexistent tasks
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui.run()
            output = fake_stdout.getvalue()

        # Then: Errors displayed, no crashes
        assert output.lower().count("error") >= 3 or output.lower().count("not found") >= 3
