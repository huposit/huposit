import asyncio
from datetime import UTC, datetime
from uuid import uuid4

from fastapi.testclient import TestClient

import app.features.auth.router as auth_router
import app.features.auth.service as auth_service
from app.features.auth.model import User
from app.main import app


def _user(email: str) -> User:
    return User(
        id=uuid4(),
        email=email,
        email_verified=False,
        password_hash="$argon2id$test",
        created_at=datetime(2026, 7, 1, 12, 0, tzinfo=UTC),
        updated_at=datetime(2026, 7, 1, 12, 0, tzinfo=UTC),
    )


def test_login_route_is_registered() -> None:
    paths = app.openapi()["paths"]

    assert "post" in paths["/auth/login"]
    assert paths["/auth/login"]["post"]["operationId"] == "loginWithEmail"


def test_login_returns_access_token_when_credentials_are_valid(monkeypatch) -> None:
    received: dict[str, str] = {}

    async def fake_authenticate_user(email: str, password: str) -> str:
        received["email"] = email
        received["password"] = password
        return "access-token"

    monkeypatch.setattr(auth_router, "authenticate_user", fake_authenticate_user)

    client = TestClient(app)

    response = client.post(
        "/auth/login",
        json={"email": "USER@example.com", "password": "password-123"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "email": "USER@example.com",
        "access_token": "access-token",
        "message": "Login successful",
    }
    assert received == {
        "email": "USER@example.com",
        "password": "password-123",
    }


def test_login_returns_same_error_when_email_does_not_exist(monkeypatch) -> None:
    async def fake_authenticate_user(email: str, password: str) -> None:
        return None

    monkeypatch.setattr(auth_router, "authenticate_user", fake_authenticate_user)

    client = TestClient(app)

    response = client.post(
        "/auth/login",
        json={"email": "missing@example.com", "password": "password-123"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "email": "missing@example.com",
        "access_token": None,
        "message": "Invalid email or password",
    }


def test_login_returns_same_error_when_password_is_wrong(monkeypatch) -> None:
    async def fake_authenticate_user(email: str, password: str) -> None:
        return None

    monkeypatch.setattr(auth_router, "authenticate_user", fake_authenticate_user)

    client = TestClient(app)

    response = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "email": "user@example.com",
        "access_token": None,
        "message": "Invalid email or password",
    }


def test_authenticate_user_normalizes_email_and_creates_token(monkeypatch) -> None:
    received: dict[str, object] = {}
    user = _user("user@example.com")

    async def fake_get_user_by_email(email: str) -> User:
        received["email"] = email
        return user

    def fake_verify_password(password: str, password_hash: str) -> bool:
        received["password"] = password
        received["password_hash"] = password_hash
        return True

    def fake_create_access_token(user_id) -> str:
        received["user_id"] = user_id
        return "access-token"

    monkeypatch.setattr(auth_service, "get_user_by_email", fake_get_user_by_email)
    monkeypatch.setattr(auth_service, "verify_password", fake_verify_password)
    monkeypatch.setattr(auth_service, "create_access_token", fake_create_access_token)

    token = asyncio.run(
        auth_service.authenticate_user(" USER@example.com ", "password-123")
    )

    assert token == "access-token"
    assert received == {
        "email": "user@example.com",
        "password": "password-123",
        "password_hash": "$argon2id$test",
        "user_id": user.id,
    }


def test_authenticate_user_returns_none_when_email_does_not_exist(
    monkeypatch,
) -> None:
    async def fake_get_user_by_email(email: str) -> None:
        return None

    monkeypatch.setattr(auth_service, "get_user_by_email", fake_get_user_by_email)

    token = asyncio.run(
        auth_service.authenticate_user("missing@example.com", "password-123")
    )

    assert token is None


def test_authenticate_user_returns_none_when_password_is_wrong(
    monkeypatch,
) -> None:
    user = _user("user@example.com")

    async def fake_get_user_by_email(email: str) -> User:
        return user

    def fake_verify_password(password: str, password_hash: str) -> bool:
        return False

    monkeypatch.setattr(auth_service, "get_user_by_email", fake_get_user_by_email)
    monkeypatch.setattr(auth_service, "verify_password", fake_verify_password)

    token = asyncio.run(
        auth_service.authenticate_user("user@example.com", "wrong-password")
    )

    assert token is None
