# Implementation Plan: Phase II - Full-Stack Todo Application

**Branch**: `001-name-phase2-fullstack-web` | **Date**: 2026-01-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-name-phase2-fullstack-web/spec.md`

## Summary

Implement a full-stack web application for multi-user todo task management with secure authentication. The system consists of a Next.js 16+ frontend with Better Auth integration and a FastAPI backend with SQLModel ORM connected to Neon PostgreSQL. Users can register, authenticate via JWT tokens (7-day expiration), and perform CRUD operations on their personal tasks with filtering and sorting capabilities. The architecture enforces strict user isolation and follows Spec-Driven Development with TDD methodology.

**Key Technical Decisions:**
- Better Auth (not NextAuth) for authentication with JWT tokens
- Monorepo structure with separate frontend (Vercel) and backend (Railway) deployments
- SQLModel for type-safe database operations with Pydantic validation
- Shared BETTER_AUTH_SECRET for JWT validation across frontend and backend
- Database indexes on user_id, completed, and created_at for performance
- Standardized JSON API responses with success/error structure

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.3+ with Next.js 16+
- Backend: Python 3.11+

**Primary Dependencies**:
- Frontend: Next.js 16+, React 18+, Better Auth, Tailwind CSS 3+, Lucide React (icons), SWR
- Backend: FastAPI 0.104+, SQLModel, Pydantic 2.0+, python-jose (JWT), bcrypt, Alembic (migrations)

**Storage**: Neon Serverless PostgreSQL 16+ with connection pooling

**Testing**:
- Frontend: Jest, React Testing Library, Playwright (E2E)
- Backend: pytest, pytest-asyncio, httpx (async test client)

**Target Platform**:
- Frontend: Vercel (Node.js 18+)
- Backend: Railway or Render (Docker container)
- Database: Neon cloud (serverless PostgreSQL)

**Project Type**: Web application (monorepo with separate frontend and backend)

**Performance Goals**:
- API response time: <200ms p95 for single-task operations
- Database queries: <50ms for indexed lookups
- JWT validation: <10ms
- Frontend page load: <2s on 3G
- Support 100 concurrent authenticated users

**Constraints**:
- JWT tokens must remain valid for exactly 7 days
- User data isolation: 100% enforcement (no cross-user access)
- All passwords hashed with bcrypt (minimum 10 rounds)
- API endpoints must validate JWT on every protected request
- Database operations must be atomic (no partial updates)
- Input validation: title 1-200 chars, description max 1000 chars

**Scale/Scope**:
- Expected users: 100-1000 concurrent users
- Tasks per user: Up to 10,000 tasks
- API endpoints: 6 task CRUD endpoints + auth endpoints
- Frontend pages: 4 pages (signin, signup, dashboard, task list)
- Database tables: 2 (users managed by Better Auth, tasks application-managed)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Spec-Driven Development ✅ PASS
- Feature specification completed in spec.md
- All implementation will follow specification requirements
- No manual coding outside of spec-driven workflow
- Claude Code will generate all code from specifications

### II. Clean Code ✅ PASS
- Python backend will follow PEP 8 conventions
- Type hints required for all function signatures (TypeScript frontend, Python backend)
- Docstrings mandatory for all public functions and classes
- Code readability enforced through linting (ESLint frontend, Black/Ruff backend)

### III. Test-First Development (TDD) ✅ PASS
- TDD workflow: Red (failing test) → Green (minimal implementation) → Refactor
- Backend: pytest with test coverage ≥90%
- Frontend: Jest + React Testing Library for components, Playwright for E2E
- No implementation without prior failing test
- Integration tests for all API endpoints and user flows

### IV. Single Responsibility Principle ✅ PASS
- **Frontend Separation:**
  - Components: UI presentation only (TaskCard, TaskList, CreateTaskForm)
  - API Client: API communication logic (lib/api.ts)
  - Auth Client: Authentication logic (lib/auth.ts)
  - Pages: Route handling and composition (app/*/page.tsx)
- **Backend Separation:**
  - Models: Data structures (SQLModel classes)
  - Services: Business logic (task operations, validation)
  - API Routes: Request/response handling (FastAPI endpoints)
  - Auth Middleware: JWT validation (dependency injection)

### V. Evolutionary Architecture ✅ PASS
- Backend uses repository pattern via SQLModel (can swap to different ORM)
- Frontend API client abstraction allows backend changes without UI rewrites
- Environment-based configuration (local, staging, production)
- Database migrations via Alembic for schema evolution
- Monorepo structure supports future services (notifications, analytics, AI chatbot in Phase III)

### VI. User Experience First ✅ PASS
- Clear authentication flows with helpful error messages
- Immediate feedback on task operations (optimistic updates with SWR)
- Loading states for all async operations
- Intuitive task list with filtering and sorting
- Responsive design with Tailwind CSS (mobile-first)
- Error messages are actionable (e.g., "Password must be at least 8 characters")

**Constitution Compliance: ALL GATES PASSED ✅**

## Project Structure

### Documentation (this feature)

```text
specs/001-name-phase2-fullstack-web/
├── spec.md              # Feature specification (COMPLETED)
├── plan.md              # This file - Implementation plan
├── research.md          # Phase 0 output - Technology decisions and patterns
├── data-model.md        # Phase 1 output - Entity relationships and validation
├── quickstart.md        # Phase 1 output - Developer setup guide
├── contracts/           # Phase 1 output - API contracts
│   ├── auth-api.yaml    # Better Auth API specification
│   └── tasks-api.yaml   # Task CRUD API specification (OpenAPI 3.0)
└── tasks.md             # Phase 2 output - Implementation tasks (/sp.tasks command)
```

### Source Code (repository root)

```text
# Monorepo structure for web application

