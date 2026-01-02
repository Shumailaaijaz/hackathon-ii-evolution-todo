# AGENTS.md - Phase I: In-Memory Python Console App

## Project Overview

**Project Name**: Todo CLI - Phase I
**Type**: In-Memory Python Console Application
**Development Approach**: Agentic Dev Stack (Spec-Driven Development)
**Hackathon**: Panaversity Hackathon II
**Points**: 100

## Purpose

This project uses **Spec-Driven Development (SDD)** where:
- No agent is allowed to write code until specifications are complete
- All implementations must map back to specific Task IDs
- Every architectural decision must be documented in specs
- The workflow follows: **Specify → Plan → Tasks → Implement**

---

## Agent Roles & Responsibilities

### 1. **Specification Agent** (The Requirements Gatherer)

**Primary Tool**: `speckit_specify`

**Responsibilities**:
- Analyze user requirements and convert to structured specifications
- Write user stories with clear acceptance criteria
- Define domain models and business rules
- Document constraints and validation rules
- Create feature specifications

**Workflow**:
```
User Request → Analyze → Extract Requirements → Write Spec → Review with Constitution
```

**Output Files**:
- `speckit.specify` - Main requirements document
- `specs/features/*.md` - Individual feature specs

**Quality Checks**:
- [ ] All user stories have acceptance criteria
- [ ] All data models are defined
- [ ] All validations are specified
- [ ] Business rules are documented
- [ ] Edge cases are identified

---

### 2. **Architecture Agent** (The Technical Planner)

**Primary Tool**: `speckit_plan`

**Responsibilities**:
- Convert specifications into technical architecture
- Design component structure and interactions
- Define data flow and state management
- Plan error handling strategy
- Create sequence diagrams for complex flows

**Workflow**:
```
Read Spec → Design Architecture → Plan Components → Define Interfaces → Document in Plan
```

**Output Files**:
- `speckit.plan` - Technical architecture document

**Quality Checks**:
- [ ] All components are identified
- [ ] Interfaces are clearly defined
- [ ] Data flow is documented
- [ ] Error handling is planned
- [ ] Testing strategy is outlined

---

### 3. **Task Breakdown Agent** (The Work Organizer)

**Primary Tool**: `speckit_tasks`

**Responsibilities**:
- Break architecture plan into atomic tasks
- Sequence tasks with dependencies
- Assign task IDs and priorities
- Define success criteria for each task
- Link tasks back to specs and plan

**Workflow**:
```
Read Plan → Identify Components → Break into Tasks → Define Dependencies → Create Task List
```

**Output Files**:
- `speckit.tasks` - Comprehensive task list

**Task Format**:
```markdown
## Task T-XXX: [Task Name]

**From**: speckit.specify §X.Y, speckit.plan §Z.W
**Priority**: High/Medium/Low
**Depends On**: T-XXX, T-YYY
**Type**: Model/Logic/CLI/Test

**Description**:
Clear description of what needs to be done

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2

**Files to Modify**:
- src/todo_cli/models.py
- tests/test_models.py

**Expected Output**:
What the task should produce
```

**Quality Checks**:
- [ ] Each task is atomic (can be done in one session)
- [ ] All dependencies are identified
- [ ] Success criteria are clear
- [ ] Files to modify are listed
- [ ] Links to specs exist

---

### 4. **Implementation Agent** (The Code Builder)

**Primary Tool**: `speckit_implement`

**Responsibilities**:
- Implement tasks following the plan exactly
- Write type-safe, tested code
- Add proper documentation and comments
- Link code back to task IDs
- Follow constitution standards

**Workflow**:
```
Read Task → Verify Spec → Write Code → Add Tests → Link to Task ID → Validate Quality
```

