# AGENTS.md - Complete Agent System for Phase I

**Project**: In-Memory Python Console Todo App  
**Type**: Agentic Dev Stack Implementation  
**Version**: 2.0 (With Subagents & Skills)

---

## 🏗️ Complete Agent Hierarchy

```
MAIN AGENTS (4)
│
├─ 1. SPECIFICATION AGENT
│   ├── Requirements Subagent: Extracts & structures requirements
│   ├── Validation Subagent: Defines validation rules
│   └── Documentation Subagent: Documents specs clearly
│
├─ 2. ARCHITECTURE AGENT
│   ├── Design Subagent: Creates component architecture
│   ├── Interface Subagent: Defines APIs and interfaces
│   └── Performance Subagent: Plans performance strategy
│
├─ 3. TASK BREAKDOWN AGENT
│   ├── Sequencing Subagent: Orders tasks optimally
│   ├── Dependency Subagent: Maps dependencies
│   └── Estimation Subagent: Estimates effort & complexity
│
└─ 4. IMPLEMENTATION AGENT
    ├── Code Generation Subagent: Writes implementation code
    ├── Testing Subagent: Creates comprehensive tests
    └── Quality Assurance Subagent: Validates quality

REUSABLE SKILLS (10+)
├── Validation Skill: Input validation with rules
├── Type Checking Skill: Mypy integration
├── Testing Skill: Pytest & coverage
├── Documentation Skill: Docstring generation
├── Error Handling Skill: Standardized errors
├── Formatting Skill: Output formatting
├── File Operations Skill: Safe file I/O
├── Git Operations Skill: Version control
├── Logging Skill: Structured logging
└── CLI Interaction Skill: User input/output
```

---

## 🎯 Core Workflow: Agentic Dev Stack (SDD)

```
User Request
    ↓
┌──────────────────────────────────┐
│  SPECIFICATION AGENT             │
│  ├─ Requirements Subagent        │ → speckit.specify
│  ├─ Validation Subagent          │ → validation rules
│  └─ Documentation Subagent       │ → specs/features/*.md
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│  ARCHITECTURE AGENT              │
│  ├─ Design Subagent              │ → speckit.plan
│  ├─ Interface Subagent           │ → interfaces defined
│  └─ Performance Subagent         │ → performance targets
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│  TASK BREAKDOWN AGENT            │
│  ├─ Sequencing Subagent          │ → task order
│  ├─ Dependency Subagent          │ → dependency graph
│  └─ Estimation Subagent          │ → effort estimates
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│  IMPLEMENTATION AGENT            │
│  ├─ Code Generation Subagent    │ → src/*.py
│  ├─ Testing Subagent             │ → tests/test_*.py
│  └─ Quality Assurance Subagent  │ → QA report
└──────────────────────────────────┘
    ↓
Working Feature ✅
```

---

## 📋 Agent 1: SPECIFICATION AGENT

### **Primary Responsibility**
Convert user requests into structured, testable specifications

### **Subagents**

#### **1.1 Requirements Subagent**
**Role**: Extract and structure functional requirements

**Inputs**:
- User request/story
- Domain context
- Existing specifications

**Process**:
1. Identify user needs
2. Extract functional requirements
3. Define acceptance criteria
4. List edge cases
5. Document constraints

**Outputs**:
- User stories with acceptance criteria
- Business rules list
- Constraint definitions

**Skills Used**:
- Validation Skill (to define validation rules)
- Documentation Skill (to structure requirements)

#### **1.2 Validation Subagent**
**Role**: Define input validation rules and data constraints

**Inputs**:
- Requirements from Requirements Subagent
- Constitution validation standards

**Process**:
1. Identify all input fields
2. Define validation rules per field
3. Specify error messages
4. Document edge cases

**Outputs**:
```markdown
### Validation Rules
- title: 
  - Type: string
  - Min length: 1
  - Max length: 200
  - Required: true
  - Strip whitespace: true
  - Error: "Title must be 1-200 characters"
  
- description:
  - Type: string
  - Max length: 1000
  - Required: false
  - Error: "Description max 1000 characters"
```

