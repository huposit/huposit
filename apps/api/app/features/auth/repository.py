from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.session import AsyncSessionLocal
from app.features.auth.error import DuplicateEmailError
from app.features.auth.model import User


async def email_exists(email: str) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User.id)
            .where(User.email == email)
            .limit(1)
        )
        return result.scalar_one_or_none() is not None


async def create_user(email: str, hash_pass: str) -> User:
    user = User(
        email=email,
        password_hash=hash_pass,
        email_verified=False,
    )

    async with AsyncSessionLocal() as session:
        session.add(user)

        try:
            await session.commit()
            return user

        except IntegrityError as exc:
            await session.rollback()
            raise DuplicateEmailError(email) from exc


async def get_users() -> list[User]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User)
            .order_by(User.created_at.desc())
            .limit(50)
        )
        return list(result.scalars().all())
