from datetime import UTC, datetime
from uuid import uuid4

from fastapi.testclient import TestClient

import app.features.auth.router as auth_router
from app.features.auth.error import DuplicateEmailError
from app.features.auth.model import User
from app.main import app


def _user(email: str) -> User:
    return User(
        id=uuid4(),
        email=email,
        email_verified=False,
        password_hash="$argon2id$test",
        created_at=datetime(2026, 6, 27, 12, 0, tzinfo=UTC),
        updated_at=datetime(2026, 6, 27, 12, 0, tzinfo=UTC),
    )


def test_signup_route_is_registered() -> None:
    paths = app.openapi()["paths"]

    assert "post" in paths["/auth/signup"]
    assert paths["/auth/signup"]["post"]["operationId"] == "signupWithEmail"
    assert "get" in paths["/auth/users"]
    assert paths["/auth/users"]["get"]["operationId"] == "getUsersInfo"


def test_signup_receives_user_create_request(monkeypatch) -> None:
    received: dict[str, str] = {}

    async def fake_signup_with_email(*, email: str, password: str) -> User:
        received["email"] = email
        received["password"] = password
        return _user(email.lower())

    monkeypatch.setattr(auth_router, "signup_with_email", fake_signup_with_email)

    client = TestClient(app)

    response = client.post(
        "/auth/signup",
        json={"email": "USER@example.com", "password": "password-123"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "email": "user@example.com",
        "email_verified": False,
        "message": "User created successfully",
    }
    assert received == {
        "email": "USER@example.com",
        "password": "password-123",
    }


def test_signup_returns_error_when_email_is_duplicate(monkeypatch) -> None:
    async def fake_signup_with_email(*, email: str, password: str) -> User:
        raise DuplicateEmailError(email.lower())

    monkeypatch.setattr(auth_router, "signup_with_email", fake_signup_with_email)

    client = TestClient(app)

    response = client.post(
        "/auth/signup",
        json={"email": "USER@example.com", "password": "password-123"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "email": "user@example.com",
        "email_verified": False,
        "message": "이미 가입된 이메일입니다.",
    }


def test_get_users_info_returns_user_list(monkeypatch) -> None:
    async def fake_get_all_users() -> list[User]:
        return [_user("user@example.com")]

    monkeypatch.setattr(auth_router, "get_all_users", fake_get_all_users)

    client = TestClient(app)

    response = client.get("/auth/users")

    assert response.status_code == 200

    body = response.json()
    assert len(body) == 1
    assert body[0]["email"] == "user@example.com"
    assert body[0]["email_verified"] is False
    assert body[0]["id"]
    assert body[0]["created_at"]
