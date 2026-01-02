# Reusable Skills System for Phase I

## Overview

Reusable skills are modular, atomic capabilities that can be combined by agents to accomplish complex tasks. Each skill has a single, clear purpose and well-defined inputs/outputs.

---

## 🎯 Core Skills Catalog

### 1. Validation Skill

**Purpose**: Validate user input according to specifications

**Inputs**:
- `value`: The value to validate
- `rules`: Validation rules object
  ```python
  {
      "type": "string",
      "min_length": 1,
      "max_length": 200,
      "strip": true,
      "required": true,
      "pattern": r"^[A-Za-z0-9\s]+$"  # optional regex
  }
  ```

**Outputs**:
- `valid`: boolean
- `cleaned_value`: processed value (stripped, normalized)
- `error_message`: string (if invalid)

**Implementation Template**:
```python
# File: src/todo_cli/skills/validation.py
# [Skill]: Validation

"""
Reusable validation skill.

Provides input validation with configurable rules.
"""

from typing import Optional
from dataclasses import dataclass
import re


@dataclass
class ValidationRule:
    """Validation rule configuration."""
    type: str  # "string", "int", "bool"
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    strip: bool = True
    required: bool = True
    pattern: Optional[str] = None
    

@dataclass
class ValidationResult:
    """Validation result."""
    valid: bool
    cleaned_value: any
    error_message: Optional[str] = None


class ValidationSkill:
    """Reusable validation skill."""
    
    @staticmethod
    def validate_string(
        value: str,
        rule: ValidationRule
    ) -> ValidationResult:
        """
        Validate string input.
        
        Args:
            value: String to validate
            rule: Validation rules
            
        Returns:
            ValidationResult with outcome
        """
        # Strip if requested
        if rule.strip:
            value = value.strip()
        
        # Check required
        if rule.required and not value:
            return ValidationResult(
                valid=False,
                cleaned_value=value,
                error_message="Value cannot be empty"
            )
        
        # Check min length
        if rule.min_length and len(value) < rule.min_length:
            return ValidationResult(
                valid=False,
                cleaned_value=value,
                error_message=f"Minimum length: {rule.min_length} characters"
            )
        
        # Check max length
        if rule.max_length and len(value) > rule.max_length:
            return ValidationResult(
                valid=False,
                cleaned_value=value,
                error_message=f"Maximum length: {rule.max_length} characters, got {len(value)}"
            )
        
        # Check pattern
        if rule.pattern and not re.match(rule.pattern, value):
            return ValidationResult(
                valid=False,
                cleaned_value=value,
                error_message="Value does not match required pattern"
            )
        
        return ValidationResult(
            valid=True,
            cleaned_value=value,
            error_message=None
        )


# Usage Example:
"""
from todo_cli.skills.validation import ValidationSkill, ValidationRule

rule = ValidationRule(
    type="string",
    min_length=1,
    max_length=200,
    strip=True,
    required=True
)

result = ValidationSkill.validate_string("  My Task  ", rule)
if result.valid:
    task.title = result.cleaned_value
else:
    print(f"Error: {result.error_message}")
"""
```

---

### 2. Type Checking Skill

**Purpose**: Ensure type safety and run mypy validation

**Inputs**:
- `files`: List of Python files to check
- `strict`: Whether to use strict mode (default: true)

**Outputs**:
- `success`: boolean
- `errors`: List of type errors
- `error_count`: int

**Implementation Template**:
```python
# File: src/todo_cli/skills/type_checking.py
# [Skill]: Type Checking

"""
Reusable type checking skill.

Runs mypy and validates type hints.
"""

import subprocess
from typing import List
from dataclasses import dataclass


@dataclass
class TypeCheckResult:
    """Type checking result."""
    success: bool
    errors: List[str]
    error_count: int


class TypeCheckingSkill:
    """Reusable type checking skill."""
    
    @staticmethod
    def check_files(
        files: List[str],
        strict: bool = True
    ) -> TypeCheckResult:
        """
        Run mypy on files.
        
        Args:
            files: List of file paths
            strict: Use strict mode
            
        Returns:
            TypeCheckResult
        """
        cmd = ["mypy"]
        if strict:
            cmd.append("--strict")
        cmd.extend(files)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        errors = []
        if result.returncode != 0:
            errors = result.stdout.split("\n")
            errors = [e for e in errors if e.strip()]
        
        return TypeCheckResult(
            success=result.returncode == 0,
            errors=errors,
            error_count=len(errors)
        )
    
    @staticmethod
    def validate_function_hints(func) -> bool:
        """
        Check if function has type hints.
        
        Args:
            func: Function to check
            
        Returns:
            True if all params and return are typed
        """
        import inspect
        sig = inspect.signature(func)
        
        # Check return type
        if sig.return_annotation == inspect.Signature.empty:
            return False
        
        # Check parameters
        for param in sig.parameters.values():
            if param.annotation == inspect.Parameter.empty:
                return False
        
        return True
```

