# Feature Specification: Task CRUD Operations

**Feature Branch**: `002-task-crud-api`
**Created**: 2026-01-08
**Status**: Draft
**Input**: User description: "Comprehensive task CRUD specification for Phase II web application"

## Overview

This specification defines the complete Create, Read, Update, Delete (CRUD) operations for tasks in the Evolution of Todo web application. Tasks are the core domain entity, representing user-defined action items with title, description, and status tracking. All operations are scoped to authenticated users, ensuring data isolation and security.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create New Task (Priority: P1)

As a user, I want to create a new task with a title and optional description so that I can track things I need to do.

**Why this priority**: Creating tasks is the foundational operation of the todo application. Without task creation, no other functionality has value. This is the absolute minimum viable product.

**Independent Test**: Can be fully tested by submitting a task creation form and verifying the task appears in the task list with the correct data and system-generated ID.

**Acceptance Scenarios**:

1. **Given** I am an authenticated user on the task list page, **When** I enter a title "Buy groceries" and click "Create Task", **Then** a new task with status "pending" is created and appears at the top of my task list with a unique ID and current timestamp
2. **Given** I am creating a task, **When** I enter a title "Meeting prep" and description "Prepare slides for Q1 review", **Then** the task is created with both title and description stored correctly
3. **Given** I am creating a task, **When** I submit an empty title, **Then** I see an error message "Title is required (1-200 characters)" and the task is not created
4. **Given** I am creating a task, **When** I enter a title with 201 characters, **Then** I see an error message "Title must not exceed 200 characters" and the task is not created
5. **Given** I am creating a task, **When** I enter a description with 2001 characters, **Then** I see an error message "Description must not exceed 2000 characters" and the task is not created

---

### User Story 2 - View All My Tasks (Priority: P1)

As a user, I want to view a list of all my tasks so that I can see what I need to do.

**Why this priority**: Viewing tasks is essential for the application to be useful. Without this, users cannot see what they've created. This must be implemented alongside creation for a viable MVP.

**Independent Test**: Can be fully tested by creating multiple tasks and verifying they all appear in the task list in the correct order (newest first by default).

**Acceptance Scenarios**:

1. **Given** I have created 5 tasks, **When** I open the task list page, **Then** I see all 5 tasks displayed in reverse chronological order (newest first)
2. **Given** I have no tasks, **When** I open the task list page, **Then** I see a message "No tasks yet. Create your first task!"
3. **Given** I have 100 tasks, **When** I open the task list page, **Then** I see the first 20 tasks (pagination default) with a "Load More" button
4. **Given** another user has created tasks, **When** I view my task list, **Then** I only see my own tasks, not tasks from other users

---

### User Story 3 - View Single Task Details (Priority: P2)

As a user, I want to click on a task to see its full details so that I can review all information about a specific task.

**Why this priority**: While important for user experience, this is not strictly required for a minimal todo app. Users can see key information in the list view. This enhances the experience but is not foundational.

**Independent Test**: Can be fully tested by clicking on a task in the list and verifying the detail view shows complete task information including full description, timestamps, and status.

**Acceptance Scenarios**:

1. **Given** I am viewing my task list, **When** I click on a task with title "Buy groceries", **Then** I see a detail view showing the full title, description, status, created date, and last updated date
2. **Given** I am viewing task details, **When** the task has a long description, **Then** the full description is displayed without truncation
3. **Given** I attempt to view a task by entering a URL with an invalid task ID, **When** the page loads, **Then** I see a 404 error "Task not found"
4. **Given** I attempt to view another user's task by ID, **When** the page loads, **Then** I see a 403 error "Access denied" and cannot view the task

---

### User Story 4 - Update Task Information (Priority: P1)

As a user, I want to edit my task's title, description, or status so that I can keep my tasks accurate and up to date.

**Why this priority**: Editing is critical because users make mistakes and tasks evolve. Without editing, users must delete and recreate tasks, which is a poor experience and loses data like creation timestamps.

**Independent Test**: Can be fully tested by editing a task's fields and verifying the changes persist and the updated_at timestamp is refreshed.

