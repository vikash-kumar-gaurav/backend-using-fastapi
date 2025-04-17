import jwt
import datetime
import os
from dotenv import load_dotenv
load_dotenv

ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
REFRESH_TOKEN_SECRET_KEY = os.getenv("REFRESH_TOKEN_SECRET_KEY")

def create_access_token(data:dict):
    try:
        to_encode = data.copy()
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        to_encode.update({"exp":expire})
        token = jwt.encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm = "HS256")
        return token
    except Exception as error:
        print("error from create_access_token", error)
def create_refresh_token(data:dict):
    try:
        to_encode = data.copy()
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        to_encode.update({"exp":expire})
        token = jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm="HS256")
        return token
    except Exception as error:
        print("error from create_refresh_token",error)