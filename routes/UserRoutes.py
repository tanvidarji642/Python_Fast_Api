from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from pydantic import EmailStr  
from controllers.UserControllar import (
    addUser,
    getAllUsers,
    deleteUser,
    getUserById,
    loginUser,
    addSignupWithFile,
    updateUser, 
    forgotPassword,
    resetPassword
)
from models.UserModel import User, UserOut, UserLogin, ResetPasswordReq

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
    
@router.put("/user/{userId}")
async def put_user(
    userId: str,
    firstname: str = Form(...),
    lastname: str = Form(...),
    gender: str = Form(...),
    contact: int = Form(...),
    email: EmailStr = Form(...),
    age: int = Form(...),
    role: str = Form(...),
    role_id: str = Form(...),
    status: bool = Form(...)
):
    try:
        # Prepare the update data as a dictionary
        update_data = {
            "firstname": firstname,
            "lastname": lastname,
            "gender": gender,
            "contact": contact,
            "email": email,
            "age": age,
            "role": role,
            "role_id": role_id,
            "status": status,
        }

        # Call the controller function to update the user
        updated_user = await updateUser(userId, update_data)
        return {"message": "User updated successfully", "user": updated_user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/user/forgotpassword")
async def forgot_password(email:str):
    return await forgotPassword(email)

@router.post("/user/resetpassword")
async def reset_password(data:ResetPasswordReq):
    return await resetPassword(data)