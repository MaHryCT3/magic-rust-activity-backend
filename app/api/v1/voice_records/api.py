from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Body, Depends

from app.api.v1.voice_records.models import VoiceRecordSchema
from app.dependencies import discord_authentication
from app.repositories.voices_records import VoiceRecordsRepository
from app.services.voices_records.start_craig_transcribe import (
    StartCraigTranscribeAction,
)

voice_record_router = APIRouter()


@voice_record_router.post(
    path='/craig/start_transcribe',
    dependencies=[Depends(discord_authentication)],
)
async def start_craig_transcribe(craig_download_url: Annotated[str, Body()]):
    action = StartCraigTranscribeAction(craig_record_url=craig_download_url)
    record_id = await action.execute()
    return {'id': record_id}


@voice_record_router.get(
    path='/{id}',
    dependencies=[Depends(discord_authentication)],
    response_model=VoiceRecordSchema,
)
async def get_voice_record(id: str):
    record = await VoiceRecordsRepository().get(id=id)
    return VoiceRecordSchema(**asdict(record))
