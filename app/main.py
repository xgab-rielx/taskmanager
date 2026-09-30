from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tasks = [{"id": 1, "title": "Estudar FastAPI", "completed": False}]


@app.get("/tasks")
async def get_tasks():
    return tasks


class TaskCreate(BaseModel):
    title: str
    completed: bool = False


@app.post("/tasks")
async def create_task(task: TaskCreate):
    id_ = len(tasks) + 1
    task_dict = {"id": id_, "title": task.title, "completed": task.completed}
    tasks.append(task_dict)

    return task_dict
