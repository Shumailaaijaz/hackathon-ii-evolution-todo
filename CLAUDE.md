# Evolution of Todo - Phase II: Full-Stack Web Application

> **Spec-Driven Development with AI-Assisted Coding**
> Building a production-ready todo application using Next.js + FastAPI + PostgreSQL

---

## 🎯 Project Overview

This is **Phase II** of the "Evolution of Todo" hackathon project. We're transforming the Phase I console application into a full-stack web system with:

- **Frontend**: Next.js 14+ (React, TypeScript, Tailwind CSS)
- **Backend**: FastAPI (Python 3.11+, SQLModel, Pydantic)
- **Database**: PostgreSQL (Neon serverless)
- **Deployment**: Vercel (frontend) + Railway (backend)
- **Architecture**: Monorepo with workspace management

### Phase I → Phase II Evolution
Phase II **builds upon** Phase I foundations by:
1. ✅ Adding web UI (Next.js with React)
2. ✅ Exposing REST API (FastAPI)
3. ✅ Adding persistence (PostgreSQL)
4. ✅ Containerizing services (Docker Compose)
5. ✅ Deploying to production (Vercel + Railway)

**Core business logic from Phase I is preserved and extended**, not rewritten.

---

## 📁 Monorepo Structure

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
│   │   └── sp.adr.md              # Document decisions
│   └── skills/
│       └── skills.md              # Phase II implementation skills
│
├── .specify/                       # SpecKit Plus Configuration
│   ├── memory/
│   │   └── constitution.md        # Project principles & standards
│   ├── templates/                 # Spec/Plan/Task templates
│   └── scripts/                   # Automation scripts
│
├── specs/                          # Feature Specifications
│   ├── phase-1-todo-app/          # Phase I specs (reference)
│   │   ├── spec.md
│   │   ├── plan.md
│   │   └── tasks.md
│   └── phase-2-todo-web/          # Phase II specs (active)
│       ├── README.md              # Spec structure guide
│       ├── spec.md                # Main feature spec
│       ├── plan.md                # Architecture plan
│       ├── tasks.md               # Task breakdown
│       ├── features/              # Feature-specific specs
│       ├── api/                   # API endpoint specs
│       ├── database/              # Schema & migration specs
│       └── ui/                    # Component & UX specs
│
├── history/                        # Project History
│   ├── prompts/                   # Prompt History Records (PHRs)
│   │   ├── constitution/
│   │   ├── phase-1-todo-app/
│   │   ├── phase-2-todo-web/
│   │   └── general/
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
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── tests/
│   │   │   └── e2e/              # Playwright E2E tests
│   │   ├── .env.example
│   │   ├── .env.local
│   │   ├── CLAUDE.md             # Frontend-specific guidelines
│   │   ├── package.json
│   │   ├── next.config.js
│   │   ├── tsconfig.json
│   │   └── tailwind.config.ts
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
│       ├── tests/
│       │   ├── unit/
│       │   └── integration/
│       ├── .env.example
│       ├── .env
│       ├── CLAUDE.md             # Backend-specific guidelines
│       ├── pyproject.toml
│       └── alembic.ini
│
├── packages/                       # Shared Packages (optional)
│   └── shared-types/
│       ├── src/
│       └── package.json
│
├── docker-compose.yml             # Local development services
├── vercel.json                    # Frontend deployment config
├── railway.json                   # Backend deployment config
├── package.json                   # Workspace root
├── CLAUDE.md                      # This file
└── README.md                      # User-facing documentation
```

---

## 📖 How to Reference Specifications

### SpecKit Plus Structure

This project uses **SpecKit Plus** for Spec-Driven Development. All features follow this workflow:

1. **Specification** (`specs/<feature>/spec.md`) - Requirements & acceptance criteria
2. **Architecture Plan** (`specs/<feature>/plan.md`) - Technical design & decisions
3. **Task Breakdown** (`specs/<feature>/tasks.md`) - Implementable tasks with test cases
4. **Prompt History** (`history/prompts/<feature>/`) - Development conversation records
5. **ADRs** (`history/adr/`) - Architectural decision records

### Referencing Specs in Code

When implementing features, **always reference the spec**:

```typescript
// ✅ GOOD: Clear spec reference
// Implementation follows spec.md section 3.2: Task Creation Validation
export function validateTaskTitle(title: string): boolean {
  // Spec requirement: Title must be 1-200 characters
  return title.trim().length >= 1 && title.length <= 200;
}
```

```python
# ✅ GOOD: Clear spec reference
# Implements plan.md Section 4.1: REST API Design
@router.post("/api/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate):
    """
    Create new task.

    Spec: specs/phase-2-todo-web/api/tasks-api.md
    Plan: specs/phase-2-todo-web/plan.md (Section 4.1)
    """
```

### Finding Relevant Specs

```bash
# List all Phase II specs
ls specs/phase-2-todo-web/

# View main specification
cat specs/phase-2-todo-web/spec.md

# Check API endpoint specs
cat specs/phase-2-todo-web/api/tasks-api.md

# Review database schema
cat specs/phase-2-todo-web/database/tasks-schema.md

# Check UI components
cat specs/phase-2-todo-web/ui/task-list-page.md
```

---

## 🔄 Development Workflow

### Step 1: Create Specification

Navigate to the feature directory and run:

```bash
cd specs/phase-2-todo-web
/sp.specify
```

This launches the **spec-generator agent** to create `spec.md` with:
- User stories
- Acceptance criteria
- Validation rules
- Business logic
- Edge cases

### Step 2: Generate Architecture Plan

```bash
/sp.plan
```

This launches the **spec-to-architecture agent** to create `plan.md` with:
- Technical design
- Component architecture
- API contracts
- Database schema
- Performance targets

### Step 3: Break Down Into Tasks

```bash
/sp.tasks
```

This launches the **task-breakdown-organizer agent** to create `tasks.md` with:
- Atomic, testable tasks
- Dependencies
- Acceptance criteria
- Test cases

### Step 4: Implement Tasks

For **frontend tasks**:
```bash
# Uses nextjs-frontend-developer agent
<implement frontend components, hooks, pages>
```

For **backend tasks**:
```bash
# Uses fastapi-backend-developer agent
<implement API endpoints, models, services>
```

For **database tasks**:
```bash
# Uses database-architect agent
<create schemas, migrations, indexes>
```

### Step 5: Test Integration

```bash
# Uses integration-testing-agent
<run E2E tests, API tests, integration tests>
```

### Step 6: Document Decisions

When making significant architectural decisions:

```bash
/sp.adr <decision-title>
```

This creates an ADR in `history/adr/` documenting:
- Context
- Options considered
- Decision made
- Rationale
- Consequences

---

## 💻 Development Commands

### Frontend (Next.js)

```bash
# Navigate to frontend
cd apps/frontend

# Install dependencies
npm install

# Development server (http://localhost:3000)
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# E2E tests (Playwright)
npm run test:e2e

# Type checking
npm run type-check

# Linting
npm run lint
```

### Backend (FastAPI)

```bash
# Navigate to backend
cd apps/backend

# Install dependencies
poetry install

# Development server (http://localhost:8000)
poetry run uvicorn app.main:app --reload

# API documentation (auto-generated)
# http://localhost:8000/docs (Swagger)
# http://localhost:8000/redoc (ReDoc)

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=app --cov-report=html

# Type checking
poetry run mypy app

# Database migrations
poetry run alembic revision --autogenerate -m "Description"
poetry run alembic upgrade head
```

### Full Stack (Docker Compose)

```bash
# Start all services (Postgres + Backend + Frontend)
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild containers
docker-compose up --build
```

### Workspace Commands (Root)

```bash
# Install all dependencies (frontend + backend)
npm install

# Run frontend dev server
npm run dev:frontend

# Run backend dev server
npm run dev:backend

# Run both in parallel
npm run dev

# Run all tests
npm run test

# Build frontend
npm run build:frontend

# Deploy (requires configuration)
npm run deploy
```

---

## 🧠 AI Agents & Skills

This project uses specialized AI agents for different tasks:

### Available Agents

1. **nextjs-frontend-developer** - Frontend implementation
   - React components
   - Next.js pages
   - API routes (BFF pattern)
   - Tailwind CSS styling
   - SWR data fetching

2. **fastapi-backend-developer** - Backend API development
   - REST endpoints
   - Pydantic validation
   - SQLModel integration
   - Error handling

3. **database-architect** - Database design
   - Schema design
   - Migrations (Alembic)
   - Indexes & constraints
   - Query optimization

4. **auth-security-guardian** - Security & authentication
   - JWT authentication
   - CORS configuration
   - Input sanitization
   - Security headers

5. **integration-testing-agent** - E2E & integration testing
   - Playwright E2E tests
   - API integration tests
   - Database testing

### Skills Reference

All Phase II implementation skills are documented in:
```
.claude/skills/skills.md
```

**Available Skills**:
1. Next.js Component Skill
2. API Route Skill
3. FastAPI Endpoint Skill
4. Database Schema Skill
5. Frontend Data Fetching Skill
6. Form Handling Skill
7. Environment Configuration Skill
8. Integration Testing Skill
9. Monorepo Setup Skill
10. API Testing Skill
11. Deployment Skill

---

## 📋 Constitution & Standards

### Core Principles

This project follows **Spec-Driven Development (SDD)** as defined in:
```
.specify/memory/constitution.md
```

**Key Principles**:
1. ✅ **Spec-Driven Development** - All code from specs
2. ✅ **Clean Code** - PEP 8, TypeScript strict mode
3. ✅ **Test-First Development (TDD)** - Red-Green-Refactor
4. ✅ **Single Responsibility** - Clear separation of concerns
5. ✅ **Evolutionary Architecture** - Forward compatible
6. ✅ **User Experience First** - Accessible, responsive

### Quality Gates

Before any merge:
- ✅ All tests passing (unit + integration + E2E)
- ✅ Type checking passes (mypy for Python, tsc for TypeScript)
- ✅ Linting passes (flake8, ESLint)
- ✅ Code coverage > 80%
- ✅ Spec requirements met
- ✅ No secrets in code

---

## 🚀 Deployment

### Frontend (Vercel)

```bash
cd apps/frontend

# Deploy to production
vercel --prod

# Environment variables in Vercel dashboard:
# NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

### Backend (Railway)

```bash
cd apps/backend

# Deploy to production
railway up

# Run migrations in production
railway run poetry run alembic upgrade head

# Environment variables in Railway dashboard:
# DATABASE_URL=<neon-connection-string>
# API_SECRET_KEY=<32-char-secret>
# CORS_ORIGINS=["https://your-app.vercel.app"]
```

### Database (Neon)

1. Create project at https://neon.tech
2. Copy connection string
3. Add to Railway environment variables
4. Run migrations

See `specs/phase-2-todo-web/README.md` for detailed deployment guide.

---

## 🧪 Testing Strategy

### Frontend Testing

- **Unit Tests**: Jest + React Testing Library
- **E2E Tests**: Playwright
- **Coverage Target**: > 80%

```bash
cd apps/frontend
npm run test          # Unit tests
npm run test:e2e      # E2E tests
```

### Backend Testing

- **Unit Tests**: Pytest (models, services)
- **Integration Tests**: Pytest with httpx (API endpoints)
- **Coverage Target**: > 80%

```bash
cd apps/backend
poetry run pytest --cov=app
```

### Integration Testing

Full-stack integration tests verify:
- API endpoints work end-to-end
- Database operations succeed
- Frontend-backend integration
- Authentication flows

```bash
# Run from root
npm run test:integration
```

---

## 📚 Additional Resources

### Documentation Files

- **This File**: Overall project guide
- **Frontend Guide**: `apps/frontend/CLAUDE.md`
- **Backend Guide**: `apps/backend/CLAUDE.md`
- **Spec Structure**: `specs/phase-2-todo-web/README.md`
- **Constitution**: `.specify/memory/constitution.md`
- **Skills Reference**: `.claude/skills/skills.md`

### SpecKit Plus Commands

All available commands:
- `/sp.specify` - Create feature specification
- `/sp.plan` - Generate architecture plan
- `/sp.tasks` - Break down into tasks
- `/sp.implement` - Execute implementation
- `/sp.adr <title>` - Document architectural decision
- `/sp.checklist` - Generate feature checklist
- `/sp.git.commit_pr` - Create commit and PR

### External Links

- **Next.js Docs**: https://nextjs.org/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLModel Docs**: https://sqlmodel.tiangolo.com
- **Neon Docs**: https://neon.tech/docs
- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app

---

## 🎯 Current Status

**Phase**: II - Full-Stack Web Application
**Stage**: Specification & Planning
**Next Steps**:
1. Run `/sp.specify` in `specs/phase-2-todo-web/`
2. Generate architecture plan with `/sp.plan`
3. Break down tasks with `/sp.tasks`
4. Begin implementation

---

## 💡 Pro Tips

### For Frontend Development
- Use Server Components by default, Client Components only when needed
- Reference `apps/frontend/CLAUDE.md` for component patterns
- Check `.claude/skills/skills.md` for Next.js Component Skill

### For Backend Development
- All API endpoints should have OpenAPI docs
- Reference `apps/backend/CLAUDE.md` for API patterns
- Check `.claude/skills/skills.md` for FastAPI Endpoint Skill

### For Database Work
- Always create migrations, never modify schema directly
- Reference `.claude/skills/skills.md` for Database Schema Skill
- Test migrations both up and down

### For Testing
- Write tests for specs, not implementation
- Use Given-When-Then format
- Reference `.claude/skills/skills.md` for Testing Skills

---

**Built with Spec-Driven Development**
**Powered by Claude Code + SpecKit Plus**

For questions or issues, reference:
- Constitution: `.specify/memory/constitution.md`
- Agents: `.claude/agents/`
- Skills: `.claude/skills/skills.md`
- Specs: `specs/phase-2-todo-web/`
