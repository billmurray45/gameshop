from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_session
from models.users import User
from models.games import Game
from dependencies.templates import templates
from services.auth import auth_user, get_current_user
from core.security import decode_access_token
from dependencies.dependencies import current_user_optional

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    token = request.cookies.get("access_token")
    if token and decode_access_token(token):
        return RedirectResponse("/profile", status_code=302)

    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/logout", response_class=HTMLResponse)
async def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("access_token")
    return response


@router.get("/profile", response_class=HTMLResponse)
async def profile_page(
        request: Request,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
        user: User = Depends(current_user_optional)
):
    result = await session.execute(select(Game).where(Game.owner_id == user.id))
    user_games = result.scalars().all()
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": current_user,
            "user_games": user_games
        }
    )


@router.post("/login", response_class=HTMLResponse)
async def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    try:
        token = await auth_user(session, email, password)
        response = RedirectResponse(url="/profile", status_code=302)
        response.set_cookie(key="access_token", value=token, httponly=True)
        return response
    except HTTPException as e:
        return templates.TemplateResponse("login.html", {"request": request, "error": e.detail})
