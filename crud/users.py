from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from schemas.users import UserCreate, UserUpdate
from core.security import hash_password


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    hashed_pw = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_pw
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_id(user_id: int, session: AsyncSession):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    return user


async def get_user_by_username(username: str, session: AsyncSession):
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    return user


async def get_user_by_email(user_email: str, session: AsyncSession):
    result = await session.execute(select(User).where(User.email == user_email))
    user = result.scalars().first()
    return user


async def update_user_by_username(username: str, session: AsyncSession, user_data: UserUpdate):
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    update_data = user_data.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(user, field, value)

    await session.commit()
    await session.refresh(user)
    return user
