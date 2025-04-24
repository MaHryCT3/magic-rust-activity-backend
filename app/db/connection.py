from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.config import settings


def get_default_mongo_client() -> AsyncMongoClient:
    return AsyncMongoClient(settings.MONGO_URI)


def get_activity_mongo_database() -> AsyncDatabase:
    return get_default_mongo_client()[settings.MONGO_ACTIVITY_DB]


def get_tickets_mongo_database() -> AsyncDatabase:
    return get_default_mongo_client()[settings.MONGO_TICKETS_DB]


def get_voice_records_mongo_database() -> AsyncDatabase:
    return get_default_mongo_client()[settings.MONGO_VOICE_RECORDS_DB]
