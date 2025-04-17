
from fastapi import Request, HTTPException
from jose import JWTError, ExpiredSignatureError, jwt
from config.dbconnection import get_db
from utils.jwt_handler import create_access_token
import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
REFRESH_TOKEN_SECRET_KEY = os.getenv("REFRESH_TOKEN_SECRET_KEY")
ALGORITHM = "HS256"

async def get_current_user(request:Request):
    db = get_db()

    try:
        access_token = None
        refresh_token= None
        payload = None
        new_access_token = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            access_token = auth_header.replace("Bearer ", "")
        else:
            access_token = request.cookies.get("accessToken")
            refresh_token = request.cookies.get("refreshToken")

        if not access_token and not refresh_token:
            raise HTTPException(status_code=401,detail="No accesstoken found nor the refresh token")
        
        #try if accesstoken is valid
        try:
            payload = jwt.decode(access_token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
            user_email = payload.get("email")
            if user_email is None:
                 raise HTTPException(status_code=401, detail="Invalid token")
            
            userData = await db["users"].find_one({"email":user_email})
            if  not userData:
                raise HTTPException(status_code=401, detail="no user found")
            
            return {
                "userData":userData,
                "new_access_token":None
            }

        except ExpiredSignatureError:
            #now accessToken is expired try with refresh token 
            if not refresh_token:
                raise HTTPException(status_code=401,detail="accessToken expired and no refresh token found")
            
            try:
                payload = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
                user_email = payload.get("email")
                if not user_email:
                    raise HTTPException(status_code=401, detail="Invalid refresh token")
                
                userData = await db["users"].find_one({"email":user_email})
                if not userData:
                    raise HTTPException(status_code=401, detail="no user found")
                new_access_token = create_access_token({"email":user_email})
                print("userData is ",userData)
                
                return {
                    "userData":userData,
                    "new_access_token":new_access_token
                }

            except ExpiredSignatureError:
                raise HTTPException(status_code=401,detail="refresh token is expired plese login again")    


    except Exception as error:
        print("error from get_current_user",error)
        raise HTTPException(status_code=500, detail="server error try later")
            

