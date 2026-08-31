tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build task endpoints", "done": False},
    {"id": 3, "title": "Test the API", "done": False},
]


def get_all_tasks():
    return tasks


def find_task(task_id: int):
    return next((task for task in tasks if task["id"] == task_id), None)