**Acceptance Scenarios**:

1. **Given** I am viewing a task with title "Buy groceries", **When** I click "Edit", change the title to "Buy groceries and milk", and save, **Then** the task title is updated and updated_at timestamp is refreshed
2. **Given** I am editing a task, **When** I change the status from "pending" to "in_progress", **Then** the status is updated and reflected in the task list
3. **Given** I am editing a task, **When** I change the status to "completed", **Then** the task moves to the completed section and shows a completion checkmark
4. **Given** I am editing a task, **When** I clear the title field and try to save, **Then** I see an error "Title is required" and changes are not saved
5. **Given** I am editing a task, **When** I update only the description, **Then** only the description and updated_at fields change, other fields remain unchanged

---

### User Story 5 - Mark Task as Complete/Incomplete (Priority: P2)

As a user, I want to quickly mark tasks as complete or incomplete with a single click so that I can efficiently track my progress.

**Why this priority**: While important for usability, this is essentially a shortcut for the update operation. Users could achieve the same result by editing status. This enhances workflow efficiency.

**Independent Test**: Can be fully tested by clicking a checkbox or toggle button and verifying the task status changes between "completed" and "pending" immediately.

**Acceptance Scenarios**:

1. **Given** I have a task with status "pending", **When** I click the checkbox next to it, **Then** the status changes to "completed" and the task is visually marked as complete
2. **Given** I have a task with status "completed", **When** I click the checkbox to uncheck it, **Then** the status changes back to "pending" and the completion mark is removed
3. **Given** I mark a task as complete, **When** the status update succeeds, **Then** the updated_at timestamp is refreshed automatically
4. **Given** I have many tasks, **When** I mark one as complete, **Then** only that task's status changes, others remain unchanged

---

### User Story 6 - Delete Task (Priority: P2)

As a user, I want to delete tasks I no longer need so that my task list stays clean and relevant.

**Why this priority**: Deletion is important but not critical for initial MVP. Users can work around missing deletion by leaving tasks uncompleted or marking them as completed. However, it's essential for long-term usability.

**Independent Test**: Can be fully tested by deleting a task and verifying it no longer appears in the task list and returns 404 if accessed by ID.

**Acceptance Scenarios**:

1. **Given** I am viewing my task list, **When** I click "Delete" on a task and confirm the deletion, **Then** the task is permanently removed from my list
2. **Given** I am deleting a task, **When** I click "Delete", **Then** I see a confirmation dialog "Are you sure you want to delete this task? This action cannot be undone"
3. **Given** I have confirmed task deletion, **When** the deletion completes, **Then** I see a success message "Task deleted successfully" and the task disappears from the list
4. **Given** I attempt to delete a non-existent task, **When** the API request is sent, **Then** I receive a 404 error "Task not found"
5. **Given** I attempt to delete another user's task, **When** the API request is sent, **Then** I receive a 403 error "Access denied"

---

### User Story 7 - Filter Tasks by Status (Priority: P3)

As a user, I want to filter my tasks by status (all, active, completed) so that I can focus on specific categories of tasks.

**Why this priority**: Filtering enhances usability for users with many tasks but is not essential for basic todo functionality. Users can manage without this in early versions.

**Independent Test**: Can be fully tested by creating tasks with different statuses and verifying that filter buttons show only the relevant tasks.

**Acceptance Scenarios**:

1. **Given** I have 10 pending tasks and 5 completed tasks, **When** I click the "Active" filter, **Then** I see only the 10 pending tasks
2. **Given** I have tasks with different statuses, **When** I click the "Completed" filter, **Then** I see only tasks with status "completed"
3. **Given** I have filtered to show only active tasks, **When** I click "All" filter, **Then** I see all tasks regardless of status
4. **Given** I have filtered tasks, **When** I mark a task as complete, **Then** the filter updates automatically to reflect the new status

---

### User Story 8 - Search Tasks by Title/Description (Priority: P3)

As a user, I want to search my tasks by keywords in the title or description so that I can quickly find specific tasks.

