from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.config import settings


def get_default_mongo_client() -> AsyncMongoClient:
    return AsyncMongoClient(settings.MONGO_URI)


def get_default_mongo_database() -> AsyncDatabase:
    return get_default_mongo_client()[settings.MONGO_DB]
