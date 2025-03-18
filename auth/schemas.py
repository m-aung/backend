from pydantic import BaseModel, EmailStr
from typing import Optional
from database.schemas import UserBase

class UserSignup(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str
    created_at: Optional[str] = None

    class Config:
        orm_mode = True