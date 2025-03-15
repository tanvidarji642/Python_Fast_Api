from fastapi import APIRouter
from controllers.RatingControllar import (
    addRating, getRatings, getRatingById, updateRating, deleteRating
)
from models.RatingModel import Rating

router = APIRouter()

@router.post("/rating")
async def post_rating(rating: Rating):
    return await addRating(rating)

@router.get("/ratings")
async def get_all_ratings():
    return await getRatings()

@router.get("/rating/{id}")
async def get_single_rating(id: str):
    return await getRatingById(id)

@router.put("/rating/{id}")
async def put_rating(id: str, rating: Rating):
    return await updateRating(id, rating)
1
@router.delete("/rating/{id}")
async def delete_rating(id: str):
    return await deleteRating(id)
