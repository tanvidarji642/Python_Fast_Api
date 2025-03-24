from fastapi import APIRouter
from controllers.RestaurantController import (
    addRestaurant,
    getAllRestaurants,
    deleteRestaurant,
    getRestaurantById,
    loginRestaurant,
)
from models.RestaurantModel import Restaurant, RestaurantLogin

router = APIRouter()

@router.post("/restaurant")
async def create_restaurant(restaurant: Restaurant):
    return await addRestaurant(restaurant)

@router.get("/restaurants")
async def get_restaurants():
    return await getAllRestaurants()

@router.get("/restaurant/{restaurant_id}")
async def get_restaurant_by_id(restaurant_id: str):
    return await getRestaurantById(restaurant_id)

@router.delete("/restaurant/{restaurant_id}")
async def delete_restaurant(restaurant_id: str):
    return await deleteRestaurant(restaurant_id)

@router.post("/restaurant/login")
async def login_restaurant(request: RestaurantLogin):
    return await loginRestaurant(request)