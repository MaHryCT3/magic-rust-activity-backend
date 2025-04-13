from app.config import settings


def make_history_file_url(ticket_id: str) -> str:
    return f'{settings.BASE_URL}/api/v1/tickets/history/{ticket_id}/logs'
