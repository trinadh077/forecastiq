# Installation Guide

## Quickstart with Docker Compose

1. Clone repository:
   ```bash
   git clone https://github.com/your-org/forecastiq.git
   cd forecastiq
   ```

2. Copy environment file:
   ```bash
   cp .env.example .env
   ```

3. Launch application stack:
   ```bash
   docker-compose up --build -d
   ```

4. Verify services:
   - Frontend: `http://localhost`
   - Backend OpenAPI Docs: `http://localhost/docs` or `http://localhost:8000/docs`
