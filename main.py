"""Entry point for the Phase I Console Todo Application.

This module initializes the TaskManager and MenuUI components and starts
the main application loop.
"""

from todo_app.manager.task_manager import TaskManager
from todo_app.ui.menu_ui import MenuUI


def main() -> None:
    """Initialize and run the todo application.

    Creates a TaskManager instance, wraps it with MenuUI for user interaction,
    and starts the main menu loop.
    """
    # Initialize business logic layer
    manager = TaskManager()

    # Initialize UI layer with manager
    ui = MenuUI(manager)

    # Start application
    print("Welcome to the Todo Application!")
    ui.run()


if __name__ == "__main__":
    main()
