from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str

class CreateUser(UserBase):
    password_hash: str

class UpdateUser(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: Optional[str] = None