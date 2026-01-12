from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# Used when creating a new athlete
class AthleteCreate(BaseModel):
    name: str = Field(..., example="Alex Honnold")
    email: str = Field(..., example="alex@example.com")
    date_of_birth: Optional[date] = None


# Used when returning athlete info
class AthleteRead(BaseModel):
    id: int
    name: str
    email: str
    date_of_birth: Optional[date] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Used when updating athlete info
class AthleteUpdate(BaseModel):
    email: str = Field(..., example="email@example.com")
