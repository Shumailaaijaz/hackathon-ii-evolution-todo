# Evolution of Todo - Phase II: Full-Stack Web Application

A production-ready, full-stack todo application with secure multi-user authentication. Built as part of the "Evolution of Todo" hackathon project, Phase II transforms the console application into a modern web platform.

## 🎯 Overview

**Phase II Evolution**: Console App → Full-Stack Web Application

- ✅ **Multi-user authentication** with Better Auth + JWT
- ✅ **Web UI** built with Next.js 16+ and Tailwind CSS
- ✅ **REST API** powered by FastAPI with SQLModel ORM
- ✅ **PostgreSQL database** on Neon serverless platform
- ✅ **User isolation** - Each user's tasks are private and secure
- ✅ **Production deployment** on Vercel (frontend) + Railway (backend)

## 🏗️ Architecture

**Monorepo Structure**:

```
apps/
├── frontend/          Next.js 16+ (TypeScript, Tailwind CSS, Better Auth)
└── backend/           FastAPI (Python 3.11+, SQLModel, Pydantic)

Database: Neon PostgreSQL 16+ (serverless with connection pooling)
```

**Technology Stack**:

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | Next.js | 16+ |
| UI Library | React | 18+ |
| Styling | Tailwind CSS | 3+ |
| Auth | Better Auth | Latest |
| Data Fetching | SWR | Latest |
| Icons | Lucide React | Latest |
| Backend | FastAPI | 0.104+ |
| ORM | SQLModel | Latest |
| Validation | Pydantic | 2.0+ |
| Database | PostgreSQL (Neon) | 16+ |
| Migrations | Alembic | Latest |
| Testing (FE) | Jest + Playwright | Latest |
| Testing (BE) | pytest | Latest |

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm 9+
- **Python** 3.11+
- **PostgreSQL** database (Neon account recommended)
- **Git** for version control

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hackathon-ii-evolution-todo
   ```

2. **Install root dependencies** (optional - for running both services):
   ```bash
   npm install
   ```

3. **Setup Backend**:
   ```bash
   cd apps/backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Setup Frontend**:
   ```bash
   cd apps/frontend
   npm install
   ```

### Environment Configuration

1. **Backend** - Create `apps/backend/.env`:
   ```env
   DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
   BETTER_AUTH_SECRET=your-secret-key-min-32-characters
   JWT_ALGORITHM=HS256
   JWT_EXPIRE_DAYS=7
   CORS_ORIGINS=http://localhost:3000
   ENVIRONMENT=development
   DEBUG=True
   ```

2. **Frontend** - Create `apps/frontend/.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   BETTER_AUTH_SECRET=your-secret-key-min-32-characters
   NODE_ENV=development
   ```

   **⚠️ IMPORTANT**: `BETTER_AUTH_SECRET` must be identical in both .env files!

### Database Setup

```bash
cd apps/backend
alembic upgrade head  # Run database migrations
```

### Running Locally

**Option 1: Run both services together** (from root):
```bash
npm run dev
```

**Option 2: Run services separately**:

```bash
# Terminal 1: Backend (http://localhost:8000)
cd apps/backend
uvicorn app.main:app --reload

# Terminal 2: Frontend (http://localhost:3000)
cd apps/frontend
npm run dev
```

### Verification

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/health

## 📚 Documentation

- **Project Structure**: See [CLAUDE.md](./CLAUDE.md)
- **Specifications**: See [specs/](./specs/)
- **Phase I Reference**: See [Phase I README](./specs/phase-1-todo-app/)

## 🧪 Testing

### Backend Tests

```bash
cd apps/backend
pytest                      # Run all tests
pytest --cov=app           # With coverage
pytest tests/test_tasks.py # Specific test file
```

**Test Coverage Target**: ≥90%

### Frontend Tests

```bash
cd apps/frontend
npm test                   # Unit tests (Jest)
npm run test:e2e          # E2E tests (Playwright)
```

**Test Coverage Target**: ≥80%

## 🚢 Deployment

### Backend (Railway/Render)

1. Connect GitHub repository
2. Set environment variables (DATABASE_URL, BETTER_AUTH_SECRET, etc.)
3. Deploy from `apps/backend`
4. Run migrations: `alembic upgrade head`

### Frontend (Vercel)

1. Connect GitHub repository
2. Set root directory to `apps/frontend`
3. Set environment variables (NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET)
4. Deploy

### Database (Neon)

1. Create project at https://neon.tech
2. Copy connection string
3. Add to backend environment variables
4. Run migrations

## 🔐 Security Features

- ✅ **JWT Authentication** with 7-day token expiration
- ✅ **Password Hashing** with bcrypt (10+ rounds)
- ✅ **User Isolation** - 100% enforcement (no cross-user access)
- ✅ **HTTPS Only** in production
- ✅ **CORS** restricted to allowed origins
- ✅ **Input Validation** on both frontend and backend
- ✅ **SQL Injection Protection** via parameterized queries

## 📊 Performance Targets

- API Response Time: < 200ms (p95)
- Database Queries: < 50ms
- JWT Validation: < 10ms
- Frontend Page Load: < 2s on 3G
- Concurrent Users: 100+

## 🔄 Development Workflow

This project follows **Spec-Driven Development (SDD)** with **Test-Driven Development (TDD)**:

1. **Spec** → Define requirements
2. **Plan** → Design architecture
3. **Tasks** → Break down implementation
4. **Red** → Write failing tests
5. **Green** → Minimal implementation
6. **Refactor** → Improve code quality

## 📁 Project Structure

```
hackathon-ii-evolution-todo/
├── apps/
│   ├── frontend/            # Next.js application
│   │   ├── app/            # App Router pages
│   │   ├── components/     # React components
│   │   ├── lib/           # Utilities and API client
│   │   └── tests/         # Frontend tests
│   └── backend/            # FastAPI application
│       ├── app/
│       │   ├── models/    # SQLModel data models
│       │   ├── api/       # API routes
│       │   ├── core/      # Config and security
│       │   └── schemas/   # Pydantic schemas
│       ├── alembic/       # Database migrations
│       └── tests/         # Backend tests
├── specs/                  # Feature specifications
├── history/               # ADRs and prompt history
├── .claude/              # AI agent configurations
├── .specify/            # SpecKit Plus configuration
└── package.json         # Workspace configuration
```

## 🛠️ Development Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Run both frontend and backend |
| `npm run dev:frontend` | Run only frontend |
| `npm run dev:backend` | Run only backend |
| `npm test` | Run all tests |
| `npm run test:frontend` | Run frontend tests |
| `npm run test:backend` | Run backend tests |
| `npm run build:frontend` | Build frontend for production |
| `npm run lint` | Lint all code |

## 🎓 Learning Resources

- **Next.js**: https://nextjs.org/docs
- **Better Auth**: https://better-auth.com/docs
- **FastAPI**: https://fastapi.tiangolo.com
- **SQLModel**: https://sqlmodel.tiangolo.com
- **Neon PostgreSQL**: https://neon.tech/docs
- **Tailwind CSS**: https://tailwindcss.com/docs

## 📝 License

MIT

## 🙏 Acknowledgments

Built as part of the "Evolution of Todo" hackathon project using Spec-Driven Development with AI-assisted coding (Claude Code).

---

**Phase**: II - Full-Stack Web Application
**Status**: In Development
**Next Phase**: III - Mobile + Real-time Features
