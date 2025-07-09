from datetime import datetime
from models.OfferModel import Offer, OfferOut
from bson import ObjectId
from config.database import offer_collection, location_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from utils.SendMail import send_mail
from fastapi import APIRouter, HTTPException, UploadFile, File,Form
from utils.CloudinaryUtil import upload_image
import shutil
import os
import cloudinary
import cloudinary.uploader



async def addOffer(offer: Offer):
    offer_dict = offer.dict()

    # Convert startDate and endDate from date to datetime
    offer_dict["startDate"] = datetime.combine(offer.startDate, datetime.min.time())
    offer_dict["endDate"] = datetime.combine(offer.endDate, datetime.min.time())

    offer_dict["locationId"] = ObjectId(offer_dict["locationId"])  # Convert to ObjectId

    saved_offer = await offer_collection.insert_one(offer_dict)
    
    if not saved_offer.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to create offer")
    
    return JSONResponse(content={"message": "Offer created successfully"}, status_code=201)

async def getOffers():
    offers = await offer_collection.find().to_list(length=1000)

    for offer in offers:
        offer["_id"] = str(offer["_id"])
        offer["locationId"] = str(offer["locationId"])

        # Convert datetime to string for JSON response
        offer["startDate"] = offer["startDate"].isoformat()
        offer["endDate"] = offer["endDate"].isoformat()

        # Fetch location details
        location = await location_collection.find_one({"_id": ObjectId(offer["locationId"])})
        if location:
            location["_id"] = str(location["_id"])
            offer["location"] = location  # Attach location details

    return [OfferOut(**offer) for offer in offers]


async def updateOffer(offer_id: str, offer: Offer):
    existing_offer = await offer_collection.find_one({"_id": ObjectId(offer_id)})
    
    if not existing_offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    updated_offer = await offer_collection.update_one(
        {"_id": ObjectId(offer_id)}, {"$set": offer.dict()}
    )

    if updated_offer.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update offer")

    return JSONResponse(content={"message": "Offer updated successfully"}, status_code=200)

async def deleteOffer(offer_id: str):
    deleted_offer = await offer_collection.delete_one({"_id": ObjectId(offer_id)})

    if deleted_offer.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Offer not found")

    return JSONResponse(content={"message": "Offer deleted successfully"}, status_code=200)

async def addOfferWithFile(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    active: bool = Form(...),
    startDate: datetime = Form(...),
    endDate: datetime = Form(...),
    discountPercentage: Optional[int] = Form(None),
    minOrderAmount: Optional[int] = Form(None),
    locationId: str = Form(...),
    foodType: str = Form(...),
    image: UploadFile = File(...),
):
    try:
        # Ensure upload directory exists
        UPLOAD_DIR = "uploads"
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Extract file extension
        file_ext = image.filename.split(".")[-1]
        file_name = f"{ObjectId()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        # Save file locally before uploading to Cloudinary
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Upload image to Cloudinary and get URL
        cloudinary_url = await upload_image(file_path)

        # Create offer data
        offer_data = {
            "title": title,
            "description": description,
            "active": active,
            "startDate": startDate,
            "endDate": endDate,
            "discountPercentage": discountPercentage,
            "minOrderAmount": minOrderAmount,
            "locationId": locationId,
            "foodType": foodType,
            "image": cloudinary_url,  # Store Cloudinary URL
            "createdAt": datetime.utcnow(),
        }

        # Insert into MongoDB
        result = await offer_collection.insert_one(offer_data)

        # Clean up local file after uploading to Cloudinary
        os.remove(file_path)

        return {
            "message": "Offer created successfully",
            "imageURL": cloudinary_url,
            "offerId": str(result.inserted_id),
        }

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

async def get_offers_by_restaurant(location_id: str):
    try:
        # Validate location_id as ObjectId
        if not ObjectId.is_valid(location_id):
            raise HTTPException(status_code=400, detail="Invalid location ID format")

        # Query offers by locationId
        offers = await offer_collection.find({"locationId": ObjectId(location_id)}).to_list(length=100)

        for offer in offers:
            offer["_id"] = str(offer["_id"])
            offer["locationId"] = str(offer["locationId"])
            offer["startDate"] = offer["startDate"].isoformat()
            offer["endDate"] = offer["endDate"].isoformat()

        return {"offers": offers}

    except Exception as e:
        print(f"Error fetching offers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch offers: {str(e)}")