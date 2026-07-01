
from app.core.security import hash_password, verify_password
from app.core.token import create_access_token
from app.features.auth.error import DuplicateEmailError
from app.features.auth.model import User
from app.features.auth.repository import create_user, email_exists, get_user_by_email, get_users


async def signup_with_email(*, email: str, password: str) -> User:
    norm_email = email.strip().lower()

    if await email_exists(norm_email):
        raise DuplicateEmailError(norm_email)

    hashed_pass = hash_password(password)
    return await create_user(norm_email, hashed_pass)


async def get_all_users() -> list[User]:
    return await get_users()


async def authenticate_user(email: str, password: str) -> str | None:
    norm_email = email.strip().lower()
    user = await get_user_by_email(norm_email)

    if user is None:
        return None

    if user.password_hash and verify_password(password, user.password_hash):
        return create_access_token(user.id)

    return None
