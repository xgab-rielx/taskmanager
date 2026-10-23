


# TaskManager API

API REST para gerenciamento de tarefas, desenvolvida com FastAPI, PostgreSQL e SQLAlchemy.

Projeto de estudos com foco em desenvolvimento de APIs, persistência de dados, validação de entrada e testes automatizados.

## Funcionalidades

- Criar tarefas.
- Listar tarefas.
- Filtrar tarefas por conclusão e prioridade.
- Combinar os filtros de conclusão e prioridade.
- Consultar uma tarefa pelo ID.
- Atualizar título, conclusão e prioridade.
- Alterar somente o status de conclusão.
- Excluir tarefas.
- Validar os dados de entrada com Pydantic.
- Executar testes de integração com um banco PostgreSQL separado.

## Tecnologias

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- psycopg2
- Pydantic
- python-dotenv
- pytest
- HTTPX / TestClient
- Uvicorn

## Pré-requisitos

- Python instalado.
- Git instalado.
- PostgreSQL instalado e em execução.
- Acesso ao PostgreSQL para criar bancos e configurar permissões.

Os comandos de ativação do ambiente virtual abaixo usam Windows PowerShell.

## Como executar

### 1. Clonar o repositório

```powershell
git clone https://github.com/xgab-rielx/taskmanager.git
cd taskmanager
```

### 2. Criar e ativar o ambiente virtual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 4. Preparar o banco de desenvolvimento

Crie um banco PostgreSQL para a aplicação, por exemplo:

```sql
CREATE DATABASE taskmanager;
```

Esse comando deve ser executado no PostgreSQL, usando uma conta com permissão para criar bancos.

O usuário utilizado pela aplicação precisa conseguir conectar ao banco e criar as tabelas no schema escolhido.

Se necessário, conecte-se especificamente ao banco `taskmanager` como administrador ou proprietário do schema e execute:

```sql
GRANT USAGE, CREATE ON SCHEMA public TO usuario_da_aplicacao;
```

Substitua `usuario_da_aplicacao` pelo usuário real. Esse comando não cria o usuário nem concede automaticamente permissões sobre tabelas pertencentes a outras contas.

### 5. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```dotenv
DB_USER=usuario_da_aplicacao
DB_PASSWORD=sua_senha_local
DB_HOST=localhost
DB_PORT=5432
DB_NAME=taskmanager
```

Ajuste os valores de acordo com sua instalação do PostgreSQL.

Não envie o arquivo `.env` com credenciais para o GitHub.

### 6. Criar as tabelas

Na raiz do projeto, execute:

```powershell
python create_tables.py
```

Esse script usa a configuração do banco da aplicação para criar as tabelas que ainda não existem e exibir suas colunas.

O banco PostgreSQL deve existir antes da execução. O script cria tabelas, não o banco em si, e não substitui um sistema de migrações de schema.

### 7. Iniciar a API

```powershell
python -m uvicorn app.main:app --reload
```

Documentação interativa:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/tasks` | Lista tarefas e permite aplicar filtros |
| POST | `/tasks` | Cria uma tarefa |
| GET | `/tasks/{task_id}` | Consulta uma tarefa pelo ID |
| PUT | `/tasks/{task_id}` | Atualiza título, conclusão e prioridade |
| PATCH | `/tasks/{task_id}/status` | Atualiza somente o status de conclusão |
| DELETE | `/tasks/{task_id}` | Exclui uma tarefa |

## Exemplos de uso

Os corpos JSON podem ser enviados pela documentação interativa em `/docs`.

### Criar uma tarefa

`POST /tasks`

```json
{
  "title": "Estudar Docker",
  "completed": false,
  "priority": "alta"
}
```

Somente `title` é obrigatório na criação.

Se os campos opcionais forem omitidos, os valores padrão são:

- `completed`: `false`
- `priority`: `"media"`

Exemplo mínimo:

```json
{
  "title": "Praticar testes automatizados"
}
```

Prioridades permitidas:

- `"baixa"`
- `"media"`
- `"alta"`

### Listar e filtrar tarefas

Listar todas:

```text
GET /tasks
```

Listar somente concluídas:

```text
GET /tasks?completed=true
```

Listar somente pendentes:

```text
GET /tasks?completed=false
```

Filtrar por prioridade:

```text
GET /tasks?priority=alta
```

Combinar os filtros:

```text
GET /tasks?completed=true&priority=alta
```

