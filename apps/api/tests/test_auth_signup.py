from fastapi.testclient import TestClient

from app.main import app


def test_signup_route_is_registered() -> None:
    paths = app.openapi()["paths"]

    assert "post" in paths["/auth/signup"]
    assert paths["/auth/signup"]["post"]["operationId"] == "signupWithEmail"


def test_signup_receives_user_create_request(capsys) -> None:
    client = TestClient(app)

    response = client.post(
        "/auth/signup",
        json={"email": "USER@example.com", "password": "password-123"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "email": "USER@example.com",
        "email_verified": False,
        "message": "회원가입 요청을 받았습니다.",
    }

    stdout = capsys.readouterr().out

    assert "[auth.signup] received" in stdout
    assert "USER@example.com" in stdout
    assert "password-123" not in stdout
