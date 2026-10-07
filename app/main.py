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
async def get_task_by_id(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, completed FROM tasks WHERE id = ?",
        (task_id,),
    )
    row = cursor.fetchone()

    conn.close()

    if row:
        return {
            "id": row["id"],
            "title": row["title"],
            "completed": bool(row["completed"]),
        }

    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


class TaskUpdate(BaseModel):
    title: str
    completed: bool


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET title = ?, completed = ? WHERE id = ?",
        (task_update.title, int(task_update.completed), task_id),
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

    return {"message": f'Tarefa {task_id} removida'}
