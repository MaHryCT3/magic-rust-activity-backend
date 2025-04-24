import datetime

from pydantic import BaseModel

from app.structs.voices_records.voice import VoiceProcessStatusEnum


class VoiceRecordSchema(BaseModel):
    id: str
    length: float | None
    recorded_at: datetime.datetime | None
    started_at: datetime.datetime | None
    transcribed_text: str | None
    is_process_error: bool
    process_status: VoiceProcessStatusEnum
