from datetime import datetime, timezone

from app.crud_postgres import create_task, get_task_by_id


if __name__ == "__main__":
    task_id = create_task(
        title="Primeira tarefa CRUD PostgreSQL",
        completed=False,
        priority="media",
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    task = get_task_by_id(task_id)

    assert task is not None
    assert task["id"] == task_id
    assert task["title"] == "Primeira tarefa CRUD PostgreSQL"
    assert task["completed"] is False
    assert task["priority"] == "media"

    print(f"Tarefa Criada e consultada com sucesso. ID: {task_id}")
    print(task)