**Why this priority**: Search is a nice-to-have feature for users with many tasks but not essential for basic functionality. This can be added after core CRUD operations are stable.

**Independent Test**: Can be fully tested by entering a search query and verifying that only tasks matching the keyword in title or description are displayed.

**Acceptance Scenarios**:

1. **Given** I have tasks with various titles, **When** I enter "groceries" in the search box, **Then** I see only tasks containing "groceries" in the title or description
2. **Given** I have performed a search, **When** I clear the search box, **Then** all tasks are displayed again
3. **Given** I search for a keyword that doesn't match any tasks, **When** the search completes, **Then** I see a message "No tasks found matching 'keyword'"
4. **Given** I am searching, **When** I combine search with status filter, **Then** I see only tasks that match both the search term and status filter

---

### User Story 9 - Sort Tasks (Priority: P3)

As a user, I want to sort my tasks by created date, updated date, or title so that I can organize my task list according to my preference.

**Why this priority**: Sorting is a nice-to-have feature that enhances usability but is not critical. Default chronological ordering is sufficient for initial versions.

**Independent Test**: Can be fully tested by clicking sort options and verifying tasks reorder correctly according to the selected criterion.

**Acceptance Scenarios**:

1. **Given** I have multiple tasks, **When** I select "Sort by: Title (A-Z)", **Then** tasks are displayed in alphabetical order by title
2. **Given** I have multiple tasks, **When** I select "Sort by: Created Date (Newest)", **Then** tasks are displayed with newest first
3. **Given** I have multiple tasks, **When** I select "Sort by: Updated Date (Newest)", **Then** tasks are displayed with most recently updated first
4. **Given** I have sorted tasks, **When** I combine sorting with filtering, **Then** the filtered results are sorted according to the selected criterion

---

### Edge Cases

1. **Concurrent Updates**: What happens when two users (or two browser tabs of the same user) try to update the same task simultaneously?
   - System MUST use optimistic locking or last-write-wins strategy
   - updated_at timestamp ensures latest change is tracked

2. **Long-Running Operations**: How does the system handle slow network conditions during create/update/delete operations?
   - UI MUST show loading states
   - Operations MUST have timeout handling (30 seconds)
   - Failed operations MUST show clear error messages

3. **Pagination Edge Cases**: What happens when viewing page 5 of tasks and deleting items causes fewer total pages?
   - System MUST redirect to last valid page
   - System MUST handle empty pages gracefully

4. **Whitespace Handling**: What happens when user enters only whitespace in title?
   - System MUST trim whitespace before validation
   - Empty strings after trimming MUST be rejected

5. **Special Characters**: How does system handle emojis, unicode, or special HTML characters in title/description?
   - System MUST support full UTF-8 character set
   - System MUST sanitize input to prevent XSS attacks
   - System MUST escape HTML entities

6. **Database Connection Failures**: What happens when database is unavailable during CRUD operation?
   - System MUST return 503 Service Unavailable
   - System MUST log error for monitoring
   - User MUST see friendly error message with retry option

7. **Invalid UUID Format**: What happens when API receives malformed task ID?
   - System MUST validate UUID format
   - System MUST return 400 Bad Request with clear error message

8. **Deleted Task References**: What happens when user has a task detail page open and another session deletes it?
   - System MUST handle 404 gracefully on any subsequent operation
   - System MUST show "This task has been deleted" message

9. **Rate Limiting**: What happens when user makes too many rapid requests?
   - System SHOULD implement rate limiting (100 requests per minute per user)
   - System MUST return 429 Too Many Requests with Retry-After header

10. **Large Description Text**: How does UI handle tasks with 2000-character descriptions?
    - List view MUST truncate to 100 characters with "..." indicator
    - Detail view MUST display full text with proper word wrapping

## Requirements *(mandatory)*

### Functional Requirements

#### Create Operation

