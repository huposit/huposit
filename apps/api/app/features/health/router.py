from fastapi import APIRouter

from app.db.session import DbSession
from app.features.health.schema import (
    DatabaseHealthResponse,
    HealthResponse,
    WorkerHealthResponse,
)
from app.features.health.service import (
    build_database_health,
    build_health,
    build_worker_health,
)

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "",
    response_model=HealthResponse,
    operation_id="getServerHealth",
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


@router.get(
    "/worker",
    response_model=WorkerHealthResponse,
    operation_id="getWorkerHealth",
)
def health_worker() -> WorkerHealthResponse:
    return build_worker_health()
