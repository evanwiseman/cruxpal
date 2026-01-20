from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
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
from backend.app.schemas.auth import LoginRequest
from backend.app.schemas.token import Token
from backend.app.schemas.user import UserCreate
from backend.app.services.auth import authenticate_user
from backend.app.utils.time import utc_now

router = APIRouter()


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
    return {"message": "ok"}


@router.post("/login")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(
        payload.email,
        payload.password,
        db,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
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

    return {
        "access_token": jwt_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
