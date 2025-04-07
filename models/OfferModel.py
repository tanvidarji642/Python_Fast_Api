from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from datetime import datetime
# from datetime import date

class Offer(BaseModel):
    
    title: str
    description: Optional[str] = None
    active: bool
    startDate: datetime 
    endDate: datetime 
    discountPercentage: Optional[int] 
    minOrderAmount: Optional[int]
    locationId: str 
    foodType: str 
    image: str 

    

class OfferOut(Offer):
    # id: str

    @staticmethod
    def convert_objectId(value):
        return str(value) if isinstance(value, ObjectId) else value

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data["_id"] = self.convert_objectId(data.get("_id"))
        return data