---

### 3. Testing Skill

**Purpose**: Generate and run tests with coverage

**Inputs**:
- `module`: Module to test
- `test_file`: Path to test file
- `coverage_threshold`: Minimum coverage (default: 90)

**Outputs**:
- `tests_passed`: boolean
- `coverage_percentage`: float
- `failed_tests`: List[str]

**Implementation Template**:
```python
# File: src/todo_cli/skills/testing.py
# [Skill]: Testing

"""
Reusable testing skill.

Generates and runs tests with coverage reporting.
"""

import subprocess
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class TestResult:
    """Test execution result."""
    tests_passed: bool
    coverage_percentage: float
    failed_tests: List[str]
    total_tests: int
    passed_tests: int


class TestingSkill:
    """Reusable testing skill."""
    
    @staticmethod
    def run_tests(
        test_file: Optional[str] = None,
        coverage: bool = True,
        threshold: int = 90
    ) -> TestResult:
        """
        Run pytest with coverage.
        
        Args:
            test_file: Specific test file (None = all)
            coverage: Enable coverage reporting
            threshold: Minimum coverage %
            
        Returns:
            TestResult
        """
        cmd = ["pytest", "-v"]
        
        if coverage:
            cmd.extend([
                "--cov=todo_cli",
                "--cov-report=term",
                f"--cov-fail-under={threshold}"
            ])
        
        if test_file:
            cmd.append(test_file)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        # Parse output
        output = result.stdout
        failed_tests = []
        coverage_pct = 0.0
        
        # Extract coverage percentage
        for line in output.split("\n"):
            if "TOTAL" in line and "%" in line:
                parts = line.split()
                for part in parts:
                    if "%" in part:
                        coverage_pct = float(part.replace("%", ""))
        
        # Extract failed tests
        if "FAILED" in output:
            for line in output.split("\n"):
                if "FAILED" in line:
                    failed_tests.append(line.strip())
        
        return TestResult(
            tests_passed=result.returncode == 0,
            coverage_percentage=coverage_pct,
            failed_tests=failed_tests,
            total_tests=0,  # Parse from output
            passed_tests=0   # Parse from output
        )
    
    @staticmethod
    def generate_test_template(
        module_name: str,
        class_name: str,
        methods: List[str]
    ) -> str:
        """
        Generate test template.
        
        Args:
            module_name: Module being tested
            class_name: Class being tested
            methods: List of methods to test
            
        Returns:
            Test file content
        """
        template = f'''"""Tests for {module_name} module."""

import pytest
from todo_cli.{module_name} import {class_name}


class Test{class_name}:
    """Test suite for {class_name}."""
    
'''
        for method in methods:
            template += f'''    def test_{method}_happy_path(self):
        """Should work with valid input."""
        # Arrange
        instance = {class_name}()
        
        # Act
        result = instance.{method}(valid_input)
        
        # Assert
        assert result == expected
    
    def test_{method}_invalid_input(self):
        """Should handle invalid input."""
        instance = {class_name}()
        
        with pytest.raises(ValueError):
            instance.{method}(invalid_input)
    
'''
        
        return template
```

---

### 4. Documentation Skill

**Purpose**: Generate and validate documentation

**Inputs**:
- `code`: Code to document
- `style`: Documentation style (default: "google")

**Outputs**:
- `docstring`: Generated documentation
- `is_complete`: boolean

**Implementation Template**:
```python
# File: src/todo_cli/skills/documentation.py
# [Skill]: Documentation

"""
Reusable documentation skill.

Generates Google-style docstrings and validates completeness.
"""

import ast
import inspect
from typing import Optional
from dataclasses import dataclass


@dataclass
class DocstringInfo:
    """Docstring information."""
    present: bool
    complete: bool
    has_args: bool
    has_returns: bool
    has_raises: bool
    has_examples: bool


class DocumentationSkill:
    """Reusable documentation skill."""
    
    @staticmethod
    def generate_function_docstring(
        func_name: str,
        params: dict,
        return_type: str,
        raises: list = None,
        brief: str = ""
    ) -> str:
        """
        Generate Google-style docstring.
        
        Args:
            func_name: Name of function
            params: Dict of {param_name: (type, description)}
            return_type: Return type description
            raises: List of (ExceptionType, description)
            brief: Brief one-line description
            
        Returns:
            Formatted docstring
        """
        doc = f'"""\n    {brief or f"{func_name} function."}\n'
        
        if len(params) > 0:
            doc += '\n    Args:\n'
            for name, (ptype, desc) in params.items():
                doc += f'        {name}: {desc}\n'
        
        if return_type:
            doc += f'\n    Returns:\n        {return_type}\n'
        
        if raises:
            doc += '\n    Raises:\n'
            for exc_type, desc in raises:
                doc += f'        {exc_type}: {desc}\n'
        
        doc += '    """'
        return doc
    
    @staticmethod
    def validate_docstring(code: str) -> DocstringInfo:
        """
        Validate docstring completeness.
        
        Args:
            code: Python source code
            
        Returns:
            DocstringInfo with validation results
        """
        tree = ast.parse(code)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                
                if not docstring:
                    return DocstringInfo(
                        present=False,
                        complete=False,
                        has_args=False,
                        has_returns=False,
                        has_raises=False,
                        has_examples=False
                    )
                
                return DocstringInfo(
                    present=True,
                    complete="Args:" in docstring and "Returns:" in docstring,
                    has_args="Args:" in docstring,
                    has_returns="Returns:" in docstring,
                    has_raises="Raises:" in docstring,
                    has_examples="Example:" in docstring or ">>>" in docstring
                )
        
        return DocstringInfo(
            present=False,
            complete=False,
            has_args=False,
            has_returns=False,
            has_raises=False,
            has_examples=False
        )
```

