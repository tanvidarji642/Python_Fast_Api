from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId

class Rating(BaseModel):
    offerId: str  # Foreign key reference to Offer
    comments: Optional[str] = None
    rating: int  # Rating value between 1 to 5

    @validator("rating")
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError("Rating must be between 1 and 5")
        return v

class RatingOut(Rating):
    id: str = Field(alias="_id")

    @validator("id", pre=True, always=True)
    def convert_objectId(cls, v):
        return str(v) if isinstance(v, ObjectId) else v