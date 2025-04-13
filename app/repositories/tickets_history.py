import datetime
from dataclasses import asdict

from bson import ObjectId

from app.config import settings
from app.db.connection import get_tickets_mongo_database
from app.structs.ticket_history import TicketHistory


class TicketHistoryRepository:
    def __init__(self):
        self.collection = get_tickets_mongo_database()[settings.MONGO_HISTORY_LOGS_COLLECTION]

    async def get_history_html_logs(self, ticket_id: str) -> str:
        history_data = await self.collection.find_one(ObjectId(ticket_id))
        return history_data['html_logs']

    async def get_ticket_history_id_by_number(self, ticket_number: int) -> str:
        history_data = await self.collection.find_one({'ticket_number': ticket_number})
        return str(history_data['_id'])

    async def create(
        self,
        ticket_history: TicketHistory,
    ) -> str:
        raw_object = self._object_to_dict(ticket_history)
        result = await self.collection.insert_one(raw_object)
        return str(result.inserted_id)

    async def update_ticket_review(self, ticket_number: int, score: int | None, comment: str | None = None):
        update_data = {}
        if score:
            update_data['score'] = score
        if comment:
            update_data['comment'] = comment

        await self.collection.update_one(
            {'ticket_number': ticket_number},
            {'$set': update_data},
        )

    async def get_ticket_by_ticket_number(self, ticket_number: int) -> TicketHistory | None:
        result = await self.collection.find_one(
            {
                'ticket_number': ticket_number,
            },
        )
        if result:
            return self._dict_to_object(result)

    @staticmethod
    def _object_to_dict(ticket_history: TicketHistory) -> dict:
        data = asdict(ticket_history)
        del data['id']
        return data

    @staticmethod
    def _dict_to_object(mongo_data: dict) -> TicketHistory:
        mongo_data['start_datetime'] = mongo_data['start_datetime'].replace(tzinfo=datetime.UTC)
        mongo_data['end_datetime'] = mongo_data['end_datetime'].replace(tzinfo=datetime.UTC)
        mongo_data['id'] = str(mongo_data['_id'])
        del mongo_data['_id']
        return TicketHistory(**mongo_data)
