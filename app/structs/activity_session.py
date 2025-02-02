import datetime
from dataclasses import dataclass

from app.structs.enums import ActivitySessionChannelType


@dataclass(kw_only=True)
class ActivitySession:
    id: str | None = None
    user_discord_id: str
    channel_id: str
    channel_type: ActivitySessionChannelType
    start_at: datetime.datetime
    end_at: datetime.datetime | None = None
    last_event_at: datetime.datetime
    microphone_mute_duration: datetime.timedelta = datetime.timedelta(0)
    sound_disabled_duration: datetime.timedelta = datetime.timedelta(0)
    # отслеживание в лайве для подсчета мута
    is_microphone_mute: bool = False
    is_sound_disabled: bool = False
