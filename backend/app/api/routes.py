from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.models.route import Route
from backend.app.db.session import get_db
from backend.app.schemas.route import RouteCreate, RouteRead, RouteUpdate

router = APIRouter()


def raise_not_found():
    raise HTTPException(status_code=404, detail="Route not found")


# /.../routes POST
@router.post("/", response_model=RouteRead)
async def create_route(payload: RouteCreate, db: AsyncSession = Depends(get_db)):
    route = Route(
        name=payload.name,
        difficulty=payload.difficulty,
    )
    db.add(route)
    await db.commit()
    await db.refresh(route)
    return route


# /.../routes GET
@router.get("/", response_model=List[RouteRead])
async def get_all_routes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Route))
    routes = result.scalars().all()
    return routes


# /.../routes/{id} GET
@router.get("/{route_id}", response_model=RouteRead)
async def get_route(route_id: int, db: AsyncSession = Depends(get_db)):
    route = await db.get(Route, route_id)
    if not route:
        raise_not_found()
    return route


# /.../routes/{id} PUT
@router.put("/{route_id}", response_model=RouteRead)
async def update_route(
    route_id: int, payload: RouteUpdate, db: AsyncSession = Depends(get_db)
):
    route = await db.get(Route, route_id)
    if not route:
        raise_not_found()

    # update route
    route.name = payload.name
    route.difficulty = payload.difficulty

    db.add(route)
    await db.commit()
    await db.refresh(route)
    return route


# /.../routes/{id} DELETE
@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(route_id: int, db: AsyncSession = Depends(get_db)):
    route = await db.get(Route, route_id)
    if not route:
        raise_not_found()

    await db.delete(route)
    await db.commit()
    return
