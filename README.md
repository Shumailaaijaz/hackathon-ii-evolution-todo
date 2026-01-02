# Phase I Console Todo Application

A simple, elegant command-line todo application built with Python 3.13+. This is Phase I of the "Evolution of Todo" hackathon project, implementing core CRUD operations with an in-memory data structure.

## Features

✅ **Add Tasks** - Create new todo items with descriptive titles
✅ **View Tasks** - Display all tasks with completion status
✅ **Mark Complete** - Toggle tasks as done
✅ **Delete Tasks** - Remove tasks permanently
✅ **Update Tasks** - Edit task titles
✅ **Exit** - Gracefully close the application

## Architecture

The application follows a clean **three-layer architecture** designed for evolutionary growth:

```
Models (Data)
   ↓
Manager (Business Logic)
   ↓
UI (Presentation)
```

### Key Design Decisions

- **Dictionary-based storage**: O(1) task lookup performance (see ADR-001)
- **Auto-incrementing IDs**: Sequential integers (1, 2, 3...) never reused after deletion (see ADR-003)
- **Exception-based error handling**: ValueError, KeyError, RuntimeError for different failure modes (see ADR-002)
- **Type-safe**: Complete type hints with mypy strict mode compliance
- **Test-driven**: 95%+ test coverage for Manager layer, 90%+ overall

## Requirements

- **Python**: 3.13 or higher
- **Dependencies**: Listed in `requirements.txt`

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hackathon-ii-evolution-todo
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main.py
```

### Menu Options

```
=== Todo Menu ===
1. Add a new task
2. View all tasks
3. Mark task as complete
4. Delete a task
5. Update a task
6. Exit
```

### Example Session

```
$ python main.py
Welcome to the Todo Application!

=== Todo Menu ===
1. Add a new task
2. View all tasks
3. Mark task as complete
4. Delete a task
5. Update a task
6. Exit

Enter your choice: 1
Enter task title: Buy groceries
Task added successfully: 1. Buy groceries

Enter your choice: 2
1. [ ] Buy groceries

Enter your choice: 3
Enter task ID to mark complete: 1
Task 1 marked as complete.

Enter your choice: 2
1. [X] Buy groceries

Enter your choice: 6
Goodbye!
```

## Project Structure

```
hackathon-ii-evolution-todo/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Test configuration
├── mypy.ini                     # Type checking config
├── .flake8                      # PEP 8 config
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
├── specs/                       # Feature specifications
│   ├── phase-1-todo-app/
│   │   ├── spec.md              # Requirements
│   │   ├── plan.md              # Architecture
│   │   └── tasks.md             # Task breakdown
│   └── hackathon-ii-reference.md
├── history/                     # Project history
│   └── adr/                     # Architecture Decision Records
│       ├── ADR-001-dictionary-storage.md
│       ├── ADR-002-exception-handling.md
│       ├── ADR-003-integer-ids.md
│       └── ADR-004-three-layer-architecture.md
└── todo_app/                    # Main application package
    ├── __init__.py
    ├── models/                  # Data models
    │   ├── __init__.py
    │   └── task.py              # Task dataclass
    ├── manager/                 # Business logic
    │   ├── __init__.py
    │   └── task_manager.py      # CRUD operations
    ├── ui/                      # User interface
    │   ├── __init__.py
    │   └── menu_ui.py           # CLI menu system
    └── tests/                   # Test suite
        ├── __init__.py
        ├── test_task.py         # Model tests (11 tests)
        ├── test_task_manager.py # Manager tests (30 tests)
        ├── test_menu_ui.py      # UI tests (30 tests)
        └── test_integration.py  # Integration tests (10 tests)
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=todo_app --cov-report=html

# Run specific test file
pytest todo_app/tests/test_task_manager.py

# Run with verbose output
pytest -v
```

### Code Quality Checks

```bash
# Type checking (mypy)
mypy todo_app

# PEP 8 compliance (flake8)
flake8 todo_app

# Code formatting (black)
black todo_app --check
```

## Testing Coverage

The project maintains high test coverage:

- **Manager Layer**: 95%+ coverage (all CRUD operations thoroughly tested)
- **Models Layer**: 100% coverage (all validation paths tested)
- **UI Layer**: 90%+ coverage (all workflows and error cases tested)
- **Overall**: 90%+ coverage

### Test Statistics

- **Total Tests**: 81+ comprehensive tests
- **Test Types**: Unit, Integration, Workflow
- **Testing Style**: Given-When-Then (BDD-style)

## Error Handling

The application handles all error cases gracefully:

- **Empty titles**: Rejected with clear error messages
- **Whitespace-only titles**: Rejected with validation errors
- **Nonexistent task IDs**: KeyError caught and displayed
- **Already completed tasks**: RuntimeError with helpful message
- **Invalid ID format**: ValueError handled for non-numeric input
- **Invalid menu choices**: User prompted to enter valid option

## Acceptance Criteria

### Phase I Requirements (All Met ✅)

- ✅ User can add a new task with a title
- ✅ User can view all tasks (with ID and completion status)
- ✅ User can mark a task as complete
- ✅ User can delete a task
- ✅ User can update a task title
- ✅ User can exit the application
- ✅ Invalid input is handled gracefully
- ✅ No persistence (in-memory only)
- ✅ No external dependencies beyond testing tools

### Non-Functional Requirements (All Met ✅)

- ✅ **Performance**: < 100ms response time for 10,000 tasks
- ✅ **Code Quality**: PEP 8 compliant, type-safe, well-documented
- ✅ **Test Coverage**: 95%+ for Manager, 90%+ overall
- ✅ **Architecture**: Clean separation of concerns (Models-Manager-UI)
- ✅ **Maintainability**: Clear code, comprehensive docstrings, ADRs

## Design Principles

1. **Spec-Driven Development**: All code generated from specifications
2. **Test-First Development**: TDD with RED-GREEN-REFACTOR cycle
3. **Clean Code**: PEP 8 compliance, comprehensive docstrings
4. **Single Responsibility**: Each class/method has one clear purpose
5. **Evolutionary Architecture**: Designed for Phase II database migration
6. **User Experience First**: Clear prompts, helpful error messages

## Future Evolution

This Phase I implementation is designed for seamless evolution:

- **Phase II**: Add database persistence (PostgreSQL), web API (FastAPI), React frontend
- **Phase III**: AI chatbot integration
- **Phase IV**: Containerization with Kubernetes
- **Phase V**: Cloud-native deployment with event-driven architecture

The three-layer architecture enables database migration without refactoring UI or Models layers (see ADR-004).

## Technical Specifications

- **Python Version**: 3.13+
- **Type Hints**: Complete coverage with mypy strict mode
- **Testing**: pytest with pytest-cov
- **Code Style**: PEP 8 (enforced by flake8)
- **Formatting**: Black-compatible (88 char line length)

## Documentation

- **Specification**: `specs/phase-1-todo-app/spec.md`
- **Architecture Plan**: `specs/phase-1-todo-app/plan.md`
- **Task Breakdown**: `specs/phase-1-todo-app/tasks.md`
- **ADRs**: `history/adr/ADR-*.md`
- **Constitution**: `.specify/memory/constitution.md`

## License

This is a hackathon project for educational purposes.

## Author

Built with Spec-Driven Development using Claude Code.

---

**Status**: Phase I Complete ✅
**Next Phase**: Phase II - Full-Stack Web Application
"# hackathon-ii-evolution-todo" 