- **FR-001**: System MUST allow authenticated users to create new tasks with required title field
- **FR-002**: System MUST validate title is between 1 and 200 characters (after trimming whitespace)
- **FR-003**: System MUST allow optional description field up to 2000 characters
- **FR-004**: System MUST automatically set status to "pending" for new tasks
- **FR-005**: System MUST generate unique UUID for each task
- **FR-006**: System MUST automatically capture created_at timestamp in UTC
- **FR-007**: System MUST automatically capture updated_at timestamp in UTC (same as created_at on creation)
- **FR-008**: System MUST associate task with authenticated user's ID (from JWT token)
- **FR-009**: System MUST return 201 Created status with full task object including generated ID and timestamps
- **FR-010**: System MUST return 400 Bad Request with validation errors for invalid input

#### Read Operations

- **FR-011**: System MUST provide endpoint to retrieve all tasks for authenticated user
- **FR-012**: System MUST return tasks in reverse chronological order by created_at (newest first) by default
- **FR-013**: System MUST support pagination with configurable page and limit parameters
- **FR-014**: System MUST default to 20 tasks per page if limit not specified
- **FR-015**: System MUST provide endpoint to retrieve single task by ID
- **FR-016**: System MUST return 404 Not Found if task ID does not exist
- **FR-017**: System MUST return 403 Forbidden if task belongs to different user
- **FR-018**: System MUST support filtering by status query parameter (pending, in_progress, completed)
- **FR-019**: System MUST support search by keyword in title or description (case-insensitive)
- **FR-020**: System MUST support sorting by created_at, updated_at, or title (ascending/descending)
- **FR-021**: System MUST include total count of tasks in list response for pagination
- **FR-022**: System MUST return empty array (not null) when user has no tasks

#### Update Operations

- **FR-023**: System MUST provide endpoint to update task fields (full update with PUT)
- **FR-024**: System MUST provide endpoint for partial updates (PATCH)
- **FR-025**: System MUST validate updated fields using same rules as creation
- **FR-026**: System MUST automatically update updated_at timestamp on any field change
- **FR-027**: System MUST return 404 Not Found if task ID does not exist
- **FR-028**: System MUST return 403 Forbidden if task belongs to different user
- **FR-029**: System MUST return 200 OK with updated task object on success
- **FR-030**: System MUST return 400 Bad Request with validation errors for invalid updates
- **FR-031**: System MUST preserve created_at timestamp (never modify)
- **FR-032**: System MUST allow status transitions: pending ↔ in_progress ↔ completed
- **FR-033**: System MUST validate status is one of allowed enum values

#### Delete Operations

- **FR-034**: System MUST provide endpoint to permanently delete task by ID
- **FR-035**: System MUST return 204 No Content on successful deletion
- **FR-036**: System MUST return 404 Not Found if task ID does not exist
- **FR-037**: System MUST return 403 Forbidden if task belongs to different user
- **FR-038**: System MUST permanently remove task from database (hard delete)
- **FR-039**: System MUST NOT allow recovery of deleted tasks (Phase II requirement)
- **FR-040**: System SHOULD implement soft delete architecture for future undo feature (optional)

#### Security & Authorization

- **FR-041**: System MUST require valid JWT token for all CRUD operations
- **FR-042**: System MUST extract user_id from JWT payload for all operations
- **FR-043**: System MUST filter all queries by authenticated user's ID
- **FR-044**: System MUST return 401 Unauthorized if JWT is missing, invalid, or expired
- **FR-045**: System MUST prevent users from accessing other users' tasks
- **FR-046**: System MUST sanitize all input to prevent XSS attacks
- **FR-047**: System MUST sanitize all input to prevent SQL injection attacks
- **FR-048**: System MUST validate UUID format for task IDs
- **FR-049**: System MUST implement rate limiting to prevent abuse
- **FR-050**: System MUST log all security-related errors (auth failures, forbidden access)

#### Performance Requirements

- **FR-051**: System MUST return task list in < 100ms for users with up to 1000 tasks
- **FR-052**: System MUST return single task by ID in < 20ms
- **FR-053**: System MUST complete create/update/delete operations in < 50ms
- **FR-054**: System MUST handle 100 concurrent requests per second without degradation
- **FR-055**: System MUST implement database indexes on user_id, status, and created_at
- **FR-056**: System MUST use connection pooling for database efficiency

