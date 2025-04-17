

from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum
from typing import Optional

#  Registration schema
class RegisterUserModel(BaseModel):
    name: str = Field(..., min_length=3, max_length=30)
    mobile_no: Optional[str] = Field(None, min_length=10, max_length=10)
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)
    email: EmailStr
    is_varified: Optional[bool] = Field(False)

    @validator("email")
    def trim_email(cls, email):
        return email.strip()

#  Login schema
class LoginUserModel(BaseModel):
    email: EmailStr
    password: str

    @validator("email")
    def trim_email(cls, email):
        return email.strip()

class userRole(str,Enum):
    admin= "admin"
    student= "student"


#  Optional: Full user schema (for DB or fetching user profile)
class UserSchema(BaseModel):
    name: str
    mobile_no: str
    is_varified: bool = False
    password: str
    email: EmailStr
    role:userRole = userRole.student