---

### 5. Error Handling Skill

**Purpose**: Standardized error handling patterns

**Inputs**:
- `error_type`: Type of error (validation, not_found, system)
- `context`: Error context information

**Outputs**:
- `exception`: Appropriate exception instance
- `user_message`: User-friendly message
- `log_message`: Technical log message

**Implementation Template**:
```python
# File: src/todo_cli/skills/error_handling.py
# [Skill]: Error Handling

"""
Reusable error handling skill.

Provides standardized error handling patterns.
"""

from typing import Optional, Type
from dataclasses import dataclass


@dataclass
class ErrorContext:
    """Error context information."""
    operation: str
    input_value: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None


@dataclass
class ErrorInfo:
    """Error information."""
    exception: Exception
    user_message: str
    log_message: str
    should_retry: bool


class ErrorHandlingSkill:
    """Reusable error handling skill."""
    
    @staticmethod
    def validation_error(
        field: str,
        value: any,
        constraint: str
    ) -> ErrorInfo:
        """
        Create validation error.
        
        Args:
            field: Field name
            value: Invalid value
            constraint: Constraint that was violated
            
        Returns:
            ErrorInfo
        """
        user_msg = f"{field} validation failed: {constraint}"
        log_msg = f"Validation error: {field}='{value}' violates {constraint}"
        
        return ErrorInfo(
            exception=ValueError(user_msg),
            user_message=user_msg,
            log_message=log_msg,
            should_retry=True
        )
    
    @staticmethod
    def not_found_error(
        entity: str,
        identifier: any
    ) -> ErrorInfo:
        """
        Create not found error.
        
        Args:
            entity: Entity type (e.g., "Task")
            identifier: Entity identifier
            
        Returns:
            ErrorInfo
        """
        user_msg = f"{entity} #{identifier} not found"
        log_msg = f"{entity} lookup failed: id={identifier}"
        
        return ErrorInfo(
            exception=KeyError(user_msg),
            user_message=user_msg,
            log_message=log_msg,
            should_retry=False
        )
    
    @staticmethod
    def format_error_message(
        error: Exception,
        context: ErrorContext
    ) -> str:
        """
        Format error for user display.
        
        Args:
            error: The exception
            context: Error context
            
        Returns:
            Formatted error message
        """
        msg = f"❌ Error in {context.operation}: {str(error)}"
        
        if context.input_value:
            msg += f"\nInput: {context.input_value}"
        
        if context.expected:
            msg += f"\nExpected: {context.expected}"
        
        if context.actual:
            msg += f"\nActual: {context.actual}"
        
        return msg
```

---

### 6. Formatting Skill

**Purpose**: Format output for display

**Inputs**:
- `data`: Data to format
- `format_type`: Output format (table, list, json, etc.)

**Outputs**:
- `formatted_output`: Formatted string

