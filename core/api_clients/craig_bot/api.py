from typing import Final

from core.api_clients.craig_bot.models import CookStatus
from core.clients.http import HTTPClient


class CraigBotAPI:
    COOK_URI: Final[str] = 'api/recording/{record_id}/cook'
    DOWNLOAD_URI: Final[str] = 'dl/{file_name}'

    def __init__(self, key: str, base_url: str = 'https://craig.horse'):
        self.http_client = HTTPClient(base_url=base_url)
        self.key = key

    async def start_cook_flac(self, record_id: str):
        response = await self.http_client.post(
            url=self.COOK_URI.format(record_id=record_id),
            query={'key': self.key},
            body={
                'container': 'zip',
                'dynaudnorm': False,
                'format': 'flac',
            },
            headers={
                'content-type': 'application/json',
            },
        )
        return CookStatus(**response.json())

    async def cook(self, record_id: str):
        response = await self.http_client.get(
            url=self.COOK_URI.format(record_id=record_id),
            query={'key': self.key},
        )
        return CookStatus(**response.json())

    async def download_cook(self, file_name: str):
        response = await self.http_client.get(
            url=self.DOWNLOAD_URI.format(file_name=file_name),
        )
        return response.content
