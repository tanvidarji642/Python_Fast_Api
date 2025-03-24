from pydantic import BaseModel, Field, validator, EmailStr, constr
from bson import ObjectId
from typing import Optional, Dict, Any
import bcrypt   # pip install bcrypt
from fastapi import FastAPI


# class User(BaseModel):
#     firstname: Optional[str] = None 
#     lastname: Optional[str] = None 
#     gender: Optional[str] = None  
#     contact: Optional[int] = None  
#     email: EmailStr  # Validates email format
#     password: Optional[str] = None
#     confirm_password: Optional[str] = None 
#     age: int
#     profilePicPath: Optional[str] = None 
#     role: str 
#     role_id: Optional[str] = None
#     status: bool
    
#     @validator("password", pre=True, always=True)
#     def encrypt_password(cls, v):
#         if v is None:
#             return None
#         return bcrypt.hashpw(v.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")


class User(BaseModel):
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

    # @validator("confirm_password", pre=True, always=True)
    # def match_passwords(cls, v, values):
    #     if "password" in values and v != values["password"]:
    #         raise ValueError("Passwords do not match")
    #     return bcrypt.hashpw(v.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")

# class UserOut(User):
#     id: str = Field(alias="_id")  
#     role: Optional[Dict[str, Any]] = None
#     firstname: Optional[str] = None
#     lastname: Optional[str] = None
#     email: Optional[str] = None
#     password: Optional[str] = None
#     confirm_password: Optional[str] = None
#     status: Optional[bool] = None
#     profilePicPath: Optional[str] = None
#     # role_id: Optional[str] = None

    
#     @validator("id", pre=True, always=True)
#     def convert_objectId(cls, v):
#         if isinstance(v, ObjectId):
#             return str(v)
#         return v
    
#     @validator("role", pre=True, always=True)
#     def convert_role(cls, v):
#         if isinstance(v, dict) and "_id" in v:
#             v["_id"] = str(v["_id"])  # Convert role _id to string
#         return v




# class UserOut(BaseModel):
#     id: str = Field(alias="_id")  
#     role: Optional[Dict[str, Any]] = None  # Allow both dict and string
#     firstname: Optional[str] = None
#     lastname: Optional[str] = None
#     email: Optional[str] = None
#     password: Optional[str] = None
#     confirm_password: Optional[str] = None
#     status: Optional[bool] = None
#     profilePicPath: Optional[str] = None

#     @validator("id", pre=True, always=True)
#     def convert_objectId(cls, v):
#         if isinstance(v, ObjectId):
#             return str(v)
#         return v

#     @validator("role", pre=True, always=True)
#     def convert_role(cls, v):
#         if isinstance(v, dict):
#             if "_id" in v and isinstance(v["_id"], ObjectId):
#                 v["_id"] = str(v["_id"])  # Convert role _id to string
#         elif isinstance(v, ObjectId):
#             return str(v)  # Convert ObjectId directly to string
#         return v




# class UserOut(BaseModel):
#     id: str = Field(alias="_id")  
#     role: Optional[Dict[str, Any]] = None  # Expecting a dictionary for role
#     firstname: Optional[str] = None
#     lastname: Optional[str] = None
#     email: Optional[str] = None
#     password: Optional[str] = None
#     confirm_password: Optional[str] = None
#     status: Optional[bool] = None
#     profilePicPath: Optional[str] = None
#     # role_id:Optional[Dict[str, Any]]

#     @validator("id", pre=True, always=True)
#     def convert_objectId(cls, v):
#         if isinstance(v, ObjectId):
#             return str(v)
#         return v

#     @validator("role", pre=True, always=True)
#     def convert_role(cls, v):
#         if isinstance(v, dict):
#             if "_id" in v and isinstance(v["_id"], ObjectId):
#                 v["_id"] = str(v["_id"])  # Convert role _id to string
#             return v  # Return as dictionary if it's valid
#         elif isinstance(v, str):
#             return {"_id": v}  # Convert string role_id into a dictionary
#         elif isinstance(v, ObjectId):
#             return {"_id": str(v)}  # Convert ObjectId directly to dictionary
#         return None  # Ensure role remains None if it's invalid

class UserOut(User):
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



class UserLogin(BaseModel):
    email: EmailStr
    password: str

