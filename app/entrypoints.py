from contextlib import asynccontextmanager

import aio_pika
import sentry_sdk
from fastapi import FastAPI

from app.config import settings
from app.consume import activity_consume
from core.consumer import RabbitMQConsumer

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    max_request_body_size='always',
)

rabbit_connection = aio_pika.Connection(
    url=settings.RABBIT_MQ_URI,
)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    # On startup
    activity_consumer = RabbitMQConsumer(
        connection=rabbit_connection,
        queue_name=settings.ACTIVITY_QUEUE_NAME,
        callback=activity_consume,
    )
    await activity_consumer.start()
    yield
    # On shutdown
    await activity_consumer.stop()
