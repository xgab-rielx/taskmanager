const taskForm = document.getElementById("task-form");
const taskTitle = document.getElementById("task-title");
const taskPriority = document.getElementById("task-priority");
const taskList = document.getElementById("task-list");
const feedback = document.getElementById("feedback");
const createTaskButton = document.getElementById("create-task-button");
const cancelEditButton = document.getElementById("cancel-edit-button");
const statusFilter = document.getElementById("status-filter");
const priorityFilter = document.getElementById("priority-filter");
const taskCounter = document.getElementById("task-counter");

let editingTask  = null;

function showMessage(message, type) {
    feedback.textContent = message;
    feedback.className = type;
}

function updateCounter(tasks) {
    const completedTasks = tasks.filter(function (task) {
        return task.completed;
    });

    const pendingTasks = tasks.length - completedTasks.length;

    taskCounter.textContent =
        `Exibidas: ${tasks.length} | ` +
        `Pendentes: ${pendingTasks} | ` +
        `Concluídas: ${completedTasks.length}`;
}

function renderTasks(tasks) {
    taskList.replaceChildren();
    
    updateCounter(tasks);

    if (tasks.length === 0) {
        const message = document.createElement("li");
        message.textContent = "Nenhuma tarefa encontrada para este filtro.";
        taskList.append(message);
        return;
    }

    tasks.forEach(function (task) {
        const item = document.createElement("li");
        const label = document.createElement("label");
        const checkbox = document.createElement("input");
        const text = document.createElement("span");

        checkbox.type = "checkbox";
        checkbox.checked = task.completed;

        text.textContent = `${task.title} - Prioridade: ${task.priority}`;

        checkbox.addEventListener("change", async function () {
            const previousCompleted = task.completed;
            const completed = checkbox.checked;

            checkbox.disabled = true;

            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/tasks/${task.id}/status`,
                    {
                        method: "PATCH",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            completed: completed
                        })
                    }
                );

                if (!response.ok) {
                    const errorDetails = await response.text();

                    throw new Error(
                        `Erro ${response.status}: ${errorDetails}`
                    );
                }

                const updatedTask = await response.json();

                task.completed = updatedTask.completed;
                checkbox.checked = updatedTask.completed;

                console.log("Status atualizado:", updatedTask);

                showMessage(
                    updatedTask.completed
                        ? "Tarefa concluída!"
                        : "Tarefa marcada como pendente.",
                    "success"
                );

                await loadTasks();

            } catch (error) {
                checkbox.checked = previousCompleted;

                console.error(
                    "Não foi possível atualizar o status:",
                    error
                );

                showMessage(
                    "Não foi possivel atualizar o status. Tente novamente.",
                    "error"
                );
            } finally {
                checkbox.disabled = false;
            }
        });

        const deleteButton = document.createElement("button");

        deleteButton.type = "button";
        deleteButton.textContent = "Excluir";
        deleteButton.classList.add("delete-button");

        deleteButton.addEventListener("click", async function () {
            const confirmed = window.confirm(
                `Excluir a tarefa "${task.title}"?`
            );

            if (!confirmed) {
                return;
            }

            deleteButton.disabled = true;

            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/tasks/${task.id}`,
                    {
                        method: "DELETE"
                    }
                );

                if (!response.ok) {
                    const errorDetails = await response.text();

                    throw new Error(
                        `Erro ${response.status}: ${errorDetails}`
                    );
                }

                console.log("Tarefa excluída. ID:", task.id);

                showMessage("Tarefa excluída com sucesso!", "success");

                await loadTasks();
            } catch (error) {
                console.error(
                    "Não foi possivel excluir a tarefa:",
                    error
                );

                showMessage(
                    "Não foi possível excluir a tarefa. Tente novamente.",
                    "error"
                );
            } finally {
                deleteButton.disabled = false;
            }
        });

        const editButton = document.createElement("button");

        editButton.type = "button";
        editButton.textContent = "Editar";
        editButton.classList.add("edit-button");

        editButton.addEventListener("click", function () {
            if (createTaskButton.disabled) {
                return;
            }

            editingTask = task;

            taskTitle.value = task.title;
            taskPriority.value = task.priority;

            createTaskButton.textContent = "Salvar alterações";
            cancelEditButton.hidden = false;

            showMessage("Modo de edição ativado.", "success");

            taskTitle.focus();

        });

        label.append(checkbox, text);
        item.append(label, editButton, deleteButton);
        taskList.append(item);
    });
}

async function loadTasks() {
    try {
        const params = new URLSearchParams();

        if (statusFilter.value !== "") {
            params.set("completed", statusFilter.value);
        }

        if (priorityFilter.value !== "") {
            params.set("priority", priorityFilter.value);
        }

        const query = params.toString();

        const url = query
            ? `http://127.0.0.1:8000/tasks?${query}`
            : "http://127.0.0.1:8000/tasks";

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`Erro ${response.status}`);
        }

        const tasks = await response.json();

        renderTasks(tasks);
    } catch (error) {
        console.error(
            "Não foi possível carregar as tarefas:",
            error
        );
    }
}

loadTasks();

statusFilter.addEventListener("change", function () {
    loadTasks();
});

priorityFilter.addEventListener("change", function () {
    loadTasks();
});

taskForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    if (createTaskButton.disabled) {
        return;
    }

    const isEditing = editingTask !== null;
    const title = taskTitle.value;
    const priority = taskPriority.value;

    const task = {
        title: title,
        completed: isEditing ? editingTask.completed : false,
        priority: priority
    };

    const url = isEditing
        ? `http://127.0.0.1:8000/tasks/${editingTask.id}`
        : "http://127.0.0.1:8000/tasks";

    const method = isEditing ? "PUT" : "POST";

    createTaskButton.disabled = true;
    cancelEditButton.disabled = true;

    createTaskButton.textContent = isEditing
    ? "Salvando..."
    : "Criando...";

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(task)
        });

        if (!response.ok) {
            const errorDetails = await response.text();

            throw new Error(
                `Erro ${response.status}: ${errorDetails}`
            );
        }

        const savedTask = await response.json();

        console.log("Tarefa salva", savedTask);

        showMessage(
            isEditing
                ? "Tarefa atualizada com sucesso!"
                : "Tarefa criada com sucesso!",
            "success"
        );

        editingTask = null;
        taskForm.reset();
        cancelEditButton.hidden = true;

        await loadTasks();
    } catch (error) {
        console.error("Não foi possivel salvar a tarefa:", error);

        showMessage(
            isEditing
                ? "Não foi possivel atualizar a tarefa. Tente novamente."
                : "Não foi possivel criar a tarefa. Tente novamente.",
            "error"
        );
    } finally {
        createTaskButton.disabled = false;
        cancelEditButton.disabled = false;

        createTaskButton.textContent = editingTask !== null
            ? "Salvar alterações"
            : "Criar tarefa";
    }
});

    

cancelEditButton.addEventListener("click", function () {
    editingTask = null;

    taskForm.reset();

    createTaskButton.textContent = "Criar tarefa";
    cancelEditButton.hidden = true;

    feedback.textContent = "";
    feedback.className = "";
});