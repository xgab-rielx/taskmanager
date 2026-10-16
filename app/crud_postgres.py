from app.db_session import SessionLocal
from app.models import Task
from sqlalchemy import select

def create_task(
        title: str,
        completed: bool,
        priority: str,
        created_at: str,
) -> dict:
    with SessionLocal.begin() as session:
        task = Task(
            title=title,
            completed=completed,
            priority=priority,
            created_at=created_at
        )

        session.add(task)
        session.flush()

        created_task = {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
            "priority": task.priority,
            "created_at": task.created_at
        }

    return created_task


def get_task_by_id(task_id: int) -> dict | None:
    with SessionLocal() as session:
        task = session.get(Task, task_id)

        if task is None:
            return None

        return {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
            "priority": task.priority,
            "created_at": task.created_at
        }


def get_tasks(
        completed: bool | None = None,
        priority: str | None = None,
    ):

    with SessionLocal() as session:
        stmt = select(Task)

        if completed is not None:
            stmt = stmt.where(Task.completed == completed)

        if priority is not None:
            stmt = stmt.where(Task.priority == priority)

        tasks = session.scalars(stmt).all()

        return [
            {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "priority": task.priority,
                "created_at": task.created_at
            }
            for task in tasks
        ]

def update_task(
        task_id: int,
        title: str | None = None,
        completed: bool | None = None,
        priority: str | None = None
) -> dict:
    with SessionLocal.begin() as session:
        task = session.get(Task, task_id)

        if task is None:
            return None

        if title is not None:
            task.title = title
        
        if completed is not None:
            task.completed = completed
        
        if priority is not None:
            task.priority = priority

        updated_task = {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
            "priority": task.priority,
            "created_at": task.created_at
        }

    return updated_task

def update_task_status(
        task_id: int,
        completed: bool
) -> dict:
    with SessionLocal.begin() as session:
        task = session.get(Task, task_id)

        if task is None:
            return None 

        task.completed = completed

        updated_task = {
            "id": task_id,
            "title": task.title,
            "completed": task.completed,
            "priority": task.priority,
            "created_at": task.created_at
        }

    return updated_task


def delete_task(task_id: int) -> dict | None:
    with SessionLocal.begin() as session:
        task = session.get(Task, task_id)

        if task is None:
            return None

        session.delete(task)

    return {"message": f"Tarefa {task_id} removida"}
