from fastapi import FastAPI

from app.api.router import api_router
from app.entrypoints import lifespan  # noqa

app = FastAPI(
    lifespan=lifespan,
    title='MagicRust Discord Backend',
)

app.include_router(api_router)
