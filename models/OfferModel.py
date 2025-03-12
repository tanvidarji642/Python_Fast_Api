from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
# from datetime import date

class Offer(BaseModel):
    title: str
    description: Optional[str] = None
    active: bool
    startDate: str
    endDate: str
    locationId: str  # Foreign key reference to Location
    foodType: str  # Example: "burger, pizza, pasta"

class OfferOut(Offer):
    # id: str

    @staticmethod
    def convert_objectId(value):
        return str(value) if isinstance(value, ObjectId) else value

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data["_id"] = self.convert_objectId(data.get("_id"))
        return data
