from pydantic import BaseModel,Field,validator
from typing import List, Optional,Dict,Any
from bson import ObjectId

class Area(BaseModel):
    areaName: str
    cityId: str  # Foreign key reference to City

class AreaOut(Area):
    id: str = Field(alias="_id")
    city: Optional[Dict[str, Any]] = None
    state:Optional[Dict[str, Any]] = None

    @validator("id", pre=True, always=True)
    def convert_objectId(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator("city", pre=True, always=True)
    def convert_city(cls, v):
        if isinstance(v, dict) and "_id" in v:
            v["_id"] = str(v["_id"])  # Convert role _id to string
        return v

   