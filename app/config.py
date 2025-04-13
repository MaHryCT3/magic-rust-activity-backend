from datetime import timedelta, timezone

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(extra='ignore')

    # General
    BASE_URL: str = 'http://localhost:8000'
    SENTRY_DSN: str = ''
    DEBUG: bool = False
    TIMEZONE: timezone = timezone(offset=timedelta(hours=3), name='Europe/Moscow')

    # Application
    DISCORD_AUTHENTICATION_TOKEN: str

    # Database
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_ACTIVITY_DB: str = 'activity'
    MONGO_TICKETS_DB: str = 'tickets'

    MONGO_ACTIVITY_SESSION_COLLECTION: str = 'activity_session'
    MONGO_HISTORY_LOGS_COLLECTION: str = 'history_logs'

    # MQ
    RABBIT_MQ_URI: str
    ACTIVITY_QUEUE_NAME: str = 'activity'

    # Integration
    ## Magic Rust
    MAGIC_RUST_STATS_URL: str
    MAGIC_RUST_STATS_TOKEN: str

    @property
    def MONGO_URI(self) -> str:  # noqa
        return f'mongodb://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}'


settings = Settings(_env_file='.env')
