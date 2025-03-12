from fastapi import APIRouter,HTTPException
from controllers.AreaControllar import addArea, getAreas , getAreasByCityId
from models.AreaModel import Area
from bson import ObjectId

router = APIRouter()

@router.post("/area")
async def post_area(area: Area):
    return await addArea(area)

@router.get("/areas")
async def get_all_areas():
    return await getAreas()

@router.get("/area/{city_id}")
async def get_area_by_city_id(city_id: str):    
    return await getAreasByCityId(city_id)

