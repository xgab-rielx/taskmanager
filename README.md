# TaskManager API

API REST para gerenciamento de tarefas, desenvolvida com FastAPI e SQLite.

## Funcionalidades

- Criar tarefas
- Listar tarefas
- Buscar tarefa por ID
- Atualizar tarefas
- Excluir tarefas
- Definir prioridade: baixa, media ou alta
- Marcar tarefas como concluídas
- Validação automática com Pydantic
- Testes automatizados com pytest

## Tecnologias

- Python
- FastAPI
- SQLite
- Pydantic
- pytest
- HTTPX

## Como executar

Clone o repositório:

```bash
git clone [https://github.com/xgab-rielx/taskmanager.git](https://github.com/xgab-rielx/taskmanager.git)
cd taskmanager
```

Crie e ative o ambiente virtual:

```bash
python -m venv venv
```

No Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Inicie a API:

```bash
uvicorn app.main:app --reload
```

Acesse a documentação interativa:

```text
http://127.0.0.1:8000/docs
```

## Testes

Execute:

```bash
python -m pytest
```

A suíte possui testes de CRUD, validações de entrada, erros 404 e isolamento do banco de testes.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/tasks` | Lista todas as tarefas |
| POST | `/tasks` | Cria uma tarefa |
| GET | `/tasks/{task_id}` | Busca uma tarefa por ID |
| PUT | `/tasks/{task_id}` | Atualiza uma tarefa |
| DELETE | `/tasks/{task_id}` | Exclui uma tarefa |

## Exemplo de criação

```json
{
  "title": "Estudar Docker",
  "priority": "alta"
}
```