**Code Template**:
```python
# File: src/todo_cli/models.py
# [Task]: T-001
# [From]: speckit.specify §2.1, speckit.plan §3.2

"""
Task data model for todo CLI application.

Spec Reference: speckit.specify §2.1
Architecture: speckit.plan §3.2
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    """
    Represents a todo task.
    
    Task Reference: T-001
    
    Attributes:
        id: Unique task identifier
        title: Task title (1-200 characters)
        description: Optional task description (max 1000 chars)
        completed: Completion status
        created_at: Creation timestamp
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = datetime.now()
```

**Quality Checks**:
- [ ] Code references Task ID in comments
- [ ] All functions have docstrings
- [ ] Type hints are present
- [ ] Tests are written
- [ ] Code passes mypy
- [ ] Code follows PEP 8

---

## Mandatory Agent Rules

### **Golden Rules** (Never Violate)

1. ❌ **No code without Task ID**
   - Every file must reference its Task ID
   - Every function must link back to spec sections

2. ❌ **No architecture changes without updating plan**
   - If approach changes, update `speckit.plan` first
   - Document why the change was needed

3. ❌ **No new features without updating specification**
   - New requirements → Update `speckit.specify`
   - New user stories → Add to specs

4. ❌ **No principle violations**
   - Check `.specify/memory/constitution.md` before every decision
   - If conflict, ask for constitution update

5. ❌ **No freestyle coding**
   - Follow the plan exactly
   - Don't invent "better" solutions
   - If improvement needed, update spec first

---

## Spec-Kit Workflow (The Pipeline)

### **Step 1: Specify (WHAT)**

**File**: `speckit.specify`

**Content Structure**:
```markdown
# Todo CLI Specification

## 1. Project Overview
- Purpose: In-memory Python console todo app
- Users: Individual developers
- Scope: Basic CRUD operations

## 2. User Stories

### US-001: Add Task
As a user, I want to add new tasks to my todo list so that I can track my work.

**Acceptance Criteria**:
- User can provide task title (required, 1-200 chars)
- User can provide description (optional, max 1000 chars)
- Task receives unique ID automatically
- Task is stored in memory
- Confirmation message shows task was added

**Business Rules**:
- Title cannot be empty or whitespace only
- Duplicate titles are allowed (different tasks)
- ID must be auto-incrementing integer

### US-002: List Tasks
...

## 3. Data Models

### Task Model
- id: integer (primary key, auto-increment)
- title: string (1-200 chars, required)
- description: string (0-1000 chars, optional)
- completed: boolean (default: false)
- created_at: datetime (auto-generated)

## 4. Validation Rules
...

## 5. Error Scenarios
...
```

**Agent Instructions**:
- Read user request carefully
- Extract functional requirements
- Define acceptance criteria clearly
- Identify edge cases
- Specify validation rules

---

### **Step 2: Plan (HOW)**

**File**: `speckit.plan`

**Content Structure**:
```markdown
# Todo CLI Technical Plan

## 1. Architecture Overview

### Pattern
- Clean Architecture principles
- Separation of concerns
- Domain-driven design

### Layers
1. **Domain Layer** (models.py)
   - Task dataclass
   - Pure business logic

2. **Storage Layer** (storage.py)
   - InMemoryTaskStorage class
   - CRUD operations

3. **Command Layer** (commands.py)
   - Command handlers
   - Input validation
   - Business logic orchestration

4. **Interface Layer** (cli.py)
   - User interaction
   - Command parsing
   - Output formatting

## 2. Component Design

### Component: Task Model
**Responsibility**: Represent todo task
**Location**: src/todo_cli/models.py
**Dependencies**: None (pure dataclass)

**Interface**:
```python
@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = datetime.now()
```

### Component: InMemoryTaskStorage
**Responsibility**: Store and retrieve tasks
**Location**: src/todo_cli/storage.py
**Dependencies**: Task model

**Interface**:
```python
class InMemoryTaskStorage:
    def add(self, task: Task) -> Task
    def get(self, task_id: int) -> Optional[Task]
    def list_all(self) -> list[Task]
    def update(self, task_id: int, **updates) -> Optional[Task]
    def delete(self, task_id: int) -> bool
    def toggle_complete(self, task_id: int) -> Optional[Task]
