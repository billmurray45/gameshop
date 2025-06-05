from fastapi import APIRouter, HTTPException, status, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models.users import User
from schemas.cart import CartItemCreate
from crud.cart import get_cart_items, get_cart_item, add_to_cart, remove_from_cart, clear_cart
from dependencies.templates import templates
from dependencies.dependencies import current_user_optional

router = APIRouter()


@router.get("/cart", response_class=HTMLResponse)
async def get_cart_page(
        request: Request,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(current_user_optional)
):
    cart_items = await get_cart_items(session, user_id=user.id)
    return templates.TemplateResponse("cart.html", {"request": request, "cart_items": cart_items, "user": user})


@router.post("/cart")
async def add_game_to_cart(
    game_id: int = Form(...),
    quantity: int = Form(1),
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user_optional)
):
    item = CartItemCreate(game_id=game_id, quantity=quantity)
    await add_to_cart(session, user_id=user.id, item_data=item)
    return RedirectResponse(url="/cart", status_code=303)


@router.post("/cart/remove")
async def remove_game(
        game_id: int = Form(...),
        session: AsyncSession = Depends(get_session),
        user: User = Depends(current_user_optional)
):
    await remove_from_cart(session, user_id=user.id, game_id=game_id)
    return RedirectResponse("/cart", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/cart/clear")
async def clear_cart_all(
        session: AsyncSession = Depends(get_session),
        user: User = Depends(current_user_optional)
):
    await clear_cart(session, user_id=user.id)
    return RedirectResponse("/cart", status_code=status.HTTP_303_SEE_OTHER)