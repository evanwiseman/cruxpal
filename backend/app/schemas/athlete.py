from datetime import date
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

    model_config = ConfigDict(from_attributes=True)