apps/
├── frontend/                   # Next.js 16+ application
│   ├── app/                    # App Router pages
│   │   ├── (auth)/            # Auth layout group
│   │   │   ├── signin/        # Sign in page
│   │   │   └── signup/        # Sign up page
│   │   ├── (dashboard)/       # Protected layout group
│   │   │   ├── layout.tsx     # Dashboard shell
│   │   │   └── page.tsx       # Task list page
│   │   ├── api/               # API routes
│   │   │   └── auth/          # Better Auth handlers
│   │   │       └── [...all]/route.ts
│   │   ├── layout.tsx         # Root layout
│   │   └── page.tsx           # Landing page
│   ├── components/            # React components
│   │   ├── tasks/            # Task-related components
│   │   │   ├── task-card.tsx
│   │   │   ├── task-list.tsx
│   │   │   ├── create-task-form.tsx
│   │   │   └── task-filters.tsx
│   │   └── ui/               # Shared UI components
│   │       ├── button.tsx
│   │       ├── input.tsx
│   │       └── card.tsx
│   ├── lib/                  # Utility libraries
│   │   ├── api.ts           # API client with JWT handling
│   │   ├── auth.ts          # Better Auth configuration
│   │   ├── types.ts         # TypeScript type definitions
│   │   └── utils.ts         # Helper functions
│   ├── middleware.ts         # Route protection
│   ├── tailwind.config.ts   # Tailwind configuration
│   ├── next.config.js       # Next.js configuration
│   ├── package.json
│   └── tsconfig.json
│   └── tests/               # Frontend tests
│       ├── components/      # Component tests (Jest)
│       └── e2e/            # End-to-end tests (Playwright)
│
└── backend/                  # FastAPI application
    ├── app/                  # Application code
    │   ├── models/          # SQLModel data models
    │   │   ├── user.py      # User model (Better Auth integration)
    │   │   └── task.py      # Task model
    │   ├── services/        # Business logic
    │   │   ├── auth.py      # JWT validation service
    │   │   └── tasks.py     # Task operations service
    │   ├── api/             # API routes
    │   │   ├── deps.py      # Dependency injection (get_current_user)
    │   │   ├── auth.py      # Auth endpoints
    │   │   └── tasks.py     # Task CRUD endpoints
    │   ├── core/            # Core configuration
    │   │   ├── config.py    # Settings (env vars)
    │   │   ├── database.py  # Database connection
    │   │   └── security.py  # JWT utilities
    │   ├── schemas/         # Pydantic request/response schemas
    │   │   ├── auth.py      # Auth DTOs
    │   │   └── task.py      # Task DTOs
    │   └── main.py          # FastAPI app initialization
    ├── alembic/             # Database migrations
    │   ├── versions/        # Migration files
    │   └── env.py           # Alembic configuration
    ├── tests/               # Backend tests
    │   ├── conftest.py      # Pytest fixtures
    │   ├── test_auth.py     # Authentication tests
    │   ├── test_tasks.py    # Task CRUD tests
    │   └── test_integration.py  # Integration tests
    ├── requirements.txt     # Python dependencies
    ├── pyproject.toml       # Python project config
    ├── Dockerfile           # Container image
    └── alembic.ini          # Alembic config