**Skills Used**:
- Validation Skill (to create rule objects)

#### **1.3 Documentation Subagent**
**Role**: Ensure specifications are clear and complete

**Inputs**:
- Raw requirements
- Validation rules
- Acceptance criteria

**Process**:
1. Structure information clearly
2. Add examples
3. Link to constitution
4. Create diagrams if needed
5. Review for completeness

**Outputs**:
- Well-formatted specification documents
- Usage examples
- Edge case documentation

**Skills Used**:
- Documentation Skill (generate structured docs)
- Formatting Skill (create readable output)

### **Main Agent Workflow**

```python
class SpecificationAgent:
    """Main specification agent coordinating subagents."""
    
    def create_specification(self, user_request: str) -> Specification:
        # Phase 1: Requirements
        requirements = self.requirements_subagent.extract(user_request)
        
        # Phase 2: Validation
        validation_rules = self.validation_subagent.define_rules(requirements)
        
        # Phase 3: Documentation
        spec_doc = self.documentation_subagent.format(
            requirements,
            validation_rules
        )
        
        # Generate output
        return Specification(
            user_stories=requirements.stories,
            acceptance_criteria=requirements.criteria,
            validation_rules=validation_rules,
            documentation=spec_doc
        )
```

### **Output Files**
- `speckit.specify`: Main specification
- `specs/features/{feature}.md`: Detailed feature spec

---

## 🏛️ Agent 2: ARCHITECTURE AGENT

### **Primary Responsibility**
Convert specifications into technical architecture

### **Subagents**

#### **2.1 Design Subagent**
**Role**: Create component architecture and layer design

**Inputs**:
- Specification from Specification Agent
- Constitution architecture standards

**Process**:
1. Identify components needed
2. Define layer structure
3. Assign responsibilities
4. Plan data flow
5. Design state management

**Outputs**:
```markdown
### Components
1. Task Model (Domain Layer)
   - Responsibility: Represent todo task
   - Location: src/todo_cli/models.py
   - Dependencies: None
   
2. TaskStorage (Storage Layer)
   - Responsibility: CRUD operations
   - Location: src/todo_cli/storage.py
   - Dependencies: Task Model
```

**Skills Used**:
- Documentation Skill (structure architecture docs)

#### **2.2 Interface Subagent**
**Role**: Define clean interfaces between components

**Inputs**:
- Component list from Design Subagent
- Constitution interface standards

**Process**:
1. Define Protocol/Interface for each component
2. Specify method signatures
3. Add type hints
4. Document parameters and returns
5. Plan error handling

**Outputs**:
```python
from typing import Protocol, Optional

class TaskStorage(Protocol):
    """Storage interface."""
    
    def add(self, task: Task) -> Task:
        """Add task and return with ID."""
        ...
    
    def get(self, task_id: int) -> Optional[Task]:
        """Get task by ID or None."""
        ...
```

**Skills Used**:
- Type Checking Skill (ensure type safety)
- Documentation Skill (document interfaces)

#### **2.3 Performance Subagent**
**Role**: Plan performance characteristics

**Inputs**:
- Component design
- Constitution performance targets

**Process**:
1. Identify performance-critical operations
2. Choose appropriate data structures
3. Define complexity targets (Big-O)
4. Plan optimization strategies

**Outputs**:
```markdown
### Performance Targets
- Add task: O(1) using dict with ID key
- Get by ID: O(1) dict lookup
- List all: O(n) iteration
- Storage: dict[int, Task] for O(1) access
```

**Skills Used**:
- Documentation Skill

### **Main Agent Workflow**

