import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import database


@pytest.fixture
def client():
    database.DB_FILE = "test_tasks.db"
    database.init_db()

    with TestClient(app) as test_client:
        yield test_client

    if os.path.exists("test_tasks.db"):
        os.remove("test_tasks.db")


def test_get_task(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client):
    response = client.post(
        "/tasks", json={"title": "Tarefa criada pelo teste", "priority": "alta"}
    )

    assert response.status_code == 200

    task = response.json()

    assert task["id"] == 1
    assert task["title"] == "Tarefa criada pelo teste"
    assert task["completed"] is False
    assert task["priority"] == "alta"
    assert "created_at" in task


def test_task_by_id(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa não encontrada"}


def test_create_task_with_invalid_priority(client):
    response = client.post(
        "/tasks",
        json={"title": "Tarefa com prioridade inválida", "priority": "urgente"},
    )

    assert response.status_code == 422

    error = response.json()

    assert "priority" in str(error)


def test_get_task_by_id(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Tarefa pra buscar por id", "priority": "alta"},
    )

    assert create_response.status_code == 200

    created_task = create_response.json()
    task_id = created_task["id"]

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 200

    task = get_response.json()

    assert task["id"] == task_id
    assert task["title"] == "Tarefa pra buscar por id"
    assert task["priority"] == "alta"
    assert task["completed"] is False
    assert "created_at" in task


def test_update_task(client):
    create_response = client.post(
        "/tasks", json={"title": "Tarefa para atualizar", "priority": "baixa"}
    )

    assert create_response.status_code == 200

    created_task = create_response.json()
    task_id = created_task["id"]

    update_response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Tarefa atualizada", "completed": True, "priority": "alta"},
    )

    assert update_response.status_code == 200

    updated_task = update_response.json()

    assert updated_task["id"] == task_id
    assert updated_task["title"] == "Tarefa atualizada"
    assert updated_task["completed"] is True
    assert updated_task["priority"] == "alta"


def test_update_task_not_found(client):
    response = client.put(
        "/tasks/999",
        json={"title": "Tarefa inexistente", "completed": "True", "priority": "alta"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa não encontrada"}


def test_dekete_task(client):
    create_response = client.post(
        "/tasks", json={"title": "Tarefa para deletar", "priority": "media"}
    )

    assert create_response.status_code == 200

    created_task = create_response.json()
    task_id = created_task["id"]

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 200

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Tarefa não encontrada"}


def test_delete_task_not_found(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa não encontrada"}


def test_create_task_without_title(client):
    response = client.post(
        "/tasks",
        json={
            "priority": "alta"
        }
    )

    assert response.status_code == 422

    error = response.json()
    assert "title" in str(error)