```

## 3. Data Flow

### Add Task Flow
```
User Input → CLI Parser → Validate Input → Create Task → 
Store in Memory → Generate Response → Display to User
```

## 4. Error Handling Strategy
- Input validation at CLI layer
- Business rule validation in command layer
- Storage errors propagate up
- User-friendly error messages

## 5. Testing Strategy
- Unit tests for models (100% coverage)
- Unit tests for storage (100% coverage)
- Integration tests for commands
- CLI interaction tests
```

**Agent Instructions**:
- Read specification completely
- Design clean architecture
- Define clear component boundaries
- Plan data flow
- Consider error cases

---

### **Step 3: Tasks (BREAKDOWN)**

**File**: `speckit.tasks`

**Content Structure**:
```markdown
# Todo CLI - Implementation Tasks

## Phase 1: Core Domain (Foundation)

### Task T-001: Create Task Model
**From**: speckit.specify §3.1, speckit.plan §2.1
**Priority**: High
**Depends On**: None
**Type**: Model

**Description**:
Create the Task dataclass with all required fields and validation.

**Acceptance Criteria**:
- [ ] Dataclass with id, title, description, completed, created_at
- [ ] Type hints on all fields
- [ ] Default values for optional fields
- [ ] Docstring with field descriptions
- [ ] 100% test coverage

**Files to Create/Modify**:
- src/todo_cli/models.py (create)
- tests/test_models.py (create)

**Expected Output**:
- Working Task dataclass
- Passing unit tests
- Type checking passes

---

### Task T-002: Create InMemoryTaskStorage
**From**: speckit.specify §3.2, speckit.plan §2.2
**Priority**: High
**Depends On**: T-001
**Type**: Storage

**Description**:
Implement in-memory storage with CRUD operations.

**Acceptance Criteria**:
- [ ] Class with private dictionary for storage
- [ ] Auto-incrementing ID generation
- [ ] All CRUD methods implemented
- [ ] Proper type hints
- [ ] Thread-safe operations (if needed)
- [ ] 100% test coverage

**Files to Create/Modify**:
- src/todo_cli/storage.py (create)
- tests/test_storage.py (create)

**Expected Output**:
- Working storage class
- All CRUD operations tested
- Edge cases handled

---

### Task T-003: Implement Add Task Command
**From**: speckit.specify §2.1, speckit.plan §2.3
**Priority**: High
**Depends On**: T-001, T-002
**Type**: Logic

**Description**:
Create command handler for adding new tasks.

**Acceptance Criteria**:
- [ ] Function accepts title and optional description
- [ ] Validates title length (1-200 chars)
- [ ] Validates description length (max 1000 chars)
- [ ] Strips whitespace
- [ ] Returns created task
- [ ] Raises clear errors for invalid input

**Files to Create/Modify**:
- src/todo_cli/commands.py (create)
- tests/test_commands.py (create)

**Expected Output**:
- Working add_task() function
- Input validation working
- Error messages clear

---

## Phase 2: CLI Interface

### Task T-004: Create CLI Parser
...

### Task T-005: Implement List Command
...

### Task T-006: Implement Update Command
...

### Task T-007: Implement Delete Command
...

### Task T-008: Implement Toggle Complete Command
...

---

## Phase 3: Polish & Quality

### Task T-009: Add Type Checking
...

### Task T-010: Add Linting
...

### Task T-011: Complete Documentation
...

### Task T-012: Demo Video
...
```

**Agent Instructions**:
- Break plan into atomic tasks
- Sequence by dependencies
- Each task should be 1-2 hours max
- Link every task to spec and plan
- Define clear success criteria

---

### **Step 4: Implement (CODE)**

**Agent Instructions**:
1. Read the task completely
2. Verify understanding of spec and plan
3. Write code with Task ID reference
4. Add comprehensive docstrings
5. Write tests alongside code
6. Validate against constitution
7. Run type checker
8. Run tests

