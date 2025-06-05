from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(max_length=25, description="Логин пользователя")
    full_name: str = Field(min_length=5, max_length=50, description="Полное имя пользователя")


class UserCreate(UserBase):
    password: str = Field(max_length=25, description="Пароль пользователя")


class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str] = Field(max_length=25, description="Логин пользователя")
    password: Optional[str] = Field(max_length=25, description="Пароль пользователя")
    full_name: Optional[str] = Field(min_length=5, max_length=50, description="Полное имя пользователя")


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
