# Database Schema Specification

**Version**: 1.0
**Last Updated**: 2026-01-08
**Status**: Draft

---

## Table of Contents

1. [Database Overview](#1-database-overview)
2. [Users Table](#2-users-table)
3. [Tasks Table](#3-tasks-table)
4. [Indexes Strategy](#4-indexes-strategy)
5. [Relationships and Constraints](#5-relationships-and-constraints)
6. [Database Triggers](#6-database-triggers)
7. [SQLModel Definitions](#7-sqlmodel-definitions)
8. [Migration Scripts](#8-migration-scripts)
9. [Performance Considerations](#9-performance-considerations)
10. [Data Validation Strategy](#10-data-validation-strategy)
11. [Security Considerations](#11-security-considerations)
12. [Sample Data](#12-sample-data)
13. [Cross-References](#13-cross-references)

---

## 1. Database Overview

### Database Platform

- **Database**: PostgreSQL 15+ (Neon Serverless)
- **Provider**: Neon (https://neon.tech)
- **ORM**: SQLModel (combination of SQLAlchemy + Pydantic)
- **Migration Tool**: Alembic
- **Connection Pool**: SQLAlchemy async engine with connection pooling

### Connection Configuration

**Development**:
```
postgresql://localhost:5432/evolution_todo_dev
```

**Production (Neon)**:
```
postgresql://user:password@ep-cool-name-123456.us-east-2.aws.neon.tech/evolution_todo?sslmode=require
```

### Global Settings

- **Timezone**: All timestamps stored in UTC
- **Character Set**: UTF-8
- **Collation**: en_US.UTF-8
- **Connection Pool Size**: 20 connections (min: 5, max: 20)
- **Connection Timeout**: 30 seconds
- **Statement Timeout**: 30 seconds
- **Idle Transaction Timeout**: 60 seconds

### Schema Versioning

- **Current Version**: 1.0 (Initial schema)
- **Migration Strategy**: Alembic with autogenerate
- **Backward Compatibility**: All migrations must be reversible
- **Zero-Downtime Deployment**: Use expand-contract pattern for schema changes

---

## 2. Users Table

### Purpose

The `users` table stores authentication and user profile information. This table is managed by **Better Auth** but documented here for completeness and reference.

### Table Definition (SQL)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(254) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE
);
```

### Column Specifications

| Column | Type | Constraints | Default | Description |
|--------|------|-------------|---------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL | `gen_random_uuid()` | Unique user identifier (UUID v4) |
| `email` | VARCHAR(254) | NOT NULL, UNIQUE | - | User email address (RFC 5321 max length) |
| `password_hash` | VARCHAR(255) | NOT NULL | - | Bcrypt password hash (60 chars + future-proofing) |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL | `NOW()` | Account creation timestamp (UTC) |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL | `NOW()` | Last modification timestamp (UTC) |
| `is_active` | BOOLEAN | NOT NULL | `TRUE` | Account status / soft delete flag |
| `last_login` | TIMESTAMP WITH TIME ZONE | NULL | - | Last successful authentication timestamp |

### Validation Rules

**Email**:
- Must be valid email format (RFC 5322)
- Case-insensitive uniqueness (stored as-is, indexed as lowercase)
- Maximum 254 characters (RFC 5321)
- Cannot be empty or whitespace-only

**Password Hash**:
- Must be bcrypt hash format (`$2b$...`)
- Exactly 60 characters for bcrypt (up to 255 for future algorithms)
- Never store plaintext passwords
- MUST use bcrypt work factor >= 12

**Timestamps**:
- All timestamps in UTC
- `created_at` immutable after insert
- `updated_at` automatically updated on modification
- `last_login` updated on successful authentication only

**Account Status**:
- `is_active = TRUE`: Account can authenticate
- `is_active = FALSE`: Account suspended (soft delete)
- Deleted users retain data for audit trail

### Indexes

```sql
-- Unique index for case-insensitive email lookup
CREATE UNIQUE INDEX idx_users_email ON users(LOWER(email));

-- Index for recent user queries (admin dashboards)
CREATE INDEX idx_users_created_at ON users(created_at DESC);

-- Partial index for active users only (optimization)
CREATE INDEX idx_users_is_active ON users(is_active) WHERE is_active = TRUE;
```

### Check Constraints

```sql
-- Email must not be empty
ALTER TABLE users
ADD CONSTRAINT users_email_not_empty
CHECK (LENGTH(TRIM(email)) > 0);

-- Email must be valid length
ALTER TABLE users
ADD CONSTRAINT users_email_max_length
CHECK (LENGTH(email) <= 254);

-- Password hash must not be empty
ALTER TABLE users
ADD CONSTRAINT users_password_hash_not_empty
CHECK (LENGTH(password_hash) >= 60);
```

### Sample Data

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "alice@example.com",
    "password_hash": "$2b$12$KIXx6jH3r.tQVxFwZ9vVGeJ3YQ7Z8pL3vWn0qY5jK9mN2oP1qR2sS",
    "created_at": "2026-01-01T10:00:00Z",
    "updated_at": "2026-01-08T15:30:00Z",
    "is_active": true,
    "last_login": "2026-01-08T15:30:00Z"
  },
  {
    "id": "223e4567-e89b-12d3-a456-426614174001",
    "email": "bob@example.com",
    "password_hash": "$2b$12$anotherHashValueHere1234567890123456789012345678901",
    "created_at": "2026-01-02T14:20:00Z",
    "updated_at": "2026-01-07T09:15:00Z",
    "is_active": true,
    "last_login": "2026-01-07T09:15:00Z"
  },
  {
    "id": "323e4567-e89b-12d3-a456-426614174002",
    "email": "charlie@example.com",
    "password_hash": "$2b$12$yetAnotherHashValue123456789012345678901234567890",
    "created_at": "2026-01-03T08:45:00Z",
    "updated_at": "2026-01-05T12:00:00Z",
    "is_active": false,
    "last_login": "2026-01-05T11:55:00Z"
  }
]
```

---

## 3. Tasks Table

### Purpose

The `tasks` table stores all user tasks with their status, metadata, and relationships to users. This is the core domain entity of the application.

### Table Definition (SQL)

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,

    -- Foreign key constraint
    CONSTRAINT fk_tasks_user FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Check constraints
    CONSTRAINT tasks_title_not_empty
        CHECK (LENGTH(TRIM(title)) > 0),

    CONSTRAINT tasks_title_max_length
        CHECK (LENGTH(title) <= 200),

    CONSTRAINT tasks_description_max_length
        CHECK (description IS NULL OR LENGTH(description) <= 2000),

    CONSTRAINT tasks_status_valid
        CHECK (status IN ('pending', 'in_progress', 'completed'))
);
```

### Column Specifications

| Column | Type | Constraints | Default | Description |
|--------|------|-------------|---------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL | `gen_random_uuid()` | Unique task identifier (UUID v4) |
| `user_id` | UUID | FOREIGN KEY, NOT NULL | - | Owner of the task (references users.id) |
| `title` | VARCHAR(200) | NOT NULL | - | Task title (1-200 characters) |
| `description` | TEXT | NULL | - | Optional task description (max 2000 characters) |
| `status` | VARCHAR(20) | NOT NULL | `'pending'` | Task status enum |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL | `NOW()` | Task creation timestamp (UTC) |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL | `NOW()` | Last modification timestamp (UTC) |

### Status Enum

```python
class TaskStatus(str, Enum):
    PENDING = "pending"         # Task created but not started
    IN_PROGRESS = "in_progress" # Task actively being worked on
    COMPLETED = "completed"     # Task finished
```

**Status Transitions**:
- `pending` → `in_progress` (user starts task)
- `pending` → `completed` (quick completion)
- `in_progress` → `completed` (normal completion)
- `in_progress` → `pending` (user pauses/resets)
- `completed` → `pending` (user reopens task)
- `completed` → `in_progress` (rare: user continues completed task)

All transitions are valid (flexible workflow).

### Validation Rules

**Title**:
- Minimum 1 character (after trimming whitespace)
- Maximum 200 characters
- Cannot be empty string or whitespace-only
- Supports Unicode characters (emojis, non-Latin scripts)

**Description**:
- Optional (nullable)
- Maximum 2000 characters
- Supports Markdown formatting (rendered in frontend)
- Can be empty string (treated as NULL)

**Status**:
- Must be one of: `pending`, `in_progress`, `completed`
- Case-sensitive
- No custom statuses allowed (enforce via CHECK constraint)

**User ID**:
- Must reference existing user
- Cannot be NULL
- Cascade delete: When user deleted, all tasks deleted
- Cascade update: When user ID changes, task user_id updates (rare)

### Indexes

```sql
-- Primary access pattern: Get all tasks for a user
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Filter tasks by status
CREATE INDEX idx_tasks_status ON tasks(status);

-- Sort tasks by creation date (newest first)
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

-- Sort tasks by last update (recently modified first)
CREATE INDEX idx_tasks_updated_at ON tasks(updated_at DESC);

-- Composite index: User's tasks filtered by status (common query)
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);

-- Composite index: User's tasks sorted by creation (common query)
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);

-- Full-text search on task title
CREATE INDEX idx_tasks_title_search
ON tasks USING gin(to_tsvector('english', title));

-- Full-text search on task description
CREATE INDEX idx_tasks_description_search
ON tasks USING gin(to_tsvector('english', COALESCE(description, '')));
```

### Check Constraints

```sql
-- Title cannot be empty after trimming
ALTER TABLE tasks
ADD CONSTRAINT tasks_title_not_empty
CHECK (LENGTH(TRIM(title)) > 0);

-- Title maximum length
ALTER TABLE tasks
ADD CONSTRAINT tasks_title_max_length
CHECK (LENGTH(title) <= 200);

-- Description maximum length (nullable)
ALTER TABLE tasks
ADD CONSTRAINT tasks_description_max_length
CHECK (description IS NULL OR LENGTH(description) <= 2000);

-- Status must be valid enum value
ALTER TABLE tasks
ADD CONSTRAINT tasks_status_valid
CHECK (status IN ('pending', 'in_progress', 'completed'));
```

### Sample Data

```json
[
  {
    "id": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Complete project proposal",
    "description": "Write and submit Q1 project proposal with budget breakdown and timeline. Include risk assessment and resource allocation.",
    "status": "in_progress",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-08T14:30:00Z"
  },
  {
    "id": "b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e",
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Review pull requests",
    "description": null,
    "status": "pending",
    "created_at": "2026-01-08T10:15:00Z",
    "updated_at": "2026-01-08T10:15:00Z"
  },
  {
    "id": "c3d4e5f6-a7b8-4c5d-0e1f-2a3b4c5d6e7f",
    "user_id": "223e4567-e89b-12d3-a456-426614174001",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread, vegetables",
    "status": "completed",
    "created_at": "2026-01-06T08:00:00Z",
    "updated_at": "2026-01-07T18:45:00Z"
  },
  {
    "id": "d4e5f6a7-b8c9-4d5e-1f2a-3b4c5d6e7f8a",
    "user_id": "223e4567-e89b-12d3-a456-426614174001",
    "title": "Schedule dentist appointment",
    "description": "Call Dr. Smith's office for regular checkup",
    "status": "pending",
    "created_at": "2026-01-08T11:30:00Z",
    "updated_at": "2026-01-08T11:30:00Z"
  }
]
```

---

## 4. Indexes Strategy

### Index Selection Criteria

Indexes are created based on:
1. **Query Frequency**: Most common queries get indexes
2. **Query Performance**: Slow queries without indexes get priority
3. **Cardinality**: High-cardinality columns (e.g., user_id, status) are good candidates
4. **Write Cost**: Balance read performance vs write overhead

### Primary Access Patterns

#### Pattern 1: Get all tasks for a user
```sql
SELECT * FROM tasks WHERE user_id = $1 ORDER BY created_at DESC;
```
**Index**: `idx_tasks_user_created` (composite index on user_id + created_at DESC)

#### Pattern 2: Get user's tasks filtered by status
```sql
SELECT * FROM tasks WHERE user_id = $1 AND status = $2;
```
**Index**: `idx_tasks_user_status` (composite index on user_id + status)

#### Pattern 3: Search tasks by title
```sql
SELECT * FROM tasks WHERE user_id = $1 AND to_tsvector('english', title) @@ to_tsquery('english', $2);
```
**Index**: `idx_tasks_title_search` (GIN index for full-text search)

#### Pattern 4: Get recently updated tasks
```sql
SELECT * FROM tasks WHERE user_id = $1 ORDER BY updated_at DESC LIMIT 10;
```
**Index**: `idx_tasks_user_created` (can be reused) or separate `idx_tasks_user_updated`

### Index Maintenance

- **Rebuild Frequency**: Automatic (PostgreSQL handles via VACUUM)
- **Monitoring**: Track index usage via `pg_stat_user_indexes`
- **Unused Index Cleanup**: Remove indexes with `idx_scan = 0` after 30 days
- **Index Bloat**: Monitor with `pg_stat_user_tables` and `pgstattuple`

### Performance Targets

- **User task list query**: < 50ms (p95)
- **Task search query**: < 100ms (p95)
- **Task creation**: < 20ms (p95)
- **Task update**: < 20ms (p95)

---

## 5. Relationships and Constraints

### Entity Relationship Diagram (ERD)

```
┌─────────────────────┐
│      users          │
├─────────────────────┤
│ id (PK)            │
│ email (UNIQUE)     │
│ password_hash      │
│ created_at         │
│ updated_at         │
│ is_active          │
│ last_login         │
└─────────────────────┘
         │
         │ 1
         │
         │ has
         │
         │ many
         │
         ▼
┌─────────────────────┐
│      tasks          │
├─────────────────────┤
│ id (PK)            │
│ user_id (FK)       │───┐
│ title              │   │
│ description        │   │ REFERENCES users(id)
│ status             │   │ ON DELETE CASCADE
│ created_at         │   │ ON UPDATE CASCADE
│ updated_at         │◄──┘
└─────────────────────┘
```

### Foreign Key Constraints

#### FK: tasks.user_id → users.id

```sql
ALTER TABLE tasks
ADD CONSTRAINT fk_tasks_user
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE
ON UPDATE CASCADE;
```

**Behavior**:
- **ON DELETE CASCADE**: When user deleted, all their tasks automatically deleted
- **ON UPDATE CASCADE**: When user.id changes (rare), task.user_id automatically updates
- **Validation**: Cannot create task with non-existent user_id
- **Referential Integrity**: Enforced at database level

### Cascade Delete Implications

**Scenario**: User account deletion
```sql
DELETE FROM users WHERE id = '123e4567-e89b-12d3-a456-426614174000';
```

**Result**:
1. All tasks where `user_id = '123e4567...'` are automatically deleted
2. No orphaned tasks remain
3. Transaction is atomic (all or nothing)
4. Triggers fire in order: tasks triggers → users triggers

**Alternative**: Soft delete (recommended for production)
```sql
UPDATE users SET is_active = FALSE WHERE id = '123e4567-e89b-12d3-a456-426614174000';
```
- Preserves task data for audit trail
- User cannot login but data retained
- Can be reversed if needed

### Referential Integrity Rules

1. **Cannot create task without valid user**:
   ```sql
   INSERT INTO tasks (user_id, title) VALUES ('non-existent-uuid', 'Task');
   -- ERROR: violates foreign key constraint "fk_tasks_user"
   ```

2. **Cannot delete user with tasks (if no CASCADE)**:
   ```sql
   -- Without CASCADE, this would fail if user has tasks
   DELETE FROM users WHERE id = '123e4567...';
   ```

3. **Orphaned tasks are impossible**:
   - Database guarantees every task has a valid user
   - Application logic simplified (no orphan checks needed)

---

## 6. Database Triggers

### Purpose

Triggers automate timestamp updates and maintain data consistency without application-level logic.

### Trigger Function: Update Timestamp

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    -- Set updated_at to current timestamp (UTC)
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Function Details**:
- **Trigger Type**: `BEFORE UPDATE` (runs before row modification)
- **Language**: PL/pgSQL
- **Return**: Modified `NEW` row
- **Side Effects**: None (pure timestamp update)

### Trigger: Users Table

```sql
CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

**Behavior**:
- Fires on every `UPDATE` to `users` table
- Automatically sets `updated_at = NOW()`
- Application does not need to set `updated_at` manually
- Consistent timestamp across all updates

### Trigger: Tasks Table

```sql
CREATE TRIGGER update_tasks_updated_at
BEFORE UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

**Behavior**:
- Fires on every `UPDATE` to `tasks` table
- Automatically sets `updated_at = NOW()`
- Tracks last modification time for task changes
- Useful for "recently updated" queries

### Trigger Execution Order

When updating a task:
1. Application executes: `UPDATE tasks SET status = 'completed' WHERE id = $1`
2. Trigger fires: `update_tasks_updated_at`
3. Trigger function executes: `NEW.updated_at = NOW()`
4. Row updated with new status AND new timestamp
5. Transaction commits

### Testing Triggers

```sql
-- Create user
INSERT INTO users (email, password_hash)
VALUES ('test@example.com', '$2b$12$test...hash...');

-- Verify created_at and updated_at are set
SELECT created_at, updated_at FROM users WHERE email = 'test@example.com';
-- Both should be identical (just created)

-- Update user
UPDATE users SET last_login = NOW() WHERE email = 'test@example.com';

-- Verify updated_at changed
SELECT created_at, updated_at FROM users WHERE email = 'test@example.com';
-- created_at unchanged, updated_at should be newer
```

---

## 7. SQLModel Definitions

### User Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List

class User(SQLModel, table=True):
    """
    User model representing authenticated users.

    Managed by Better Auth but defined here for SQLModel integration.
    """
    __tablename__ = "users"

    # Primary Key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique user identifier"
    )

    # Authentication
    email: str = Field(
        max_length=254,
        unique=True,
        index=True,
        description="User email address (unique, case-insensitive)"
    )
    password_hash: str = Field(
        max_length=255,
        description="Bcrypt password hash (never store plaintext)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp (UTC)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last modification timestamp (UTC)"
    )

    # Account Status
    is_active: bool = Field(
        default=True,
        description="Account active status (False = soft deleted)"
    )
    last_login: Optional[datetime] = Field(
        default=None,
        description="Last successful authentication timestamp"
    )

    # Relationships
    tasks: List["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "alice@example.com",
                "password_hash": "$2b$12$KIXx6jH3r...",
                "created_at": "2026-01-01T10:00:00Z",
                "updated_at": "2026-01-08T15:30:00Z",
                "is_active": True,
                "last_login": "2026-01-08T15:30:00Z"
            }
        }
```

### Task Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(SQLModel, table=True):
    """
    Task model representing user to-do items.

    Each task belongs to exactly one user (1:N relationship).
    """
    __tablename__ = "tasks"

    # Primary Key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique task identifier"
    )

    # Foreign Key
    user_id: UUID = Field(
        foreign_key="users.id",
        description="Task owner (references users.id)"
    )

    # Task Content
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional task description (max 2000 characters)"
    )

    # Task Status
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Task status (pending | in_progress | completed)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp (UTC)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last modification timestamp (UTC)"
    )

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tasks")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "id": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Complete project proposal",
                "description": "Write and submit Q1 project proposal",
                "status": "in_progress",
                "created_at": "2026-01-05T09:00:00Z",
                "updated_at": "2026-01-08T14:30:00Z"
            }
        }
```

### Pydantic Schemas (API Layer)

```python
from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from uuid import UUID
from typing import Optional

# ============================================================================
# User Schemas
# ============================================================================

class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr = Field(..., description="User email address")

class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password (8-128 characters)"
    )

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets security requirements."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserResponse(UserBase):
    """Schema for user responses (public data only)."""
    id: UUID
    created_at: datetime
    is_active: bool
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

# ============================================================================
# Task Schemas
# ============================================================================

class TaskBase(BaseModel):
    """Base task schema with common fields."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)

class TaskCreate(TaskBase):
    """Schema for task creation."""
    pass

class TaskUpdate(BaseModel):
    """Schema for task updates (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None

class TaskResponse(TaskBase):
    """Schema for task responses."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

---

## 8. Migration Scripts

### Alembic Migration: Initial Schema

**File**: `alembic/versions/001_initial_schema.py`

```python
"""Initial schema with users and tasks tables

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-01-08 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    """
    Create initial schema with users and tasks tables.

    Includes:
    - users table with authentication fields
    - tasks table with user relationship
    - All indexes for performance
    - Triggers for automatic timestamp updates
    - Check constraints for data validation
    """

    # ========================================================================
    # Create users table
    # ========================================================================
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(254), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('is_active', sa.Boolean(), nullable=False,
                  server_default=sa.text('TRUE')),
        sa.Column('last_login', sa.TIMESTAMP(timezone=True), nullable=True),

        # Check constraints
        sa.CheckConstraint("LENGTH(TRIM(email)) > 0", name='users_email_not_empty'),
        sa.CheckConstraint("LENGTH(email) <= 254", name='users_email_max_length'),
        sa.CheckConstraint("LENGTH(password_hash) >= 60", name='users_password_hash_not_empty')
    )

    # ========================================================================
    # Create tasks table
    # ========================================================================
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False,
                  server_default=sa.text("'pending'")),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),

        # Check constraints
        sa.CheckConstraint("LENGTH(TRIM(title)) > 0", name='tasks_title_not_empty'),
        sa.CheckConstraint("LENGTH(title) <= 200", name='tasks_title_max_length'),
        sa.CheckConstraint("description IS NULL OR LENGTH(description) <= 2000",
                          name='tasks_description_max_length'),
        sa.CheckConstraint("status IN ('pending', 'in_progress', 'completed')",
                          name='tasks_status_valid'),

        # Foreign key
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            name='fk_tasks_user',
            ondelete='CASCADE',
            onupdate='CASCADE'
        )
    )

    # ========================================================================
    # Create indexes for users table
    # ========================================================================
    op.create_index(
        'idx_users_email',
        'users',
        [sa.text('LOWER(email)')],
        unique=True
    )
    op.create_index(
        'idx_users_created_at',
        'users',
        ['created_at'],
        postgresql_using='btree',
        postgresql_ops={'created_at': 'DESC'}
    )
    op.create_index(
        'idx_users_is_active',
        'users',
        ['is_active'],
        postgresql_where=sa.text('is_active = TRUE')
    )

    # ========================================================================
    # Create indexes for tasks table
    # ========================================================================
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_status', 'tasks', ['status'])
    op.create_index(
        'idx_tasks_created_at',
        'tasks',
        ['created_at'],
        postgresql_ops={'created_at': 'DESC'}
    )
    op.create_index(
        'idx_tasks_updated_at',
        'tasks',
        ['updated_at'],
        postgresql_ops={'updated_at': 'DESC'}
    )
    op.create_index('idx_tasks_user_status', 'tasks', ['user_id', 'status'])
    op.create_index(
        'idx_tasks_user_created',
        'tasks',
        ['user_id', 'created_at'],
        postgresql_ops={'created_at': 'DESC'}
    )

    # Full-text search indexes
    op.create_index(
        'idx_tasks_title_search',
        'tasks',
        [sa.text("to_tsvector('english', title)")],
        postgresql_using='gin'
    )
    op.create_index(
        'idx_tasks_description_search',
        'tasks',
        [sa.text("to_tsvector('english', COALESCE(description, ''))")],
        postgresql_using='gin'
    )

    # ========================================================================
    # Create trigger function for updated_at
    # ========================================================================
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # ========================================================================
    # Create triggers
    # ========================================================================
    op.execute("""
        CREATE TRIGGER update_users_updated_at
        BEFORE UPDATE ON users
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)

    op.execute("""
        CREATE TRIGGER update_tasks_updated_at
        BEFORE UPDATE ON tasks
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)

