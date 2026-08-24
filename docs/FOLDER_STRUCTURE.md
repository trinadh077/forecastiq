# ForecastIQ Directory Map

```
forecastiq/
├── backend/
│   ├── alembic/              # Alembic migrations & script template
│   ├── app/
│   │   ├── api/              # API v1 routes & health endpoints
│   │   ├── auth/             # JWT & RBAC permission logic
│   │   ├── config/           # Pydantic settings & logging
│   │   ├── core/             # Security, exceptions, & hashing
│   │   ├── database/         # Session factory & Base ORM model
│   │   ├── dependencies/     # DB & Current User injectors
│   │   ├── middlewares/      # Correlation ID & logger middlewares
│   │   ├── models/           # 11 Async SQLAlchemy 2.0 ORM models
│   │   ├── repositories/     # Base generic CRUD repository
│   │   ├── schemas/          # Pydantic v2 schemas for request/response
│   │   ├── services/         # Business logic layer
│   │   ├── tasks/            # Celery background workers
│   │   ├── utils/            # Helper utilities
│   │   └── main.py           # FastAPI application entrypoint
│   ├── pyproject.toml
│   └── requirements.txt
├── database/
│   └── init.sql              # Initial PostgreSQL seed script
├── docker/
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docs/                     # System architecture & deployment docs
├── frontend/
│   ├── src/                  # React 19 + TypeScript + Tailwind UI
│   ├── package.json
│   └── vite.config.ts
├── nginx/                    # Reverse proxy configs
├── scripts/                  # Seed scripts & dev runners
├── tests/                    # Pytest test suite
├── .env.example
├── docker-compose.yml
└── README.md
```
