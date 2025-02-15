import datetime

from fastapi import APIRouter

from app.repositories.activity_session import ActivitySessionRepository

activity_router = APIRouter()


@activity_router.get(path='/')
async def get_user_activities(
    user_discord_id: str | None = None,
    channel_id: str | None = None,
    start_at: datetime.datetime | None = None,
    end_at: datetime.datetime | None = None,
    limit: int = 10,
    offset: int | None = None,
):
    data = await ActivitySessionRepository().aggregate_filtered_sessions(
        user_discord_id=user_discord_id,
        channel_id=channel_id,
        start_at=start_at,
        end_at=end_at,
        limit=limit,
        offset=offset,
    )
    return data
