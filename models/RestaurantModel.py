from pydantic import BaseModel, Field, validator, EmailStr, constr
from bson import ObjectId
from typing import Optional, Dict, Any
import bcrypt   # pip install bcrypt
from fastapi import FastAPI

class Restaurant(BaseModel):
    firstName:str
    lastName:str
    gender: str
    contact:int
    email:EmailStr
    password:str
    confirm_password:str
    age:int
    profilePicPath:str
    status:bool
    # role:str
    role_id:str
    status: bool

    
    #10,11,12,13,14,15,16,20,,,25,31
    @validator("password",pre=True,always=True)
    def encrypt_password(cls,v):
        if v is None:
            return None
        return bcrypt.hashpw(v.encode("utf-8"),bcrypt.gensalt())

class RestaurantOut(Restaurant):
    id:str = Field(alias="_id")    
    #role:str = Field(alias="role_id")
    #[{firstna,,,,role:{"onjectid",des,name}},{},{}]
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

