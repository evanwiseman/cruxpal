import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_user
from backend.app.core.config import settings
from backend.app.core.security import (
    create_jwt_token,
    create_refresh_token,
    hash_password,
)
from backend.app.db.models.token import RefreshToken
from backend.app.db.models.user import User
from backend.app.db.session import get_db
from backend.app.schemas.token import Token
from backend.app.schemas.user import UserCreate
from backend.app.services.auth import authenticate_user
from backend.app.utils.time import utc_now

router = APIRouter()
logger = logging.getLogger(__name__)


# At the top with your other imports
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.get("/debug-token")
async def debug_token(token: str = Depends(oauth2_scheme)):
    """Debug: Check if token is being received"""
    return {"token_preview": token[:30] + "...", "token_length": len(token)}


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return user


@router.post("/refresh", response_model=Token)
async def refresh(refresh_token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token == refresh_token,
            RefreshToken.revoked.is_(False),
        )
    )
    token = result.scalar_one_or_none()

    if not token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token.expires_at < utc_now():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    # Revoke old token
    token.revoked = True

    # Create new tokens
    new_refresh = create_refresh_token()
    db.add(
        RefreshToken(
            user_id=token.user_id,
            token=new_refresh,
            expires_at=utc_now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
    )

    jwt_token = create_jwt_token(subject=str(token.user_id))

    await db.commit()

    return {
        "access_token": jwt_token,
        "refresh_token": new_refresh,
        "token_type": "bearer",
    }


@router.post("/signup")
async def signup(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    await db.commit()
    logger.info(f'successfully signed up {{"email": "{user.email}"}}')
    return {"message": "ok"}


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # Changed from payload: LoginRequest
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(
        form_data.username,  # OAuth2 uses 'username' field, but you can use it for email
        form_data.password,
        db,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jwt_token = create_jwt_token(subject=str(user.id))
    refresh_token = create_refresh_token()

    db.add(
        RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=utc_now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
    )

    await db.commit()
    logger.info(f'successfully logged in {{"email": "{user.email}"}}')

    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }