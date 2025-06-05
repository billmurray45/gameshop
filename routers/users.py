from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserCreate, UserUpdate
from crud.users import get_user_by_username, update_user_by_username
from database import get_session
from dependencies.templates import templates
from services.users import register_user_service
from core.security import decode_access_token
from models.users import User
from dependencies.dependencies import current_user_optional


router = APIRouter()


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    token = request.cookies.get("access_token")
    if token and decode_access_token(token):
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/user/{username}", response_class=HTMLResponse)
async def get_one_user(request: Request, username: str, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_username(username, session)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return templates.TemplateResponse("profile.html", {"request": request, "user": user})


@router.get("/profile/edit", response_class=HTMLResponse)
async def get_edit_user(
    request: Request,
    user: User = Depends(current_user_optional)
):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})


@router.post("/register", response_class=HTMLResponse)
async def register_user(
        session: AsyncSession = Depends(get_session),
        email: str = Form(...),
        username: str = Form(...),
        password: str = Form(...),
        full_name: str = Form(...)
):
    user_date = UserCreate(
        username=username,
        email=email,
        password=password,
        full_name=full_name
    )

    await register_user_service(session, user_date)
    return RedirectResponse("/", status_code=302)


@router.post("/profile/edit", response_class=HTMLResponse)
async def update_user(
        session: AsyncSession = Depends(get_session),
        email: str = Form(...),
        username: str = Form(...),
        password: str = Form(...),
        full_name: str = Form(...),
        user: User = Depends(current_user_optional)
):
    user_date = UserUpdate(
        username=username,
        email=email,
        password=password,
        full_name=full_name
    )
    await update_user_by_username(user.username, session, user_date)
    return RedirectResponse("/profile", status_code=302)
