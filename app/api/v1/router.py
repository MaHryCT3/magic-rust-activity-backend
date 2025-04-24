from fastapi import APIRouter

from app.api.v1.activity.api import activity_router
from app.api.v1.tickets.api import ticket_router
from app.api.v1.voice_records.api import voice_record_router

v1_router = APIRouter(prefix='/v1')

v1_router.include_router(activity_router, prefix='/activities')
v1_router.include_router(ticket_router, prefix='/tickets')
v1_router.include_router(voice_record_router, prefix='/voices-records')
