from models.LocationModel import Location, LocationOut
from bson import ObjectId
from config.database import location_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse

async def addLocation(location: Location):
    location_dict = location.dict()
    location_dict["cityId"] = ObjectId(location_dict["cityId"])
    location_dict["areaId"] = ObjectId(location_dict["areaId"])

    saved_location = await location_collection.insert_one(location_dict)
    if not saved_location.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to create location")
    
    return JSONResponse(content={"message": "Location created successfully"}, status_code=201)

async def getLocations():
    locations = await location_collection.find().to_list(length=1000)

    for loc in locations:
        loc["_id"] = str(loc["_id"])
        loc["cityId"] = str(loc["cityId"])
        loc["areaId"] = str(loc["areaId"])

    return [LocationOut(**loc) for loc in locations]

async def getLocationById(id: str):
    location = await location_collection.find_one({"_id": ObjectId(id)})
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    location["_id"] = str(location["_id"])
    location["cityId"] = str(location["cityId"])
    location["areaId"] = str(location["areaId"])

    return LocationOut(**location)

async def updateLocation(id: str, location: Location):
    update_result = await location_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": location.dict()}
    )

    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Location not found")

    return JSONResponse(content={"message": "Location updated successfully"}, status_code=200)

async def deleteLocation(id: str):
    delete_result = await location_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Location not found")

    return JSONResponse(content={"message": "Location deleted successfully"}, status_code=200)
