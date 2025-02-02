import datetime
import json

from aio_pika import IncomingMessage

from app.config import logger
from app.services.handle_activity_queue import ActivityHandler
from app.structs.activity_message import ActivityMessage
from app.structs.enums import ActivitySessionChannelType, ActivityType


async def activity_consume(message: IncomingMessage):
    data = json.loads(message.body.decode())
    logger.debug(f'Receive data {data}')

    activity_message = ActivityMessage(
        datetime=datetime.datetime.fromisoformat(data['datetime']),
        user_id=data['user_id'],
        channel_id=data['channel_id'],
        channel_type=ActivitySessionChannelType(data['channel_type']),
        activity_type=ActivityType(data['activity_type']),
    )
    logger.info(f'Receive activity message: {activity_message}')

    handler = ActivityHandler(activity_message=activity_message)

    async with message.process():
        await handler.handle()
