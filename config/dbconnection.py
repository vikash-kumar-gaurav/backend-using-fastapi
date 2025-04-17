# from motor.motor_asyncio import AsyncIOMotorClient
# import asyncio
# import os
# from dotenv import load_dotenv
# from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
# load_dotenv()
# db = None
# mongodbURI = os.getenv("MONGODB_URI")


# async def connectDB():
    
#     try:
#         client = AsyncIOMotorClient(mongodbURI, serverSelectionTimeoutMS=3000)
#         db = client["test"]
#         await client.admin.command('ping')
#         print("connection to mongodb is successfull")
#         print(db)
#         return db
#     except (ConnectionFailure, ServerSelectionTimeoutError) as error:
#         print("error in connection mongodb",str(error)) 
#         raise error   


 
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
load_dotenv()
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError



db = None
mongodbURI = os.getenv("MONGODB_URI")

async def connectDB():
    global db
    try:
        client = AsyncIOMotorClient(mongodbURI, serverSelectionTimeoutMS=3000)
        db = client["test"]
        await client.admin.command("ping")
        print("Connected to MongoDB")
        print(mongodbURI)
        return db
    except (ConnectionFailure, ServerSelectionTimeoutError) as error:
        print("MongoDB connection error:", str(error))
        raise error

def get_db():
    return db