# Root configuration
docker-compose.yml           # Local development environment
.env.example                 # Environment variable template
.gitignore
package.json                 # Workspace configuration (npm workspaces)
README.md                    # Project documentation
```

**Structure Decision**: Web application (Option 2) selected because the feature requires separate frontend (Next.js) and backend (FastAPI) with different runtime environments. Frontend deploys to Vercel (Node.js), backend deploys to Railway (Python/Docker). Monorepo structure enables code sharing, unified versioning, and coordinated deployments while maintaining clear service boundaries.

## Complexity Tracking

> **No constitutional violations detected - this section intentionally left blank.**

All constitutional principles are satisfied without requiring exceptions or complexity justifications. The architecture follows established patterns (repository pattern, dependency injection, separation of concerns) that align with SRP and evolutionary architecture principles.

## Phase 0: Research & Technology Decisions

**Objective**: Resolve all technical uncertainties and document technology choices with rationale.

### Research Tasks

1. **Better Auth Integration Pattern**
   - Research: How to integrate Better Auth in Next.js 16+ App Router
   - Research: Better Auth database adapter configuration for Neon PostgreSQL
   - Research: JWT plugin configuration and token validation flow
   - Document: Setup steps, configuration examples, and integration patterns

2. **JWT Validation Architecture**
   - Research: How FastAPI validates JWT tokens from Better Auth
   - Research: python-jose vs PyJWT for JWT verification
   - Research: Shared secret management (BETTER_AUTH_SECRET) between services
   - Document: Validation flow, error handling, and security best practices

3. **SQLModel with Neon PostgreSQL**
   - Research: SQLModel connection pooling configuration for Neon
   - Research: Alembic migration patterns with SQLModel
   - Research: Database trigger creation for updated_at automation
   - Document: Connection setup, migration workflow, and performance tuning

4. **Next.js App Router Patterns**
   - Research: Server Components vs Client Components for task UI
   - Research: Route groups for auth and dashboard layouts
   - Research: Middleware for route protection and JWT validation
   - Document: Component architecture, data fetching patterns, and authentication flow

5. **SWR Data Fetching**
   - Research: SWR configuration for authenticated requests
   - Research: Optimistic updates for task operations
   - Research: Error handling and retry strategies
   - Document: Implementation patterns, cache invalidation, and mutation strategies

6. **Deployment Architecture**
   - Research: Vercel environment variable configuration for Next.js
   - Research: Railway/Render Docker deployment for FastAPI
   - Research: Neon PostgreSQL connection string and pooling limits
   - Document: Deployment checklist, environment setup, and CI/CD considerations

### Deliverables

**research.md** containing:
- Technology selections with rationale for each decision
- Architecture diagrams showing frontend ↔ backend ↔ database flow
- Security considerations for JWT token handling
- Performance optimization strategies (database indexes, connection pooling)
- Development environment setup requirements
- Testing strategy for each layer (unit, integration, E2E)

**Acceptance Criteria**:
- All NEEDS CLARIFICATION items from Technical Context resolved
- Each technology choice justified with alternatives considered
- Security implications documented and mitigated
- Performance targets mapped to implementation strategies
- Development setup reproducible from documentation

## Phase 1: Design & Contracts

**Prerequisites**: research.md completed with all technology decisions documented

### 1.1 Data Model Design

**Task**: Create data-model.md with entity definitions, relationships, and validation rules.

**Entities**:

1. **User** (managed by Better Auth)
   - id: string (UUID, primary key)
   - email: string (unique, indexed, RFC 5322 validation)
   - name: string (required, 1-100 chars)
   - password_hash: string (bcrypt, 10+ rounds)
   - created_at: datetime (auto-set)
   - updated_at: datetime (auto-update trigger)
   - Relationships: One-to-Many with Task (user.id → task.user_id)

2. **Task** (application-managed)
   - id: integer (auto-increment, primary key)
   - user_id: string (foreign key → users.id, indexed, ON DELETE CASCADE)
   - title: string (required, 1-200 chars, non-empty validation)
   - description: string | null (optional, max 1000 chars)
   - completed: boolean (default false, indexed)
   - created_at: datetime (auto-set, indexed)
   - updated_at: datetime (auto-update trigger)
   - Relationships: Many-to-One with User (task.user_id → user.id)

**Validation Rules**:
- Email: Must match RFC 5322 format, case-insensitive uniqueness
- Password: Minimum 8 characters, bcrypt hashing before storage
- Title: Non-empty after trimming whitespace, max 200 characters
- Description: Nullable, max 1000 characters if provided
- Timestamps: UTC timezone, ISO 8601 format in API responses

**Database Constraints**:
- Users table: UNIQUE(email), PRIMARY KEY(id)
- Tasks table: PRIMARY KEY(id), FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
- Indexes: tasks(user_id), tasks(completed), tasks(created_at)
- Trigger: tasks.updated_at auto-update on UPDATE operations

**State Transitions**:
- Task completion: incomplete (false) ↔ complete (true)
- No soft deletes - DELETE operations are permanent

### 1.2 API Contract Generation

**Task**: Generate OpenAPI 3.0 specifications in `/contracts/` directory.

**contracts/auth-api.yaml**:
```yaml
# Better Auth endpoints (auto-generated by Better Auth library)
POST /api/auth/signup
  Request: { email, name, password }
  Response: { user: User, session: { token: string, expiresAt: datetime } }
  Errors: 400 (validation), 409 (email exists)

