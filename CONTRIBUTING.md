# Contributing to AutoClip AI

## Getting Started

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/yourusername/autoclip-ai.git`
3. **Copy** environment: `cp .env.example .env`
4. **Start** services: `docker compose up -d --build`

## Development Workflow

### Branch Naming

```
feature/description    → New features
fix/description        → Bug fixes
docs/description       → Documentation
refactor/description   → Code refactoring
```

### Running Locally (without Docker)

```bash
# Backend
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000

# Frontend
cd frontend && npm install && npm run dev

# Worker
celery -A core.celery_app worker --loglevel=info
```

### Tests

```bash
pytest tests/ -v
```

## Project Structure

- `api/` — FastAPI endpoints and authentication
- `core/` — Database models, Celery config
- `worker/` — Background task definitions
- `engines/` — AI analysis engine integrations
- `frontend/` — Next.js web application
- Root `.py` files — Video processing pipeline modules

## Code Style

- **Python**: Follow PEP 8, use type hints
- **TypeScript**: ESLint + Prettier defaults
- **Commits**: Use conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`)

## Pull Request Process

1. Create a feature branch from `develop`
2. Make your changes with clear commit messages
3. Ensure tests pass
4. Submit a PR with a description of changes
5. Wait for code review