#### Data Integrity Requirements

- **FR-057**: System MUST ensure task IDs are unique across all users
- **FR-058**: System MUST enforce foreign key constraint between tasks and users
- **FR-059**: System MUST use UTC timezone for all timestamps
- **FR-060**: System MUST ensure created_at is never modified after creation
- **FR-061**: System MUST ensure updated_at is automatically updated on every modification
- **FR-062**: System MUST handle database transaction rollback on errors

### Key Entities

- **Task**: Represents a user-defined action item with tracking information
  - Attributes: id (UUID), user_id (UUID), title (string), description (text), status (enum), created_at (timestamp), updated_at (timestamp)
  - Relationships: Belongs to one User
  - Constraints: title required and 1-200 chars, description optional max 2000 chars, status must be valid enum

- **User**: Represents an authenticated user (defined in authentication spec)
  - Attributes: id (UUID), email, hashed_password, created_at, updated_at
  - Relationships: Has many Tasks
  - Note: Full user entity defined in specs/features/authentication.md

- **TaskStatus**: Enumeration of valid task states
  - Values: "pending", "in_progress", "completed"
  - Default: "pending"
  - Transitions: All states can transition to any other state

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a task in under 5 seconds from clicking "New Task" to seeing it in the list
- **SC-002**: System handles 1000 tasks per user with list view loading in under 100ms
- **SC-003**: 95% of CRUD operations complete successfully within 50ms response time
- **SC-004**: Zero instances of users accessing other users' tasks in production
- **SC-005**: Task list updates in real-time after create/update/delete operations without requiring page refresh
- **SC-006**: 100% of validation errors provide clear, actionable error messages to users
- **SC-007**: System maintains 99.9% uptime for task CRUD operations
- **SC-008**: Search functionality returns results in under 200ms for users with 1000+ tasks
- **SC-009**: All CRUD endpoints achieve > 95% test coverage
- **SC-010**: Users can successfully complete all CRUD operations on mobile devices with touch-friendly UI

### User Experience Metrics

- **SC-011**: 90% of users successfully create their first task on first attempt without errors
- **SC-012**: Average time to mark task as complete is under 2 seconds
- **SC-013**: Users report task list is "easy to navigate" in > 85% of usability tests
- **SC-014**: Zero data loss incidents during concurrent edit scenarios
- **SC-015**: Error messages result in successful retry in > 80% of cases

## API Contract Reference

Full API specifications are defined in:
- **Create Task**: specs/phase-2-todo-web/api/tasks-api.md#create-task
- **List Tasks**: specs/phase-2-todo-web/api/tasks-api.md#list-tasks
- **Get Task**: specs/phase-2-todo-web/api/tasks-api.md#get-task
- **Update Task**: specs/phase-2-todo-web/api/tasks-api.md#update-task
- **Delete Task**: specs/phase-2-todo-web/api/tasks-api.md#delete-task

## Database Schema Reference

Full database schema is defined in:
- **Tasks Table**: specs/phase-2-todo-web/database/tasks-schema.md
- **Relationships**: specs/phase-2-todo-web/database/erd.md
- **Migrations**: specs/phase-2-todo-web/database/migrations.md

## UI Components Reference

UI implementations are specified in:
- **Task List Page**: specs/phase-2-todo-web/ui/task-list-page.md
- **Task Form Component**: specs/phase-2-todo-web/ui/task-form.md
- **Task Item Component**: specs/phase-2-todo-web/ui/task-item.md
- **Task Detail Page**: specs/phase-2-todo-web/ui/task-detail-page.md

## Dependencies

### Required Features

- **Authentication System**: specs/features/authentication.md
  - JWT token generation and validation
  - User identity extraction from tokens
  - User session management

### Optional Features (Future Enhancements)

- **Task Categories/Tags**: specs/features/task-categories.md (not yet created)
- **Task Priorities**: specs/features/task-priorities.md (not yet created)
- **Task Due Dates**: specs/features/task-due-dates.md (not yet created)
- **Task Collaboration**: specs/features/task-sharing.md (not yet created)
- **Soft Delete & Undo**: specs/features/task-recovery.md (not yet created)

