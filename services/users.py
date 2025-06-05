from fastapi import HTTPException
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from schemas.users import UserCreate
from crud.users import create_user


async def register_user_service(session: AsyncSession, user_data: UserCreate) -> User:
    result = await session.execute(
        select(User).where(
            or_(User.email == user_data.email, User.username == user_data.username)
        )
    )
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email или username уже заняты")

    return await create_user(session, user_data)
