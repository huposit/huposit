from fastapi import APIRouter

from app.features.auth.schema import SignupRequest, SignupResponse
from app.features.auth.service import signup_with_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=SignupResponse,
    operation_id="signupWithEmail",
)
async def signup(request: SignupRequest) -> SignupResponse:

    created_user = await signup_with_email(
        email=request.email,
        password=request.password
    )

    return SignupResponse(
        status="success",
        email=created_user.email,
        email_verified=created_user.email_verified,
        message="User created successfully"
    )
