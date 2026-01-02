# Evolution of Todo - Constitution

## Core Principles

### I. Spec-Driven Development
All code MUST be generated from specifications using Claude Code; no manual coding is allowed.
- Every feature begins with a written specification
- Specifications are the single source of truth for implementation
- Code generation strictly follows spec requirements
- Manual code writing violates this constitutional principle

### II. Clean Code
Follow Python conventions (PEP 8), use type hints, write docstrings for all public functions.
- Code MUST adhere to PEP 8 style guidelines
- Type hints are REQUIRED for all function signatures
- Docstrings are MANDATORY for all public functions and classes
- Code readability and maintainability are non-negotiable

### III. Test-First Development (TDD)
TDD is mandatory; write failing tests first (Red), implement to pass (Green), then refactor.
- Red: Write a failing test that defines desired behavior
- Green: Implement minimal code to make the test pass
- Refactor: Improve code quality while keeping tests green
- No implementation without a failing test first
- This principle is NON-NEGOTIABLE

### IV. Single Responsibility Principle
Each module and function has one clear purpose; separate concerns (models, manager, UI).
- One class/function = one reason to change
- Clear separation between data models, business logic, and UI
- Manager layer handles business operations
- UI layer handles only presentation and user interaction
- Models represent data structures only

### V. Evolutionary Architecture
Design for Phase I in-memory storage but structure code to support future database persistence.
- Current implementation: in-memory storage
- Architecture MUST allow seamless transition to persistent storage
- Use abstractions (e.g., repository pattern) to decouple storage from logic
- No hardcoded dependencies on in-memory implementation details
- Forward compatibility is a design requirement

### VI. User Experience First
Clear prompts, helpful error messages, intuitive interactive menu flow.
- User prompts MUST be clear and unambiguous
- Error messages MUST be helpful and actionable
- Menu navigation MUST be intuitive and consistent
- User feedback MUST be immediate and informative
- The application MUST feel polished even in console mode

## Development Workflow

### Spec-to-Code Pipeline
1. Write specification document
2. Review and approve specification
3. Generate architecture plan from spec
4. Break down into testable tasks
5. Implement using TDD (Red-Green-Refactor)
6. Create Prompt History Records (PHRs) for all steps

### Quality Gates
- All code MUST pass PEP 8 linting
- All public APIs MUST have type hints
- All public functions MUST have docstrings
- All features MUST have passing tests
- No implementation without prior failing test

### Code Organization
- `models/` - Data structures and domain entities
- `manager/` - Business logic and operations
- `ui/` - User interface and interaction handling
- `tests/` - Test suites organized by module
- `specs/` - Feature specifications and plans

## Security & Data Handling

### Phase I Constraints
- No external service calls
- No file I/O or persistence
- No authentication required
- No network operations
- In-memory only operations

### Data Integrity
- Task IDs MUST be unique
- State changes MUST be validated
- Input MUST be sanitized and validated
- Error handling MUST prevent data corruption

## Governance

### Constitutional Authority
This constitution supersedes all other development practices and preferences.
Any deviation MUST be explicitly documented and justified.

### Amendment Process
1. Propose amendment with clear rationale
2. Document architectural decision (ADR)
3. Update constitution version
4. Communicate changes to all stakeholders

### Compliance
- All code reviews MUST verify constitutional compliance
- PHRs MUST document adherence to principles
- Violations MUST be corrected before merge

**Version**: 1.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-02
