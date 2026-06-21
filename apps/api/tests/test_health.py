from app.main import app, health


def test_health_route_is_registered() -> None:
    route = next(
        route for route in app.routes if getattr(route, "path", None) == "/health"
    )

    assert "GET" in getattr(route, "methods", set())


def test_health_returns_ok() -> None:
    assert health() == {"status": "ok"}
