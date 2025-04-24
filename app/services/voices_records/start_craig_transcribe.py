from dataclasses import dataclass

from app.repositories.voices_records import VoiceRecordsRepository
from app.services.voices_records.craig_info_parser import parse_craig_record_id_and_key
from app.services.voices_records.tasks import transcribe_craig_audio
from app.structs.voices_records import VoiceRecord
from core.actions.abstract import AbstractAction


@dataclass
class StartCraigTranscribeAction(AbstractAction[str]):
    craig_record_url: str

    async def action(self) -> str:
        record_id, key = parse_craig_record_id_and_key(self.craig_record_url)

        voice_record = await VoiceRecordsRepository().create(VoiceRecord())
        transcribe_craig_audio.send(record_id, key, voice_record.id)
        return voice_record.id
