from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import init_db, get_connection

app = FastAPI()

init_db()

tasks = [{"id": 1, "title": "Estudar FastAPI", "completed": False}]


@app.get("/tasks")
async def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    tasks = [
        {"id": row["id"], "title": row["title"], "completed": bool(row["completed"])}
        for row in rows
    ]

    conn.close()

    return tasks


class TaskCreate(BaseModel):
    title: str
    completed: bool = False


@app.post("/tasks")
async def create_task(task: TaskCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, completed) VALUES (?, ?)",
        (task.title, int(task.completed)),
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return {"id": task_id, "title": task.title, "completed": task.completed}


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
