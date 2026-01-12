from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.models.athlete import Athlete
from backend.app.db.session import get_db
from backend.app.schemas.athlete import AthleteCreate, AthleteRead

router = APIRouter()


@router.post("/", response_model=AthleteRead)
async def create_athlete(athlete: AthleteCreate, db: AsyncSession = Depends(get_db)):
    db_athlete = Athlete(
        name=athlete.name,
        email=athlete.email,
        date_of_birth=athlete.date_of_birth,
    )
    db.add(db_athlete)
    await db.commit()
    await db.refresh(db_athlete)
    return db_athlete
