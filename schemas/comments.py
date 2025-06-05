from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class CommentBase(BaseModel):
    text: str = Field(min_length=30, max_length=1000, description="Комментарии игры")


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    text: Optional[str] = Field(min_length=30, max_length=1000, description="Комментарии игры")


class UserInfo(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)


class CommentRead(CommentBase):
    id: int
    created_at: datetime
    owner: UserInfo
    game_id: int
    model_config = ConfigDict(from_attributes=True)
