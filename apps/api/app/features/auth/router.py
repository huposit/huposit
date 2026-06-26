from fastapi import APIRouter

from app.features.auth.schema import SignupRequest, SignupResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=SignupResponse,
    operation_id="signupWithEmail",
)
async def signup(request: SignupRequest) -> SignupResponse:
    print(
        "[auth.signup] received",
        {"email": request.email, "password_length": len(request.password)},
    )

    return SignupResponse(
        status="success",
        email=request.email,
        email_verified=False,
        message="회원가입 요청을 받았습니다.",
    )
