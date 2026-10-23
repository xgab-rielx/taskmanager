# -------------- GET -------------

def test_get_tasks_empty_list(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_with_one_task(client):
    payload = {
        "title": "testando",
        "completed": False,
        "priority": "media"
    }

    created_response = client.post("/tasks", json=payload)

    assert created_response.status_code == 200

    created_task = created_response.json()

    response = client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == created_task["id"]
    assert data[0]["title"] == payload["title"]
    assert data[0]["completed"] is False
    assert data[0]["priority"] == payload["priority"]


def test_get_tasks_with_two_tasks(client):
    payload_1 = {
            "title": "testando",
            "completed": False,
            "priority": "media"
        }
    created_response_1 = client.post("/tasks", json=payload_1)
    assert created_response_1.status_code == 200
    created_task_1 = created_response_1.json()

    payload_2 = {
                "title": "testando denovo",
                "completed": False,
                "priority": "media"
            }
    created_response_2 = client.post("/tasks", json=payload_2)
    assert created_response_2.status_code == 200
    created_task_2 = created_response_2.json()

    response = client.get("/tasks")
    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    returned_ids = {task["id"] for task in data}
    expected_ids = {created_task_1["id"], created_task_2["id"]}

    assert returned_ids == expected_ids


def test_get_tasks_filter_completed_true(client):
    payload_1 = {
            "title": "Tarefa concluida",
            "completed": True,
            "priority": "media"
        }
    created_response_1 = client.post("/tasks", json=payload_1)
    assert created_response_1.status_code == 200
    completed_task = created_response_1.json()

    payload_2 = {
                "title": "Tarefa pendente",
                "completed": False,
                "priority": "media"
            }
    created_response_2 = client.post("/tasks", json=payload_2)
    assert created_response_2.status_code == 200

    response = client.get("/tasks", params={"completed": "true"})

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == completed_task["id"]
    assert data[0]["completed"] is True


def test_get_tasks_filter_completed_false(client):
    payload_1 = {
            "title": "Tarefa concluida",
            "completed": True,
            "priority": "media"
        }
    created_response_1 = client.post("/tasks", json=payload_1)
    assert created_response_1.status_code == 200
    

    payload_2 = {
                "title": "Tarefa pendente",
                "completed": False,
                "priority": "media"
            }
    created_response_2 = client.post("/tasks", json=payload_2)
    assert created_response_2.status_code == 200
    pending_task = created_response_2.json()

    response = client.get("/tasks", params={"completed": "false"})

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == pending_task["id"]
    assert data[0]["completed"] is False


def test_get_tasks_filter_priority(client):
    create_1 = client.post("/tasks", json={
        "title": "Tarefa baixa",
        "completed": False,
        "priority": "baixa"
    })
    assert create_1.status_code == 200

    create_2 = client.post("/tasks", json={
        "title": "Tarefa media",
        "completed": False,
        "priority": "media"
    })
    assert create_2.status_code == 200

    create_3 = client.post("/tasks", json={
        "title": "Tarefa alta",
        "completed": False,
        "priority": "alta"
    })
    assert create_3.status_code == 200
    high_priority_task = create_3.json()

    response = client.get("/tasks", params={"priority": "alta"})
    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == high_priority_task["id"]
    assert data[0]["priority"] == "alta"


def test_get_tasks_filter_completed_and_priority(client):
    create_1 = client.post("/tasks", json={
        "title": "Concluida alta",
        "completed": True,
        "priority": "alta"
    })
    assert create_1.status_code == 200
    expected_task = create_1.json()

    create_2 = client.post("/tasks", json={
        "title": "Concluida baixa",
        "completed": True,
        "priority": "baixa"
    })
    assert create_2.status_code == 200

    create_3 = client.post("/tasks", json={
        "title": "Pendente alta",
        "completed": False,
        "priority": "alta"
    })
    assert create_3.status_code == 200
    
    
    create_4 = client.post("/tasks", json={
        "title": "Pendente baixa",
        "completed": False,
        "priority": "baixa"
    })
    assert create_4.status_code == 200

    response = client.get(
        "/tasks",
        params={"completed": "true", "priority": "alta"}
    )
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == expected_task["id"]
    assert data[0]["completed"] is True
    assert data[0]["priority"] == "alta"


# ------------ POST ---------------

def test_create_task(client):
    payload = {
        "title": "testando",
        "completed": False,
        "priority": "media"
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == payload["title"]
    assert data["completed"] is False
    assert data["priority"] == payload["priority"]
    assert "id" in data


def test_create_task_with_default_values(client):
    payload = {
        "title": "Teste POST"
    }

    response = client.post("/tasks", json=payload)
    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["title"] == payload["title"]
    assert data["completed"] is False
    assert data["priority"] == "media"


def test_create_task_without_title(client):
    payload = {
        "completed": False,
        "priority": "media"
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422


def test_create_task_with_invalid_priority(client):
    payload = {
        "title": "Testar prioridade invalida",
        "completed": False,
        "priority": "urgente",
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422


def test_create_task_with_invalid_completed(client):
    payload = {
        "title": "Testar completed invalido",
        "completed": "invalido",
        "priority": "media",
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422


#-------------- Get por Id --------------------

def test_get_task_by_id(client):
    payload = {
        "title": "Consultar tarefa pelo ID",
        "completed": False,
        "priority": "alta",
    }

    create = client.post("/tasks", json=payload)
    assert create.status_code == 200

    created_task = create.json()

    response = client.get(f"/tasks/{created_task['id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == created_task["id"]
    assert data["title"] == payload["title"]
    assert data["completed"] is False
    assert data["priority"] == payload["priority"]


def test_get_task_by_id_not_found(client):
    response = client.post("/tasks", json={
        "title": "Consultar tarefa pelo ID",
        "completed": False,
        "priority": "alta",
    })

    assert response.status_code == 200

    created_task = response.json()

    deleted_response = client.delete(f"/tasks/{created_task['id']}")
    assert deleted_response.status_code == 200

    get_response = client.get(f"/tasks/{created_task['id']}")

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Tarefa não encontrada"}


def test_get_task_by_id_invalid_id(client):
    response = client.get("/tasks/abc")

    assert response.status_code == 422


#-------------- PUT ---------------

def test_update_task(client):
    payload = {
        "title": "Tarefa original",
        "completed": False,
        "priority": "baixa",
    }
    create = client.post("/tasks", json=payload)

    assert create.status_code == 200
    created_task = create.json()

    update_payload = {
        "title": "Tarefa atualizada",
        "completed": True,
        "priority": "alta",
    }

    response = client.put(
        f"/tasks/{created_task['id']}",
        json=update_payload,
    )
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == created_task["id"]
    assert data["title"] == update_payload["title"]
    assert data["completed"] is True
    assert data["priority"] == update_payload["priority"]

    get_response = client.get(f"/tasks/{created_task['id']}")
    assert get_response.status_code == 200
    updated_task = get_response.json()

    assert updated_task["id"] == created_task["id"]
    assert updated_task["title"] == update_payload["title"]
    assert updated_task["completed"] is True
    assert updated_task["priority"] == update_payload["priority"]


def test_update_task_not_found(client):
    response = client.post("/tasks", json={
        "title": "Consultar tarefa pelo ID",
        "completed": False,
        "priority": "alta",
    })

    assert response.status_code == 200

    created_task = response.json()

    deleted_response = client.delete(f"/tasks/{created_task['id']}")
    assert deleted_response.status_code == 200

    update_payload = {
        "title": "Tentativa de atualizacao",
        "completed": True,
        "priority": "alta",
    }

    response = client.put(
        f"/tasks/{created_task['id']}",
        json=update_payload,
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa não encontrada"}


def test_update_task_without_required_field(client):
    create = client.post("/tasks", json={
        "title": "Omitir campo obrigatorio",
        "completed": False,
        "priority": "alta",
    })
    assert create.status_code == 200 
    created_task = create.json()

    update = client.put(f"/tasks/{created_task['id']}", json= {
            "title": "Tentativa sem prioridade",
            "completed": True,
        })
    assert update.status_code == 422


def test_update_task_with_invalid_priority(client):
    payload = {
        "title": "Tarefa original",
        "completed": False,
        "priority": "baixa",
    }
    create = client.post("/tasks", json=payload)
    assert create.status_code == 200
    created_task = create.json()

    update_payload = {
        "title": "Tentativa de alteracao",
        "completed": True,
        "priority": "urgente",
    }

    update = client.put(f"/tasks/{created_task['id']}", json=update_payload)
    assert update.status_code == 422

    search = client.get(f"/tasks/{created_task['id']}")
    assert search.status_code == 200
    data = search.json()

    assert data["id"] == created_task["id"]
    assert data["title"] == payload["title"]
    assert data["completed"] is False
    assert data["priority"] == payload["priority"]


# ----------------- PATCH status ---------------

def test_update_task_status_to_completed(client):
    payload = {
        "title": "Concluir tarefa",
        "completed": False,
        "priority": "media",
    }
    create = client.post("/tasks", json=payload)
    assert create.status_code == 200
    created_task = create.json()

    update = client.patch(
        f"/tasks/{created_task['id']}/status",
        json={"completed": True},
    )
    assert update.status_code == 200
    data = update.json()

    assert data["id"] == created_task["id"]
    assert data["completed"] is True
    assert data["title"] == payload["title"]
    assert data["priority"] == payload["priority"]

    search = client.get(f"/tasks/{created_task['id']}")
    assert search.status_code == 200
    updated_task = search.json()

    assert updated_task["id"] == created_task["id"]
    assert updated_task["completed"] is True
    assert updated_task["title"] == payload["title"]
    assert updated_task["priority"] == payload["priority"]


def test_update_task_status_to_pending(client):
    payload = {
        "title": "Concluir tarefa",
        "completed": True,
        "priority": "media",
    }
    create = client.post("/tasks", json=payload)
    assert create.status_code == 200
    created_task = create.json()

    update = client.patch(
        f"/tasks/{created_task['id']}/status",
        json={"completed": False},
    )
    assert update.status_code == 200
    data = update.json()

    assert data["id"] == created_task["id"]
    assert data["completed"] is False
    assert data["title"] == payload["title"]
    assert data["priority"] == payload["priority"]

    search = client.get(f"/tasks/{created_task['id']}")
    assert search.status_code == 200
    updated_task = search.json()

    assert updated_task["id"] == created_task["id"]
    assert updated_task["completed"] is False
    assert updated_task["title"] == payload["title"]
    assert updated_task["priority"] == payload["priority"]


def test_update_task_status_not_found(client):
    payload = {
        "title": "Concluir tarefa",
        "completed": False,
        "priority": "media",
    }
    create = client.post("/tasks", json=payload)
    assert create.status_code == 200
    created_task = create.json()

    remove = client.delete(f"/tasks/{created_task['id']}")
    assert remove.status_code == 200

    update = client.patch(
        f"/tasks/{created_task['id']}/status",
        json={"completed": True},
    )

    assert update.status_code == 404
    assert update.json() == {"detail": "Tarefa não encontrada"}

# ----------------- DELETE -------------------
    
def test_delete_task(client):
    create = client.post("/tasks", json={
        "title": "Tarefa valida",
        "completed": False,
        "priority": "media"
    })
    assert create.status_code == 200
    created_task = create.json()

    remove = client.delete(f"/tasks/{created_task['id']}")
    assert remove.status_code == 200

    search = client.get(f"/tasks/{created_task['id']}")

    assert search.status_code == 404
    assert search.json() == {"detail": "Tarefa não encontrada"}


def test_delete_task_not_found(client):
    create = client.post("/tasks", json={
        "title": "Tarefa valida",
        "completed": False,
        "priority": "media"
    })
    assert create.status_code == 200
    created_task = create.json()

    remove = client.delete(f"/tasks/{created_task['id']}")
    assert remove.status_code == 200

    second_remove = client.delete(f"/tasks/{created_task['id']}")

    assert second_remove.status_code == 404
    assert second_remove.json() == {"detail": "Tarefa não encontrada"}