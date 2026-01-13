from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.models.ascent import Ascent
from backend.app.db.session import get_db
from backend.app.schemas.ascent import AscentCreate, AscentRead

router = APIRouter()


@router.post("/", response_model=AscentRead)
async def create_ascent(payload: AscentCreate, db: AsyncSession = Depends(get_db)):
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
