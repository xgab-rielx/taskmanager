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
        "/tasks",
        json={
            "title": "Tarefa criada pelo teste",
            "priority": "alta"
        }
    )

    assert response.status_code == 200

    task = response.json()

    assert task["id"] == 1
    assert task["title"] == "Tarefa criada pelo teste"
    assert task["completed"] is False
    assert task["priority"] == "alta"
    assert "created_at" in task