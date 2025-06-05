from database import engine, Base

from models.users import User
from models.games import Game
from models.cart import CartItem
from models.comments import Comment

Base.metadata.create_all(bind=engine)
