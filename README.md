# ForecastIQ
### AI-Powered Sales Forecasting SaaS Platform Architecture

ForecastIQ is a production-ready enterprise AI-powered Sales Forecasting SaaS foundation built with clean architecture, SOLID design principles, async database access, and modern web standards.

---

## Technical Features

- **FastAPI + Python 3.12 Backend**: Async architecture with Pydantic v2 schemas and OAuth2 JWT authentication.
- **SQLAlchemy 2.0 & Alembic**: PostgreSQL ORM with complete 11-table schema (`users`, `organizations`, `roles`, `datasets`, `ml_models`, `forecasts`, `reports`, `integrations`, `subscriptions`, `payments`, `audit_logs`).
- **Role-Based Access Control (RBAC)**: Supports `ADMIN`, `MANAGER`, and `SALES_ANALYST` access controls.
- **React 19 + TypeScript + Tailwind CSS Frontend**: Modern Vite SPA with theme context (Dark/Light mode), Layout systems, and state hooks.
- **Docker Compose Production Stack**: Complete multi-stage Dockerfiles for Backend & Frontend with NGINX reverse proxy setup.
- **CI/CD Pipeline**: GitHub Actions workflow covering linting, backend testing with Pytest, and frontend builds.

---

## Quickstart

```bash
# Clone and enter repo
git clone https://github.com/your-org/forecastiq.git
cd forecastiq

# Launch full stack
docker-compose up --build -d
```

Access Swagger UI at `http://localhost:8000/docs` and Frontend at `http://localhost`.

---

## Verification & Testing

To run the automated test suite:
```bash
pip install -r backend/requirements.txt pytest pytest-asyncio httpx
pytest tests/ -v
```