```python
class ArchitectureAgent:
    """Main architecture agent coordinating subagents."""
    
    def create_plan(self, spec: Specification) -> TechnicalPlan:
        # Phase 1: Design components
        components = self.design_subagent.design_components(spec)
        
        # Phase 2: Define interfaces
        interfaces = self.interface_subagent.define_interfaces(components)
        
        # Phase 3: Plan performance
        performance = self.performance_subagent.plan_performance(
            components,
            interfaces
        )
        
        return TechnicalPlan(
            components=components,
            interfaces=interfaces,
            performance_targets=performance
        )
```

### **Output Files**
- `speckit.plan`: Main technical plan
- `specs/architecture.md`: Detailed architecture

---

## 📊 Agent 3: TASK BREAKDOWN AGENT

### **Primary Responsibility**
Break architecture into atomic, implementable tasks

### **Subagents**

#### **3.1 Sequencing Subagent**
**Role**: Determine optimal task order

**Inputs**:
- Technical plan from Architecture Agent
- Component dependency graph

**Process**:
1. Identify foundation tasks (no dependencies)
2. Group related tasks
3. Find parallelization opportunities
4. Create sequential phases
5. Identify critical path

**Outputs**:
```markdown
### Sequencing
Phase 1: Foundation
- T-001: Task Model (no dependencies)
- T-002: Storage Interface (depends on T-001)

Phase 2: Implementation
- T-003: Storage Implementation (depends on T-002)
Can parallelize after T-003:
- T-004: Add Command
- T-005: List Command
- T-006: Update Command
```

**Skills Used**:
- Documentation Skill

#### **3.2 Dependency Subagent**
**Role**: Map all task dependencies

**Inputs**:
- Component list
- Interface definitions
- Sequencing plan

**Process**:
1. Map code dependencies (A imports B)
2. Map data dependencies (A needs data from B)
3. Map test dependencies (test needs implementation)
4. Create dependency graph
5. Detect circular dependencies

**Outputs**:
```
Dependency Graph:
T-001 (Task Model)
  ↓
T-002 (Storage Interface)
  ↓
T-003 (Storage Implementation)
  ↓         ↓         ↓
T-004    T-005    T-006
(Add)    (List)   (Update)
```

**Skills Used**:
- Documentation Skill (visualize graph)

#### **3.3 Estimation Subagent**
**Role**: Estimate effort and complexity

**Inputs**:
- Task list
- Component complexity
- Developer experience level

**Process**:
1. Analyze lines of code needed
2. Count number of methods
3. Assess logic complexity
4. Identify risk factors
5. Estimate time

**Outputs**:
```markdown
T-001: Task Model
- Complexity: Simple (dataclass)
- LOC: ~30
- Methods: 0 (dataclass)
- Risks: None
- Effort: 30 minutes

T-003: Storage Implementation
- Complexity: Medium
- LOC: ~100
- Methods: 6 CRUD operations
- Risks: Edge cases, ID generation
- Effort: 2 hours
```

**Skills Used**:
- Documentation Skill

### **Main Agent Workflow**

```python
class TaskBreakdownAgent:
    """Main task breakdown agent coordinating subagents."""
    
    def create_tasks(self, plan: TechnicalPlan) -> TaskList:
        # Phase 1: Sequence tasks
        sequence = self.sequencing_subagent.determine_sequence(
            plan.components
        )
        
        # Phase 2: Map dependencies
        dependencies = self.dependency_subagent.map_dependencies(
            plan.components,
            sequence
        )
        
        # Phase 3: Estimate effort
        estimates = self.estimation_subagent.estimate_tasks(
            sequence,
            dependencies
        )
        
        # Generate task list
        tasks = []
        task_id = 1
        for phase in sequence.phases:
            for component in phase.components:
                task = Task(
                    id=f"T-{task_id:03d}",
                    component=component,
                    dependencies=dependencies[component],
                    estimate=estimates[component]
                )
                tasks.append(task)
                task_id += 1
        
        return TaskList(tasks=tasks)
```

### **Output Files**
- `speckit.tasks`: Complete task list
- `specs/tasks/{feature}.md`: Detailed task breakdown

---

## 💻 Agent 4: IMPLEMENTATION AGENT

