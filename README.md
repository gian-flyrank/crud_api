# Task API

A FastAPI project for the Week 2 CRUD API assignment.

## Run locally

```bash
source .venv/bin/activate
uvicorn src.main:app --reload
```

Open <http://localhost:8000/> to see API information, or visit
<http://localhost:8000/health> to check that the server is running.

Interactive API documentation is available at <http://localhost:8000/docs>.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/` | API information |
| GET | `/health` | Server health check |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{task_id}` | Get one task |
