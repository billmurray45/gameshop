from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CartItemBase(BaseModel):
    game_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItemRead(CartItemBase):
    id: int
    user_id: int
    added_at: datetime
    model_config = ConfigDict(from_attributes=True)