### **Primary Responsibility**
Generate production-ready code with tests

### **Subagents**

#### **4.1 Code Generation Subagent**
**Role**: Write clean, documented implementation code

**Inputs**:
- Task specification
- Spec and Plan references
- Constitution code standards

**Process**:
1. Generate file header with Task ID
2. Generate imports
3. Generate module docstring
4. Generate class/function skeleton
5. Implement business logic
6. Add inline comments
7. Add comprehensive docstrings

**Outputs**:
```python
# File: src/todo_cli/models.py
# [Task]: T-001
# [From]: speckit.specify §2.1, speckit.plan §2.1

"""
Task data model.

Spec Reference: speckit.specify §2.1
Task: T-001
"""

from dataclasses import dataclass

@dataclass
class Task:
    """Task model with full documentation."""
    id: int
    title: str
    # ... implementation
```

**Skills Used**:
- Documentation Skill (generate docstrings)
- Type Checking Skill (add type hints)
- Validation Skill (implement validation)
- Error Handling Skill (handle errors)

#### **4.2 Testing Subagent**
**Role**: Create comprehensive test coverage

**Inputs**:
- Implementation code
- Acceptance criteria from spec
- Constitution testing standards

**Process**:
1. Analyze acceptance criteria
2. Generate happy path tests
3. Generate edge case tests
4. Generate boundary tests
5. Generate error tests
6. Create test fixtures
7. Aim for >90% coverage

**Outputs**:
```python
# File: tests/test_models.py
# [Task]: T-001

"""Tests for Task model."""

import pytest
from todo_cli.models import Task

def test_task_creation():
    """Should create task with all fields."""
    task = Task(id=1, title="Test")
    assert task.id == 1

def test_task_defaults():
    """Should have correct defaults."""
    task = Task(id=1, title="Test")
    assert task.completed is False

# ... 10+ more tests
```

**Skills Used**:
- Testing Skill (run tests, measure coverage)
- Documentation Skill (document tests)

#### **4.3 Quality Assurance Subagent**
**Role**: Validate implementation meets all standards

**Inputs**:
- Generated code
- Generated tests
- Constitution quality metrics

**Process**:
1. Verify type hints on all functions
2. Check docstring completeness
3. Run mypy type checking
4. Run ruff linting
5. Run tests
6. Check test coverage
7. Verify Task ID in files
8. Validate against constitution

**Outputs**:
```markdown
✅ QA Report for Task T-001

Type Safety:
✓ All functions have type hints
✓ mypy --strict: 0 errors

Documentation:
✓ Module docstring present
✓ Class docstring complete
✓ All attributes documented

Code Quality:
✓ ruff check: 0 warnings
✓ Complexity: Low (dataclass)

Testing:
✓ All tests pass (8/8)
✓ Coverage: 100%
✓ Edge cases covered

Traceability:
✓ Task ID: T-001 referenced
✓ Spec section: §2.1 referenced

OVERALL: ✅ APPROVED
```

**Skills Used**:
- Type Checking Skill
- Testing Skill
- Documentation Skill (validation)
- Formatting Skill (create report)

### **Main Agent Workflow**

```python
class ImplementationAgent:
    """Main implementation agent coordinating subagents."""
    
    def implement_task(self, task: Task) -> Implementation:
        # Phase 1: Generate code
        code = self.code_generation_subagent.generate(task)
        
        # Phase 2: Generate tests
        tests = self.testing_subagent.generate_tests(
            code,
            task.acceptance_criteria
        )
        
        # Phase 3: Quality assurance
        qa_report = self.qa_subagent.validate(
            code,
            tests,
            task
        )
        
        if not qa_report.approved:
            # Iterate until approved
            code = self.code_generation_subagent.fix(
                code,
                qa_report.issues
            )
            tests = self.testing_subagent.update(tests, code)
            qa_report = self.qa_subagent.validate(code, tests, task)
        
        return Implementation(
            code=code,
            tests=tests,
            qa_report=qa_report
        )
```

