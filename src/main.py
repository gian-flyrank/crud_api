from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.modules.health import get_health_status
from src.modules.root import get_api_info
from src.modules.tasks import find_task, get_all_tasks

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


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )

    return task
