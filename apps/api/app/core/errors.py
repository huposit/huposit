
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.features.auth.error import DuplicateEmailError
from app.features.auth.schema import SignupResponse


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DuplicateEmailError)
    async def duplicate_email_handler(
        request: Request,
        exc: DuplicateEmailError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=200,
            content=SignupResponse(
                status="error",
                email=exc.email,
                email_verified=False,
                message="이미 가입된 이메일입니다.",
            ).model_dump(mode="json"),
        )
