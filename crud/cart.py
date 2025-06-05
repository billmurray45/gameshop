from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.cart import CartItem
from schemas.cart import CartItemCreate


async def get_cart_items(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(CartItem)
        .options(selectinload(CartItem.game))
        .filter(CartItem.owner_id == user_id)
    )
    cart_items = result.scalars().all()
    return cart_items


async def get_cart_item(session: AsyncSession, user_id: int, game_id: int):
    result = await session.execute(select(CartItem).filter(
        CartItem.owner_id == user_id,
        CartItem.game_id == game_id
    ))
    cart_item = result.scalars().first()
    return cart_item


async def add_to_cart(session: AsyncSession, user_id: int, item_data: CartItemCreate):
    existing_item = await get_cart_item(session, user_id, item_data.game_id)
    if existing_item:
        existing_item.quantity += item_data.quantity
        session.add(existing_item)
        await session.commit()
        await session.refresh(existing_item)
        return existing_item
    else:
        new_item = CartItem(owner_id=user_id, **item_data.dict())
        session.add(new_item)
        await session.commit()
        await session.refresh(new_item)
        return new_item


async def remove_from_cart(session: AsyncSession, user_id: int, game_id: int):
    result = await session.execute(select(CartItem).filter(
        CartItem.owner_id == user_id,
        CartItem.game_id == game_id
    ))
    item = result.scalars().first()
    if item:
        await session.delete(item)
        await session.commit()


async def clear_cart(session: AsyncSession, user_id: int):
    await session.execute(delete(CartItem).filter(CartItem.owner_id == user_id))
    await session.commit()
