from fastapi import APIRouter

from app.db.session import DbSession
from app.features.health.schema import DatabaseHealthResponse, HealthResponse
from app.features.health.service import build_database_health, build_health

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "",
    response_model=HealthResponse,
    operation_id="getHealth",
)
def health() -> HealthResponse:
    return build_health()


@router.get(
    "/db",
    response_model=DatabaseHealthResponse,
    operation_id="getDatabaseHealth",
)
async def health_db(session: DbSession) -> DatabaseHealthResponse:
    return await build_database_health(session)
