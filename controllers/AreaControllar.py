from models.AreaModel import Area, AreaOut
from bson import ObjectId
from config.database import area_collection, city_collection,state_collection
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse


async def addArea(area: Area):
    savedarea = await area_collection.insert_one(area.dict())  
    return JSONResponse(content={"message": "Area created successfully"}, status_code=201)  # Return success message

async def getAreas():
    print("areas")
    areas = await area_collection.find().to_list()  # Retrieve all areas
    print(areas)
    for area in areas:
        if "cityId" in area and isinstance(area["cityId"], ObjectId):
            area["cityId"] = str(area["cityId"]) 

        city = await city_collection.find_one({"_id": ObjectId(area["cityId"])})  # Fetch city details
        if city:
            city["_id"] = str(city["_id"])
            area["city"] = city  # Attach city details

    return [AreaOut(**area) for area in areas]  # Return areas   


async def getAreasByCityId(cityId: str):
    areas = await area_collection.find({"cityId": ObjectId(cityId)}).to_list()  # Retrieve areas by city_id
    for area in areas:
        if "cityId" in area and isinstance(area["cityId"], ObjectId):
            area["cityId"] = str(area["cityId"])  # Convert cityId to string

        city = await city_collection.find_one({"_id": ObjectId(area["cityId"])})  # Fetch city details
        if city:
            city["_id"] = str(city["_id"])
            area["city"] = city

    return [AreaOut(**area) for area in areas]  # Return areas