### **Output Files**
- `src/todo_cli/*.py`: Implementation code
- `tests/test_*.py`: Test code

---

## 🔧 Reusable Skills Integration

### **How Agents Use Skills**

```python
# Example: Specification Agent using Validation Skill

from todo_cli.skills.validation import ValidationSkill, ValidationRule

class ValidationSubagent:
    def define_rules(self, requirements):
        # Create validation rules using the skill
        title_rule = ValidationRule(
            type="string",
            min_length=1,
            max_length=200,
            required=True,
            strip=True
        )
        
        # Document in spec
        return {
            "title": title_rule,
            "description": ValidationRule(
                type="string",
                max_length=1000,
                required=False
            )
        }
```

```python
# Example: Implementation Agent using multiple skills

from todo_cli.skills.validation import ValidationSkill
from todo_cli.skills.error_handling import ErrorHandlingSkill
from todo_cli.skills.documentation import DocumentationSkill

class CodeGenerationSubagent:
    def generate_validation_function(self, field, rule):
        # Use skills to generate code
        
        # 1. Generate docstring using Documentation Skill
        docstring = DocumentationSkill.generate_function_docstring(
            func_name=f"validate_{field}",
            params={
                "value": ("str", f"{field} to validate"),
                "rule": ("ValidationRule", "Validation rules")
            },
            return_type="ValidationResult",
            raises=[("ValueError", "If validation fails")]
        )
        
        # 2. Generate validation logic using Validation Skill patterns
        code = f'''
def validate_{field}(value: str, rule: ValidationRule) -> ValidationResult:
    {docstring}
    return ValidationSkill.validate_string(value, rule)
'''
        
        return code
```

### **Skill Composition Patterns**

**Pattern 1: Validation → Error Handling → Formatting**
```python
# In Implementation Agent
def generate_add_task():
    # Use Validation Skill
    result = ValidationSkill.validate_string(title, rule)
    
    if not result.valid:
        # Use Error Handling Skill
        error = ErrorHandlingSkill.validation_error(
            "title", title, "1-200 chars"
        )
        # Use Formatting Skill
        print(FormattingSkill.format_error(error.user_message))
    else:
        # Use Formatting Skill
        print(FormattingSkill.format_success("Task added!"))
```

---

## 📊 Quality Gates

### **Gate 1: After Specification**
- [ ] All user stories have acceptance criteria
- [ ] All validation rules defined
- [ ] All error scenarios documented
- [ ] Examples provided
- [ ] Constitution standards referenced

### **Gate 2: After Architecture**
- [ ] All components identified
- [ ] All interfaces defined with type hints
- [ ] Data flow documented
- [ ] Performance targets specified
- [ ] Testing strategy outlined

### **Gate 3: After Task Breakdown**
- [ ] All tasks have unique IDs
- [ ] All dependencies mapped
- [ ] All tasks link to spec and plan
- [ ] Effort estimates provided
- [ ] Sequencing makes sense

### **Gate 4: After Implementation**
- [ ] Code references Task ID
- [ ] All tests pass
- [ ] Coverage >90%
- [ ] Type checking passes (mypy --strict)
- [ ] Linting passes (ruff)
- [ ] Documentation complete
- [ ] QA subagent approves

---

## 🎯 Success Criteria

### **For Individual Agents**
- **Specification Agent**: Clear, testable specs
- **Architecture Agent**: Well-designed components
- **Task Breakdown Agent**: Atomic, sequenced tasks
- **Implementation Agent**: Working, tested code

### **For Agent System**
- Complete traceability: Code → Task → Plan → Spec
- All quality gates passed
- Constitution standards met
- Judges can follow the workflow

---

## 📝 Development Log Template

Track agent interactions:

