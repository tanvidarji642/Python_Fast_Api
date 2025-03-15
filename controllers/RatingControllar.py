from models.RatingModel import Rating, RatingOut
from bson import ObjectId
from config.database import rating_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse

async def addRating(rating: Rating):
    try:
        rating_dict = rating.model_dump()
        
        # Validate offerId as a valid ObjectId
        if not ObjectId.is_valid(rating_dict["offerId"]):
            raise HTTPException(status_code=400, detail="Invalid offerId format")
        
        rating_dict["offerId"] = ObjectId(rating_dict["offerId"])

        saved_rating = await rating_collection.insert_one(rating_dict)
        if not saved_rating.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create rating")
        
        return JSONResponse(content={"message": "Rating created successfully"}, status_code=201)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def getRatings():
    ratings = await rating_collection.find().to_list(length=1000)

    for rate in ratings:
        rate["_id"] = str(rate["_id"])
        rate["offerId"] = str(rate["offerId"])

    return [RatingOut(**rate) for rate in ratings]

async def getRatingById(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid rating ID format")
    
    rating = await rating_collection.find_one({"_id": ObjectId(id)})
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    rating["_id"] = str(rating["_id"])
    rating["offerId"] = str(rating["offerId"])

    return RatingOut(**rating)

async def updateRating(id: str, rating: Rating):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid rating ID format")

    update_data = rating.model_dump(exclude_unset=True)  # Prevent empty fields

    update_result = await rating_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": update_data}
    )

    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Rating not found")

    return JSONResponse(content={"message": "Rating updated successfully"}, status_code=200)

async def deleteRating(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid rating ID format")

    delete_result = await rating_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Rating not found")

    return JSONResponse(content={"message": "Rating deleted successfully"}, status_code=200)
