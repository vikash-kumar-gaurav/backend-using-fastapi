from fastapi import FastAPI
from config.dbconnection import connectDB
from routes.userRoutes import user_router
from routes.noticeRoutes import notice_router

from fastapi.middleware.cors import CORSMiddleware

app= FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["GET","POST"],  # GET, POST, PUT, DELETE etc.
    allow_headers=["*"],  # Authorization, Content-Type etc.
)

@app.on_event("startup")
async def startup_event():
    await connectDB()

 

app.include_router(user_router)
app.include_router(notice_router)
@app.get('/')
async def send_data():
    try:
        return {"data":"hi therre"}
    except Exception as e:
        return {"error":{e}}    
