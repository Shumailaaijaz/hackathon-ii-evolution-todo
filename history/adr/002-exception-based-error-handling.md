# ADR-002: Exception-Based Error Handling

> **Scope**: Error handling and validation strategy across Manager and UI layers.

- **Status:** Accepted
- **Date:** 2026-01-02
- **Feature:** phase-1-todo-app
- **Context:** Phase I Console Todo App requires clear error handling for invalid operations (task not found, empty titles, invalid IDs) while maintaining clean separation between business logic (Manager) and user messaging (UI).

## Decision

Use Python exceptions (`ValueError`, `KeyError`, `RuntimeError`) for error conditions in the Manager layer, with try/except blocks in the UI layer to catch and format user-friendly error messages.

**Error Handling Pattern**:
- **Manager Layer**: Raise typed exceptions when business rules violated
  - `ValueError`: Invalid input (empty title, whitespace-only string)
  - `KeyError`: Task ID not found in storage
  - `RuntimeError`: Invalid state transitions (mark already-completed task)
- **UI Layer**: Catch all Manager exceptions and display formatted error messages
  - Wrap Manager calls in try/except blocks
  - Transform exception messages into user-friendly prompts
  - Continue menu loop after displaying errors

**Implementation Example**:
```python
# Manager raises exceptions
def add_task(self, title: str) -> Task:
    if not title.strip():
        raise ValueError("Task title cannot be empty")
    # ... implementation

# UI catches and formats
def _handle_add_task(self) -> None:
    try:
        task = self._task_manager.add_task(title)
        print(f"✓ Task added: {task.title} [ID: {task.id}]")
    except ValueError as e:
        print(f"✗ Error: {e}")
```

## Consequences

### Positive

- **Clear Error Semantics**: Each exception type signals specific failure mode (ValueError = bad input, KeyError = not found, RuntimeError = invalid state)
- **Cannot Ignore Errors**: Exceptions force explicit error handling at UI boundary, preventing silent failures
- **Pythonic EAFP Pattern**: Follows Python's "Easier to Ask Forgiveness than Permission" idiom, standard in Python community
- **Separation of Concerns**: Manager focuses on business logic and correctness; UI handles user communication and error formatting
- **Type Safety**: Static type checkers (mypy) can verify exception handling completeness
- **Debugging Clarity**: Stack traces provide clear error propagation path during development

### Negative

- **Try/Except Verbosity**: Every UI operation requires try/except block wrapper (5-10 additional lines per operation)
- **Stack Trace Overhead**: Expected errors generate stack traces, though caught at UI boundary before reaching user
- **Exception Performance**: Exception raising/catching has minor performance cost vs return codes (< 1ms impact, acceptable for interactive console UI)

## Alternatives Considered

### Alternative 1: Return Optional[Task] or None
- **Pattern**: Manager methods return `Task | None`, with None indicating failure
- **Example**: `def add_task(title: str) -> Task | None`
- **Rejection Reason**: Ambiguous semantics. Does None mean "task not found" or "validation error" or "system error"? Caller must guess failure reason. No way to communicate error details (which validation failed?). Forces UI to handle None without context for user messaging.

### Alternative 2: Return Tuple (success: bool, data: Task | None, error: str)
- **Pattern**: `def add_task(title: str) -> tuple[bool, Task | None, str]`
- **Example**: `success, task, error = manager.add_task("Buy milk")`
- **Rejection Reason**: Verbose and non-Pythonic. Unpacking tuples adds cognitive load. Callers can accidentally ignore success flag. Not idiomatic Python (exceptions preferred). Type safety weaker (mypy cannot enforce checking success flag).

### Alternative 3: Custom Result Type (Result[T, E])
- **Pattern**: Rust-style Result monad with Ok/Err variants
- **Example**: `Result[Task, str]` with pattern matching
- **Rejection Reason**: Over-engineering for Phase I scope. Requires custom Result class implementation and extensive type machinery. Python lacks pattern matching (before 3.10) and exhaustiveness checking. Adds complexity without proportional benefit for simple console application.

## References

- Feature Spec: `specs/phase-1-todo-app/spec.md` (Edge Cases section, FR-007 to FR-020)
- Implementation Plan: `specs/phase-1-todo-app/plan.md` (Section 4: Data Flow, Error Propagation)
- Related ADRs: ADR-004 (Three-Layer Architecture - establishes UI/Manager boundary)
- Python Best Practices: PEP 20 (Zen of Python: "Errors should never pass silently")
