# Implementation Plan: Phase I - In-Memory Python Console Todo App

**Feature Branch**: `001-phase-1-todo-app`
**Created**: 2026-01-02
**Status**: Approved for Implementation
**Specification**: `specs/phase-1-todo-app/spec.md`

## 1. Architecture Overview

### High-Level Approach

This implementation follows a three-layer architecture with strict separation of concerns to enable future database migration while maintaining clean, testable code. The application uses an in-memory storage approach for Phase I with architectural patterns that allow seamless transition to persistent storage in Phase II.

**Core Architectural Decisions**:

1. **Three-Layer Separation**: Models (data structures) → Manager (business logic) → UI (presentation)
2. **Repository Pattern Readiness**: TaskManager encapsulates storage operations with method signatures that map directly to future repository interfaces
3. **Dependency Direction**: UI depends on Manager, Manager depends on Models, no circular dependencies
4. **Exception-Based Error Handling**: Business logic raises typed exceptions, UI catches and formats for user display
5. **Type Safety First**: Complete type hints throughout with no `Any` types unless unavoidable

### Component Relationship Diagram

```
┌─────────────────────────────────────────────────────────┐
│                      main.py                            │
│                  (Application Entry)                    │
└───────────────┬─────────────────────────────────────────┘
                │
                │ initializes and wires
                ▼
┌───────────────────────────────────────────────────────────┐
│                    UI Layer (ui/menu.py)                  │
│  - Display menus and prompts                             │
│  - Capture and validate input format                     │
│  - Format output for console display                     │
│  - Catch exceptions and show user-friendly errors        │
└───────────────┬───────────────────────────────────────────┘
                │
                │ delegates operations to
                ▼
┌───────────────────────────────────────────────────────────┐
│           Manager Layer (manager/task_manager.py)         │
│  - Manage in-memory task collection                      │
│  - Generate unique task IDs                              │
│  - Implement CRUD operations                             │
│  - Validate business rules                               │
│  - Enforce data integrity                                │
│  - Raise typed exceptions for errors                     │
└───────────────┬───────────────────────────────────────────┘
                │
                │ uses and stores
                ▼
┌───────────────────────────────────────────────────────────┐
│              Models Layer (models/task.py)                │
│  - Define Task data structure                            │
│  - Pure data representation                              │
│  - No business logic                                     │
└───────────────────────────────────────────────────────────┘
```

### Data Flow Example: Adding a Task

```
User enters "Buy groceries"
    → UI (menu.py) captures input, trims whitespace
    → UI calls task_manager.add_task("Buy groceries")
    → TaskManager validates title (not empty)
    → TaskManager generates ID (e.g., 1)
    → TaskManager creates Task(id=1, title="Buy groceries", completed=False)
    → TaskManager stores in internal dict {1: Task(...)}
    → TaskManager returns Task object to UI
    → UI formats and displays "Task added successfully: Buy groceries [ID: 1]"
```

---

## 2. Components

### Task (Models Layer)

**Responsibility**: Represent a single todo item with immutable identity and mutable state

**Location**: `todo_app/models/task.py`

**Dependencies**: None (pure data class)

**Public Interface**:
- Attributes: `id` (int), `title` (str), `completed` (bool)
- Constructor: `__init__(id: int, title: str, completed: bool = False)`
- String representation: `__repr__()` for debugging

