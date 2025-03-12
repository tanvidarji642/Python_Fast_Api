from models.UserModel import User,UserOut,UserLogin
from bson import ObjectId
from config.database import user_collection,role_collection
from fastapi import HTTPException,APIRouter
from fastapi.responses import JSONResponse
import bcrypt
# from utils. import send_mail

from utils.SendMail import send_mail


async def addUser(user:User):
    #typeCast
    #print("user....",user.role_id)
    #convert string id to object it comp.,, to mongo db
    user.role_id = ObjectId(user.role_id)
    print("after type cast",user.role_id)
    result = await user_collection.insert_one(user.dict())
    send_mail(user.email,"User Created","user Created Successfully")
    # return {"Message":"user created successfully"}

    return JSONResponse(status_code=201,content={"message":"user created successfully!!"})
    #raise HTTPException(status_code=500,detail="User not created")

# async def getAllUsers():
#     users = await user_collection.find().to_list()
#     print("users",users)
#     return [UserOut(**user) for user in users]

async def getAllUsers():
    users = await user_collection.find().to_list(length=None)

    print("users...................",users)
    # return [UserOut(**role) for role in users]

    for user in users:
        # Convert role_id from ObjectId to str before validation
        if "role_id" in user and isinstance(user["role_id"], ObjectId):
            user["role_id"] = str(user["role_id"])
        
        # Fetch role details
        role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})  
        
        if role:
            role["_id"] = str(role["_id"])  # Convert role _id to string
            user["role"] = role

    return [UserOut(**user) for user in users]


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
    return UserOut(**result)    