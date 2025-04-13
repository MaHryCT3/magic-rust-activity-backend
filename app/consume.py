import datetime
import json

from aio_pika import IncomingMessage

from app.services.handle_activity_queue import ActivityHandler
from app.structs.activity_message import ActivityMessage
from app.structs.enums import ActivitySessionChannelType, ActivityStatus
from core.logger import logger


async def activity_consume(message: IncomingMessage):
    data = json.loads(message.body.decode())
    logger.debug(f'Receive data {data}')

    activity_message = ActivityMessage(
        datetime=datetime.datetime.fromisoformat(data['datetime']).astimezone(datetime.UTC),
        user_id=data['user_id'],
        channel_id=data['channel_id'],
        channel_type=ActivitySessionChannelType(data['channel_type']),
        activity_status=ActivityStatus(data['activity_status']),
        is_microphone_muted=data['is_microphone_muted'],
        is_sound_muted=data['is_sound_muted'],
    )
    logger.info(f'Receive activity message: {activity_message}')

    handler = ActivityHandler(activity_message=activity_message)

    async with message.process():
        await handler.handle()
