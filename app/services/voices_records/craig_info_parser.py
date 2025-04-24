import datetime
from dataclasses import dataclass


@dataclass
class CraigVoiceInfoTrack:
    user_name: str
    discord_tag: str
    discord_id: str


@dataclass
class CraigVoiceInfo:
    record_id: str
    start_time: datetime.datetime
    tracks: list[CraigVoiceInfoTrack]


def parse_craig_record_id_and_key(url: str) -> tuple[str, str]:
    url, key = url.split('?key=')
    record_id = url.split('/')[-1]
    return record_id, key


class CraigVoiceInfoParser:
    def __init__(self, raw_info: list[str]) -> None:
        self.raw_info = raw_info

    def parse(self):
        record_id = self._parse_record_id()
        start_time = self._parse_start_time()
        tracks = self._parse_tracks()
        return CraigVoiceInfo(
            record_id=record_id,
            start_time=start_time,
            tracks=tracks,
        )

    def _parse_record_id(self) -> str:
        return self.raw_info[0].removeprefix('Recording ').strip()

    def _parse_start_time(self) -> datetime.datetime:
        raw_time = self.raw_info[5].removeprefix('Start time:').strip()
        return datetime.datetime.fromisoformat(raw_time)

    def _parse_tracks(self) -> list[CraigVoiceInfoTrack]:
        raw_tracks = self.raw_info[8:]
        tracks: list[CraigVoiceInfoTrack] = []
        for raw_track in raw_tracks:
            if not raw_track:
                break

            tracks.append(self._parse_track(raw_track))
        return tracks

    def _parse_track(self, track_raw: str) -> CraigVoiceInfoTrack:
        user_name, raw_discord_tag, raw_discord_id = track_raw.strip().split(' ')

        return CraigVoiceInfoTrack(
            user_name=user_name.strip(),
            discord_tag=raw_discord_tag.strip().removeprefix('(').removesuffix(')'),
            discord_id=raw_discord_id.strip().removeprefix('(').removesuffix(')'),
        )
