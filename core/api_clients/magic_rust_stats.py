import datetime
from typing import Final

from core.clients.http import HTTPClient


class MagicRustStatsAPI:
    TICKETS_POST_METHOD: Final[str] = 'discordTickets.postTicket'
    TICKET_PATCH_METHOD: Final[str] = 'discordTickets.patchTicket'

    def __init__(self, url: str, token: str):
        self.http_client = HTTPClient(base_url=url)
        self.token = token

    async def send_ticket_with_score(
        self,
        ticket_number: int,
        author_discord_id: str,
        moderator_discord_id: str | None,
        score: int,
        ticket_url: str,
        start_datetime: datetime.datetime,
        end_datetime: datetime.datetime,
    ):
        payload = {
            'ticket_number': ticket_number,
            'author_discord_id': author_discord_id,
            'moderator_discord_id': moderator_discord_id,
            'score': score,
            'ticket_url': ticket_url,
            'start_datetime': start_datetime.timestamp(),
            'end_datetime': end_datetime.timestamp(),
        }
        return await self._make_request(
            method_name=self.TICKETS_POST_METHOD,
            payload=payload,
        )

    async def send_ticket_comment(self, ticket_number: int, comment: str):
        payload = {
            'ticket_number': ticket_number,
            'comment': comment,
        }
        return await self._make_request(
            method_name=self.TICKET_PATCH_METHOD,
            payload=payload,
        )

    async def _make_request(self, method_name: str, payload: dict):
        payload = payload | {'key': self.token, 'method': method_name}

        return await self.http_client.get(
            '',
            query=payload,
        )