**Design Notes**:
- Uses Python `dataclass` for automatic generation of `__init__`, `__repr__`, `__eq__`
- Immutable ID after construction (no setter)
- Mutable title and completed status (supports update operations)
- No validation logic (validation is Manager's responsibility)

---

### TaskManager (Manager Layer)

**Responsibility**: Manage the lifecycle of all tasks and enforce business rules

**Location**: `todo_app/manager/task_manager.py`

**Dependencies**:
- `models.task.Task` (creates and stores Task instances)
- `typing` (type hints for return values and parameters)

**Public Interface**:
- `add_task(title: str) -> Task`: Create and store new task with auto-generated ID
- `get_all_tasks() -> list[Task]`: Retrieve all tasks in creation order
- `get_task_by_id(task_id: int) -> Task`: Retrieve single task or raise exception
- `mark_complete(task_id: int) -> Task`: Mark task as complete, raise if already complete
- `delete_task(task_id: int) -> None`: Remove task from storage
- `update_task(task_id: int, new_title: str) -> Task`: Update task title

**Internal State**:
- `_tasks: dict[int, Task]` - Task storage with ID as key for O(1) lookup
- `_next_id: int` - Monotonically increasing ID counter

**Error Handling**:
- Raises `ValueError` for validation errors (empty titles, whitespace-only)
- Raises `KeyError` for non-existent task IDs
- Raises `RuntimeError` for business rule violations (already complete)

**Design Notes**:
- Dictionary storage provides O(1) lookup/insert/delete performance
- ID generation is encapsulated (future: can be replaced with database auto-increment)
- No direct storage access from outside (future: repository pattern injection point)
- Methods are stateless operations (no side effects beyond storage mutation)

---

### Menu (UI Layer)

**Responsibility**: Provide interactive console interface and delegate operations to TaskManager

**Location**: `todo_app/ui/menu.py`

**Dependencies**:
- `manager.task_manager.TaskManager` (delegates all operations)
- `models.task.Task` (for type hints only, not instantiation)

**Public Interface**:
- `MenuUI.__init__(task_manager: TaskManager)`: Initialize with TaskManager instance
- `MenuUI.run() -> None`: Start main menu loop (runs until user exits)

**Internal Methods** (private):
- `_display_main_menu() -> None`: Show menu options
- `_get_menu_choice() -> int`: Capture and validate menu selection
- `_handle_add_task() -> None`: Add task workflow
- `_handle_view_tasks() -> None`: Display all tasks workflow
- `_handle_mark_complete() -> None`: Mark complete workflow
- `_handle_delete_task() -> None`: Delete task workflow
- `_handle_update_task() -> None`: Update task workflow
- `_format_task_list(tasks: list[Task]) -> str`: Format tasks for display
- `_get_task_id_input(prompt: str) -> int`: Get and validate task ID from user

**Error Handling**:
- Catches exceptions from TaskManager
- Displays user-friendly error messages
- Handles invalid input formats (non-numeric menu choices, invalid IDs)
- Never crashes - always returns to main menu on errors

**Design Notes**:
- No direct task manipulation (always through TaskManager)
- All input is trimmed and validated before passing to Manager
- Menu loop continues until explicit exit choice
- Each operation returns to main menu automatically

---

### Application Entry Point (Main)

**Responsibility**: Initialize components and start application

**Location**: `todo_app/main.py`

**Dependencies**:
- `manager.task_manager.TaskManager`
- `ui.menu.MenuUI`

**Public Interface**:
- `main() -> None`: Application entry point

**Design Notes**:
- Minimal wiring logic only
- Creates TaskManager instance
- Creates MenuUI with TaskManager dependency
- Starts menu loop
- No error handling (UI handles all errors)

---

## 3. Interfaces

### Task Data Model

```python
from dataclasses import dataclass

@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier, auto-generated and immutable
        title: Task description, non-empty string
        completed: Completion status, defaults to False
    """
    id: int
    title: str
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate task attributes after initialization.

        Raises:
            ValueError: If id is not positive or title is empty
        """
        if self.id <= 0:
            raise ValueError("Task ID must be a positive integer")
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
```

---

### TaskManager Interface

```python
from typing import Protocol, Optional
from models.task import Task

class TaskManagerProtocol(Protocol):
    """Protocol defining the task management interface.

    This protocol enables future repository pattern implementation
    by defining the contract that any task management implementation
    must satisfy.
    """

    def add_task(self, title: str) -> Task:
        """Create a new task with auto-generated ID.

        Args:
            title: Task description, will be trimmed of whitespace

        Returns:
            The newly created Task instance

        Raises:
            ValueError: If title is empty or whitespace-only after trimming
        """
        ...

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks in creation order.

        Returns:
            List of all tasks ordered by ID (creation time)
            Empty list if no tasks exist
        """
        ...

    def get_task_by_id(self, task_id: int) -> Task:
        """Retrieve a specific task by ID.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The Task instance with the specified ID

        Raises:
            KeyError: If no task exists with the given ID
        """
        ...

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as completed.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The updated Task instance

        Raises:
            KeyError: If no task exists with the given ID
            RuntimeError: If task is already marked as complete
        """
        ...

    def delete_task(self, task_id: int) -> None:
        """Permanently remove a task.

        Args:
            task_id: The unique identifier of the task

        Raises:
            KeyError: If no task exists with the given ID
        """
        ...

    def update_task(self, task_id: int, new_title: str) -> Task:
        """Update the title of an existing task.

        Args:
            task_id: The unique identifier of the task
            new_title: The new task description, will be trimmed

        Returns:
            The updated Task instance

        Raises:
            KeyError: If no task exists with the given ID
            ValueError: If new_title is empty or whitespace-only after trimming
        """
        ...
```

---

### TaskManager Concrete Implementation

```python
from models.task import Task

class TaskManager:
    """Manages in-memory task storage and operations.

    This implementation uses a dictionary for O(1) task lookup
    and maintains a monotonically increasing ID counter.

    Attributes:
        _tasks: Internal storage mapping task IDs to Task instances
        _next_id: Counter for generating unique task IDs
    """

    def __init__(self) -> None:
        """Initialize empty task manager with ID counter at 1."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str) -> Task:
        """Create a new task with auto-generated ID.

        Args:
            title: Task description, will be trimmed of whitespace

        Returns:
            The newly created Task instance

        Raises:
            ValueError: If title is empty or whitespace-only after trimming
        """
        # Implementation details in TDD phase
        ...

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks in creation order (sorted by ID).

        Returns:
            List of all tasks ordered by ID (creation time)
            Empty list if no tasks exist
        """
        # Implementation details in TDD phase
        ...

    def get_task_by_id(self, task_id: int) -> Task:
        """Retrieve a specific task by ID.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The Task instance with the specified ID

        Raises:
            KeyError: If no task exists with the given ID
        """
        # Implementation details in TDD phase
        ...

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as completed.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The updated Task instance

        Raises:
            KeyError: If no task exists with the given ID
            RuntimeError: If task is already marked as complete
        """
        # Implementation details in TDD phase
        ...

    def delete_task(self, task_id: int) -> None:
        """Permanently remove a task.

        The task ID is never reused even after deletion.

        Args:
            task_id: The unique identifier of the task

        Raises:
            KeyError: If no task exists with the given ID
        """
        # Implementation details in TDD phase
        ...

    def update_task(self, task_id: int, new_title: str) -> Task:
        """Update the title of an existing task.

        Args:
            task_id: The unique identifier of the task
            new_title: The new task description, will be trimmed

        Returns:
            The updated Task instance

        Raises:
            KeyError: If no task exists with the given ID
            ValueError: If new_title is empty or whitespace-only after trimming
        """
        # Implementation details in TDD phase
        ...
```

---

### MenuUI Interface

```python
from manager.task_manager import TaskManager

class MenuUI:
    """Console-based interactive menu for task management.

    Provides a numbered menu interface for all task operations,
    handles user input validation, and displays formatted output.

    Attributes:
        _task_manager: TaskManager instance for delegating operations
    """

    def __init__(self, task_manager: TaskManager) -> None:
        """Initialize menu with task manager dependency.

        Args:
            task_manager: TaskManager instance for task operations
        """
        self._task_manager = task_manager

    def run(self) -> None:
        """Start the main menu loop.

        Displays menu, processes user selections, and handles errors
        until user chooses to exit.
        """
        # Implementation details in TDD phase
        ...

    def _display_main_menu(self) -> None:
        """Display the main menu options to console."""
        # Implementation details in TDD phase
        ...

    def _get_menu_choice(self) -> int:
        """Get and validate menu selection from user.

        Returns:
            Integer menu choice (1-6)

        Raises:
            ValueError: If input is not a valid integer
        """
        # Implementation details in TDD phase
        ...

    def _handle_add_task(self) -> None:
        """Handle add task workflow: prompt for title, call manager, show result."""
        # Implementation details in TDD phase
        ...

    def _handle_view_tasks(self) -> None:
        """Handle view tasks workflow: get tasks from manager, format and display."""
        # Implementation details in TDD phase
        ...

    def _handle_mark_complete(self) -> None:
        """Handle mark complete workflow: get ID, call manager, show result."""
        # Implementation details in TDD phase
        ...

    def _handle_delete_task(self) -> None:
        """Handle delete task workflow: get ID, call manager, show result."""
        # Implementation details in TDD phase
        ...

    def _handle_update_task(self) -> None:
        """Handle update task workflow: get ID and new title, call manager, show result."""
        # Implementation details in TDD phase
        ...

    def _format_task_list(self, tasks: list[Task]) -> str:
        """Format list of tasks for console display.

        Args:
            tasks: List of Task instances to format

        Returns:
            Formatted string with task list or empty message
        """
        # Implementation details in TDD phase
        ...

    def _get_task_id_input(self, prompt: str) -> int:
        """Get and validate task ID from user input.

        Args:
            prompt: Message to display when requesting ID

        Returns:
            Valid integer task ID

        Raises:
            ValueError: If input is not a valid integer
        """
        # Implementation details in TDD phase
        ...
```

---

## 4. Data Flow

### Layer Boundaries and Transformations

**User Input → UI Layer**:
- Raw string input from console
- Transformation: Strip whitespace, validate format (numeric for IDs)
- Validation: Check for empty strings, non-numeric values where numbers expected
- Output: Clean strings and integers passed to Manager

**UI Layer → Manager Layer**:
- Clean, validated input values (strings, integers)
- Transformation: None (pass-through)
- Validation: UI validates format; Manager validates business rules
- Output: Task objects or exceptions

**Manager Layer → Models Layer**:
- Validated business data (IDs, titles, completion status)
- Transformation: Create Task instances from validated data
- Validation: Task dataclass validates attribute types and constraints
- Output: Task objects stored in dictionary

**Manager Layer → UI Layer (Return Path)**:
- Task objects or exceptions
- Transformation: None (UI receives domain objects)
- Validation: None (data already validated)
- Output: Task objects

**UI Layer → User (Output)**:
- Task objects and status messages
- Transformation: Format Task objects into human-readable strings
- Validation: None (display only)
- Output: Formatted console text with status indicators ([✓], [ ])

### Data Validation Points

**Level 1 - UI Input Validation** (ui/menu.py):
- Check input is not empty
- Validate menu choices are integers 1-6
- Validate task IDs are numeric
- Trim whitespace from all string inputs

**Level 2 - Manager Business Validation** (manager/task_manager.py):
- Validate trimmed titles are not empty
- Verify task IDs exist in storage
- Check task not already complete before marking
- Enforce ID uniqueness and monotonic increment

**Level 3 - Model Data Validation** (models/task.py):
- Validate ID is positive integer
- Validate title is non-empty string
- Validate completed is boolean

### Error Propagation Flow

```
User enters invalid input
    → UI validates format
    → If invalid format: UI displays format error, prompts again
    → If valid format: UI passes to Manager
    → Manager validates business rules
    → If business rule violated: Manager raises exception
    → UI catches exception
    → UI formats error for user display
    → UI returns to main menu (graceful degradation)
```

---

## 5. Performance Targets

### Operation Performance Requirements

All performance targets assume in-memory operation with up to 10,000 tasks (NFR-007).

| Operation | Complexity Target | Data Structure | Justification |
|-----------|------------------|----------------|---------------|
| Add Task | O(1) | `dict[int, Task]` | Dictionary insertion with integer key is constant time. ID generation is simple increment. |
| View All Tasks | O(n log n) | `dict[int, Task]` → `sorted(list)` | Must sort by ID for creation order. Python's Timsort is O(n log n). For 10,000 tasks, ~133k comparisons. |
| Get Task by ID | O(1) | `dict[int, Task]` | Dictionary lookup with integer key is constant time via hash. |
| Mark Complete | O(1) | `dict[int, Task]` | Lookup is O(1), mutation is O(1). Total O(1). |
| Delete Task | O(1) | `dict[int, Task]` | Dictionary deletion with key is O(1). |
| Update Task | O(1) | `dict[int, Task]` | Lookup is O(1), string assignment is O(1). Total O(1). |

### Memory Complexity

- **Storage**: O(n) where n = number of tasks
- **Task Size**: ~100-200 bytes per task (id: 8 bytes, title: ~50-100 bytes average, completed: 1 byte, Python object overhead: ~40 bytes)
- **10,000 Tasks**: ~1-2 MB memory footprint (well within acceptable range)

### Response Time Targets

Based on NFR-001: All user actions must respond within 100ms for lists up to 10,000 tasks.

| Operation | Target Response Time | Expected Actual |
|-----------|---------------------|-----------------|
| Add Task | < 100ms | < 1ms |
| View All Tasks (10,000) | < 100ms | ~5-10ms (sort + format) |
| Mark Complete | < 100ms | < 1ms |
| Delete Task | < 100ms | < 1ms |
| Update Task | < 100ms | < 1ms |
| Menu Display | < 100ms | < 1ms |

All targets comfortably met with chosen data structures.

### Optimization Strategies

**Current (Phase I)**:
- Use dictionary for O(1) lookups (not list with O(n) search)
- Store tasks by ID key for direct access
- Sort only when displaying (lazy evaluation)
- Keep ID counter as simple integer (not search for max ID)

**Future Considerations (Phase II+)**:
- Database indexes on task ID for O(log n) lookup
- Pagination for large task lists (limit display to 50-100 at a time)
- Caching for frequently accessed tasks
- Lazy loading for task details

---

## 6. Architecture Decision Records

### ADR-001: Use Dictionary for Task Storage Instead of List

**Decision**: Store tasks in `dict[int, Task]` instead of `list[Task]`

**Rationale**:
- Dictionary provides O(1) lookup by ID vs O(n) for list search
- Deletion is O(1) vs O(n) for list (search + remove)
- Meets performance requirement (NFR-001) for 10,000 tasks
- ID-based access is the primary operation (mark complete, delete, update)

**Alternatives Considered**:
1. **List of Tasks**: Simpler conceptually but O(n) search for every ID-based operation
2. **Custom Binary Search Tree**: O(log n) lookup but unnecessary complexity for in-memory
3. **OrderedDict**: Same performance as dict but ordering not needed (we sort on display)

**Tradeoffs**:
- Pro: Excellent lookup/insert/delete performance
- Pro: Natural mapping of ID to Task
- Con: Requires sorting when displaying in order (acceptable cost for display-only operation)
- Con: Slightly more memory overhead than list (hash table structure)

**Impact**: Low risk, high benefit. Standard Python pattern for ID-based storage.

**Reference**: Create full ADR at `history/adr/001-dictionary-task-storage.md`

---

### ADR-002: Exception-Based Error Handling Over Return Codes

**Decision**: Use exceptions (`ValueError`, `KeyError`, `RuntimeError`) for error conditions instead of return codes or sentinel values

**Rationale**:
- Python idiomatic approach (EAFP: Easier to Ask Forgiveness than Permission)
- Forces error handling at UI layer (cannot ignore exceptions)
- Provides clear separation: Manager focuses on business logic, UI handles user messaging
- Enables specific error types for different failure modes

**Alternatives Considered**:
1. **Return Optional[Task] or None**: Ambiguous (None for not found? None for error?)
2. **Return Tuple (success: bool, data: Task | None, error: str)**: Verbose and non-Pythonic
3. **Custom Result Type**: Over-engineering for Phase I scope

**Tradeoffs**:
- Pro: Clear error semantics
- Pro: Cannot accidentally ignore errors
- Pro: Standard Python pattern
- Con: Requires try/except blocks in UI layer
- Con: Stack traces for expected errors (mitigated by catching at UI boundary)

**Impact**: Low risk. Standard Python error handling pattern.

**Reference**: Create full ADR at `history/adr/002-exception-based-error-handling.md`

---

### ADR-003: Auto-Incrementing Integer IDs Over UUIDs

**Decision**: Use simple integer counter for task IDs (1, 2, 3, ...) instead of UUIDs

**Rationale**:
- Simpler user experience (users enter "1" instead of "550e8400-e29b-41d4-a716-446655440000")
- Monotonically increasing IDs provide implicit creation ordering
- Sufficient uniqueness for single-user, single-session application
- Aligns with specification requirement (FR-003: auto-incrementing integer ID)
- Easier to test and debug

**Alternatives Considered**:
1. **UUIDs**: Globally unique but poor UX for console input
2. **Timestamp-based IDs**: Complex and unnecessary for Phase I
3. **Random integers**: Risk of collision, no ordering guarantee

**Tradeoffs**:
- Pro: Simple, user-friendly
- Pro: Implicit ordering by creation time
- Pro: Easy to implement and test
- Con: IDs not globally unique (acceptable for Phase I scope)
- Con: Predictable sequence (not a security concern for Phase I)

**Migration Path**: Phase II can replace integer IDs with database auto-increment primary keys (similar behavior) or add UUID as separate field.

**Impact**: Low risk. Meets all Phase I requirements.

**Reference**: Create full ADR at `history/adr/003-integer-id-generation.md`

---

### ADR-004: Three-Layer Architecture for Future Database Migration

**Decision**: Strictly separate Models, Manager, and UI layers with unidirectional dependencies

**Rationale**:
- Enables Phase II database migration without UI changes
- Manager layer provides repository-like interface (add, get_all, delete, update)
- Storage implementation is encapsulated (future: swap dict for database)
- Supports testing in isolation (mock Manager for UI tests, test Manager independently)
- Aligns with Constitution Principle V (Evolutionary Architecture)

**Alternatives Considered**:
1. **Two-Layer (UI + Models)**: Business logic mixed with UI, hard to migrate
2. **Four-Layer (add Repository)**: Over-engineering for Phase I in-memory storage
3. **Service-Oriented**: Overkill for console application

**Tradeoffs**:
- Pro: Clean separation of concerns
- Pro: Easy to test each layer independently
- Pro: Future-proof for database migration
- Pro: Follows Single Responsibility Principle
- Con: More files and classes than simple approach
- Con: Requires discipline to maintain boundaries

**Migration Path**:
- Phase II: Extract repository interface from TaskManager
- Create InMemoryRepository (current implementation)
- Create DatabaseRepository (SQLite/PostgreSQL)
- Inject repository into TaskManager via dependency injection
- UI and Models remain unchanged

**Impact**: Medium complexity, high long-term benefit. Critical for evolutionary architecture.

**Reference**: Create full ADR at `history/adr/004-three-layer-architecture.md`

---

## 7. Execution Roadmap

### Implementation Sequence

The implementation follows strict Test-Driven Development (Red-Green-Refactor) as mandated by Constitution Principle III.

**Phase 1: Models Layer** (Estimated: 2-4 hours)
1. Write failing tests for Task creation
2. Implement Task dataclass to pass tests
3. Write failing tests for Task validation
4. Implement Task validation
5. Refactor for clarity and type safety

**Phase 2: Manager Layer** (Estimated: 6-10 hours)
1. Write failing test: Add first task (ID=1)
2. Implement add_task minimal implementation
3. Write failing test: Add second task (ID=2)
4. Extend add_task for ID increment
5. Write failing test: Add task with empty title raises ValueError
6. Implement title validation
7. Write failing test: Get all tasks returns empty list initially
8. Implement get_all_tasks
9. Write failing test: Get all tasks returns tasks in ID order
10. Implement sorting in get_all_tasks
11. Write failing test: Get task by ID returns correct task
12. Implement get_task_by_id
13. Write failing test: Get non-existent ID raises KeyError
14. Implement error handling
15. Write failing test: Mark complete changes status to True
16. Implement mark_complete
17. Write failing test: Mark already-complete raises RuntimeError
18. Implement idempotency check
19. Write failing test: Delete task removes it from storage
20. Implement delete_task
21. Write failing test: Delete non-existent ID raises KeyError
22. Implement delete error handling
23. Write failing test: Delete doesn't reuse ID
24. Verify ID counter behavior
25. Write failing test: Update task changes title
26. Implement update_task
27. Write failing test: Update with empty title raises ValueError
28. Implement update validation
29. Refactor TaskManager for code quality

**Phase 3: UI Layer** (Estimated: 8-12 hours)
1. Write failing test: Menu displays all options
2. Implement _display_main_menu
3. Write failing test: Get menu choice validates input
4. Implement _get_menu_choice with validation
5. Write failing test: Add task workflow prompts and calls manager
6. Implement _handle_add_task
7. Write failing test: View tasks displays formatted list
8. Implement _handle_view_tasks and _format_task_list
9. Write failing test: View empty list shows "No tasks found"
10. Implement empty state handling
11. Write failing test: Mark complete workflow
12. Implement _handle_mark_complete
13. Write failing test: Delete task workflow
14. Implement _handle_delete_task
15. Write failing test: Update task workflow
16. Implement _handle_update_task
17. Write failing test: Exit workflow displays goodbye
18. Implement exit handling
19. Write failing test: Invalid menu choice shows error
20. Implement error message display
21. Write failing test: Main loop continues until exit
22. Implement run() main loop
23. Refactor UI for clarity and DRY principles

**Phase 4: Integration** (Estimated: 2-4 hours)
1. Create main.py entry point
2. Write integration test: Launch app, add task, view, exit
3. Wire components together
4. Test full user workflows manually
5. Create README with usage instructions

**Phase 5: Quality Gates** (Estimated: 2-4 hours)
1. Run coverage report (target: 95%+ for Manager, 90%+ overall)
2. Run PEP 8 linter (target: zero violations)
3. Verify all public functions have docstrings
4. Verify all functions have type hints
5. Run mypy type checker (target: zero type errors)
6. Final manual testing of all user stories

**Total Estimated Time**: 20-34 hours of focused development

---

### Critical Dependencies

**Blocking Dependencies**:
1. **Models → Manager**: Manager cannot be implemented until Task model exists
2. **Manager → UI**: UI cannot be implemented until TaskManager interface exists
3. **Models + Manager → Integration**: Cannot wire components until both exist

**Non-Blocking Dependencies**:
- Tests can be written in parallel once interfaces are defined
- Documentation can be written alongside implementation
- Manual testing scripts can be prepared while coding

**Risk Mitigation**:
- Implement in strict layer order (Models → Manager → UI) to avoid rework
- Define interfaces completely before implementation
- Keep each TDD cycle small (one test, one feature at a time)
- Commit after each successful Red-Green-Refactor cycle

---

### Testing Milestones

**Milestone 1: Models Complete**
- Criteria: 100% test coverage of Task class
- Tests: 5-8 test cases covering creation, validation, edge cases
- Exit Gate: All tests pass, no type errors, PEP 8 compliant

**Milestone 2: Manager Complete**
- Criteria: 95%+ test coverage of TaskManager
- Tests: 25-35 test cases covering all CRUD operations, validation, error cases
- Exit Gate: All tests pass, integration with Task model verified

**Milestone 3: UI Complete**
- Criteria: 70%+ test coverage of MenuUI
- Tests: 15-25 test cases covering workflows, formatting, error handling
- Exit Gate: All tests pass, integration with TaskManager verified

**Milestone 4: Integration Complete**
- Criteria: All user stories have passing acceptance tests
- Tests: 6 user story integration tests + edge case tests
- Exit Gate: Manual testing confirms all features work end-to-end

**Milestone 5: Quality Gates Passed**
- Criteria: All quality requirements met (PEP 8, type hints, docstrings, coverage)
- Tests: Automated linting and type checking pass
- Exit Gate: Ready for deployment/delivery

---

### Risk Analysis and Mitigation

**Risk 1: Test Coverage Below 95% for Manager**
- **Impact**: High (violates success criterion SC-007)
- **Probability**: Low (TDD ensures coverage)
- **Mitigation**: Write tests first, measure coverage after each cycle, add missing cases
- **Contingency**: Identify untested branches with coverage tool, add targeted tests

**Risk 2: PEP 8 Violations Accumulate**
- **Impact**: Medium (violates NFR-002 and SC-009)
- **Probability**: Medium (easy to overlook in fast development)
- **Mitigation**: Run linter after each file completion, fix immediately
- **Contingency**: Final cleanup pass with automated formatter (black/autopep8)

**Risk 3: Type Hints Incomplete or Using `Any`**
- **Impact**: Medium (violates NFR-003 and SC-008)
- **Probability**: Low (interfaces defined upfront)
- **Mitigation**: Run mypy after each module, enforce strict mode
- **Contingency**: Manual review of all function signatures

**Risk 4: UI Exception Handling Doesn't Catch All Manager Errors**
- **Impact**: High (app crashes on errors)
- **Probability**: Medium (easy to miss edge cases)
- **Mitigation**: Comprehensive exception testing in UI layer
- **Contingency**: Add top-level try/except in menu loop as safety net

**Risk 5: Circular Dependencies Between Layers**
- **Impact**: High (violates architecture principle)
- **Probability**: Low (clear dependency direction)
- **Mitigation**: Import checking, enforce unidirectional flow (UI→Manager→Models)
- **Contingency**: Refactor to extract interface if circular dependency occurs

**Risk 6: ID Generation Allows Duplicates**
- **Impact**: Critical (data integrity violation)
- **Probability**: Very Low (simple counter implementation)
- **Mitigation**: Explicit test for ID uniqueness and increment behavior
- **Contingency**: Add assertion in TaskManager to verify ID uniqueness on add

---

## 8. File Structure

```
todo_app/
│
├── models/
│   ├── __init__.py
│   └── task.py                 # Task dataclass with validation
│
├── manager/
│   ├── __init__.py
│   └── task_manager.py         # TaskManager with CRUD operations
│
├── ui/
│   ├── __init__.py
│   └── menu.py                 # MenuUI console interface
│
├── tests/
│   ├── __init__.py
│   ├── test_task.py            # Task model tests (100% coverage)
│   ├── test_task_manager.py    # TaskManager tests (95%+ coverage)
│   └── test_menu.py            # MenuUI tests (70%+ coverage)
│
├── main.py                     # Application entry point
├── README.md                   # Usage instructions and setup
└── requirements.txt            # Dependencies (pytest, coverage, mypy)
```

---

## 9. Acceptance Criteria Mapping

Each component directly satisfies specific acceptance criteria from the specification:

### Task Model
- **FR-004**: Stores id (int), title (str), completed (bool)
- **FR-019**: ID is immutable after creation (no setter)

### TaskManager.add_task
- **FR-002**: Allows adding tasks with non-empty title
- **FR-003**: Assigns unique, auto-incrementing ID
- **FR-011**: Trims whitespace from titles
- **FR-012**: Rejects empty/whitespace-only titles
- **FR-019**: Never reuses IDs (monotonic counter)
- **SC-004**: Maintains data integrity (no duplicate IDs)

### TaskManager.get_all_tasks
- **FR-005**: Returns all tasks in formatted list
- **FR-014**: Maintains creation order (sorted by ID)
- **FR-017**: Returns empty list when no tasks exist
- **NFR-007**: Handles 10,000 tasks without degradation

### TaskManager.mark_complete
- **FR-006**: Marks incomplete tasks as complete
- **FR-007**: Prevents re-marking completed tasks (idempotent)
- **FR-018**: Validates task ID exists

### TaskManager.delete_task
- **FR-008**: Deletes tasks by ID
- **FR-018**: Validates task ID exists
- **FR-019**: Never reuses deleted IDs

### TaskManager.update_task
- **FR-009**: Updates task title by ID
- **FR-011**: Trims whitespace from new title
- **FR-012**: Rejects empty/whitespace-only titles
- **FR-018**: Validates task ID exists

### MenuUI
- **FR-001**: Provides interactive console menu with numbered options
- **FR-010**: Validates input and displays clear error messages
- **FR-013**: Displays [✓] for complete, [ ] for incomplete
- **FR-015**: Returns to main menu after operations
- **FR-016**: Allows clean exit with goodbye message
- **NFR-008**: Shows specific, actionable error messages
- **NFR-009**: Provides immediate feedback for all actions

### Application (main.py)
- **FR-020**: Operates entirely in-memory (no I/O)
- **NFR-005**: Separates concerns into three layers
- **NFR-006**: Supports future database persistence (architecture)

### Quality Criteria
- **NFR-002**: PEP 8 compliance (verified by linter)
- **NFR-003**: Type hints for all functions (verified by mypy)
- **NFR-004**: Docstrings for all public APIs (verified by review)
- **NFR-010**: Testable in isolation (TDD approach)
- **SC-007**: 95%+ coverage for TaskManager (verified by coverage tool)
- **SC-008**: Type hints and docstrings (verified by automated checks)
- **SC-009**: Zero PEP 8 violations (verified by linter)

---

## 10. Future Phase II Migration Path

### Repository Pattern Introduction

**Step 1: Extract Repository Interface** (No Code Changes Required)

```python
# New file: manager/repository.py
from typing import Protocol
from models.task import Task

class TaskRepositoryProtocol(Protocol):
    """Abstract interface for task storage."""

    def add(self, task: Task) -> None: ...
    def get_all(self) -> list[Task]: ...
    def get_by_id(self, task_id: int) -> Task: ...
    def update(self, task: Task) -> None: ...
    def delete(self, task_id: int) -> None: ...
    def get_next_id(self) -> int: ...
```

**Step 2: Create InMemoryRepository** (Extract from TaskManager)

```python
# New file: manager/in_memory_repository.py
class InMemoryRepository:
    """Current Phase I implementation extracted to repository."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    # Move storage logic from TaskManager here
```

**Step 3: Refactor TaskManager to Use Repository**

```python
# Modified: manager/task_manager.py
class TaskManager:
    def __init__(self, repository: TaskRepositoryProtocol) -> None:
        self._repository = repository

    def add_task(self, title: str) -> Task:
        # Validation stays here
        # Delegate storage to repository
        task_id = self._repository.get_next_id()
        task = Task(id=task_id, title=title.strip())
        self._repository.add(task)
        return task
```

**Step 4: Create DatabaseRepository** (New Implementation)

```python
# New file: manager/database_repository.py
class DatabaseRepository:
    """Phase II database-backed storage."""

    def __init__(self, connection_string: str) -> None:
        # Initialize database connection
        pass

    def add(self, task: Task) -> None:
        # INSERT INTO tasks ...
        pass
```

**Step 5: Update main.py** (Minimal Change)

```python
# Phase I (current)
task_manager = TaskManager()

# Phase II (database)
from manager.database_repository import DatabaseRepository
repository = DatabaseRepository(connection_string="...")
task_manager = TaskManager(repository)
```

**Key Benefits**:
- UI layer unchanged (zero modifications)
- Task model unchanged (zero modifications)
- TaskManager business logic unchanged (only storage delegation modified)
- Tests remain valid (can test with InMemoryRepository)
- Clean separation enables A/B testing of storage backends

---

## 11. Summary and Next Steps

### Architecture Summary

This plan defines a three-layer architecture for a console-based todo application with the following characteristics:

1. **Clean Separation**: Models, Manager, and UI layers with unidirectional dependencies
2. **Type Safety**: Complete type hints throughout with no `Any` types
3. **Performance**: O(1) operations for all CRUD except View All (O(n log n) sort)
4. **Future-Proof**: Repository pattern readiness for Phase II database migration
5. **Testability**: TDD-driven development with 95%+ coverage target
6. **Quality**: PEP 8 compliance, comprehensive docstrings, clear error messages

### Key Architectural Decisions Requiring ADRs

The following decisions should be documented in full ADRs before implementation begins:

1. **Dictionary-Based Storage** (ADR-001): Use `dict[int, Task]` for O(1) lookup performance
2. **Exception-Based Error Handling** (ADR-002): Raise exceptions instead of return codes
3. **Integer ID Generation** (ADR-003): Auto-incrementing integers instead of UUIDs
4. **Three-Layer Architecture** (ADR-004): Models-Manager-UI separation for evolutionary architecture

**Recommended Action**: Run `/sp.adr <title>` for each decision above to create comprehensive architectural decision records.

### Implementation Readiness Checklist

- [x] Component responsibilities defined and non-overlapping
- [x] Interfaces specified with complete type hints
- [x] Data flow documented and validated
- [x] Performance targets established with justification
- [x] Error handling strategy defined
- [x] Testing approach planned (TDD workflow)
- [x] File structure defined
- [x] Dependencies mapped
- [x] Risks identified with mitigation strategies
- [x] All specification requirements mapped to components
- [x] Future migration path documented

### Identified Risks

**High Priority**:
- UI exception handling must catch all Manager errors (mitigate with comprehensive tests)

**Medium Priority**:
- PEP 8 violations may accumulate (mitigate with continuous linting)
- Type hints may be incomplete (mitigate with mypy strict mode)

**Low Priority**:
- Test coverage below 95% (mitigate with TDD discipline)
- Circular dependencies (mitigate with clear layer boundaries)

### Next Steps

1. **Create ADRs**: Document the four key architectural decisions identified above
2. **Task Breakdown**: Run `/sp.tasks` to break down implementation into TDD-driven tasks
3. **Environment Setup**: Create project structure and install dependencies (pytest, coverage, mypy)
4. **Begin Red Phase**: Write first failing test for Task model creation
5. **Follow TDD Cycle**: Red (failing test) → Green (minimal implementation) → Refactor (improve code quality)

### Success Metrics

Implementation will be considered complete when:
- All 6 user stories pass acceptance scenarios
- TaskManager achieves 95%+ test coverage
- Overall project achieves 90%+ test coverage
- Zero PEP 8 violations reported by linter
- Zero type errors reported by mypy
- All public functions have complete docstrings
- All manual testing workflows succeed

---

**Plan Version**: 1.0.0
**Created**: 2026-01-02
**Status**: Approved for Task Breakdown
**Next Phase**: Task Planning (`/sp.tasks`)
