from fastapi import Body, FastAPI, Response
from fastapi.responses import JSONResponse

from src.modules.health import get_health_status
from src.modules.root import get_api_info
from src.modules.tasks import (
    create_task,
    delete_task,
    find_task,
    get_all_tasks,
    update_task,
)

openapi_tags = [
    {
        "name": "General",
        "description": "Basic information about the Task API.",
    },
    {
        "name": "Health",
        "description": "Endpoints for checking whether the API is running.",
    },
    {
        "name": "Tasks",
        "description": "Create, read, update, and delete to-do tasks.",
    },
]

app = FastAPI(
    title="Task API",
    description="A simple in-memory CRUD API for managing to-do tasks.",
    version="1.0.0",
    openapi_tags=openapi_tags,
)


@app.get("/", tags=["General"], summary="Get API information")
def read_root():
    return get_api_info()


@app.get("/health", tags=["Health"], summary="Check API health")
def health_check():
    return get_health_status()


@app.get("/tasks", tags=["Tasks"], summary="List all tasks")
def list_tasks():
    return get_all_tasks()


@app.post("/tasks", tags=["Tasks"], status_code=201, summary="Create a task")
def add_task(payload: dict | None = Body(default=None)):
    title = payload.get("title") if payload else None

    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"},
        )

    return create_task(title.strip())


@app.get("/tasks/{task_id}", tags=["Tasks"], summary="Get one task")
def get_task(task_id: int):
    task = find_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )

    return task


@app.put("/tasks/{task_id}", tags=["Tasks"], summary="Update a task")
def edit_task(task_id: int, payload: dict | None = Body(default=None)):
    task = find_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )

    if not payload or not {"title", "done"}.intersection(payload):
        return JSONResponse(
            status_code=400,
            content={"error": "Provide a title and/or done value to update"},
        )

    title = payload.get("title")
    if "title" in payload and (not isinstance(title, str) or not title.strip()):
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"},
        )

    done = payload.get("done")
    if "done" in payload and not isinstance(done, bool):
        return JSONResponse(
            status_code=400,
            content={"error": "Done must be true or false"},
        )

    changes = {}
    if "title" in payload:
        changes["title"] = title.strip()
    if "done" in payload:
        changes["done"] = done

    return update_task(task, changes)


@app.delete(
    "/tasks/{task_id}",
    tags=["Tasks"],
    status_code=204,
    summary="Delete a task",
)
def remove_task(task_id: int):
    task = find_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )

    delete_task(task)
    return Response(status_code=204)
