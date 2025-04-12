from fastapi import APIRouter

from app.api.v1.activity.api import activity_router
from app.api.v1.tickets.api import ticket_router

v1_router = APIRouter(prefix='/v1')

v1_router.include_router(activity_router, prefix='/activities')
v1_router.include_router(ticket_router, prefix='/tickets')