POST /api/auth/signin
  Request: { email, password }
  Response: { user: User, session: { token: string, expiresAt: datetime } }
  Errors: 400 (validation), 401 (invalid credentials)

POST /api/auth/signout
  Request: Authorization: Bearer <token>
  Response: { success: true }
  Errors: 401 (invalid token)

GET /api/auth/session
  Request: Authorization: Bearer <token>
  Response: { user: User, session: Session }
  Errors: 401 (invalid token)
```

**contracts/tasks-api.yaml**:
```yaml
# Task CRUD endpoints
POST /api/{user_id}/tasks
  Request: Authorization: Bearer <token>, Body: { title, description? }
  Response: { success: true, data: Task, error: null }
  Errors: 400 (validation), 401 (unauthorized), 403 (forbidden)

GET /api/{user_id}/tasks
  Request: Authorization: Bearer <token>, Query: { completed?, sort?, order? }
  Response: { success: true, data: Task[], error: null }
  Errors: 401 (unauthorized), 403 (forbidden), 400 (invalid query params)

GET /api/{user_id}/tasks/{task_id}
  Request: Authorization: Bearer <token>
  Response: { success: true, data: Task, error: null }
  Errors: 401 (unauthorized), 403 (forbidden), 404 (not found)

PUT /api/{user_id}/tasks/{task_id}
  Request: Authorization: Bearer <token>, Body: { title?, description?, completed? }
  Response: { success: true, data: Task, error: null }
  Errors: 400 (validation), 401 (unauthorized), 403 (forbidden), 404 (not found)

DELETE /api/{user_id}/tasks/{task_id}
  Request: Authorization: Bearer <token>
  Response: { success: true, data: { message: "Task deleted" }, error: null }
  Errors: 401 (unauthorized), 403 (forbidden), 404 (not found)
