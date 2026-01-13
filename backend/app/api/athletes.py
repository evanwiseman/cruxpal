from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.models.ascent import Ascent
from backend.app.db.models.athlete import Athlete
from backend.app.db.models.route import Route
from backend.app.db.session import get_db
from backend.app.schemas.ascent import AscentRead
from backend.app.schemas.athlete import AthleteCreate, AthleteRead, AthleteUpdate
from backend.app.schemas.route import RouteRead

router = APIRouter()


async def require_athlete(athlete_id: int, db: AsyncSession) -> Athlete:
    athlete = await db.get(Athlete, athlete_id)
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return athlete


@router.post("/", response_model=AthleteRead)
async def create_athlete(payload: AthleteCreate, db: AsyncSession = Depends(get_db)):
    athlete = Athlete(
        name=payload.name,
        email=payload.email,
        date_of_birth=payload.date_of_birth,
    )
    db.add(athlete)
    await db.commit()
    await db.refresh(athlete)
    return athlete


@router.get("/", response_model=List[AthleteRead])
async def get_all_athletes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Athlete))
    athletes = result.scalars().all()
    return athletes


@router.get("/{athlete_id}", response_model=AthleteRead)
async def get_athlete(athlete_id: int, db: AsyncSession = Depends(get_db)):
    athlete = await require_athlete(athlete_id, db)
    return athlete


@router.get("/{athlete_id}/ascents", response_model=List[AscentRead])
async def get_ascents(athlete_id: int, db: AsyncSession = Depends(get_db)):
    await require_athlete(athlete_id, db)

    result = await db.execute(select(Ascent).where(Ascent.athlete_id == athlete_id))
    ascents = result.scalars().all()
    return ascents


@router.get("/{athlete_id}/routes", response_model=List[RouteRead])
async def get_routes(athlete_id: int, db: AsyncSession = Depends(get_db)):
    await require_athlete(athlete_id, db)

    result = await db.execute(
        select(Route).join(Ascent).where(Ascent.athlete_id == athlete_id)
    )
    routes = result.scalars().all()
    return routes


@router.put("/{athlete_id}", response_model=AthleteRead)
async def update_athlete(
    athlete_id: int, payload: AthleteUpdate, db: AsyncSession = Depends(get_db)
):
    athlete = await require_athlete(athlete_id, db)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(athlete, field, value)

    await db.commit()
    await db.refresh(athlete)

    return athlete


@router.delete("/{athlete_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_athlete(athlete_id: int, db: AsyncSession = Depends(get_db)):
    athlete = await require_athlete(athlete_id, db)

    await db.delete(athlete)
    await db.commit()
