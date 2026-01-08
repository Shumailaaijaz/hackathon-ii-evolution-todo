# Evolution of Todo - Project Overview

**Project Type**: Educational Hackathon - Spec-Driven Development with AI-Assisted Coding
**Current Phase**: Phase II - Full-Stack Web Application
**Status**: Specification & Planning Stage
**Last Updated**: 2026-01-08

---

## Table of Contents

1. [Project Purpose](#project-purpose)
2. [Current Phase](#current-phase)
3. [Technology Stack](#technology-stack)
4. [Feature List](#feature-list)
5. [Architecture Overview](#architecture-overview)
6. [Development Approach](#development-approach)
7. [Project Structure](#project-structure)
8. [Getting Started](#getting-started)
9. [Cross-References](#cross-references)

---

## Project Purpose

### Educational Context

"Evolution of Todo" is a **hackathon project** demonstrating the evolution of a simple application through multiple phases of architectural sophistication. The project serves as a comprehensive case study for:

- **Spec-Driven Development (SDD)**: All code is generated from specifications
- **AI-Assisted Coding**: Using specialized AI agents for different development concerns
- **Clean Architecture**: Maintaining separation of concerns through evolution
- **Test-First Development**: TDD with comprehensive test coverage
- **Evolutionary Design**: Forward-compatible architecture enabling seamless upgrades

### Phase Evolution Journey

The project progresses through five phases, each adding new capabilities while preserving existing functionality:

| Phase | Description | Status |
|-------|-------------|--------|
| **Phase I** | In-memory Python console app | ✅ Complete |
| **Phase II** | Full-stack web app (Next.js + FastAPI + PostgreSQL) | 🔄 In Progress |
| Phase III | AI chatbot integration | ⏳ Planned |
| Phase IV | Containerization with Kubernetes | ⏳ Planned |
| Phase V | Cloud-native event-driven architecture | ⏳ Planned |

### Production-Ready Goals

While educational in nature, Phase II targets **production-ready** quality standards:

- Comprehensive test coverage (>80% unit, E2E, integration)
- Type-safe implementations (TypeScript strict mode, Python type hints)
- Security best practices (JWT authentication, input validation, SQL injection prevention)
- Performance optimization (connection pooling, caching, lazy loading)
- Accessibility compliance (WCAG 2.1 Level AA)
- Responsive design (mobile-first approach)
- CI/CD deployment (Vercel + Railway)
- Comprehensive documentation (OpenAPI, JSDoc, Python docstrings)

---

## Current Phase

### Phase II: Full-Stack Web Application

**Objective**: Transform the Phase I console application into a modern full-stack web system with persistence, authentication, and RESTful API.

#### What's New in Phase II

Phase II **extends** Phase I by adding:

| Category | Phase I | Phase II Enhancement |
|----------|---------|---------------------|
| **User Interface** | Console menu | Next.js 16+ web UI with React 19 |
| **Data Access** | In-memory dictionary | PostgreSQL with SQLModel ORM |
| **Business Logic** | Python TaskManager class | FastAPI REST API endpoints |
| **User Management** | Single user (implicit) | Multi-user with Better Auth + JWT |
| **State Management** | Direct object manipulation | API calls with SWR caching |
| **Testing** | Pytest unit tests | Playwright E2E + API integration tests |
| **Deployment** | Local Python script | Vercel (frontend) + Railway (backend) |
| **Development** | Single Python file | Monorepo with workspace management |

#### What's Preserved from Phase I

Phase II maintains Phase I's architectural principles:

- Three-layer architecture (UI → Business Logic → Data)
- Single Responsibility Principle (clear separation of concerns)
- Exception-based error handling
- Type-safe implementations
- Comprehensive test coverage
- User experience focus (clear messages, validation)

#### Project Timeline

- **Phase I Completion**: 2026-01-02 ✅
- **Phase II Start**: 2026-01-08 (current)
- **Phase II Target**: TBD (specification-driven)

**Current Stage**: Specification & Planning
- Main specification (`spec.md`): Pending
- Architecture plan (`plan.md`): Pending
- Task breakdown (`tasks.md`): Pending

---

## Technology Stack

### Frontend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | 16+ | React framework with App Router, Server Components |
| **React** | 19 | UI library with Server Actions, Suspense |
| **TypeScript** | 5.x | Type-safe JavaScript with strict mode |
| **Tailwind CSS** | 3.x | Utility-first CSS framework |
| **SWR** | 2.x | Data fetching with caching and revalidation |
| **Better Auth** | Latest | Authentication library (client-side) |
| **Playwright** | Latest | E2E testing framework |
| **Jest** | Latest | Unit testing framework |
| **React Testing Library** | Latest | Component testing utilities |

**Key Frontend Patterns**:
- Server Components by default (Client Components only when needed)
- Backend-for-Frontend (BFF) pattern for API routes
- Optimistic UI updates with SWR
- Progressive enhancement
- Mobile-first responsive design

### Backend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.115+ | Modern Python web framework with async support |
| **Python** | 3.11+ | Programming language (with type hints) |
| **SQLModel** | 0.0.24+ | SQL database ORM based on Pydantic |
| **Pydantic** | 2.x | Data validation using Python type annotations |
| **Uvicorn** | Latest | ASGI server for FastAPI |
| **Better Auth** | Latest | Authentication library (server-side) |
| **Alembic** | 1.x | Database migration tool |
| **Pytest** | Latest | Testing framework |
| **httpx** | Latest | Async HTTP client for testing |

**Key Backend Patterns**:
- REST API with OpenAPI documentation
- Repository pattern for data access
- Service layer for business logic
- Dependency injection for testability
- Async/await for I/O operations

### Database Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **PostgreSQL** | 15+ | Primary relational database |
| **Neon** | Latest | Serverless PostgreSQL hosting |
| **PgBouncer** | Integrated | Connection pooling (Neon provides this) |

**Key Database Features**:
- Connection pooling for performance
- Prepared statements for security (SQL injection prevention)
- B-tree indexes for query optimization
- Foreign key constraints for referential integrity
- JSON columns for flexible data (if needed)

### Authentication Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Authentication Library** | Better Auth | User registration, login, session management |
| **Token Format** | JWT | Stateless authentication tokens |
| **Token Storage** | httpOnly cookies | XSS-safe token storage |
| **Password Hashing** | bcrypt | Secure password storage |
| **Session Management** | Redis (optional) | Server-side session tracking |

### Development Stack

| Tool | Purpose |
|------|---------|
| **pnpm** | Fast, disk-space efficient package manager |
| **pnpm workspaces** | Monorepo management |
| **Docker Compose** | Local development environment orchestration |
| **ESLint** | JavaScript/TypeScript linting |
| **Prettier** | Code formatting |
| **mypy** | Python static type checking |
| **flake8** | Python linting |
| **Black** | Python code formatting |

### Deployment Stack

| Component | Platform | Purpose |
|-----------|----------|---------|
| **Frontend Hosting** | Vercel | Static site hosting with edge functions |
| **Backend Hosting** | Railway | Container hosting with auto-scaling |
| **Database Hosting** | Neon | Serverless PostgreSQL |
| **CI/CD** | GitHub Actions | Automated testing and deployment |
| **Monitoring** | Vercel Analytics, Railway Logs | Performance and error tracking |

---

## Feature List

### Core Todo Features

#### Task Management (CRUD Operations)

- **Create Tasks**: Add new todo items with titles (1-200 characters)
- **Read Tasks**: View all tasks with ID, title, completion status, timestamps
- **Update Tasks**: Edit task titles and toggle completion status
- **Delete Tasks**: Permanently remove tasks from the system

**Validation Rules**:
- Task titles must be non-empty after trimming whitespace
- Task titles limited to 200 characters
- Tasks must belong to authenticated user (user isolation)

#### Task Operations

- **Mark Complete/Incomplete**: Toggle task completion status
- **Filter Tasks**: View all, completed only, or incomplete only
- **Sort Tasks**: By creation date, title, or completion status
- **Search Tasks**: Filter by title substring (case-insensitive)

### User Management Features

#### Authentication

- **User Registration**: Create new account with email and password
  - Email validation (format and uniqueness)
  - Password strength requirements (min 8 characters, complexity rules)
  - Automatic login after registration

- **User Login**: Authenticate with email and password
  - JWT token issued on successful login
  - httpOnly cookie for token storage
  - Remember me option (extended session)

- **User Logout**: Invalidate session and clear tokens
  - Client-side token removal
  - Server-side session invalidation (if using Redis)

- **Password Reset**: (Future enhancement)
  - Email-based password reset flow
  - Secure token generation

#### Authorization

- **User Isolation**: Each user can only access their own tasks
  - Database queries filtered by user_id
  - API endpoints validate ownership
  - Frontend hides other users' data

#### Session Management

- **Session Persistence**: User remains logged in across browser sessions
- **Session Expiry**: Automatic logout after token expiration
- **Session Refresh**: Token refresh for extended sessions

### User Interface Features

#### Pages

1. **Home Page** (`/`): Landing page with login/register CTAs
2. **Login Page** (`/auth/login`): User authentication form
3. **Register Page** (`/auth/register`): New user registration form
4. **Dashboard** (`/dashboard`): Task list with CRUD operations (protected route)
5. **404 Page**: Custom not-found page

#### Components

- **Task List**: Display all tasks with completion toggles
- **Task Form**: Create and edit tasks
- **Task Item**: Individual task display with actions
- **Filter Controls**: Filter and sort task list
- **Navigation Bar**: App navigation with user menu
- **Authentication Forms**: Login and registration forms
- **Loading States**: Skeleton screens and spinners
- **Error States**: User-friendly error messages
- **Empty States**: Helpful messages when no tasks exist

#### UI/UX Features

- **Responsive Design**: Mobile-first, adapts to tablet/desktop
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: ARIA labels and semantic HTML
- **Focus Management**: Logical tab order, focus indicators
- **Optimistic Updates**: Instant UI feedback before API confirmation
- **Error Recovery**: Rollback on API failures
- **Loading Indicators**: Visual feedback for async operations
- **Toast Notifications**: Success/error messages

### API Features

#### REST Endpoints

**Tasks API** (`/api/tasks`):
- `GET /api/tasks` - List all tasks (with optional filters)
- `POST /api/tasks` - Create new task
- `GET /api/tasks/:id` - Get single task
- `PUT /api/tasks/:id` - Update task
- `PATCH /api/tasks/:id/complete` - Toggle completion
- `DELETE /api/tasks/:id` - Delete task

**Auth API** (`/api/auth`):
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Authenticate user
- `POST /api/auth/logout` - End user session
- `GET /api/auth/me` - Get current user profile

#### API Features

- **OpenAPI Documentation**: Auto-generated Swagger UI at `/docs`
- **Request Validation**: Pydantic schemas validate all inputs
- **Response Schemas**: Consistent response structure
- **Error Handling**: Standard error format with codes and messages
- **CORS Configuration**: Secure cross-origin requests
- **Rate Limiting**: (Future enhancement) Prevent abuse
- **API Versioning**: `/api/v1/` prefix for future compatibility

### Database Features

#### Schema

**Users Table**:
- `id` (UUID, primary key)
- `email` (string, unique, indexed)
- `password_hash` (string)
- `created_at` (timestamp)
- `updated_at` (timestamp)

**Tasks Table**:
- `id` (integer, primary key, auto-increment)
- `title` (string, max 200 chars)
- `is_complete` (boolean, default false)
- `user_id` (UUID, foreign key → users.id)
- `created_at` (timestamp)
- `updated_at` (timestamp)

#### Database Operations

- **Migrations**: Alembic for schema versioning
- **Indexes**: On user_id, email, created_at for query performance
- **Constraints**: Foreign keys, unique constraints, not-null constraints
- **Transactions**: ACID compliance for data integrity

### Development Features

- **Hot Reload**: Instant updates during development
- **Type Checking**: TypeScript + mypy for type safety
- **Linting**: ESLint + flake8 for code quality
- **Formatting**: Prettier + Black for consistent style
- **Testing**: Unit, integration, and E2E test suites
- **Debugging**: Source maps, debug configurations

### Deployment Features

- **Environment Configuration**: Separate dev/staging/production configs
- **Secret Management**: Environment variables for sensitive data
- **Health Checks**: `/health` endpoint for monitoring
- **Logging**: Structured logs for debugging
- **Monitoring**: Performance and error tracking
- **CI/CD**: Automated testing and deployment

---

## Architecture Overview

### Monorepo Structure

The project uses a **monorepo** structure with workspaces for shared dependencies and coordinated development:

```
hackathon-ii-evolution-todo/
├── apps/
│   ├── frontend/         # Next.js application
│   └── backend/          # FastAPI application
├── packages/             # Shared packages (optional)
│   └── shared-types/     # Shared TypeScript types
├── specs/                # Feature specifications
├── history/              # ADRs and PHRs
├── .claude/              # AI agent configurations
├── .specify/             # SpecKit Plus configuration
└── docker-compose.yml    # Local development environment
```

### Three-Layer Architecture

The application maintains a clean **three-layer architecture** from Phase I, now distributed across frontend and backend:

```
┌─────────────────────────────────────────────────────────────┐
│                     Presentation Layer                       │
│  (Next.js: React Components, Pages, Client-Side Logic)      │
└─────────────────────────────────────────────────────────────┘
                            ↕ REST API
┌─────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                    │
│  (FastAPI: Endpoints, Services, Validation, Auth)           │
└─────────────────────────────────────────────────────────────┘
                            ↕ SQLModel ORM
┌─────────────────────────────────────────────────────────────┐
│                      Data Access Layer                       │
│  (PostgreSQL: Tables, Constraints, Indexes)                  │
└─────────────────────────────────────────────────────────────┘
```

### Component Architecture

#### Frontend Architecture

```
apps/frontend/
├── app/
│   ├── api/              # Backend-for-Frontend (BFF) routes
│   │   └── proxy/        # API proxy to backend
│   ├── components/       # React components
│   │   ├── ui/           # Reusable UI components
│   │   ├── tasks/        # Task-specific components
│   │   └── auth/         # Auth-related components
│   ├── hooks/            # Custom React hooks
│   │   ├── useTasks.ts   # Task data fetching
│   │   └── useAuth.ts    # Authentication state
│   ├── types/            # TypeScript type definitions
│   ├── lib/              # Utility functions
│   │   ├── api.ts        # API client
│   │   └── auth.ts       # Auth utilities
│   ├── layout.tsx        # Root layout (navigation, providers)
│   └── page.tsx          # Home page
└── tests/e2e/            # Playwright E2E tests
```

**Frontend Patterns**:
- **Server Components**: Default for static content and data fetching
- **Client Components**: For interactive UI (forms, buttons with state)
- **API Routes**: BFF pattern for server-side API calls
- **Custom Hooks**: Encapsulate data fetching and state logic
- **Component Composition**: Small, reusable components

#### Backend Architecture

```
apps/backend/
├── app/
│   ├── api/
│   │   └── routes/       # API endpoint handlers
│   │       ├── tasks.py  # Task CRUD endpoints
│   │       └── auth.py   # Authentication endpoints
│   ├── core/             # Core configuration
│   │   ├── config.py     # App settings (from env)
│   │   ├── database.py   # Database connection
│   │   └── security.py   # JWT utilities
│   ├── models/           # SQLModel database models
│   │   ├── user.py       # User model
│   │   └── task.py       # Task model
│   ├── schemas/          # Pydantic request/response schemas
│   │   ├── user.py       # User DTOs
│   │   └── task.py       # Task DTOs
│   ├── services/         # Business logic services
│   │   ├── task_service.py   # Task operations
│   │   └── auth_service.py   # Auth operations
│   └── main.py           # FastAPI app initialization
├── alembic/              # Database migrations
│   └── versions/         # Migration files
└── tests/
    ├── unit/             # Unit tests for services
    └── integration/      # API integration tests
```

**Backend Patterns**:
- **Layered Architecture**: Routes → Services → Models
- **Dependency Injection**: FastAPI dependencies for auth, DB
- **Repository Pattern**: Service layer abstracts data access
- **DTO Pattern**: Pydantic schemas separate API contracts from DB models
- **Middleware**: CORS, authentication, error handling

### API-First Design

The backend exposes a **REST API** that serves as the contract between frontend and backend:

- **OpenAPI Specification**: Auto-generated from FastAPI code
- **Type-Safe Contracts**: Pydantic schemas ensure validation
- **Versioned Endpoints**: `/api/v1/` prefix for future compatibility
- **Standard HTTP Methods**: GET, POST, PUT, PATCH, DELETE
- **Consistent Response Format**: Success and error responses

### Database Design

**Entity-Relationship Model**:

```
┌─────────────────┐         ┌─────────────────┐
│     Users       │         │     Tasks       │
├─────────────────┤         ├─────────────────┤
│ id (UUID) PK    │────┐    │ id (int) PK     │
│ email           │    │    │ title           │
│ password_hash   │    │    │ is_complete     │
│ created_at      │    └───→│ user_id (FK)    │
│ updated_at      │         │ created_at      │
└─────────────────┘         │ updated_at      │
                            └─────────────────┘
```

**Key Design Decisions**:
- **User IDs**: UUIDs for security (prevents enumeration)
- **Task IDs**: Auto-incrementing integers for simplicity
- **Timestamps**: Track creation and modification times
- **Indexes**: On foreign keys and frequently queried columns

### Security Architecture

**Authentication Flow**:

```
1. User submits credentials → Backend validates
2. Backend generates JWT → Returns httpOnly cookie
3. Frontend stores cookie → Browser sends automatically
4. Backend validates JWT → Extracts user_id
5. Backend filters data by user_id → Returns user-specific data
```

**Security Measures**:
- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: Signed with secret key, includes expiry
- **httpOnly Cookies**: Prevents XSS attacks
- **CORS Configuration**: Restricts API access to frontend origin
- **Input Validation**: Pydantic schemas sanitize inputs
- **SQL Injection Prevention**: SQLModel parameterized queries
- **Rate Limiting**: (Future) Prevent brute-force attacks

### Deployment Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    User's Browser                        │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ↓ HTTPS
┌──────────────────────────────────────────────────────────┐
│                  Vercel Edge Network                     │
│              (Next.js Frontend Hosting)                  │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ↓ HTTPS REST API
┌──────────────────────────────────────────────────────────┐
│                    Railway Container                     │
│               (FastAPI Backend Hosting)                  │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ↓ PostgreSQL Protocol
┌──────────────────────────────────────────────────────────┐
│                   Neon PostgreSQL                        │
│            (Serverless Database Hosting)                 │
└──────────────────────────────────────────────────────────┘
```

---

## Development Approach

### Spec-Driven Development (SDD)

This project strictly follows **Spec-Driven Development** as defined in the project constitution:

> "All code MUST be generated from specifications using Claude Code; no manual coding is allowed."

#### SpecKit Plus Workflow

Every feature follows this structured workflow:

```
1. /sp.specify   → Create spec.md (requirements, acceptance criteria)
2. /sp.plan      → Generate plan.md (architecture, technical design)
3. /sp.tasks     → Create tasks.md (atomic implementation tasks)
4. /sp.implement → Execute tasks with AI agents
5. /sp.adr       → Document architectural decisions (when needed)
```

#### Specification Structure

Each feature has three core documents in `specs/phase-2-todo-web/`:

**1. spec.md** - Requirements Specification
- User stories with acceptance scenarios
- Business rules and validation logic
- Edge cases and error handling
- Non-functional requirements (performance, security)

**2. plan.md** - Architecture Plan
- Technical design and component architecture
- API contracts and database schema
- Technology choices and justifications
- Performance targets and optimization strategies

**3. tasks.md** - Task Breakdown
- Atomic, testable implementation tasks
- Task dependencies and ordering
- Acceptance criteria per task
- Test cases for validation

### Test-First Development (TDD)

Following the project constitution:

> "TDD is mandatory; write failing tests first (Red), implement to pass (Green), then refactor."

#### TDD Cycle

```
┌─────────────┐
│  RED        │  Write failing test
│  ↓          │
│  GREEN      │  Implement minimal code to pass
│  ↓          │
│  REFACTOR   │  Improve code quality
└─────────────┘
```

#### Test Coverage Targets

| Layer | Target Coverage | Test Types |
|-------|----------------|------------|
| **Frontend** | >80% | Unit (Jest), E2E (Playwright) |
| **Backend** | >80% | Unit (Pytest), Integration (httpx) |
| **API** | 100% | Integration tests for all endpoints |

### AI-Assisted Coding

The project uses **specialized AI agents** for different development concerns:

#### Available Agents

1. **nextjs-frontend-developer** (`.claude/agents/nextjs-frontend-developer.md`)
   - React component implementation
   - Next.js page and API route creation
   - Tailwind CSS styling
   - Frontend state management (SWR)

2. **fastapi-backend-developer** (`.claude/agents/fastapi-backend-developer.md`)
   - REST API endpoint implementation
   - Pydantic schema creation
   - SQLModel integration
   - Business logic services

3. **database-architect** (`.claude/agents/database-architect.md`)
   - Database schema design
   - Alembic migrations
   - Index and constraint optimization
   - Query performance tuning

4. **auth-security-guardian** (`.claude/agents/auth-security-guardian.md`)
   - Authentication implementation (Better Auth)
   - JWT token management
   - Security best practices
   - CORS and security headers

5. **integration-testing-agent** (`.claude/agents/integration-testing-agent.md`)
   - Playwright E2E tests
   - API integration tests
   - Database testing utilities

#### Agent Coordination

Agents work together following a **layered handoff pattern**:

```
database-architect → fastapi-backend-developer → nextjs-frontend-developer
                              ↓
                   integration-testing-agent
                              ↑
                   auth-security-guardian (cross-cutting)
```

### Code Quality Standards

Following the project constitution:

#### Python Standards

- **PEP 8 Compliance**: Enforced by flake8
- **Type Hints**: Required for all function signatures
- **Docstrings**: Mandatory for all public functions/classes
- **Type Checking**: mypy with strict mode
- **Formatting**: Black (88-character line length)

#### TypeScript Standards

- **Strict Mode**: Enabled in tsconfig.json
- **ESLint Rules**: Enforced via pre-commit hooks
- **Prettier Formatting**: Consistent code style
- **JSDoc Comments**: For complex functions
- **Type Imports**: Explicit `import type` statements

#### Testing Standards

- **Given-When-Then**: BDD-style test descriptions
- **Arrange-Act-Assert**: Unit test structure
- **Test Isolation**: No shared state between tests
- **Realistic Data**: Fixtures and factories for test data
- **Comprehensive Coverage**: Happy paths + edge cases + error scenarios

### Version Control Practices

- **Feature Branches**: One branch per feature (e.g., `002-user-authentication`)
- **Conventional Commits**: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
- **Pull Requests**: Required for all merges to main
- **Code Review**: AI agent validates against specs
- **CI/CD**: Automated testing on every push

### Documentation Practices

Every code artifact references its specification:

```typescript
// Implementation follows spec.md section 3.2: Task Creation Validation
export function validateTaskTitle(title: string): boolean {
  // Spec requirement: Title must be 1-200 characters
  return title.trim().length >= 1 && title.length <= 200;
}
```

---

## Project Structure

### Root Directory

```
hackathon-ii-evolution-todo/
├── .claude/                        # AI Agent Configurations
│   ├── agents/                     # Specialized agents
│   │   ├── nextjs-frontend-developer.md
│   │   ├── fastapi-backend-developer.md
│   │   ├── database-architect.md
│   │   ├── auth-security-guardian.md
│   │   └── integration-testing-agent.md
│   ├── commands/                   # SpecKit Plus commands
│   │   ├── sp.specify.md          # Create specifications
│   │   ├── sp.plan.md             # Generate architecture plans
│   │   ├── sp.tasks.md            # Break down into tasks
│   │   ├── sp.implement.md        # Execute implementation
│   │   └── sp.adr.md              # Document decisions
│   └── skills/
│       └── skills.md              # Phase II implementation skills
│
├── .specify/                       # SpecKit Plus Configuration
│   ├── memory/
│   │   └── constitution.md        # Project principles & standards
│   ├── templates/                 # Spec/Plan/Task templates
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   └── tasks-template.md
│   └── scripts/                   # Automation scripts
│
├── specs/                          # Feature Specifications
│   ├── overview.md                # This file - project overview
│   ├── phase-1-todo-app/          # Phase I specs (reference)
│   │   ├── spec.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   └── checklist.md
│   └── phase-2-todo-web/          # Phase II specs (active)
│       ├── README.md              # Spec structure guide
│       ├── spec.md                # Main feature spec
│       ├── plan.md                # Architecture plan
│       ├── tasks.md               # Task breakdown
│       ├── features/              # Feature-specific specs
│       │   ├── task-management.md
│       │   ├── user-authentication.md
│       │   └── task-filtering.md
│       ├── api/                   # API endpoint specs
│       │   ├── tasks-api.md
│       │   └── auth-api.md
│       ├── database/              # Schema & migration specs
│       │   ├── users-schema.md
│       │   ├── tasks-schema.md
│       │   └── migrations.md
│       └── ui/                    # Component & UX specs
│           ├── task-list-page.md
│           ├── task-form.md
│           └── auth-pages.md
│
├── history/                        # Project History
│   ├── prompts/                   # Prompt History Records (PHRs)
│   │   ├── constitution/          # Constitution creation PHRs
│   │   ├── phase-1-todo-app/      # Phase I development PHRs
│   │   ├── phase-2-todo-web/      # Phase II development PHRs
│   │   └── general/               # General project PHRs
│   └── adr/                       # Architecture Decision Records
│       ├── 001-dictionary-task-storage.md
│       ├── 002-exception-based-error-handling.md
│       ├── 003-integer-id-generation.md
│       └── 004-three-layer-architecture.md
│
├── apps/                           # Application Services
│   ├── frontend/                  # Next.js Application
│   │   ├── app/                   # Next.js App Router
│   │   │   ├── api/              # Backend-for-Frontend (BFF)
│   │   │   ├── components/       # React components
│   │   │   ├── hooks/            # Custom React hooks
│   │   │   ├── types/            # TypeScript types
│   │   │   ├── lib/              # Utility functions
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── public/               # Static assets
│   │   ├── tests/
│   │   │   ├── unit/             # Jest unit tests
│   │   │   └── e2e/              # Playwright E2E tests
│   │   ├── .env.example
│   │   ├── .env.local
│   │   ├── CLAUDE.md             # Frontend-specific guidelines
│   │   ├── package.json
│   │   ├── next.config.js
│   │   ├── tsconfig.json
│   │   ├── tailwind.config.ts
│   │   └── playwright.config.ts
│   │
│   └── backend/                   # FastAPI Application
│       ├── app/
│       │   ├── api/
│       │   │   └── routes/       # API endpoints
│       │   ├── core/             # Config, DB, security
│       │   ├── models/           # SQLModel schemas
│       │   ├── services/         # Business logic
│       │   ├── schemas/          # Pydantic schemas
│       │   └── main.py
│       ├── alembic/              # Database migrations
│       │   ├── versions/         # Migration files
│       │   └── env.py
│       ├── tests/
│       │   ├── unit/             # Pytest unit tests
│       │   ├── integration/      # API integration tests
│       │   └── conftest.py       # Test fixtures
│       ├── .env.example
│       ├── .env
│       ├── CLAUDE.md             # Backend-specific guidelines
│       ├── pyproject.toml        # Poetry dependencies
│       ├── alembic.ini           # Alembic config
│       └── Dockerfile            # Container definition
│
├── packages/                       # Shared Packages (optional)
│   └── shared-types/
│       ├── src/
│       │   └── index.ts
│       ├── package.json
│       └── tsconfig.json
│
├── docker-compose.yml             # Local development services
├── vercel.json                    # Frontend deployment config
├── railway.json                   # Backend deployment config
├── package.json                   # Workspace root
├── pnpm-workspace.yaml            # Workspace configuration
├── .gitignore                     # Git ignore rules
├── CLAUDE.md                      # Main project guide (AI instructions)
└── README.md                      # User-facing documentation
```

### Key Directories Explained

#### `.claude/` - AI Agent Configurations

Contains specialized agent definitions and skills for AI-assisted development:
- **agents/**: AI agent prompts for different roles
- **commands/**: SpecKit Plus slash commands
- **skills/**: Reusable implementation patterns

#### `.specify/` - SpecKit Plus Configuration

SpecKit Plus framework configuration:
- **memory/constitution.md**: Project principles and standards
- **templates/**: Templates for specs, plans, tasks
- **scripts/**: Automation utilities

#### `specs/` - Feature Specifications

All project specifications organized by phase:
- **overview.md**: This file - entry point for understanding the project
- **phase-1-todo-app/**: Phase I reference specs
- **phase-2-todo-web/**: Phase II active specs with subdirectories for features, API, database, UI

#### `history/` - Project History

Permanent record of decisions and development:
- **prompts/**: PHRs documenting AI conversations
- **adr/**: Architectural Decision Records

#### `apps/` - Application Code

Monorepo applications:
- **frontend/**: Next.js web application
- **backend/**: FastAPI REST API

#### `packages/` - Shared Code

Optional shared packages (e.g., TypeScript types shared between frontend and backend)

---

## Getting Started

### Prerequisites

Ensure you have the following installed:

- **Node.js**: 18.x or higher
- **pnpm**: 8.x or higher (`npm install -g pnpm`)
- **Python**: 3.11 or higher
- **Poetry**: Latest version (for Python dependency management)
- **Docker**: Latest version (for local development environment)
- **Git**: For version control

### Initial Setup

#### 1. Clone Repository

```bash
git clone <repository-url>
cd hackathon-ii-evolution-todo
```

#### 2. Install Dependencies

**Install all workspace dependencies**:
```bash
pnpm install
```

This installs:
- Root workspace dependencies
- Frontend dependencies (`apps/frontend/`)
- Shared package dependencies (`packages/*/`)

**Install backend dependencies**:
```bash
cd apps/backend
poetry install
cd ../..
```

#### 3. Environment Configuration

**Frontend** (`apps/frontend/.env.local`):
```bash
cp apps/frontend/.env.example apps/frontend/.env.local
# Edit .env.local with your values
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend** (`apps/backend/.env`):
```bash
cp apps/backend/.env.example apps/backend/.env
# Edit .env with your values
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
API_SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:3000"]
```

#### 4. Start Local Development Environment

**Option A: Docker Compose (Recommended)**

Starts all services (PostgreSQL, backend, frontend):
```bash
docker-compose up
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Option B: Manual Start**

Start services individually:

```bash
# Terminal 1: Start PostgreSQL (if not using Docker)
# (Use your local PostgreSQL installation or Docker)

# Terminal 2: Start backend
cd apps/backend
poetry run uvicorn app.main:app --reload
# Running on http://localhost:8000

# Terminal 3: Start frontend
cd apps/frontend
pnpm dev
# Running on http://localhost:3000
```

#### 5. Run Database Migrations

```bash
cd apps/backend
poetry run alembic upgrade head
```

### Development Workflow

#### For New Features

1. **Navigate to specs directory**:
   ```bash
   cd specs/phase-2-todo-web
   ```

2. **Create specification**:
   ```bash
   /sp.specify
   ```
   Follow prompts to generate `spec.md`

3. **Generate architecture plan**:
   ```bash
   /sp.plan
   ```
   Generates `plan.md` from `spec.md`

4. **Break down into tasks**:
   ```bash
   /sp.tasks
   ```
   Generates `tasks.md` with implementation tasks

5. **Implement tasks**:
   ```bash
   /sp.implement
   ```
   Executes tasks using specialized agents

6. **Run tests**:
   ```bash
   # Frontend tests
   cd apps/frontend
   pnpm test              # Unit tests
   pnpm test:e2e          # E2E tests

   # Backend tests
   cd apps/backend
   poetry run pytest      # All tests
   poetry run pytest --cov=app  # With coverage
   ```

7. **Document decisions** (if needed):
   ```bash
   /sp.adr <decision-title>
   ```
   Creates ADR in `history/adr/`

### Testing

#### Frontend Testing

```bash
cd apps/frontend

# Unit tests (Jest + React Testing Library)
pnpm test
pnpm test:watch        # Watch mode
pnpm test:coverage     # With coverage

# E2E tests (Playwright)
pnpm test:e2e
pnpm test:e2e:ui       # Interactive UI mode

# Type checking
pnpm type-check

# Linting
pnpm lint
pnpm lint:fix          # Auto-fix issues
```

#### Backend Testing

```bash
cd apps/backend

# Unit tests
poetry run pytest tests/unit

# Integration tests
poetry run pytest tests/integration

# All tests with coverage
poetry run pytest --cov=app --cov-report=html

# Type checking
poetry run mypy app

# Linting
poetry run flake8 app
```

### Building

#### Frontend

```bash
cd apps/frontend
pnpm build              # Production build
pnpm start              # Serve production build
```

#### Backend

```bash
cd apps/backend
poetry build            # Build package
```

### Deployment

#### Frontend (Vercel)

```bash
cd apps/frontend
vercel --prod
```

Set environment variables in Vercel dashboard:
- `NEXT_PUBLIC_API_URL`: Your backend URL (Railway)

#### Backend (Railway)

```bash
cd apps/backend
railway up
```

Set environment variables in Railway dashboard:
- `DATABASE_URL`: Neon connection string
- `API_SECRET_KEY`: 32+ character secret
- `CORS_ORIGINS`: Frontend URL (Vercel)

#### Database (Neon)

1. Create project at https://neon.tech
2. Copy connection string
3. Add to Railway environment variables
4. Run migrations:
   ```bash
   railway run poetry run alembic upgrade head
   ```

---

## Cross-References

### Core Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| **Project Overview** | `/specs/overview.md` | This file - comprehensive project guide |
| **Main Instructions** | `/CLAUDE.md` | AI agent instructions and development guide |
| **Constitution** | `/.specify/memory/constitution.md` | Project principles and standards |
| **User Documentation** | `/README.md` | User-facing project documentation |

### Phase I Reference

| Document | Location | Purpose |
|----------|----------|---------|
| **Phase I Spec** | `/specs/phase-1-todo-app/spec.md` | Console app requirements |
| **Phase I Plan** | `/specs/phase-1-todo-app/plan.md` | Console app architecture |
| **Phase I Tasks** | `/specs/phase-1-todo-app/tasks.md` | Console app implementation tasks |
| **Phase I Checklist** | `/specs/phase-1-todo-app/checklist.md` | Feature completion checklist |

### Phase II Specifications

| Document | Location | Purpose |
|----------|----------|---------|
| **Phase II Spec** | `/specs/phase-2-todo-web/spec.md` | Web app requirements (pending) |
| **Phase II Plan** | `/specs/phase-2-todo-web/plan.md` | Web app architecture (pending) |
| **Phase II Tasks** | `/specs/phase-2-todo-web/tasks.md` | Web app implementation tasks (pending) |
| **Spec Structure Guide** | `/specs/phase-2-todo-web/README.md` | How to organize Phase II specs |

### Feature Specifications (To Be Created)

| Document | Location | Purpose |
|----------|----------|---------|
| **Task Management** | `/specs/phase-2-todo-web/features/task-management.md` | Task CRUD feature spec |
| **User Authentication** | `/specs/phase-2-todo-web/features/user-authentication.md` | Auth feature spec |
| **Task Filtering** | `/specs/phase-2-todo-web/features/task-filtering.md` | Filter/sort feature spec |

### API Specifications (To Be Created)

| Document | Location | Purpose |
|----------|----------|---------|
| **Tasks API** | `/specs/phase-2-todo-web/api/tasks-api.md` | Task endpoints specification |
| **Auth API** | `/specs/phase-2-todo-web/api/auth-api.md` | Authentication endpoints |

### Database Specifications (To Be Created)

| Document | Location | Purpose |
|----------|----------|---------|
| **Users Schema** | `/specs/phase-2-todo-web/database/users-schema.md` | Users table definition |
| **Tasks Schema** | `/specs/phase-2-todo-web/database/tasks-schema.md` | Tasks table definition |
| **Migrations** | `/specs/phase-2-todo-web/database/migrations.md` | Migration strategy |

### UI Specifications (To Be Created)

| Document | Location | Purpose |
|----------|----------|---------|
| **Task List Page** | `/specs/phase-2-todo-web/ui/task-list-page.md` | Dashboard page spec |
| **Task Form** | `/specs/phase-2-todo-web/ui/task-form.md` | Task create/edit form |
| **Auth Pages** | `/specs/phase-2-todo-web/ui/auth-pages.md` | Login/register pages |

### Agent Configurations

| Document | Location | Purpose |
|----------|----------|---------|
| **Frontend Agent** | `/.claude/agents/nextjs-frontend-developer.md` | Next.js development agent |
| **Backend Agent** | `/.claude/agents/fastapi-backend-developer.md` | FastAPI development agent |
| **Database Agent** | `/.claude/agents/database-architect.md` | Database design agent |
| **Security Agent** | `/.claude/agents/auth-security-guardian.md` | Authentication agent |
| **Testing Agent** | `/.claude/agents/integration-testing-agent.md` | E2E testing agent |

### Implementation Skills

| Document | Location | Purpose |
|----------|----------|---------|
| **Skills Reference** | `/.claude/skills/skills.md` | All implementation patterns |

### Application-Specific Guides

| Document | Location | Purpose |
|----------|----------|---------|
| **Frontend Guide** | `/apps/frontend/CLAUDE.md` | Frontend-specific patterns |
| **Backend Guide** | `/apps/backend/CLAUDE.md` | Backend-specific patterns |

### Architectural Decisions

| Document | Location | Purpose |
|----------|----------|---------|
| **ADR-001** | `/history/adr/001-dictionary-task-storage.md` | Dictionary storage decision |
| **ADR-002** | `/history/adr/002-exception-based-error-handling.md` | Exception handling |
| **ADR-003** | `/history/adr/003-integer-id-generation.md` | ID generation strategy |
| **ADR-004** | `/history/adr/004-three-layer-architecture.md` | Architectural layers |

### External Documentation

| Resource | URL | Purpose |
|----------|-----|---------|
| **Next.js Docs** | https://nextjs.org/docs | Next.js framework reference |
| **FastAPI Docs** | https://fastapi.tiangolo.com | FastAPI framework reference |
| **SQLModel Docs** | https://sqlmodel.tiangolo.com | SQLModel ORM reference |
| **Better Auth Docs** | https://www.better-auth.com | Authentication library |
| **Neon Docs** | https://neon.tech/docs | Database platform |
| **Vercel Docs** | https://vercel.com/docs | Frontend deployment |
| **Railway Docs** | https://docs.railway.app | Backend deployment |
| **Playwright Docs** | https://playwright.dev | E2E testing framework |

---

## Next Steps

### Immediate Actions

1. **Create Main Specification**:
   ```bash
   cd specs/phase-2-todo-web
   /sp.specify
   ```

2. **Generate Architecture Plan**:
   ```bash
   /sp.plan
   ```

3. **Break Down Tasks**:
   ```bash
   /sp.tasks
   ```

4. **Begin Implementation**:
   ```bash
   /sp.implement
   ```

### Recommended Reading Order

For new team members or contributors:

1. Read this file (`specs/overview.md`) - comprehensive project overview
2. Read `/CLAUDE.md` - development workflow and commands
3. Read `/.specify/memory/constitution.md` - project principles
4. Read `/specs/phase-1-todo-app/spec.md` - understand Phase I foundation
5. Read `/specs/phase-2-todo-web/README.md` - Phase II spec structure
6. Read relevant agent configurations in `/.claude/agents/`
7. Explore implementation skills in `/.claude/skills/skills.md`

### Development Path

Follow this path for feature development:

```
Specification → Planning → Task Breakdown → Implementation → Testing → Documentation
```

Each step uses SpecKit Plus commands:
- `/sp.specify` → `/sp.plan` → `/sp.tasks` → `/sp.implement` → `/sp.adr`

---

## Summary

The **Evolution of Todo - Phase II** project demonstrates:

- **Spec-Driven Development**: All code generated from clear specifications
- **AI-Assisted Coding**: Specialized agents for different concerns
- **Test-First Development**: TDD with comprehensive coverage
- **Clean Architecture**: Separation of concerns across layers
- **Evolutionary Design**: Building on Phase I foundations
- **Production-Ready Quality**: Security, performance, accessibility

**Current Status**: Specification & Planning Stage

**Next Milestone**: Complete main specification, architecture plan, and task breakdown

**Goal**: Build a production-ready full-stack web todo application that serves as a comprehensive case study for modern software development practices.

---

**Built with Spec-Driven Development**
**Powered by Claude Code + SpecKit Plus**

For questions, reference:
- Constitution: `/.specify/memory/constitution.md`
- Main Guide: `/CLAUDE.md`
- Agents: `/.claude/agents/`
- Skills: `/.claude/skills/skills.md`
- This Overview: `/specs/overview.md`
