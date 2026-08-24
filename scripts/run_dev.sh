#!/bin/bash
set -e

echo "Starting ForecastIQ Local Development Environment..."

# Start Docker Services (PostgreSQL & Redis)
docker-compose up -d postgres redis

# Run Database Migrations
echo "Running database migrations..."
cd backend
alembic upgrade head
cd ..

echo "Development infrastructure is live!"
echo "Backend URL: http://localhost:8000"
echo "Frontend Dev Server: cd frontend && npm run dev"
