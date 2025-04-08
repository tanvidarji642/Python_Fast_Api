# from fastapi import APIRouter
# from controllers.UserControllar import addUser,getAllUsers,deleteUser,getUserById,loginUser,addSignupWithFile
# from models.UserModel import User,UserOut,UserLogin
# from fastapi import APIRouter, Form, UploadFile, File


# router = APIRouter()

from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from pydantic import EmailStr  # Import EmailStr for validation
from controllers.UserControllar import (
    addUser,
    getAllUsers,
    deleteUser,
    getUserById,
    loginUser,
    addSignupWithFile,
)
from models.UserModel import User, UserOut, UserLogin

router = APIRouter()


@router.post("/user/")
async def post_user(user:User):
    return await addUser(user)

@router.get("/users/")
async def get_users():
    return await getAllUsers()
 
@router.delete("/user/{userId}")
async def delete_user(userId:str):
    return await deleteUser(userId)

@router.get("/user/{userId}")
async def get_user_byId(userId:str):
    return await getUserById(userId)

@router.post("/user/login")
async def login_user(user: UserLogin):
    return await loginUser(user)

@router.post("/user/addwithfile")  # Changed from just "/addwithfile" to "/user/addwithfile"
async def addwithfile(
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
        return await addSignupWithFile(
            firstname, lastname, gender, contact, email, password, confirm_password, age, role, role_id, status, profilePicPath
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    

    #put user/{userId}
# @router.put("/user/{userId}")   
# async def put_user(userId:str,user:User):
#     try:
#         # Assuming you have a function to update user details in your controller
#         updated_user = await updateUser(userId, user)
#         return {"message": "User updated successfully", "user": updated_user}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")