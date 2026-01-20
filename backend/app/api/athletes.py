from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.endpoints import endpoints
from backend.app.db.models.ascent import Ascent
from backend.app.db.models.athlete import Athlete
from backend.app.db.models.route import Route
from backend.app.db.session import get_db
from backend.app.schemas.ascent import AscentRead
from backend.app.schemas.athlete import AthleteCreate, AthleteRead, AthleteUpdate
from backend.app.schemas.route import RouteRead

router = APIRouter()
routes = endpoints.AthletesRoutes()


async def require_athlete(athlete_id: int, db: AsyncSession) -> Athlete:
    athlete = await db.get(Athlete, athlete_id)
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return athlete


@router.post(routes.CREATE, response_model=AthleteRead)
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


@router.get(routes.LIST, response_model=List[AthleteRead])
async def get_all_athletes(
    name: Optional[str] = None,
    email: Optional[str] = None,
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    statement = select(Athlete)
    if name:
        statement = statement.where(Athlete.name.ilike(f"%{name}%"))

    if email:
        statement = statement.where(Athlete.email == email)

    statement = statement.limit(limit).offset(offset)

    result = await db.execute(statement)
    return result.scalars().all()


@router.get(routes.GET_BY_ID, response_model=AthleteRead)
async def get_athlete(athlete_id: int, db: AsyncSession = Depends(get_db)):
    athlete = await require_athlete(athlete_id, db)
    return athlete


@router.get(routes.LIST_ASCENTS, response_model=List[AscentRead])
async def get_ascents(
    athlete_id: int,
    sent: Optional[bool] = None,
    route_id: Optional[bool] = None,
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    await require_athlete(athlete_id, db)

    statement = select(Ascent).where(Ascent.athlete_id == athlete_id)
    if sent is not None:
        statement = statement.where(Ascent.sent == sent)

    if route_id is not None:
        statement = statement.where(Ascent.route_id == route_id)

    statement = statement.limit(limit).offset(offset)
    result = await db.execute(statement)
    return result.scalars().all()


@router.get(routes.LIST_ROUTES, response_model=List[RouteRead])
async def get_routes(
    athlete_id: int,
    sent: Optional[bool] = None,
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    await require_athlete(athlete_id, db)

    statement = select(Route).join(Ascent).where(Ascent.athlete_id == athlete_id)
    if sent is not None:
        statement = statement.where(Ascent.sent == sent)

    statement = statement.distinct().limit(limit).offset(offset)

    result = await db.execute(statement)
    return result.scalars().all()


@router.put(routes.UPDATE, response_model=AthleteRead)
async def update_athlete(
    athlete_id: int, payload: AthleteUpdate, db: AsyncSession = Depends(get_db)
):
    athlete = await require_athlete(athlete_id, db)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(athlete, field, value)

    await db.commit()
    await db.refresh(athlete)

    return athlete


@router.delete(routes.DELETE, status_code=status.HTTP_204_NO_CONTENT)
async def delete_athlete(athlete_id: int, db: AsyncSession = Depends(get_db)):
    athlete = await require_athlete(athlete_id, db)

    await db.delete(athlete)
    await db.commit()