def downgrade() -> None:
    """
    Rollback initial schema.

    Drops all tables, indexes, triggers, and functions created in upgrade().
    """

    # Drop triggers
    op.execute('DROP TRIGGER IF EXISTS update_tasks_updated_at ON tasks;')
    op.execute('DROP TRIGGER IF EXISTS update_users_updated_at ON users;')

    # Drop trigger function
    op.execute('DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;')

    # Drop tables (cascade will drop foreign keys and indexes)
    op.drop_table('tasks')
    op.drop_table('users')
```

### Manual SQL Migration (Alternative)

**File**: `database/migrations/001_initial_schema.sql`

```sql
-- ============================================================================
-- Phase II Database Schema Migration
-- Creates users and tasks tables with all constraints, indexes, and triggers
-- ============================================================================
-- Version: 1.0
-- Date: 2026-01-08
-- Author: Evolution of Todo Team
-- ============================================================================

BEGIN;

-- ============================================================================
-- 1. Create users table
-- ============================================================================

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(254) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE
);

-- ============================================================================
-- 2. Create tasks table
-- ============================================================================

CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- ============================================================================
-- 3. Add check constraints
-- ============================================================================

-- Users constraints
ALTER TABLE users
ADD CONSTRAINT users_email_not_empty
CHECK (LENGTH(TRIM(email)) > 0);

