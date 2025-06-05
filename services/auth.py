from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import User
from fastapi import HTTPException, status, Request, Depends
from core.security import verify_password, create_access_token, decode_access_token
from database import get_session


async def auth_user(session: AsyncSession, user_email: str, password: str):
    result = await session.execute(select(User).where(User.email == user_email))
    user = result.scalars().first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )

    return create_access_token(data={"sub": user.email})


async def get_current_user(request: Request, session: AsyncSession = Depends(get_session)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user_email = decode_access_token(token)
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await session.execute(select(User).where(User.email == user_email))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
