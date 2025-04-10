from models.UserModel import User,UserOut,UserLogin,ResetPasswordReq
from bson import ObjectId
from config.database import user_collection,role_collection
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
import jwt 
import datetime
from urllib.parse import unquote
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError





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
        print("users...................", users)

        for user in users:
            # Convert role_id from ObjectId to str before validation
            if "role_id" in user and isinstance(user["role_id"], ObjectId):
                user["role_id"] = str(user["role_id"])

            # Fetch role details
            role = None
            if user.get("role_id"):
                role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})
                if role:
                    role["_id"] = str(role["_id"])  # Convert role _id to string
                    user["role"] = role
                else:
                    user["role"] = None  # Ensure role is None if not found

        return [UserOut(**user) for user in users]
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

        # Fetch role details if role_id exists
        if user.get("role_id"):
            role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})
            if role:
                role["_id"] = str(role["_id"])  # Convert role _id to string
                user["role"] = role
            else:
                user["role"] = None
        else:
            user["role"] = None

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
    
async def updateUser(userId: str, update_data: dict):
    try:
        if not ObjectId.is_valid(userId):
            raise HTTPException(status_code=400, detail="Invalid user ID")

        # Convert role_id to ObjectId if it exists
        if "role_id" in update_data and ObjectId.is_valid(update_data["role_id"]):
            update_data["role_id"] = ObjectId(update_data["role_id"])

        result = await user_collection.update_one(
            {"_id": ObjectId(userId)},
            {"$set": update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found or no changes made")

        updated_user = await user_collection.find_one({"_id": ObjectId(userId)})

        return {
            "message": "User updated successfully",
            "user": updated_user
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")
    

SECRET_KEY ="royal"

def generate_token(email: str):
    from datetime import datetime, timedelta
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": email, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

async def forgotPassword(email:str):
    foundUser = await user_collection.find_one({"email":email})
    if not foundUser:
        raise HTTPException(status_code=404,detail="email not found")
    
    token = generate_token(email)
    resetLink = f"http://localhost:5173/resetpassword/{token}"
    body = f"""
    <html>
        <h1>HELLO THIS IS RESET PASSWORD LINK EXPIRES IN 1 hour</h1>
        <a href= "{resetLink}">RESET PASSWORD</a>
    </html>
    """
    subject = "RESET PASSWORD"
    send_mail(email,subject,body)
    return {"message":"reset link sent successfully"}
    

async def resetPassword(data: ResetPasswordReq):
    try:
        print(f"Received token: {data.token}")
        
        # Ensure the token is URL-decoded
        token = unquote(data.token)

        # Validate the token format
        if token.count(".") != 2:
            raise HTTPException(status_code=400, detail="Invalid token format: Token must have three segments")

        # Decode the token
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Reset token has expired")
        except InvalidTokenError as e:
            print(f"JWT Decode Error: {e}")
            raise HTTPException(status_code=400, detail="Reset token is invalid or malformed")

        # Extract email from the token payload
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token payload: Email missing")

        # Hash the new password
        hashed_password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Update the user's password in the database
        result = await user_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found or password not updated")

        return {"message": "Password updated successfully"}

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong while resetting password")