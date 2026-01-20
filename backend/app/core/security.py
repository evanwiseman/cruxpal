import secrets
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from backend.app.core.config import settings

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_jwt_token(
    subject: str,
    expires_delta: timedelta = timedelta(minutes=settings.JWT_TOKEN_EXPIRE_MINUTES),
) -> str:
    payload = {
        "sub": subject,
        "exp": datetime.utcnow() + expires_delta,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token() -> str:
    return secrets.token_urlsafe(32)
