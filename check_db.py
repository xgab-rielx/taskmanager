from sqlalchemy import text

from app.db_session import engine


with engine.connect() as connection:
    result = connection.execute(
        text("SELECT current_user, current_database()")
    )
    user, database = result.one()

    print(f"Usuário: {user}")
    print(f"Banco: {database}")

engine.dispose()