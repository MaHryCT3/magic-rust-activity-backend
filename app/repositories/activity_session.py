import datetime
from dataclasses import asdict

from bson import ObjectId
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from app.config import settings
from app.db.connection import get_default_mongo_database
from app.structs.activity_session import ActivitySession


class ActivitySessionRepository:
    def __init__(self, database: AsyncDatabase | None = None):
        self.database = database or get_default_mongo_database()

        self.collection: AsyncCollection = self.database[settings.MONGO_ACTIVITY_SESSION_DATABASE]

    async def get(self, id: str) -> ActivitySession:
        row_object = await self.collection.find_one(ObjectId(id))
        return self._dict_to_object(row_object)

    async def create(self, activity_session: ActivitySession) -> ActivitySession:
        row_object = self._object_to_dict(activity_session)
        result = await self.collection.insert_one(row_object)

        activity_session.id = str(result.inserted_id)
        return activity_session

    async def update(self, activity_session: ActivitySession) -> bool:
        if not activity_session.id:
            raise ValueError('Невозможно обновить запись без ID')

        update_data = self._object_to_dict(activity_session)

        result = await self.collection.update_one(
            {'_id': ObjectId(activity_session.id)},
            {'$set': update_data},
        )
        return result.modified_count > 0

    async def get_user_last_activity_session(
        self,
        user_id: str,
        start_at_max: datetime.datetime,
        channel_id: str,
    ) -> ActivitySession | None:
        result = await self.collection.find_one(
            {
                'user_discord_id': user_id,
                'start_at': {'$lte': start_at_max},
                'channel_id': channel_id,
            },
            sort=[('start_at', -1)],
        )
        if result:
            return self._dict_to_object(result)

    @staticmethod
    def _object_to_dict(activity_session: ActivitySession) -> dict:
        data = asdict(activity_session)
        data['microphone_mute_duration'] = activity_session.microphone_mute_duration.total_seconds()
        data['sound_disabled_duration'] = activity_session.sound_disabled_duration.total_seconds()
        del data['id']
        return data

    @staticmethod
    def _dict_to_object(mongo_data: dict) -> ActivitySession:
        mongo_data['microphone_mute_duration'] = datetime.timedelta(seconds=mongo_data['microphone_mute_duration'])
        mongo_data['sound_disabled_duration'] = datetime.timedelta(seconds=mongo_data['sound_disabled_duration'])
        mongo_data['last_event_at'] = mongo_data['last_event_at'].replace(tzinfo=datetime.UTC)
        mongo_data['id'] = str(mongo_data['_id'])
        del mongo_data['_id']
        return ActivitySession(**mongo_data)
