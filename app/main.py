from app.crud_postgres import (
    get_tasks as get_tasks_from_db,
    create_task as create_task_from_db,
    get_task_by_id as get_task_by_id_from_db,
    update_task as update_task_from_db,
    update_task_status as update_task_status_from_db,
    delete_task as delete_task_from_db
)
from fastapi import FastAPI, HTTPException
from datetime import datetime

from app.schemas import TaskCreate, TaskUpdate, TaskUpdateStatus, Priority

app = FastAPI()


@app.post("/tasks")
async def create_task(task: TaskCreate):
    created_at = datetime.now().isoformat()

    return create_task_from_db(
        title=task.title,
        completed=task.completed,
        priority=task.priority,
        created_at=created_at,
    )



@app.get("/tasks")
async def get_tasks(completed: bool | None = None, priority: Priority | None = None):

    return get_tasks_from_db(completed=completed, priority=priority,)


@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int):

    task = get_task_by_id_from_db(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return task
        


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate):

    updated_task = update_task_from_db(
        task_id=task_id,
        title=task_update.title,
        completed=task_update.completed,
        priority=task_update.priority,
    )
    
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return updated_task


@app.patch("/tasks/{task_id}/status")
async def update_status(task_id: int, update_completed: TaskUpdateStatus):

    updated_task = update_task_status_from_db(
        task_id=task_id,
        completed=update_completed.completed
    )

    if updated_task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return updated_task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):

    deleted_task = delete_task_from_db(
        task_id=task_id
    )

    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return deleted_task
