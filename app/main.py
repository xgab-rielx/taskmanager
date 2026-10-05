from fastapi import FastAPI, HTTPException
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
    id_ = max(task["id"] for task in tasks) + 1
    task_dict = {"id": id_, "title": task.title, "completed": task.completed}
    tasks.append(task_dict)

    return task_dict


@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for task in tasks:
        if task_id == task["id"]:
            return task

    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


class TaskUpdate(BaseModel):
    title: str
    completed: bool


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task_id == task["id"]:
            task["title"] = task_update.title
            task["completed"] = task_update.completed

            return task

    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for task in tasks:
        if task_id == task["id"]:
            tasks.remove(task)

            return {"message": f"Tarefa {task['id']} removida"}

    raise HTTPException(status_code=404, detail="Tarefa não encontrada")
