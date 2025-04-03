from models.UserModel import User,UserOut,UserLogin
from bson import ObjectId
from config.database import user_collection,role_collection
from fastapi import HTTPException,APIRouter
from fastapi.responses import JSONResponse
import bcrypt  
from pydantic import EmailStr 
# from utils. import send_mail
from utils.SendMail import send_mail
from fastapi import APIRouter, HTTPException, UploadFile, File,Form
from utils.CloudinaryUtil import upload_image
import shutil
import os
import cloudinary
import cloudinary.uploader


async def addUser(user:User):
    #typeCast
    #print("user....",user.role_id)
    #convert string id to object it comp.,, to mongo db
    user.role_id = ObjectId(user.role_id)
    print("after type cast",user.role_id)
    result = await user_collection.insert_one(user.dict())
    send_mail(user.email,"User Created","User created successfully")
    #mail...
    #return {"Message":"user created successfully"}
    
    return JSONResponse(status_code=201,content={"message":"User created successfully"})
    #raise HTTPException(status_code=500,detail="User not created")

# async def getAllUsers():
#     users = await user_collection.find().to_list()
#     print("users",users)
#     return [UserOut(**user) for user in users]

async def getAllUsers():
    print("getAllUsers")
    try:
        users = await user_collection.find().to_list(length=None)

        print("users...................",users)
    # return [UserOut(**role) for role in users]
        print("users",users)

        for user in users:
        # Convert role_id from ObjectId to str before validation
            if "role_id" in user and isinstance(user["role_id"], ObjectId):
                user["role_id"] = str(user["role_id"])
        
        # Fetch role details
        # role = None
        # if user.get("role_id"):
            role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})

        
            if role:
                role["_id"] = str(role["_id"])  # Convert role _id to string
                user["role"] = role

        # return {"ok":"ok"}
        return[UserOut(**user)for user in users]
    #return [UserOut(**user) for user in users]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching users")
 
async def loginUser(request: UserLogin):
    try:
        # Find user by email
        foundUser = await user_collection.find_one({"email": request.email})
        
        if not foundUser:
            raise HTTPException(status_code=404, detail="Email not found")

        # Convert ObjectId fields to string
        foundUser["_id"] = str(foundUser["_id"])
        if "role_id" in foundUser and isinstance(foundUser["role_id"], ObjectId):
            foundUser["role_id"] = str(foundUser["role_id"])

        # Check if the user has a password stored
        if "password" not in foundUser or not foundUser["password"]:
            raise HTTPException(status_code=400, detail="Password not set for this user")

        # Compare hashed password with user input
        if not bcrypt.checkpw(request.password.encode("utf-8"), foundUser["password"].encode("utf-8")):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Fetch role details
        role = None
        if foundUser.get("role_id"):
            role = await role_collection.find_one({"_id": ObjectId(foundUser["role_id"])})
            if role:
                foundUser["role"] = {
                    "_id": str(role["_id"]),
                    "name": role.get("name", "Unknown")
                }
            else:
                foundUser["role"] = {"_id": "", "name": "Unknown"}

        # Remove sensitive data before returning
        foundUser.pop("password", None)

        return {
            "message": "Login successful",
            "user": foundUser
        }

    except Exception as e:
        print(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



async def deleteUser(userId:str):
    result = await user_collection.delete_one({"_id":ObjectId(userId)})
    print("after delet result",result)
    return {"message":"user deleted successfully!!"}

async def getUserById(userId: str):
    try:
        print(f"Received userId: {userId}")  # Debugging

        # Validate ObjectId
        if not ObjectId.is_valid(userId):
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        # Convert to ObjectId and fetch user
        object_id = ObjectId(userId)
        print(f"Converted userId to ObjectId: {object_id}")  # Debugging
        
        user = await user_collection.find_one({"_id": object_id})
        print(f"Fetched user from DB: {user}")  # Debugging

        # Check if user exists
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Convert ObjectId fields to strings
        user["_id"] = str(user["_id"])
        if "role_id" in user and isinstance(user["role_id"], ObjectId):
            user["role_id"] = str(user["role_id"])

        return {"message": "User fetched successfully", "user": UserOut(**user)}

    except Exception as e:
        print(f"Error in getUserById: {str(e)}")  # Print full error
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



async def addSignupWithFile(
    firstname: str = Form(...),
    lastname: str = Form(...),
    gender: str = Form(...),
    contact: int = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    age: int = Form(...),
    role: str = Form(...),
    role_id: str = Form(...),
    status: bool = Form(...),
    profilePicPath: UploadFile = File(...)
):
    try:
        # Ensure upload directory exists
        UPLOAD_DIR = "uploads"
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        # Validate role_id
        if not ObjectId.is_valid(role_id):
            raise HTTPException(status_code=400, detail="Invalid role ID")
        
        # Extract file extension
        if not profilePicPath.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")
        file_ext = profilePicPath.filename.split(".")[-1]
        file_name = f"{ObjectId()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        
        # Save file locally before uploading to Cloudinary
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profilePicPath.file, buffer)
        
        # Upload image to Cloudinary and get URL
        cloudinary_url = await upload_image(file_path)
        
        # Hash the password for security
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
        
        # Create user data
        user_data = {
            "firstname": firstname,
            "lastname": lastname,
            "gender": gender,
            "contact": contact,
            "email": email,
            "password": hashed_password, 
            "confirm_password": confirm_password,
            "age": age,
            "role": role,
            "role_id": ObjectId(role_id),  # Convert to ObjectId
            "status": status,
            "profilePicPath": cloudinary_url  # Store Cloudinary URL
        }
        
        # Insert into MongoDB
        result = await user_collection.insert_one(user_data)
        
        # Clean up local file after uploading to Cloudinary
        os.remove(file_path)
        
        return {"message": "User created successfully", "profilePicURL": cloudinary_url, "userId": str(result.inserted_id)}
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")