## Validation Rules

### Title Validation

```typescript
// Pseudocode for title validation
function validateTitle(title: string): ValidationResult {
  const trimmed = title.trim();

  if (trimmed.length === 0) {
    return { valid: false, error: "Title is required (1-200 characters)" };
  }

  if (trimmed.length > 200) {
    return { valid: false, error: "Title must not exceed 200 characters" };
  }

  // Check for XSS patterns
  if (containsHTMLTags(trimmed)) {
    return { valid: false, error: "Title cannot contain HTML tags" };
  }

  return { valid: true };
}
```

### Description Validation

```typescript
// Pseudocode for description validation
function validateDescription(description: string | null): ValidationResult {
  if (description === null || description === undefined) {
    return { valid: true }; // Optional field
  }

  if (description.length > 2000) {
    return { valid: false, error: "Description must not exceed 2000 characters" };
  }

  // Check for XSS patterns
  if (containsScriptTags(description)) {
    return { valid: false, error: "Description cannot contain script tags" };
  }

  return { valid: true };
}
```

### Status Validation

```typescript
// Pseudocode for status validation
const VALID_STATUSES = ["pending", "in_progress", "completed"];

function validateStatus(status: string): ValidationResult {
  if (!VALID_STATUSES.includes(status)) {
    return {
      valid: false,
      error: `Status must be one of: ${VALID_STATUSES.join(", ")}`
    };
  }

  return { valid: true };
}
```

### UUID Validation

```typescript
// Pseudocode for UUID validation
function validateUUID(id: string): ValidationResult {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

  if (!uuidRegex.test(id)) {
    return { valid: false, error: "Invalid task ID format" };
  }

  return { valid: true };
}
```

## Test Scenarios (Given/When/Then)

### Create Task Tests

#### Test 1: Create task with valid title only
- **Given** I am an authenticated user with valid JWT token
- **When** I POST to /api/tasks with body `{ "title": "Buy groceries" }`
- **Then** I receive 201 Created status
- **And** Response contains task with id, user_id, title "Buy groceries", status "pending", null description, created_at, updated_at

#### Test 2: Create task with title and description
- **Given** I am an authenticated user
- **When** I POST to /api/tasks with body `{ "title": "Meeting prep", "description": "Prepare slides" }`
- **Then** I receive 201 Created status
- **And** Response contains task with title "Meeting prep" and description "Prepare slides"

#### Test 3: Create task with empty title
- **Given** I am an authenticated user
- **When** I POST to /api/tasks with body `{ "title": "" }`
- **Then** I receive 400 Bad Request status
- **And** Response contains error "Title is required (1-200 characters)"

#### Test 4: Create task with title exceeding max length
- **Given** I am an authenticated user
- **When** I POST to /api/tasks with title of 201 characters
- **Then** I receive 400 Bad Request status
- **And** Response contains error "Title must not exceed 200 characters"

#### Test 5: Create task with description exceeding max length
- **Given** I am an authenticated user
- **When** I POST to /api/tasks with description of 2001 characters
- **Then** I receive 400 Bad Request status
- **And** Response contains error "Description must not exceed 2000 characters"

#### Test 6: Create task without authentication
- **Given** I do not have a valid JWT token
- **When** I POST to /api/tasks with valid body
- **Then** I receive 401 Unauthorized status
- **And** Response contains error "Authentication required"

#### Test 7: Create task with whitespace-only title
- **Given** I am an authenticated user
- **When** I POST to /api/tasks with body `{ "title": "   " }`
- **Then** I receive 400 Bad Request status
- **And** Response contains error "Title is required (1-200 characters)"

### Read Tasks Tests

#### Test 8: List all tasks for authenticated user
- **Given** I am an authenticated user with 5 tasks
- **When** I GET /api/tasks
- **Then** I receive 200 OK status
- **And** Response contains array of 5 tasks ordered by created_at DESC
- **And** Response contains total count of 5

