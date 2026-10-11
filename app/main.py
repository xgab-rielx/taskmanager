from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import init_db, get_connection
from datetime import datetime
from typing import Literal

app = FastAPI()

init_db()

tasks = [{"id": 1, "title": "Estudar FastAPI", "completed": False}]

Priority = Literal["baixa", "media", "alta"]


@app.get("/tasks")
async def get_tasks(
    completed: bool | None = None,
    priority: Priority | None = None
):
    conn = get_connection()
    cursor = conn.cursor()

    if completed is not None and priority is not None:
        cursor.execute("SELECT * FROM tasks WHERE completed = ? AND priority = ?",
                   (int(completed), priority),
        )
    elif completed is not None:
        cursor.execute("SELECT * FROM tasks WHERE completed = ?",
                       (int(completed),)
        )
    elif priority is not None:
        cursor.execute("SELECT * FROM tasks WHERE priority = ?",
                        (priority,)
        )
    else:
        cursor.execute("SELECT * FROM tasks")
        
    rows = cursor.fetchall()

    tasks = [
        {
            "id": row["id"],
            "title": row["title"],
            "completed": bool(row["completed"]),
            "priority": row["priority"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]

    conn.close()

    return tasks


class TaskCreate(BaseModel):
    title: str
    completed: bool = False
    priority: Priority = "media"


@app.post("/tasks")
async def create_task(task: TaskCreate):
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO tasks (title, completed, priority, created_at) VALUES (?, ?, ?, ?)",
        (task.title, int(task.completed), task.priority, created_at),
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return {
        "id": task_id,
        "title": task.title,
        "completed": task.completed,
        "priority": task.priority,
        "created_at": created_at,
    }


@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,),
    )
    row = cursor.fetchone()

    conn.close()

    if row:
        return {
            "id": row["id"],
            "title": row["title"],
            "completed": bool(row["completed"]),
            "priority": row["priority"],
            "created_at": row["created_at"],
        }

    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


class TaskUpdate(BaseModel):
    title: str
    completed: bool
    priority: Priority


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET title = ?, completed = ?, priority = ? WHERE id = ?",
        (task_update.title, int(task_update.completed), task_update.priority, task_id),
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    conn.commit()
    conn.close()

    return {
        "id": task_id,
        "title": task_update.title,
        "completed": task_update.completed,
        "priority": task_update.priority
    }


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,),
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    conn.commit()
    conn.close()

    return {"message": f"Tarefa {task_id} removida"}
