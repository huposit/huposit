from app.db.session import DbSession
from app.features.health.repository import check_database_connection
from app.features.health.schema import DatabaseHealthResponse, HealthResponse


def build_health() -> HealthResponse:
    return HealthResponse(status="ok")


async def build_database_health(session: DbSession) -> DatabaseHealthResponse:
    result = await check_database_connection(session)

    return DatabaseHealthResponse(
        status="ok" if result else "error",
        database="connected" if result else "disconnected",
    )
