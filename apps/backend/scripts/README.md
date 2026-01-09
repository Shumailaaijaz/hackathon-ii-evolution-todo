# Database Management Scripts

This directory contains utility scripts for database initialization and maintenance.

## scripts/init_db.py

Database initialization and management CLI tool.

### Prerequisites

- Python 3.11+
- Poetry environment with dependencies installed
- DATABASE_URL configured in .env file

### Usage

All commands must be run from the `apps/backend` directory using Poetry:

```bash
cd apps/backend

# Install dependencies first
poetry install

# Run commands with poetry
poetry run python scripts/init_db.py <command>
```

### Commands

#### Verify Database Connection
```bash
poetry run python scripts/init_db.py verify
```
Checks database connectivity and displays connection information.

#### Create Tables
```bash
poetry run python scripts/init_db.py create
```
Creates all database tables based on SQLModel definitions.

#### Create Tables with Sample Data
```bash
poetry run python scripts/init_db.py create --seed
```
Creates tables and populates them with sample development data:
- 3 sample users (alice, bob, charlie)
- 10 sample tasks with various statuses

#### Show Database Info
```bash
poetry run python scripts/init_db.py info
```
Displays comprehensive database information:
- Connection details
- Connection pool status
- Table list with row counts

#### Seed Sample Data
```bash
poetry run python scripts/init_db.py seed
```
Adds sample data to existing tables.

#### Drop All Tables (Destructive!)
```bash
poetry run python scripts/init_db.py drop
```
Drops all database tables with interactive confirmation.
**WARNING**: This permanently deletes all data!

Protected in production environments.

#### Drop Tables Without Confirmation
```bash
poetry run python scripts/init_db.py drop --force
```
Skips confirmation prompt. **Use with extreme caution!**

## Safety Features

- **Production Protection**: Cannot drop tables in production
- **Interactive Confirmation**: Required for destructive operations
- **Connection Verification**: Checks connectivity before operations
- **Detailed Logging**: All operations are logged with timestamps
- **Error Handling**: Comprehensive error catching and reporting

## Examples

### Complete Setup Workflow
```bash
cd apps/backend

# 1. Verify connection
poetry run python scripts/init_db.py verify

# 2. Create tables with sample data
poetry run python scripts/init_db.py create --seed

# 3. Check database status
poetry run python scripts/init_db.py info
```

### Development Reset
```bash
# Drop and recreate with fresh sample data
poetry run python scripts/init_db.py drop --force
poetry run python scripts/init_db.py create --seed
```

## Environment Configuration

Ensure your `.env` file contains:

```env
# Local PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/evolution_todo_dev

# Neon PostgreSQL (recommended)
DATABASE_URL=postgresql://user:password@ep-name.region.aws.neon.tech/dbname

# Neon with pooler (best for production)
DATABASE_URL=postgresql://user:password@ep-name.pooler.region.aws.neon.tech/dbname
```

## Production Deployment

**IMPORTANT**: For production, use Alembic migrations instead of `create_db_and_tables()`:

```bash
# Generate migration
poetry run alembic revision --autogenerate -m "Description"

# Review migration file in alembic/versions/

# Apply migration
poetry run alembic upgrade head
```

The `init_db.py` script's `create` command is intended for development and testing only.
