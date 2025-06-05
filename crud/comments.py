from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from models.comments import Comment
from schemas.comments import CommentCreate, CommentUpdate


async def create_comment(session: AsyncSession, comment_data: CommentCreate, game_id: int, owner_id: int) -> Comment:
    new_comment = Comment(**comment_data.dict(), owner_id=owner_id, game_id=game_id)
    session.add(new_comment)
    await session.commit()
    await session.refresh(new_comment)
    return new_comment


async def get_game_comments(session: AsyncSession, game_id: int):
    result = await session.execute(
        select(Comment)
        .options(selectinload(Comment.owner))
        .where(Comment.game_id == game_id))
    comment = result.scalars().all()
    return comment
