from app.features.health.router import health, health_worker
from app.main import app


def test_health_routes_are_registered() -> None:
    paths = app.openapi()["paths"]

    assert "get" in paths["/health"]
    assert "get" in paths["/health/worker"]


def test_health_returns_ok() -> None:
    assert health().model_dump() == {"status": "ok"}


def test_worker_health_returns_api_placeholder() -> None:
    assert health_worker().model_dump() == {
        "status": "ok",
        "worker": "available",
        "mode": "api_placeholder",
    }
