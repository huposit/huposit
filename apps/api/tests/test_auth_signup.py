from fastapi.testclient import TestClient

import app.features.auth.router as auth_router
from app.features.auth.error import DuplicateEmailError
from app.features.auth.model import User
from app.main import app


def _user(email: str) -> User:
    return User(
        email=email,
        email_verified=False,
        password_hash="$argon2id$test",
    )


def test_signup_route_is_registered() -> None:
    paths = app.openapi()["paths"]

    assert "post" in paths["/auth/signup"]
    assert paths["/auth/signup"]["post"]["operationId"] == "signupWithEmail"


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
