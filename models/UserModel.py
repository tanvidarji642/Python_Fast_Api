from pydantic import BaseModel, Field, validator, EmailStr, constr
from bson import ObjectId
from typing import Optional, Dict, Any
import bcrypt   # pip install bcrypt
from fastapi import FastAPI


class User(BaseModel):
    firstname: Optional[str] = None 
    lastname: Optional[str] = None 
    gender: Optional[str] = None  
    contact: Optional[str] = None  
    email: EmailStr  # Validates email format
    password: Optional[str] = None
    confirm_password: Optional[str] = None 
    age: int
    profilePicPath: Optional[str] = None 
    role: str 
    role_id: Optional[str] = None
    status: bool
    
    @validator("password", pre=True, always=True)
    def encrypt_password(cls, v):
        if v is None:
            return None
        return bcrypt.hashpw(v.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")

    # @validator("confirm_password", pre=True, always=True)
    # def match_passwords(cls, v, values):
    #     if "password" in values and v != values["password"]:
    #         raise ValueError("Passwords do not match")
    #     return bcrypt.hashpw(v.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")

class UserOut(User):
    id: str = Field(alias="_id")  
    role: Optional[Dict[str, Any]] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    status: Optional[bool] = None
    profilePicPath: Optional[str] = None
    # role_id: Optional[str] = None

    
    @validator("id", pre=True, always=True)
    def convert_objectId(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
    @validator("role", pre=True, always=True)
    def convert_role(cls, v):
        if isinstance(v, dict) and "_id" in v:
            v["_id"] = str(v["_id"])  # Convert role _id to string
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    