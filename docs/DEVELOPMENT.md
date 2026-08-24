# Local Development Workflow

## Prerequisites
- Python 3.12+
- Node.js 20+
- Docker & Docker Compose

## Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Running Tests
```bash
pytest tests/
```
