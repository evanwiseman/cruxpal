from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.endpoints import endpoints
from backend.app.db.models.ascent import Ascent
from backend.app.db.models.athlete import Athlete
from backend.app.db.models.route import Route
from backend.app.db.session import get_db
from backend.app.schemas.athlete import AthleteRead
from backend.app.schemas.route import RouteCreate, RouteRead, RouteUpdate

router = APIRouter()
routes = endpoints.RoutesRoutes()


async def require_route(route_id: int, db: AsyncSession):
    route = await db.get(Route, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


@router.post(routes.CREATE, response_model=RouteRead)
async def create_route(payload: RouteCreate, db: AsyncSession = Depends(get_db)):
    route = Route(
        name=payload.name,
        difficulty=payload.difficulty,
    )
    db.add(route)
    await db.commit()
    await db.refresh(route)
    return route


@router.get(routes.LIST, response_model=List[RouteRead])
async def get_all_routes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Route))
    routes = result.scalars().all()
    return routes


@router.get(routes.GET_BY_ID, response_model=RouteRead)
async def get_route(route_id: int, db: AsyncSession = Depends(get_db)):
    route = await require_route(route_id, db)
    return route


@router.get(routes.LIST_ATHLETES, response_model=List[AthleteRead])
async def get_athletes(route_id: int, db: AsyncSession = Depends(get_db)):
    require_route(route_id, db)

    result = await db.execute(
        select(Athlete).join(Ascent).where(Ascent.route_id == route_id)
    )
    athletes = result.scalars().all()
    return athletes


@router.put(routes.UPDATE, response_model=RouteRead)
async def update_route(
    route_id: int, payload: RouteUpdate, db: AsyncSession = Depends(get_db)
):
    route = await require_route(route_id, db)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(route, field, value)

    db.add(route)
    await db.commit()
    await db.refresh(route)
    return route


@router.delete(routes.DELETE, status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(route_id: int, db: AsyncSession = Depends(get_db)):
    route = await require_route(route_id, db)

    await db.delete(route)
    await db.commit()
