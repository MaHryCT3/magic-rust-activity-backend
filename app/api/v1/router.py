from fastapi import APIRouter

from app.api.v1.activity.api import activity_router

v1_router = APIRouter(prefix='/v1')

v1_router.include_router(activity_router, prefix='/activities')