**Example Implementation**:

```python
# File: src/todo_cli/storage.py
# [Task]: T-002
# [From]: speckit.specify §3.2, speckit.plan §2.2

"""
In-memory storage for todo tasks.

This module provides a simple in-memory storage implementation
for managing todo tasks. It's designed for Phase I of the project
and will be replaced with persistent storage in later phases.

Spec Reference: speckit.specify §3.2
Architecture: speckit.plan §2.2
Task: T-002
"""

from typing import Optional
from .models import Task


class InMemoryTaskStorage:
    """
    In-memory storage for todo tasks.
    
    This class provides CRUD operations for tasks using a simple
    dictionary-based storage. IDs are auto-incremented.
    
    Task Reference: T-002
    
    Attributes:
        _tasks: Dictionary storing tasks by ID
        _next_id: Next available task ID
    """
    
    def __init__(self) -> None:
        """Initialize empty storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
    
    def add(self, task: Task) -> Task:
        """
        Add a new task to storage.
        
        Automatically assigns an ID to the task.
        
        Args:
            task: Task to add (id will be assigned)
            
        Returns:
            The task with assigned ID
            
        Example:
            >>> storage = InMemoryTaskStorage()
            >>> task = Task(id=0, title="Buy milk")
            >>> saved = storage.add(task)
            >>> saved.id
            1
        """
        task.id = self._next_id
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task
    
    def get(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.
        
        Args:
            task_id: ID of task to retrieve
            
        Returns:
            Task if found, None otherwise
        """
        return self._tasks.get(task_id)
    
    def list_all(self) -> list[Task]:
        """
        Get all tasks.
        
        Returns:
            List of all tasks, ordered by ID
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)
    
    def update(self, task_id: int, **updates) -> Optional[Task]:
        """
        Update a task's fields.
        
        Args:
            task_id: ID of task to update
            **updates: Fields to update (title, description, completed)
            
        Returns:
            Updated task if found, None otherwise
            
        Example:
            >>> storage.update(1, title="Buy groceries", completed=True)
        """
        task = self._tasks.get(task_id)
        if not task:
            return None
            
        # Update allowed fields
        if 'title' in updates:
            task.title = updates['title']
        if 'description' in updates:
            task.description = updates['description']
        if 'completed' in updates:
            task.completed = updates['completed']
            
        return task
    
    def delete(self, task_id: int) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: ID of task to delete
            
        Returns:
            True if deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """
        Toggle task completion status.
        
        Args:
            task_id: ID of task to toggle
            
        Returns:
            Updated task if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if task:
            task.completed = not task.completed
            return task
        return None
```

---

## Agent Communication Protocol

### **When Agents Need Clarification**

**Specification Agent**:
```
"Spec unclear: User story US-003 mentions 'smart filters' but acceptance 
criteria are missing. Should I:
1. Add basic filter by status only
2. Add multiple filter types (status, date, priority)
3. Defer to later phase

Please update speckit.specify §2.3"
```

**Architecture Agent**:
```
"Plan conflict: Constitution §3.2 requires O(1) lookup, but current 
list-based storage is O(n). Should I:
1. Use dictionary with ID keys
2. Maintain dual storage (dict + list)
3. Update constitution to allow O(n)

Please resolve and update constitution or plan"
```

**Task Agent**:
```
"Task dependency unclear: T-005 (List Command) depends on T-002 (Storage),
but the plan doesn't specify if filtering should be in storage or command layer.
Should filtering be:
1. Storage responsibility (T-002)
2. Command responsibility (T-005)

Please update speckit.plan §2.2 or §2.3"
```

**Implementation Agent**:
```
"Implementation blocked: Task T-003 requires title validation, but spec 
doesn't specify:
- Should whitespace-only titles be rejected?
- Should we trim leading/trailing spaces?
- Should we normalize multiple spaces?

Cannot proceed without clear spec. Please update speckit.specify §2.1"
```

