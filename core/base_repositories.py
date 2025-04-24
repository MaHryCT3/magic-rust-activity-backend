from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from bson import ObjectId
from pymongo.asynchronous.collection import AsyncCollection

DTOModel = TypeVar('DTOModel')


class BaseRepository(ABC, Generic[DTOModel]):
    collection: AsyncCollection

    async def get(self, id: str) -> DTOModel:
        row_object = await self.collection.find_one(ObjectId(id))
        return self._dict_to_object(row_object)

    async def create(self, dto_object: DTOModel) -> DTOModel:
        row_object = self._object_to_dict(dto_object)
        result = await self.collection.insert_one(row_object)

        dto_object.id = str(result.inserted_id)
        return dto_object

    async def update(self, dto_object: DTOModel) -> bool:
        if not dto_object.id:
            raise ValueError('Невозможно обновить запись без ID')

        update_data = self._object_to_dict(dto_object)

        result = await self.collection.update_one(
            {'_id': ObjectId(dto_object.id)},
            {'$set': update_data},
        )
        return result.modified_count > 0

    @staticmethod
    @abstractmethod
    def _object_to_dict(dto_object: DTOModel) -> dict: ...

    @staticmethod
    @abstractmethod
    def _dict_to_object(mongo_data: dict) -> DTOModel: ...
