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

app = FastAPI(title="Task API")


@app.get("/")
def read_root():
    return get_api_info()


@app.get("/health")
def health_check():
    return get_health_status()


@app.get("/tasks")
def list_tasks():
    return get_all_tasks()


@app.post("/tasks", status_code=201)
def add_task(payload: dict | None = Body(default=None)):
    title = payload.get("title") if payload else None

    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"},
        )

    return create_task(title.strip())


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )

    return task


@app.put("/tasks/{task_id}")
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


@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: int):
    task = find_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )

    delete_task(task)
    return Response(status_code=204)
