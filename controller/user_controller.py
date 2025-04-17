from fastapi import HTTPException, Response
from passlib.context import CryptContext
from bson import objectid
from utils.jwt_handler import create_access_token, create_refresh_token
from utils.send_mail import send_verification_email_atREgistration_time
from config.dbconnection import get_db
from models.usermodel import RegisterUserModel, LoginUserModel
from datetime import datetime
import httpx
from utils.send_mail import send_login_alert
from fastapi.responses import JSONResponse
from jose import JWTError, ExpiredSignatureError, jwt
import os


get_db()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")

class UserController:
    #create a new user
    @staticmethod
    async def create_user(db, user_data:RegisterUserModel):
        try:

            print(user_data)
            if not user_data.email or not user_data.password or not user_data.confirm_password:
                raise HTTPException(status_code=400, detail= "Missing required fields")
            
            if user_data.password != user_data.confirm_password :
                raise HTTPException(status_code=401, detail="password and confirm Password must be same")
        
            
            existing_user = await db["users"].find_one({"email":user_data.email})
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            
            user_data.password = pwd_context.hash(user_data.password)

            user_dict = user_data.dict(exclude={"confirm_password"})
            user_dict["role"]= "student"

            result = await db["users"].insert_one(user_dict)
            accessToken = create_access_token({"email":user_data.email})
            #send verification email
            await send_verification_email_atREgistration_time(user_data.email,accessToken)

            return {
                "msg":"User created. Verify you account through mail",
                "user_Id":str(result.inserted_id),
                "accessToken":accessToken
            }

        except HTTPException as http_err:
            raise http_err  # yeh FastAPI ko handle karne do properly
        
        except Exception as error:
            print("error from UserController and in create_user", str(error))
            raise HTTPException(status_code=500, detail="server error try later")

    #login controller
    @staticmethod
    async def login(db, user_data:LoginUserModel, request, backgroundTask):
        try:
            
            #challo ab request se pata lagete hai kha se request aaya hai
            ip = request.client.host #ip address
            user_agent = request.headers.get("user-agent")
            login_time = datetime.utcnow()  #device name or browser
            

            #we will call an api to fecch address from api
            async with httpx.AsyncClient() as client:
                response = await client.get(f"http://ip-api.com/json/{ip}")
                loc_data = response.json()
            
            location = {
            "city": loc_data.get("city"),
            "region": loc_data.get("regionName"),
            "country": loc_data.get("country")
            }
            print("IP-",ip)
            print("device name-",user_agent)
            
            print("Location",location)
            if not user_data.email or not user_data.password:
                raise HTTPException(status_code=401, detail="All credientials are required")

            validEmail = await db["users"].find_one({"email":user_data.email})
            if not validEmail:
                raise HTTPException(status_code=404, detail="No user found ")
            
            isValidPassword = pwd_context.verify(user_data.password, validEmail["password"])
            if not isValidPassword:
                raise HTTPException(status_code=401,detail="Invalid credentials")
            
            # sab valid ho gaya ab token bhej de aur ek mail bhi ki user is device per login hua hai aur itne bje
            backgroundTask.add_task(send_login_alert,validEmail["name"],user_data.email,location,login_time)
            

            accessToken =  create_access_token({"email":user_data.email})
            refreshToken = create_refresh_token({"email":user_data.email})
            

            response = JSONResponse(content={
            "msg": f"hey {validEmail['name']} welcome back",
            "accessToken": accessToken,
            "refreshToken" : refreshToken,
            "user":{
                "name":validEmail["name"],
                "role":validEmail["role"]
            }

            })

            response.set_cookie(
            key="accessToken",
            value=accessToken,
            httponly=True,
            secure=False,
            samesite="lax"
            )

            response.set_cookie(
                key="refreshToken",
                value=refreshToken,
                httponly=True,
                secure=False,
                samesite='lax'
            )

            return response
        
        except HTTPException as http_err:
            raise http_err  # yeh FastAPI ko handle karne do properly
    
        except Exception as error:
            print("Error from login from usserController",(error))
            raise HTTPException(status_code=500, detail="Server error try later")
        


    #verify Email after registering
    @staticmethod
    async def verifyEmail(db,request,token):
        ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
        ALGORITHM="HS256"
        try:
            if not token:
               raise HTTPException(status_code=401, detail="no token found")

            payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
            user_email= payload.get("email")
            await db["user"].update_one(
                {"email":user_email},
                {"$set":{"is_varified" :True}}
            )
            return {
                "msg":"email is verified just logIN"
            }

        except ExpiredSignatureError:
            raise HTTPException(status_code=402,detail="token expired ")
