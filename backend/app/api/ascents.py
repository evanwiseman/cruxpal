from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.athletes import require_athlete
from backend.app.api.routes import require_route
from backend.app.core.endpoints import endpoints
from backend.app.db.models.ascent import Ascent
from backend.app.db.session import get_db
from backend.app.schemas.ascent import AscentCreate, AscentRead, AscentUpdate

router = APIRouter()
routes = endpoints.AscentsRoutes()

async def require_ascent(ascent_id: int, db: AsyncSession) -> Ascent:
    ascent = await db.get(Ascent, ascent_id)
    if not ascent:
        raise HTTPException(status_code=404, detail="Ascent not found")
    return ascent


@router.post(routes.CREATE, response_model=AscentRead)
async def create_ascent(payload: AscentCreate, db: AsyncSession = Depends(get_db)):
    await require_athlete(payload.athlete_id, db)
    await require_route(payload.route_id, db)

    ascent = Ascent(
        athlete_id=payload.athlete_id,
        route_id=payload.route_id,
        sent=payload.sent,
        attempt=payload.attempt,
        notes=payload.notes,
    )

    db.add(ascent)
    await db.commit()
    await db.refresh(ascent)
    return ascent


@router.get(routes.LIST, response_model=List[AscentRead])
async def get_all_ascents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ascent))
    ascents = result.scalars().all()
    return ascents


@router.get(routes.GET_BY_ID, response_model=AscentRead)
async def get_ascent(ascent_id: int, db: AsyncSession = Depends(get_db)):
    ascent = await require_ascent(ascent_id, db)
    return ascent


@router.put(routes.UPDATE, response_model=AscentRead)
async def update_ascent(
    ascent_id: int, payload: AscentUpdate, db: AsyncSession = Depends(get_db)
):
    ascent = await require_ascent(ascent_id, db)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(ascent, field, value)

    await db.commit()
    await db.refresh(ascent)

    return ascent


@router.delete(routes.DELETE, status_code=status.HTTP_204_NO_CONTENT)
async def delete_ascent(ascent_id: int, db: AsyncSession = Depends(get_db)):
    ascent = await require_ascent(ascent_id, db)

    await db.delete(ascent)
    await db.commit()