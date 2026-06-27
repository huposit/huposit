from fastapi import APIRouter

from app.features.auth.schema import SignupRequest, SignupResponse, UserInfoResponse
from app.features.auth.service import get_all_users, signup_with_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=SignupResponse,
    operation_id="signupWithEmail",
)
async def signup(request: SignupRequest) -> SignupResponse:
    created_user = await signup_with_email(
        email=request.email,
        password=request.password,
    )

    return SignupResponse(
        status="success",
        email=created_user.email,
        email_verified=created_user.email_verified,
        message="User created successfully",
    )


@router.get(
    "/users",
    response_model=list[UserInfoResponse],
    operation_id="getUsersInfo",
)
async def get_users_info() -> list[UserInfoResponse]:
    users = await get_all_users()

    return [
        UserInfoResponse(
            id=str(user.id),
            email=user.email,
            email_verified=user.email_verified,
            created_at=user.created_at,
        )
        for user in users
    ]
