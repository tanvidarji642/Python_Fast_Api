from models.RestaurantModel import Restaurant, RestaurantOut, RestaurantLogin
from config.database import user_collection
from bson import ObjectId
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import bcrypt

async def addRestaurant(restaurant: Restaurant):
    restaurant_dict = restaurant.dict()
    result = await user_collection.insert_one(restaurant_dict)
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to create restaurant")
    return JSONResponse(content={"message": "Restaurant created successfully"}, status_code=201)

async def getAllRestaurants():
    restaurants = await user_collection.find({"role": "restaurant"}).to_list(length=1000)
    for restaurant in restaurants:
        restaurant["_id"] = str(restaurant["_id"])
    return [RestaurantOut(**restaurant) for restaurant in restaurants]

async def getRestaurantById(restaurant_id: str):
    restaurant = await user_collection.find_one({"_id": ObjectId(restaurant_id)})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return RestaurantOut(**restaurant)

async def deleteRestaurant(restaurant_id: str):
    result = await user_collection.delete_one({"_id": ObjectId(restaurant_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return JSONResponse(content={"message": "Restaurant deleted successfully"}, status_code=200)

async def loginRestaurant(request: RestaurantLogin):
    restaurant = await user_collection.find_one({"email": request.email})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if not bcrypt.checkpw(request.password.encode("utf-8"), restaurant["password"].encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid password")
    restaurant["_id"] = str(restaurant["_id"])
    return {"message": "Login successful", "restaurant": RestaurantOut(**restaurant)}