#### Test 9: List tasks when user has no tasks
- **Given** I am an authenticated user with zero tasks
- **When** I GET /api/tasks
- **Then** I receive 200 OK status
- **And** Response contains empty array
- **And** Response contains total count of 0

#### Test 10: List tasks with pagination
- **Given** I am an authenticated user with 50 tasks
- **When** I GET /api/tasks?page=2&limit=20
- **Then** I receive 200 OK status
- **And** Response contains 20 tasks (tasks 21-40)
- **And** Response contains total count of 50
- **And** Response contains pagination metadata (page 2, limit 20, total_pages 3)

#### Test 11: Get single task by ID
- **Given** I am an authenticated user with a task having ID "123e4567-e89b-12d3-a456-426614174000"
- **When** I GET /api/tasks/123e4567-e89b-12d3-a456-426614174000
- **Then** I receive 200 OK status
- **And** Response contains the task with all fields

#### Test 12: Get non-existent task
- **Given** I am an authenticated user
- **When** I GET /api/tasks/123e4567-e89b-12d3-a456-426614174999 (non-existent ID)
- **Then** I receive 404 Not Found status
- **And** Response contains error "Task not found"

#### Test 13: Get another user's task
- **Given** I am authenticated as user A
- **And** User B has a task with ID "123e4567-e89b-12d3-a456-426614174000"
- **When** I GET /api/tasks/123e4567-e89b-12d3-a456-426614174000
- **Then** I receive 403 Forbidden status
- **And** Response contains error "Access denied"

#### Test 14: Filter tasks by status
- **Given** I have 10 pending tasks and 5 completed tasks
- **When** I GET /api/tasks?status=completed
- **Then** I receive 200 OK status
- **And** Response contains array of 5 completed tasks only

#### Test 15: Search tasks by keyword
- **Given** I have tasks with titles "Buy groceries", "Buy milk", "Clean house"
- **When** I GET /api/tasks?search=buy
- **Then** I receive 200 OK status
- **And** Response contains 2 tasks ("Buy groceries" and "Buy milk")

#### Test 16: Sort tasks by title ascending
- **Given** I have tasks with titles "Zebra", "Apple", "Banana"
- **When** I GET /api/tasks?sort=title&order=asc
- **Then** I receive 200 OK status
- **And** Response contains tasks in order: "Apple", "Banana", "Zebra"

#### Test 17: List tasks with invalid UUID format
- **Given** I am an authenticated user
- **When** I GET /api/tasks/invalid-uuid
- **Then** I receive 400 Bad Request status
- **And** Response contains error "Invalid task ID format"

### Update Task Tests

#### Test 18: Update task title
- **Given** I have a task with title "Buy groceries"
- **When** I PUT /api/tasks/{id} with body `{ "title": "Buy groceries and milk" }`
- **Then** I receive 200 OK status
- **And** Response contains task with updated title "Buy groceries and milk"
- **And** updated_at timestamp is refreshed
- **And** created_at timestamp is unchanged

#### Test 19: Update task status
- **Given** I have a task with status "pending"
- **When** I PATCH /api/tasks/{id} with body `{ "status": "completed" }`
- **Then** I receive 200 OK status
- **And** Response contains task with status "completed"
- **And** updated_at timestamp is refreshed

#### Test 20: Update task with empty title
- **Given** I have a task
- **When** I PUT /api/tasks/{id} with body `{ "title": "" }`
- **Then** I receive 400 Bad Request status
- **And** Response contains error "Title is required (1-200 characters)"
- **And** Task is not modified

#### Test 21: Update task with invalid status
- **Given** I have a task
- **When** I PATCH /api/tasks/{id} with body `{ "status": "invalid_status" }`
- **Then** I receive 400 Bad Request status
- **And** Response contains error "Status must be one of: pending, in_progress, completed"

#### Test 22: Update non-existent task
- **Given** I am an authenticated user
- **When** I PUT /api/tasks/123e4567-e89b-12d3-a456-426614174999 (non-existent ID)
- **Then** I receive 404 Not Found status
- **And** Response contains error "Task not found"

