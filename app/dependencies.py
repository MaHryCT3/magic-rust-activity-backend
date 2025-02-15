from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.config import settings


def discord_authentication(
    key=Security(
        APIKeyHeader(
            name='X-API-Key',
            auto_error=True,
        )
    )
):
    if key != settings.DISCORD_AUTHENTICATION_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Missing or invalid API key',
        )