```markdown
## Feature: Add Task

### 2025-01-01 09:00 - Specification Phase

**Agent**: Specification Agent
**Subagents Used**: Requirements, Validation, Documentation

**Iteration 1**:
- Requirements Subagent extracted: "Add task with title and description"
- Validation Subagent defined: title (1-200 chars), description (max 1000)
- Documentation Subagent created: specs/features/add-task.md
- Output: speckit.specify §2.1 created

**Quality Gate**: ✅ All acceptance criteria defined

---

### 2025-01-01 10:30 - Architecture Phase

**Agent**: Architecture Agent
**Subagents Used**: Design, Interface, Performance

**Iteration 1**:
- Design Subagent created: Task model, Storage, Command layers
- Interface Subagent defined: TaskStorage Protocol
- Performance Subagent specified: O(1) operations using dict
- Output: speckit.plan §2 created

**Quality Gate**: ✅ All interfaces have type hints

---

### 2025-01-01 12:00 - Task Breakdown Phase

**Agent**: Task Breakdown Agent
**Subagents Used**: Sequencing, Dependency, Estimation

**Iteration 1**:
- Sequencing Subagent ordered: T-001 (Model) → T-002 (Storage) → T-003 (Command)
- Dependency Subagent mapped: T-003 depends on T-001, T-002
- Estimation Subagent estimated: T-001 (30min), T-002 (2hrs), T-003 (1.5hrs)
- Output: speckit.tasks with 3 tasks

**Quality Gate**: ✅ No circular dependencies

---

### 2025-01-01 14:00 - Implementation Phase (T-001)

**Agent**: Implementation Agent
**Subagents Used**: Code Generation, Testing, QA

**Iteration 1**:
- Code Generation Subagent created: models.py with Task dataclass
- Testing Subagent generated: 8 tests covering all scenarios
- QA Subagent validated: ✅ All checks passed
- Output: src/todo_cli/models.py, tests/test_models.py

**Quality Gate**: ✅ 100% coverage, all tests pass

**Final Status**: T-001 COMPLETE ✅
```

---

## 🎓 Agent Training Examples

### Example 1: Specification Agent in Action

**User Input**: "I want to add tasks to my todo list"

**Requirements Subagent**:
```
User Story Extracted:
- As a user, I want to add new tasks so I can track my work

Functional Requirements:
1. User can provide task title
2. User can provide optional description
3. Task gets unique ID
4. Task is stored
5. Confirmation is shown
```

**Validation Subagent**:
```
Validation Rules:
- Title: 1-200 chars, required, strip whitespace
- Description: max 1000 chars, optional
```

**Documentation Subagent**:
```markdown
# Feature: Add Task

## User Story
As a user, I want to add new tasks...

## Acceptance Criteria
- [ ] Title required (1-200 chars)
- [ ] Description optional (max 1000)
...
```

### Example 2: Full Agent Flow

**Feature**: Delete Task

**Specification Agent** creates:
- User story with acceptance criteria
- Validation: task_id must exist
- Error scenarios: task not found

**Architecture Agent** creates:
- Component: delete_task() function
- Interface: storage.delete(task_id: int) -> bool
- Performance: O(1) dictionary delete

**Task Breakdown Agent** creates:
- T-007: Implement delete_task command
- Dependencies: T-003 (Storage)
- Estimate: 1 hour

**Implementation Agent** creates:
```python
# [Task]: T-007
def delete_task(storage, task_id):
    """Delete task with validation."""
    if not storage.delete(task_id):
        raise ValueError(f"Task #{task_id} not found")
```
Plus 5+ tests, QA approval

---

## 🏆 Final Deliverables

Using this agent system, you will produce:

1. **Specifications** (`speckit.specify`, `specs/features/*.md`)
2. **Architecture** (`speckit.plan`, `specs/architecture.md`)
3. **Tasks** (`speckit.tasks`)
4. **Implementation** (`src/`, `tests/`)
5. **Quality Reports** (from QA Subagent)
6. **Development Log** (showing agent workflow)

All with **complete traceability**: Code → Task → Plan → Spec

---

**This is your complete agent system for Phase I. Use it to build professionally!** 🚀
