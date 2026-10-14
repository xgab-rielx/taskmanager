from app.database import get_connection


def get_tasks(
    completed: bool | None = None,
    priority: str | None = None,
):
    conn = get_connection()
    cursor = conn.cursor()
    if completed is not None and priority is not None:
        cursor.execute(
            "SELECT * FROM tasks WHERE completed = ? AND priority = ?",
            (int(completed), priority),
        )
    elif completed is not None:
        cursor.execute(
            "SELECT * FROM tasks WHERE completed = ?", 
            (int(completed),)
        )
    elif priority is not None:
        cursor.execute(
            "SELECT * FROM tasks WHERE priority = ?", 
            (priority,)
        )
    else:
        cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    conn.close()

    return tasks


def get_task_by_id(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,),
    )
    row = cursor.fetchone()

    conn.close()

    return row


def create_task(title: str, completed: bool, priority: str, created_at: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, completed, priority, created_at) VALUES (?, ?, ?, ?)",
        (title, int(completed), priority, created_at),
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return task_id


def update_task(task_id: int, title: str, completed: bool, priority: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET title = ?, completed = ?, priority = ? WHERE id = ?",
        (title, int(completed), priority, task_id),
    )

    rows_affected = cursor.rowcount

    conn.commit()
    conn.close()

    return rows_affected

def update_task_status(task_id: int, completed: bool):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET completed = ? WHERE id = ?",
        (int(completed), task_id),
    )

    rows_affected = cursor.rowcount

    conn.commit()
    conn.close()

    return rows_affected


def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,),
    )

    rows_effected = cursor.rowcount

    conn.commit()
    conn.close()

    return rows_effected