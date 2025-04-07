from fastapi import APIRouter, Query, Form, File, UploadFile, HTTPException
from controllers.OfferController import addOffer, getOffers, updateOffer, deleteOffer,addOfferWithFile
from models.OfferModel import Offer, OfferOut
from config.database import offer_collection
from bson import ObjectId
from typing import Optional
from datetime import datetime
from pydantic import EmailStr

router = APIRouter()

@router.post("/offer")
async def post_offer(offer: Offer):
    return await addOffer(offer)

@router.get("/offers")
async def get_all_offers(category: str = Query(None)):
    query = {}

    # If category is provided, filter by it
    if category:
        query["foodType"] = {"$regex": category, "$options": "i"}  # Case-insensitive match

    offers = await offer_collection.find(query).to_list(length=1000)

    for offer in offers:
        offer["_id"] = str(offer["_id"])
        offer["locationId"] = str(offer["locationId"])
        offer["startDate"] = offer["startDate"].isoformat()
        offer["endDate"] = offer["endDate"].isoformat()

    return [OfferOut(**offer) for offer in offers]

@router.put("/offer/{offer_id}")
async def put_offer(offer_id: str, offer: Offer):
    return await updateOffer(offer_id, offer)

@router.delete("/offer/{offer_id}")
async def delete_offer(offer_id: str):
    return await deleteOffer(offer_id)

@router.post("/offer/addwithfile")
async def add_offer_with_file(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    active: bool = Form(...),
    startDate: datetime = Form(...),
    endDate: datetime = Form(...),
    discountPercentage: Optional[int] = Form(None),
    minOrderAmount: Optional[int] = Form(None),
    locationId: str = Form(...),
    foodType: str = Form(...),
    image: UploadFile = File(...)  # Image file upload
):
    try:
        return await addOfferWithFile(
            title, description, active, startDate, endDate,
            discountPercentage, minOrderAmount, locationId, foodType, image
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")