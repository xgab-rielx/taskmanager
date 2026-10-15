from app.db_session import SessionLocal
from app.models import Task
from sqlalchemy import select

def create_task(
        title: str,
        completed: bool,
        priority: str,
        created_at: str,
) -> int:
    with SessionLocal.begin() as session:
        task = Task(
            title=title,
            completed=completed,
            priority=priority,
            created_at=created_at
        )

        session.add(task)
        session.flush()

        task_id = task.id

    return task_id


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

        return session.scalars(stmt).all()


def update_task(
        task_id: int,
        title: str | None = None,
        completed: bool | None = None,
        priority: str | None = None
) -> int:
    with SessionLocal.begin() as session:
        task = session.get(Task, task_id)

        if task is None:
            return 0

        if title is not None:
            task.title = title
        
        if completed is not None:
            task.completed = completed
        
        if priority is not None:
            task.priority = priority

    return 1


def update_task_status(
        task_id: int,
        completed: bool
) -> int:
    with SessionLocal.begin() as session:
        task = session.get(Task, task_id)

        if task is None:
            return 0 

        task.completed = completed

    return 1 


def delete_task(task_id: int) -> int:
    with SessionLocal.begin() as session:
        task = session.get(Task, task_id)

        if task is None:
            return 0

        session.delete(task)

    return 1
