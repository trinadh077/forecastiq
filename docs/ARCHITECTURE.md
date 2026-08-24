# ForecastIQ System Architecture Overview

ForecastIQ is designed using clean multi-layer architectural principles to deliver high-performance, enterprise-grade AI Sales Revenue forecasting.

## Architectural Layers

```
[ Frontend: React 19 + TypeScript + TailwindCSS ]
                     │  (HTTP / REST API)
                     ▼
  [ Nginx Reverse Proxy & SSL Termination ]
                     │
                     ▼
 [ Backend: FastAPI + Pydantic v2 + OAuth2/JWT ]
       │                         │
       ▼                         ▼
[ SQLAlchemy 2 Async ]   [ Celery / Redis Queue ]
       │                         │
       ▼                         ▼
[ PostgreSQL DB ]        [ ML Worker Engine ]
```

### Key Subsystems
1. **API Gateway / Core**: FastAPI ASGI engine managing auth, middleware correlation IDs, Pydantic validation, and OpenAPI 3.0 schema generation.
2. **Data Layer**: PostgreSQL database managed via SQLAlchemy 2.0 async ORM and Alembic schema migrations.
3. **ML Training & Inference Engine**: Standalone processing pipeline running auto-model selection (Prophet, XGBoost, ARIMA, LSTM, Ensemble).
4. **Presentation Layer**: Single Page Application built on React 19, Vite, TailwindCSS, and Recharts.
