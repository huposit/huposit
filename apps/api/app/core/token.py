from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from app.core.config import settings

ALGORITHM = "HS256"


def create_access_token(user_id: UUID) -> str:
    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(
        minutes=settings.access_token_expire_minutes,
    )

    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": issued_at,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.access_token_secret,
        algorithm=ALGORITHM,
    )
