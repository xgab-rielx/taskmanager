from sqlalchemy import inspect

from app.db_session import Base, engine
from app.models import Task

if __name__ == "__main__":
    Base.metadata.create_all(engine)

    inspector = inspect(engine)
    columns = inspector.get_columns(Task.__tablename__)

    print(f"Tabela: {Task.__tablename__}")

    for column in columns:
        print(f"{column['name']}: {column['type']}")

    engine.dispose()
