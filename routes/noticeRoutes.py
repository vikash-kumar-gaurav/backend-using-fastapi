from fastapi import Request, APIRouter
from config.dbconnection import get_db
from controller.notice_controller import NoticeController
from models.noticemodel import createNotice
from middlewares.auth import get_current_user

notice_router = APIRouter(
    prefix='/api/notice',
    tags=["Notices"]
)

@notice_router.get('/all-notice')
async def get_all_notice():
    db = get_db() # you can yse db = Depends(get_db)
    return await NoticeController.available_notice(db)


@notice_router.post('/create-notice')
async def create_notice(notice_data:createNotice, request:Request):
    db= get_db()
    current_user =await get_current_user(request)
    return await NoticeController.create_notice(db,notice_data, current_user)