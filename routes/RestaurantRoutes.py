from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr   
from controllers.RestaurantController import (
    addRestaurant,
    getAllRestaurants,
    deleteRestaurant,
    getRestaurantById,
    loginRestaurant,
    forgotPassword,
    resetPassword,
    addRestaurantOffer,
    getRestaurantOffers
)
from models.RestaurantModel import Restaurant, ResetPasswordReq, RestaurantLogin, RestaurantOffer
from fastapi.security import OAuth2PasswordBearer
import jwt
from typing import Optional

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="restaurant/login")

async def get_current_restaurant(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "royal", algorithms=["HS256"])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

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

@router.post("/restaurant/forgotpassword")
async def forgot_password(email: str):
    return await forgotPassword(email)

@router.post("/restaurant/resetpassword")
async def reset_password(data: ResetPasswordReq):
    return await resetPassword(data)

@router.post("/restaurant/offer", dependencies=[Depends(get_current_restaurant)])
async def create_offer(offer: RestaurantOffer):
    return await addRestaurantOffer(offer)

@router.get("/restaurant/{restaurant_id}/offers")
async def get_offers(restaurant_id: str):
    return await getRestaurantOffers(restaurant_id)