from fastapi import FastAPI

from app.entrypoints import lifespan

app = FastAPI(lifespan=lifespan)
