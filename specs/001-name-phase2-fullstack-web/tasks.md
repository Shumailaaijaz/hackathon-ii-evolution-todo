# Implementation Tasks: Phase II - Full-Stack Todo Application

**Feature Branch**: `001-name-phase2-fullstack-web`
**Created**: 2026-01-08
**Status**: Ready for Implementation
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Task Overview

**Total Tasks**: 50
**Estimated Duration**: ASAP (Aggressive implementation schedule)
**Implementation Approach**: TDD (Red-Green-Refactor cycle)
**Priority Distribution**: 22 Critical, 18 High, 7 Medium, 3 Low

## Task Tracking Legend

```
[ ] Not Started
[>] In Progress
[x] Completed
[!] Blocked
[~] Skipped/Deferred
```

---

## PHASE 1: PROJECT SETUP & SPECIFICATIONS (4 Tasks)

### TASK-001: Initialize Monorepo Structure
**Priority**: Critical (P1) | **Time**: 30 min | **Dependencies**: None | **Status**: [x]

**Description:**
Create the monorepo folder structure with apps/ directory containing separate frontend and backend applications.

**Acceptance Criteria:**
- [ ] Root directory initialized with Git
- [ ] apps/frontend/ directory created
- [ ] apps/backend/ directory created
- [ ] .gitignore configured for Node.js, Python, and IDE files
- [ ] package.json created for workspace configuration
- [ ] README.md created with project overview

**Files to Create:**
- `.gitignore`
- `package.json` (workspace root)
- `README.md`
- `apps/frontend/.gitkeep`
- `apps/backend/.gitkeep`

**Claude Code Prompt:**
```
Create monorepo structure for Phase II Todo Application:

1. Create .gitignore with:
   - Node.js: node_modules/, .next/, dist/, build/
   - Python: venv/, __pycache__/, *.pyc, .pytest_cache/, *.egg-info/
   - Environment: .env, .env.local, .env.*.local
   - IDE: .vscode/, .idea/, *.swp, .DS_Store

2. Create package.json:
{
  "name": "todo-fullstack-monorepo",
  "version": "2.0.0",
  "private": true,
  "workspaces": ["apps/frontend", "apps/backend"],
  "scripts": {
    "dev:frontend": "cd apps/frontend && npm run dev",
    "dev:backend": "cd apps/backend && uvicorn app.main:app --reload",
    "test": "npm run test:frontend && npm run test:backend",
    "test:frontend": "cd apps/frontend && npm test",
    "test:backend": "cd apps/backend && pytest"
  }
}

3. Create README.md with project overview and quick start
```

**Verification:**
```bash
ls -la
cat package.json
cat .gitignore
```

---

### TASK-002: Create Environment Variable Templates
**Priority**: Critical (P1) | **Time**: 15 min | **Dependencies**: TASK-001 | **Status**: [x]

**Description:**
Create .env.example files for frontend and backend with all required environment variables documented.

**Acceptance Criteria:**
- [ ] .env.example created in project root
- [ ] apps/frontend/.env.example created
- [ ] apps/backend/.env.example created
- [ ] All variables documented with comments
- [ ] BETTER_AUTH_SECRET noted as shared between frontend/backend

**Files to Create:**
- `.env.example`
- `apps/frontend/.env.example`
- `apps/backend/.env.example`

**Reference Specs:**
- @spec.md (Environment Configuration Reference)

**Claude Code Prompt:**
```
@spec.md Create environment templates:

Root .env.example:
# BETTER_AUTH_SECRET must be identical in frontend and backend
BETTER_AUTH_SECRET=your-secret-min-32-chars-change-in-production

Frontend apps/frontend/.env.example:
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-min-32-chars
NODE_ENV=development

Backend apps/backend/.env.example:
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=your-secret-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
DEBUG=True
```

---

### TASK-003: Setup Git and Initial Commit
**Priority**: High (P1) | **Time**: 10 min | **Dependencies**: TASK-002 | **Status**: [x]

**Description:**
Verify Git repository, confirm branch, and create initial commit with monorepo structure.

**Acceptance Criteria:**
- [ ] On branch 001-name-phase2-fullstack-web
- [ ] All structure files staged
- [ ] Initial commit created
- [ ] .env files NOT committed

