"""MenuUI presentation layer for the Todo application.

This module implements the MenuUI class which handles all user interaction,
including displaying menus, formatting output, and processing user input.
"""

from todo_app.manager.task_manager import TaskManager
from todo_app.models.task import Task


class MenuUI:
    """Manages console-based user interface for todo application.

    MenuUI provides a menu-driven interface for users to interact with
    the todo application. It handles displaying the menu, formatting task
    lists, processing user input, and coordinating with TaskManager for
    business logic operations.

    Attributes:
        manager: The TaskManager instance for task operations (private).

    Example:
        >>> manager = TaskManager()
        >>> ui = MenuUI(manager)
        >>> ui.display_menu()
        === Todo Menu ===
        1. Add a new task
        ...
    """

    def __init__(self, manager: TaskManager) -> None:
        """Initialize MenuUI with a TaskManager instance.

        Args:
            manager: The TaskManager to use for task operations.
        """
        self._manager = manager

    def display_menu(self) -> None:
        """Display the main menu with all available options.

        Prints the menu header and all available operations to stdout.
        Menu options include: Add, View, Mark Complete, Delete, Update, Exit.
        """
        print("\n=== Todo Menu ===")
        print("1. Add a new task")
        print("2. View all tasks")
        print("3. Mark task as complete")
        print("4. Delete a task")
        print("5. Update a task")
        print("6. Exit")

    def _format_task_list(self, tasks: list[Task]) -> str:
        """Format a list of tasks for display.

        Converts a list of Task instances into a formatted string suitable
        for console output. Each task is shown with its ID, completion status
        (checkbox), and title. Empty lists return a "no tasks" message.

        Args:
            tasks: List of Task instances to format.

        Returns:
            str: Formatted string representation of all tasks, or empty
                message if no tasks exist.

        Example:
            >>> tasks = [Task(id=1, title="Buy milk", completed=False)]
            >>> formatted = ui._format_task_list(tasks)
            >>> print(formatted)
            1. [ ] Buy milk
        """
        # Handle empty task list
        if not tasks:
            return "No tasks found."

        # Build formatted output
        lines = []
        for task in tasks:
            # Determine checkbox based on completion status
            checkbox = "[X]" if task.completed else "[ ]"
            # Format: ID. [checkbox] Title
            line = f"{task.id}. {checkbox} {task.title}"
            lines.append(line)

        return "\n".join(lines)

    def _handle_add_task(self) -> None:
        """Handle the add task workflow.

        Prompts the user to enter a task title, validates the input via
        TaskManager, creates the task, and displays a confirmation message.
        Catches and displays validation errors for empty or invalid input.
        """
        # Prompt user for task title
        title = input("Enter task title: ")

        # Attempt to create task via manager
        try:
            task = self._manager.add_task(title)
            print(f"Task added successfully: {task.id}. {task.title}")
        except ValueError as e:
            # Handle validation error (empty title)
            print(f"Error: {e}")

    def _handle_view_tasks(self) -> None:
        """Handle the view all tasks workflow.

        Retrieves all tasks from TaskManager, formats them using
        _format_task_list, and displays the result to the user.
        """
        # Get all tasks from manager
        tasks = self._manager.get_all_tasks()

        # Format and display tasks
        formatted = self._format_task_list(tasks)
        print(formatted)

    def _handle_mark_complete(self) -> None:
        """Handle the mark task complete workflow.

        Prompts the user for a task ID, validates the input, marks the
        task as complete via TaskManager, and displays confirmation.
        Handles errors for invalid input, nonexistent tasks, and
        already-completed tasks.
        """
        # Prompt user for task ID
        task_id_str = input("Enter task ID to mark complete: ")

        # Attempt to mark task complete
        try:
            task_id = int(task_id_str)
            self._manager.mark_complete(task_id)
            print(f"Task {task_id} marked as complete.")
        except ValueError:
            # Handle non-numeric input
            print("Error: Invalid task ID. Please enter a number.")
        except KeyError:
            # Handle nonexistent task
            print(f"Error: Task {task_id_str} not found.")
        except RuntimeError as e:
            # Handle already complete task
            print(f"Error: {e}")

    def _handle_delete_task(self) -> None:
        """Handle the delete task workflow.

        Prompts the user for a task ID, validates the input, deletes the
        task via TaskManager, and displays confirmation. Handles errors
        for invalid input and nonexistent tasks.
        """
        # Prompt user for task ID
        task_id_str = input("Enter task ID to delete: ")

        # Attempt to delete task
        try:
            task_id = int(task_id_str)
            self._manager.delete_task(task_id)
            print(f"Task {task_id} deleted successfully.")
        except ValueError:
            # Handle non-numeric input
            print("Error: Invalid task ID. Please enter a number.")
        except KeyError:
            # Handle nonexistent task
            print(f"Error: Task {task_id_str} not found.")

    def _handle_update_task(self) -> None:
        """Handle the update task workflow.

        Prompts the user for a task ID and new title, validates the input,
        updates the task via TaskManager, and displays confirmation.
        Handles errors for invalid input, nonexistent tasks, and empty titles.
        """
        # Prompt user for task ID and new title
        task_id_str = input("Enter task ID to update: ")
        new_title = input("Enter new title: ")

        # Attempt to update task
        try:
            task_id = int(task_id_str)
            updated_task = self._manager.update_task(task_id, new_title)
            print(f"Task {task_id} updated successfully: {updated_task.title}")
        except ValueError as e:
            # Handle non-numeric ID or empty title
            if "title" in str(e).lower():
                print(f"Error: {e}")
            else:
                print("Error: Invalid task ID. Please enter a number.")
        except KeyError:
            # Handle nonexistent task
            print(f"Error: Task {task_id_str} not found.")

    def run(self) -> None:
        """Run the main menu loop.

        Displays the menu, prompts for user choice, and executes the
        corresponding action. Continues looping until the user selects
        the exit option (6). Handles invalid menu choices gracefully.
        """
        while True:
            # Display menu
            self.display_menu()

            # Prompt for choice
            choice = input("\nEnter your choice: ")

            # Handle menu selection
            if choice == "1":
                self._handle_add_task()
            elif choice == "2":
                self._handle_view_tasks()
            elif choice == "3":
                self._handle_mark_complete()
            elif choice == "4":
                self._handle_delete_task()
            elif choice == "5":
                self._handle_update_task()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
