# ADR-004: Three-Layer Architecture (Models-Manager-UI)

> **Scope**: Overall application architecture and separation of concerns strategy for evolutionary design across Phases I-V.

- **Status:** Accepted
- **Date:** 2026-01-02
- **Feature:** phase-1-todo-app
- **Context:** Hackathon II Evolution of Todo requires building Phase I (console app) with architecture that supports seamless evolution to Phase II (web app with database), Phase III (AI integration), Phase IV (containerization), and Phase V (cloud-native). The architecture must enable backward compatibility and minimize refactoring between phases while maintaining testability and code quality.

## Decision

Implement a three-layer architecture with strict separation of concerns:

1. **Models Layer** (`models/task.py`): Pure data structures
   - Task dataclass with id, title, completed attributes
   - No business logic or dependencies
   - Represents domain entities only

2. **Manager Layer** (`manager/task_manager.py`): Business logic and operations
   - TaskManager class with CRUD operations
   - Encapsulates storage implementation (dict[int, Task])
   - Validates business rules and data integrity
   - Raises exceptions for error conditions
   - No UI or presentation logic

3. **UI Layer** (`ui/menu.py`): Presentation and user interaction
   - MenuUI class with console interface
   - Displays menus, prompts, and formatted output
   - Captures and validates input format
   - Delegates operations to TaskManager
   - Catches exceptions and shows user-friendly errors
   - No business logic or direct storage access

**Dependency Direction**: UI → Manager → Models (unidirectional, no circular dependencies)

**Layer Boundaries**:
- Models: Zero dependencies
- Manager: Depends only on Models
- UI: Depends on Manager and Models (for type hints only)

## Consequences

### Positive

- **Evolutionary Architecture**: Enables seamless Phase II migration:
  - Extract repository interface from TaskManager
  - Create InMemoryRepository (current) and DatabaseRepository (PostgreSQL)
  - Inject repository via dependency injection
  - **UI and Models layers unchanged** - zero refactoring needed
- **Testability**: Each layer tested independently:
  - Models: Unit tests for data validation
  - Manager: Business logic tests without UI complexity
  - UI: Interface tests with mocked TaskManager
- **Single Responsibility**: Each component has one clear purpose (Constitutional Principle IV)
- **Maintainability**: Changes isolated to specific layers (update storage → Manager only; change menu → UI only)
- **Code Reusability**: Manager can be reused with different UIs (console, web, API) without modification
- **Type Safety**: Clear interfaces between layers enable strong type checking (mypy)

### Negative

- **More Files**: Three directories vs single file (acceptable complexity for long-term maintainability)
- **Requires Discipline**: Developers must resist adding business logic to UI or storage logic to Models (mitigated by code reviews and TDD)
- **Slight Verbosity**: Operations pass through multiple layers (UI → Manager → Models) vs direct manipulation (acceptable trade-off for separation of concerns)

## Alternatives Considered

### Alternative 1: Two-Layer Architecture (UI + Models)
- **Structure**: UI handles both presentation and business logic; Models are data only
- **Example**: MenuUI directly manages `list[Task]`, performs validation, generates IDs
- **Rejection Reason**:
  - Business logic mixed with UI makes Phase II migration painful (must extract logic from 10+ UI methods)
  - Cannot test business logic without UI complexity
  - Violates Single Responsibility Principle (UI does presentation AND business logic)
  - Database migration requires rewriting UI layer
  - Poor code reusability (cannot use same logic with web UI)

### Alternative 2: Four-Layer Architecture (UI-Manager-Repository-Models)
- **Structure**: Add explicit Repository layer between Manager and Models
- **Example**: InMemoryRepository class with add/get/update/delete methods
- **Rejection Reason**:
  - Over-engineering for Phase I in-memory scope
  - Repository pattern not needed until Phase II (no multiple storage backends)
  - Adds complexity (extra files, interfaces, abstractions) without immediate benefit
  - TaskManager already encapsulates storage operations (acts as implicit repository)
  - **Defer to Phase II**: Extract repository when actually needed (YAGNI principle)

### Alternative 3: Service-Oriented Architecture
- **Structure**: Multiple service classes (TaskService, ValidationService, StorageService)
- **Rejection Reason**:
  - Excessive for console application (10+ classes vs 3)
  - Network boundaries not needed in single-process application
  - Adds indirection without benefit
  - Violates Hackathon reference guidance: "Prefer conservative interpretation"

## Phase II Migration Path

**Current (Phase I)**:
```
UI (menu.py)
  → TaskManager (task_manager.py)
      → dict[int, Task] (in-memory storage)
          → Task (task.py)
```

**Future (Phase II)**:
```
Web UI (React/Next.js)                    Console UI (menu.py)
  ↓                                          ↓
  API Endpoints (FastAPI)         →     TaskManager (task_manager.py)
                                            ↓
                                        Repository Interface
                                            ↓
                          ┌─────────────────┴─────────────────┐
                          ↓                                   ↓
                  InMemoryRepository              DatabaseRepository (PostgreSQL)
                          ↓                                   ↓
                      dict[int, Task]                    SQL Database
                          ↓                                   ↓
                        Task (task.py) ←──────────────────────┘
```

**Migration Steps**:
1. Define `TaskRepository` protocol/interface with add/get/update/delete methods
2. Create `InMemoryRepository` class implementing interface (move dict logic from TaskManager)
3. Create `DatabaseRepository` class implementing interface (SQL operations)
4. Inject repository into TaskManager via constructor dependency injection
5. **UI layer unchanged** - still calls same TaskManager methods
6. **Models layer unchanged** - Task dataclass stays identical
7. **TaskManager methods unchanged** - delegates to repository instead of direct dict access

## References

- Feature Spec: `specs/phase-1-todo-app/spec.md` (Architecture section)
- Implementation Plan: `specs/phase-1-todo-app/plan.md` (Section 1: Architecture Overview, Section 6: Migration Path)
- Constitution: `.specify/memory/constitution.md` (Principle IV: Single Responsibility, Principle V: Evolutionary Architecture)
- Hackathon Reference: `specs/hackathon-ii-reference.md` (Phase I-II evolution requirements)
- Related ADRs: ADR-001 (Dictionary Storage), ADR-002 (Exception Handling - defines layer boundaries)
