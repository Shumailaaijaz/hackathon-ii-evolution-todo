# ADR-001: Dictionary-Based Task Storage

> **Scope**: Storage implementation strategy for in-memory task management in Phase I.

- **Status:** Accepted
- **Date:** 2026-01-02
- **Feature:** phase-1-todo-app
- **Context:** Phase I Console Todo App requires high-performance in-memory storage for CRUD operations on tasks while maintaining simplicity and preparing for Phase II database migration.

## Decision

Use `dict[int, Task]` (dictionary with integer keys mapping to Task objects) as the internal storage mechanism in TaskManager, rather than list-based or other collection structures.

**Implementation Details**:
- Storage: `self._tasks: dict[int, Task] = {}`
- Key: Task ID (integer)
- Value: Task object instance
- Operations: Direct dictionary access for add, get, update, delete, mark complete

## Consequences

### Positive

- **O(1) Performance**: Dictionary provides constant-time lookup, insertion, and deletion by task ID, meeting NFR-001 requirement (< 100ms for 10,000 tasks)
- **Natural ID Mapping**: Task ID naturally serves as dictionary key, creating intuitive `id -> Task` relationship
- **Pythonic Pattern**: Standard Python idiom for ID-based entity storage, improving code readability
- **Deletion Efficiency**: Removing tasks is O(1) operation vs O(n) for list-based approaches
- **Memory Efficiency**: Hash table structure provides reasonable memory overhead for expected task volumes (< 10,000 tasks)

### Negative

- **Ordering Cost**: Viewing all tasks requires sorting operation O(n log n) to restore creation order, though this only occurs during display
- **Memory Overhead**: Dictionary hash table structure uses more memory than simple list (acceptable for in-memory Phase I scope)
- **No Implicit Ordering**: Unlike lists, dictionaries don't preserve insertion order as primary structure (mitigated by sorting on display)

## Alternatives Considered

### Alternative 1: List of Tasks
- **Structure**: `self._tasks: list[Task] = []`
- **Lookup**: Linear search O(n) through list to find task by ID
- **Rejection Reason**: Every ID-based operation (mark complete, delete, update) requires O(n) search, failing NFR-001 performance requirement for 10,000 tasks. Update/delete operations would take ~500ms at scale vs < 100ms target.

### Alternative 2: Custom Binary Search Tree
- **Structure**: Self-balancing BST with Task ID as key
- **Lookup**: O(log n) search time
- **Rejection Reason**: Unnecessary complexity for Phase I in-memory scope. O(log n) provides minimal benefit over O(1) for expected task volumes. Adds implementation and testing burden without meaningful performance gain.

### Alternative 3: OrderedDict
- **Structure**: `collections.OrderedDict[int, Task]`
- **Lookup**: O(1) with preserved insertion order
- **Rejection Reason**: Insertion order preservation not needed since we explicitly sort by creation order during display. Standard dict provides same performance with simpler interface. Python 3.7+ dicts maintain insertion order as implementation detail, making OrderedDict redundant.

## References

- Feature Spec: `specs/phase-1-todo-app/spec.md` (FR-001 to FR-006, NFR-001)
- Implementation Plan: `specs/phase-1-todo-app/plan.md` (Section 6: Key Decisions)
- Related ADRs: ADR-003 (Integer ID Generation), ADR-004 (Three-Layer Architecture)
- Performance Requirement: NFR-001 (< 100ms operations for 10,000 tasks)
