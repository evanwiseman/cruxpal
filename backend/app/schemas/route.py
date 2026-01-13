from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# Used when creating a route
class RouteCreate(BaseModel):
    name: str = Field(..., example="El Capitan")
    difficulty: str = Field(..., example="5.13b")


# Used when reading a route
class RouteRead(BaseModel):
    name: str
    difficulty: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Used when updating a route
class RouteUpdate(BaseModel):
    name: str = Field(..., example="name")
    difficulty: str = Field(..., example="v0")
