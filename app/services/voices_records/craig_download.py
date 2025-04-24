import asyncio
import datetime
import io
import os
import tempfile
import zipfile
from dataclasses import dataclass
from typing import ClassVar

import sentry_sdk

from app.services.voices_records.craig_info_parser import (
    CraigVoiceInfo,
    CraigVoiceInfoParser,
    CraigVoiceInfoTrack,
)
from app.services.voices_records.errors import CraigCookTimeout
from core.actions.abstract import AbstractAction
from core.api_clients.craig_bot import CookStatus, CraigBotAPI
from core.logger import logger


@dataclass
class CraigTrack:
    user_name: str
    discord_tag: str
    discord_id: str
    track_path: str


@dataclass
class CraigDownloadedVoices:
    record_id: str
    start_time: datetime.datetime
    length: float | None
    extract_path: str
    tracks: list[CraigTrack]


@dataclass
class CraigVoiceDownload(AbstractAction[CraigDownloadedVoices]):
    record_id: str
    key: str

    SECOND_BETWEEN_AWAITING_COOK: ClassVar[int] = 60
    MAX_RETRIES_TO_WAIT_COOK: ClassVar[int] = 30
    CRAIG_INFO_FILENAME: ClassVar[str] = 'info.txt'

    async def action(self) -> CraigDownloadedVoices:
        zip_file = await self._download_zipfile()
        temp_dir = tempfile.gettempdir()
        extract_path = f'{temp_dir}/{self.record_id}'
        zip_file.extractall(extract_path)

        tracks_paths = [path for path in os.listdir(extract_path) if path.endswith('.flac')]
        track_info = self._load_tracks_info(extract_path)
        craig_tracks = self._match_voice_tracks_with_info(
            extract_path=extract_path,
            voice_tracks_paths=tracks_paths,
            tracks_info=track_info.tracks,
        )

        return CraigDownloadedVoices(
            length=None,
            record_id=track_info.record_id,
            start_time=track_info.start_time,
            extract_path=extract_path,
            tracks=craig_tracks,
        )

    async def _download_zipfile(self) -> zipfile.ZipFile:
        # start treatment
        craig_client = CraigBotAPI(key=self.key)
        await craig_client.start_cook_flac(self.record_id)

        # waiting download
        for _ in range(self.MAX_RETRIES_TO_WAIT_COOK):
            await asyncio.sleep(self.SECOND_BETWEEN_AWAITING_COOK)
            cook = await self._get_cook_when_ready(craig_client)
            if cook:
                break
        else:
            raise CraigCookTimeout(f'Время ожидания ответа для скачивания записи {self.craig_voice_url} истекло')

        # download and get zip
        file_content = await craig_client.download_cook(file_name=cook.download.file)
        return zipfile.ZipFile(io.BytesIO(file_content))

    async def _get_cook_when_ready(self, craig_client: CraigBotAPI) -> CookStatus | None:
        try:
            cook_response = await craig_client.cook(record_id=self.record_id)
            logger.debug('cook_status', cook_response)
        except Exception as exception:
            sentry_sdk.capture_exception(exception)
            return

        if cook_response.ready:
            return cook_response

    def _load_tracks_info(self, extract_path: str) -> CraigVoiceInfo:
        with open(f'{extract_path}/{self.CRAIG_INFO_FILENAME}', 'r') as info:
            info = info.readlines()

        return CraigVoiceInfoParser(info).parse()

    def _match_voice_tracks_with_info(
        self,
        extract_path: str,
        voice_tracks_paths: list[str],
        tracks_info: list[CraigVoiceInfoTrack],
    ) -> list[CraigTrack]:
        craig_tracks: list[CraigTrack] = []
        voice_tracks_paths.sort(key=lambda track: int(track.split('-')[0]))
        for voice_track_path, track_info in zip(voice_tracks_paths, tracks_info):
            voice_track_path: str
            track_info: CraigVoiceInfoTrack

            craig_tracks.append(
                CraigTrack(
                    user_name=track_info.user_name,
                    discord_id=track_info.discord_id,
                    discord_tag=track_info.discord_tag,
                    track_path=f'{extract_path}/{voice_track_path}',
                )
            )

        return craig_tracks