**Implementation Template**:
```python
# File: src/todo_cli/skills/formatting.py
# [Skill]: Formatting

"""
Reusable formatting skill.

Provides output formatting for CLI display.
"""

from typing import List, Dict, Any
from datetime import datetime


class FormattingSkill:
    """Reusable formatting skill."""
    
    @staticmethod
    def format_task_list(tasks: List[Any]) -> str:
        """
        Format tasks as a table.
        
        Args:
            tasks: List of Task objects
            
        Returns:
            Formatted table string
        """
        if not tasks:
            return "No tasks found."
        
        output = "\n"
        output += "ID  | Status | Title\n"
        output += "----|--------|" + "-" * 50 + "\n"
        
        for task in tasks:
            status = "✅" if task.completed else "⬜"
            title = task.title[:47] + "..." if len(task.title) > 50 else task.title
            output += f"{task.id:<3} | {status:^6} | {title}\n"
        
        return output
    
    @staticmethod
    def format_task_detail(task: Any) -> str:
        """
        Format single task details.
        
        Args:
            task: Task object
            
        Returns:
            Formatted detail string
        """
        status = "✅ Completed" if task.completed else "⬜ Pending"
        
        output = f"\n{'=' * 60}\n"
        output += f"Task #{task.id}\n"
        output += f"{'=' * 60}\n\n"
        output += f"Title: {task.title}\n"
        output += f"Status: {status}\n"
        output += f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        
        if task.description:
            output += f"\nDescription:\n{task.description}\n"
        
        output += f"\n{'=' * 60}\n"
        
        return output
    
    @staticmethod
    def format_success(message: str) -> str:
        """Format success message."""
        return f"✅ {message}"
    
    @staticmethod
    def format_error(message: str) -> str:
        """Format error message."""
        return f"❌ {message}"
    
    @staticmethod
    def format_info(message: str) -> str:
        """Format info message."""
        return f"ℹ️  {message}"
```

---

## 🔧 Skill Composition Patterns

### Pattern 1: Validation → Error Handling
```python
from todo_cli.skills.validation import ValidationSkill, ValidationRule
from todo_cli.skills.error_handling import ErrorHandlingSkill, ErrorContext

def add_task(title: str) -> Task:
    # Use validation skill
    rule = ValidationRule(type="string", min_length=1, max_length=200)
    result = ValidationSkill.validate_string(title, rule)
    
    if not result.valid:
        # Use error handling skill
        error_info = ErrorHandlingSkill.validation_error(
            field="title",
            value=title,
            constraint="1-200 characters"
        )
        raise error_info.exception
    
    # Proceed with validated value
    task = Task(id=0, title=result.cleaned_value)
    return storage.add(task)
```

### Pattern 2: Testing → Documentation → Type Checking
```python
from todo_cli.skills.testing import TestingSkill
from todo_cli.skills.documentation import DocumentationSkill
from todo_cli.skills.type_checking import TypeCheckingSkill

def validate_implementation(module_path: str) -> bool:
    """Validate implementation quality using skills."""
    
    # 1. Check documentation
    with open(module_path) as f:
        code = f.read()
    doc_info = DocumentationSkill.validate_docstring(code)
    
    if not doc_info.complete:
        print("❌ Documentation incomplete")
        return False
    
    # 2. Check types
    type_result = TypeCheckingSkill.check_files([module_path])
    
    if not type_result.success:
        print(f"❌ Type errors: {type_result.error_count}")
        return False
    
    # 3. Run tests
    test_result = TestingSkill.run_tests(
        test_file=f"tests/test_{module_path.split('/')[-1]}",
        threshold=90
    )
    
    if not test_result.tests_passed:
        print(f"❌ Tests failed: {test_result.failed_tests}")
        return False
    
    if test_result.coverage_percentage < 90:
        print(f"❌ Coverage too low: {test_result.coverage_percentage}%")
        return False
    
    print("✅ All quality checks passed!")
    return True
```

---

## 📚 Skill Usage in Agents

### Specification Agent Uses:
- Validation Skill (to define validation rules)
- Documentation Skill (to document requirements)

### Architecture Agent Uses:
- Documentation Skill (to document design)
- Error Handling Skill (to plan error strategies)

### Implementation Agent Uses:
- Validation Skill (for input validation)
- Type Checking Skill (to verify types)
- Testing Skill (to generate tests)
- Documentation Skill (to generate docstrings)
- Error Handling Skill (for error handling)
- Formatting Skill (for output display)

### QA Agent Uses:
- Type Checking Skill
- Testing Skill
- Documentation Skill (validation)

---

## 📖 Skills Documentation Template

Each skill should have:

```markdown
# {Skill Name} Skill

## Purpose
Brief description of what the skill does

## When to Use
- Use case 1
- Use case 2

## Inputs
- param1: Description
- param2: Description

## Outputs
- output1: Description
- output2: Description

## Usage Example
```python
from todo_cli.skills.{skill} import {SkillClass}

result = SkillClass.method(inputs)
```

## Quality Standards
- How to ensure quality
- Edge cases to handle

## Related Skills
- Skill that commonly combines with this
```

---

## 🎯 Creating New Skills

When creating a new skill:

1. ✅ **Single Responsibility**: One clear purpose
2. ✅ **Reusable**: Works across multiple agents
3. ✅ **Well-Documented**: Clear inputs/outputs
4. ✅ **Testable**: Can be tested independently
5. ✅ **Composable**: Works well with other skills

---

This skills system provides the foundation for Phase I agents to work efficiently and consistently!
