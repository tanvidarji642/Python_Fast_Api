from models.RestaurantModel import Restaurant, RestaurantOut, RestaurantLogin, ResetPasswordReq, RestaurantOffer
from config.database import restaurant_collection, offer_collection
from bson import ObjectId
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import bcrypt
from utils.SendMail import send_mail
import jwt 
import datetime
from urllib.parse import unquote
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from typing import List

SECRET_KEY = "royal"

async def addRestaurant(restaurant: Restaurant):
    try:
        # Check if email already exists
        existing_restaurant = await restaurant_collection.find_one({"email": restaurant.email})
        if existing_restaurant:
            raise HTTPException(status_code=400, detail="Email already registered")

        restaurant_dict = restaurant.dict()
        restaurant_dict["role_id"] = {
            "_id": ObjectId(),
            "name": "RESTAURANT"
        }
        restaurant_dict["created_at"] = datetime.datetime.utcnow()

        result = await restaurant_collection.insert_one(restaurant_dict)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create restaurant")

        # Send welcome email
        send_mail(restaurant.email, "Welcome to Our Platform", 
                 f"Dear {restaurant.name},\n\nThank you for joining our platform. You can now login and start adding your offers.")

        return JSONResponse(
            content={"message": "Restaurant created successfully", "restaurant_id": str(result.inserted_id)},
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def getAllRestaurants():
    restaurants = await restaurant_collection.find({"role": "restaurant"}).to_list(length=1000)
    for restaurant in restaurants:
        restaurant["_id"] = str(restaurant["_id"])
    return [RestaurantOut(**restaurant) for restaurant in restaurants]

async def getRestaurantById(restaurant_id: str):
    restaurant = await restaurant_collection.find_one({"_id": ObjectId(restaurant_id)})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return RestaurantOut(**restaurant)

async def deleteRestaurant(restaurant_id: str):
    result = await restaurant_collection.delete_one({"_id": ObjectId(restaurant_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return JSONResponse(content={"message": "Restaurant deleted successfully"}, status_code=200)

async def loginRestaurant(request: RestaurantLogin):
    try:
        restaurant = await restaurant_collection.find_one({"email": request.email})
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        if not bcrypt.checkpw(request.password.encode("utf-8"), restaurant["password"].encode("utf-8")):
            raise HTTPException(status_code=401, detail="Invalid password")

        # Generate JWT token
        token = generate_token(request.email)
        
        return {
            "message": "Login successful",
            "token": token,
            "restaurant": {
                "id": str(restaurant["_id"]),
                "name": restaurant["name"],
                "email": restaurant["email"],
                "is_verified": restaurant.get("is_verified", False)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def addRestaurantOffer(offer: RestaurantOffer):
    try:
        # Validate restaurant exists
        if not ObjectId.is_valid(offer.restaurant_id):
            raise HTTPException(status_code=400, detail="Invalid restaurant ID")

        restaurant = await restaurant_collection.find_one({"_id": ObjectId(offer.restaurant_id)})
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        offer_dict = offer.dict()
        offer_dict["restaurant_id"] = ObjectId(offer.restaurant_id)
        offer_dict["created_at"] = datetime.datetime.utcnow()

        result = await offer_collection.insert_one(offer_dict)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create offer")

        return JSONResponse(
            content={"message": "Offer created successfully", "offer_id": str(result.inserted_id)},
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def getRestaurantOffers(restaurant_id: str):
    try:
        if not ObjectId.is_valid(restaurant_id):
            raise HTTPException(status_code=400, detail="Invalid restaurant ID")

        offers = await offer_collection.find({"restaurant_id": ObjectId(restaurant_id)}).to_list(length=100)
        for offer in offers:
            offer["_id"] = str(offer["_id"])
            offer["restaurant_id"] = str(offer["restaurant_id"])

        return {"offers": offers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_token(email: str):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    payload = {"sub": email, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

async def forgotPassword(email: str):
    try:
        restaurant = await restaurant_collection.find_one({"email": email})
        if not restaurant:
            raise HTTPException(status_code=404, detail="Email not found")

        token = generate_token(email)
        resetLink = f"http://localhost:5173/restaurant/resetpassword/{token}"
        body = f"""
        <html>
            <h1>Password Reset Request</h1>
            <p>Hello {restaurant['name']},</p>
            <p>You have requested to reset your password. Click the link below to proceed:</p>
            <a href="{resetLink}">Reset Password</a>
            <p>This link will expire in 24 hours.</p>
        </html>
        """
        subject = "Password Reset Request"
        send_mail(email, subject, body)
        return {"message": "Reset link sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def resetPassword(data: ResetPasswordReq):
    try:
        token = unquote(data.token)
        if token.count(".") != 2:
            raise HTTPException(status_code=400, detail="Invalid token format")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Reset token has expired")
        except InvalidTokenError:
            raise HTTPException(status_code=400, detail="Invalid token")

        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token payload")

        hashed_password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        result = await restaurant_collection.update_one(
            {"email": email},
            {"$set": {"password": hashed_password}}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        return {"message": "Password updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))