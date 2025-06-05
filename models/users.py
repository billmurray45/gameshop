from sqlalchemy import String, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    games = relationship("Game", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")
    cart_items = relationship("CartItem", back_populates="owner")

    def __repr__(self):
        return f"<User id={self.id} username={self.username} email={self.email}>"