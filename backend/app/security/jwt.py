from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.core.config import settings


ALGORITHM = "HS256"


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=ALGORITHM
    )


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[ALGORITHM]
        )

        return payload.get("sub")

    except JWTError:
        return None