### **Agent Escalation Path**

```
1. Check Constitution → If principle unclear, request update
2. Check Specification → If requirement unclear, request clarification
3. Check Plan → If architecture unclear, request revision
4. Check Tasks → If task unclear, request breakdown

Never: Make assumptions or "do what seems right"
Always: Stop and request explicit clarification
```

---

## Quality Gates (Agent Checkpoints)

### **Before Implementing**
- [ ] Task ID is assigned
- [ ] Spec section is referenced
- [ ] Plan section is referenced
- [ ] Dependencies are completed
- [ ] Acceptance criteria are clear

### **During Implementation**
- [ ] Code has Task ID in header comment
- [ ] Functions have Google-style docstrings
- [ ] Type hints are present
- [ ] No mypy errors
- [ ] No ruff warnings

### **After Implementation**
- [ ] All tests pass
- [ ] Coverage >90%
- [ ] Code links back to Task ID
- [ ] Task marked as complete
- [ ] Next task can begin

---

## Agent Skills Summary

| Agent | Primary Skill | Output | Quality Metric |
|-------|--------------|---------|----------------|
| Specification | Requirements Analysis | speckit.specify | All user stories have acceptance criteria |
| Architecture | System Design | speckit.plan | All components have clear interfaces |
| Task Breakdown | Work Planning | speckit.tasks | All tasks are atomic and sequenced |
| Implementation | Code Generation | src/*.py | 100% type coverage, >90% test coverage |

---

## Constitution Reference

For all agents, the constitution at `.specify/memory/constitution.md` is the highest authority.

**Priority Order** (in case of conflict):
1. Constitution (WHY - principles)
2. Specification (WHAT - requirements)
3. Plan (HOW - architecture)
4. Tasks (BREAKDOWN - work items)

---

## Technology Stack (Phase I)

### **Required**
- Python 3.13+
- UV for package management
- pytest for testing
- mypy for type checking
- ruff for linting

### **Forbidden**
- Manual coding (must use Claude Code)
- External dependencies (except dev tools)
- Persistent storage (in-memory only)
- Web frameworks (CLI only)

---

## Success Criteria

### **For Agents**
- ✅ All code has Task ID references
- ✅ All specs link to code
- ✅ All tests pass
- ✅ Type coverage = 100%
- ✅ Test coverage >90%

### **For Project**
- ✅ All 5 basic features work
- ✅ Clean architecture maintained
- ✅ Documentation complete
- ✅ Judges can trace code → task → spec

---

## Development Log Template

Keep track of agent interactions:

```markdown
## 2025-01-01 - Add Task Feature

**Iteration 1: Specify**
- Prompt: "Create spec for adding tasks"
- Output: speckit.specify §2.1
- Issues: Missing validation rules
- Action: Updated with char limits

**Iteration 2: Plan**
- Prompt: "Create technical plan for add task"
- Output: speckit.plan §2.3
- Issues: None
- Action: Approved

**Iteration 3: Tasks**
- Prompt: "Break add task into implementation tasks"
- Output: Tasks T-001, T-002, T-003
- Issues: None
- Action: Ready to implement

**Iteration 4: Implement T-001**
- Prompt: "Implement task T-001"
- Output: src/todo_cli/models.py
- Issues: Missing docstrings
- Action: Added comprehensive docs

**Iteration 5: Implement T-002**
- Prompt: "Implement task T-002"
- Output: src/todo_cli/storage.py
- Issues: None
- Action: Tests passing, ready for T-003
```

---

## Final Checklist

Before submission:
- [ ] All agents followed SDD workflow
- [ ] Every file has Task ID reference
- [ ] Constitution is documented
- [ ] All specs are complete
- [ ] All code is tested
- [ ] Demo video shows spec-driven process
- [ ] Development log is maintained

---

**Remember**: Agents are tools for execution. Your job as architect is to write clear, complete specifications. The better your specs, the better the code.
