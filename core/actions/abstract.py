from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ActionReturn = TypeVar('ActionReturn')


class AbstractAction(ABC, Generic[ActionReturn]):
    async def load_data(self):
        pass

    async def validate(self):  # noqa: B027
        pass

    @abstractmethod
    async def action(self) -> ActionReturn:
        pass

    async def execute(self) -> ActionReturn:
        await self.load_data()
        await self.validate()
        return await self.action()

    async def execute_no_validation(self) -> ActionReturn:
        await self.load_data()
        return await self.action()
