from pydantic import BaseModel, Field, validator, EmailStr, constr
from bson import ObjectId
from typing import Optional, Dict, Any
import bcrypt  
from fastapi import FastAPI

class Restaurant(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirmPassword: str
    # role_id:str


    
    #10,11,12,13,14,15,16,20,,,25,31
    @validator("password",pre=True,always=True)
    def encrypt_password(cls,v):
        if v is None:
            return None
        return bcrypt.hashpw(v.encode("utf-8"),bcrypt.gensalt())

class RestaurantOut(Restaurant):
    id:str = Field(alias="_id")    
    role:Optional[Dict[str,Any]] = None
    email:Optional[str] = None
    password:Optional[str] = None
    
    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    
    @validator("role", pre=True, always=True)
    def convert_role(cls, v):
        if isinstance(v, dict) and "_id" in v:
            v["_id"] = str(v["_id"])  # Convert role _id to string
        return v



class RestaurantLogin(BaseModel):
    email: EmailStr
    password: str

class ResetPasswordReq(BaseModel):
    token:str
    password:str 

class RestaurantOffer(BaseModel):
    restaurant_id: str
    title: str
    description: Optional[str] = None
    active: bool
    startDate: str
    endDate: str
    discountPercentage: Optional[int]
    minOrderAmount: Optional[int]
    locationId: str
    foodType: str
    image: str