**Claude Code Prompt:**
```
git status
git add .gitignore package.json README.md .env.example apps/
git commit -m "chore: initialize Phase II monorepo structure

- Create apps/frontend and apps/backend directories
- Configure workspace with npm workspaces
- Add environment variable templates
- Setup .gitignore for Node.js and Python

Part of: Phase II Full-Stack Todo Application
Tasks: TASK-001, TASK-002, TASK-003"
```

---

### TASK-004: Document Project Structure in README
**Priority**: Medium (P1) | **Time**: 20 min | **Dependencies**: TASK-003 | **Status**: [x]

**Description:**
Update README.md with complete technology stack, project structure tree, setup instructions, and development commands.

**Acceptance Criteria:**
- [ ] Technology stack documented
- [ ] Project structure tree included
- [ ] Prerequisites listed
- [ ] Setup instructions clear and tested
- [ ] Development commands documented

**Files to Modify:**
- `README.md`

**Reference Specs:**
- @plan.md (Project Structure section)

---

## PHASE 2: DATABASE SETUP & MODELS (5 Tasks)

### TASK-005: Initialize Backend Python Project
**Priority**: Critical (P1) | **Time**: 20 min | **Dependencies**: TASK-004 | **Status**: [x]

**Description:**
Initialize Python project structure with virtual environment, requirements.txt, and directory structure.

**Acceptance Criteria:**
- [ ] apps/backend/app/ directory with __init__.py
- [ ] Virtual environment created (venv/)
- [ ] requirements.txt with all dependencies
- [ ] pyproject.toml created
- [ ] All subdirectories created (models/, services/, api/, core/, schemas/)

**Files to Create:**
- `apps/backend/requirements.txt`
- `apps/backend/pyproject.toml`
- `apps/backend/app/__init__.py`
- `apps/backend/app/models/__init__.py`
- `apps/backend/app/services/__init__.py`
- `apps/backend/app/api/__init__.py`
- `apps/backend/app/core/__init__.py`
- `apps/backend/app/schemas/__init__.py`

**Claude Code Prompt:**
```
Create apps/backend/requirements.txt:
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
pyjwt==2.8.0
python-jose[cryptography]==3.3.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
bcrypt==4.1.2
alembic==1.13.1
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.26.0
python-multipart==0.0.6

Create pyproject.toml with project metadata and pytest configuration
Create directory structure with __init__.py files
```

**Verification:**
```bash
cd apps/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -c "import fastapi; import sqlmodel; print('OK')"
```

---

### TASK-006: Create SQLModel User and Task Models
**Priority**: Critical (P1) | **Time**: 45 min | **Dependencies**: TASK-005 | **Status**: [x]

**Description:**
Create SQLModel data models for User and Task entities with relationships, constraints, and validation.

**Acceptance Criteria:**
- [ ] apps/backend/app/models/user.py with User model
- [ ] apps/backend/app/models/task.py with Task model
- [ ] Foreign key relationship (task.user_id → user.id)
- [ ] Indexes on user_id, completed, created_at
- [ ] Validation rules (title 1-200, description max 1000)
- [ ] Type hints complete

**Files to Create:**
- `apps/backend/app/models/user.py`
- `apps/backend/app/models/task.py`

**Reference Specs:**
- @spec.md (Key Entities section)
- @plan.md (Phase 1 Data Model Design)

**Claude Code Prompt:**
```
@spec.md @plan.md @database-architect.md

Create User model (managed by Better Auth):
- id: str (UUID primary key)
- email: str (unique, indexed, RFC 5322)
- name: str (1-100 chars)
- password_hash: str (bcrypt)
- created_at, updated_at: datetime (auto-set)

Create Task model:
- id: int (auto-increment primary key)
- user_id: str (FK to users.id, indexed, ON DELETE CASCADE)
- title: str (1-200 chars, required)
- description: Optional[str] (max 1000 chars)
- completed: bool (default False, indexed)
- created_at: datetime (auto-set, indexed)
- updated_at: datetime (auto-update via trigger)

Include docstrings and type hints for all fields
```

---

### TASK-007: Create Database Configuration
**Priority**: Critical (P1) | **Time**: 30 min | **Dependencies**: TASK-006 | **Status**: [x]

**Description:**
Create database connection config with SQLModel engine, connection pooling for Neon PostgreSQL, and session management.

