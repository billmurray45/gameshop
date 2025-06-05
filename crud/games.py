from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.games import Game
from schemas.games import GameCreate, GameUpdate


async def create_game(session: AsyncSession, game_data: GameCreate, owner_id: int) -> Game:
    new_game = Game(**game_data.dict(), owner_id=owner_id)
    session.add(new_game)
    await session.commit()
    await session.refresh(new_game)
    return new_game


async def get_games(session: AsyncSession):
    result = await session.execute(select(Game))
    return result.scalars().all()


async def get_game_by_id(game_id: int, session: AsyncSession):
    result = await session.execute(select(Game).where(Game.id == game_id))
    game = result.scalars().first()
    return game


async def update_game(game_id: int, session: AsyncSession, game_data: GameUpdate, user_id: int):
    result = await session.execute(select(Game).where(Game.id == game_id))
    game = result.scalars().first()

    if not game:
        return None

    if game.owner_id != user_id:
        raise PermissionError("Нет прав на обновление этой игры")

    for field, value in game_data.dict(exclude_unset=True).items():
        setattr(game, field, value)
    await session.commit()
    return game


async def delete_game(game_id: int, session: AsyncSession, user_id: int):
    result = await session.execute(select(Game).where(Game.id == game_id))
    game = result.scalars().first()

    if not game:
        return None

    if game.owner_id != user_id:
        raise PermissionError("Нет прав на удаление этой игры")

    await session.delete(game)
    await session.commit()
    return {"message": "Игра успешно удалена!"}
