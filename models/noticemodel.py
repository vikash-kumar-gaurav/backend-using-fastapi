from pydantic import BaseModel, Field, validator
from typing import Optional
import datetime
from bson import objectid
# for creating a new routine
class createNotice(BaseModel):
    title:str = Field(..., min_length=3, max_length=30)
    content:str =Field(..., min_length=10,max_length=5000)
    department:str = Field(min_length=2, max_length=10)

# for seeing notice
class availableNotice(BaseModel):
    title:str
    content:str
    department:str
    posted_by:str
    created_at:datetime.datetime  

#notice Schema
class noticeSchema(BaseModel):
    title:str
    content:str
    department:Optional[str] = None
    created_at:datetime.datetime
    created_by:str