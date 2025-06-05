from typing import Optional
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from dependencies.templates import templates
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from crud.games import get_games, create_game, get_game_by_id, update_game, delete_game
from crud.comments import create_comment, get_game_comments
from models.games import Game
from schemas.games import GameCreate, GameUpdate
from schemas.comments import CommentCreate
from models.users import User
from dependencies.dependencies import current_user_optional

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def get_home_page(
    request: Request,
    session: AsyncSession = Depends(get_session),
    user: User | None = Depends(current_user_optional),
):
    games = await get_games(session)
    return templates.TemplateResponse("home.html", {"request": request, "games": games, "user": user})


@router.get("/games")
async def get_filtered_games(
    request: Request,
    year_min: Optional[str] = Query(None),
    year_max: Optional[str] = Query(None),
    price_min: Optional[str] = Query(None),
    price_max: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session)
):
    def to_int_or_none(value: Optional[str]) -> Optional[int]:
        try:
            if value is None or value == "":
                return None
            return int(value)
        except ValueError:
            return None

    year_min_i = to_int_or_none(year_min)
    year_max_i = to_int_or_none(year_max)
    price_min_i = to_int_or_none(price_min)
    price_max_i = to_int_or_none(price_max)

    query = select(Game)

    if year_min_i is not None:
        query = query.filter(Game.year >= year_min_i)
    if year_max_i is not None:
        query = query.filter(Game.year <= year_max_i)

    if price_min_i is not None:
        query = query.filter(Game.price >= price_min_i)
    if price_max_i is not None:
        query = query.filter(Game.price <= price_max_i)

    result = await session.execute(query)
    games = result.scalars().all()

    return templates.TemplateResponse("list.html", {
        "request": request,
        "games": games
    })


@router.get("/games/create", response_class=HTMLResponse)
async def get_add_page(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})


@router.get("/games/{game_id}", response_class=HTMLResponse)
async def get_game_page(
        request: Request,
        game_id: int,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(current_user_optional)
):
    game = await get_game_by_id(game_id, session)
    if game is None:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    comments = await get_game_comments(session, game_id)
    print("comments", comments, "user", user, "game", game_id)
    return templates.TemplateResponse(
        "full_page.html",
        {
            "request": request,
            "game": game,
            "user": user,
            "comments": comments
        }
    )


@router.get("/games/{game_id}/edit", response_class=HTMLResponse)
async def get_edit_page(game_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    game = await get_game_by_id(game_id, session)
    if game is None:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return templates.TemplateResponse("edit.html", {"request": request, "game": game})


@router.post("/games/create", response_class=HTMLResponse)
async def add_game(
        title: str = Form(),
        genre: str = Form(),
        year: int = Form(),
        platform: str = Form(),
        descr: str = Form(),
        price: int = Form(),
        poster: str = Form(),
        session: AsyncSession = Depends(get_session),
        user: User = Depends(current_user_optional)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Необходимо авторизация")

    game_data = GameCreate(
        title=title,
        genre=genre,
        year=year,
        platform=platform,
        descr=descr,
        price=price,
        poster=poster
    )
    await create_game(session, game_data, owner_id=user.id)
    return RedirectResponse("/", status_code=302)


@router.post("/games/{game_id}/comments", response_class=HTMLResponse)
async def post_comment(
        game_id: int,
        text: str = Form(...),
        session: AsyncSession = Depends(get_session),
        user: User = Depends(current_user_optional)
):
    comment_data = CommentCreate(text=text)
    await create_comment(session, comment_data, game_id=game_id, owner_id=user.id)
    return RedirectResponse(f"/games/{game_id}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/games/{game_id}/edit", response_class=HTMLResponse)
async def edit_game(
        game_id: int,
        title: str = Form(...),
        genre: str = Form(...),
        year: int = Form(...),
        platform: str = Form(...),
        descr: str = Form(...),
        price: int = Form(...),
        poster: str = Form(...),
        session: AsyncSession = Depends(get_session),
        user: User = Depends(current_user_optional)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Требуется авторизация")

    game = await get_game_by_id(game_id, session)
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Игра не найдена")

    if game.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав на редактирование игры")

    game_data = GameUpdate(
        title=title,
        genre=genre,
        year=year,
        platform=platform,
        descr=descr,
        price=price,
        poster=poster
    )

    await update_game(game_id, session, game_data, user.id)
    return RedirectResponse(f"/games/{game_id}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/games/{game_id}/delete", response_class=HTMLResponse)
async def delete_game_by_id(
    game_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user_optional)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Требуется авторизация")

    game = await get_game_by_id(game_id, session)
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Игра не найдена')

    if game.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав на удаление игры")

    await delete_game(game_id, session, user)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
