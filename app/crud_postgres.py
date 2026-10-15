from app.db_session import SessionLocal
from app.models import Task


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