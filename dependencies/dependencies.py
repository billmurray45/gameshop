from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from core.security import SECRET_KEY, ALGORITHM
from database import get_session
from crud.users import get_user_by_email
from models.users import User


async def current_user_optional(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> User | None:
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except JWTError as e:
        print("JWT decode error:", e)
        return None

    user = await get_user_by_email(email, session)
    return user
