import logging
from datetime import timedelta, timezone

import colorlog
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(extra='ignore')

    # General
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
    MONGO_DB: str

    MONGO_ACTIVITY_SESSION_DATABASE: str = 'activity_session'

    # MQ
    RABBIT_MQ_URI: str
    ACTIVITY_QUEUE_NAME: str = 'activity'

    @property
    def MONGO_URI(self) -> str:  # noqa
        return f'mongodb://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}'


settings = Settings(_env_file='.env')


def setup_logging():
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt=None,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        },
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        handlers=[console_handler],
    )


setup_logging()

logger = logging.getLogger()
