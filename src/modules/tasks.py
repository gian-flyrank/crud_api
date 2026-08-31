tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build task endpoints", "done": False},
    {"id": 3, "title": "Test the API", "done": False},
]


def get_all_tasks():
    return tasks


def create_task(title: str):
    next_id = max(task["id"] for task in tasks) + 1
    task = {"id": next_id, "title": title, "done": False}
    tasks.append(task)
    return task


def find_task(task_id: int):
    return next((task for task in tasks if task["id"] == task_id), None)


def update_task(task: dict, changes: dict):
    task.update(changes)
    return task


def delete_task(task: dict):
    tasks.remove(task)
