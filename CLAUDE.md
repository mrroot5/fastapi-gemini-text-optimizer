# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI application integrating with Gemini AI (2.5 Flash) to transform ecommerce product titles and descriptions into engaging, persuasive messaging. The API simulates fetching product data from an external source (internally loads JSON) and uses Gemini AI's free tier for text transformation.

## Development Commands

### Environment Setup
```bash
poetry install
cp .env.example .env  # Configure environment variables
```

### Running the Application
```bash
# Development server with hot reload
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server with multiple workers
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Testing and Quality
```bash
# Run all tests
poetry run pytest

# Type checking
poetry run mypy .

# Linting
poetry run ruff check .

# Code formatting (note: project uses Ruff)
poetry run ruff format .
```

### Building
```bash
poetry build
```

## Architecture

### Application Structure

The application follows FastAPI's **Bigger Applications** pattern with modular routers:

- **[app/main.py](app/main.py)** - Main FastAPI app instance with global dependencies
- **[app/routers/](app/routers/)** - Feature-specific routers (users, items)
- **[app/internal/](app/internal/)** - Internal/admin routes with restricted access
- **[app/dependencies.py](app/dependencies.py)** - Shared dependency injection functions

### Dependency Injection Pattern

The app uses FastAPI's dependency injection at multiple levels:

1. **Global dependencies** - Applied to entire app via `FastAPI(dependencies=[...])`
   - `get_query_token` is applied globally in [app/main.py:8](app/main.py#L8)

2. **Router-level dependencies** - Applied to all endpoints in a router
   - Items router uses `get_token_header` in [app/routers/items.py:8](app/routers/items.py#L8)
   - Admin router uses `get_token_header` in [app/main.py:17](app/main.py#L17)

3. **Endpoint-level dependencies** - Applied to specific endpoints (not currently used but supported)

### Authentication/Token System

Currently uses placeholder token authentication:
- **Query token**: `token=jessica` (global requirement via `get_query_token`)
- **Header token**: `X-Token: fake-super-secret-token` (for items and admin routes via `get_token_header`)

These are demo tokens and should be replaced with proper authentication in production.

## Code Quality Configuration

### Ruff Settings ([pyproject.toml:23-39](pyproject.toml#L23-L39))
- Line length: 100 characters
- Target: Python 3.11+
- Enabled rules: pycodestyle, pyflakes, isort, flake8-bugbear, comprehensions, pyupgrade
- Note: E501 (line too long) is ignored

### MyPy Settings ([pyproject.toml:41-46](pyproject.toml#L41-L46))
- Strict mode enabled
- Requires type hints for all function definitions
- Python version: 3.12

### Pytest Settings ([pyproject.toml:48-50](pyproject.toml#L48-L50))
- Async mode: auto (for testing async endpoints)
- Test directory: `tests/` (currently no tests exist)

## Important Notes

- Python 3.12.3+ required
- Poetry 1.8+ required for dependency management
- No actual Gemini API integration exists yet in the codebase (mentioned in README but not implemented)
- No database integration currently - uses in-memory fake data stores