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
    
    # async def getAllUsers():
    #find --> select * from roles
    # users = await user_collection.find().to_list()

async def loginUser(request: UserLogin):
    # Find the user by email
    foundUser = await user_collection.find_one({"email": request.email})
    if not foundUser:
        raise HTTPException(status_code=404, detail="User not found!")

    # Convert _id and role_id to strings
    foundUser["_id"] = str(foundUser["_id"])
    foundUser["role_id"] = str(foundUser["role_id"])

    # Compare password
    if "password" in foundUser and bcrypt.checkpw(request.password.encode("utf-8"), foundUser["password"].encode("utf-8")):
        # Find the role using role_id
        role = await role_collection.find_one({"_id": ObjectId(foundUser["role_id"])})

        # If the role is found, assign it to the user
        if role:
            foundUser["role"] = {"_id": str(role["_id"]), "name": role.get("name", "Unknown")}
        else:
            foundUser["role"] = {"_id": "", "name": "Unknown"}  # Fallback role

        # Ensure all required fields are present in foundUser for UserOut
        # Example: firstname, lastname, etc. If missing, set defaults
        foundUser.setdefault("firstname", "")
        foundUser.setdefault("lastname", "")
        foundUser.setdefault("email", "")
        foundUser.setdefault("password", "")
        foundUser.setdefault("confirm_password", "")
        foundUser.setdefault("status", True)

        return {"message": "User login successful", "user": UserOut(**foundUser)}

    else:

        raise HTTPException(status_code=404, detail="Invalid password")
    

async def deleteUser(userId:str):
    result = await user_collection.delete_one({"_id":ObjectId(userId)})
    print("after delet result",result)
    return {"message":"user deleted successfully!!"}

async def getUserById(userId:str):
    result = await user_collection.find_one({"_id":ObjectId(userId)})
    print(result)    
    #return {"message":"role fetched successfully!"}
    #return result
    # UserOut(**result)  
    return {"message": "User login successful", "user": UserOut(**result)}

# async def addSignupWithFile(
#     firstname: str = Form(...),
#     lastname: str = Form(...),
#     gender: str = Form(...),
#     contact: int = Form(...),
#     email: EmailStr = Form(...),  # Validate email format
#     password: str = Form(...),
#     confirm_password: str = Form(...),
#     age: int = Form(...),
#     role: str = Form(...),
#     role_id: str = Form(...),
#     status: str = Form(...),
#     profilePicPath: UploadFile = File(...)
# ):
    
#     try:
#         # Ensure upload directory exists
#         UPLOAD_DIR = "uploads"
#         os.makedirs(UPLOAD_DIR, exist_ok=True)

#         # Validate role_id
#         if not ObjectId.is_valid(role_id):
#             raise HTTPException(status_code=400, detail="Invalid role ID")

#         # Extract file extension
#         file_ext = profilePicPath.filename.split(".")[-1]
#         file_name = f"{ObjectId()}.{file_ext}"
#         file_path = os.path.join(UPLOAD_DIR, file_name)

#         # Save file locally before uploading to Cloudinary
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(profilePicPath.file, buffer)

#         # Upload image to Cloudinary and get URL
#         cloudinary_url = await upload_image(file_path)

#         # Create user data
#         user_data = {
#             "firstname": firstname,
#             "lastname": lastname,
#             "gender": gender,
#             "contact": contact,
#             "email": email,
#             "password": password,
#             "confirm_password": confirm_password,
#             "age": age,
#             "role": role,
#             "role_id": ObjectId(role_id),  # Convert to ObjectId
#             "status": status,
#             "profilePicPath": cloudinary_url  # Store Cloudinary URL
#         }

#         # Insert into MongoDB
#         await image_collection.insert_one(user_data)

#         return {"message": "User created successfully", "profilePicURL": cloudinary_url}
    
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


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
        file_ext = profilePicPath.filename.split(".")[-1]
        file_name = f"{ObjectId()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        
        # Save file locally before uploading to Cloudinary
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profilePicPath.file, buffer)
        
        # Upload image to Cloudinary and get URL
        cloudinary_url = await upload_image(file_path)
        
        # Hash the password for security
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user data
        user_data = {
            "firstname": firstname,
            "lastname": lastname,
            "gender": gender,
            "contact": contact,
            "email": email,
            "password": hashed_password.decode('utf-8'),  # Store hashed password
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