from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AscentCreate(BaseModel):
    athlete_id: int
    route_id: int

    sent: bool
    attempt: int
    notes: Optional[str] = None


class AscentRead(BaseModel):
    id: int
    athlete_id: int
    route_id: int

    sent: bool
    attempt: int
    notes: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