ALTER TABLE users
ADD CONSTRAINT users_email_max_length
CHECK (LENGTH(email) <= 254);

ALTER TABLE users
ADD CONSTRAINT users_password_hash_not_empty
CHECK (LENGTH(password_hash) >= 60);

-- Tasks constraints
ALTER TABLE tasks
ADD CONSTRAINT tasks_title_not_empty
CHECK (LENGTH(TRIM(title)) > 0);

ALTER TABLE tasks
ADD CONSTRAINT tasks_title_max_length
CHECK (LENGTH(title) <= 200);

ALTER TABLE tasks
ADD CONSTRAINT tasks_description_max_length
CHECK (description IS NULL OR LENGTH(description) <= 2000);

ALTER TABLE tasks
ADD CONSTRAINT tasks_status_valid
CHECK (status IN ('pending', 'in_progress', 'completed'));

-- ============================================================================
-- 4. Add foreign key constraints
-- ============================================================================

ALTER TABLE tasks
ADD CONSTRAINT fk_tasks_user
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- ============================================================================
-- 5. Create indexes for users table
-- ============================================================================

CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email
ON users(LOWER(email));

CREATE INDEX IF NOT EXISTS idx_users_created_at
ON users(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_users_is_active
ON users(is_active)
WHERE is_active = TRUE;

-- ============================================================================
-- 6. Create indexes for tasks table
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_tasks_user_id
ON tasks(user_id);

CREATE INDEX IF NOT EXISTS idx_tasks_status
ON tasks(status);

CREATE INDEX IF NOT EXISTS idx_tasks_created_at
ON tasks(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_tasks_updated_at
ON tasks(updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_tasks_user_status
ON tasks(user_id, status);

CREATE INDEX IF NOT EXISTS idx_tasks_user_created
ON tasks(user_id, created_at DESC);

-- Full-text search indexes
CREATE INDEX IF NOT EXISTS idx_tasks_title_search
ON tasks USING gin(to_tsvector('english', title));

CREATE INDEX IF NOT EXISTS idx_tasks_description_search
ON tasks USING gin(to_tsvector('english', COALESCE(description, '')));

-- ============================================================================
-- 7. Create trigger function for updated_at
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 8. Create triggers
-- ============================================================================

DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_tasks_updated_at ON tasks;
CREATE TRIGGER update_tasks_updated_at
BEFORE UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 9. Verify schema
-- ============================================================================

-- Display table information
SELECT
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
FROM information_schema.tables t
WHERE table_schema = 'public'
AND table_name IN ('users', 'tasks')
ORDER BY table_name;

COMMIT;

-- ============================================================================
-- Migration complete
-- ============================================================================
```

### Running Migrations

**Using Alembic**:
```bash
# Navigate to backend
cd apps/backend

# Generate migration (auto-detect schema changes)
poetry run alembic revision --autogenerate -m "Initial schema"

# Review generated migration
cat alembic/versions/001_initial_schema.py

# Apply migration
poetry run alembic upgrade head

# Verify current version
poetry run alembic current

# Rollback migration
poetry run alembic downgrade -1
```

**Using Manual SQL**:
```bash
# Connect to database
psql postgresql://localhost:5432/evolution_todo_dev

# Run migration
\i database/migrations/001_initial_schema.sql

# Verify tables created
\dt

# Verify indexes
\di

# Exit
\q
```

---

## 9. Performance Considerations

### Query Optimization

#### 1. Index Usage Verification

```sql
-- Check if indexes are being used
EXPLAIN ANALYZE
SELECT * FROM tasks
WHERE user_id = '123e4567-e89b-12d3-a456-426614174000'
ORDER BY created_at DESC;

-- Expected: Index Scan using idx_tasks_user_created
-- NOT: Seq Scan on tasks
```

#### 2. Composite Index Benefits

**Without composite index**:
```sql
SELECT * FROM tasks
WHERE user_id = $1 AND status = 'pending';

-- Uses: idx_tasks_user_id (partial scan) + Filter on status
-- Cost: Higher (must filter results)
```

**With composite index** (`idx_tasks_user_status`):
```sql
-- Uses: idx_tasks_user_status (direct lookup)
-- Cost: Lower (precise index match)
```

#### 3. Full-Text Search Performance

```sql
-- Full-text search on title
SELECT * FROM tasks
WHERE user_id = $1
AND to_tsvector('english', title) @@ to_tsquery('english', 'project & proposal');

-- Uses: idx_tasks_title_search (GIN index)
-- Performance: O(log n) instead of O(n)
```

### Connection Pooling

**SQLAlchemy Configuration**:
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Database URL (from environment)
DATABASE_URL = "postgresql+asyncpg://localhost:5432/evolution_todo_dev"

# Create async engine with connection pool
engine = create_async_engine(
    DATABASE_URL,
    echo=False,                    # Disable SQL logging in production
    pool_size=20,                  # Max connections in pool
    max_overflow=10,               # Additional connections when pool full
    pool_timeout=30,               # Timeout waiting for connection (seconds)
    pool_recycle=3600,             # Recycle connections after 1 hour
    pool_pre_ping=True,            # Verify connections before use
    connect_args={
        "server_settings": {
            "application_name": "evolution-todo-api",
            "timezone": "UTC"
        }
    }
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

### Database-Level Optimizations

#### 1. Vacuum and Analyze

```sql
-- Manual vacuum (reclaim space and update statistics)
VACUUM ANALYZE users;
VACUUM ANALYZE tasks;

-- Auto-vacuum configuration (postgresql.conf)
autovacuum = on
autovacuum_vacuum_scale_factor = 0.1
autovacuum_analyze_scale_factor = 0.05
```

#### 2. Index Maintenance

```sql
-- Reindex (rebuild indexes to remove bloat)
REINDEX TABLE users;
REINDEX TABLE tasks;

-- Check index bloat
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
    idx_scan AS scans,
    idx_tup_read AS tuples_read,
    idx_tup_fetch AS tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;
```

#### 3. Query Performance Monitoring

```sql
-- Enable pg_stat_statements extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find slow queries
SELECT
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time
FROM pg_stat_statements
WHERE query LIKE '%tasks%'
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Neon-Specific Optimizations

**Neon Autoscaling**:
- Neon automatically scales compute based on demand
- Connection pooling is critical (limited connections on free tier)
- Use Neon's connection pooler: `pooler.neon.tech:5432`

**Connection String**:
```
# Direct connection (limited)
postgresql://user:pass@ep-name.region.aws.neon.tech/db

# Pooled connection (recommended)
postgresql://user:pass@ep-name.pooler.region.aws.neon.tech/db
```

**Neon-Specific Settings**:
```python
# Use Neon's connection pooler
DATABASE_URL = os.getenv("DATABASE_URL").replace(
    ".neon.tech",
    ".pooler.neon.tech"
)

# Reduce pool size for Neon (they handle pooling)
engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,        # Lower for Neon pooler
    max_overflow=5,     # Lower for Neon pooler
    pool_pre_ping=True  # Essential for serverless
)
```

### Performance Targets

| Operation | Target (p95) | Index Used |
|-----------|--------------|------------|
| Get user's tasks | < 50ms | `idx_tasks_user_created` |
| Get tasks by status | < 50ms | `idx_tasks_user_status` |
| Search task title | < 100ms | `idx_tasks_title_search` |
| Create task | < 20ms | N/A (insert) |
| Update task | < 20ms | Primary key lookup |
| Delete task | < 20ms | Primary key lookup |
| User authentication | < 100ms | `idx_users_email` |

---

## 10. Data Validation Strategy

### Validation Layers

Evolution of Todo implements **defense in depth** with three validation layers:

```
┌─────────────────────────────────────┐
│ 1. Frontend Validation              │
│    - Immediate user feedback        │
│    - Client-side type checking      │
│    - Basic format validation        │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ 2. Backend Validation (Pydantic)    │
│    - Type coercion and validation   │
│    - Business logic rules           │
│    - Cross-field validation         │
│    - Custom validators              │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ 3. Database Validation (Postgres)   │
│    - CHECK constraints              │
│    - Foreign key integrity          │
│    - Unique constraints             │
│    - NOT NULL enforcement           │
└─────────────────────────────────────┘
```

### Layer 1: Frontend Validation (React/Next.js)

**Purpose**: Provide immediate user feedback and reduce server load

```typescript
// Task form validation (Zod schema)
import { z } from 'zod';

const taskFormSchema = z.object({
  title: z.string()
    .min(1, 'Title is required')
    .max(200, 'Title must be 200 characters or less')
    .trim(),

  description: z.string()
    .max(2000, 'Description must be 2000 characters or less')
    .optional()
    .nullable(),

  status: z.enum(['pending', 'in_progress', 'completed'])
    .default('pending')
});

type TaskFormData = z.infer<typeof taskFormSchema>;
```

**When to use**:
- Form submission validation
- Real-time input validation
- User experience improvements

**Limitations**:
- Can be bypassed by malicious users
- Not sufficient for security
- Must be duplicated on backend

### Layer 2: Backend Validation (Pydantic)

**Purpose**: Enforce business rules and type safety at API boundary

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class TaskCreate(BaseModel):
    """Task creation schema with validation."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title"
    )

    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Task description"
    )

    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Task status"
    )

    @field_validator('title')
    @classmethod
    def title_not_empty_after_trim(cls, v: str) -> str:
        """Ensure title is not empty after trimming whitespace."""
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()

    @field_validator('description')
    @classmethod
    def description_normalize(cls, v: Optional[str]) -> Optional[str]:
        """Normalize empty string to None."""
        if v is not None and not v.strip():
            return None
        return v.strip() if v else None
```

**When to use**:
- API request/response validation
- Type coercion (e.g., string to UUID)
- Business logic enforcement
- Custom validation rules

**Benefits**:
- Automatic OpenAPI documentation
- Type safety with Python type hints
- Detailed error messages
- Runs before database interaction

### Layer 3: Database Validation (PostgreSQL)

**Purpose**: Final guarantee of data integrity at storage layer

```sql
-- CHECK constraints (defined in schema)
ALTER TABLE tasks
ADD CONSTRAINT tasks_title_not_empty
CHECK (LENGTH(TRIM(title)) > 0);

ALTER TABLE tasks
ADD CONSTRAINT tasks_title_max_length
CHECK (LENGTH(title) <= 200);

ALTER TABLE tasks
ADD CONSTRAINT tasks_description_max_length
CHECK (description IS NULL OR LENGTH(description) <= 2000);

ALTER TABLE tasks
ADD CONSTRAINT tasks_status_valid
CHECK (status IN ('pending', 'in_progress', 'completed'));
```

**When to use**:
- Critical data integrity rules
- Constraints that must NEVER be violated
- Protection against direct database access
- Multi-application data consistency

**Benefits**:
- Cannot be bypassed (even by SQL)
- Enforced for all clients (API, admin tools, etc.)
- Atomic with transaction
- Database-level guarantee

### Validation Error Handling

**Frontend Error Display**:
```typescript
// React Hook Form error handling
<input
  {...register('title')}
  className={errors.title ? 'border-red-500' : 'border-gray-300'}
/>
{errors.title && (
  <p className="text-red-500 text-sm mt-1">
    {errors.title.message}
  </p>
)}
```

**Backend Error Response**:
```python
from fastapi import HTTPException, status

# Pydantic validation error (automatic)
# Returns 422 Unprocessable Entity with details

# Database constraint violation
try:
    db.add(task)
    await db.commit()
except IntegrityError as e:
    if 'tasks_title_not_empty' in str(e):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty"
        )
    raise
```

**Error Response Format**:
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Title cannot be empty or whitespace only",
      "type": "value_error"
    }
  ]
}
```

### Validation Best Practices

1. **Validate Early**: Frontend validation for UX, backend for security
2. **Fail Fast**: Return validation errors immediately (don't process invalid data)
3. **Specific Messages**: Clear error messages (e.g., "Title must be 1-200 characters")
4. **Consistent Rules**: Same validation logic across all layers
5. **Trust Database**: Database constraints are the source of truth
6. **Test Boundaries**: Test min/max values, empty strings, null values
7. **Document Rules**: Validation rules in spec (this document)

---

## 11. Security Considerations

### Password Security

**Hashing Algorithm**: Bcrypt with work factor 12

```python
from passlib.context import CryptContext

# Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Work factor (2^12 iterations)
)

# Hash password
password_hash = pwd_context.hash("user_password")

# Verify password
is_valid = pwd_context.verify("user_password", password_hash)
```

**Password Requirements** (enforced by Pydantic):
- Minimum 8 characters
- Maximum 128 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 digit
- At least 1 special character (optional but recommended)

**Storage Rules**:
- NEVER store plaintext passwords
- NEVER log passwords (even hashed)
- NEVER transmit passwords in GET requests
- NEVER include passwords in API responses

### SQL Injection Prevention

**Parameterized Queries** (SQLAlchemy/SQLModel):

```python
# ✅ SAFE: Parameterized query
user = await session.exec(
    select(User).where(User.email == email)
).first()

# ❌ UNSAFE: String concatenation (DO NOT USE)
query = f"SELECT * FROM users WHERE email = '{email}'"
```

**ORM Benefits**:
- Automatic parameter binding
- Type safety
- SQL injection protection
- Query validation

### Authentication Token Security

**JWT Configuration**:
```python
from datetime import datetime, timedelta
import jwt

# Token settings
SECRET_KEY = os.getenv("API_SECRET_KEY")  # 32+ character random string
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create token
def create_access_token(user_id: UUID) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

**Token Storage**:
- Frontend: HTTP-only cookies (preferred) or localStorage (less secure)
- Never log tokens
- Rotate tokens on password change
- Invalidate tokens on logout (use token blacklist or short expiry)

### Data Access Control

**Row-Level Security** (application layer):

```python
# Users can only access their own tasks
@router.get("/api/v1/tasks")
async def get_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get tasks for authenticated user only."""
    tasks = await db.exec(
        select(Task).where(Task.user_id == current_user.id)
    )
    return tasks.all()
```

**Foreign Key Protection**:
- Database enforces user_id exists (FK constraint)
- Application enforces user_id matches authenticated user
- Cannot create tasks for other users
- Cannot view/modify other users' tasks

### HTTPS/TLS

**Production Requirements**:
- All connections over HTTPS (TLS 1.2+)
- Redirect HTTP to HTTPS
- HSTS headers enabled
- Secure cookies (Secure flag)

**Vercel/Railway Configuration**:
```python
# FastAPI HTTPS redirect
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
```

### Rate Limiting

**Protection Against**:
- Brute force attacks
- DDoS attacks
- API abuse

**Implementation** (see `specs/phase-2-todo-web/api/rest-endpoints.md`):
- 100 requests per minute per user
- 429 Too Many Requests response
- Exponential backoff recommended

### Environment Variables

**Sensitive Data**:
```bash
# .env (NEVER commit to git)
DATABASE_URL=postgresql://...
API_SECRET_KEY=your-32-character-secret-key-here
CORS_ORIGINS=["https://your-app.vercel.app"]
```

**Security Rules**:
- Never hardcode secrets
- Use `.env.example` for documentation
- Add `.env` to `.gitignore`
- Rotate secrets regularly
- Use different secrets per environment

---

## 12. Sample Data

### Development Seed Data

**File**: `database/seeds/001_sample_data.sql`

```sql
-- ============================================================================
-- Sample data for development and testing
-- DO NOT run in production
-- ============================================================================

BEGIN;

-- ============================================================================
-- Seed users (3 test users)
-- ============================================================================

INSERT INTO users (id, email, password_hash, created_at, updated_at, is_active, last_login) VALUES
(
    '123e4567-e89b-12d3-a456-426614174000',
    'alice@example.com',
    '$2b$12$KIXx6jH3r.tQVxFwZ9vVGeJ3YQ7Z8pL3vWn0qY5jK9mN2oP1qR2sS',  -- password: "Password123"
    '2026-01-01 10:00:00+00',
    '2026-01-08 15:30:00+00',
    TRUE,
    '2026-01-08 15:30:00+00'
),
(
    '223e4567-e89b-12d3-a456-426614174001',
    'bob@example.com',
    '$2b$12$L9wE5jI4s.uRWyGxA0wWFuK4ZR8aQm4oXwO1rZ6lN0pO2qS3rT4uU',  -- password: "Password456"
    '2026-01-02 14:20:00+00',
    '2026-01-07 09:15:00+00',
    TRUE,
    '2026-01-07 09:15:00+00'
),
(
    '323e4567-e89b-12d3-a456-426614174002',
    'charlie@example.com',
    '$2b$12$M0xF6kJ5t.vSXzHyB1xXGvL5aS9bRn5pYxP2sA7mO1qP3rT4uU5vV',  -- password: "Password789"
    '2026-01-03 08:45:00+00',
    '2026-01-05 12:00:00+00',
    FALSE,  -- Inactive account
    '2026-01-05 11:55:00+00'
);

-- ============================================================================
-- Seed tasks (10 sample tasks)
-- ============================================================================

INSERT INTO tasks (id, user_id, title, description, status, created_at, updated_at) VALUES
-- Alice's tasks (5 tasks)
(
    'a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d',
    '123e4567-e89b-12d3-a456-426614174000',
    'Complete project proposal',
    'Write and submit Q1 project proposal with budget breakdown, timeline, risk assessment, and resource allocation.',
    'in_progress',
    '2026-01-05 09:00:00+00',
    '2026-01-08 14:30:00+00'
),
(
    'b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e',
    '123e4567-e89b-12d3-a456-426614174000',
    'Review pull requests',
    NULL,
    'pending',
    '2026-01-08 10:15:00+00',
    '2026-01-08 10:15:00+00'
),
(
    'c3d4e5f6-a7b8-4c5d-0e1f-2a3b4c5d6e7f',
    '123e4567-e89b-12d3-a456-426614174000',
    'Update documentation',
    'Add API examples and troubleshooting guide to README',
    'completed',
    '2026-01-04 11:00:00+00',
    '2026-01-06 16:20:00+00'
),
(
    'd4e5f6a7-b8c9-4d5e-1f2a-3b4c5d6e7f8a',
    '123e4567-e89b-12d3-a456-426614174000',
    'Fix bug in authentication flow',
    'Users are getting logged out unexpectedly after 5 minutes instead of 30 minutes',
    'in_progress',
    '2026-01-07 14:00:00+00',
    '2026-01-08 09:30:00+00'
),
(
    'e5f6a7b8-c9d0-4e5f-2a3b-4c5d6e7f8a9b',
    '123e4567-e89b-12d3-a456-426614174000',
    'Prepare presentation slides',
    'Create slides for weekly team meeting covering sprint progress and blockers',
    'pending',
    '2026-01-08 08:00:00+00',
    '2026-01-08 08:00:00+00'
),

-- Bob's tasks (3 tasks)
(
    'f6a7b8c9-d0e1-4f5a-3b4c-5d6e7f8a9b0c',
    '223e4567-e89b-12d3-a456-426614174001',
    'Buy groceries',
    'Milk, eggs, bread, vegetables, coffee',
    'completed',
    '2026-01-06 08:00:00+00',
    '2026-01-07 18:45:00+00'
),
(
    'a7b8c9d0-e1f2-4a5b-4c5d-6e7f8a9b0c1d',
    '223e4567-e89b-12d3-a456-426614174001',
    'Schedule dentist appointment',
    'Call Dr. Smith office for regular checkup',
    'pending',
    '2026-01-08 11:30:00+00',
    '2026-01-08 11:30:00+00'
),
(
    'b8c9d0e1-f2a3-4b5c-5d6e-7f8a9b0c1d2e',
    '223e4567-e89b-12d3-a456-426614174001',
    'Renew car insurance',
    'Insurance expires on Jan 31. Compare quotes from 3 providers.',
    'in_progress',
    '2026-01-05 13:00:00+00',
    '2026-01-08 10:00:00+00'
),

-- Charlie's tasks (2 tasks - user is inactive but data retained)
(
    'c9d0e1f2-a3b4-4c5d-6e7f-8a9b0c1d2e3f',
    '323e4567-e89b-12d3-a456-426614174002',
    'Update resume',
    'Add recent project experience and new certifications',
    'pending',
    '2026-01-04 15:00:00+00',
    '2026-01-04 15:00:00+00'
),
(
    'd0e1f2a3-b4c5-4d6e-7f8a-9b0c1d2e3f4a',
    '323e4567-e89b-12d3-a456-426614174002',
    'Read book: Clean Code',
    NULL,
    'completed',
    '2026-01-01 09:00:00+00',
    '2026-01-05 20:00:00+00'
);

-- ============================================================================
-- Verify seed data
-- ============================================================================

SELECT 'Users created:' as info, COUNT(*) as count FROM users;
SELECT 'Tasks created:' as info, COUNT(*) as count FROM tasks;
SELECT 'Active users:' as info, COUNT(*) as count FROM users WHERE is_active = TRUE;
SELECT 'Pending tasks:' as info, COUNT(*) as count FROM tasks WHERE status = 'pending';
SELECT 'In progress tasks:' as info, COUNT(*) as count FROM tasks WHERE status = 'in_progress';
SELECT 'Completed tasks:' as info, COUNT(*) as count FROM tasks WHERE status = 'completed';

COMMIT;
```

### Running Seed Script

```bash
# Connect to database
psql $DATABASE_URL

# Run seed script
\i database/seeds/001_sample_data.sql

# Verify data
SELECT u.email, COUNT(t.id) as task_count
FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.email;
```

---

## 13. Cross-References

### Related Specifications

**Feature Specifications**:
- `specs/phase-2-todo-web/features/authentication.md` - User authentication and JWT tokens (uses `users` table)
- `specs/phase-2-todo-web/features/task-management.md` - Task CRUD operations (uses `tasks` table)

**API Specifications**:
- `specs/phase-2-todo-web/api/rest-endpoints.md` - REST API endpoints that interact with this schema
  - Section 3: Task Endpoints (GET, POST, PUT, DELETE tasks)
  - Section 2: Authentication (user login, token generation)

**UI Specifications**:
- `specs/phase-2-todo-web/ui/task-list-page.md` - Task list UI (displays data from `tasks` table)
- `specs/phase-2-todo-web/ui/task-form.md` - Task creation/editing form (validates against schema constraints)

### Agent References

**Database Agent**:
- `.claude/agents/database-architect.md` - Responsible for implementing this schema, creating migrations, and optimizing queries

**Backend Agent**:
- `.claude/agents/fastapi-backend-developer.md` - Implements SQLModel models and database operations based on this schema

**Security Agent**:
- `.claude/agents/auth-security-guardian.md` - Enforces password hashing, JWT security, and data access controls defined here

### Configuration Files

**Backend Configuration**:
- `apps/backend/app/core/database.py` - Database connection and session management
- `apps/backend/app/models/` - SQLModel model definitions (implements this schema)
- `apps/backend/alembic/versions/` - Migration scripts (generated from this schema)
- `apps/backend/alembic.ini` - Alembic configuration

**Environment Variables**:
- `apps/backend/.env.example` - Database URL and connection settings template
- `apps/backend/.env` - Actual database credentials (not committed)

### External Resources

**Documentation**:
- PostgreSQL 15 Documentation: https://www.postgresql.org/docs/15/
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- Alembic Documentation: https://alembic.sqlalchemy.org/
- Neon Documentation: https://neon.tech/docs/

**Tools**:
- pgAdmin: Database administration GUI
- psql: PostgreSQL command-line client
- Postico: macOS database client
- TablePlus: Cross-platform database client

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-08 | Spec Architect | Initial schema specification |

---

**Status**: Draft
**Review Required**: Yes
**Approved By**: Pending
**Implementation Status**: Not Started

---

**Next Steps**:
1. Review and approve this specification
2. Create Alembic migration from SQLModel definitions
3. Test migration on development database
4. Create seed data for development
5. Deploy to Neon production database
6. Update API documentation with schema references
