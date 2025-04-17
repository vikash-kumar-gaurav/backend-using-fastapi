from fastapi import APIRouter, Request, Depends, HTTPException, BackgroundTasks, Response
from fastapi.responses import JSONResponse
from controller.user_controller import UserController
from models.usermodel import LoginUserModel, RegisterUserModel
from middlewares.auth import get_current_user

from config.dbconnection import get_db
user_router = APIRouter(
    prefix="/api/user",
    tags=["User"]
)

@user_router.post("/register")
async def register_user(user_data: RegisterUserModel):
    db = get_db()
    return await UserController.create_user(db,user_data)


@user_router.post("/login")
async def login_user(user_data: LoginUserModel, request:Request,response:Response,backgroundTask:BackgroundTasks):
    db = get_db()
    return await UserController.login(db, user_data, request,backgroundTask)

@user_router.post('/verify-email/{token}')
async def verify_email(token:str,request:Request):
    db = get_db()
    return await UserController.verifyEmail(db,request,token)

@user_router.get('/profile')
async def myProfile(request:Request):
    response =await get_current_user(request)
    user = response["userData"]
    accessToken = response["new_access_token"]
    user_data = {
        "name":user["name"] ,
        "role":user["role"] 
        
    }
    if accessToken:
        response = JSONResponse(content=user_data)
        response.set_cookie(
            key="accessToken",
            value=accessToken,
            httponly=True,
            secure=False,
            samesite="lax"
        )

        return response
    

    return user_data