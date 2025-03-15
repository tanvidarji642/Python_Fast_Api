from fastapi import APIRouter
from controllers.LocationController import (
    addLocation, getLocations, getLocationById, updateLocation, deleteLocation
)
from models.LocationModel import Location

router = APIRouter()

@router.post("/location")
async def post_location(location: Location):
    return await addLocation(location)

@router.get("/locations")
async def get_all_locations():
    return await getLocations()

@router.get("/location/{id}")
async def get_single_location(id: str):
    return await getLocationById(id)

@router.put("/location/{id}")
async def put_location(id: str, location: Location):
    return await updateLocation(id, location)

@router.delete("/location/{id}")
async def delete_location(id: str):
    return await deleteLocation(id)

    
