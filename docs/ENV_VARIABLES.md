# Environment Variables Reference

| Variable | Description | Default |
|---|---|---|
| `APP_NAME` | Name of the platform | `ForecastIQ` |
| `APP_ENV` | Environment mode (`development`, `production`, `test`) | `development` |
| `SECRET_KEY` | JWT Signing key | `super-secret-key-change-this-in-production...` |
| `DATABASE_URL` | Async PostgreSQL database connection string | `postgresql+asyncpg://forecastiq:forecastiq_password@localhost:5432/forecastiq_db` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `BACKEND_CORS_ORIGINS` | JSON list of allowed origins | `["http://localhost:3000","http://localhost:5173"]` |
