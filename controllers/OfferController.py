from models.OfferModel import Offer, OfferOut
from bson import ObjectId
from config.database import offer_collection, location_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse

async def addOffer(offer: Offer):
    offer_dict = offer.dict()
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
