import shutil
from dataclasses import dataclass, field

import dramatiq

from app.repositories.voices_records import VoiceRecordsRepository
from app.services.voices_records.audio_merge import AudioMergeAction
from app.services.voices_records.craig_download import (
    CraigDownloadedVoices,
    CraigVoiceDownload,
)
from app.services.voices_records.transcript import TranscriptAudioAction
from app.structs.voices_records.voice import VoiceProcessStatusEnum


@dataclass
class CraigAudioTranscribePipeline:
    craig_record_id: str
    craig_api_key: str
    voice_record_id: str

    voice_record_repository: VoiceRecordsRepository = field(default_factory=VoiceRecordsRepository, init=False)

    _remove_dir_on_ready: str | None = field(default=None, init=False)

    async def run(self):
        try:
            await self._run()
        except Exception as ex:
            await self.voice_record_repository.update_is_process_error(
                id=self.voice_record_id,
                is_error=True,
            )
            raise ex
        finally:
            if self._remove_dir_on_ready:
                shutil.rmtree(self._remove_dir_on_ready)

    async def _run(self):
        await self._update_status(VoiceProcessStatusEnum.DOWNLOADING_AUDIO)
        downloaded_info = await CraigVoiceDownload(
            record_id=self.craig_record_id,
            key=self.craig_api_key,
        ).execute()
        self._remove_dir_on_ready = downloaded_info.extract_path

        await self._update_status(VoiceProcessStatusEnum.AUDIO_PROCESS)
        merged_audio_paths = await AudioMergeAction(
            voices_paths=[track.track_path for track in downloaded_info.tracks],
            output_dir=downloaded_info.extract_path,
        ).execute()

        await self._update_status(VoiceProcessStatusEnum.AUDIO_TRANSCRIPTION)
        transcribed_text = await self._transcribe_audio(
            downloaded_info,
            merged_audio_paths,
        )
        await self._update_db_instance(
            downloaded_info,
            transcribed_text,
            status=VoiceProcessStatusEnum.COMPLETED,
        )

    async def _update_status(self, new_status: VoiceProcessStatusEnum):
        await self.voice_record_repository.update_process_status(
            id=self.voice_record_id,
            new_status=new_status,
        )

    async def _transcribe_audio(self, downloaded_info: CraigDownloadedVoices, merged_audio_paths: list[str]) -> str:
        transcribed_text = ''
        for audio_path in merged_audio_paths:
            text = await TranscriptAudioAction(
                audio_path=audio_path,
                tracks_info=downloaded_info.tracks,
            ).execute()
            transcribed_text += f'{text}\n'
        return transcribed_text

    async def _update_db_instance(
        self,
        downloaded_info: CraigDownloadedVoices,
        transcribed_text: str,
        status: VoiceProcessStatusEnum,
    ):
        instance = await self.voice_record_repository.get(self.voice_record_id)
        instance.length = downloaded_info.length
        instance.recorded_at = downloaded_info.start_time
        instance.transcribed_text = transcribed_text
        instance.process_status = status
        await self.voice_record_repository.update(instance)


@dramatiq.actor
async def transcribe_craig_audio(craig_record_id: str, craig_api_key: str, voice_record_id: str):
    pipeline = CraigAudioTranscribePipeline(
        craig_record_id=craig_record_id,
        craig_api_key=craig_api_key,
        voice_record_id=voice_record_id,
    )
    await pipeline.run()
