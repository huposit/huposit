
from app.core.security import hash_password
from app.features.auth.error import DuplicateEmailError
from app.features.auth.model import User
from app.features.auth.repository import create_user, email_exists, get_users


async def signup_with_email(*, email: str, password: str) -> User:
    norm_email = email.strip().lower()

    if await email_exists(norm_email):
        raise DuplicateEmailError(norm_email)

    hashed_pass = hash_password(password)
    return await create_user(norm_email, hashed_pass)


async def get_all_users() -> list[User]:
    return await get_users()