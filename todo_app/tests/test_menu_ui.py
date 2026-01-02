"""Tests for the MenuUI presentation layer.

This module contains comprehensive tests for the MenuUI class,
covering display methods, user workflows, and input handling.
"""

from io import StringIO
from unittest.mock import MagicMock, patch

import pytest
from todo_app.manager.task_manager import TaskManager
from todo_app.models.task import Task
from todo_app.ui.menu_ui import MenuUI


@pytest.fixture
def manager() -> TaskManager:
    """Provide a fresh TaskManager instance for each test.

    Returns:
        TaskManager: A new TaskManager instance with empty task storage.
    """
    return TaskManager()


@pytest.fixture
def menu_ui(manager: TaskManager) -> MenuUI:
    """Provide a MenuUI instance with a fresh TaskManager.

    Args:
        manager: The TaskManager fixture.

    Returns:
        MenuUI: A new MenuUI instance connected to the manager.
    """
    return MenuUI(manager)


class TestMenuUIDisplayMethods:
    """Tests for MenuUI display methods."""

    def test_display_menu_shows_all_options(self, menu_ui: MenuUI) -> None:
        """Test that display_menu shows all available menu options."""
        # Given: A MenuUI instance
        # When: Displaying the menu
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui.display_menu()
            output = fake_stdout.getvalue()

        # Then: Output should contain all menu options
        assert "1" in output  # Add task option
        assert "2" in output  # View tasks option
        assert "3" in output  # Mark complete option
        assert "4" in output  # Delete task option
        assert "5" in output  # Update task option
        assert "6" in output  # Exit option
        assert "add" in output.lower() or "create" in output.lower()
        assert "view" in output.lower() or "list" in output.lower()
        assert "complete" in output.lower() or "done" in output.lower()
        assert "delete" in output.lower() or "remove" in output.lower()
        assert "update" in output.lower() or "edit" in output.lower()
        assert "exit" in output.lower() or "quit" in output.lower()

    def test_display_menu_has_title(self, menu_ui: MenuUI) -> None:
        """Test that display_menu includes a title or header."""
        # Given: A MenuUI instance
        # When: Displaying the menu
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui.display_menu()
            output = fake_stdout.getvalue()

        # Then: Output should have a title/header
        assert "todo" in output.lower() or "menu" in output.lower()

    def test_format_task_list_empty_returns_empty_message(
        self, menu_ui: MenuUI
    ) -> None:
        """Test that formatting empty task list returns appropriate message."""
        # Given: An empty task list
        tasks: list[Task] = []

        # When: Formatting the task list
        formatted = menu_ui._format_task_list(tasks)

        # Then: Should return message indicating no tasks
        assert "no tasks" in formatted.lower() or "empty" in formatted.lower()

    def test_format_task_list_single_task_includes_all_fields(
        self, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that formatting single task includes ID, title, and status."""
        # Given: A task list with one task
        task = manager.add_task("Buy groceries")
        tasks = [task]

        # When: Formatting the task list
        formatted = menu_ui._format_task_list(tasks)

        # Then: Output should include task ID, title, and completion status
        assert str(task.id) in formatted
        assert "Buy groceries" in formatted
        assert "[ ]" in formatted or "incomplete" in formatted.lower()

    def test_format_task_list_completed_task_shows_checkmark(
        self, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that completed tasks are visually distinguished."""
        # Given: A completed task
        task = manager.add_task("Completed task")
        manager.mark_complete(task.id)
        tasks = [task]

        # When: Formatting the task list
        formatted = menu_ui._format_task_list(tasks)

        # Then: Should show completed status (checkmark or similar)
        assert "[x]" in formatted.lower() or "[✓]" in formatted or "complete" in formatted.lower()

    def test_format_task_list_multiple_tasks_all_shown(
        self, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that all tasks in list are formatted and displayed."""
        # Given: Multiple tasks
        task1 = manager.add_task("First task")
        task2 = manager.add_task("Second task")
        task3 = manager.add_task("Third task")
        tasks = [task1, task2, task3]

        # When: Formatting the task list
        formatted = menu_ui._format_task_list(tasks)

        # Then: All tasks should be present in output
        assert "First task" in formatted
        assert "Second task" in formatted
        assert "Third task" in formatted
        assert str(task1.id) in formatted
        assert str(task2.id) in formatted
        assert str(task3.id) in formatted

    def test_format_task_list_preserves_task_order(
        self, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that tasks are formatted in the order provided."""
        # Given: Tasks in specific order
        task1 = manager.add_task("First")
        task2 = manager.add_task("Second")
        tasks = [task1, task2]

        # When: Formatting the task list
        formatted = menu_ui._format_task_list(tasks)

        # Then: "First" should appear before "Second" in output
        first_pos = formatted.index("First")
        second_pos = formatted.index("Second")
        assert first_pos < second_pos


class TestMenuUIAddTaskWorkflow:
    """Tests for MenuUI add task workflow (_handle_add_task)."""

    @patch("builtins.input", return_value="Buy groceries")
    def test_handle_add_task_prompts_for_title(
        self, mock_input: MagicMock, menu_ui: MenuUI
    ) -> None:
        """Test that _handle_add_task prompts user for task title."""
        # Given: User will input "Buy groceries"
        # When: Handling add task
        menu_ui._handle_add_task()

        # Then: Should have prompted for input
        mock_input.assert_called_once()
        call_args = str(mock_input.call_args).lower()
        assert "title" in call_args or "task" in call_args

    @patch("builtins.input", return_value="Buy groceries")
    def test_handle_add_task_creates_task_via_manager(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_add_task calls manager.add_task."""
        # Given: User inputs valid title
        # When: Handling add task
        menu_ui._handle_add_task()

        # Then: Task should be created in manager
        tasks = manager.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Buy groceries"

    @patch("builtins.input", return_value="New task")
    def test_handle_add_task_displays_success_message(
        self, mock_input: MagicMock, menu_ui: MenuUI
    ) -> None:
        """Test that _handle_add_task displays success confirmation."""
        # Given: User inputs valid title
        # When: Handling add task
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_add_task()
            output = fake_stdout.getvalue()

        # Then: Should display success message
        assert "added" in output.lower() or "created" in output.lower()

    @patch("builtins.input", return_value="")
    def test_handle_add_task_handles_empty_input(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_add_task handles empty input gracefully."""
        # Given: User inputs empty string
        # When: Handling add task
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_add_task()
            output = fake_stdout.getvalue()

        # Then: Should display error message and not create task
        assert "error" in output.lower() or "empty" in output.lower() or "cannot" in output.lower()
        assert len(manager.get_all_tasks()) == 0

    @patch("builtins.input", return_value="   ")
    def test_handle_add_task_handles_whitespace_only_input(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_add_task rejects whitespace-only input."""
        # Given: User inputs whitespace only
        # When: Handling add task
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_add_task()
            output = fake_stdout.getvalue()

        # Then: Should display error and not create task
        assert "error" in output.lower() or "empty" in output.lower()
        assert len(manager.get_all_tasks()) == 0


class TestMenuUIViewTasksWorkflow:
    """Tests for MenuUI view tasks workflow (_handle_view_tasks)."""

    def test_handle_view_tasks_displays_empty_message_when_no_tasks(
        self, menu_ui: MenuUI
    ) -> None:
        """Test that viewing with no tasks shows appropriate message."""
        # Given: No tasks in manager
        # When: Handling view tasks
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_view_tasks()
            output = fake_stdout.getvalue()

        # Then: Should display "no tasks" message
        assert "no tasks" in output.lower() or "empty" in output.lower()

    def test_handle_view_tasks_displays_all_tasks(
        self, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that all tasks are displayed when viewing."""
        # Given: Multiple tasks exist
        manager.add_task("First task")
        manager.add_task("Second task")
        manager.add_task("Third task")

        # When: Handling view tasks
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_view_tasks()
            output = fake_stdout.getvalue()

        # Then: All tasks should be in output
        assert "First task" in output
        assert "Second task" in output
        assert "Third task" in output

    def test_handle_view_tasks_shows_task_ids(
        self, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that task IDs are displayed."""
        # Given: Tasks with specific IDs
        task1 = manager.add_task("Task one")
        task2 = manager.add_task("Task two")

        # When: Handling view tasks
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_view_tasks()
            output = fake_stdout.getvalue()

        # Then: Task IDs should be visible
        assert str(task1.id) in output
        assert str(task2.id) in output

    def test_handle_view_tasks_distinguishes_completed_tasks(
        self, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that completed tasks are visually different from incomplete."""
        # Given: One completed and one incomplete task
        incomplete = manager.add_task("Incomplete task")
        complete = manager.add_task("Complete task")
        manager.mark_complete(complete.id)

        # When: Handling view tasks
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_view_tasks()
            output = fake_stdout.getvalue()

        # Then: Should show different status indicators
        assert "[ ]" in output or "incomplete" in output.lower()
        assert "[x]" in output.lower() or "[✓]" in output or "complete" in output.lower()


class TestMenuUIMarkCompleteWorkflow:
    """Tests for MenuUI mark complete workflow (_handle_mark_complete)."""

    @patch("builtins.input", return_value="1")
    def test_handle_mark_complete_prompts_for_task_id(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_mark_complete prompts for task ID."""
        # Given: A task exists
        manager.add_task("Test task")

        # When: Handling mark complete
        menu_ui._handle_mark_complete()

        # Then: Should have prompted for ID
        mock_input.assert_called_once()

    @patch("builtins.input", return_value="1")
    def test_handle_mark_complete_marks_task_complete(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_mark_complete calls manager.mark_complete."""
        # Given: An incomplete task
        task = manager.add_task("Task to complete")
        assert task.completed is False

        # When: Handling mark complete for task ID 1
        menu_ui._handle_mark_complete()

        # Then: Task should be marked complete
        assert manager.get_task_by_id(1).completed is True

    @patch("builtins.input", return_value="1")
    def test_handle_mark_complete_displays_success_message(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_mark_complete shows success confirmation."""
        # Given: A task to complete
        manager.add_task("Task")

        # When: Handling mark complete
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_mark_complete()
            output = fake_stdout.getvalue()

        # Then: Should display success message
        assert "complete" in output.lower() or "marked" in output.lower()

    @patch("builtins.input", return_value="999")
    def test_handle_mark_complete_handles_nonexistent_task(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_mark_complete handles invalid task ID."""
        # Given: No task with ID 999
        manager.add_task("Task 1")

        # When: Attempting to mark nonexistent task complete
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_mark_complete()
            output = fake_stdout.getvalue()

        # Then: Should display error message
        assert "error" in output.lower() or "not found" in output.lower()

    @patch("builtins.input", return_value="1")
    def test_handle_mark_complete_handles_already_complete_task(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_mark_complete handles already-completed task."""
        # Given: An already completed task
        task = manager.add_task("Task")
        manager.mark_complete(task.id)

        # When: Attempting to mark it complete again
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_mark_complete()
            output = fake_stdout.getvalue()

        # Then: Should display error about already complete
        assert "error" in output.lower() or "already" in output.lower()

    @patch("builtins.input", return_value="invalid")
    def test_handle_mark_complete_handles_invalid_id_format(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_mark_complete handles non-numeric ID input."""
        # Given: A task exists
        manager.add_task("Task")

        # When: User inputs non-numeric ID
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_mark_complete()
            output = fake_stdout.getvalue()

        # Then: Should display error about invalid input
        assert "error" in output.lower() or "invalid" in output.lower()


class TestMenuUIDeleteTaskWorkflow:
    """Tests for MenuUI delete task workflow (_handle_delete_task)."""

    @patch("builtins.input", return_value="1")
    def test_handle_delete_task_prompts_for_task_id(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_delete_task prompts for task ID."""
        # Given: A task exists
        manager.add_task("Test task")

        # When: Handling delete task
        menu_ui._handle_delete_task()

        # Then: Should have prompted for ID
        mock_input.assert_called_once()

    @patch("builtins.input", return_value="1")
    def test_handle_delete_task_deletes_task(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_delete_task removes task from manager."""
        # Given: A task exists
        manager.add_task("Task to delete")
        assert len(manager.get_all_tasks()) == 1

        # When: Handling delete for task ID 1
        menu_ui._handle_delete_task()

        # Then: Task should be deleted
        assert len(manager.get_all_tasks()) == 0

    @patch("builtins.input", return_value="1")
    def test_handle_delete_task_displays_success_message(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_delete_task shows confirmation."""
        # Given: A task to delete
        manager.add_task("Task")

        # When: Handling delete
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_delete_task()
            output = fake_stdout.getvalue()

        # Then: Should display success message
        assert "delete" in output.lower() or "removed" in output.lower()

    @patch("builtins.input", return_value="999")
    def test_handle_delete_task_handles_nonexistent_task(
        self, mock_input: MagicMock, menu_ui: MenuUI
    ) -> None:
        """Test that _handle_delete_task handles invalid task ID."""
        # Given: No task with ID 999
        # When: Attempting to delete nonexistent task
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_delete_task()
            output = fake_stdout.getvalue()

        # Then: Should display error message
        assert "error" in output.lower() or "not found" in output.lower()

    @patch("builtins.input", return_value="invalid")
    def test_handle_delete_task_handles_invalid_id_format(
        self, mock_input: MagicMock, menu_ui: MenuUI
    ) -> None:
        """Test that _handle_delete_task handles non-numeric ID."""
        # Given: User inputs non-numeric ID
        # When: Handling delete
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_delete_task()
            output = fake_stdout.getvalue()

        # Then: Should display error about invalid input
        assert "error" in output.lower() or "invalid" in output.lower()


class TestMenuUIUpdateTaskWorkflow:
    """Tests for MenuUI update task workflow (_handle_update_task)."""

    @patch("builtins.input", side_effect=["1", "Updated title"])
    def test_handle_update_task_prompts_for_id_and_title(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_update_task prompts for ID and new title."""
        # Given: A task exists
        manager.add_task("Original title")

        # When: Handling update task
        menu_ui._handle_update_task()

        # Then: Should have prompted twice (ID and title)
        assert mock_input.call_count == 2

    @patch("builtins.input", side_effect=["1", "New title"])
    def test_handle_update_task_updates_task_title(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_update_task changes task title."""
        # Given: A task with original title
        task = manager.add_task("Original")
        assert task.title == "Original"

        # When: Updating task with ID 1
        menu_ui._handle_update_task()

        # Then: Title should be updated
        updated = manager.get_task_by_id(1)
        assert updated.title == "New title"

    @patch("builtins.input", side_effect=["1", "Updated"])
    def test_handle_update_task_displays_success_message(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_update_task shows confirmation."""
        # Given: A task to update
        manager.add_task("Task")

        # When: Handling update
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_update_task()
            output = fake_stdout.getvalue()

        # Then: Should display success message
        assert "update" in output.lower() or "changed" in output.lower()

    @patch("builtins.input", side_effect=["999", "New title"])
    def test_handle_update_task_handles_nonexistent_task(
        self, mock_input: MagicMock, menu_ui: MenuUI
    ) -> None:
        """Test that _handle_update_task handles invalid task ID."""
        # Given: No task with ID 999
        # When: Attempting to update nonexistent task
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_update_task()
            output = fake_stdout.getvalue()

        # Then: Should display error message
        assert "error" in output.lower() or "not found" in output.lower()

    @patch("builtins.input", side_effect=["1", ""])
    def test_handle_update_task_handles_empty_title(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that _handle_update_task rejects empty title."""
        # Given: A task exists
        manager.add_task("Original")

        # When: Attempting to update with empty title
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_update_task()
            output = fake_stdout.getvalue()

        # Then: Should display error about empty title
        assert "error" in output.lower() or "empty" in output.lower()

    @patch("builtins.input", side_effect=["invalid", "New title"])
    def test_handle_update_task_handles_invalid_id_format(
        self, mock_input: MagicMock, menu_ui: MenuUI
    ) -> None:
        """Test that _handle_update_task handles non-numeric ID."""
        # Given: User inputs non-numeric ID
        # When: Handling update
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui._handle_update_task()
            output = fake_stdout.getvalue()

        # Then: Should display error about invalid input
        assert "error" in output.lower() or "invalid" in output.lower()


class TestMenuUIRunMainLoop:
    """Tests for MenuUI.run main loop."""

    @patch("builtins.input", return_value="6")
    def test_run_exits_on_option_6(
        self, mock_input: MagicMock, menu_ui: MenuUI
    ) -> None:
        """Test that run() exits when user selects option 6."""
        # Given: User will choose exit (6)
        # When: Running main loop
        menu_ui.run()

        # Then: Should have prompted for choice and exited cleanly
        mock_input.assert_called()

    @patch("builtins.input", side_effect=["1", "Test task", "6"])
    def test_run_handles_add_task_option(
        self, mock_input: MagicMock, menu_ui: MenuUI, manager: TaskManager
    ) -> None:
        """Test that run() calls add task handler for option 1."""
        # Given: User chooses add (1), enters title, then exits (6)
        # When: Running main loop
        menu_ui.run()

        # Then: Task should be created
        tasks = manager.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Test task"

    @patch("builtins.input", side_effect=["2", "6"])
    def test_run_handles_view_tasks_option(
        self, mock_input: MagicMock, menu_ui: MenuUI
    ) -> None:
        """Test that run() calls view tasks handler for option 2."""
        # Given: User chooses view (2), then exits (6)
        # When: Running main loop
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui.run()
            output = fake_stdout.getvalue()

        # Then: Should display tasks (even if empty)
        assert "no tasks" in output.lower() or "menu" in output.lower()

    @patch("builtins.input", side_effect=["invalid", "6"])
    def test_run_handles_invalid_option(
        self, mock_input: MagicMock, menu_ui: MenuUI
    ) -> None:
        """Test that run() handles invalid menu choices gracefully."""
        # Given: User enters invalid choice, then exits
        # When: Running main loop
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui.run()
            output = fake_stdout.getvalue()

        # Then: Should display error and continue running
        assert "invalid" in output.lower() or "error" in output.lower()

    @patch("builtins.input", side_effect=["6"])
    def test_run_displays_menu_before_prompting(
        self, mock_input: MagicMock, menu_ui: MenuUI
    ) -> None:
        """Test that run() displays menu before asking for choice."""
        # Given: User will exit immediately
        # When: Running main loop
        with patch("sys.stdout", new=StringIO()) as fake_stdout:
            menu_ui.run()
            output = fake_stdout.getvalue()

        # Then: Menu should be displayed
        assert "menu" in output.lower() or "1" in output
