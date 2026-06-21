from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import DbSession


async def check_database_connection(session: DbSession) -> bool:
    try:
        await session.execute(text("SELECT 1"))
    except (SQLAlchemyError, OSError):
        return False

    return True
