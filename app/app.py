from fastapi import FastAPI
from fastapi.params import Depends

from app.api.router import api_router
from app.dependencies import discord_authentication
from app.entrypoints import lifespan

app = FastAPI(
    lifespan=lifespan,
    title='MagicRust Discord Activity Backend',
    dependencies=[Depends(discord_authentication)],
)

app.include_router(api_router)
