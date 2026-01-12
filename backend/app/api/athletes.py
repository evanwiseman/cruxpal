from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.models.athlete import Athlete
from backend.app.db.session import get_db
from backend.app.schemas.athlete import AthleteCreate, AthleteRead, AthleteUpdate

router = APIRouter()


# /.../athletes POST
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


# /.../athletes GET
@router.get("/", response_model=List[AthleteRead])
async def get_all_athletes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Athlete))
    athletes = result.scalars().all()
    return athletes


# /.../athletes/{id} GET
@router.get("/{athlete_id}", response_model=AthleteRead)
async def get_athlete(athlete_id: int, db: AsyncSession = Depends(get_db)):
    athlete = await db.get(Athlete, athlete_id)
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return athlete


# /.../athletes/{id} PUT
@router.put("/{athlete_id}", response_model=AthleteRead)
async def update_athlete(
    athlete_id: int, payload: AthleteUpdate, db: AsyncSession = Depends(get_db)
):
    athlete = await db.get(Athlete, athlete_id)
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    # update fields
    athlete.email = payload.email

    # persist changes
    db.add(athlete)
    await db.commit()
    await db.refresh(athlete)

    return athlete


# /.../athletes DELETE
@router.delete("/{athlete_id}", response_model=dict)
async def delete_athlete(athlete_id: int, db: AsyncSession = Depends(get_db)):
    athlete = await db.get(Athlete, athlete_id)
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    await db.delete(athlete)
    await db.commit()
    return {"message": "Deleted successfully"}