**Acceptance Criteria:**
- [ ] apps/backend/app/core/database.py created
- [ ] Engine with pool_size=5, max_overflow=10, pool_pre_ping=True
- [ ] SSL mode required for Neon
- [ ] get_session() FastAPI dependency
- [ ] create_db_and_tables() function
- [ ] drop_all_tables() for development

**Files to Create:**
- `apps/backend/app/core/database.py`

**Reference Specs:**
- @plan.md (SQLModel with Neon PostgreSQL)

**Claude Code Prompt:**
```
@plan.md Create database.py with:

from sqlmodel import Session, create_engine, SQLModel
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args={"sslmode": "require", "connect_timeout": 10}
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

---

### TASK-008: Create Alembic Migration Configuration
**Priority**: High (P1) | **Time**: 30 min | **Dependencies**: TASK-007 | **Status**: [ ]

**Description:**
Initialize Alembic for migrations and create initial migration with tables, indexes, and updated_at trigger.

**Acceptance Criteria:**
- [ ] Alembic initialized in apps/backend/alembic/
- [ ] alembic.ini configured
- [ ] env.py uses SQLModel metadata
- [ ] Initial migration with all tables and indexes
- [ ] PostgreSQL trigger for updated_at included
- [ ] Can run `alembic upgrade head`

**Files to Create:**
- `apps/backend/alembic.ini`
- `apps/backend/alembic/env.py`
- `apps/backend/alembic/versions/001_initial_schema.py`

**Claude Code Prompt:**
```
@database-architect.md

1. Initialize Alembic: cd apps/backend && alembic init alembic
2. Configure alembic.ini with DATABASE_URL from env
3. Update env.py to import SQLModel metadata
4. Create migration: alembic revision -m "initial schema"
5. Add PostgreSQL trigger in migration:
   CREATE FUNCTION update_updated_at_column()
   RETURNS TRIGGER AS $$
   BEGIN
       NEW.updated_at = NOW();
       RETURN NEW;
   END;
   $$ language 'plpgsql';

   CREATE TRIGGER update_tasks_updated_at
   BEFORE UPDATE ON tasks
   FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

**Verification:**
```bash
cd apps/backend
alembic upgrade head
psql $DATABASE_URL -c "\dt"
```

---

### TASK-009: Create Database Initialization Script
**Priority**: Medium (P1) | **Time**: 20 min | **Dependencies**: TASK-008 | **Status**: [ ]

**Description:**
Create Python script to initialize database, verify connection, and provide dev utilities.

**Acceptance Criteria:**
- [ ] apps/backend/scripts/init_db.py created
- [ ] Verifies Neon PostgreSQL connection
- [ ] Creates tables via SQLModel
- [ ] Can run multiple times (idempotent)
- [ ] Includes reset function with confirmation

**Files to Create:**
- `apps/backend/scripts/__init__.py`
- `apps/backend/scripts/init_db.py`

**Usage:**
```bash
cd apps/backend
python scripts/init_db.py
python scripts/init_db.py --reset  # DEV ONLY
```

---

## PHASE 3: BACKEND API IMPLEMENTATION (12 Tasks)

### TASK-010: Create Pydantic Settings Configuration
**Priority**: Critical (P1) | **Time**: 25 min | **Dependencies**: TASK-009 | **Status**: [ ]

**Description:**
Create Pydantic settings class for environment variable management with validation.

**Acceptance Criteria:**
- [ ] apps/backend/app/core/config.py created
- [ ] Settings class with all env vars
- [ ] Validation (BETTER_AUTH_SECRET min 32 chars)
- [ ] Type hints for all settings
- [ ] Global settings instance

**Files to Create:**
- `apps/backend/app/core/config.py`

**Claude Code Prompt:**
```
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    BETTER_AUTH_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

---

### TASK-011: Create JWT Utilities
**Priority**: Critical (P1) | **Time**: 40 min | **Dependencies**: TASK-010 | **Status**: [ ]

**Description:**
Implement JWT token verification utilities for Better Auth token validation.

**Acceptance Criteria:**
- [ ] apps/backend/app/core/security.py created
- [ ] verify_jwt_token() validates signature and expiration
- [ ] get_user_id_from_token() extracts user ID
- [ ] Invalid/expired tokens rejected properly
- [ ] Uses BETTER_AUTH_SECRET

**Files to Create:**
- `apps/backend/app/core/security.py`

**Reference Specs:**
- @spec.md (FR-004, FR-005, FR-007)

**Claude Code Prompt:**
```
import jwt
from app.core.config import settings