### Consultar pelo ID

```text
GET /tasks/1
```

O ID acima é ilustrativo. Use o ID retornado ao criar uma tarefa.

### Atualizar uma tarefa

`PUT /tasks/{task_id}`

O corpo exige os três campos:

```json
{
  "title": "Estudar Docker e executar os exemplos",
  "completed": true,
  "priority": "alta"
}
```

### Atualizar somente o status

`PATCH /tasks/{task_id}/status`

```json
{
  "completed": true
}
```

Para voltar a tarefa para pendente:

```json
{
  "completed": false
}
```

### Excluir uma tarefa

```text
DELETE /tasks/{task_id}
```

### Respostas de erro

As rotas de consulta individual, atualização e exclusão retornam `404` quando a tarefa não existe:

```json
{
  "detail": "Tarefa não encontrada"
}
```

Requisições que não atendem ao schema, como título obrigatório ausente, prioridade inválida ou ID não inteiro, retornam `422`.

## Testes automatizados

A suíte possui 24 testes de integração:

| Bloco | Quantidade |
|---|---:|
| Listagem e filtros | 7 |
| Criação e validação | 5 |
| Consulta por ID | 3 |
| Atualização com PUT | 4 |
| Atualização de status com PATCH | 3 |
| Exclusão | 2 |
| Total | 24 |

Os testes utilizam PostgreSQL real, separado do banco da aplicação.

### 1. Criar o banco de testes

No PostgreSQL, usando uma conta com permissão para criar bancos:

```sql
CREATE DATABASE taskmanager_test;
```

O nome precisa ser exatamente `taskmanager_test`, pois a configuração dos testes bloqueia outros nomes.

### 2. Configurar as permissões

O usuário dos testes precisa conseguir conectar ao banco e criar a tabela utilizada pela suíte.

Se necessário, conecte-se especificamente ao banco `taskmanager_test` como administrador ou proprietário do schema e execute:

```sql
GRANT USAGE, CREATE ON SCHEMA public TO usuario_dos_testes;
```

Substitua `usuario_dos_testes` pelo usuário configurado no arquivo `.env.test`.

Conceder permissões no schema `public` de outro banco não configura o schema `public` de `taskmanager_test`.

### 3. Criar o arquivo `.env.test`

Na raiz do projeto:

```dotenv
DB_USER=usuario_dos_testes
DB_PASSWORD=sua_senha_local_de_testes
DB_HOST=localhost
DB_PORT=5432
DB_NAME=taskmanager_test
```

Não envie esse arquivo com credenciais para o GitHub.

Mantenha também o `.env` da aplicação configurado: os módulos da aplicação carregam essa configuração durante a importação, mesmo quando os testes substituem a fábrica de sessões do CRUD.

### 4. Executar os testes

Na raiz do projeto, com o ambiente virtual ativado:

```powershell
python -m pytest test/test_tasks.py -v
```

Não é necessário iniciar o Uvicorn para executar os testes.

A fixture cria a tabela `tasks` no banco de testes caso ela ainda não exista. Não é necessário executar `create_tables.py` para preparar essa tabela de testes.

### Isolamento dos testes

A configuração em `test/conftest.py`:

- Lê as credenciais do `.env.test`.
- Exige `DB_NAME=taskmanager_test`.
- Confere o nome do banco na conexão real.
- Substitui a fábrica de sessões usada pelo CRUD.
- Abre uma transação externa para cada teste.
- Usa savepoints nas sessões.
- Executa rollback da transação externa ao final.

As alterações feitas por meio dessas sessões durante cada teste são desfeitas ao terminar.

Use um banco dedicado aos testes e inicialmente sem tarefas. O rollback não apaga dados que já existiam antes da execução.

## Estrutura do projeto

```text
taskmanager/
├── app/
│   ├── __init__.py
│   ├── crud_postgres.py
│   ├── db_session.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── test/
│   ├── conftest.py
│   └── test_tasks.py
├── .gitignore
├── create_tables.py
├── README.md
└── requirements.txt
```

Os arquivos `.env` e `.env.test` devem ser criados localmente e não devem ser publicados com credenciais.

## Observações

- A implementação atual utiliza PostgreSQL; o CRUD legado de SQLite foi removido.
- A inicialização da API não cria automaticamente as tabelas do PostgreSQL.
- Execute os comandos a partir da raiz do projeto.
- O projeto foi desenvolvido para estudos e evolução prática de uma API REST.