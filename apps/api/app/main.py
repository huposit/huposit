from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session

app = FastAPI(title="Huposit API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db")
async def health_db(
    session: AsyncSession = Depends(get_db_session)
) -> dict[str, str]:

    try:
        await session.execute(text("SELECT 1"))

    except (SQLAlchemyError, OSError) as exc:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "database": "disconnected"
            },
        ) from exc

    return {
        "status": "ok",
        "database": "connected"
    }
