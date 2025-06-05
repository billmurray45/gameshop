from __future__ import annotations
from sqlalchemy import String, Integer, func, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from datetime import datetime


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    genre: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    platform: Mapped[str] = mapped_column(String, nullable=False)
    descr: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    poster: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="games")
    comments = relationship("Comment", back_populates="game")
    cart_items = relationship("CartItem", back_populates="game")

    def __repr__(self):
        return f"<Game id={self.id} title={self.title} descr={self.descr}>"