def verify_jwt_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        if "userId" not in payload:
            return None
        return payload
    except jwt.PyJWTError:
        return None

def get_user_id_from_token(token: str) -> Optional[str]:
    payload = verify_jwt_token(token)
    return payload.get("userId") if payload else None
```

---

### TASK-012: Create FastAPI Auth Dependency
**Priority**: Critical (P1) | **Time**: 35 min | **Dependencies**: TASK-011 | **Status**: [ ]

**Description:**
Create FastAPI dependency to extract and validate JWT from Authorization header.

**Acceptance Criteria:**
- [ ] apps/backend/app/api/deps.py created
- [ ] get_current_user() extracts token from Bearer header
- [ ] Returns user_id if valid
- [ ] Raises 401 if missing/invalid
- [ ] verify_user_access() checks resource ownership

**Files to Create:**
- `apps/backend/app/api/deps.py`

**Claude Code Prompt:**
```
from fastapi import Depends, HTTPException, Header
from app.core.security import get_user_id_from_token

async def get_current_user(authorization: str | None = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = authorization.split()[1]
    user_id = get_user_id_from_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_id

def verify_user_access(user_id: str, requested_user_id: str):
    if user_id != requested_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
```

---

### TASK-013: Create Pydantic Response Schemas
**Priority**: High (P1) | **Time**: 30 min | **Dependencies**: TASK-006 | **Status**: [ ]

**Description:**
Create Pydantic schemas for API request/response validation.

**Acceptance Criteria:**
- [ ] apps/backend/app/schemas/task.py created
- [ ] TaskCreate, TaskUpdate, TaskResponse defined
- [ ] ApiResponse[T] wrapper with success/error fields
- [ ] Validation rules match spec
- [ ] Examples for API docs

**Files to Create:**
- `apps/backend/app/schemas/task.py`
- `apps/backend/app/schemas/response.py`

**Reference Specs:**
- @spec.md (API Response Requirements)

---

### TASK-014: Create FastAPI Application
**Priority**: Critical (P1) | **Time**: 30 min | **Dependencies**: TASK-012, TASK-013 | **Status**: [ ]

**Description:**
Initialize FastAPI app with CORS, lifespan events, and health check.

**Acceptance Criteria:**
- [ ] apps/backend/app/main.py created
- [ ] CORS middleware configured
- [ ] Lifespan calls create_db_and_tables()
- [ ] GET / returns API info
- [ ] GET /health returns status
- [ ] Can run with uvicorn

**Files to Create:**
- `apps/backend/app/main.py`

**Verification:**
```bash
cd apps/backend
uvicorn app.main:app --reload
curl http://localhost:8000/health
```

---

### TASK-015: Implement GET /api/{user_id}/tasks
**Priority**: High (P2) | **Time**: 50 min | **Dependencies**: TASK-014 | **Status**: [ ]

**Description:**
Implement endpoint to list tasks with filtering (completed) and sorting (created_at, title).

**Acceptance Criteria:**
- [ ] GET endpoint with query params: completed, sort, order
- [ ] Filters by user_id (enforced)
- [ ] Default sort: created_at desc
- [ ] Returns ApiResponse[List[TaskResponse]]
- [ ] Verifies JWT and user access

**Files to Create:**
- `apps/backend/app/api/tasks.py`

**Reference Specs:**
- @spec.md (User Story 2, FR-013, FR-018-022)

---

### TASK-016: Implement POST /api/{user_id}/tasks
**Priority**: High (P2) | **Time**: 40 min | **Dependencies**: TASK-015 | **Status**: [ ]

**Description:**
Implement endpoint to create new task with title and optional description.

**Acceptance Criteria:**
- [ ] POST endpoint accepts TaskCreate
- [ ] Validates title (1-200) and description (max 1000)
- [ ] Sets user_id from path
- [ ] Returns 201 with TaskResponse
- [ ] Verifies JWT and user access

**Reference Specs:**
- @spec.md (User Story 2, FR-009-012)

---

### TASK-017: Implement GET /api/{user_id}/tasks/{task_id}
**Priority**: High (P2) | **Time**: 30 min | **Dependencies**: TASK-016 | **Status**: [ ]

**Description:**
Implement endpoint to get single task by ID.

**Acceptance Criteria:**
- [ ] GET endpoint returns single TaskResponse
- [ ] Verifies task exists (404 if not)
- [ ] Verifies ownership (403 if different user)
- [ ] Verifies JWT

---

### TASK-018: Implement PUT /api/{user_id}/tasks/{task_id}
**Priority**: High (P3) | **Time**: 40 min | **Dependencies**: TASK-017 | **Status**: [ ]

**Description:**
Implement endpoint to update task (title, description, completed).

**Acceptance Criteria:**
- [ ] PUT endpoint accepts TaskUpdate (all fields optional)
- [ ] Updates only provided fields
- [ ] updated_at auto-updated by DB trigger
- [ ] Validates and verifies ownership
- [ ] Returns updated TaskResponse

**Reference Specs:**
- @spec.md (User Story 3, FR-014-015)

---

### TASK-019: Implement DELETE /api/{user_id}/tasks/{task_id}
**Priority**: High (P5) | **Time**: 30 min | **Dependencies**: TASK-018 | **Status**: [ ]

**Description:**
Implement endpoint to permanently delete task.

**Acceptance Criteria:**
- [ ] DELETE endpoint removes task
- [ ] Verifies ownership before deletion
- [ ] Returns success message
- [ ] 404 if not found, 403 if not owner

**Reference Specs:**
- @spec.md (User Story 5, FR-016)

---

### TASK-020: Implement PATCH /api/{user_id}/tasks/{task_id}/toggle
**Priority**: High (P3) | **Time**: 25 min | **Dependencies**: TASK-019 | **Status**: [ ]

**Description:**
Implement convenience endpoint to toggle task completion status.

**Acceptance Criteria:**
- [ ] PATCH endpoint toggles completed (true↔false)
- [ ] updated_at auto-updated
- [ ] Verifies ownership
- [ ] Returns updated TaskResponse

**Reference Specs:**
- @spec.md (User Story 3)

---

### TASK-021: Add Error Handling to All Endpoints
**Priority**: High (P1) | **Time**: 40 min | **Dependencies**: TASK-020 | **Status**: [ ]

**Description:**
Add comprehensive error handling to all API endpoints with proper status codes and error messages.

**Acceptance Criteria:**
- [ ] All endpoints return standardized error responses
- [ ] 400 for validation errors
- [ ] 401 for auth errors
- [ ] 403 for authorization errors
- [ ] 404 for not found
- [ ] 500 for server errors
- [ ] Error messages are descriptive

**Reference Specs:**
- @spec.md (FR-027 to FR-031)

---

## PHASE 4: FRONTEND IMPLEMENTATION (15 Tasks)

### TASK-022: Initialize Next.js Frontend
**Priority**: Critical (P1) | **Time**: 25 min | **Dependencies**: TASK-004 | **Status**: [ ]

**Description:**
Create Next.js 16+ project with TypeScript, Tailwind CSS, and App Router.

**Commands:**
```bash
cd apps/frontend
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir
```

**Verification:**
```bash
npm run dev  # Should start on port 3000
```

---

### TASK-023: Install Frontend Dependencies
**Priority**: Critical (P1) | **Time**: 15 min | **Dependencies**: TASK-022 | **Status**: [ ]

**Description:**
Install Better Auth, SWR, Lucide React, and other frontend dependencies.

**Commands:**
```bash
cd apps/frontend
npm install better-auth swr lucide-react
npm install -D @types/node
```

---

### TASK-024: Create TypeScript Type Definitions
**Priority**: High (P1) | **Time**: 25 min | **Dependencies**: TASK-023 | **Status**: [ ]

**Description:**
Create TypeScript interfaces for User, Task, and API responses.

**Files to Create:**
- `apps/frontend/lib/types.ts`

**Content:**
```typescript
export interface User {
  id: string;
  email: string;
  name: string;
  createdAt: string;
  updatedAt: string;
}

export interface Task {
  id: number;
  userId: string;
  title: string;
  description: string | null;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: { code: string; message: string } | null;
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}
```

---

### TASK-025: Configure Better Auth Client
**Priority**: Critical (P1) | **Time**: 45 min | **Dependencies**: TASK-024 | **Status**: [ ]

**Description:**
Set up Better Auth client configuration for Next.js frontend.

**Files to Create:**
- `apps/frontend/lib/auth.ts`
- `apps/frontend/app/api/auth/[...all]/route.ts`

**Reference:** https://better-auth.com/docs/quickstart

---

### TASK-026: Create API Client with JWT Handling
**Priority**: Critical (P1) | **Time**: 50 min | **Dependencies**: TASK-025 | **Status**: [ ]

**Description:**
Create API client wrapper with JWT token handling.

**Files to Create:**
- `apps/frontend/lib/api.ts`

**Functions:** getTasks(), createTask(), updateTask(), deleteTask(), toggleTask()

---

### TASK-027: Create Sign In Page
**Priority**: Critical (P1) | **Time**: 60 min | **Dependencies**: TASK-026 | **Status**: [ ]

**Description:**
Create user sign-in page with email/password form.

**Files to Create:**
- `apps/frontend/app/auth/signin/page.tsx`

**Acceptance Criteria:**
- [ ] Email and password fields
- [ ] Form validation
- [ ] Better Auth integration
- [ ] Redirects to /tasks on success
- [ ] Link to sign up page
- [ ] Error messages displayed

---

### TASK-028: Create Sign Up Page
**Priority**: Critical (P1) | **Time**: 70 min | **Dependencies**: TASK-027 | **Status**: [ ]

**Description:**
Create user registration page with validation.

**Files to Create:**
- `apps/frontend/app/auth/signup/page.tsx`

**Acceptance Criteria:**
- [ ] Name, email, password, confirm password fields
- [ ] Password validation (min 8 chars, match)
- [ ] Auto sign-in after registration
- [ ] Redirects to /tasks
- [ ] Link to sign in page

---

### TASK-029: Create Route Protection Middleware
**Priority**: Critical (P1) | **Time**: 30 min | **Dependencies**: TASK-028 | **Status**: [ ]

**Description:**
Create middleware to protect routes requiring authentication.

**Files to Create:**
- `apps/frontend/middleware.ts`

**Acceptance Criteria:**
- [ ] Checks Better Auth session
- [ ] Redirects to /auth/signin if not authenticated
- [ ] Allows public routes (/, /auth/*)
- [ ] Works on /tasks route

---

### TASK-030: Create TaskCard Component
**Priority**: High (P2) | **Time**: 60 min | **Dependencies**: TASK-024 | **Status**: [ ]

**Description:**
Create reusable task card component with checkbox, edit, delete buttons.

**Files to Create:**
- `apps/frontend/components/tasks/task-card.tsx`

**Acceptance Criteria:**
- [ ] Displays title, description, date
- [ ] Completion checkbox
- [ ] Edit and delete buttons (Lucide icons)
- [ ] Strike-through when completed
- [ ] Loading states
- [ ] Hover effects

---

### TASK-031: Create TaskList Component
**Priority**: High (P2) | **Time**: 30 min | **Dependencies**: TASK-030 | **Status**: [ ]

**Description:**
Create task list container component.

**Files to Create:**
- `apps/frontend/components/tasks/task-list.tsx`

**Acceptance Criteria:**
- [ ] Maps tasks to TaskCard components
- [ ] Empty state message
- [ ] Responsive grid layout

---

### TASK-032: Create CreateTaskForm Component
**Priority**: High (P2) | **Time**: 60 min | **Dependencies**: TASK-024 | **Status**: [ ]

**Description:**
Create form for adding new tasks.

**Files to Create:**
- `apps/frontend/components/tasks/create-task-form.tsx`

**Acceptance Criteria:**
- [ ] Toggle open/close
- [ ] Title input with validation
- [ ] Description textarea
- [ ] Submit calls API
- [ ] Error messages
- [ ] Refreshes on success

---

### TASK-033: Create TaskFilters Component
**Priority**: Medium (P4) | **Time**: 40 min | **Dependencies**: TASK-024 | **Status**: [ ]

**Description:**
Create filters for completion status and sorting.

**Files to Create:**
- `apps/frontend/components/tasks/task-filters.tsx`

**Acceptance Criteria:**
- [ ] Filter by completed (all/active/completed)
- [ ] Sort by created_at or title
- [ ] Sort order (asc/desc)
- [ ] Updates URL query params

---

### TASK-034: Create Tasks Page with SWR
**Priority**: Critical (P2) | **Time**: 70 min | **Dependencies**: TASK-031, TASK-032, TASK-033 | **Status**: [ ]

**Description:**
Create main tasks page integrating all components with SWR for data fetching.

**Files to Create:**
- `apps/frontend/app/tasks/page.tsx`

**Acceptance Criteria:**
- [ ] Fetches tasks with SWR
- [ ] Integrates TaskList, CreateTaskForm, TaskFilters
- [ ] Handles loading and error states
- [ ] Optimistic updates
- [ ] Revalidates on mutations

---

### TASK-035: Create Edit Task Modal
**Priority**: Medium (P3) | **Time**: 50 min | **Dependencies**: TASK-034 | **Status**: [ ]

**Description:**
Create modal dialog for editing tasks.

**Files to Create:**
- `apps/frontend/components/tasks/edit-task-modal.tsx`

**Acceptance Criteria:**
- [ ] Opens when edit button clicked
- [ ] Pre-fills with current values
- [ ] Updates task on submit
- [ ] Closes on cancel or success
- [ ] Shows validation errors

---

### TASK-036: Add Loading and Error States
**Priority**: High (P2) | **Time**: 30 min | **Dependencies**: TASK-034 | **Status**: [ ]

**Description:**
Add proper loading spinners and error messages throughout the app.

**Acceptance Criteria:**
- [ ] Loading spinners on all async operations
- [ ] Error toasts/messages for failures
- [ ] Retry buttons on errors
- [ ] Skeleton loaders for task list

---

## PHASE 5: TESTING & INTEGRATION (5 Tasks)

### TASK-037: Setup Backend Test Configuration
**Priority**: High (P1) | **Time**: 30 min | **Dependencies**: TASK-021 | **Status**: [ ]

**Description:**
Configure pytest with fixtures for database and authentication.

**Files to Create:**
- `apps/backend/tests/conftest.py`

**Acceptance Criteria:**
- [ ] Test database fixtures
- [ ] Auth token fixtures
- [ ] Test client fixtures
- [ ] Can run pytest

---

### TASK-038: Write Backend API Tests
**Priority**: High (P3) | **Time**: 90 min | **Dependencies**: TASK-037 | **Status**: [ ]

**Description:**
Write comprehensive tests for all task endpoints.

**Files to Create:**
- `apps/backend/tests/test_tasks_api.py`

**Test Coverage:**
- [ ] List tasks (success, filters, sorting)
- [ ] Create task (success, validation errors)
- [ ] Get task (success, 404, 403)
- [ ] Update task (success, validation)
- [ ] Delete task (success, 404, 403)
- [ ] Toggle task (success, multiple toggles)

---

### TASK-039: Write Authentication Tests
**Priority**: High (P1) | **Time**: 60 min | **Dependencies**: TASK-037 | **Status**: [ ]

**Description:**
Test JWT authentication and user isolation.

**Files to Create:**
- `apps/backend/tests/test_authentication.py`

**Test Coverage:**
- [ ] Valid token accepted
- [ ] Invalid token rejected (401)
- [ ] Missing token rejected (401)
- [ ] User isolation enforced (403)

---

### TASK-040: Setup Frontend Testing
**Priority**: Medium (P2) | **Time**: 40 min | **Dependencies**: TASK-036 | **Status**: [ ]

**Description:**
Configure Jest and React Testing Library.

**Commands:**
```bash
cd apps/frontend
npm install -D @testing-library/react @testing-library/jest-dom jest jest-environment-jsdom
```

---

### TASK-041: Write Component Tests
**Priority**: Medium (P2) | **Time**: 80 min | **Dependencies**: TASK-040 | **Status**: [ ]

**Description:**
Write tests for TaskCard, TaskList, CreateTaskForm components.

**Files to Create:**
- `apps/frontend/components/tasks/__tests__/task-card.test.tsx`
- `apps/frontend/components/tasks/__tests__/task-list.test.tsx`
- `apps/frontend/components/tasks/__tests__/create-task-form.test.tsx`

---

## PHASE 6: DEPLOYMENT & DOCUMENTATION (9 Tasks)

### TASK-042: Prepare Backend for Deployment
**Priority**: High (P1) | **Time**: 30 min | **Dependencies**: TASK-039 | **Status**: [ ]

**Description:**
Configure backend for production deployment.

**Files to Create:**
- `apps/backend/Procfile`
- `apps/backend/Dockerfile` (optional)

**Acceptance Criteria:**
- [ ] Production settings configured
- [ ] DEBUG=False in production
- [ ] Procfile/start command created

---

### TASK-043: Deploy Backend to Railway/Render
**Priority**: Critical (P1) | **Time**: 60 min | **Dependencies**: TASK-042 | **Status**: [ ]

**Description:**
Deploy FastAPI backend to cloud platform.

**Steps:**
1. Connect GitHub repository
2. Configure environment variables
3. Deploy and verify
4. Test health endpoint
5. Update CORS_ORIGINS

---

### TASK-044: Deploy Frontend to Vercel
**Priority**: Critical (P1) | **Time**: 45 min | **Dependencies**: TASK-036 | **Status**: [ ]

**Description:**
Deploy Next.js frontend to Vercel.

**Steps:**
1. Connect GitHub repository
2. Configure environment variables
3. Deploy and verify
4. Test authentication flow

---

### TASK-045: Setup Database on Neon
**Priority**: Critical (P1) | **Time**: 30 min | **Dependencies**: TASK-008 | **Status**: [ ]

**Description:**
Create production database on Neon.

**Steps:**
1. Create Neon project
2. Create database
3. Run migrations
4. Update DATABASE_URL in backend

---

### TASK-046: Run End-to-End Tests
**Priority**: High (P2) | **Time**: 60 min | **Dependencies**: TASK-044 | **Status**: [ ]

**Description:**
Test complete user flows in production.

**Test Scenarios:**
- [ ] Sign up new account
- [ ] Sign in with credentials
- [ ] Create multiple tasks
- [ ] Edit task
- [ ] Toggle completion
- [ ] Filter and sort tasks
- [ ] Delete task
- [ ] Sign out

---

### TASK-047: Update Documentation
**Priority**: Medium (P1) | **Time**: 40 min | **Dependencies**: TASK-046 | **Status**: [ ]

**Description:**
Update README with deployment URLs and complete instructions.

**Updates:**
- [ ] Add production URLs
- [ ] Update setup instructions
- [ ] Add deployment section
- [ ] Add troubleshooting guide

---

### TASK-048: Create User Guide
**Priority**: Low (P2) | **Time**: 30 min | **Dependencies**: TASK-047 | **Status**: [ ]

**Description:**
Create user guide with screenshots.

**Files to Create:**
- `docs/USER_GUIDE.md`

**Content:**
- [ ] How to sign up/sign in
- [ ] How to create tasks
- [ ] How to manage tasks
- [ ] Screenshots of key features

---

### TASK-049: Performance Testing
**Priority**: Low (P2) | **Time**: 45 min | **Dependencies**: TASK-046 | **Status**: [ ]

**Description:**
Test performance against success criteria.

**Metrics to Verify:**
- [ ] API response time <200ms p95
- [ ] Database queries <50ms
- [ ] JWT validation <10ms
- [ ] Frontend page load <2s on 3G

---

### TASK-050: Final Review and Handoff
**Priority**: Low (P1) | **Time**: 30 min | **Dependencies**: TASK-049 | **Status**: [ ]

**Description:**
Final review of all deliverables.

**Checklist:**
- [ ] All user stories (P1-P5) implemented
- [ ] All FR-001 to FR-031 satisfied
- [ ] Test coverage ≥90% backend, ≥80% frontend
- [ ] All success criteria met
- [ ] Documentation complete
- [ ] Production deployment verified
- [ ] No critical bugs

---

## Task Summary

**Phase 1**: 4 tasks (Setup)
**Phase 2**: 5 tasks (Database)
**Phase 3**: 12 tasks (Backend API)
**Phase 4**: 15 tasks (Frontend)
**Phase 5**: 5 tasks (Testing)
**Phase 6**: 9 tasks (Deployment)

**Total**: 50 tasks

## Progress Tracking

Update task statuses as you complete them:
- [ ] → [>] when starting
- [>] → [x] when completed
- [>] → [!] if blocked
- [ ] → [~] if skipped/deferred

## Using These Tasks

### Reference during work:
```bash
@tasks.md show TASK-015 details
@backend-developer-agent.md implement TASK-015
```

### Track progress:
```bash
# Mark task as in progress
# Change [ ] to [>] in tasks.md

# Mark task as complete
# Change [>] to [x] in tasks.md
```

### Daily workflow:
1. Morning: Review next 3-5 tasks
2. During work: Reference task details and prompts
3. Evening: Update task statuses
4. Commit: Include completed task IDs in commit messages

---

**End of Tasks Document**