#### Test 23: Update another user's task
- **Given** I am authenticated as user A
- **And** User B has a task with ID "123e4567-e89b-12d3-a456-426614174000"
- **When** I PUT /api/tasks/123e4567-e89b-12d3-a456-426614174000
- **Then** I receive 403 Forbidden status
- **And** Response contains error "Access denied"

#### Test 24: Partial update (PATCH) multiple fields
- **Given** I have a task with title "Old title" and status "pending"
- **When** I PATCH /api/tasks/{id} with body `{ "title": "New title", "status": "in_progress" }`
- **Then** I receive 200 OK status
- **And** Response contains task with title "New title" and status "in_progress"
- **And** updated_at timestamp is refreshed

### Delete Task Tests

#### Test 25: Delete existing task
- **Given** I have a task with ID "123e4567-e89b-12d3-a456-426614174000"
- **When** I DELETE /api/tasks/123e4567-e89b-12d3-a456-426614174000
- **Then** I receive 204 No Content status
- **And** Task is permanently removed from database

#### Test 26: Delete non-existent task
- **Given** I am an authenticated user
- **When** I DELETE /api/tasks/123e4567-e89b-12d3-a456-426614174999 (non-existent ID)
- **Then** I receive 404 Not Found status
- **And** Response contains error "Task not found"

#### Test 27: Delete another user's task
- **Given** I am authenticated as user A
- **And** User B has a task with ID "123e4567-e89b-12d3-a456-426614174000"
- **When** I DELETE /api/tasks/123e4567-e89b-12d3-a456-426614174000
- **Then** I receive 403 Forbidden status
- **And** Response contains error "Access denied"

#### Test 28: Verify deleted task is inaccessible
- **Given** I have deleted a task with ID "123e4567-e89b-12d3-a456-426614174000"
- **When** I GET /api/tasks/123e4567-e89b-12d3-a456-426614174000
- **Then** I receive 404 Not Found status
- **And** Response contains error "Task not found"

### Error Handling Tests

#### Test 29: Database connection failure during create
- **Given** I am an authenticated user
- **And** Database connection is unavailable
- **When** I POST to /api/tasks with valid body
- **Then** I receive 503 Service Unavailable status
- **And** Response contains error "Service temporarily unavailable"

#### Test 30: Concurrent update conflict
- **Given** I have a task with updated_at "2026-01-08T10:00:00Z"
- **And** Another session updates the task to updated_at "2026-01-08T10:01:00Z"
- **When** I PUT /api/tasks/{id} with my changes
- **Then** I receive 200 OK status (last-write-wins)
- **And** My changes overwrite the previous update
- **And** updated_at is set to current timestamp

#### Test 31: XSS attempt in title
- **Given** I am an authenticated user
- **When** I POST to /api/tasks with body `{ "title": "<script>alert('xss')</script>" }`
- **Then** I receive 400 Bad Request status
- **And** Response contains error "Title cannot contain HTML tags"

#### Test 32: SQL injection attempt in search
- **Given** I am an authenticated user
- **When** I GET /api/tasks?search='; DROP TABLE tasks; --
- **Then** I receive 200 OK status
- **And** Search is safely parameterized
- **And** No tasks are deleted

## Implementation Notes

### Backend (FastAPI)

- Use SQLModel for ORM and Pydantic for validation
- Implement JWT authentication middleware
- Use dependency injection for database sessions
- Implement OpenAPI documentation automatically
- Use async/await for all database operations
- Implement proper error handling and logging
- Use database indexes for performance

### Frontend (Next.js)

- Use React Server Components for initial page load
- Use Client Components for interactive task list
- Implement optimistic updates for better UX
- Use SWR for data fetching and caching
- Implement proper error boundaries
- Use React Hook Form for form validation
- Implement loading skeletons for better UX

### Database (PostgreSQL)

- Use UUID for task IDs (uuid_generate_v4())
- Use TIMESTAMPTZ for timestamps (UTC)
- Create indexes on user_id, status, created_at
- Use foreign key constraints to users table
- Consider partial indexes for filtered queries

## Changelog

- **2026-01-08**: Initial specification created
