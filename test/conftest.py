from pathlib import Path

from dotenv import dotenv_values

from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import sessionmaker

import pytest
from app.models import Task

ROOT_DIR = Path(__file__).resolve().parent.parent
TEST_ENV_FILE = ROOT_DIR / ".env.test"

if not TEST_ENV_FILE.is_file():
    raise RuntimeError("Arquivo .env.test não encontrado")

test_config = dotenv_values(TEST_ENV_FILE)

if test_config.get("DB_NAME") != "taskmanager_test":
    raise RuntimeError("Testes bloqueados: DB_NAME deve ser taskmanager_test")


test_database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=test_config["DB_USER"],
    password=test_config["DB_PASSWORD"],
    host=test_config["DB_HOST"],
    port=int(test_config["DB_PORT"]),
    database=test_config["DB_NAME"],
)

test_engine = create_engine(test_database_url)

if test_engine.url.database != "taskmanager_test":
    raise RuntimeError("Testes bloqueados: o engine não aponta para taskmanager_test")


@pytest.fixture(scope="session")
def db_engine():
    try:
        with test_engine.begin() as conn:
            database_name = conn.execute(text("SELECT current_database()")).scalar_one()

            if database_name != "taskmanager_test":
                raise RuntimeError("Conexão bloqueada: banco diferente de taskmanager_test")

            Task.__table__.create(bind=conn, checkfirst=True)
        yield test_engine
    finally:
        test_engine.dispose()



@pytest.fixture
def db_session_factory(db_engine, monkeypatch):
    from app import crud_postgres

    with db_engine.connect() as conn:
        transaction = conn.begin()

        try:
            test_session_factory = sessionmaker(
                bind=conn,
                join_transaction_mode="create_savepoint",
            )

            monkeypatch.setattr(
                crud_postgres,
                "SessionLocal",
                test_session_factory,
            )

            yield test_session_factory
        finally:
            transaction.rollback()

from fastapi.testclient import TestClient

@pytest.fixture
def client(db_session_factory):
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client