```

**Error Response Format** (applies to all endpoints):
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

**Error Codes**:
- VALIDATION_ERROR (400)
- UNAUTHORIZED (401)
- FORBIDDEN (403)
- NOT_FOUND (404)
- CONFLICT (409)
- INTERNAL_SERVER_ERROR (500)
- SERVICE_UNAVAILABLE (503)

### 1.3 Developer Quickstart Guide

**Task**: Create quickstart.md with step-by-step setup instructions.

**Contents**:
1. **Prerequisites**
   - Node.js 18+, Python 3.11+, Docker (optional)
   - Neon account and database created
   - Git repository cloned

2. **Environment Setup**
   ```bash
   # Backend setup
   cd apps/backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt

   # Frontend setup
   cd apps/frontend
   npm install
   ```

3. **Environment Variables**
   ```bash
   # Backend .env
   DATABASE_URL=postgresql://user:pass@host/db
   BETTER_AUTH_SECRET=your-secret-key
   JWT_ALGORITHM=HS256
   JWT_EXPIRE_DAYS=7

   # Frontend .env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000
   BETTER_AUTH_SECRET=your-secret-key
   ```

4. **Database Migrations**
   ```bash
   cd apps/backend
   alembic upgrade head
   ```

5. **Running Locally**
   ```bash
   # Terminal 1: Backend
   cd apps/backend
   uvicorn app.main:app --reload --port 8000

   # Terminal 2: Frontend
   cd apps/frontend
   npm run dev
   ```

6. **Testing**
   ```bash
   # Backend tests
   cd apps/backend
   pytest

   # Frontend tests
   cd apps/frontend
   npm test
   npm run test:e2e
   ```

### 1.4 Agent Context Update

**Task**: Update Claude Code agent context with Phase II technologies.

```bash
bash .specify/scripts/bash/update-agent-context.sh claude
```

This adds to agent-specific context:
- Next.js 16+ App Router patterns
- Better Auth integration
- FastAPI + SQLModel patterns
- Neon PostgreSQL connection
- JWT validation flow
- Monorepo workspace configuration

### Deliverables

- ✅ data-model.md with entities, relationships, validation rules
- ✅ contracts/auth-api.yaml with Better Auth endpoints
- ✅ contracts/tasks-api.yaml with Task CRUD endpoints (OpenAPI 3.0)
- ✅ quickstart.md with developer setup guide
- ✅ Agent context updated with Phase II technology stack

**Acceptance Criteria**:
- Data model maps 1:1 to functional requirements from spec.md
- API contracts specify all request/response formats with examples
- Validation rules enforce constraints from FR-001 through FR-031
- Quickstart guide is reproducible (new developer can follow and run app)
- Agent context contains all technologies needed for implementation

## Phase 2: Task Breakdown

**Prerequisites**: research.md, data-model.md, contracts/, quickstart.md all completed

**Objective**: Generate tasks.md with atomic, testable implementation tasks.

**Process**: Run `/sp.tasks` command to automatically generate tasks from:
- User stories in spec.md (P1-P5 priorities)
- Functional requirements (FR-001 through FR-031)
- API contracts in contracts/ directory
- Data model in data-model.md
- Success criteria in spec.md

**Expected Task Structure**:
1. **Authentication Tasks (P1)**
   - Setup Better Auth in Next.js frontend
   - Implement JWT validation middleware in FastAPI
   - Create signup/signin pages
   - Test user registration flow
   - Test JWT token expiration

2. **Database Tasks (P1)**
   - Create SQLModel models (User, Task)
   - Generate Alembic migration for initial schema
   - Create database indexes (user_id, completed, created_at)
   - Implement updated_at trigger
   - Test database operations

3. **Backend API Tasks (P2-P5)**
   - Implement POST /api/{user_id}/tasks (P2)
   - Implement GET /api/{user_id}/tasks (P2)
   - Implement GET /api/{user_id}/tasks/{task_id} (P3)
   - Implement PUT /api/{user_id}/tasks/{task_id} (P3)
   - Implement DELETE /api/{user_id}/tasks/{task_id} (P5)
   - Add filtering by completed status (P4)
   - Add sorting by created_at and title (P4)
   - Test all endpoints with user isolation

4. **Frontend UI Tasks (P2-P5)**
   - Create TaskCard component (P2)
   - Create TaskList component (P2)
   - Create CreateTaskForm component (P2)
   - Create TaskFilters component (P4)
   - Implement task completion toggle (P3)
   - Implement task editing (P3)
   - Implement task deletion (P5)
   - Test all components

5. **Integration Tasks**
   - Connect frontend API client to backend
   - Implement SWR for data fetching
   - Add optimistic updates
   - Test end-to-end user flows
   - Test error handling and edge cases

**Deliverable**: tasks.md generated by `/sp.tasks` command (NOT created by /sp.plan)

**Note**: The `/sp.plan` command stops after Phase 1. Phase 2 (task breakdown) requires running the separate `/sp.tasks` command.

## Implementation Sequence

**This plan establishes the foundation for implementation but does NOT include the actual implementation tasks. The implementation tasks will be generated by the `/sp.tasks` command in Phase 2.**

### Pre-Implementation Checklist

Before running `/sp.tasks`:
- [ ] Constitution Check passed (all principles satisfied)
- [ ] research.md completed with all technology decisions
- [ ] data-model.md completed with entity definitions
- [ ] contracts/ directory contains auth-api.yaml and tasks-api.yaml
- [ ] quickstart.md completed with setup instructions
- [ ] Agent context updated with Phase II technologies

### Task Generation Command

```bash
# After plan.md is approved, run:
/sp.tasks
```

This will:
1. Parse user stories from spec.md (P1-P5 priorities)
2. Extract functional requirements (FR-001 through FR-031)
3. Map requirements to API contracts
4. Generate atomic tasks with test cases
5. Establish task dependencies
6. Output tasks.md with implementation checklist

### Implementation Workflow (Post-Task Generation)

Once tasks.md is generated:

1. **TDD Cycle for Each Task**
   - Red: Write failing test(s) for the task
   - Green: Implement minimal code to pass tests
   - Refactor: Improve code quality while keeping tests green

2. **Task Dependencies**
   - Complete P1 tasks before P2-P5 (authentication foundation)
   - Complete backend API before frontend integration
   - Complete data model before business logic

3. **Testing Strategy**
   - Unit tests: All services, models, and utility functions (≥90% coverage)
   - Integration tests: All API endpoints with authentication
   - Component tests: All React components
   - E2E tests: Critical user flows (signup → login → create task → complete task)

4. **Deployment**
   - Backend: Railway/Render with Docker container
   - Frontend: Vercel with environment variables
   - Database: Neon PostgreSQL with connection pooling

## Risk Management

### Identified Risks & Mitigation

1. **Better Auth Learning Curve**
   - **Risk**: Complex setup with Next.js 16+ App Router and database adapter
   - **Mitigation**: Phase 0 research includes Better Auth integration patterns and examples
   - **Fallback**: Use NextAuth v5 if Better Auth proves too complex (requires spec update)
   - **Indicator**: If setup takes >4 hours in Phase 0, escalate for decision

2. **JWT Validation Synchronization**
   - **Risk**: Frontend and backend JWT validation could fall out of sync if BETTER_AUTH_SECRET differs
   - **Mitigation**: Shared environment variable with validation checks on startup
   - **Fallback**: Centralized auth service (increases complexity)
   - **Indicator**: 401 errors during testing despite valid tokens

3. **Neon PostgreSQL Connection Limits**
   - **Risk**: Serverless PostgreSQL has connection limits, could cause 503 errors under load
   - **Mitigation**: Configure connection pooling (max_connections=10, min_connections=2)
   - **Fallback**: Upgrade Neon plan or use PgBouncer connection pooler
   - **Indicator**: Database connection errors in logs

4. **Database Trigger Compatibility**
   - **Risk**: Alembic migration for updated_at trigger may fail or not work as expected
   - **Mitigation**: Test trigger in Phase 0 research with sample migration
   - **Fallback**: Application-level timestamp updates (add to service layer)
   - **Indicator**: updated_at not updating automatically on task modifications

5. **Time Overrun on Frontend Components**
   - **Risk**: 5 days might be insufficient for full frontend implementation with styling
   - **Mitigation**: Prioritize P1-P3 features (auth + basic CRUD), defer P4-P5 if needed
   - **Fallback**: MVP = authentication + task list without filters/sorting
   - **Indicator**: End of day 3 and frontend not yet started

6. **Deployment Configuration Issues**
   - **Risk**: Environment variables, CORS, or database connections fail in production
   - **Mitigation**: Test deployment to staging environment before production
   - **Fallback**: Local Docker compose environment for demos
   - **Indicator**: Production deployment errors on first attempt

### Performance Risk Mitigation

**Target**: <200ms p95 API response time, <50ms database queries

**Risks**:
- Unindexed queries causing slow task list retrieval
- N+1 query problems with SQLModel relationships
- Large task lists without pagination

**Mitigation**:
- Phase 1: Define indexes in data-model.md (user_id, completed, created_at)
- Database migrations include all index creation
- Test with 1000+ tasks per user during integration testing
- Implement pagination if response time exceeds targets (defer to Phase III if not needed for MVP)

### Security Risk Mitigation

**Target**: 100% user isolation, 100% JWT validation on protected endpoints

**Risks**:
- Improper JWT validation allowing unauthorized access
- Missing user_id checks enabling cross-user data access
- Password storage without proper bcrypt hashing

**Mitigation**:
- Phase 0: Document JWT validation pattern from Better Auth
- Every API endpoint includes get_current_user dependency injection
- Integration tests include cross-user access attempts (must return 403)
- Better Auth handles password hashing (bcrypt by default)
- Security review before deployment

## Success Criteria

### Phase 0 Complete When:
- [ ] research.md contains all technology decisions with rationale
- [ ] All "NEEDS CLARIFICATION" items resolved
- [ ] Better Auth integration pattern documented with examples
- [ ] JWT validation flow documented with security considerations
- [ ] Database schema design validated against requirements

### Phase 1 Complete When:
- [ ] data-model.md defines all entities with validation rules
- [ ] contracts/ contains complete OpenAPI specifications
- [ ] quickstart.md allows new developer to run app locally
- [ ] Agent context updated with Phase II technologies
- [ ] All deliverables reviewed and approved

### Phase 2 Ready When:
- [ ] Plan approved by stakeholder
- [ ] All Phase 0 and Phase 1 deliverables completed
- [ ] No blocking technical uncertainties remain
- [ ] Ready to run `/sp.tasks` command for task generation

### Final Implementation Success (Post-Tasks):
- [ ] All user stories (P1-P5) implemented and tested
- [ ] All functional requirements (FR-001 to FR-031) satisfied
- [ ] Test coverage ≥90% for backend, ≥80% for frontend
- [ ] All success criteria from spec.md met (SC-001 to SC-012)
- [ ] Performance targets achieved (<200ms p95, <50ms DB queries)
- [ ] Security targets achieved (100% user isolation, 100% JWT validation)
- [ ] Deployed to production (Vercel + Railway + Neon)
- [ ] Documentation complete (README.md, API docs, deployment guide)

## Next Steps

1. **Review and Approve Plan**: Stakeholder reviews this plan.md for completeness
2. **Execute Phase 0**: Generate research.md with technology decisions
3. **Execute Phase 1**: Generate data-model.md, contracts/, quickstart.md
4. **Run `/sp.tasks`**: Generate tasks.md with implementation tasks
5. **Implement with TDD**: Follow Red-Green-Refactor cycle for each task
6. **Deploy and Validate**: Deploy to production and verify success criteria

**Command to Generate Tasks** (after plan approval):
```bash
/sp.tasks
```

## Architecture Decision Records (ADR) Checkpoints

**During Phase 0 Research**: If significant architectural decisions are made (e.g., choosing Better Auth over NextAuth, selecting SQLModel over raw SQLAlchemy), consider documenting with:
```bash
/sp.adr "Better Auth vs NextAuth for Next.js 16 App Router"
```

**During Phase 1 Design**: If API design choices involve tradeoffs (e.g., REST vs GraphQL, JWT vs sessions), document with:
```bash
/sp.adr "JWT Token Authentication vs Session-Based Auth"
```

**During Implementation**: If major refactoring or pattern changes occur, document the decision before proceeding.

## Appendix: Reference Materials

### Specification Reference
- Feature Spec: [spec.md](./spec.md)
- User Stories: 5 stories (P1-P5) with 20 acceptance scenarios
- Functional Requirements: 31 requirements (FR-001 to FR-031)
- Success Criteria: 12 measurable outcomes + 4 performance targets + 5 security targets

### Technology Documentation
- Next.js 16: https://nextjs.org/docs
- Better Auth: https://better-auth.com/docs
- FastAPI: https://fastapi.tiangolo.com/
- SQLModel: https://sqlmodel.tiangolo.com/
- Neon PostgreSQL: https://neon.tech/docs
- Alembic: https://alembic.sqlalchemy.org/

### Constitutional Principles
- Spec-Driven Development: All code from specifications
- TDD Mandatory: Red-Green-Refactor cycle for all features
- Single Responsibility: Clear separation of concerns
- Evolutionary Architecture: Design for Phase III enhancements
- User Experience First: Intuitive, responsive, helpful interface

---

**Plan Status**: Ready for Phase 0 Execution
**Next Command**: Begin Phase 0 research or proceed directly to Phase 1 design if no clarifications needed
**Final Command**: `/sp.tasks` (after Phases 0 and 1 complete)
