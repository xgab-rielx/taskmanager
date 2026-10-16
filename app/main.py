from app.crud_postgres import (
    get_tasks as get_tasks_from_db,
    create_task as create_task_from_db,
)
from app.crud import (
    get_task_by_id as get_task_by_id_from_db,
    update_task as update_task_from_db,
    update_task_status,
    delete_task as delete_task_from_db
)
from fastapi import FastAPI, HTTPException
from app.database import init_db
from datetime import datetime

from app.schemas import TaskCreate, TaskUpdate, TaskUpdateStatus, Priority

app = FastAPI()

init_db()


@app.get("/tasks")
async def get_tasks(completed: bool | None = None, priority: Priority | None = None):

    rows = get_tasks_from_db(completed=completed, priority=priority)

    tasks = [
        {
           "id": row.id,
            "title": row.title,
            "completed": row.completed,
            "priority": row.priority,
            "created_at": row.created_at,
        }
        for row in rows
    ]

    return tasks


@app.post("/tasks")
async def create_task(task: TaskCreate):
    created_at = datetime.now().isoformat()
    task_id = create_task_from_db(
        title=task.title,
        completed=task.completed,
        priority=task.priority,
        created_at=created_at,
    )

    return {
        "id": task_id,
        "title": task.title,
        "completed": task.completed,
        "priority": task.priority,
        "created_at": created_at,
    }


@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int):

    row = get_task_by_id_from_db(task_id)

    if row:
        return {
            "id": row["id"],
            "title": row["title"],
            "completed": bool(row["completed"]),
            "priority": row["priority"],
            "created_at": row["created_at"],
        }

    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate):

    rows_affected = update_task_from_db(
        task_id=task_id,
        title=task_update.title,
        completed=task_update.completed,
        priority=task_update.priority,
    )
    
    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return {
        "id": task_id,
        "title": task_update.title,
        "completed": task_update.completed,
        "priority": task_update.priority,
    }


@app.patch("/tasks/{task_id}/status")
async def update_status(task_id: int, update_completed: TaskUpdateStatus):

    rows_affected = update_task_status(
        task_id=task_id,
        completed=update_completed.completed
    )

    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return {
        "message": "Status da tarefa atualizado com sucesso",
        "id": task_id,
        "completed": update_completed.completed,
    }


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):

    rows_effected = delete_task_from_db(
        task_id=task_id
    )

    if rows_effected == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return {"message": f"Tarefa {task_id} removida"}
