.PHONY: install dev run migrate test lint

install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

migrate:
	alembic upgrade head

test:
	pytest -v

lint:
	fastapi codegen --help > /dev/null 2>&1 || echo "lint not configured"
