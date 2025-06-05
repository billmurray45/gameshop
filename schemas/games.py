from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GameBase(BaseModel):
    title: str = Field(min_length=3, max_length=50, description="Название игры")
    genre: str = Field(max_length=300, description="Жанр игры")
    year: int = Field(ge=2000, le=2050, description="Год выпуска игры")
    platform: str = Field(max_length=50, description="Платформы игры")
    descr: str = Field(min_length=40, max_length=1000, description="Описание игры")
    price: int = Field(ge=500, le=200000, description="Цена игры")
    poster: str = Field(min_length=3, max_length=150, description="Изображение игры")


class GameCreate(GameBase):
    pass


class GameUpdate(BaseModel):
    title: Optional[str] = Field(min_length=3, max_length=50, description="Название игры")
    genre: Optional[str] = Field(max_length=300, description="Жанр игры")
    year: Optional[int] = Field(ge=2000, le=2050, description="Год выпуска игры")
    platform: Optional[str] = Field(max_length=50, description="Платформы игры")
    descr: Optional[str] = Field(min_length=40, max_length=1000, description="Описание игры")
    price: Optional[int] = Field(ge=500, le=200000, description="Цена игры")
    poster: Optional[str] = Field(min_length=3, max_length=150, description="Изображение игры")


class GameRead(GameBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
