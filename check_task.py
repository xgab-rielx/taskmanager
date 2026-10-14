from datetime import datetime, timezone

from app.db_session import SessionLocal
from app.models import Task


with SessionLocal() as session:
    task = Task(
        title="Teste de conexão com ORM",
        completed=False,
        priority="media",
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    session.add(task)
    session.flush()

    task_id = task.id

    print(f"Id gerado: {task_id}")
    print(f"Titulo: {task.title}")
    print(f"Concluída: {task.completed}")

    session.rollback()

with SessionLocal() as session:
    saved_task = session.get(Task, task_id)
    print(f"Tarefa existe após rollback: {saved_task is not None}")