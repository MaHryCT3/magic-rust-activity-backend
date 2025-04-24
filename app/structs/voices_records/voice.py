import datetime
from dataclasses import dataclass, field
from enum import StrEnum

from app.config import settings
from core.defaults import get_default_datetime_factory


class VoiceProcessStatusEnum(StrEnum):
    AWAITING_PROCESS = 'AWAITING_PROCESS'
    DOWNLOADING_AUDIO = 'DOWNLOADING_AUDIO'
    AUDIO_PROCESS = 'AUDIO_PROCESS'
    AUDIO_TRANSCRIPTION = 'AUDIO_TRANSCRIPTION'
    COMPLETED = 'COMPLETED'


@dataclass
class VoiceRecord:
    length: float | None = None
    transcribed_text: str | None = None
    recorded_at: datetime.datetime | None = None
    started_at: datetime.datetime = field(
        default_factory=get_default_datetime_factory(settings.TIMEZONE),
    )
    process_status: VoiceProcessStatusEnum = VoiceProcessStatusEnum.AWAITING_PROCESS
    is_process_error: bool = False
    id: str | None = None
