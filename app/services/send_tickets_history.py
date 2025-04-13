from app.config import settings
from app.repositories.tickets_history import TicketHistoryRepository
from app.services.make_ticket_history_file_url import make_history_file_url
from app.structs.ticket_history import TicketHistory
from core.api_clients.magic_rust_stats import MagicRustStatsAPI


def build_magic_rust_stats_api() -> MagicRustStatsAPI:
    return MagicRustStatsAPI(
        url=settings.MAGIC_RUST_STATS_URL,
        token=settings.MAGIC_RUST_STATS_TOKEN,
    )


async def send_ticket_stats(
    ticket_number: int,
    score: int | None = None,
    comment: str | None = None,
):
    ticket_history = await TicketHistoryRepository().get_ticket_by_ticket_number(ticket_number)
    if score:
        await send_new_ticket_score(ticket_history)
    if comment:
        await send_ticket_comment(ticket_number, comment)


async def send_new_ticket_score(ticket_history: TicketHistory):
    magic_rust_client = build_magic_rust_stats_api()

    await magic_rust_client.send_ticket_with_score(
        ticket_number=ticket_history.ticket_number,
        author_discord_id=str(ticket_history.author_discord_id),
        moderator_discord_id=(
            str(ticket_history.last_moderator_answer_id) if ticket_history.last_moderator_answer_id else None
        ),
        score=ticket_history.score,
        ticket_url=make_history_file_url(ticket_history.id),
        start_datetime=ticket_history.start_datetime,
        end_datetime=ticket_history.end_datetime,
    )


async def send_ticket_comment(ticket_number: int, comment: str):
    magic_rust_client = build_magic_rust_stats_api()

    await magic_rust_client.send_ticket_comment(
        ticket_number=ticket_number,
        comment=comment,
    )
