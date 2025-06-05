from fastapi import FastAPI
from routers import games, users, auth, cart
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(games.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(cart.router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
