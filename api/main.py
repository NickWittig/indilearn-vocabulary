import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from api.core.db.initializers.load_achievements import load_achievements
from api.core.db.initializers.load_items import load_items
from api.core.db.initializers.load_ranks import load_ranks
from api.core.db.initializers.load_users import load_users
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from api.config.config import DataConfig, SecurityConfig
from api.core.db.session import Base, SessionLocal, engine
from api.middleware.authentication_middleware import AuthMiddleware
from api.routes.achievement_routes import achievement_router
from api.routes.item_routes import item_router
from api.routes.leaderboard_routes import leaderboard_router
from api.routes.rank_routes import rank_router
from api.routes.user_routes import user_router

# Enable logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%a, %d %b %Y %H:%M:%S",
    filename="./logs/runtime.log",
    filemode="w",
)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Lifespan event handler for the FastAPI application.
    """
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

    # Load achievements
    session = SessionLocal()
    load_achievements(session, DataConfig.PATH_ACHIEVEMENTS)
    load_ranks(session, DataConfig.PATH_RANKS)
    load_items(session, DataConfig.PATH_ITEMS)
    load_users(session, DataConfig.PATH_USERS)

    yield

    print("Disposing engine...")
    engine.dispose()
    print("Engine disposed successfully!")


app = FastAPI(lifespan=lifespan)


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Route to redirect '/' to '/docs'
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


# Register the routers
app.add_middleware(AuthMiddleware, htpasswd_path=SecurityConfig.HTPASSWD_PATH, whitelist=SecurityConfig.WHITELIST)
app.include_router(item_router, prefix="/item")
app.include_router(leaderboard_router, prefix="/leaderboard")
app.include_router(user_router, prefix="/user")
app.include_router(achievement_router, prefix="/achievement")
app.include_router(rank_router, prefix="/rank")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)
