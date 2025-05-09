import datetime
from dataclasses import dataclass


@dataclass
class TicketHistory:
    author_discord_id: int
    moderators_discord_ids: list[int]
    last_moderator_answer_id: int | None
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
    ticket_number: int
    html_logs: str
    score: int | None = None
    comment: str | None = None
    id: None = None
