from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId

class Location(BaseModel):
    title: str
    category: str
    description: str
    timings: str
    active: bool
    contactNumber: str
    address: str
    cityId: str  # Foreign key reference to City
    areaId: str  # Foreign key reference to Area
    foodType: str
    latitude: float

class LocationOut(Location):
    id: str = Field(alias="_id")

    @validator("id", pre=True, always=True)
    def convert_objectId(cls, v):
        return str(v) if isinstance(v, ObjectId) else v
