from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException
from starlette.responses import HTMLResponse
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.v1.tickets.payloads import TicketHistoryPayload
from app.dependencies import discord_authentication
from app.repositories.tickets_history import TicketHistoryRepository
from app.services.make_ticket_history_file_url import make_history_file_url
from app.services.send_tickets_history import send_ticket_stats
from app.structs.ticket_history import TicketHistory

ticket_router = APIRouter()


@ticket_router.get(
    path='/history/{ticket_id}/logs',
    response_class=HTMLResponse,
    dependencies=[],
)
async def get_history_file_logs(ticket_id: str):
    return await TicketHistoryRepository().get_history_html_logs(ticket_id)


@ticket_router.get(
    path='/history/{ticket_number}/logs/url',
    dependencies=[Depends(discord_authentication)],
)
async def get_ticket_logs_url(ticket_number: int) -> str:
    ticket_id = await TicketHistoryRepository().get_ticket_history_id_by_number(ticket_number)
    return make_history_file_url(ticket_id)


@ticket_router.post(
    path='/history',
    dependencies=[Depends(discord_authentication)],
)
async def add_history(
    payload: TicketHistoryPayload,
) -> dict:
    ticket_domain = TicketHistory(**payload.model_dump())
    row_id = await TicketHistoryRepository().create(ticket_domain)

    return {'id': row_id}


@ticket_router.patch(
    path='/history/{ticket_number}/review',
    dependencies=[Depends(discord_authentication)],
)
async def add_review(
    ticket_number: int,
    score: Annotated[int | None, Body()] = None,
    comment: Annotated[str | None, Body()] = None,
    *,
    background_tasks: BackgroundTasks,
):
    if score is None and comment is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Необходимо передать хотя бы один параметр',
        )
    await TicketHistoryRepository().update_ticket_review(
        ticket_number,
        score=score,
        comment=comment,
    )
    background_tasks.add_task(
        send_ticket_stats,
        ticket_number=ticket_number,
        score=score,
        comment=comment,
    )
