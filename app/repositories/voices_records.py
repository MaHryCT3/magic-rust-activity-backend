import datetime
from dataclasses import asdict

from bson import ObjectId

from app.config import settings
from app.db.connection import get_voice_records_mongo_database
from app.structs.voices_records import VoiceRecord
from app.structs.voices_records.voice import VoiceProcessStatusEnum
from core.base_repositories import BaseRepository


class VoiceRecordsRepository(BaseRepository[VoiceRecord]):
    collection = get_voice_records_mongo_database()[settings.MONGO_VOICE_RECORDS_COLLECTION]

    async def update_process_status(self, id: str, new_status: VoiceProcessStatusEnum):
        update_data = {'process_status': new_status}
        await self.collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': update_data},
        )

    async def update_is_process_error(self, id: str, is_error: bool):
        update_data = {'is_process_error': is_error}
        await self.collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': update_data},
        )

    @staticmethod
    def _object_to_dict(voice_record: VoiceRecord) -> dict:
        data = asdict(voice_record)
        del data['id']
        return data

    @staticmethod
    def _dict_to_object(mongo_data: dict) -> VoiceRecord:
        if recorded_at := mongo_data['recorded_at']:
            mongo_data['recorded_at'] = recorded_at.replace(tzinfo=datetime.UTC)
        if started_at := mongo_data['started_at']:
            mongo_data['started_at'] = started_at.replace(tzinfo=datetime.UTC)
        mongo_data['process_status'] = VoiceProcessStatusEnum(mongo_data['process_status'])
        mongo_data['id'] = str(mongo_data['_id'])
        del mongo_data['_id']
        return VoiceRecord(**mongo_data)
